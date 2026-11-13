import unittest

from factory import ProductFactory
from inventory import Inventory
from order import Order, OrderLine
from product import DigitalProduct, PhysicalProduct, Product
from tests.helpers import make_supplier


class TestProductFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = make_supplier()

    def test_creates_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, self.supplier, 1.2)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)

    def test_creates_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D1", "Editor", 49.9, 100, self.supplier, 500)
        self.assertIsInstance(product, DigitalProduct)

    def test_type_is_case_insensitive(self) -> None:
        product = ProductFactory.create(" Physical ", "P2", "Stand", 39.5, 7, self.supplier)
        self.assertIsInstance(product, PhysicalProduct)

    def test_unknown_type_raises_clear_value_error(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S1", "Installation", 30.0, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")


class TestValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = make_supplier()

    def make(self, price: float = 10.0, stock: int = 1) -> Product:
        return ProductFactory.create("physical", "P1", "Lamp", price, stock, self.supplier)

    def test_price_must_be_greater_than_zero(self) -> None:
        for bad in (0, -5.0):
            with self.assertRaises(ValueError):
                self.make(price=bad)

    def test_stock_cannot_be_negative(self) -> None:
        with self.assertRaises(ValueError):
            self.make(stock=-1)

    def test_update_stock_rejects_negative_for_both_subclasses(self) -> None:
        products = [
            self.make(),
            ProductFactory.create("digital", "D1", "App", 5.0, 3, self.supplier),
        ]
        for product in products:
            with self.assertRaises(ValueError):
                product.update_stock(-1)
            product.update_stock(0)
            self.assertEqual(product.get_stock(), 0)

    def test_order_line_quantity_must_be_greater_than_zero(self) -> None:
        product = self.make()
        for bad in (0, -2):
            with self.assertRaises(ValueError):
                OrderLine(product, bad)

    def test_order_rejects_bad_quantity_through_order_line(self) -> None:
        order = Order("O1")
        with self.assertRaises(ValueError):
            order.add_order_line(self.make(), 0)
        self.assertEqual(order.get_order_lines(), [])

    def test_inventory_rejects_duplicate_product_id(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.make())
        with self.assertRaises(ValueError):
            inventory.add_product(self.make())
        self.assertEqual(len(inventory.get_products()), 1)


if __name__ == "__main__":
    unittest.main()
