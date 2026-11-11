"""
PhysicalProduct Class
INF1103 Lab 8
2605565
"""

from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier

# Shipping rule: a flat base fee plus a charge per kilogram
BASE_SHIPPING_FEE = 5.00
SHIPPING_RATE_PER_KG = 2.00


# A product that is stored and shipped (is-a Product, can-be-shipped)
class PhysicalProduct(Product, CanBeShipped):

    # Initializer: pass the shared details and supplier to Product, then add the weight
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

    # Getter for the weight in kilograms
    def get_weight(self) -> float:
        return self.__weight

    # Override: show the shared details from Product, then the weight
    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    # Implement Product's abstract method
    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    # Implement the CanBeShipped interface
    def calculate_shipping_cost(self) -> float:
        return BASE_SHIPPING_FEE + SHIPPING_RATE_PER_KG * self.__weight
