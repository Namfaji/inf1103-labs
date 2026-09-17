inventory = 0
fail = 0
while True:
    input = get_valid_input()
    if input == "quit":
        generate_report(inventory, fail)
        break
    elif input.isdigit() == True:
        process_delivery(inventory, int(input))
    else:
        fail += 1



if int(inventory) == 500:
    print("Total inventory exceeds 500 units")
else:
    print("Total Units Processed "+str(inventory))
print("Number of Failed/Rejected Entries "+str(fail)) 

def get_valid_input():
    print("type 'quit' to quit")
    user_input = input("Please enter a stock quantity: ")
    if user_input.lower() == "quit":
        return user_input.lower()
    elif user_input.isdigit() and int(user_input) >= 0:
        return int(user_input)
    else:
        print("Rejected,please provide positive numbers only")
        fail += 1

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