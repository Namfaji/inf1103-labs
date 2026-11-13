from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
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
    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        # Composition: the Order creates its own OrderLine; none is passed in.
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Quantity must be a positive whole number.")
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id().upper() == product_id.upper():
                self.__order_lines.remove(order_line)
                return True
        return False

    def get_order_lines(self) -> list[OrderLine]:
        return self.__order_lines.copy()

    def calculate_total(self) -> float:
        return sum(
            order_line.calculate_subtotal() for order_line in self.__order_lines
        )

    def display_order(self) -> None:
        print(f"Order: {self.__order_id}")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"Total: ${self.calculate_total():.2f}")
