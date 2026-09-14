def main():
    inventory = 0
    failed_entries = 0

    while inventory <= 500:
        print("type 'quit' to quit")
        entry = input("Please enter a stock quantity: ")

        if entry == "quit":
            break

        if not entry.lstrip("-").isdigit():
            print("Rejected, positive numbers only")
            failed_entries += 1
        else:
            quantity = int(entry)
            if quantity < 0:
                print("Rejected negative numbers, positive numbers only")
                failed_entries += 1
            else:
                inventory = quantity

        print(inventory)

    if inventory == 500:
        print("Total inventory exceeds 500 units")
    else:
        print(f"Total Units Processed {inventory}")
    print(f"Number of Failed/Rejected Entries {failed_entries}")


if __name__ == "__main__":
    main()