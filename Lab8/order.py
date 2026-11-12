"""
Order Class
INF1103 Lab 8
2605565
"""

from product import Product
from order_line import OrderLine


# A customer order (composition: it creates, owns and removes its own OrderLines)
class Order:

    # Initializer: an order starts with no lines
    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    # Getter for the order ID
    def get_order_id(self) -> str:
        return self.__order_id

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

    # Total of the order, asking each line for its subtotal
    def calculate_total(self) -> float:
        return sum(order_line.calculate_subtotal() for order_line in self.__order_lines)

    # Return a copy of the lines, so outside code can read them but not add, remove or move them
    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)

    # Print every line and the order total
    def display_order(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print("-" * 48)
        if not self.__order_lines:
            print("No items in this order.")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("-" * 48)
        print(f"Total: ${self.calculate_total():.2f}")
