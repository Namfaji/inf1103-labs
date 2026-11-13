import json
from pathlib import Path

from factory import ProductFactory
from input_helpers import (
    get_choice,
    get_non_empty_text,
    get_non_negative_float,
    get_non_negative_int,
    get_positive_float,
)
from inventory import Inventory
from product import Product
from product_loader import load_products
from supplier import Supplier

INVENTORY_FILE: Path = Path(__file__).resolve().with_name("inventory.json")
PRODUCTS_CSV: Path = Path(__file__).resolve().with_name("products.csv")

PRODUCT_TYPES: dict[str, str] = {"1": "physical", "2": "digital"}


def load_inventory() -> tuple[Inventory, dict[str, Supplier]]:
    """Load inventory.json. A missing file gives an empty inventory.

    A damaged file raises json.JSONDecodeError, KeyError or ValueError,
    which main() catches so the program can stop without overwriting it.
    """
    loaded_inventory: Inventory = Inventory()
    suppliers: dict[str, Supplier] = {}

    try:
        file = INVENTORY_FILE.open("r", encoding="utf-8")
    except FileNotFoundError:
        print("inventory.json not found. Starting with an empty inventory.")
        return loaded_inventory, suppliers

    with file:
        records = json.load(file)

    for record in records["Suppliers"]:
        supplier: Supplier = Supplier(
            record["SupplierID"],
            record["Name"],
            record["ContactEmail"],
        )
        suppliers[supplier.get_supplier_id()] = supplier

    for record in records["Products"]:
        # Factory pattern: no PhysicalProduct/DigitalProduct created here.
        product: Product = ProductFactory.create(
            record["Type"],
            record["ProductID"],
            record["Name"],
            record["Price"],
            record["Stock"],
            suppliers[record["SupplierID"]],
            record.get("Weight", record.get("DownloadSize", 0.0)),
        )
        loaded_inventory.add_product(product)

    print("inventory.json found.")
    print("Inventory loaded successfully.")
    return loaded_inventory, suppliers


def save_inventory(inventory: Inventory, suppliers: dict[str, Supplier]) -> bool:
    supplier_records: list[dict[str, str]] = []
    for supplier in suppliers.values():
        supplier_records.append(
            {
                "SupplierID": supplier.get_supplier_id(),
                "Name": supplier.get_name(),
                "ContactEmail": supplier.get_contact_email(),
            }
        )

    # Polymorphism: each product builds its own record, so no type checks here.
    product_records: list[dict[str, str | int | float]] = [
        product.to_dict() for product in inventory.get_products()
    ]

    data: dict[str, list[dict[str, str]] | list[dict[str, str | int | float]]] = {
        "Suppliers": supplier_records,
        "Products": product_records,
    }
    try:
        with INVENTORY_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except OSError as error:
        print(f"Could not save inventory.json: {error}")
        return False

    print("Inventory saved successfully to inventory.json.")
    return True


def get_or_create_supplier(suppliers: dict[str, Supplier]) -> Supplier:
    supplier_id: str = get_non_empty_text("Supplier ID: ").upper()
    supplier: Supplier | None = suppliers.get(supplier_id)
    if supplier is None:
        print("New supplier. Please enter its details.")
        supplier = Supplier(
            supplier_id,
            get_non_empty_text("Supplier Name: "),
            get_non_empty_text("Supplier Contact Email: "),
        )
        suppliers[supplier_id] = supplier
    return supplier


def add_product(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    type_choice: str = get_choice(
        "Product Type (1 for Physical, 2 for Digital): ", tuple(PRODUCT_TYPES)
    )

    while True:
        product_id: str = get_non_empty_text("Product ID: ").upper()
        if inventory.find_product(product_id) is None:
            break
        print("That product ID is already in use. Please enter another.")

    name: str = get_non_empty_text("Product Name: ")
    supplier: Supplier = get_or_create_supplier(suppliers)
    price: float = get_positive_float("Price: ")
    stock: int = get_non_negative_int("Stock Quantity: ")
    extra_label: str = (
        "Weight in kg" if type_choice == "1" else "Download size in MB"
    )
    extra: float = get_non_negative_float(f"{extra_label}: ")

    try:
        product: Product = ProductFactory.create(
            PRODUCT_TYPES[type_choice], product_id, name, price, stock, supplier, extra
        )
        inventory.add_product(product)
    except ValueError as error:
        print(f"Product not added: {error}")
        return
    print("Product added successfully!")


def update_stock(inventory: Inventory) -> None:
    product_id: str = input("Enter Product ID: ").strip().upper()
    product: Product | None = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    product.update_stock(get_non_negative_int("New Stock Quantity: "))
    print("Stock updated successfully!")


def search_product(inventory: Inventory) -> None:
    product_id: str = input("Enter Product ID: ").strip().upper()
    product: Product | None = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found")
    print("-" * 50)
    product.display_information()
    print(product.get_fulfilment_info())
    print("-" * 50)


def remove_product(inventory: Inventory) -> None:
    product_id: str = input("Enter Product ID: ").strip().upper()
    if inventory.remove_product(product_id):
        print("Product removed successfully.")
    else:
        print("Product not found.")


def import_products(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    path: str = input(f"CSV file path [{PRODUCTS_CSV.name}]: ").strip()
    if not path:
        path = str(PRODUCTS_CSV)
    print("Which supplier provides these products?")
    supplier: Supplier = get_or_create_supplier(suppliers)
    load_products(path, inventory, supplier)


def main() -> None:
    try:
        inventory, suppliers = load_inventory()
    except (json.JSONDecodeError, KeyError, ValueError) as error:
        # Do not continue with incomplete data, and do not overwrite the file.
        print(f"inventory.json could not be read: {error}")
        print("Please fix or remove the file, then run the program again.")
        return

    inventory.display_all()

    while True:
        print("\n---------- MENU ----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Remove Product")
        print("7. Import Products from CSV")
        print("8. Exit")
        option: str = input("Enter option: ").strip()
        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product(inventory, suppliers)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory, suppliers)
        elif option == "6":
            remove_product(inventory)
        elif option == "7":
            import_products(inventory, suppliers)
        elif option == "8":
            print("Saving inventory before exit...")
            save_inventory(inventory, suppliers)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please choose 1-8.")


if __name__ == "__main__":
    main()
