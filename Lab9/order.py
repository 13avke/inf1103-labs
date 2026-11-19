"""
Order Class
INF1103 Lab 9
2605565
"""

from product import Product
from order_line import OrderLine
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount


# A customer order (composition: it creates, owns and removes its own OrderLines)
class Order:

    # Initializer: an order starts with no lines and uses the discount it is given (NoDiscount if none)
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    # Getters for the order ID and the current discount
    def get_order_id(self) -> str:
        return self.__order_id

    def get_discount(self) -> DiscountStrategy:
        return self.__discount

    # Swap the discount strategy (Order doesn't need to know which one it is)
    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    # Create a new OrderLine inside this order (lines are never passed in from outside)
    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    # Remove the line for a product; the line goes, the Product itself is untouched
    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id.strip().upper():
                self.__order_lines.remove(order_line)
                return True
        return False

    # Total before discount, asking each line for its subtotal
    def calculate_subtotal(self) -> float:
        return sum(order_line.calculate_subtotal() for order_line in self.__order_lines)

    # Total after discount: the strategy decides how much comes off
    def calculate_total(self) -> float:
        return self.__discount.apply(self.calculate_subtotal())

    # Return a copy of the lines, so outside code can read them but not add, remove or move them
    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)

    # Print every line, the subtotal, the discount used and the final total
    def display_order(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print("-" * 48)
        if not self.__order_lines:
            print("No items in this order.")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("-" * 48)
        print(f"Subtotal: ${self.calculate_subtotal():.2f}")
        print(f"Discount: {type(self.__discount).__name__}")
        print(f"Total: ${self.calculate_total():.2f}")
