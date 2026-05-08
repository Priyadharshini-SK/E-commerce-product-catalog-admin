⚡ Smart E-Commerce Management System

A full-featured desktop application built with Python & Tkinter for managing an e-commerce business — products, billing, customers, sales history, and analytics — all from a single offline-ready interface.

---

FEATURES

- Secure Admin Login — password-protected access gate
- Product Management — add, edit, delete, search with duplicate detection and stock tracking
- Cart-Based Billing — multi-item cart with auto invoice generation and save-to-file
- Live Analytics Chart — canvas-rendered bar chart of recent sales with low-stock warnings
- Customer Database — auto-logs every customer with purchase date and total spent
- Sales History — reverse-chronological transaction log with running revenue total
- Real-Time Search — instant product filter by name or category on every keystroke
- Invoice Export — saves bills as timestamped .txt files
- Low Stock Alerts — flags products at or below 5 units

---

TECH STACK

Python 3.x — Core language
Tkinter — GUI framework
ttk (Themed Tkinter) — Styled widgets: Treeview, Notebook, Scrollbar
JSON — Local data persistence
datetime — Transaction timestamping
os — File system setup on startup

No external libraries required. Runs on pure Python standard library.

---

PROJECT STRUCTURE

smart-ecommerce/
├── main.py              → Full application source
├── products.json        → Product data (auto-created)
├── sales.json           → Sales records (auto-created)
├── customers.json       → Customer log (auto-created)
└── README.md

---

INSTALLATION & SETUP

Prerequisites
- Python 3.7 or above
- Tkinter (bundled with Python on Windows/macOS)

Linux users — install Tkinter first:
    sudo apt-get install python3-tk
---

DEFAULT LOGIN

Username : admin
Password : 1234

---

HOW TO USE

1. Login with admin credentials
2. Add Products using the left panel — name, category, price, stock quantity
3. Build a Cart — select a product from the list and click Add to Cart
4. Enter Customer Details — name and 10-digit phone number
5. Generate Bill — auto-deducts stock and logs the sale
6. View Reports — check the Sales, Customers, and Analytics tabs
7. Logout safely from the bottom status bar

---

MODULES OVERVIEW

Products Tab     — Full CRUD with inline search and stock status badges
Billing Tab      — Cart checkout with formatted invoice and quick summary KPIs
Sales History    — All transactions in reverse order with grand total revenue
Customers Tab    — Customer log with name, phone, date, and spending
Analytics Tab    — Bar chart of last 12 sales with low-stock product footer alert

---

FUTURE ENHANCEMENTS

Phase 1 — Short Term (0–3 Months)
- SQLite / PostgreSQL database backend
- PDF invoice generation using ReportLab or WeasyPrint
- Advanced multi-field product search and sorting
- Monthly/weekly sales trend charts with matplotlib

Phase 2 — Mid Term (3–9 Months)
- Web interface with Flask + React for multi-device access
- Multi-user role system (Admin, Cashier, Viewer)
- Barcode / QR code scanner integration for fast billing
- Automated low-stock email/SMS alerts via Twilio or SMTP

Phase 3 — Long Term (9–18 Months)
- Cloud deployment on AWS / Azure with remote data sync
- AI-powered demand forecasting and restocking suggestions
- Mobile companion app using Flutter or React Native
- Payment gateway integration — Razorpay, Stripe, UPI

Built with Python & Tkinter | 2025–2026
