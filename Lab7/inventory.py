class Inventory:
    """Store the information and behavior shared by all inventory products."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id().upper() == product_id.upper():
                return product
        return None

    def get_products(self):
        return self.__products

    def display_all(self):
        if not self.__products:
            print("Inventory is empty.")
            return

        print("\nCurrent Inventory")
        print("-" * 50)
        for product in self.__products:
            product.display_information()
            print("-" * 50)
