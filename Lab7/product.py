from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def update_stock(self, quantity):
        self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    @abstractmethod
    def get_fulfilment_info(self):
        pass


class DigitalProduct(Product):
    """A product delivered digitally."""

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"Download size: {self.__download_size} MB")

    def get_fulfilment_info(self):
        return "This product is delivered digitally."

    def get_download_size(self):
        return self.__download_size


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped."""

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def get_weight(self):
        return self.__weight

    def calculate_shipping_cost(self):
        return self.__weight * 2.50
