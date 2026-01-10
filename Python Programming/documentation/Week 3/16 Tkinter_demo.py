import tkinter as tk

window = tk.Tk()
window.title("My First Tkinter App")
window.geometry("300x200")

label = tk.Label(window, text="Hello, Tkinter!", font=("Arial", 14))
label.pack(pady=20)

window.mainloop()

print("Window closed")   # 👈 ADD THIS
