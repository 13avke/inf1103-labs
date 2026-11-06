"""
CanBeShipped Interface
INF1103 Lab 7
2605565
"""

from abc import ABC, abstractmethod


# Interface: any class that signs this contract must be able to work out a shipping cost
class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        pass
