import tkinter as tk
from tkinter import messagebox
import mysql.connector

# MySQL Connection
def connect_db():
    try:
        con = mysql.connector.connect(
            host="localhost",  # Use your MySQL host (usually 'localhost')
            user="root",  # Replace with your MySQL username
            password="root",  # Replace with your MySQL password
            database="ecommerce"  # Ensure the 'ecommerce' database exists
        )
        print("Connected to database!")  # Debugging line
        return con
    except mysql.connector.Error as err:
        print("Error: Unable to connect to database:", err)  # Print error
        messagebox.showerror("Connection Error", f"Unable to connect to database: {err}")
        return None

# Add Product
def add_product():
    name = name_entry.get()
    price = price_entry.get()
    qty = qty_entry.get()
    desc = desc_entry.get()

    print(f"Trying to add product: {name}, {price}, {qty}, {desc}")  # Debugging line
    
    if name == "" or price == "" or qty == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        # Connect to the database
        con = connect_db()
        if not con:
            return  # Stop if no database connection is available

        # Create a cursor object
        cur = con.cursor()

        # Disable safe updates temporarily
        cur.execute("SET SQL_SAFE_UPDATES = 0;")

        # Debugging message before executing query
        print("Executing INSERT query...")  # Debugging line
        
        # Query for inserting product
        query = "INSERT INTO products (name, price, quantity, description) VALUES (%s, %s, %s, %s)"
        
        # Print the query with values for debugging
        print(f"Executing query: {query} with values: ({name}, {price}, {qty}, {desc})")
        
        # Execute the insert query with actual values
        cur.execute(query, (name, price, qty, desc))

        # Commit the transaction to save the data to the database
        con.commit()  # Commit the changes
        print(f"{cur.rowcount} row(s) affected.")  # Show number of affected rows

        # If no rows were affected, there might be an issue
        if cur.rowcount == 0:
            print("No rows were inserted into the database.")
        else:
            print("Product added successfully!")

        # Close the connection
        con.close()

        # After successful insertion
        messagebox.showinfo("Success", "Product Added")

        # Clear the input fields
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        qty_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)

        # Refresh the product list
        view_products()

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")  # Debugging line
        messagebox.showerror("Database Error", f"Error occurred: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")  # Debugging line
        messagebox.showerror("Unexpected Error", str(e))

# Update display text with product list
def update_display_text(products):
    display_text.delete(1.0, tk.END)  # Clear the previous content
    display_text.insert(tk.END, "ID\tName\tPrice\tQty\tDescription\n")
    display_text.insert(tk.END, "-"*120 + "\n")
    
    for row in products:
        display_text.insert(tk.END, f"{row[0]}\t{row[1]}\t₹{row[2]}\t{row[3]}\t{row[4]}\n")

# View Products (Directly display them in the main window)
def view_products():
    try:
        con = connect_db()
        if not con:
            return  # Stop if no database connection is available
        
        cur = con.cursor()
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()
        con.close()

        # Update the display with the products
        update_display_text(rows)

    except Exception as e:
        print("Error occurred while viewing products:", e)  # Debugging line
        messagebox.showerror("Error", str(e))

# Delete Product
def delete_product():
    pid = delete_entry.get()
    if pid == "":
        messagebox.showerror("Error", "Enter Product ID")
        return

    try:
        con = connect_db()
        if not con:
            return  # Stop if no database connection is available
        
        cur = con.cursor()
        cur.execute("DELETE FROM products WHERE id = %s", (pid,))
        con.commit()
        con.close()

        if cur.rowcount > 0:
            messagebox.showinfo("Success", "Product Deleted")
        else:
            messagebox.showwarning("Not Found", "Product ID not found")

        delete_entry.delete(0, tk.END)

        # Refresh the product list
        view_products()

    except Exception as e:
        print("Error occurred while deleting product:", e)  # Debugging line
        messagebox.showerror("Error", str(e))

# Search Product
def search_product():
    keyword = search_entry.get()
    if keyword == "":
        messagebox.showerror("Error", "Enter product name to search")
        return

    try:
        con = connect_db()
        if not con:
            return  # Stop if no database connection is available
        
        cur = con.cursor()
        cur.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + keyword + '%',))
        rows = cur.fetchall()
        con.close()

        if rows:
            # Update the display with the search results
            update_display_text(rows)
        else:
            display_text.delete(1.0, tk.END)  # Clear if no products found
            display_text.insert(tk.END, "No matching products found.\n")

    except Exception as e:
        print("Error occurred while searching for products:", e)  # Debugging line
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("🛒 E-commerce Product Catalog - Admin Panel")
root.geometry("1000x700")
root.configure(bg="#F1F8E9")

# Heading
tk.Label(root, text="📦 E-commerce Admin Panel", font=("Arial Rounded MT Bold", 24), fg="#33691E", bg="#F1F8E9").pack(pady=20)

# Main Container Frame
main_frame = tk.Frame(root, bg="#F1F8E9")
main_frame.pack()

# Add Product Section
tk.Label(main_frame, text="Add Product", font=("Segoe UI", 16, "bold"), bg="#F1F8E9").grid(row=0, columnspan=2, pady=10)

tk.Label(main_frame, text="Product Name:", bg="#F1F8E9", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
name_entry = tk.Entry(main_frame, font=("Segoe UI", 12), width=30)
name_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(main_frame, text="Price:", bg="#F1F8E9", font=("Segoe UI", 12)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
price_entry = tk.Entry(main_frame, font=("Segoe UI", 12), width=30)
price_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(main_frame, text="Quantity:", bg="#F1F8E9", font=("Segoe UI", 12)).grid(row=3, column=0, sticky="e", padx=10, pady=5)
qty_entry = tk.Entry(main_frame, font=("Segoe UI", 12), width=30)
qty_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(main_frame, text="Description:", bg="#F1F8E9", font=("Segoe UI", 12)).grid(row=4, column=0, sticky="e", padx=10, pady=5)
desc_entry = tk.Entry(main_frame, font=("Segoe UI", 12), width=30)
desc_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Button(main_frame, text="➕ Add Product", command=add_product, bg="#2E7D32", fg="white", font=("Segoe UI", 12)).grid(row=5, columnspan=2, pady=10)

# View Button
tk.Button(main_frame, text="📄 View Products", command=view_products, bg="#1565C0", fg="white", font=("Segoe UI", 12)).grid(row=6, columnspan=2, pady=5)

# Delete Product
tk.Label(main_frame, text="Delete Product ID:", bg="#F1F8E9", font=("Segoe UI", 12)).grid(row=7, column=0, sticky="e", padx=10, pady=10)
delete_entry = tk.Entry(main_frame, font=("Segoe UI", 12), width=30)
delete_entry.grid(row=7, column=1, padx=10, pady=10)
tk.Button(main_frame, text="🗑️ Delete Product", command=delete_product, bg="#C62828", fg="white", font=("Segoe UI", 12)).grid(row=8, columnspan=2, pady=5)

# Search Section
tk.Label(main_frame, text="🔍 Search Product by Name:", bg="#F1F8E9", font=("Segoe UI", 12)).grid(row=9, column=0, sticky="e", padx=10, pady=5)
search_entry = tk.Entry(main_frame, font=("Segoe UI", 12), width=30)
search_entry.grid(row=9, column=1, padx=10, pady=5)
tk.Button(main_frame, text="🔎 Search", command=search_product, bg="#00796B", fg="white", font=("Segoe UI", 12)).grid(row=10, columnspan=2, pady=10)

# Display area for Products
display_text = tk.Text(main_frame, width=110, height=15, font=("Courier New", 11), bg="white")
display_text.grid(row=11, columnspan=2, padx=20, pady=10)

# Exit Button
tk.Button(main_frame, text="❌ Exit", command=root.destroy, bg="black", fg="white", font=("Segoe UI", 11)).grid(row=12, columnspan=2, pady=20)

root.mainloop()
