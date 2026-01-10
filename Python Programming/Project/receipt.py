# receipt.py
# Generates receipt after checkout

from datetime import datetime
import os

def create_receipt(cart, subtotal, gst, total):
    if not os.path.exists("receipts"):
        os.mkdir("receipts")

    time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"receipts/receipt_{time_stamp}.txt"

    with open(file_path, "w") as file:
        file.write("====== StockStream POS Receipt ======\n\n")

        for item in cart:
            line = f"{item['name']} x {item['quantity']} = ₹{item['price'] * item['quantity']}\n"
            file.write(line)

        file.write("\n----------------------------------\n")
        file.write(f"Subtotal: ₹{subtotal}\n")
        file.write(f"GST (12%): ₹{gst}\n")
        file.write(f"Total Amount: ₹{total}\n")
        file.write("\nThank you for shopping!\n")

    return file_path
