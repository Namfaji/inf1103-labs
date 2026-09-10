inventory1 = 0

while int(inventory1) <= 100:
    print("type 'quit' to quit")
    inventory1 = input("Please enter a stock quantity: ")
    if str(inventory1).isdigit() == False:
       if str(inventory1) ==  "quit":
           break
       else:
        print("Rejected, positive numbers only")
    else:
        if int(inventory1) < 0:
            print("Rejected negative numbers, positive numbers only")
        else:
            print(inventory1)




