"""
StudentDiscount Class
INF1103 Lab 9
2605565
"""

from discount_strategy import DiscountStrategy

# Student discount rate (5% off)
STUDENT_RATE = 0.05


# Fourth strategy, added without changing Order: takes 5% off for students
class StudentDiscount(DiscountStrategy):

    def apply(self, total: float) -> float:
        return total * (1 - STUDENT_RATE)
