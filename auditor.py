inventory = 0
fail = 0
while inventory <= 500:
    print("type 'quit' to quit")
    inventory1 = input("Please enter a stock quantity: ")
    if str(inventory1).isdigit() == False:
       if str(inventory1) ==  "quit":
           break
       else:
        print("Rejected, positive numbers only")
        fail+=1
    else:
        if int(inventory1) < 0:
            print("Rejected negative numbers, positive numbers only")
            fail+=1
        else:
            inventory = int(inventory1)
    print(inventory)

if int(inventory) == 500:
    print("Total inventory exceeds 500 units")
else:
    print("Total Units Processed "+str(inventory))
print("Number of Failed/Rejected Entries "+str(fail)) 