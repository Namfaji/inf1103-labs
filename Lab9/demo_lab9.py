"""Lab 9 demonstration: one section per Predict-first question.

Run: python demo_lab9.py
Each section prints a clear header so the output can be screenshotted.
"""
import os
import shutil
import tempfile
from typing import Callable
from unittest.mock import patch

from discount import BulkDiscount, PercentageDiscount, StudentDiscount
from factory import ProductFactory
from input_helpers import get_positive_float
from inventory import Inventory
from order import Order
from product_loader import load_products
from supplier import Supplier

SUPPLIER = Supplier("S001", "Northstar Supplies", "contact@northstar.example")


def header(title: str) -> None:
    print(f"\n========== {title} ==========")


def demo_strategy() -> None:
    header("2.3 STRATEGY: order lines adding up to 250")
    order = Order("O001", BulkDiscount(200, 20))
    order.add_order_line(
        ProductFactory.create("physical", "P001", "Desk", 100.0, 5, SUPPLIER, 10.0), 2
    )
    order.add_order_line(
        ProductFactory.create("digital", "D001", "App", 50.0, 9, SUPPLIER, 80.0), 1
    )
    order.display_order()

    print("\nset_discount(PercentageDiscount(10)) on the same order:")
    order.set_discount(PercentageDiscount(10))
    print(f"Total: ${order.calculate_total():.2f}")

    header("2.4 NEW STRATEGY: StudentDiscount, Order unchanged")
    order.set_discount(StudentDiscount())
    print(f"Total: ${order.calculate_total():.2f}")

    header("2.4 RELATIONSHIP: two orders sharing one strategy")
    shared = PercentageDiscount(10)
    order_a = Order("O002", shared)
    order_b = Order("O003", shared)
    print(f"Same DiscountStrategy object: {order_a.get_discount() is order_b.get_discount()}")


def demo_factory() -> None:
    header("3.2 FACTORY: ProductFactory.create('service', ...)")
    try:
        ProductFactory.create("service", "S001", "Installation", 30.0, 5, SUPPLIER)
    except ValueError as error:
        print(f"ValueError raised in ProductFactory.create(): {error}")
        print("(If nothing caught it, the program would stop with a traceback.)")


def demo_validation() -> None:
    header("4 VALIDATION")
    attempts: list[tuple[str, Callable[[], object]]] = [
        ("price 0", lambda: ProductFactory.create("physical", "P9", "Lamp", 0, 1, SUPPLIER)),
        ("stock -1", lambda: ProductFactory.create("digital", "D9", "App", 5.0, -1, SUPPLIER)),
        ("order quantity 0", lambda: Order("O9").add_order_line(
            ProductFactory.create("physical", "P8", "Lamp", 5.0, 1, SUPPLIER), 0)),
    ]
    for label, attempt in attempts:
        try:
            attempt()
        except ValueError as error:
            print(f"{label}: rejected -> {error}")

    digital = ProductFactory.create("digital", "D7", "App", 5.0, 3, SUPPLIER)
    try:
        digital.update_stock(-1)
    except ValueError as error:
        print(f"DigitalProduct.update_stock(-1): rejected -> {error}")


def demo_input() -> None:
    header("5.1 INPUT: user enters abc, then -5, then 12.50")
    answers = iter(["abc", "-5", "12.50"])

    def fake_input(prompt: str) -> str:
        answer = next(answers)
        print(f"{prompt}{answer}")
        return answer

    with patch("builtins.input", fake_input):
        value = get_positive_float("Price: ")
    print(f"Returned value: {value}")


def demo_loading() -> None:
    source = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.csv")
    start_folder = os.getcwd()
    folder = tempfile.mkdtemp()
    try:
        # Work on a copy so the real products.csv is never renamed.
        os.chdir(folder)
        shutil.copy(source, "products.csv")

        header("5.2 LOAD products.csv")
        inventory = Inventory()
        load_products("products.csv", inventory, SUPPLIER)
        print("Loaded IDs:", [p.get_product_id() for p in inventory.get_products()])

        header("5.2 LOAD after renaming products.csv")
        os.rename("products.csv", "products_renamed.csv")
        load_products("products.csv", Inventory(), SUPPLIER)
    finally:
        os.chdir(start_folder)
        shutil.rmtree(folder)


if __name__ == "__main__":
    demo_strategy()
    demo_factory()
    demo_validation()
    demo_input()
    demo_loading()
