def display_all(inventory):
    if not inventory:
        print("Inventory is empty.")
        return

    print("\nCurrent Inventory")
    print("-" * 50)
    for product in inventory:
        print(
            "ID: " + str(product["ProductID"]) + " | "
            + "Name: " + str(product["Name"]) + " | "
            + "Price: $" + format(product["Price"], ".2f") + " | "
            + "Stock: " + str(product["Stock"])
        )
    print("-" * 50)


def add_product(inventory):
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
        inventory.append({
            "ProductID": product_id,
            "Name": name,
            "Price": float(price_input),
            "Stock": int(stock_input),
        })
        print("Product added successfully!")


def update_stock(inventory):
    product_id = input("Enter Product ID: ").strip().upper()

    for product in inventory:
        if product["ProductID"].upper() == product_id:
            print("Product Found:")
            print("Name: " + product["Name"])
            print("Current Stock: " + str(product["Stock"]))

            stock_input = input("New Stock Quantity: ").strip()
            if stock_input.isdigit():
                product["Stock"] = int(stock_input)
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
            print("ID: " + product["ProductID"])
            print("Name: " + product["Name"])
            print("Price: $" + format(product["Price"], ".2f"))
            print("Stock: " + str(product["Stock"]))
            print("-" * 50)
            return

    print("Product not found.")