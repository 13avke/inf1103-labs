"""
PercentageDiscount Class
INF1103 Lab 9
2605565
"""

from discount_strategy import DiscountStrategy


# Takes a percentage off the total, e.g. PercentageDiscount(10) takes 10% off
class PercentageDiscount(DiscountStrategy):

    # Initializer: the percentage must be between 0 and 100
    def __init__(self, percentage: float):
        if percentage <= 0 or percentage > 100:
            raise ValueError("Percentage must be greater than 0 and at most 100.")
        self.__percentage: float = percentage

    # Getter for the percentage
    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)
