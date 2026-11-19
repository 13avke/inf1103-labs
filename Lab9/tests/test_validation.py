"""
Validation Tests
INF1103 Lab 9
2605565
"""

import unittest

from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order import Order


class TestValidation(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")

    # Price must be greater than zero (for both subclasses, LSP)
    def test_price_must_be_positive(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("P001", "Lamp", 0, 10, self.supplier, 1.0)
        with self.assertRaises(ValueError):
            DigitalProduct("D001", "Editor", -5, 10, self.supplier, 100)

    # Stock cannot be negative when created or updated
    def test_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("P001", "Lamp", 25.00, -1, self.supplier, 1.0)
        product = DigitalProduct("D001", "Editor", 49.90, 10, self.supplier, 100)
        with self.assertRaises(ValueError):
            product.update_stock(-3)
        self.assertEqual(product.get_stock(), 10)

    # Zero stock is allowed
    def test_zero_stock_is_allowed(self):
        product = PhysicalProduct("P001", "Lamp", 25.00, 0, self.supplier, 1.0)
        self.assertEqual(product.get_stock(), 0)

    # OrderLine quantity must be greater than zero, and a rejected line is not added
    def test_order_line_quantity_must_be_positive(self):
        product = PhysicalProduct("P001", "Lamp", 25.00, 10, self.supplier, 1.0)
        order = Order("ORD001")
        with self.assertRaises(ValueError) as context:
            order.add_order_line(product, 0)
        self.assertEqual(str(context.exception), "Quantity must be greater than zero.")
        with self.assertRaises(ValueError):
            order.add_order_line(product, -2)
        self.assertEqual(len(order.get_order_lines()), 0)


if __name__ == "__main__":
    unittest.main()
