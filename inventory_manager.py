
import json
from pathlib import Path

INVENTORY_FILE = Path(__file__).resolve().with_name("inventory.json")
inventory = []

def load_inventory():
    global inventory

    if not INVENTORY_FILE.exists():
        print("inventory.json not found. Starting with an empty inventory.")
        inventory = []
        return inventory

    with INVENTORY_FILE.open("r") as file:
        inventory = json.load(file)

    print("inventory.json found.")
    print("Inventory loaded successfully.")
    return inventory

load_inventory()









