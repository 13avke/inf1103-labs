"""
Lab 7 Tests
INF1103 Lab 7
2605565
"""

import json
import os
import tempfile

import inventory_manager as manager
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory


# Physical products store their weight and can calculate shipping
def test_physical_product():
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.0)
    assert laptop.get_weight() == 2.0
    assert "shipping" in laptop.get_fulfilment_info()
    assert isinstance(laptop, CanBeShipped)
    assert laptop.calculate_shipping_cost() == 9.00
    heavy = PhysicalProduct("P002", "Table", 500.00, 3, 15.0)
    assert heavy.calculate_shipping_cost() == 35.00


# Digital products store their download size and don't need shipping
def test_digital_product():
    ebook = DigitalProduct("D001", "E-book", 12.50, 200, 8.5)
    assert ebook.get_download_size() == 8.5
    assert "digitally" in ebook.get_fulfilment_info()
    assert not isinstance(ebook, CanBeShipped)


# Product is abstract, so creating one directly must fail
def test_product_is_abstract():
    try:
        Product("X001", "Generic", 1.00, 1)
    except TypeError as error:
        print(f"  Product() correctly refused: {error}")
        return
    raise AssertionError("Product should not be instantiable")


# Inventory operations still work with both product types
def test_inventory_operations():
    inventory = Inventory()
    assert inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.0))
    assert inventory.add_product(DigitalProduct("D001", "E-book", 12.50, 200, 8.5))
    assert not inventory.add_product(DigitalProduct("D001", "Duplicate", 1.00, 1, 1.0))
    found = inventory.search_product("d001")
    assert found.get_name() == "E-book"
    found.update_stock(150)
    assert inventory.search_product("D001").get_stock() == 150
    assert inventory.search_product("ZZZ") is None


# Saving then loading keeps each product's type and extra attribute
def test_json_round_trip():
    original_file = manager.INVENTORY_FILE
    with tempfile.TemporaryDirectory() as folder:
        manager.INVENTORY_FILE = os.path.join(folder, "inventory.json")
        inventory = Inventory()
        inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.0))
        inventory.add_product(DigitalProduct("D001", "E-book", 12.50, 200, 8.5))
        manager.save_inventory(inventory)

        with open(manager.INVENTORY_FILE) as file:
            saved = json.load(file)
        assert [item["type"] for item in saved] == ["physical", "digital"]

        loaded = manager.load_inventory()
        laptop = loaded.search_product("P001")
        ebook = loaded.search_product("D001")
        assert isinstance(laptop, PhysicalProduct) and laptop.get_weight() == 2.0
        assert isinstance(ebook, DigitalProduct) and ebook.get_download_size() == 8.5
    manager.INVENTORY_FILE = original_file


# Run every test and report the results
if __name__ == "__main__":
    tests = [test_physical_product, test_digital_product, test_product_is_abstract,
             test_inventory_operations, test_json_round_trip]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print(f"\nAll {len(tests)} tests passed.")
