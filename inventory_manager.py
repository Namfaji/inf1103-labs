
import json
from pathlib import Path

INVENTORY_FILE = Path(__file__).resolve().with_name("inventory.json")
inventory = []

def load_inventory():
    global inventory

    if not INVENTORY_FILE.exists():
        print("inventory.json not found. Starting with an empty inventory.")
        inventory = []
        return inventory

    with INVENTORY_FILE.open("r") as file:
        inventory = json.load(file)

    print("inventory.json found.")
    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    with INVENTORY_FILE.open("w") as file:
        json.dump(inventory, file)
    print("Inventory saved successfully to inventory.json.")



def display_all(inventory):
    if not inventory:
        print("Inventory is empty.")
        return

    print("\nCurrent Inventory")
    print("-" * 50)
    for product in inventory:
        print( "ID: " + str(product["ProductID"]) + " | "  
              + "Name: " + str(product["Name"]) + " | "    
              + "Price: $" + str(product["Price"]) + " | "    #ask 
              + "Stock: " + str(product["Stock"])
)
    print("-" * 50)


def add_product(inventory):
    print("\nAdd New Product example: Product ID: P001, Name: Widget, Price: 19.99, Stock: 100")
    product_id = input("Product ID: ").strip().upper()
    for product in inventory:
        if product["ProductID"].upper() == product_id:
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
    else:
        price = float(price_input)
        stock = int(stock_input)
        inventory.append({
            "ProductID": product_id,
            "Name": name,
            "Price": price,
            "Stock": stock,
        })
        print("Product added successfully!")


def update_stock(inventory):
    product_id = input("Enter Product ID: ").strip().upper()
    for product in inventory:
        if product["ProductID"].upper() == product_id:
            print("Product Found:")
            print(f"Name: {product['Name']}")
            print(f"Current Stock: {product['Stock']}")
            stock_input = input("New Stock Quantity: ").strip()
            if stock_input.isdigit():
                new_stock = int(stock_input)
                product["Stock"] = new_stock
                print("Stock updated successfully!")
            else:
                print("Stock must be a non-negative whole number.")
            return

    print("Product not found.")


def search_product(inventory):
    product_id = input("Enter Product ID: ").strip().upper()
    for product in inventory:
        if product["ProductID"].upper() == product_id:
            print("\nProduct Found")
            print("-" * 50)
            print(f"ID: {product['ProductID']}")
            print(f"Name: {product['Name']}")
            print(f"Price: ${product['Price']:.2f}")
            print(f"Stock: {product['Stock']}")
            print("-" * 50)
            return

    print("Product not found.")


load_inventory()

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
        display_all(inventory)
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












