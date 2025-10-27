"""
Inventory Management System

This module provides a class-based system to manage inventory stock data
including adding/removing items, checking quantities, and persisting data
to JSON files.
"""

import json
from datetime import datetime


class InventorySystem:
    """
    A class to manage inventory stock data with persistence capabilities.

    Attributes:
        stock_data (dict): Dictionary storing item names and quantities
        logs (list): List of log messages for inventory operations
    """

    def __init__(self):
        """Initialize an empty inventory system."""
        self.stock_data = {}
        self.logs = []

    def add_item(self, item=None, qty=0):
        """
        Add quantity to an item in the inventory.

        Args:
            item: Name of the item (string)
            qty: Quantity to add (positive integer)

        Returns:
            bool: True if successful, False otherwise
        """
        if not item or not isinstance(item, str):
            print("Error: Item must be a non-empty string")
            return False

        if not isinstance(qty, int) or qty <= 0:
            print("Error: Quantity must be a positive integer")
            return False

        self.stock_data[item] = self.stock_data.get(item, 0) + qty
        log_message = f"{datetime.now()}: Added {qty} of {item}"
        self.logs.append(log_message)
        print(log_message)
        return True

    def remove_item(self, item, qty):
        """
        Remove quantity from an item in the inventory.

        Args:
            item: Name of the item (string)
            qty: Quantity to remove (positive integer)

        Returns:
            bool: True if successful, False otherwise
        """
        if not isinstance(item, str) or not isinstance(qty, int):
            print("Error: Invalid item or quantity type")
            return False

        if qty <= 0:
            print("Error: Quantity must be positive")
            return False

        try:
            if item not in self.stock_data:
                print(f"Warning: Item '{item}' not found in inventory")
                return False

            self.stock_data[item] -= qty

            if self.stock_data[item] <= 0:
                print(
                    f"Info: Item '{item}' quantity reached zero, "
                    f"removing from inventory"
                )
                del self.stock_data[item]

            return True
        except KeyError as e:
            print(f"Error: Item not found - {e}")
            return False
        except TypeError as e:
            print(f"Error: Invalid operation - {e}")
            return False

    def get_qty(self, item):
        """
        Get the current quantity of an item.

        Args:
            item: Name of the item (string)

        Returns:
            int: Quantity of the item, or 0 if not found
        """
        if not isinstance(item, str):
            print("Error: Item must be a string")
            return 0

        return self.stock_data.get(item, 0)

    def load_data(self, file="inventory.json"):
        """
        Load inventory data from a JSON file.

        Args:
            file: Path to the JSON file (default: inventory.json)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(file, 'r', encoding='utf-8') as f:
                self.stock_data = json.load(f)
            print(f"Data loaded successfully from {file}")
            return True
        except FileNotFoundError:
            print(
                f"Warning: File '{file}' not found, "
                f"starting with empty inventory"
            )
            self.stock_data = {}
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format - {e}")
            return False
        except IOError as e:
            print(f"Error: Could not read file - {e}")
            return False

    def save_data(self, file="inventory.json"):
        """
        Save inventory data to a JSON file.

        Args:
            file: Path to the JSON file (default: inventory.json)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(self.stock_data, f, indent=2)
            print(f"Data saved successfully to {file}")
            return True
        except IOError as e:
            print(f"Error: Could not write to file - {e}")
            return False

    def print_data(self):
        """
        Print a formatted report of all items in the inventory.
        """
        print("\n" + "="*40)
        print("Items Report")
        print("="*40)

        if not self.stock_data:
            print("Inventory is empty")
        else:
            for item, qty in sorted(self.stock_data.items()):
                print(f"{item:20} -> {qty:5}")

        print("="*40 + "\n")

    def check_low_items(self, threshold=5):
        """
        Check for items with quantity below a threshold.

        Args:
            threshold: Minimum quantity threshold (default: 5)

        Returns:
            list: Items with quantity below threshold
        """
        if not isinstance(threshold, int) or threshold < 0:
            print("Error: Threshold must be a non-negative integer")
            return []

        result = []
        for item, qty in self.stock_data.items():
            if qty < threshold:
                result.append(item)

        return result


def main():
    """
    Main function to demonstrate inventory system functionality.
    """
    print("Starting Inventory Management System\n")

    # Create inventory instance
    inventory = InventorySystem()

    # Test adding items
    inventory.add_item("apple", 10)
    inventory.add_item("banana", 5)
    inventory.add_item("orange", 3)

    # Test invalid inputs (will be rejected)
    inventory.add_item("banana", -2)  # Negative quantity
    inventory.add_item(123, 10)  # Invalid type for item
    inventory.add_item("grape", "ten")  # Invalid type for quantity

    # Test removing items
    inventory.remove_item("apple", 3)
    inventory.remove_item("orange", 1)

    # Test getting quantity
    apple_qty = inventory.get_qty("apple")
    print(f"\nApple stock: {apple_qty}")

    # Test checking low items
    low_items = inventory.check_low_items()
    print(f"Low items (below 5): {low_items}")

    # Save and load data
    inventory.save_data()
    print("\nReloading data...")
    inventory.load_data()

    # Print final report
    inventory.print_data()


if __name__ == "__main__":
    main()
