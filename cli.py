
import requests

API_URL = "http://127.0.0.1:5000"


def view_inventory():
    response = requests.get(f"{API_URL}/inventory")
    print(response.status_code)
    print(response.json())


def add_item():
    name = input("Product name: ")
    brand = input("Brand: ")
    price = float(input("Price: "))
    stock = int(input("Stock quantity: "))
    barcode = input("Barcode: ")

    item = {
        "name": name,
        "brand": brand,
        "price": price,
        "stock": stock,
        "barcode": barcode
    }

    response = requests.post(f"{API_URL}/inventory", json=item)
    print(response.status_code)
    print(response.json())


def update_item():
    item_id = input("Item ID to update: ")
    stock = input("New stock quantity: ")

    response = requests.patch(
        f"{API_URL}/inventory/{item_id}",
        json={"stock": int(stock)}
    )
    print(response.status_code)
    print(response.json())


def delete_item():
    item_id = input("Item ID to delete: ")

    response = requests.delete(f"{API_URL}/inventory/{item_id}")
    print(response.status_code)
    print(response.json())


def search_barcode():
    barcode = input("Barcode to search: ")

    response = requests.get(f"{API_URL}/inventory/search/{barcode}")
    print(response.status_code)
    print(response.json())


def import_product():
    barcode = input("Barcode to import from Open Food Facts: ")

    response = requests.post(f"{API_URL}/inventory/import/{barcode}")
    print(response.status_code)
    print(response.json())


def main():
    while True:
        print("\n=== Inventory Management ===")
        print("1. View inventory")
        print("2. Add item")
        print("3. Update item stock")
        print("4. Delete item")
        print("5. Search product by barcode")
        print("6. Import product by barcode")
        print("0. Exit")

        choice = input("Choose an option: ")

        try:
            if choice == "1":
                view_inventory()
            elif choice == "2":
                add_item()
            elif choice == "3":
                update_item()
            elif choice == "4":
                delete_item()
            elif choice == "5":
                search_barcode()
            elif choice == "6":
                import_product()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
        except requests.RequestException as error:
            print("Could not connect to the Flask API:", error)
        except (ValueError, KeyError) as error:
            print("Invalid input or response:", error)


if __name__ == "__main__":
    main()
