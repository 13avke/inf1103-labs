"""
Factory Pattern Tests
INF1103 Lab 9
2605565
"""

import inspect
import unittest

import inventory_manager
from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory


class TestProductFactory(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")

    # "physical" gives a PhysicalProduct with its weight
    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 25.00, 10, self.supplier, 1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.get_weight(), 1.5)

    # "digital" gives a DigitalProduct with its download size
    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D001", "Editor", 49.90, 100, self.supplier, 250)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_download_size(), 250)

    # Type names are not case-sensitive and ignore spaces
    def test_type_name_is_normalised(self):
        product = ProductFactory.create(" Physical ", "P002", "Chair", 80.00, 3, self.supplier)
        self.assertIsInstance(product, PhysicalProduct)

    # An unknown type raises a ValueError with a clear message
    def test_unknown_type_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.00, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")

    # The menu program creates products through the factory, not directly
    def test_manager_does_not_create_products_directly(self):
        source = inspect.getsource(inventory_manager)
        self.assertNotIn("PhysicalProduct(", source)
        self.assertNotIn("DigitalProduct(", source)
        self.assertIn("ProductFactory.create(", source)


if __name__ == "__main__":
    unittest.main()
