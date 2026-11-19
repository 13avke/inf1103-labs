"""
NoDiscount Class
INF1103 Lab 9
2605565
"""

from discount_strategy import DiscountStrategy


# Default strategy: the total is not changed
class NoDiscount(DiscountStrategy):

    def apply(self, total: float) -> float:
        return total
