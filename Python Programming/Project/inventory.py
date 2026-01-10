# inventory.py
# This file manages product data and stock operations

inventory = {
    "Shirt": {"price": 500, "stock": 10},
    "Jeans": {"price": 1200, "stock": 6},
    "Shoes": {"price": 2000, "stock": 4},
    "Jacket": {"price": 2500, "stock": 8}
}

def is_stock_available(product, quantity):
    """Check if requested quantity is available"""
    return inventory[product]["stock"] >= quantity

def reduce_stock(product, quantity):
    """Reduce stock after successful checkout"""
    inventory[product]["stock"] -= quantity

def get_price(product):
    return inventory[product]["price"]

def get_stock(product):
    return inventory[product]["stock"]
