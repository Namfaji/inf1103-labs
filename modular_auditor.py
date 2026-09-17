inventory = 0
fail = 0

def get_valid_input():
    print("type 'quit' to quit")
    user_input = input("Please enter a stock quantity: ")
    if user_input.lower() == "quit":
        return user_input.lower()
    elif user_input.isdigit() and int(user_input) > 0:
        return int(user_input)
    else:
        print("Rejected,please provide positive numbers only")

def process_delivery(current_inventory, new_inventory):
    inventory = current_inventory
    if inventory <= 500:
        inventory += new_inventory
        print("Total Units Processed " + str(inventory))
        return inventory
    elif inventory == 500:
        print("Total inventory exceeds 500 units")
        return inventory

def calculate_tax(amount):
    tax_rate = 0.10
    tax_amount = amount * tax_rate
    return tax_amount


def generate_report(total_inventory, failed_entries):
    print("Total Units Processed " + str(total_inventory))
    print("Number of Failed/Rejected Entries " + str(failed_entries))


while True:
    quantity = get_valid_input()
    print(type(quantity))
    print(quantity)
    if quantity == "quit":
        generate_report(inventory, fail)
        break
    elif quantity is None:
        fail += 1
    else:
        inventory = process_delivery(inventory, quantity)
        calculate_tax(quantity)

        




