"""
Product Class
INF1103 Lab 8
2605565
"""

from abc import ABC, abstractmethod

from supplier import Supplier


# Abstract base class for every product (cannot be created directly)
class Product(ABC):

    # Initializer: set up the shared attributes, including a reference to an existing Supplier
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier):
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    # Getters: let other code read the attributes without changing them
    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    # Change the stock, rejecting negative values (same rule for every subclass)
    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    # Print the details every product shares on one line
    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock} | "
              f"Supplier: {self.__supplier.get_name()}")

    # Every subclass must say how the product reaches the customer
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass
