"""
Product Class
INF1103 Lab 7
2605565
"""

from abc import ABC, abstractmethod


# Abstract base class for every product (cannot be created directly)
class Product(ABC):

    # Initializer: set up the attributes every product shares
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # Getters: let other code read the attributes without changing them
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    # Change the stock, rejecting negative values
    def update_stock(self, quantity):
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    # Print the details every product shares on one line
    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    # Every subclass must say how the product reaches the customer
    @abstractmethod
    def get_fulfilment_info(self):
        pass
