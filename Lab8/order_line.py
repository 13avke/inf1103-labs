"""
OrderLine Class
INF1103 Lab 8
2605565
"""

from product import Product


# One product and quantity within an Order (only ever created by Order)
class OrderLine:

    # Initializer: refer to an existing Product (the line does not own it)
    def __init__(self, product: Product, quantity: int):
        self.__product: Product = product
        self.__quantity: int = quantity

    # Getters: let other code read the attributes without changing them
    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    # Price of this line: the product's price multiplied by the quantity
    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    # Print this line's product, quantity and subtotal
    def display_information(self) -> None:
        print(f"{self.__product.get_name()} x {self.__quantity} "
              f"@ ${self.__product.get_price():.2f} = ${self.calculate_subtotal():.2f}")
