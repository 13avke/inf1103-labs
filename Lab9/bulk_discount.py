"""
BulkDiscount Class
INF1103 Lab 9
2605565
"""

from discount_strategy import DiscountStrategy


# Takes a fixed amount off any total at or above a threshold, e.g. BulkDiscount(200, 20)
class BulkDiscount(DiscountStrategy):

    # Initializer: threshold and amount must be positive, and the amount can't exceed the threshold
    def __init__(self, threshold: float, amount: float):
        if threshold <= 0 or amount <= 0:
            raise ValueError("Threshold and amount must be greater than zero.")
        if amount > threshold:
            raise ValueError("Discount amount cannot be more than the threshold.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    # Getters for the threshold and amount
    def get_threshold(self) -> float:
        return self.__threshold

    def get_amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total
