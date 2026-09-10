inventory1 = 0
while int(inventory1) <= 100:
    inventory1 = input("Please enter a stock quantity: ")
    if str(inventory1).isdigit() == False:
       if str(inventory1) ==  "quit":
           break
    print(inventory1)

