from inventory import Inventory
from inventory_managerOOPv1 import load_inventory
from order import Order
from product import DigitalProduct, PhysicalProduct, Product
from supplier import Supplier


def test_association() -> None:
    print("\n========== ASSOCIATION ==========")
    supplier: Supplier = Supplier("S100", "Shared Supplier", "shared@example.com")
    physical_product: PhysicalProduct = PhysicalProduct(
        "P100", "Notebook", 4.5, 10, supplier, 0.3
    )
    digital_product: DigitalProduct = DigitalProduct(
        "D100", "E-book", 8.0, 25, supplier, 12.0
    )

    physical_product.display_information()
    digital_product.display_information()
    print(f"Physical product supplier id: {id(physical_product.get_supplier())}")
    print(f"Digital product supplier id: {id(digital_product.get_supplier())}")

    del supplier
    print("\nSupplier variable deleted; products still retain supplier information:")
    print("[Through physical product]")
    physical_product.get_supplier().display_information()
    print("[Through digital product]")
    digital_product.get_supplier().display_information()
    print(
        "Same Supplier object shared: "
        f"{physical_product.get_supplier() is digital_product.get_supplier()}"
    )


def test_aggregation() -> None:
    print("\n========== AGGREGATION ==========")
    supplier: Supplier = Supplier("S200", "Aggregation Supplier", "agg@example.com")
    product: PhysicalProduct = PhysicalProduct(
        "P200", "Desk", 150.0, 4, supplier, 12.0
    )

    inventory_a: Inventory = Inventory()
    inventory_a.add_product(product)
    print(f"Removed from inventory A: {inventory_a.remove_product('P200')}")
    print("Product still works after removal:")
    product.display_information()

    inventory_b: Inventory = Inventory()
    inventory_b.add_product(product)
    print(f"Found in inventory B: {inventory_b.find_product('p200') is product}")
    print(f"Found in inventory A: {inventory_a.find_product('P200')}")


def test_composition() -> None:
    print("\n========== COMPOSITION ==========")
    supplier: Supplier = Supplier("S300", "Order Supplier", "orders@example.com")
    product_one: PhysicalProduct = PhysicalProduct(
        "P300", "Chair", 45.0, 8, supplier, 5.0
    )
    product_two: DigitalProduct = DigitalProduct(
        "D300", "Design App", 30.0, 50, supplier, 300.0
    )

    order_one: Order = Order("O001")
    order_one.add_order_line(product_one, 2)
    order_one.add_order_line(product_two, 1)
    order_two: Order = Order("O002")
    order_two.add_order_line(product_one, 1)

    order_one.display_order()
    order_two.display_order()
    order_one_lines = order_one.get_order_lines()
    order_two_lines = order_two.get_order_lines()
    # Predict-first 4.3: the same Product (Chair) in two different Orders.
    chair_lines = [
        line
        for line in order_one_lines + order_two_lines
        if line.get_product().get_product_id() == "P300"
    ]
    chair_products = {id(line.get_product()) for line in chair_lines}
    print(
        "Same product in two orders -> "
        f"OrderLine objects: {len(chair_lines)}; "
        f"Product objects: {len(chair_products)}"
    )
    print(
        "Order lines are different objects: "
        f"{order_one_lines[0] is not order_two_lines[0]}"
    )
    print(
        "Both order lines reference the same Product: "
        f"{order_one_lines[0].get_product() is order_two_lines[0].get_product()}"
    )
    print(
        f"OrderLine ids: {id(order_one_lines[0])}, {id(order_two_lines[0])}"
    )
    print(
        "Shared Product ids: "
        f"{id(order_one_lines[0].get_product())}, "
        f"{id(order_two_lines[0].get_product())}"
    )

    print(f"Removed product line: {order_one.remove_order_line('P300')}")
    print(f"Order one new total: ${order_one.calculate_total():.2f}")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def test_lsp() -> None:
    print("\n========== LISKOV SUBSTITUTION ==========")
    supplier: Supplier = Supplier("S400", "LSP Supplier", "lsp@example.com")
    physical_product: PhysicalProduct = PhysicalProduct(
        "P400", "Speaker", 80.0, 6, supplier, 2.0
    )
    digital_product: DigitalProduct = DigitalProduct(
        "D400", "Audio App", 15.0, 12, supplier, 80.0
    )

    show_product_details(physical_product)
    show_product_details(digital_product)
    physical_product.update_stock(7)
    digital_product.update_stock(13)
    print(f"Physical product stock: {physical_product.get_stock()}")
    print(f"Digital product stock: {digital_product.get_stock()}")

    # Both subclasses keep Product's promise: invalid stock is rejected the same way.
    products: list[Product] = [physical_product, digital_product]
    for product in products:
        try:
            product.update_stock(-1)
        except ValueError as error:
            print(f"{product.get_name()} rejected -1: {error}")


def test_polymorphism() -> None:
    print("\n========== POLYMORPHISM ==========")
    supplier: Supplier = Supplier("S500", "Polymorphism Supplier", "poly@example.com")
    inventory: Inventory = Inventory()
    inventory.add_product(
        PhysicalProduct("P500", "Keyboard", 60.0, 9, supplier, 0.8)
    )
    inventory.add_product(
        DigitalProduct("D500", "Typing Tutor", 20.0, 30, supplier, 120.0)
    )

    for product in inventory.get_products():
        product.display_information()
        print(product.get_fulfilment_info())
        print("-" * 50)


def test_loaded_supplier_sharing() -> None:
    print("\n========== LOADED DATA: SHARED SUPPLIERS ==========")
    inventory, suppliers = load_inventory()
    products: list[Product] = inventory.get_products()
    if len(products) >= 2:
        first_supplier: Supplier = products[0].get_supplier()
        for product in products[1:]:
            if product.get_supplier().get_supplier_id() == first_supplier.get_supplier_id():
                print(
                    "Loaded products share the same Supplier object: "
                    f"{first_supplier is product.get_supplier()}"
                )
                break
    print(f"Suppliers loaded: {len(suppliers)}")


if __name__ == "__main__":
    test_association()
    test_aggregation()
    test_composition()
    test_lsp()
    test_polymorphism()
    test_loaded_supplier_sharing()
