from product import Product


class Inventory:
    """Store the information and behavior shared by all inventory products."""

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def remove_product(self, product_id: str) -> bool:
        for product in self.__products:
            if product.get_product_id().upper() == product_id.upper():
                self.__products.remove(product)
                return True
        return False

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id().upper() == product_id.upper():
                return product
        return None

    def get_products(self) -> list[Product]:
        return self.__products.copy()

    def display_all(self) -> None:
        if not self.__products:
            print("Inventory is empty.")
            return

        print("\nCurrent Inventory")
        print("-" * 50)
        for product in self.__products:
            product.display_information()
            print(product.get_fulfilment_info())
            print("-" * 50)
