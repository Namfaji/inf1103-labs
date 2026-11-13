from abc import ABC, abstractmethod

from supplier import Supplier


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


class Product(ABC):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
    ) -> None:
        # Validation: Product owns these rules, so every subclass inherits them.
        if not product_id.strip():
            raise ValueError("Product ID cannot be empty.")
        if not name.strip():
            raise ValueError("Product name cannot be empty.")
        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise ValueError("Price must be a number.")
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        Product.__check_stock(stock)

        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = float(price)
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    @staticmethod
    def __check_stock(quantity: int) -> None:
        if type(quantity) is not int:
            raise ValueError("Stock must be a whole number.")
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")

    def update_stock(self, quantity: int) -> None:
        Product.__check_stock(quantity)
        self.__stock = quantity

    def display_information(self) -> None:
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(f"Supplier: {self.__supplier.get_name()}")

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def to_dict(self) -> dict[str, str | int | float]:
        """Return the fields every Product shares; subclasses add their own."""
        return {
            "ProductID": self.__product_id,
            "Name": self.__name,
            "Price": self.__price,
            "Stock": self.__stock,
            "SupplierID": self.__supplier.get_supplier_id(),
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass


class DigitalProduct(Product):
    """A product delivered digitally."""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        download_size: float,
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size: float = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download size: {self.__download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally."

    def get_download_size(self) -> float:
        return self.__download_size

    def to_dict(self) -> dict[str, str | int | float]:
        record: dict[str, str | int | float] = super().to_dict()
        record["Type"] = "digital"
        record["DownloadSize"] = self.__download_size
        return record


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped."""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        weight: float,
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight: float = weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def get_weight(self) -> float:
        return self.__weight

    def calculate_shipping_cost(self) -> float:
        return self.__weight * 2.50

    def to_dict(self) -> dict[str, str | int | float]:
        record: dict[str, str | int | float] = super().to_dict()
        record["Type"] = "physical"
        record["Weight"] = self.__weight
        return record
