"""
main.py - Tkinter GUI for StockStream
Run this file to start the application
"""

import tkinter as tk
from tkinter import ttk, messagebox
from logic import InventoryManager, Cart


class StockStreamApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("StockStream - Retail Inventory & Billing")
        self.root.geometry("900x520")

        self.inventory = InventoryManager()
        self.cart = Cart()

        # ---------- BUTTON STYLES ----------
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Green.TButton",
            background="#2ecc71",
            foreground="black",
            font=("Segoe UI", 10, "bold")
        )
        style.map("Green.TButton", background=[("active", "#27ae60")])

        style.configure(
            "Yellow.TButton",
            background="#f1c40f",
            foreground="black",
            font=("Segoe UI", 10, "bold")
        )
        style.map("Yellow.TButton", background=[("active", "#d4ac0d")])
        # ----------------------------------

        self.create_widgets()
        self.populate_products()

    def create_widgets(self):
        # -------- Inventory --------
        left = ttk.Frame(self.root)
        left.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        ttk.Label(left, text="Inventory").pack(anchor="w")

        cols = ("product_id", "name", "price", "stock")
        self.tree = ttk.Treeview(left, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=120)
        self.tree.pack(fill="both", expand=True)

        # 🔹 Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_product_select)

        control = ttk.Frame(left)
        control.pack(fill="x", pady=5)

        ttk.Label(control, text="Qty:").pack(side="left")
        self.qty_var = tk.IntVar(value=1)
        ttk.Spinbox(control, from_=1, to=100, textvariable=self.qty_var, width=5)\
            .pack(side="left", padx=5)

        # 🔹 Store Add button reference
        self.add_btn = ttk.Button(
            control,
            text="Add to Cart",
            command=self.add_to_cart,
            style="Green.TButton",
            state="disabled"
        )
        self.add_btn.pack(side="left")

        # -------- Cart --------
        right = ttk.Frame(self.root)
        right.pack(side="right", fill="both", padx=8, pady=8)

        ttk.Label(right, text="Cart").pack(anchor="w")

        self.cart_tree = ttk.Treeview(
            right, columns=("product_id", "name", "qty"), show="headings"
        )
        for c in ("product_id", "name", "qty"):
            self.cart_tree.heading(c, text=c.title())
            self.cart_tree.column(c, width=120)
        self.cart_tree.pack(fill="both", expand=True)

        ttk.Button(
            right,
            text="Remove Selected from Cart",
            command=self.remove_from_cart,
            style="Yellow.TButton"
        ).pack(fill="x", pady=5)

        ttk.Button(
            right,
            text="Checkout",
            command=self.checkout,
            style="Green.TButton"
        ).pack(fill="x")

    def populate_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for p in self.inventory.list_products():
            self.tree.insert(
                "",
                "end",
                iid=p.product_id,
                values=(p.product_id, p.name, f"{p.price:.2f}", p.stock)
            )

    # 🔹 ENABLE / DISABLE ADD TO CART BASED ON STOCK
    def on_product_select(self, event=None):
        selected = self.tree.selection()
        if not selected:
            self.add_btn.config(state="disabled")
            return

        pid = selected[0]
        if self.inventory.is_add_allowed(pid):
            self.add_btn.config(state="normal")
        else:
            self.add_btn.config(state="disabled")

    def add_to_cart(self):
        selected = self.tree.selection()
        if not selected:
            return

        pid = selected[0]
        qty = self.qty_var.get()
        product = self.inventory.get(pid)

        if not product or product.stock < qty:
            messagebox.showerror("Stock Error", "Insufficient stock.")
            return

        self.cart.add(pid, qty)
        self.refresh_cart()

    def refresh_cart(self):
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)

        for pid, qty in self.cart.items.items():
            p = self.inventory.get(pid)
            if p:
                self.cart_tree.insert("", "end", iid=pid, values=(pid, p.name, qty))

    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if selected:
            self.cart.remove(selected[0])
            self.refresh_cart()

    def checkout(self):
        success, msg = self.cart.checkout(self.inventory)
        if success:
            messagebox.showinfo("Success", f"Checkout complete!\nReceipt:\n{msg}")
            self.populate_products()
            self.refresh_cart()
        else:
            messagebox.showerror("Error", msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = StockStreamApp(root)
    root.mainloop()
