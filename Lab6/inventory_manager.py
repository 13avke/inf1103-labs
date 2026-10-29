"""
Inventory Management System
INF1103 Lab 5
2605565
"""

import json
import os
import sys

# Path to inventory.json, kept in the same folder as this script
INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")


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


# Keep asking until a valid, non-negative number is entered
def get_number(prompt, number_type):
    while True:
        value = input(prompt).strip()
        try:
            number = number_type(value)
        except ValueError:
            print("  ERROR: Please enter a valid number.")
            continue
        if number < 0:
            print("  ERROR: Value cannot be negative.")
            continue
        return number


# Add a new product to the inventory
def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if product_id == "":
        print("\nProduct ID cannot be empty.")
        return
    if search_product(inventory, product_id):
        print(f"\nProduct ID {product_id} already exists.")
        return

    name = input("Product Name: ").strip()
    while name == "":
        name = input("Product Name cannot be empty. Product Name: ").strip()

    price = get_number("Price: ", float)
    stock = get_number("Stock Quantity: ", int)

    inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("\nProduct added successfully!")


# Change the stock quantity of an existing product
def update_stock(inventory):
    print("\nUpdate Stock")
    product = search_product(inventory, input("Enter Product ID: "))
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}\n")
    product["stock"] = get_number("New Stock Quantity: ", int)
    print("\nStock updated successfully!")


# Find a product by its ID, or return None if it doesn't exist
def search_product(inventory, product_id):
    for product in inventory:
        if product["id"] == product_id.strip().upper():
            return product
    return None


# Print the details of a single product
def show_product(product):
    print("\nProduct Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 48)


# Load the inventory from inventory.json, or start empty if it doesn't exist
def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        print("\ninventory.json not found. Starting with an empty inventory.")
        return []

    print("\ninventory.json found.")
    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8-sig") as file:
            inventory = json.load(file)
    except json.JSONDecodeError:
        print("ERROR: inventory.json could not be read. Fix or delete it, then run the program again.")
        sys.exit(1)

    print("Inventory loaded successfully.")
    return inventory


# Save the inventory to inventory.json
def save_inventory(inventory):
    with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(inventory, file, indent=4)


# Program header
print("=" * 40)
print("INVENTORY MANAGEMENT SYSTEM")
print("=" * 40)

# Load the saved inventory
inventory = load_inventory()

# Menu loop, runs until the user picks Exit
while True:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")

    option = input("\nEnter option: ").strip()

    # Run the chosen option
    match option:
        case "1":
            display_all(inventory)
        case "2":
            add_product(inventory)
        case "3":
            update_stock(inventory)
        case "4":
            print("\nSearch Product")
            product = search_product(inventory, input("Enter Product ID: "))
            if product:
                show_product(product)
            else:
                print("\nProduct not found.")
        case "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json.")
        case "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        case _:
            print("\nInvalid option. Please enter a number from 1 to 6.")
