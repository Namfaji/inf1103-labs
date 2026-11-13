import csv

from factory import ProductFactory
from inventory import Inventory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Load products from a CSV file, skipping bad rows (Section 5.2)."""
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded: int = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for row_number, row in enumerate(reader, start=2):
                if not row:
                    continue  # ignore blank lines
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(
                        product_type,
                        product_id.strip().upper(),
                        name.strip(),
                        float(price),
                        int(stock),
                        supplier,
                    )
                    inventory.add_product(product)
                except ValueError as error:
                    print(f"Row {row_number} skipped: {error}")
                else:
                    loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
