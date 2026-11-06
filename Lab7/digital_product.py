"""
DigitalProduct Class
INF1103 Lab 7
2605565
"""

from product import Product


# A product that is delivered by download (is-a Product, not shippable)
class DigitalProduct(Product):

    # Initializer: reuse Product's initializer, then add the download size
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    # Getter for the download size in megabytes
    def get_download_size(self):
        return self.__download_size

    # Override: show the shared details from Product, then the download size
    def display_information(self):
        super().display_information()
        print(f"    Type: Digital | Download Size: {self.__download_size:.1f} MB")

    # Implement Product's abstract method
    def get_fulfilment_info(self):
        return "This product is delivered digitally via download."
