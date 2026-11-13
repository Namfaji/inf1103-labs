"""Shared test objects."""
from supplier import Supplier


def make_supplier() -> Supplier:
    return Supplier("S900", "Test Supplier", "test@example.com")
