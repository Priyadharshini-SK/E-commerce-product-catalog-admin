import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# =========================
# FILE SETUP
# =========================
PRODUCT_FILE = "products.json"
SALES_FILE = "sales.json"
CUSTOMER_FILE = "customers.json"
ADMIN_USER = "admin"
ADMIN_PASS = "1234"

# Colors
BG_DARK = "#0f0f1a"
BG_PANEL = "#1a1a2e"
BG_CARD = "#16213e"
ACCENT = "#e94560"
ACCENT2 = "#0f3460"
GREEN = "#4ecca3"
TEXT = "#eaeaea"
TEXT_DIM = "#888aaa"
ENTRY_BG = "#0d1b2a"

# =========================
# FILE UTILITIES
# =========================
def create_files():
    for filepath, default in [
        (PRODUCT_FILE, []),
        (SALES_FILE, []),
        (CUSTOMER_FILE, [])
    ]:
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump(default, f)

create_files()

def load_json(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def load_products():   return load_json(PRODUCT_FILE)
def save_products(d):  save_json(PRODUCT_FILE, d)
def load_sales():      return load_json(SALES_FILE)
def save_sales(d):     save_json(SALES_FILE, d)
def load_customers():  return load_json(CUSTOMER_FILE)
def save_customers(d): save_json(CUSTOMER_FILE, d)

# =========================
# MAIN WINDOW
# =========================
root = tk.Tk()
root.title("Smart E-Commerce Management System")
root.geometry("1300x750")
root.configure(bg=BG_DARK)
root.resizable(True, True)

cart = []

# =========================
# WIDGET HELPERS
# =========================
def styled_label(parent, text, font_size=12, bold=False, color=TEXT, bg=None):
    bg = bg or parent.cget("bg")
    weight = "bold" if bold else "normal"
    return tk.Label(parent, text=text, font=("Segoe UI", font_size, weight),
                    bg=bg, fg=color)

def styled_entry(parent, width=28):
    e = tk.Entry(parent, font=("Segoe UI", 12), width=width,
                 bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
                 relief="flat", bd=8)
    return e

def styled_button(parent, text, command, color=ACCENT, fg="white", width=22):
    return tk.Button(parent, text=text, command=command,
                     bg=color, fg=fg, font=("Segoe UI", 11, "bold"),
                     width=width, relief="flat", cursor="hand2",
                     activebackground=GREEN, activeforeground=BG_DARK, bd=0, pady=6)

def separator(parent, bg=ACCENT2):
    tk.Frame(parent, bg=bg, height=1).pack(fill="x", pady=6, padx=10)

# =========================
# LOGIN FRAME
# =========================
login_frame = tk.Frame(root, bg=BG_DARK)
login_frame.pack(fill="both", expand=True)

tk.Label(login_frame, text="⚡ SMART E-COMMERCE SYSTEM",
         font=("Segoe UI", 30, "bold"), bg=BG_DARK, fg=ACCENT).pack(pady=50)

login_box = tk.Frame(login_frame, bg=BG_PANEL, padx=50, pady=40,
                     highlightbackground=ACCENT, highlightthickness=2)
login_box.pack()

styled_label(login_box, "Username", 13, bg=BG_PANEL).pack(anchor="w")
user_entry = styled_entry(login_box)
user_entry.pack(pady=(4, 14))

styled_label(login_box, "Password", 13, bg=BG_PANEL).pack(anchor="w")
pass_entry = styled_entry(login_box)
pass_entry.config(show="*")
pass_entry.pack(pady=(4, 14))

def login():
    if user_entry.get() == ADMIN_USER and pass_entry.get() == ADMIN_PASS:
        login_frame.pack_forget()
        dashboard_frame.pack(fill="both", expand=True)
        refresh_products()
        refresh_sales()
        refresh_customers()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

styled_button(login_box, "LOGIN", login, color=ACCENT, width=28).pack(pady=10)
styled_label(login_box, "Default: admin / 1234", 9, color=TEXT_DIM, bg=BG_PANEL).pack()

root.bind("<Return>", lambda e: login())

# =========================
# DASHBOARD FRAME
# =========================
dashboard_frame = tk.Frame(root, bg=BG_DARK)

header = tk.Frame(dashboard_frame, bg=ACCENT2, pady=10)
header.pack(fill="x")
tk.Label(header, text="⚡ SMART E-COMMERCE DASHBOARD",
         font=("Segoe UI", 20, "bold"), bg=ACCENT2, fg=TEXT).pack()

main_area = tk.Frame(dashboard_frame, bg=BG_DARK)
main_area.pack(fill="both", expand=True)

# =========================
# LEFT PANEL
# =========================
left_panel = tk.Frame(main_area, bg=BG_PANEL, width=320)
left_panel.pack(side="left", fill="y", padx=(10, 5), pady=10)
left_panel.pack_propagate(False)

# ---- ADD PRODUCT ----
styled_label(left_panel, "➕ ADD / EDIT PRODUCT", 14, bold=True,
             color=GREEN, bg=BG_PANEL).pack(pady=(14, 4))
separator(left_panel)

styled_label(left_panel, "Product Name", bg=BG_PANEL).pack(anchor="w", padx=16)
name_entry = styled_entry(left_panel)
name_entry.pack(pady=(2, 8))

styled_label(left_panel, "Category", bg=BG_PANEL).pack(anchor="w", padx=16)
cat_entry = styled_entry(left_panel)
cat_entry.pack(pady=(2, 8))

styled_label(left_panel, "Price (₹)", bg=BG_PANEL).pack(anchor="w", padx=16)
price_entry = styled_entry(left_panel)
price_entry.pack(pady=(2, 8))

styled_label(left_panel, "Stock Quantity", bg=BG_PANEL).pack(anchor="w", padx=16)
qty_entry = styled_entry(left_panel)
qty_entry.pack(pady=(2, 8))

selected_product_index = [None]

def clear_product_fields():
    for e in [name_entry, cat_entry, price_entry, qty_entry]:
        e.delete(0, tk.END)
    selected_product_index[0] = None
    add_btn.config(text="ADD PRODUCT", bg=ACCENT)

def add_product():
    name     = name_entry.get().strip()
    category = cat_entry.get().strip()
    price    = price_entry.get().strip()
    quantity = qty_entry.get().strip()

    if not all([name, category, price, quantity]):
        messagebox.showwarning("Missing Fields", "Please fill all product fields.")
        return

    try:
        price_val = float(price)
        qty_val   = int(quantity)
        if price_val < 0 or qty_val < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Price must be a positive number and quantity a positive integer.")
        return

    products = load_products()

    if selected_product_index[0] is not None:
        idx = selected_product_index[0]
        products[idx].update({"name": name, "category": category,
                               "price": price_val, "quantity": qty_val})
        save_products(products)
        messagebox.showinfo("Updated", f'"{name}" updated successfully!')
        clear_product_fields()
    else:
        # Duplicate check
        if any(p["name"].lower() == name.lower() for p in products):
            messagebox.showwarning("Duplicate", f'Product "{name}" already exists.')
            return
        products.append({"name": name, "category": category,
                          "price": price_val, "quantity": qty_val})
        save_products(products)
        messagebox.showinfo("Success", f'"{name}" added successfully!')
        clear_product_fields()

    refresh_products()

add_btn = styled_button(left_panel, "ADD PRODUCT", add_product, color=ACCENT)
add_btn.pack(pady=4)
styled_button(left_panel, "CLEAR FIELDS", clear_product_fields, color=ACCENT2).pack(pady=2)

separator(left_panel)

# ---- CUSTOMER BILLING ----
styled_label(left_panel, "🧾 CUSTOMER BILLING", 14, bold=True,
             color=GREEN, bg=BG_PANEL).pack(pady=(8, 4))

styled_label(left_panel, "Customer Name", bg=BG_PANEL).pack(anchor="w", padx=16)
customer_name_entry = styled_entry(left_panel)
customer_name_entry.pack(pady=(2, 8))

styled_label(left_panel, "Customer Phone", bg=BG_PANEL).pack(anchor="w", padx=16)
customer_phone_entry = styled_entry(left_panel)
customer_phone_entry.pack(pady=(2, 8))

# ---- CART ----
cart_label = styled_label(left_panel, "🛒 Cart: 0 items | ₹0.00",
                          10, color=TEXT_DIM, bg=BG_PANEL)
cart_label.pack()

def update_cart_label():
    total = sum(item["price"] * item["qty"] for item in cart)
    count = sum(item["qty"] for item in cart)
    cart_label.config(text=f"🛒 Cart: {count} item(s) | ₹{total:.2f}")

def add_to_cart():
    selected = product_tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Select a product from the list.")
        return
    idx = product_tree.index(selected[0])
    products = load_products()
    prod = products[idx]
    if prod["quantity"] <= 0:
        messagebox.showerror("Out of Stock", f'"{prod["name"]}" is out of stock.')
        return

    for item in cart:
        if item["name"] == prod["name"]:
            if item["qty"] >= prod["quantity"]:
                messagebox.showwarning("Stock Limit", "Not enough stock.")
                return
            item["qty"] += 1
            update_cart_label()
            return

    cart.append({"name": prod["name"], "price": prod["price"], "qty": 1,
                 "category": prod["category"]})
    update_cart_label()
    messagebox.showinfo("Cart", f'"{prod["name"]}" added to cart.')

def view_cart():
    if not cart:
        messagebox.showinfo("Cart", "Cart is empty.")
        return
    win = tk.Toplevel(root)
    win.title("🛒 Cart")
    win.geometry("500x400")
    win.configure(bg=BG_DARK)
    styled_label(win, "CART ITEMS", 16, bold=True, color=GREEN, bg=BG_DARK).pack(pady=10)

    cols = ("Product", "Qty", "Unit Price", "Total")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=10)
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=110, anchor="center")

    grand = 0
    for item in cart:
        t = item["price"] * item["qty"]
        grand += t
        tree.insert("", "end", values=(item["name"], item["qty"],
                                        f"₹{item['price']:.2f}", f"₹{t:.2f}"))
    tree.pack(fill="both", expand=True, padx=10)
    styled_label(win, f"Grand Total: ₹{grand:.2f}", 14, bold=True,
                 color=ACCENT, bg=BG_DARK).pack(pady=10)

styled_button(left_panel, "ADD TO CART", add_to_cart, color=GREEN, fg=BG_DARK).pack(pady=4)
styled_button(left_panel, "VIEW CART", view_cart, color=ACCENT2).pack(pady=2)

# =========================
# RIGHT PANEL (TABS)
# =========================
right_panel = tk.Frame(main_area, bg=BG_DARK)
right_panel.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background=BG_DARK, borderwidth=0)
style.configure("TNotebook.Tab", background=ACCENT2, foreground=TEXT,
                font=("Segoe UI", 11, "bold"), padding=[14, 6])
style.map("TNotebook.Tab", background=[("selected", ACCENT)])
style.configure("Treeview", background=BG_CARD, foreground=TEXT,
                fieldbackground=BG_CARD, rowheight=28,
                font=("Segoe UI", 11))
style.configure("Treeview.Heading", background=ACCENT2, foreground=TEXT,
                font=("Segoe UI", 11, "bold"))
style.map("Treeview", background=[("selected", ACCENT)])

notebook = ttk.Notebook(right_panel)
notebook.pack(fill="both", expand=True)

# ==================
# TAB 1 – PRODUCTS
# ==================
prod_tab = tk.Frame(notebook, bg=BG_DARK)
notebook.add(prod_tab, text="  📦 Products  ")

prod_top = tk.Frame(prod_tab, bg=BG_DARK)
prod_top.pack(fill="x", pady=(8, 4))

styled_label(prod_top, "Search:", bg=BG_DARK).pack(side="left", padx=8)
search_var = tk.StringVar()
search_entry = tk.Entry(prod_top, textvariable=search_var, font=("Segoe UI", 12),
                        bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT, relief="flat", bd=6, width=22)
search_entry.pack(side="left")

def search_products(*args):
    keyword = search_var.get().lower()
    products = load_products()
    product_tree.delete(*product_tree.get_children())
    for p in products:
        if keyword in p["name"].lower() or keyword in p["category"].lower():
            status = "✅ In Stock" if p["quantity"] > 0 else "❌ Out of Stock"
            product_tree.insert("", "end",
                                values=(p["name"], p["category"],
                                        f"₹{p['price']:.2f}", p["quantity"], status))

search_var.trace("w", search_products)

styled_button(prod_top, "DELETE SELECTED", lambda: delete_product(),
              color="#c0392b", width=18).pack(side="right", padx=6)
styled_button(prod_top, "EDIT SELECTED", lambda: edit_product(),
              color=ACCENT2, width=16).pack(side="right", padx=4)

prod_cols = ("Name", "Category", "Price", "Stock", "Status")
product_tree = ttk.Treeview(prod_tab, columns=prod_cols, show="headings", height=18)
for col, w in zip(prod_cols, [200, 140, 100, 80, 120]):
    product_tree.heading(col, text=col)
    product_tree.column(col, width=w, anchor="center")

product_tree.pack(fill="both", expand=True, padx=6, pady=4)
prod_scroll = ttk.Scrollbar(prod_tab, orient="vertical", command=product_tree.yview)
product_tree.configure(yscrollcommand=prod_scroll.set)

def refresh_products():
    product_tree.delete(*product_tree.get_children())
    for p in load_products():
        status = "✅ In Stock" if p["quantity"] > 0 else "❌ Out of Stock"
        product_tree.insert("", "end",
                            values=(p["name"], p["category"],
                                    f"₹{p['price']:.2f}", p["quantity"], status))

def delete_product():
    selected = product_tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Select a product to delete.")
        return
    idx = product_tree.index(selected[0])
    products = load_products()
    name = products[idx]["name"]
    if messagebox.askyesno("Confirm Delete", f'Delete "{name}"?'):
        products.pop(idx)
        save_products(products)
        refresh_products()
        messagebox.showinfo("Deleted", f'"{name}" deleted.')

def edit_product():
    selected = product_tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Select a product to edit.")
        return
    idx = product_tree.index(selected[0])
    products = load_products()
    p = products[idx]
    name_entry.delete(0, tk.END);  name_entry.insert(0, p["name"])
    cat_entry.delete(0, tk.END);   cat_entry.insert(0, p["category"])
    price_entry.delete(0, tk.END); price_entry.insert(0, str(p["price"]))
    qty_entry.delete(0, tk.END);   qty_entry.insert(0, str(p["quantity"]))
    selected_product_index[0] = idx
    add_btn.config(text="UPDATE PRODUCT", bg=GREEN)

# ==================
# TAB 2 – BILLING
# ==================
bill_tab = tk.Frame(notebook, bg=BG_DARK)
notebook.add(bill_tab, text="  🧾 Billing  ")

def generate_bill():
    customer_name  = customer_name_entry.get().strip()
    customer_phone = customer_phone_entry.get().strip()

    if not customer_name or not customer_phone:
        messagebox.showwarning("Missing Info", "Enter customer name and phone.")
        return
    if not cart:
        messagebox.showwarning("Empty Cart", "Add items to cart before billing.")
        return
    if not customer_phone.isdigit() or len(customer_phone) < 10:
        messagebox.showerror("Invalid Phone", "Enter a valid 10-digit phone number.")
        return

    products = load_products()
    total = 0
    bill_lines = []
    bill_lines.append("=" * 45)
    bill_lines.append("       SMART E-COMMERCE SYSTEM")
    bill_lines.append("=" * 45)
    bill_lines.append(f"Customer : {customer_name}")
    bill_lines.append(f"Phone    : {customer_phone}")
    bill_lines.append(f"Date     : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    bill_lines.append("-" * 45)
    bill_lines.append(f"{'Item':<20}{'Qty':>5}{'Price':>10}{'Total':>10}")
    bill_lines.append("-" * 45)

    for item in cart:
        t = item["price"] * item["qty"]
        total += t
        bill_lines.append(f"{item['name']:<20}{item['qty']:>5}₹{item['price']:>8.2f}₹{t:>8.2f}")
        # Deduct stock
        for p in products:
            if p["name"] == item["name"]:
                p["quantity"] -= item["qty"]

    save_products(products)
    bill_lines.append("=" * 45)
    bill_lines.append(f"{'GRAND TOTAL':>35} ₹{total:.2f}")
    bill_lines.append("=" * 45)
    bill_lines.append("       Thank you for shopping with us!")
    bill_lines.append("=" * 45)

    bill_text = "\n".join(bill_lines)

    # Save sale record
    sales = load_sales()
    sales.append({
        "customer": customer_name,
        "phone": customer_phone,
        "amount": total,
        "items": [{"name": i["name"], "qty": i["qty"], "price": i["price"]} for i in cart],
        "date": str(datetime.now())
    })
    save_sales(sales)

    # Save customer
    customers = load_customers()
    customers.append({"name": customer_name, "phone": customer_phone,
                       "date": str(datetime.now()), "total_spent": total})
    save_customers(customers)

    # Show bill window
    bill_win = tk.Toplevel(root)
    bill_win.title("Invoice")
    bill_win.geometry("520x480")
    bill_win.configure(bg=BG_DARK)
    styled_label(bill_win, "INVOICE", 16, bold=True, color=GREEN, bg=BG_DARK).pack(pady=8)
    text_box = tk.Text(bill_win, font=("Courier", 11), bg=ENTRY_BG, fg=TEXT,
                       relief="flat", padx=10, pady=10)
    text_box.pack(fill="both", expand=True, padx=10, pady=4)
    text_box.insert("1.0", bill_text)
    text_box.config(state="disabled")

    def save_bill():
        fname = f"bill_{customer_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        with open(fname, "w") as f:
            f.write(bill_text)
        messagebox.showinfo("Saved", f"Bill saved as {fname}")

    styled_button(bill_win, "SAVE BILL TO FILE", save_bill, color=GREEN, fg=BG_DARK).pack(pady=6)

    cart.clear()
    update_cart_label()
    customer_name_entry.delete(0, tk.END)
    customer_phone_entry.delete(0, tk.END)
    refresh_products()
    refresh_sales()
    refresh_customers()

styled_label(bill_tab, "Generate Bill", 16, bold=True, color=GREEN, bg=BG_DARK).pack(pady=14)
styled_label(bill_tab, "Fill customer details in the left panel, add items to cart, then click Generate Bill.",
             11, color=TEXT_DIM, bg=BG_DARK).pack()
styled_button(bill_tab, "GENERATE BILL", generate_bill, color=ACCENT, width=28).pack(pady=20)

# Summary in billing tab
bill_summary_frame = tk.Frame(bill_tab, bg=BG_PANEL, padx=20, pady=20)
bill_summary_frame.pack(pady=10, padx=20, fill="x")
styled_label(bill_summary_frame, "Quick Summary", 13, bold=True, color=GREEN, bg=BG_PANEL).pack(anchor="w")
summary_text = styled_label(bill_summary_frame, "", 11, color=TEXT_DIM, bg=BG_PANEL)
summary_text.pack(anchor="w", pady=4)

def update_summary():
    products  = load_products()
    sales     = load_sales()
    customers = load_customers()
    total_rev = sum(s["amount"] for s in sales)
    low_stock = [p for p in products if p["quantity"] <= 5]
    summary_text.config(text=(
        f"📦 Total Products: {len(products)}\n"
        f"💰 Total Revenue: ₹{total_rev:.2f}\n"
        f"🧾 Total Sales: {len(sales)}\n"
        f"👥 Total Customers: {len(customers)}\n"
        f"⚠️  Low Stock Items (≤5): {len(low_stock)}"
    ))

# ==================
# TAB 3 – SALES
# ==================
sales_tab = tk.Frame(notebook, bg=BG_DARK)
notebook.add(sales_tab, text="  📊 Sales History  ")

sale_cols = ("Date", "Customer", "Phone", "Amount")
sales_tree = ttk.Treeview(sales_tab, columns=sale_cols, show="headings", height=18)
for col, w in zip(sale_cols, [200, 160, 130, 130]):
    sales_tree.heading(col, text=col)
    sales_tree.column(col, width=w, anchor="center")
sales_tree.pack(fill="both", expand=True, padx=6, pady=8)

sales_footer = tk.Frame(sales_tab, bg=BG_DARK)
sales_footer.pack(fill="x", padx=10, pady=4)
sales_total_label = styled_label(sales_footer, "Total Revenue: ₹0.00",
                                  13, bold=True, color=GREEN, bg=BG_DARK)
sales_total_label.pack(side="left")

def refresh_sales():
    sales_tree.delete(*sales_tree.get_children())
    sales = load_sales()
    total = 0
    for s in reversed(sales):
        date_str = s.get("date", "")[:19]
        sales_tree.insert("", "end",
                          values=(date_str, s.get("customer", ""),
                                  s.get("phone", ""), f"₹{s.get('amount', 0):.2f}"))
        total += s.get("amount", 0)
    sales_total_label.config(text=f"Total Revenue: ₹{total:.2f}")
    update_summary()

# ==================
# TAB 4 – CUSTOMERS
# ==================
cust_tab = tk.Frame(notebook, bg=BG_DARK)
notebook.add(cust_tab, text="  👥 Customers  ")

cust_cols = ("Name", "Phone", "Date", "Spent")
cust_tree = ttk.Treeview(cust_tab, columns=cust_cols, show="headings", height=18)
for col, w in zip(cust_cols, [180, 140, 200, 120]):
    cust_tree.heading(col, text=col)
    cust_tree.column(col, width=w, anchor="center")
cust_tree.pack(fill="both", expand=True, padx=6, pady=8)

def refresh_customers():
    cust_tree.delete(*cust_tree.get_children())
    for c in reversed(load_customers()):
        cust_tree.insert("", "end",
                         values=(c.get("name", ""), c.get("phone", ""),
                                 c.get("date", "")[:19],
                                 f"₹{c.get('total_spent', 0):.2f}"))

# ==================
# TAB 5 – ANALYTICS
# ==================
analytics_tab = tk.Frame(notebook, bg=BG_DARK)
notebook.add(analytics_tab, text="  📈 Analytics  ")

analytics_canvas = tk.Canvas(analytics_tab, bg=BG_CARD, bd=0, highlightthickness=0)
analytics_canvas.pack(fill="both", expand=True, padx=10, pady=10)

def draw_analytics():
    analytics_canvas.delete("all")
    sales = load_sales()
    products = load_products()

    W = analytics_canvas.winfo_width() or 800
    H = analytics_canvas.winfo_height() or 400

    if not sales:
        analytics_canvas.create_text(W//2, H//2, text="No sales data yet.",
                                     font=("Segoe UI", 16), fill=TEXT_DIM)
        return

    # Bar chart – recent sales amounts
    analytics_canvas.create_text(W//2, 20,
                                  text="Recent Sales Amounts",
                                  font=("Segoe UI", 14, "bold"), fill=GREEN)

    recent = sales[-12:]
    amounts = [s["amount"] for s in recent]
    max_amt = max(amounts) if amounts else 1
    bar_area_top = 50
    bar_area_bottom = H - 60
    bar_area_left = 60
    bar_area_right = W - 40
    bar_w = (bar_area_right - bar_area_left) // max(len(recent), 1)
    bar_gap = 8

    for i, (s, amt) in enumerate(zip(recent, amounts)):
        bh = ((amt / max_amt) * (bar_area_bottom - bar_area_top))
        x0 = bar_area_left + i * bar_w + bar_gap
        x1 = x0 + bar_w - bar_gap * 2
        y0 = bar_area_bottom - bh
        y1 = bar_area_bottom
        analytics_canvas.create_rectangle(x0, y0, x1, y1, fill=ACCENT, outline="")
        analytics_canvas.create_text((x0 + x1)//2, y0 - 10,
                                      text=f"₹{int(amt)}", font=("Segoe UI", 8), fill=TEXT)
        name = s.get("customer", "?")[:6]
        analytics_canvas.create_text((x0 + x1)//2, bar_area_bottom + 14,
                                      text=name, font=("Segoe UI", 8), fill=TEXT_DIM)

    # Y-axis labels
    for i in range(5):
        y = bar_area_bottom - i * (bar_area_bottom - bar_area_top) / 4
        val = int(max_amt * i / 4)
        analytics_canvas.create_text(50, y, text=f"₹{val}", font=("Segoe UI", 8), fill=TEXT_DIM)
        analytics_canvas.create_line(bar_area_left, y, bar_area_right, y,
                                      fill=ACCENT2, dash=(2, 4))

    # Low stock warning panel
    low = [p for p in products if p["quantity"] <= 5]
    if low:
        analytics_canvas.create_text(W//2, H - 20,
                                      text="⚠️  Low Stock: " + ", ".join(p["name"] for p in low[:5]),
                                      font=("Segoe UI", 10, "bold"), fill=ACCENT)

analytics_btn = styled_button(analytics_tab, "REFRESH CHART", draw_analytics,
                               color=ACCENT2, width=20)
analytics_btn.pack()
analytics_canvas.bind("<Configure>", lambda e: draw_analytics())

# ==================
# BOTTOM STATUS BAR
# ==================
status_bar = tk.Frame(dashboard_frame, bg=ACCENT2, pady=4)
status_bar.pack(fill="x", side="bottom")
status_label = tk.Label(status_bar,
                         text=f"Logged in as: {ADMIN_USER}  |  {datetime.now().strftime('%d %b %Y')}",
                         font=("Segoe UI", 9), bg=ACCENT2, fg=TEXT_DIM)
status_label.pack(side="left", padx=14)

def logout():
    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        cart.clear()
        update_cart_label()
        dashboard_frame.pack_forget()
        user_entry.delete(0, tk.END)
        pass_entry.delete(0, tk.END)
        login_frame.pack(fill="both", expand=True)

styled_button(status_bar, "LOGOUT", logout, color=ACCENT, fg="white", width=10).pack(side="right", padx=10)

# =========================
# LAUNCH
# =========================
root.mainloop()