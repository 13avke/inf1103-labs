"""
Inventory Management System
INF1103 Lab 9
2605565
"""

import csv
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
from product_factory import ProductFactory
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from percentage_discount import PercentageDiscount
from bulk_discount import BulkDiscount
from student_discount import StudentDiscount

# Data files are kept in the same folder as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(BASE_DIR, "inventory.json")
PRODUCTS_FILE = "products.csv"


# --- File handling ---

# Turn one saved product back into an object, through the factory
def create_product_from_data(item: dict, suppliers: dict[str, Supplier]) -> Product:
    supplier = suppliers[item["supplier_id"]]
    extra_value = item.get("weight", item.get("download_size", 0.0))
    return ProductFactory.create(item["type"], item["id"], item["name"], item["price"],
                                 item["stock"], supplier, extra_value)


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

    try:
        file = open(INVENTORY_FILE, "r", encoding="utf-8-sig")
    except FileNotFoundError:
        print("\ninventory.json not found. Starting with an empty inventory.")
        return inventory, suppliers

    print("\ninventory.json found.")
    try:
        with file:
            data = json.load(file)
        # Each supplier is created once, so products from the same supplier share one Supplier object
        for item in data["suppliers"]:
            suppliers[item["id"]] = Supplier(item["id"], item["name"], item["contact_email"])
        for item in data["products"]:
            inventory.add_product(create_product_from_data(item, suppliers))
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        # Don't carry on with half-loaded data
        print("ERROR: inventory.json could not be read. Fix or delete it, then run the program again.")
        sys.exit(1)

    print("Inventory loaded successfully.")
    return inventory, suppliers


# Save every supplier and product to inventory.json; returns False if the file can't be written
def save_inventory(inventory: Inventory, suppliers: dict[str, Supplier]) -> bool:
    data = {
        "suppliers": [{"id": supplier.get_supplier_id(), "name": supplier.get_name(),
                       "contact_email": supplier.get_contact_email()}
                      for supplier in suppliers.values()],
        "products": [product_to_data(product) for product in inventory.get_products()],
    }
    try:
        with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except OSError:
        print("ERROR: inventory.json could not be saved. Check the file isn't open or read-only.")
        return False
    return True


# Convert text from the CSV to a number, with a short message the user can understand if it fails
def parse_number(text: str, field: str, number_type: type) -> int | float:
    try:
        return number_type(text)
    except ValueError:
        raise ValueError(f"{field} '{text.strip()}' is not a number") from None


# Read products from a CSV file, create each one through the factory and add it to the inventory
def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="", encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            # Each row gets its own try, so one bad row is skipped and loading carries on
            for row_number, row in enumerate(reader, start=2):
                if not row:
                    continue  # ignore blank lines
                try:
                    if len(row) != 5:
                        raise ValueError(f"expected 5 values, found {len(row)}")
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(product_type, product_id.strip().upper(), name.strip(),
                                                    parse_number(price, "price", float),
                                                    parse_number(stock, "stock", int), supplier)
                except ValueError as error:
                    print(f"Row {row_number} skipped: {error}")
                    continue
                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Row {row_number} skipped: product {product.get_product_id()} already exists.")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


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


# Keep asking until a number greater than zero is entered (e.g. a price)
def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


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


# Let the user pick a discount strategy for an order (Order itself never sees this choice)
def choose_discount() -> DiscountStrategy:
    while True:
        print("\nDiscount: 1 = None, 2 = 10% off, 3 = $20 off orders of $200+, 4 = Student (5% off)")
        match input("Choose discount: ").strip():
            case "1":
                return NoDiscount()
            case "2":
                return PercentageDiscount(10)
            case "3":
                return BulkDiscount(200, 20)
            case "4":
                return StudentDiscount()
            case _:
                print("  ERROR: Please enter 1, 2, 3 or 4.")


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
    price = get_positive_float("Price: ")
    stock = get_number("Stock Quantity: ", int)
    supplier = choose_supplier(suppliers)

    # Ask which type of product this is, then for that type's extra detail
    while True:
        match input("Product Type (1 = Physical, 2 = Digital): ").strip():
            case "1":
                product_type = "physical"
                extra_value = get_positive_float("Weight (kg): ")
                break
            case "2":
                product_type = "digital"
                extra_value = get_positive_float("Download Size (MB): ")
                break
            case _:
                print("  ERROR: Please enter 1 or 2.")

    # The factory decides which class to create
    product = ProductFactory.create(product_type, product_id, name, price, stock, supplier, extra_value)
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


# Build an order from products in the inventory, pick a discount and show the total
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
        # OrderLine validates the quantity; if it's rejected, ask again
        try:
            order.add_order_line(product, quantity)
        except ValueError as error:
            print(f"  ERROR: {error}")
            continue
        print(f"Added {product.get_name()} x {quantity}.")

    # An order must have at least one line (1..* in the UML diagram)
    if len(order.get_order_lines()) == 0:
        print("\nOrder cancelled: an order needs at least one item.")
        return

    order.set_discount(choose_discount())
    order.display_order()


# Load products from a CSV file into the inventory, all from one supplier
def load_products_menu(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nLoad Products from CSV")
    file_name = input(f"CSV file name (press Enter for {PRODUCTS_FILE}): ").strip()
    if file_name == "":
        file_name = PRODUCTS_FILE
    supplier = choose_supplier(suppliers)
    print()
    load_products(os.path.join(BASE_DIR, file_name), inventory, supplier)


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
        print("7. Load Products from CSV")
        print("8. Save Inventory")
        print("9. Exit")
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
                load_products_menu(inventory, suppliers)
            case "8":
                print("\nSaving inventory...")
                if save_inventory(inventory, suppliers):
                    print("Inventory saved successfully to inventory.json.")
            case "9":
                print("\nSaving inventory before exit...")
                if save_inventory(inventory, suppliers):
                    print("Inventory saved successfully.")
                print("\nThank you for using Inventory Management System.")
                print("Program terminated.")
                break
            case _:
                print("\nInvalid option. Please enter a number from 1 to 9.")


if __name__ == "__main__":
    main()
