"""
Strategy Pattern Tests
INF1103 Lab 9
2605565
"""

import inspect
import unittest

from supplier import Supplier
from physical_product import PhysicalProduct
from order import Order
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from percentage_discount import PercentageDiscount
from bulk_discount import BulkDiscount
from student_discount import StudentDiscount


# A new strategy made only inside the test, to prove Order works with it unchanged
class HalfPriceDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total / 2


class TestDiscountStrategies(unittest.TestCase):

    # Build an order whose lines add up to 250 (10 x 20 + 1 x 50)
    def setUp(self):
        supplier = Supplier("S001", "Test Supplier", "test@example.com")
        self.lamp = PhysicalProduct("P001", "Lamp", 20.00, 50, supplier, 1.0)
        self.chair = PhysicalProduct("P002", "Chair", 50.00, 10, supplier, 5.0)
        self.order = Order("ORD001")
        self.order.add_order_line(self.lamp, 10)
        self.order.add_order_line(self.chair, 1)

    # Each strategy on its own
    def test_no_discount(self):
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225)

    def test_bulk_discount_at_and_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(250), 230)
        self.assertEqual(BulkDiscount(200, 20).apply(200), 180)
        self.assertEqual(BulkDiscount(200, 20).apply(199), 199)

    def test_student_discount(self):
        self.assertAlmostEqual(StudentDiscount().apply(250), 237.5)

    # Order uses NoDiscount when no strategy is given
    def test_order_defaults_to_no_discount(self):
        self.assertIsInstance(self.order.get_discount(), NoDiscount)
        self.assertEqual(self.order.calculate_total(), 250)

    # Order given a strategy when it is created
    def test_order_with_bulk_discount(self):
        order = Order("ORD002", BulkDiscount(200, 20))
        order.add_order_line(self.lamp, 10)
        order.add_order_line(self.chair, 1)
        self.assertEqual(order.calculate_total(), 230)

    # The strategy on an existing order can be swapped with set_discount()
    def test_set_discount_changes_strategy(self):
        self.order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(self.order.calculate_total(), 230)
        self.order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(self.order.calculate_total(), 225)

    # A brand-new strategy works without any change to Order (OCP)
    def test_new_strategy_needs_no_change_to_order(self):
        self.order.set_discount(HalfPriceDiscount())
        self.assertEqual(self.order.calculate_total(), 125)

    # Order has no if/elif logic about discount types
    def test_order_has_no_discount_if_elif(self):
        source = inspect.getsource(Order.calculate_total)
        self.assertNotIn("if", source)
        self.assertNotIn("elif", source)

    # Two orders can share the same strategy object (aggregation, not composition)
    def test_two_orders_share_one_strategy(self):
        shared = PercentageDiscount(10)
        first = Order("ORD003", shared)
        second = Order("ORD004", shared)
        self.assertIs(first.get_discount(), second.get_discount())

    # The abstract base class cannot be created directly
    def test_discount_strategy_is_abstract(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    # Invalid strategy settings are rejected
    def test_invalid_discount_settings(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(0)
        with self.assertRaises(ValueError):
            PercentageDiscount(150)
        with self.assertRaises(ValueError):
            BulkDiscount(200, -5)
        with self.assertRaises(ValueError):
            BulkDiscount(10, 20)


if __name__ == "__main__":
    unittest.main()
