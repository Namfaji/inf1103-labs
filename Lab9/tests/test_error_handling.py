import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from input_helpers import get_non_negative_int, get_positive_float
from inventory import Inventory
from product_loader import load_products
from tests.helpers import make_supplier

CSV_TEXT = (
    "product_type,product_id,name,price,stock_quantity\n"
    "physical,P001,Desk Lamp,25.00,10\n"
    "digital,D001,Photo Editor,49.90,100\n"
    "service,S001,Installation,30.00,5\n"
    "physical,P002,Office Chair,abc,3\n"
    "physical,P003,Monitor Stand,39.50,7\n"
)


class TestUserInput(unittest.TestCase):
    def test_get_positive_float_asks_again_until_valid(self) -> None:
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with redirect_stdout(output):
                value = get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(
            output.getvalue().splitlines(),
            [
                "Please enter a valid number, e.g. 12.50",
                "Please enter a number greater than zero.",
            ],
        )

    def test_get_non_negative_int_asks_again_until_valid(self) -> None:
        with patch("builtins.input", side_effect=["ten", "-1", "2.5", "0"]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(get_non_negative_int("Stock: "), 0)


class TestLoadProducts(unittest.TestCase):
    def setUp(self) -> None:
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "products.csv")
        with open(self.path, "w", encoding="utf-8", newline="") as file:
            file.write(CSV_TEXT)
        self.inventory = Inventory()

    def tearDown(self) -> None:
        self.folder.cleanup()

    def run_load(self, path: str) -> list[str]:
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(path, self.inventory, make_supplier())
        return output.getvalue().splitlines()

    def test_bad_rows_skipped_and_valid_rows_loaded(self) -> None:
        lines = self.run_load(self.path)
        ids = [p.get_product_id() for p in self.inventory.get_products()]
        self.assertEqual(ids, ["P001", "D001", "P003"])
        self.assertEqual(
            lines,
            [
                "Row 4 skipped: Unknown product type: service",
                "Row 5 skipped: could not convert string to float: 'abc'",
                "3 products loaded.",
                "Load attempt finished.",
            ],
        )

    def test_missing_file_handled_gracefully(self) -> None:
        missing = os.path.join(self.folder.name, "renamed.csv")
        lines = self.run_load(missing)
        self.assertEqual(
            lines,
            [f"Products file not found: {missing}", "Load attempt finished."],
        )
        self.assertEqual(self.inventory.get_products(), [])

    def test_duplicate_id_row_is_skipped(self) -> None:
        self.run_load(self.path)
        lines = self.run_load(self.path)  # loading the same file again
        self.assertIn("0 products loaded.", lines)
        self.assertEqual(len(self.inventory.get_products()), 3)


if __name__ == "__main__":
    unittest.main()
