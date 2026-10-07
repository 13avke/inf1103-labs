"""
Inventory Management System
INF1103 Lab 5
2605565
"""

# Starting inventory: each product is a dictionary stored in a list
inventory = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
]


# Display every product in the inventory
def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("No products in inventory.")
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | "
              f"Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("-" * 48)


# Add a new product to the inventory
def add_product(inventory):
    pass


# Change the stock quantity of an existing product
def update_stock(inventory):
    pass


# Find a product by its ID, or return None if it doesn't exist
def search_product(inventory, product_id):
    pass


# Load the inventory from inventory.json, or start empty if it doesn't exist
def load_inventory():
    pass


# Save the inventory to inventory.json
def save_inventory(inventory):
    pass


# Program header
print("=" * 40)
print("INVENTORY MANAGEMENT SYSTEM")
print("=" * 40)

# Show the starting inventory
display_all(inventory)

