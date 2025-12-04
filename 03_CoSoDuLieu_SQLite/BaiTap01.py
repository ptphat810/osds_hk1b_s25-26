import sqlite3

# 1. Kết nối tới cơ sở dữ liệu
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# 2. Tạo bảng nếu chưa tồn tại
sql1 = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price NUMERIC NOT NULL,
    quantity INTEGER
)
"""
cursor.execute(sql1)
conn.commit()

# 3. CRUD

# 3.1 INSERT (Thêm dữ liệu)
products_data = [
    ("Laptop A100", 999.99, 15),
    ("Mouse Wireless X", 25.50, 50),
    ("Monitor 27-inch", 249.00, 10),
    ("Laptop Asus 16-inch", 500.00, 12)
]

sql2 = """INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)"""
cursor.executemany(sql2, products_data)
conn.commit()

# 3.2 SELECT (Đọc dữ liệu)
sql3 = "SELECT * FROM products"
cursor.execute(sql3)
all_products = cursor.fetchall()

print("\nDANH SÁCH SẢN PHẨM:")
print(f"{'ID':<4} | {'Tên Sản Phẩm':<20} | {'Giá':<10} | {'Số Lượng':<10}")
for p in all_products:
    print(f"{p[0]:<4} | {p[1]:<20} | {p[2]:<10} | {p[3]:<10}")

# 3.3 UPDATE (Cập nhật dữ liệu)
sql_update = """
UPDATE products 
SET price = ?, quantity = ?
WHERE id = ?
"""
cursor.execute(sql_update, (1099.99, 20, 1))   # cập nhật sản phẩm ID = 1
conn.commit()

# 3.4 DELETE (Xóa dữ liệu)
sql_delete = "DELETE FROM products WHERE id = ?"
cursor.execute(sql_delete, (2,))   # xóa sản phẩm ID = 2
conn.commit()

# Kiểm tra lại danh sách sản phẩm
print("\nDANH SÁCH SAU UPDATE + DELETE:")
cursor.execute("SELECT * FROM products")
products_after = cursor.fetchall()

print(f"{'ID':<4} | {'Tên Sản Phẩm':<20} | {'Giá':<10} | {'Số Lượng':<10}")
for p in products_after:
    print(f"{p[0]:<4} | {p[1]:<20} | {p[2]:<10} | {p[3]:<10}")

# Đóng kết nối
conn.close()
