# Inventory Management System

This is a Python inventory management application built with Flask. It provides REST API endpoints for managing inventory and integrates with the Open Food Facts API to retrieve product information by barcode.

 # Features

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

# Requirements

- Python 3
- pip
- Internet connection for Open Food Facts integration

# Installation

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

