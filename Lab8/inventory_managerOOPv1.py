import json
from pathlib import Path

from inventory import Inventory
from product import DigitalProduct, PhysicalProduct, Product
from supplier import Supplier

INVENTORY_FILE: Path = Path(__file__).resolve().with_name("inventory.json")


def load_inventory() -> tuple[Inventory, dict[str, Supplier]]:
    loaded_inventory: Inventory = Inventory()
    suppliers: dict[str, Supplier] = {}

    if not INVENTORY_FILE.exists():
        print("inventory.json not found. Starting with an empty inventory.")
        return loaded_inventory, suppliers

    with INVENTORY_FILE.open("r", encoding="utf-8") as file:
        records = json.load(file)

    for record in records["Suppliers"]:
        supplier: Supplier = Supplier(
            record["SupplierID"],
            record["Name"],
            record["ContactEmail"],
        )
        suppliers[supplier.get_supplier_id()] = supplier

    for record in records["Products"]:
        product_type: str = record["Type"]
        supplier = suppliers[record["SupplierID"]]

        if product_type == "physical":
            product: Product = PhysicalProduct(
                record["ProductID"],
                record["Name"],
                record["Price"],
                record["Stock"],
                supplier,
                record["Weight"],
            )
        elif product_type == "digital":
            product = DigitalProduct(
                record["ProductID"],
                record["Name"],
                record["Price"],
                record["Stock"],
                supplier,
                record["DownloadSize"],
            )
        else:
            raise ValueError(f"Unknown product type: {product_type}")

        loaded_inventory.add_product(product)

    print("inventory.json found.")
    print("Inventory loaded successfully.")
    return loaded_inventory, suppliers


def save_inventory(
    inventory: Inventory, suppliers: dict[str, Supplier]
) -> None:
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
    with INVENTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully to inventory.json.")


def add_product(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    product_type: str = input(
        "Product Type (1 for Physical, 2 for Digital): "
    ).strip()
    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id: str = input("Product ID: ").strip().upper()
    if not product_id or inventory.find_product(product_id) is not None:
        print("Enter a product ID that is not already in use.")
        return

    name: str = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    supplier_id: str = input("Supplier ID: ").strip().upper()
    if not supplier_id:
        print("Supplier ID cannot be empty.")
        return
    supplier: Supplier | None = suppliers.get(supplier_id)
    new_supplier: Supplier | None = None
    if supplier is None:
        supplier_name: str = input("Supplier Name: ").strip()
        contact_email: str = input("Supplier Contact Email: ").strip()
        if not supplier_name or not contact_email:
            print("Supplier name and contact email cannot be empty.")
            return
        supplier = Supplier(supplier_id, supplier_name, contact_email)
        new_supplier = supplier

    price_input: str = input("Price: ").strip()
    stock_input: str = input("Stock Quantity: ").strip()
    extra_label: str = (
        "Weight in kg" if product_type == "1" else "Download size in MB"
    )
    extra_input: str = input(f"{extra_label}: ").strip()

    try:
        price: float = float(price_input)
        stock: int = int(stock_input)
        extra: float = float(extra_input)
        if price < 0 or stock < 0 or extra < 0:
            raise ValueError
    except ValueError:
        print(
            "Price and product-specific value must be non-negative numbers; "
            "stock must be a non-negative whole number."
        )
        return

    if product_type == "1":
        product: Product = PhysicalProduct(
            product_id, name, price, stock, supplier, extra
        )
    else:
        product = DigitalProduct(product_id, name, price, stock, supplier, extra)

    if new_supplier is not None:
        suppliers[supplier_id] = new_supplier
    inventory.add_product(product)
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

    stock_input: str = input("New Stock Quantity: ").strip()
    try:
        product.update_stock(int(stock_input))
    except ValueError as error:
        print(error)
        return

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


def main() -> None:
    inventory, suppliers = load_inventory()
    inventory.display_all()

    while True:
        print("\n---------- MENU ----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Remove Product")
        print("7. Exit")
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
            print("Saving inventory before exit...")
            save_inventory(inventory, suppliers)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please choose 1-7.")


if __name__ == "__main__":
    main()
