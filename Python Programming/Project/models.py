"""
models.py - product data model
"""
from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class Product:
    product_id: str
    name: str
    price: float
    stock: int

    def to_dict(self) -> Dict[str, str]:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": f"{self.price:.2f}",
            "stock": str(self.stock),
        }

    @staticmethod
    def from_dict(d: Dict[str, str]) -> "Product":
        return Product(
            product_id=d.get("product_id", "").strip(),
            name=d.get("name", "").strip(),
            price=float(d.get("price", "0") or 0),
            stock=int(d.get("stock", "0") or 0),
        )