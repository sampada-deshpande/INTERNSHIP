"""
logic.py - inventory and cart business logic + persistence
"""

import csv
import os
from datetime import datetime
from typing import Dict, List, Tuple
from models import Product


class InventoryManager:
    CSV_FIELDS = ["product_id", "name", "price", "stock"]

    def __init__(self, csv_path: str = None):
        # ALWAYS load inventory.csv from the same folder as this file
        if csv_path is None:
            csv_path = os.path.join(os.path.dirname(__file__), "inventory.csv")

        self.csv_path = csv_path
        self.products: Dict[str, Product] = {}
        self.load()

    def load(self):
        self.products = {}
        if not os.path.exists(self.csv_path):
            return

        with open(self.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                p = Product.from_dict(row)
                if p.product_id:
                    self.products[p.product_id] = p

    def save(self):
        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.CSV_FIELDS)
            writer.writeheader()
            for p in self.products.values():
                writer.writerow(p.to_dict())

    def list_products(self) -> List[Product]:
        return list(self.products.values())

    def get(self, product_id: str):
        return self.products.get(product_id)

    def is_add_allowed(self, product_id: str) -> bool:
        p = self.get(product_id)
        return bool(p and p.stock >= 5)

    def reduce_stock(self, product_id: str, qty: int) -> bool:
        p = self.get(product_id)
        if not p or qty <= 0 or p.stock < qty:
            return False
        p.stock -= qty
        self.save()
        return True


class Cart:
    TAX_RATE = 0.12  # 12% GST

    def __init__(self):
        self.items: Dict[str, int] = {}

    def add(self, product_id: str, qty: int):
        if qty > 0:
            self.items[product_id] = self.items.get(product_id, 0) + qty

    def remove(self, product_id: str):
        if product_id in self.items:
            del self.items[product_id]

    def clear(self):
        self.items.clear()

    def subtotal(self, inventory: InventoryManager) -> float:
        total = 0.0
        for pid, qty in self.items.items():
            p = inventory.get(pid)
            if p:
                total += p.price * qty
        return total

    def totals(self, inventory: InventoryManager) -> Tuple[float, float, float]:
        sub = round(self.subtotal(inventory), 2)
        tax = round(sub * self.TAX_RATE, 2)
        total = round(sub + tax, 2)
        return sub, tax, total

    def checkout(self, inventory: InventoryManager, receipts_dir="receipts"):
        # Validate stock
        for pid, qty in self.items.items():
            p = inventory.get(pid)
            if not p or p.stock < qty:
                return False, "Insufficient stock for checkout."

        # Reduce stock
        for pid, qty in self.items.items():
            inventory.reduce_stock(pid, qty)

        # Generate receipt
        os.makedirs(receipts_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        receipt_path = os.path.join(receipts_dir, f"receipt_{ts}.txt")

        sub, tax, total = self.totals(inventory)

        with open(receipt_path, "w", encoding="utf-8") as f:
            f.write("StockStream - Receipt\n")
            f.write(f"Date & Time: {datetime.now()}\n")
            f.write("-" * 40 + "\n")
            for pid, qty in self.items.items():
                p = inventory.get(pid)
                if p:
                    f.write(f"{p.name} | {qty} x {p.price:.2f} = {qty * p.price:.2f}\n")
            f.write("-" * 40 + "\n")
            f.write(f"Subtotal: {sub:.2f}\n")
            f.write(f"GST (12%): {tax:.2f}\n")
            f.write(f"Total: {total:.2f}\n")

        self.clear()
        return True, receipt_path
