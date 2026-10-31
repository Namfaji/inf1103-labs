import json
from pathlib import Path
from abc import ABC, abstractmethod

INVENTORY_FILE = Path(__file__).resolve().with_name("inventory.json")


##=====================================================================================
## Class Definitions

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class Product(ABC):
    ##Variables for Product class
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    ##Functions for Product class
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

class Inventory:
    """Store the information and behavior shared by all inventory products."""
    ##Variables for Inventory class
    def __init__(self):
        self.__products = []

    ##Functions for Inventory class
    def add_product(self, product):
        self.__products.append(product)

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id().upper() == product_id.upper():
                return product
        return None
    
    def get_products(self):
        return self.__products

    def display_all(self):
        if not self.__products:
            print("Inventory is empty.")
            return

        print("\nCurrent Inventory")
        print("-" * 50)
        for product in self.__products:
            product.display_information()
            print("-" * 50)

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



##=====================================================================================

## Update the with the new class-based inventory system
def load_inventory():
    loaded_inventory = Inventory()

    if not INVENTORY_FILE.exists():
        print("inventory.json not found. Starting with an empty inventory.")
        return loaded_inventory

    with INVENTORY_FILE.open("r") as file:
        records = json.load(file)

    for record in records:
        product_type = record["Type"]

        if product_type == "physical":
            product = PhysicalProduct(
                record["ProductID"],
                record["Name"],
                record["Price"],
                record["Stock"],
                record["Weight"],
            )
        elif product_type == "digital":
            product = DigitalProduct(
                record["ProductID"],
                record["Name"],
                record["Price"],
                record["Stock"],
                record["DownloadSize"],
            )
        else:
            raise ValueError(f"Unknown product type: {product_type}")

        loaded_inventory.add_product(product)

    print("inventory.json found.")
    print("Inventory loaded successfully.")
    return loaded_inventory

## Update the with the new class-based inventory system
def save_inventory(inventory):
    records = []

    for product in inventory.get_products():
        record = {
            "ProductID": product.get_product_id(),
            "Name": product.get_name(),
            "Price": product.get_price(),
            "Stock": product.get_stock(),
        }

        if isinstance(product, PhysicalProduct):
            record["Type"] = "physical"
            record["Weight"] = product.get_weight()
        elif isinstance(product, DigitalProduct):
            record["Type"] = "digital"
            record["DownloadSize"] = product.get_download_size()
        else:
            raise TypeError(f"Unsupported product type: {type(product).__name__}")

        records.append(record)

    with INVENTORY_FILE.open("w") as file:
        json.dump(records, file, indent=4)

    print("Inventory saved successfully to inventory.json.")






def add_product(inventory):
    product_type = input("Product Type (1 for Physical, 2 for Digital): ").strip()
    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Product ID: ").strip().upper()
    if not product_id or inventory.search_product(product_id):
        print("Enter a product ID that is not already in use.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    price_input = input("Price: ").strip()
    stock_input = input("Stock Quantity: ").strip()
    extra_label = "Weight in kg" if product_type == "1" else "Download size in MB"
    extra_input = input(f"{extra_label}: ").strip()

    try:
        price = float(price_input)
        stock = int(stock_input)
        extra = float(extra_input)
        if price < 0 or stock < 0 or extra < 0:
            raise ValueError
    except ValueError:
        print("Price and product-specific value must be non-negative numbers; stock must be a non-negative whole number.")
        return

    if product_type == "1":
        product = PhysicalProduct(product_id, name, price, stock, extra)
    else:
        product = DigitalProduct(product_id, name, price, stock, extra)

    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory):
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    stock_input = input("New Stock Quantity: ").strip()
    if stock_input.isdigit():
        product.update_stock(int(stock_input))
        print("Stock updated successfully!")
    else:
        print("Stock must be a non-negative whole number.")


def search_product(inventory):
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found")
    print("-" * 50)
    product.display_information()
    print("-" * 50)


inventory = load_inventory()

print(inventory.display_all())
while True:
    print("\n---------- MENU ----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    option = input("Enter option: ").strip()
    if option == "1":
        inventory.display_all()
    elif option == "2":
        add_product(inventory)
    elif option == "3":
        update_stock(inventory)
    elif option == "4":
        search_product(inventory)
    elif option == "5":
        print("Saving inventory...")
        save_inventory(inventory)
    elif option == "6":
        print("Saving inventory before exit...")
        save_inventory(inventory)
        print("Thank you for using Inventory Management System.")
        print("Program terminated.")
        break
    else:
        print("Invalid option. Please choose 1-6.")














