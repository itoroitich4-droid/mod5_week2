# Inventory Management System

A Python inventory management application built with Flask. It provides REST API endpoints for managing inventory and integrates with the Open Food Facts API to retrieve product information by barcode.

## Features

- View all inventory items.
- Retrieve an item by ID.
- Add new inventory items.
- Update inventory items.
- Delete inventory items.
- Search Open Food Facts by barcode.
- Search products by name.
- Import external product information into local inventory.
- Manage inventory through a command-line interface (CLI).
- Automated tests using pytest and mocked external API responses.

## Requirements

- Python 3
- pip
- Internet connection for Open Food Facts integration

## Installation

Clone or download this project, then navigate into its directory.

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the application

Start the Flask server:

```bash
python3 app.py
```

The API runs at `http://127.0.0.1:5000`.

Keep the server running while using the CLI.

In another terminal, activate the virtual environment, navigate to the project directory, and run:

```bash
python3 cli.py
```

Follow the menu instructions.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/inventory` | List all inventory items |
| GET | `/inventory/<item_id>` | Retrieve an item by ID |
| POST | `/inventory` | Add an item |
| PATCH | `/inventory/<item_id>` | Update an item |
| DELETE | `/inventory/<item_id>` | Delete an item |
| GET | `/inventory/search/<barcode>` | Search Open Food Facts by barcode |
| GET | `/inventory/search/name/<name>` | Search Open Food Facts by name |
| POST | `/inventory/import/<barcode>` | Import a product by barcode |

### Example: Add an inventory item

```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"name":"Rice","brand":"Pishori","price":180,"stock":30,"barcode":"4567890123456"}'
```

### Example: Search by barcode

```bash
curl http://127.0.0.1:5000/inventory/search/3017620422003
```

### Example: Import a product

```bash
curl -X POST http://127.0.0.1:5000/inventory/import/3017620422003
```

Imported products initially have a price of `0.0` and stock of `0`; these values can be updated later.

## Running tests

With the virtual environment activated, run:

```bash
python3 -m pytest -v
```

The tests cover CRUD operations, error responses, and mocked Open Food Facts barcode searches.

## Data storage

Inventory is currently stored in a Python list in memory. Data resets when the Flask server restarts. A persistent database can be added in a future version.

## External API

Product information is retrieved from [Open Food Facts](https://world.openfoodfacts.org/). External requests may fail when the service is unavailable or rate-limits requests.
