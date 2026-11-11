"""
Inventory Class
INF1103 Lab 8
2605565
"""

from product import Product


# A collection of Product objects (aggregation: products exist independently of the inventory)
class Inventory:

    # Initializer: start with an empty collection of Product references
    def __init__(self):
        self.__products: list[Product] = []

    # Add an existing product, unless one with the same ID is already here
    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    # Remove a product's reference and hand the product back (it is not destroyed)
    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    # Find a product by its ID, or return None if it isn't here
    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id.strip().upper():
                return product
        return None

    # Print every product; each object runs its own display_information()
    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print("-" * 48)

    # Return a copy of the product list, so outside code can't change the original
    def get_products(self) -> list[Product]:
        return list(self.__products)
