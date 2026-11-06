"""
Inventory Class
INF1103 Lab 7
2605565
"""


# A collection of Product objects
class Inventory:

    # Initializer: start with an empty list of products
    def __init__(self):
        self.__products = []

    # Add a product, unless one with the same ID already exists
    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    # Find a product by its ID, or return None if it doesn't exist
    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id.strip().upper():
                return product
        return None

    # Print every product in the inventory
    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print("-" * 48)

    # Return a copy of the product list, so outside code can't change the original
    def get_products(self):
        return list(self.__products)
