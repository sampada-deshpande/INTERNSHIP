# billing.py
# Handles billing calculations

GST_RATE = 0.12

def calculate_bill(cart):
    subtotal = 0

    for item in cart:
        subtotal += item["price"] * item["quantity"]

    gst = subtotal * GST_RATE
    total = subtotal + gst

    return subtotal, gst, total
