from discount import DiscountStrategy, NoDiscount
from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        # Validation: the OrderLine owns the quantity rule, so it checks it.
        if type(quantity) is not int:
            raise ValueError("Quantity must be a whole number.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(
            f"{self.__product.get_name()} x {self.__quantity}: "
            f"${self.calculate_subtotal():.2f}"
        )


class Order:
    def __init__(
        self, order_id: str, discount: DiscountStrategy | None = None
    ) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        # Strategy pattern: Order is given its discount instead of deciding it.
        self.__discount: DiscountStrategy = (
            discount if discount is not None else NoDiscount()
        )

    def get_order_id(self) -> str:
        return self.__order_id

    def get_discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        # Composition: the Order creates its own OrderLine; none is passed in.
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id().upper() == product_id.upper():
                self.__order_lines.remove(order_line)
                return True
        return False

    def get_order_lines(self) -> list[OrderLine]:
        return self.__order_lines.copy()

    def calculate_subtotal(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def calculate_total(self) -> float:
        # No if/elif about discount types: the strategy decides.
        return self.__discount.apply(self.calculate_subtotal())

    def display_order(self) -> None:
        print(f"Order: {self.__order_id}")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"Subtotal: ${self.calculate_subtotal():.2f}")
        print(f"Discount: {type(self.__discount).__name__}")
        print(f"Total: ${self.calculate_total():.2f}")
