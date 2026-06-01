import tkinter as tk
from tkinter import messagebox

# ----- Data -----
USERS = {"Brew Aura": "1234"}

menu = {
    1: {"name": "Espresso", "price": 100},
    2: {"name": "Latte", "price": 150},
    3: {"name": "Cappuccino", "price": 180},
    4: {"name": "Americano", "price": 120},
    5: {"name": "Mocha", "price": 200},
    6: {"name": "Cold Coffee", "price": 160},
    7: {"name": "Sandwich", "price": 120},
    8: {"name": "Burger", "price": 180},
    9: {"name": "French Fries", "price": 100},
    10: {"name": "Chocolate Cake", "price": 220}
}

cart = {}
logged_in = False

# ----- Window -----
root = tk.Tk()
root.title("BREW AURA ☕")
root.geometry("650x720")  
root.configure(bg="#FFE4EC")

# ----- Header -----
canvas = tk.Canvas(root, width=650, height=120, bg="#FFE4EC", highlightthickness=0)
canvas.pack()

canvas.create_rectangle(0, 0, 650, 120, fill="#FF69B4")
canvas.create_text(325, 40, text="☕ BREW AURA ☕", font=("Comic Sans MS", 24, "bold"), fill="white")
canvas.create_text(325, 80, text="Welcome!", font=("Comic Sans MS", 12), fill="white")

# ----- Cute Button -----
def cute_btn(parent, text, cmd):
    return tk.Button(parent, text=text, command=cmd,
                     bg="#FF69B4", fg="white",
                     font=("Comic Sans MS", 10, "bold"),
                     relief="flat", padx=6, pady=6)

# ----- Login -----
frame = tk.Frame(root, bg="#FFE4EC")
frame.pack(pady=5)

tk.Label(frame, text="Username", bg="#FFE4EC").grid(row=0, column=0)
tk.Label(frame, text="Password", bg="#FFE4EC").grid(row=1, column=0)

username_entry = tk.Entry(frame)
password_entry = tk.Entry(frame, show="*")

username_entry.grid(row=0, column=1)
password_entry.grid(row=1, column=1)

def login_user():
    global logged_in
    if USERS.get(username_entry.get()) == password_entry.get():
        logged_in = True
        messagebox.showinfo("Login", "Welcome to BREW AURA ☕")
        for btn in buttons:
            btn.config(state="normal")
        load_menu()
    else:
        messagebox.showerror("Error", "Invalid Login ❌")

tk.Button(frame, text="Login", command=login_user).grid(row=2, columnspan=2)

# ----- Menu List -----
menu_list = tk.Listbox(root, width=45)
menu_list.pack(pady=10)

def load_menu():
    menu_list.delete(0, tk.END)
    for i, item in menu.items():
        menu_list.insert(tk.END, f"{i}. {item['name']} - {item['price']} Tk")

# ----- Cart Functions -----
def get_selected_item():
    try:
        selected = menu_list.get(menu_list.curselection())
        return int(selected.split(".")[0])
    except:
        messagebox.showwarning("Warning", "Select an item first!")
        return None

def add_to_cart():
    i = get_selected_item()
    if i:
        cart[i] = cart.get(i, 0) + 1
        view_cart()

def remove_from_cart():
    i = get_selected_item()
    if i and i in cart:
        del cart[i]
        view_cart()

def update_quantity():
    i = get_selected_item()
    if not i:
        return
    try:
        qty = int(qty_entry.get())
        if qty <= 0:
            raise ValueError
        cart[i] = qty
        view_cart()
    except:
        messagebox.showerror("Error", "Enter valid quantity!")

def clear_cart():
    cart.clear()
    view_cart()

# ----- Billing -----
def calculate_total():
    return sum(menu[i]["price"] * q for i, q in cart.items())

def view_cart():
    cart_text.delete("1.0", tk.END)

    if not cart:
        cart_text.insert(tk.END, "Cart is empty 🥺")
        return

    total = calculate_total()
    discount = total * 0.1 if total > 500 else 0
    after_discount = total - discount
    tax = after_discount * 0.05
    final = after_discount + tax

    cart_text.insert(tk.END, "🛒 CART\n\n")

    for i, q in cart.items():
        item = menu[i]
        cart_text.insert(tk.END, f"{item['name']} x{q} = {item['price']*q} Tk\n")

    cart_text.insert(tk.END, "\n-----------------\n")
    cart_text.insert(tk.END, f"Subtotal: {total} Tk\n")
    cart_text.insert(tk.END, f"Discount: -{discount:.2f} Tk\n")
    cart_text.insert(tk.END, f"Tax: {tax:.2f} Tk\n")
    cart_text.insert(tk.END, f"Final: {final:.2f} Tk\n")

# ----- Order -----
def place_order():
    if not cart:
        messagebox.showwarning("Oops", "Cart is empty!")
        return

    total = calculate_total()
    discount = total * 0.1 if total > 500 else 0
    after_discount = total - discount
    tax = after_discount * 0.05
    final = after_discount + tax

    messagebox.showinfo("Receipt", f"""
BREW AURA ☕
-------------------
Subtotal: {total} Tk
Discount: -{discount:.2f} Tk
Tax: {tax:.2f} Tk
-------------------
Final: {final:.2f} Tk

Thank you!
""")

    clear_cart()

# ----- Exit -----
def exit_app():
    if messagebox.askyesno("Exit", "Exit app?"):
        root.destroy()

# ----- Buttons -----
btn1 = cute_btn(root, "Load Menu", load_menu)
btn2 = cute_btn(root, "Add to Cart", add_to_cart)
btn3 = cute_btn(root, "Remove Item", remove_from_cart)

btn1.pack()
btn2.pack()
btn3.pack()

# Quantity
qty_frame = tk.Frame(root, bg="#FFE4EC")
qty_frame.pack()

tk.Label(qty_frame, text="Qty:", bg="#FFE4EC").pack(side=tk.LEFT)
qty_entry = tk.Entry(qty_frame, width=5)
qty_entry.pack(side=tk.LEFT)

btn4 = cute_btn(qty_frame, "Update Qty", update_quantity)
btn4.pack(side=tk.LEFT)

btn5 = cute_btn(root, "Clear Cart", clear_cart)
btn6 = cute_btn(root, "View Cart", view_cart)
btn7 = cute_btn(root, "Place Order", place_order)
btn8 = cute_btn(root, "Exit", exit_app)

btn5.pack()
btn6.pack()
btn7.pack()

#  Bigger cart (visible)
cart_text = tk.Text(root, height=12, width=45)
cart_text.pack(pady=5)

btn8.pack()

# Disable before login
buttons = [btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8]
for b in buttons:
    b.config(state="disabled")

root.protocol("WM_DELETE_WINDOW", exit_app)
root.mainloop()