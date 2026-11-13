import inspect
import unittest

from discount import (
    BulkDiscount,
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    StudentDiscount,
)
from factory import ProductFactory
from order import Order
from tests.helpers import make_supplier


class TestDiscountStrategies(unittest.TestCase):
    def test_no_discount_returns_total_unchanged(self) -> None:
        self.assertEqual(NoDiscount().apply(250.0), 250.0)

    def test_percentage_discount(self) -> None:
        self.assertAlmostEqual(PercentageDiscount(10).apply(250.0), 225.0)

    def test_bulk_discount_at_or_above_threshold(self) -> None:
        self.assertAlmostEqual(BulkDiscount(200, 20).apply(250.0), 230.0)
        self.assertAlmostEqual(BulkDiscount(200, 20).apply(200.0), 180.0)

    def test_bulk_discount_below_threshold(self) -> None:
        self.assertAlmostEqual(BulkDiscount(200, 20).apply(150.0), 150.0)

    def test_student_discount(self) -> None:
        self.assertAlmostEqual(StudentDiscount().apply(200.0), 190.0)

    def test_invalid_percentage_rejected(self) -> None:
        for bad in (0, -5, 150):
            with self.assertRaises(ValueError):
                PercentageDiscount(bad)

    def test_invalid_bulk_values_rejected(self) -> None:
        with self.assertRaises(ValueError):
            BulkDiscount(-1, 20)
        with self.assertRaises(ValueError):
            BulkDiscount(200, 0)

    def test_discount_strategy_is_abstract(self) -> None:
        with self.assertRaises(TypeError):
            DiscountStrategy()  # type: ignore[abstract]


class TestOrderUsesStrategy(unittest.TestCase):
    def setUp(self) -> None:
        # Order lines that add up to 250 (Predict first, Section 2.3).
        supplier = make_supplier()
        self.order = Order("O100")
        self.order.add_order_line(
            ProductFactory.create("physical", "P900", "Desk", 100.0, 5, supplier, 10.0), 2
        )
        self.order.add_order_line(
            ProductFactory.create("digital", "D900", "App", 50.0, 9, supplier, 80.0), 1
        )

    def test_default_is_no_discount(self) -> None:
        self.assertIsInstance(self.order.get_discount(), NoDiscount)
        self.assertAlmostEqual(self.order.calculate_total(), 250.0)

    def test_bulk_then_percentage_with_set_discount(self) -> None:
        self.order.set_discount(BulkDiscount(200, 20))
        self.assertAlmostEqual(self.order.calculate_total(), 230.0)
        self.order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(self.order.calculate_total(), 225.0)

    def test_strategy_given_when_order_is_created(self) -> None:
        order = Order("O101", StudentDiscount())
        self.assertIsInstance(order.get_discount(), StudentDiscount)

    def test_new_strategy_works_without_changing_order(self) -> None:
        class HalfPrice(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total / 2

        self.order.set_discount(HalfPrice())
        self.assertAlmostEqual(self.order.calculate_total(), 125.0)

    def test_two_orders_can_share_one_strategy(self) -> None:
        shared = PercentageDiscount(10)
        other = Order("O102", shared)
        self.order.set_discount(shared)
        self.assertIs(self.order.get_discount(), other.get_discount())

    def test_order_has_no_discount_if_elif(self) -> None:
        code_lines = [
            line.split("#")[0]
            for line in inspect.getsource(Order.calculate_total).splitlines()
        ]
        code = "\n".join(code_lines)
        self.assertNotIn("if ", code)
        self.assertNotIn("elif", code)
        self.assertNotIn("isinstance", inspect.getsource(Order))


if __name__ == "__main__":
    unittest.main()
