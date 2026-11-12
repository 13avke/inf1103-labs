"""
Inventory Management System
INF1103 Lab 8
2605565
"""

import json
import os
import sys

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from order import Order

# Path to inventory.json, kept in the same folder as this script
INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")


# --- File handling ---

# Create the right Product subclass from one saved product, linked to its Supplier object
def create_product_from_data(item: dict, suppliers: dict[str, Supplier]) -> Product:
    supplier = suppliers[item["supplier_id"]]
    match item["type"]:
        case "physical":
            return PhysicalProduct(item["id"], item["name"], item["price"], item["stock"],
                                   supplier, item["weight"])
        case "digital":
            return DigitalProduct(item["id"], item["name"], item["price"], item["stock"],
                                  supplier, item["download_size"])
        case _:
            raise ValueError(f"Unknown product type: {item['type']}")


# Turn one product into a dictionary for JSON, storing its supplier by ID
def product_to_data(product: Product) -> dict:
    data = {"type": "", "id": product.get_product_id(), "name": product.get_name(),
            "price": product.get_price(), "stock": product.get_stock(),
            "supplier_id": product.get_supplier().get_supplier_id()}
    if isinstance(product, PhysicalProduct):
        data["type"] = "physical"
        data["weight"] = product.get_weight()
    elif isinstance(product, DigitalProduct):
        data["type"] = "digital"
        data["download_size"] = product.get_download_size()
    return data


# Load suppliers and products from inventory.json
def load_inventory() -> tuple[Inventory, dict[str, Supplier]]:
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}

    if not os.path.exists(INVENTORY_FILE):
        print("\ninventory.json not found. Starting with an empty inventory.")
        return inventory, suppliers

    print("\ninventory.json found.")
    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8-sig") as file:
            data = json.load(file)
        # Each supplier is created once, so products from the same supplier share one Supplier object
        for item in data["suppliers"]:
            suppliers[item["id"]] = Supplier(item["id"], item["name"], item["contact_email"])
        for item in data["products"]:
            inventory.add_product(create_product_from_data(item, suppliers))
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("ERROR: inventory.json could not be read. Fix or delete it, then run the program again.")
        sys.exit(1)

    print("Inventory loaded successfully.")
    return inventory, suppliers


# Save every supplier and product to inventory.json
def save_inventory(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    data = {
        "suppliers": [{"id": supplier.get_supplier_id(), "name": supplier.get_name(),
                       "contact_email": supplier.get_contact_email()}
                      for supplier in suppliers.values()],
        "products": [product_to_data(product) for product in inventory.get_products()],
    }
    with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# --- User input ---

# Keep asking until a valid, non-negative number is entered
def get_number(prompt: str, number_type: type) -> int | float:
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


# Keep asking until some text is entered
def get_text(prompt: str) -> str:
    text = input(prompt).strip()
    while text == "":
        text = input(f"Cannot be empty. {prompt}").strip()
    return text


# Choose an existing supplier, or create a new one
def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier:
    print("\nSuppliers:")
    for supplier in suppliers.values():
        supplier.display_information()
    supplier_id = input("Supplier ID (or press Enter to add a new supplier): ").strip().upper()

    if supplier_id in suppliers:
        return suppliers[supplier_id]

    if supplier_id == "":
        supplier_id = get_text("New Supplier ID: ").upper()
    else:
        print(f"Supplier {supplier_id} not found. Adding it as a new supplier.")
    supplier = Supplier(supplier_id, get_text("Supplier Name: "), get_text("Contact Email: "))
    suppliers[supplier_id] = supplier
    return supplier


# --- Menu actions ---

# Ask for a new product's details and add it to the inventory
def add_product_menu(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if product_id == "":
        print("\nProduct ID cannot be empty.")
        return
    if inventory.find_product(product_id) is not None:
        print(f"\nProduct ID {product_id} already exists.")
        return

    name = get_text("Product Name: ")
    price = get_number("Price: ", float)
    stock = get_number("Stock Quantity: ", int)
    supplier = choose_supplier(suppliers)

    # Ask which type of product this is, then for that type's extra detail
    while True:
        product_type = input("Product Type (1 = Physical, 2 = Digital): ").strip()
        match product_type:
            case "1":
                weight = get_number("Weight (kg): ", float)
                product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
                break
            case "2":
                download_size = get_number("Download Size (MB): ", float)
                product = DigitalProduct(product_id, name, price, stock, supplier, download_size)
                break
            case _:
                print("  ERROR: Please enter 1 or 2.")

    inventory.add_product(product)
    print("\nProduct added successfully!")


# Ask for a product ID and a new stock quantity
def update_stock_menu(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product = inventory.find_product(input("Enter Product ID: "))
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}\n")
    product.update_stock(get_number("New Stock Quantity: ", int))
    print("\nStock updated successfully!")


# Ask for a product ID and show the product, its supplier and how it is delivered
def search_product_menu(inventory: Inventory) -> None:
    print("\nSearch Product")
    product = inventory.find_product(input("Enter Product ID: "))
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    product.display_information()
    product.get_supplier().display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("-" * 48)


# Remove a product from the inventory (the product object itself is not destroyed)
def remove_product_menu(inventory: Inventory) -> None:
    print("\nRemove Product")
    product = inventory.remove_product(input("Enter Product ID: "))
    if product is None:
        print("\nProduct not found.")
        return
    print(f"\n{product.get_name()} removed from the inventory.")


# Build an order from products in the inventory and show its total
def create_order_menu(inventory: Inventory, order_number: int) -> None:
    order = Order(f"ORD{order_number:03d}")
    print(f"\nCreate Order {order.get_order_id()}")
    print("Enter a Product ID, or press Enter when the order is complete.")

    while True:
        product_id = input("\nProduct ID: ").strip()
        if product_id == "":
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        quantity = get_number("Quantity: ", int)
        if quantity == 0:
            print("Quantity must be at least 1.")
            continue
        order.add_order_line(product, quantity)
        print(f"Added {product.get_name()} x {quantity}.")

    # An order must have at least one line (1..* in the UML diagram)
    if len(order.get_order_lines()) == 0:
        print("\nOrder cancelled: an order needs at least one item.")
        return

    order.display_order()


# --- Main program ---

# Run the menu until the user picks Exit
def main() -> None:
    # Program header
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    # Load the saved inventory and suppliers
    inventory, suppliers = load_inventory()
    order_count = 0

    # Menu loop, runs until the user picks Exit
    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Remove Product")
        print("6. Create Order")
        print("7. Save Inventory")
        print("8. Exit")
        print("----------------------------")

        option = input("\nEnter option: ").strip()

        # Run the chosen option
        match option:
            case "1":
                inventory.display_all()
            case "2":
                add_product_menu(inventory, suppliers)
            case "3":
                update_stock_menu(inventory)
            case "4":
                search_product_menu(inventory)
            case "5":
                remove_product_menu(inventory)
            case "6":
                order_count += 1
                create_order_menu(inventory, order_count)
            case "7":
                print("\nSaving inventory...")
                save_inventory(inventory, suppliers)
                print("Inventory saved successfully to inventory.json.")
            case "8":
                print("\nSaving inventory before exit...")
                save_inventory(inventory, suppliers)
                print("Inventory saved successfully.")
                print("\nThank you for using Inventory Management System.")
                print("Program terminated.")
                break
            case _:
                print("\nInvalid option. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
