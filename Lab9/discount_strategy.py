"""
DiscountStrategy Class
INF1103 Lab 9
2605565
"""

from abc import ABC, abstractmethod


# Strategy interface: every discount takes an order total and returns the discounted total
class DiscountStrategy(ABC):

    @abstractmethod
    def apply(self, total: float) -> float:
        pass
