from product import DigitalProduct, PhysicalProduct, Product
from supplier import Supplier


class ProductFactory:
    """Factory pattern: the one place that decides which Product class to build."""

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        weight_or_size: float = 0.0,
    ) -> Product:
        """Return a Product. weight_or_size is kg for physical, MB for digital."""
        kind: str = product_type.strip().lower()
        if kind == "physical":
            return PhysicalProduct(
                product_id, name, price, stock_quantity, supplier, weight_or_size
            )
        elif kind == "digital":
            return DigitalProduct(
                product_id, name, price, stock_quantity, supplier, weight_or_size
            )
        else:
            raise ValueError(f"Unknown product type: {product_type}")
