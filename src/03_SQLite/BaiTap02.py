import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import os
from bs4 import BeautifulSoup

######################################################
## I. Cấu hình và Chuẩn bị
######################################################
directory = 'data'
if not os.path.exists(directory):
    os.makedirs(directory)
DB_FILE = os.path.join(directory, 'Painters.db')
TABLE_NAME = 'painters_info'

# Xóa DB cũ nếu muốn
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"Đã xóa file DB cũ: {DB_FILE}")

# Kết nối SQLite
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Tạo bảng
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    name TEXT PRIMARY KEY,
    birth TEXT,
    death TEXT,
    nationality TEXT
);
"""
cursor.execute(create_table_sql)
conn.commit()
print(f"Đã chuẩn bị bảng '{TABLE_NAME}' trong '{DB_FILE}'.")

# Hàm đóng driver an toàn
def safe_quit_driver(driver):
    try:
        if driver:
            driver.quit()
    except:
        pass

######################################################
## II. Lấy danh sách link
######################################################

print("\n--- Bắt đầu Lấy Đường dẫn ---")
links = []

# Lấy họa sĩ bắt đầu bằng chữ F (chỉ thử một chữ cái làm ví dụ)
for i in range(69, 71):
    driver = webdriver.Chrome()
    url = f"https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22{chr(i)}%22"
    driver.get(url)
    try:
        time.sleep(3)
        content_div = driver.find_element(By.ID, "mw-content-text")
        ul_tags = content_div.find_elements(By.TAG_NAME, "ul")

        for ul in ul_tags:
            li_tags = ul.find_elements(By.TAG_NAME, "li")
            for li in li_tags:
                try:
                    a_tag = li.find_element(By.TAG_NAME, "a")
                    href = a_tag.get_attribute("href")
                    if "List_of_painters_by_name_beginning_with" in href:
                        continue
                    links.append(href)
                except:
                    continue
    except Exception as e:
        print(f"Lỗi lấy link: {e}")
    finally:
        safe_quit_driver(driver)

print(f"Tổng cộng {len(links)} link đã tìm thấy.")

######################################################
## III. Lấy thông tin & lưu SQLite
######################################################

print("\n--- Bắt đầu cào và lưu dữ liệu ---")

count = 0

for link in links:
    if count >= len(links):
        break
    count += 1
    print(f"\n[{count}] {link}")

    try:
        driver = webdriver.Chrome()
        driver.get(link)
        time.sleep(2)

        # 1. Tên họa sĩ
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""

        # 2. Ngày sinh
        try:
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            birth_text = birth_element.text
            match = re.search(r'\b\d{1,2}\s+[A-Za-z]+\s+\d{4}\b', birth_text)
            birth = match.group(0) if match else ""
        except:
            birth = ""

        # 3. Ngày mất
        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            death_text = death_element.text
            match = re.search(r'\b\d{1,2}\s+[A-Za-z]+\s+\d{4}\b', death_text)
            death = match.group(0) if match else ""
        except:
            death = ""

        # 4. Lấy nationality bằng BeautifulSoup
        try:
            infobox_html = driver.find_element(By.CLASS_NAME, "infobox").get_attribute("innerHTML")
            soup = BeautifulSoup(infobox_html, "html.parser")

            # Tìm th có Nationality hoặc Citizenship
            nationality = ""
            nat_th = soup.find('th', string=re.compile("Nationality|Citizenship"))
            if nat_th:
                td = nat_th.find_next_sibling('td')
                if td:
                    parts = [tag.get_text(strip=True) for tag in td.find_all()]
                    nationality = ", ".join(parts) if parts else td.get_text(", ", strip=True)
            else:
                # fallback lấy từ birthplace
                birthplace_div = soup.find('div', class_='birthplace')
                if birthplace_div:
                    parts = [a.get_text(strip=True) for a in birthplace_div.find_all('a')]
                    nationality = parts[-1] if parts else ""
        except:
            nationality = ""

        safe_quit_driver(driver)

        # 5. Lưu vào SQLite
        insert_sql = f"""
        INSERT OR IGNORE INTO {TABLE_NAME} (name, birth, death, nationality)
        VALUES (?, ?, ?, ?);
        """
        cursor.execute(insert_sql, (name, birth, death, nationality))
        conn.commit()
        print(f"--> Đã lưu: {name} | {birth} | {death} | {nationality}")

    except Exception as e:
        print(f"Lỗi khi xử lý {link}: {e}")
        safe_quit_driver(driver)

# Đóng kết nối
conn.close()
print("\nĐã đóng kết nối cơ sở dữ liệu.")

######################################################
## IV. Truy vấn SQL Mẫu và Đóng kết nối
######################################################

"""
A. Yêu Cầu Thống Kê và Toàn Cục
1. Đếm tổng số họa sĩ đã được lưu trữ trong bảng.
2. Hiển thị 5 dòng dữ liệu đầu tiên để kiểm tra cấu trúc và nội dung bảng.
3. Liệt kê danh sách các quốc tịch duy nhất có trong tập dữ liệu.

B. Yêu Cầu Lọc và Tìm Kiếm
4. Tìm và hiển thị tên của các họa sĩ có tên bắt đầu bằng ký tự 'F'.
5. Tìm và hiển thị tên và quốc tịch của những họa sĩ có quốc tịch chứa từ khóa 'French' (ví dụ: French, French-American).
6. Hiển thị tên của các họa sĩ không có thông tin quốc tịch (hoặc để trống, hoặc NULL).
7. Tìm và hiển thị tên của những họa sĩ có cả thông tin ngày sinh và ngày mất (không rỗng).
8. Hiển thị tất cả thông tin của họa sĩ có tên chứa từ khóa '%Fales%' (ví dụ: George Fales Baker).

C. Yêu Cầu Nhóm và Sắp Xếp
9. Sắp xếp và hiển thị tên của tất cả họa sĩ theo thứ tự bảng chữ cái (A-Z).
10. Nhóm và đếm số lượng họa sĩ theo từng quốc tịch.
"""
# Kết nối SQLite
conn = sqlite3.connect("data/Painters.db")
cursor = conn.cursor()

# Code
print("\n=================== 1. Đếm tổng số họa sĩ ===================")
sql1 = """
SELECT COUNT(*) FROM painters_info
"""
cursor.execute(sql1)
r = cursor.fetchall()
print(r[0][0])

print("\n=================== 2. 5 dòng đầu tiên ===================")
sql2 = """
SELECT * FROM painters_info LIMIT 5;
"""
cursor.execute(sql2)
rows = cursor.fetchall()
for r in rows:
    print(r)

print("\n=================== 3. Danh sách quốc tịch duy nhất ===================")
sql3 = """
SELECT DISTINCT nationality FROM painters_info;
"""
cursor.execute(sql3)
for r in cursor.fetchall():
    print(r[0])

print("\n=================== 4. Họa sĩ tên bắt đầu bằng 'F' ===================")
sql4 = """
SELECT name FROM painters_info 
WHERE name LIKE 'F%';
"""
cursor.execute(sql4)
for r in cursor.fetchall():
    print(r[0])

print("\n=================== 5. Họa sĩ có quốc tịch chứa 'French' ===================")
sql5 = """
SELECT name, nationality FROM painters_info 
WHERE nationality LIKE '%French%';
"""
cursor.execute(sql5)
for r in cursor.fetchall():
    print(r)

print("\n=================== 6. Họa sĩ không có thông tin quốc tịch ===================")
sql6 = """
SELECT name FROM painters_info 
WHERE nationality IS NULL OR nationality = '';
"""
cursor.execute(sql6)
for r in cursor.fetchall():
    print(r[0])

print("\n=================== 7. Họa sĩ có đầy đủ ngày sinh và ngày mất ===================")
sql7 = """
SELECT name FROM painters_info 
WHERE birth <> '' AND death <> '';
"""
cursor.execute(sql7)
for r in cursor.fetchall():
    print(r[0])

print("\n=================== 8. Họa sĩ có tên chứa 'Fales' ===================")
sql8 = """
SELECT * FROM painters_info 
WHERE name LIKE '%Fales%';
"""
cursor.execute(sql8)
for r in cursor.fetchall():
    print(r)

print("\n=================== 9. Sắp xếp tên họa sĩ A → Z ===================")
sql9 = """
SELECT name FROM painters_info 
ORDER BY name ASC;
"""
cursor.execute(sql9)
for r in cursor.fetchall():
    print(r[0])

print("\n=================== 10. Nhóm và đếm số họa sĩ theo quốc tịch ===================")
sql10 = """
SELECT nationality, COUNT(*) FROM painters_info 
GROUP BY nationality 
ORDER BY COUNT(*) DESC;
"""
cursor.execute(sql10)
for r in cursor.fetchall():
    print(r)

# print("\nSố lượng họa sĩ có đầy đủ thông tin")
# sql="""
# SELECT COUNT(*)
# FROM painters_info
# WHERE name IS NOT NULL
#   AND birth IS NOT NULL AND birth <> ''
#   AND death IS NOT NULL AND death <> ''
#   AND nationality IS NOT NULL AND nationality <> '';
# """
# cursor.execute(sql)
# for r in cursor.fetchall():
#     print(r)

# Đóng kết nối
conn.close()

