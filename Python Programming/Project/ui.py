# ui.py
# Handles all GUI operations

import tkinter as tk
from tkinter import messagebox

from inventory import (
    inventory, is_stock_available,
    reduce_stock, get_price, get_stock
)
from billing import calculate_bill
from receipt import create_receipt

cart = []

def start_application():
    window = tk.Tk()
    window.title("StockStream POS")
    window.geometry("450x500")

    tk.Label(window, text="Select Product").pack()

    product_var = tk.StringVar()
    product_var.set(list(inventory.keys())[0])

    tk.OptionMenu(window, product_var, *inventory.keys()).pack()

    tk.Label(window, text="Enter Quantity").pack()
    quantity_entry = tk.Entry(window)
    quantity_entry.pack()

    cart_box = tk.Listbox(window, width=45)
    cart_box.pack(pady=10)

    total_label = tk.Label(window, text="Total: ₹0")
    total_label.pack()

    def add_to_cart():
        product = product_var.get()

        try:
            quantity = int(quantity_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid quantity")
            return

        if not is_stock_available(product, quantity):
            messagebox.showerror("Error", "Not enough stock")
            return

        if get_stock(product) < 5:
            add_button.config(state=tk.DISABLED)
            messagebox.showwarning("Low Stock", "Stock below 5 units")

        cart.append({
            "name": product,
            "price": get_price(product),
            "quantity": quantity
        })

        cart_box.insert(tk.END, f"{product} x {quantity}")
        quantity_entry.delete(0, tk.END)

    def checkout():
        if not cart:
            messagebox.showwarning("Empty Cart", "No items in cart")
            return

        subtotal, gst, total = calculate_bill(cart)

        for item in cart:
            reduce_stock(item["name"], item["quantity"])

        receipt_path = create_receipt(cart, subtotal, gst, total)

        total_label.config(text=f"Total: ₹{total}")
        messagebox.showinfo("Success", f"Receipt saved:\n{receipt_path}")

        cart.clear()
        cart_box.delete(0, tk.END)

    add_button = tk.Button(window, text="Add to Cart", command=add_to_cart)
    add_button.pack(pady=5)

    tk.Button(window, text="Checkout", command=checkout).pack(pady=10)

    window.mainloop()
