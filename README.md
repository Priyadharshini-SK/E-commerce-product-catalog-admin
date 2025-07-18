# E-commerce-product-catalog-admin
# 🛒 E-commerce Product Catalog with Admin Panel

This is a simple and beginner-friendly E-commerce Admin Panel project developed using **Python** and **MySQL**.

It helps manage a product catalog with features like Add, View, and Update. A great project to understand how Python connects with a database and handles real-time data.

## ✅ Features

- ➕ Add New Products  
- 📋 View Product List  
- ✏️ Update Product Price & Stock  
- 💾 MySQL Database Integration  
- 🧠 Simple Console-Based UI

## 💻 Technologies Used

- Python 3  
- MySQL (Workbench or XAMPP)  
- MySQL Connector for Python (`mysql-connector-python`)

## 🧪 How to Run This Project

1. Clone or download this repository  
2. Create a MySQL database named: `ecommerce_db`  
3. Run this SQL to create the product table:

mysql
CREATE TABLE products 
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    price FLOAT,
    stock INT
);