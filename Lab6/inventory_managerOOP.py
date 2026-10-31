import json
from pathlib import Path

INVENTORY_FILE = Path(__file__).resolve().with_name("inventory.json")


##=====================================================================================
## Class Definitions

class Product:
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

class Inventory:
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
        product = Product(
            record["ProductID"],
            record["Name"],
            record["Price"],
            record["Stock"],
        )
        loaded_inventory.add_product(product)

    print("inventory.json found.")
    print("Inventory loaded successfully.")
    return loaded_inventory

## Update the with the new class-based inventory system
def save_inventory(inventory):
    records = []

    for product in inventory.get_products():
        records.append({
            "ProductID": product.get_product_id(),
            "Name": product.get_name(),
            "Price": product.get_price(),
            "Stock": product.get_stock(),
        })

    with INVENTORY_FILE.open("w") as file:
        json.dump(records, file)

    print("Inventory saved successfully to inventory.json.")






def add_product(inventory):
    print("\nAdd New Product example: Product ID: P001, Name: Widget, Price: 19.99, Stock: 100")
    product_id = input("Product ID: ").strip().upper()

    if inventory.search_product(product_id):
        print("A product with that ID already exists.")
        return

    name = input("Product Name: ").strip()
    price_input = input("Price: ").strip()
    stock_input = input("Stock Quantity: ").strip()

    valid_price = (
        price_input.count(".") <= 1
        and price_input.replace(".", "", 1).isdigit()
    )
    valid_stock = stock_input.isdigit()

    if not product_id or not name or not valid_price or not valid_stock:
        print("Enter a product ID and name, a non-negative price, and non-negative stock.")
        return

    product = Product(
        product_id,
        name,
        float(price_input),
        int(stock_input),
    )
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












