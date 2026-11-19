"""
Exception Handling Tests
INF1103 Lab 9
2605565
"""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from supplier import Supplier
from inventory import Inventory
from inventory_manager import get_positive_float, load_products

# Same rows as the lab's products.csv
CSV_ROWS = (
    "product_type,product_id,name,price,stock_quantity\n"
    "physical,P001,Desk Lamp,25.00,10\n"
    "digital,D001,Photo Editor,49.90,100\n"
    "service,S001,Installation,30.00,5\n"
    "physical,P002,Office Chair,abc,3\n"
    "physical,P003,Monitor Stand,39.50,7\n"
)


class TestUserInput(unittest.TestCase):

    # abc, then -5, then 12.50: asks again twice, then returns 12.5
    def test_get_positive_float_asks_again(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), redirect_stdout(output):
            value = get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])


class TestLoadProducts(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")
        self.inventory = Inventory()
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "products.csv")

    def tearDown(self):
        self.folder.cleanup()

    # Run load_products and return what it printed
    def run_load(self, path: str) -> list[str]:
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(path, self.inventory, self.supplier)
        return output.getvalue().splitlines()

    # Bad rows are reported and skipped; valid rows still load
    def test_bad_rows_skipped_and_valid_rows_load(self):
        with open(self.path, "w", newline="") as file:
            file.write(CSV_ROWS)
        lines = self.run_load(self.path)
        self.assertEqual(lines, [
            "Row 4 skipped: Unknown product type: service",
            "Row 5 skipped: price 'abc' is not a number",
            "3 products loaded.",
            "Load attempt finished.",
        ])
        ids = [product.get_product_id() for product in self.inventory.get_products()]
        self.assertEqual(ids, ["P001", "D001", "P003"])

    # Short rows and bad stock values get a clear message too
    def test_short_row_and_bad_stock(self):
        with open(self.path, "w", newline="") as file:
            file.write("product_type,product_id,name,price,stock_quantity\n"
                       "physical,P001,Desk Lamp\n"
                       "digital,D001,Photo Editor,49.90,lots\n")
        lines = self.run_load(self.path)
        self.assertEqual(lines[:2], [
            "Row 2 skipped: expected 5 values, found 3",
            "Row 3 skipped: stock 'lots' is not a number",
        ])

    # A missing file is handled without crashing (except and finally run, else does not)
    def test_missing_file_handled(self):
        missing = os.path.join(self.folder.name, "missing.csv")
        lines = self.run_load(missing)
        self.assertEqual(lines, [f"Products file not found: {missing}", "Load attempt finished."])
        self.assertEqual(self.inventory.get_products(), [])

    # Loading the same file twice doesn't add duplicates
    def test_duplicate_ids_skipped(self):
        with open(self.path, "w", newline="") as file:
            file.write(CSV_ROWS)
        self.run_load(self.path)
        lines = self.run_load(self.path)
        self.assertIn("0 products loaded.", lines)
        self.assertEqual(len(self.inventory.get_products()), 3)


if __name__ == "__main__":
    unittest.main()
