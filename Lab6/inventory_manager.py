"""
Inventory Management System
INF1103 Lab 6
2605565
"""

import json
import os
import sys

from product import Product
from inventory import Inventory

# Path to inventory.json
INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")


# --- File handling ---

# Load products from inventory.json into an Inventory object
def load_inventory():
    inventory = Inventory()

    if not os.path.exists(INVENTORY_FILE):
        print("\ninventory.json not found. Starting with an empty inventory.")
        return inventory

    print("\ninventory.json found.")
    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8-sig") as file:
            data = json.load(file)
        for item in data:
            inventory.add_product(Product(item["id"], item["name"], item["price"], item["stock"]))
    except (json.JSONDecodeError, KeyError, TypeError):
        print("ERROR: inventory.json could not be read. Fix or delete it, then run the program again.")
        sys.exit(1)

    print("Inventory loaded successfully.")
    return inventory


# Save every product in the Inventory object to inventory.json
def save_inventory(inventory):
    data = []
    for product in inventory.get_products():
        data.append({
            "id": product.get_product_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
        })
    with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# --- User input ---

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


# Ask for a new product's details and add it to the inventory
def add_product_menu(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if product_id == "":
        print("\nProduct ID cannot be empty.")
        return
    if inventory.search_product(product_id) is not None:
        print(f"\nProduct ID {product_id} already exists.")
        return

    name = input("Product Name: ").strip()
    while name == "":
        name = input("Product Name cannot be empty. Product Name: ").strip()

    price = get_number("Price: ", float)
    stock = get_number("Stock Quantity: ", int)

    inventory.add_product(Product(product_id, name, price, stock))
    print("\nProduct added successfully!")


# Ask for a product ID and a new stock quantity
def update_stock_menu(inventory):
    print("\nUpdate Stock")
    product = inventory.search_product(input("Enter Product ID: "))
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}\n")
    product.update_stock(get_number("New Stock Quantity: ", int))
    print("\nStock updated successfully!")


# Ask for a product ID and show the product if it exists
def search_product_menu(inventory):
    print("\nSearch Product")
    product = inventory.search_product(input("Enter Product ID: "))
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    product.display_information()
    print("-" * 48)


# --- Main program ---

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
            inventory.display_all()
        case "2":
            add_product_menu(inventory)
        case "3":
            update_stock_menu(inventory)
        case "4":
            search_product_menu(inventory)
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
