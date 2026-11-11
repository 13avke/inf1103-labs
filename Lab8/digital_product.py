"""
DigitalProduct Class
INF1103 Lab 8
2605565
"""

from product import Product
from supplier import Supplier


# A product that is delivered by download (is-a Product, not shippable)
class DigitalProduct(Product):

    # Initializer: pass the shared details and supplier to Product, then add the download size
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size

    # Getter for the download size in megabytes
    def get_download_size(self) -> float:
        return self.__download_size

    # Override: show the shared details from Product, then the download size
    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Digital | Download Size: {self.__download_size:.1f} MB")

    # Implement Product's abstract method
    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally via download."
