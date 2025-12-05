"""
Đề Bài Thực Hành: Cào Dữ Liệu Long Châu và Quản Lý SQLite
I. Mục Tiêu
    Thực hiện cào dữ liệu sản phẩm từ trang web chính thức của chuỗi nhà thuốc Long Châu bằng công cụ Selenium, lưu trữ dữ liệu thu thập được một cách tức thời vào cơ sở dữ liệu SQLite, và kiểm tra chất lượng dữ liệu.

II. Yêu Cầu Kỹ Thuật (Scraping & Lưu trữ)
    Công cụ: Sử dụng thư viện Selenium kết hợp với Python và Pandas (cho việc quản lý DataFrame tạm thời và lưu vào DB).

    Phạm vi Cào: Chọn một danh mục sản phẩm cụ thể trên trang Long Châu (ví dụ: "Thực phẩm chức năng", "Chăm sóc da", hoặc "Thuốc") và cào ít nhất 50 sản phẩm (có thể cào nhiều trang/URL khác nhau).

    Dữ liệu cần cào: Đối với mỗi sản phẩm, cần thu thập ít nhất các thông tin sau (table phải có các cột bên dưới):

        Mã sản phẩm (id): cố gắng phân tích và lấy mã sản phẩm gốc từ trang web, nếu không được thì dùng mã tự tăng.

        Tên sản phẩm (product_name)

        Giá bán (price)

        Giá gốc/Giá niêm yết (nếu có, original_price)

        Đơn vị tính (ví dụ: Hộp, Chai, Vỉ, unit)

        Link URL sản phẩm (product_url) (Dùng làm định danh duy nhất)

    Lưu trữ Tức thời:

        Sử dụng thư viện sqlite3 để tạo cơ sở dữ liệu (longchau_db.sqlite).

        Thực hiện lưu trữ dữ liệu ngay lập tức sau khi cào xong thông tin của mỗi sản phẩm (sử dụng conn.cursor().execute() hoặc DataFrame.to_sql(if_exists='append')) thay vì lưu trữ toàn bộ sau khi kết thúc quá trình cào.

        Sử dụng product_url hoặc một trường định danh khác làm PRIMARY KEY (hoặc kết hợp với lệnh INSERT OR IGNORE) để tránh ghi đè nếu chạy lại code.

III. Yêu Cầu Phân Tích Dữ Liệu (Query/Truy Vấn)
    Sau khi dữ liệu được thu thập, tạo và thực thi ít nhất 15 câu lệnh SQL (queries) để khảo sát chất lượng và nội dung dữ liệu.

    Nhóm 1: Kiểm Tra Chất Lượng Dữ Liệu (Bắt buộc)
        Kiểm tra trùng lặp (Duplicate Check): Kiểm tra và hiển thị tất cả các bản ghi có sự trùng lặp dựa trên trường product_url hoặc product_name.

        Kiểm tra dữ liệu thiếu (Missing Data): Đếm số lượng sản phẩm không có thông tin Giá bán (price là NULL hoặc 0).

        Kiểm tra giá: Tìm và hiển thị các sản phẩm có Giá bán lớn hơn Giá gốc/Giá niêm yết (logic bất thường).

        Kiểm tra định dạng: Liệt kê các unit (đơn vị tính) duy nhất để kiểm tra sự nhất quán trong dữ liệu.

        Tổng số lượng bản ghi: Đếm tổng số sản phẩm đã được cào.

    Nhóm 2: Khảo sát và Phân Tích (Bổ sung)
        Sản phẩm có giảm giá: Hiển thị 10 sản phẩm có mức giá giảm (chênh lệch giữa original_price và price) lớn nhất.

        Sản phẩm đắt nhất: Tìm và hiển thị sản phẩm có giá bán cao nhất.

        Thống kê theo đơn vị: Đếm số lượng sản phẩm theo từng Đơn vị tính (unit).

        Sản phẩm cụ thể: Tìm kiếm và hiển thị tất cả thông tin của các sản phẩm có tên chứa từ khóa "Vitamin C".

        Lọc theo giá: Liệt kê các sản phẩm có giá bán nằm trong khoảng từ 100.000 VNĐ đến 200.000 VNĐ.

    Nhóm 3: Các Truy vấn Nâng cao (Tùy chọn)
        Sắp xếp: Sắp xếp tất cả sản phẩm theo Giá bán từ thấp đến cao.

        Phần trăm giảm giá: Tính phần trăm giảm giá cho mỗi sản phẩm và hiển thị 5 sản phẩm có phần trăm giảm giá cao nhất (Yêu cầu tính toán trong query hoặc sau khi lấy data).

        Xóa bản ghi trùng lặp: Viết câu lệnh SQL để xóa các bản ghi bị trùng lặp, chỉ giữ lại một bản ghi (sử dụng Subquery hoặc Common Table Expression - CTE).

        Phân tích nhóm giá: Đếm số lượng sản phẩm trong từng nhóm giá (ví dụ: dưới 50k, 50k-100k, trên 100k).

        URL không hợp lệ: Liệt kê các bản ghi mà trường product_url bị NULL hoặc rỗng.
"""
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3
import os

# =======================
# Cấu hình Selenium
# =======================
gecko_path = r"C:/DATA/HUT/CMP1044/OSDS/02_ThuThapDuLieu_Selenium/project02/geckodriver.exe"
ser = Service(gecko_path)

options = webdriver.firefox.options.Options()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
options.headless = False

driver = webdriver.Firefox(options=options, service=ser)

url = 'https://nhathuoclongchau.com.vn/thuc-pham-chuc-nang/cai-thien-tang-cuong-chuc-nang'
driver.get(url)
time.sleep(1)

body = driver.find_element(By.TAG_NAME, "body")
time.sleep(3)

# =======================
# Khởi tạo SQLite
# =======================
directory = 'data'
if not os.path.exists(directory):
    os.makedirs(directory)
DB_FILE = os.path.join(directory, 'Longchau_db.sqlite')

# Xóa DB cũ nếu muốn
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"Đã xóa file DB cũ: {DB_FILE}")

# Kết nối SQLite
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    price TEXT,
    unit TEXT,
    product_url TEXT UNIQUE
)
''')
conn.commit()

# =======================
# Lấy thông tin & lưu SQLite
# =======================
for k in range(10):
    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if "Xem thêm" in button.text and "sản phẩm" in button.text:
                WebDriverWait(driver, 20).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "custom-estore-spinner"))
                )
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                driver.execute_script("arguments[0].click();", button)
                break
    except Exception as e:
        print(f"Lỗi: {e}")

for i in range(50):
    body.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.01)
time.sleep(1)

buttons = driver.find_elements(By.XPATH, "//button[text()='Chọn mua']")
print(f"Tìm thấy {len(buttons)} sản phẩm")

for bt in buttons:
    parent_div = bt
    for _ in range(3):
        parent_div = parent_div.find_element(By.XPATH, "./..")
    sp = parent_div

    # Tên sản phẩm
    try:
        product_name = sp.find_element(By.TAG_NAME, 'h3').text
    except:
        product_name = ''

    # Giá bán và đơn vị
    try:
        price_text = sp.find_element(By.CLASS_NAME, 'text-blue-5').text
        # Bỏ ký tự 'đ' và các dấu chấm
        price_text = price_text.replace('đ', '').replace('.', '').strip()
        if '/' in price_text:
            price, unit = map(str.strip, price_text.split('/'))
        else:
            price = price_text
            unit = ''
    except:
        price = ''
        unit = ''

    # URL sản phẩm
    try:
        product_url = sp.find_element(By.TAG_NAME, 'a').get_attribute('href')
    except:
        product_url = ''

    # Lưu vào SQLite nếu có tên và URL
    if product_name and product_url:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO products
                (product_name, price, unit, product_url)
                VALUES (?, ?, ?, ?)
            ''', (product_name, price, unit, product_url))
            conn.commit()
        except Exception as e:
            print(f"Lỗi khi lưu sản phẩm: {e}")


print("Hoàn tất cào dữ liệu và lưu vào SQLite.")
conn.close()
driver.quit()

######################################################
## III. Yêu Cầu Phân Tích Dữ Liệu
######################################################
## Nhóm 1
conn = sqlite3.connect("data/Longchau_db.sqlite")
cursor = conn.cursor()

print("\n=================== 1. Hiển thị tất cả các bản ghi có sự trùng lặp dựa trên trường product_url hoặc product_name ===================")
sql1 = """
SELECT product_name
FROM products
GROUP BY product_name
HAVING COUNT(product_name) > 1;
"""
cursor.execute(sql1)
for row in cursor.fetchall():
    print(row[0])

print("\n=================== 2. Đếm số lượng sản phẩm không có thông tin Giá bán ===================")
sql2 = """
SELECT COUNT(product_name)
FROM products
WHERE price IS NULL OR price =="";
"""
cursor.execute(sql2)
print(f"số lượng sản phẩm không có thông tin giá bán: {cursor.fetchall()[0][0]}")


print("\n=================== 3. Liệt kê các unit (đơn vị tính) duy nhất để kiểm tra sự nhất quán trong dữ liệu ===================")
sql3 = """
SELECT DISTINCT unit
FROM products;
"""
cursor.execute(sql3)
for row in cursor.fetchall():
    print(row[0])


print("\n=================== 4. Tổng số lượng bản ghi: Đếm tổng số sản phẩm đã được cào ===================")
sql4 = """
SELECT COUNT(*)
FROM products;
"""
cursor.execute(sql4)
print(cursor.fetchall()[0][0])


## Nhóm 2
print("\n=================== 5. Tìm và hiển thị sản phẩm có giá bán cao nhất ===================")
sql5 = """
SELECT product_name
FROM products
ORDER BY price DESC;
"""
cursor.execute(sql5)
print(cursor.fetchall()[0][0])



print("\n=================== 6. Đếm số lượng sản phẩm theo từng Đơn vị tính ===================")
sql6 = """
SELECT unit, COUNT(*)
FROM products
GROUP BY unit;
"""
cursor.execute(sql6)
for row in cursor.fetchall():
    print(row)



print("\n=================== 7. Tìm kiếm và hiển thị tất cả thông tin của các sản phẩm có tên chứa từ khóa Vitamin C ===================")
sql7 = """
SELECT *
FROM products
WHERE product_name LIKE '%Vitamin%';
"""
cursor.execute(sql7)
for row in cursor.fetchall():
    print(row)

print("\n=================== 8. Liệt kê các sản phẩm có giá bán nằm trong khoảng từ 100.000 VNĐ đến 200.000 VNĐ ===================")
sql8 = """
SELECT *
FROM products
WHERE price BETWEEN 100000 AND 200000;
"""
cursor.execute(sql8)
for row in cursor.fetchall():
    print(row)

print("\n=================== 9. Sắp xếp tất cả sản phẩm theo Giá bán từ thấp đến cao ===================")
sql9 = """
SELECT product_name, price
FROM products
ORDER BY price ASC;
"""
cursor.execute(sql9)
for row in cursor.fetchall():
    print(row)



print("\n=================== 10. Liệt kê các bản ghi mà trường product_url bị NULL hoặc rỗng ===================")
sql10 = """
SELECT COUNT(product_name)
FROM products
WHERE product_url IS NULL OR product_url = '';
"""
cursor.execute(sql10)
for row in cursor.fetchall():
    print(row)

print("\n=================== 11. Đếm số lượng sản phẩm trong từng nhóm giá (ví dụ: dưới 50k, 50k-100k, trên 100k ===================")
sql11 = """
SELECT
CASE
    WHEN price < 50000 THEN 'dưới 50k'
    WHEN price BETWEEN 50000 AND 500000 THEN '50k-500k'
    ELSE 'trên 500'
END AS price_group,
COUNT(*) as count
FROM products
GROUP BY price_group;
"""
cursor.execute(sql11)
for row in cursor.fetchall():
    print(row)

conn.close()