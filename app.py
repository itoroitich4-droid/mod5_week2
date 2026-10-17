from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

inventory = [
    {
        "id": 1,
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 350.0,
        "stock": 20,
        "barcode": "1234567890123"
    },
    {
        "id": 2,
        "name": "Oats",
        "brand": "Quaker",
        "price": 250.0,
        "stock": 15,
        "barcode": "9876543210987"
    }
]

next_id = 3

def search_openfoodfacts(barcode):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"

    try:
        response = requests.get(url,headers={"User-Agent": "MoringaInventoryApp/1.0"},timeout=10)
        response.raise_for_status()
        result = response.json()

        if result.get("status") != 1:
            return None

        product = result.get("product", {})

        return {
            "name": product.get("product_name", "Unknown"),
            "brand": product.get("brands", "Unknown"),
            "ingredients": product.get("ingredients_text", ""),
            "barcode": barcode
        }

    except requests.RequestException:
        return None



def search_openfoodfacts_by_name(name):
    url = "https://world.openfoodfacts.org/api/v2/search"

    params = {
        "categories_tags": "",
        "search_terms": name,
        "fields": "product_name,brands,code,ingredients_text",
        "page_size": 5
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers={"User-Agent": "MoringaInventoryApp/1.0"},
            timeout=15
        )
        response.raise_for_status()
        result = response.json()

        products = []

        for product in result.get("products", []):
            products.append({
                "name": product.get("product_name", "Unknown"),
                "brand": product.get("brands", "Unknown"),
                "barcode": product.get("code", ""),
                "ingredients": product.get("ingredients_text", "")
            })

        return products

    except (requests.RequestException, ValueError):
        return None




@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item), 200

    return jsonify({"error": "Item not found"}), 404

@app.route("/inventory", methods=["POST"])
def add_item():
    global next_id

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must contain JSON"}), 400

    required_fields = ["name", "brand", "price", "stock", "barcode"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    item = {
        "id": next_id,
        "name": data["name"],
        "brand": data["brand"],
        "price": data["price"],
        "stock": data["stock"],
        "barcode": data["barcode"]
    }

    inventory.append(item)
    next_id += 1

    return jsonify(item), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must contain JSON"}), 400

    allowed_fields = ["name", "brand", "price", "stock", "barcode"]

    for item in inventory:
        if item["id"] == item_id:
            for field in data:
                if field in allowed_fields:
                    item[field] = data[field]

            return jsonify(item), 200

    return jsonify({"error": "Item not found"}), 404

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            return jsonify({"message": "Item deleted successfully"}), 200

    return jsonify({"error": "Item not found"}), 404

@app.route("/inventory/search/<barcode>", methods=["GET"])
def search_product(barcode):
    product = search_openfoodfacts(barcode)

    if product is None:
        return jsonify({"error": "Product not found or external API unavailable"}), 404

    return jsonify(product), 200


@app.route("/inventory/search/name/<path:name>", methods=["GET"])
def search_product_by_name(name):
    products = search_openfoodfacts_by_name(name)

    if products is None:
        return jsonify({"error": "External API unavailable"}), 502

    if not products:
        return jsonify({"error": "No products found"}), 404

    return jsonify(products), 200


@app.route("/inventory/import/<barcode>", methods=["POST"])
def import_product(barcode):
    global next_id

    product = search_openfoodfacts(barcode)

    if product is None:
        return jsonify({
            "error": "Product not found or external API unavailable"
        }), 502

    item = {
        "id": next_id,
        "name": product["name"],
        "brand": product["brand"],
        "price": 0.0,
        "stock": 0,
        "barcode": product["barcode"]
    }

    inventory.append(item)
    next_id += 1

    return jsonify(item), 201

if __name__ == "__main__":
    app.run(debug=True)