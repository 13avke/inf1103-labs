"""
ProductFactory Class
INF1103 Lab 9
2605565
"""

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


# Factory: the one place that decides which Product subclass to create
class ProductFactory:

    # Create a product from its type name; extra_value is the weight (physical) or download size (digital)
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, extra_value: float = 0.0) -> Product:
        match product_type.strip().lower():
            case "physical":
                return PhysicalProduct(product_id, name, price, stock, supplier, extra_value)
            case "digital":
                return DigitalProduct(product_id, name, price, stock, supplier, extra_value)
            case _:
                raise ValueError(f"Unknown product type: {product_type}")
