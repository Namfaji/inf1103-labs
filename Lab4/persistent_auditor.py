
import time

inventory = 0
fail = 0
total_inventory = 0
order_no = 0
product_name = ["Wireless Mouse", "Keyboard", "USB Cable", "Laptop Stand"]
history_tracking = []
file = open("INF1103-Labs/inventory.txt", "r+")

time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def load_inventory():
    global order_no, total_inventory
    current_orders = ["Current Orders:"]

    with open("INF1103-Labs/inventory.txt", "r") as orders_file:
        for line in orders_file:
            order_number, product, quantity = line.strip().split(",", 2)
            current_orders.append(f"{order_number}, {product}, {quantity}")
            order_no = int(order_number)
            total_inventory += int(quantity)

    return "\n".join(current_orders)

def save_inventory(history_tracking, inventory, fail):
    file.write("Total Units Processed: " + str(inventory) + "\n")
    file.write("Number of Failed/Rejected Entries: " + str(fail) + "\n")
    file.write("History Tracking:\n")
    for entry in history_tracking:
        file.write(str(entry) + "\n")

def get_valid_input():
    user_input_prod = input("Enter Product Name: ").strip()

    if user_input_prod.lower() == "quit":
        return "quit"

    matched_product = None
    for product in product_name:
        if product.lower() == user_input_prod.lower():
            matched_product = product
            break

    if matched_product is None:
        print("Invalid product name")
        return None

    user_input = input("Enter Quantity: ").strip()
    if user_input.isdigit() and int(user_input) > 0:
        return matched_product, int(user_input)

    print("Rejected, please provide a positive number")
    return None

def calculate_tax(amount):
    tax_rate = 0.10
    tax_amount = amount * tax_rate
    print("Tax Amount: " + str(tax_amount))
    return tax_amount

def process_delivery(current_inventory, new_inventory):
    inventory = current_inventory
    if inventory <= 500:
        inventory += new_inventory
        print("Total Units Processed " + str(inventory))
        return inventory
    elif inventory == 500:
        print("Total inventory exceeds 500 units")
        return inventory

def generate_report(history_tracking, total_inventory, failed_entries):
    save_inventory(history_tracking, total_inventory, failed_entries)
    print("Total Units Processed " + str(total_inventory))
    print("Number of Failed/Rejected Entries " + str(failed_entries))

print(load_inventory())
while True:
    order = get_valid_input()
    if order == "quit":
        break
    elif order is None:
        fail += 1
    else:
        order_no += 1
        product, quantity = order
        with open("INF1103-Labs/inventory.txt", "a+") as orders_file:
            orders_file.seek(0, 2)
            if orders_file.tell() > 0:
                orders_file.seek(orders_file.tell() - 1)
                if orders_file.read(1) != "\n":
                    orders_file.write("\n")
            orders_file.write(f"{order_no},{product},{quantity}\n")
        total_inventory += quantity

        print("\nNew Order Added:")
        print(f"{order_no},{product},{quantity}")
        print("\nOrder successfully saved to inventory.txt")
        print(f"Total Units Processed: {total_inventory}")
        print(f"Number of Failed/Rejected Entries: {fail}")
        break
        


        




