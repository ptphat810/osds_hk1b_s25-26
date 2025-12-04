from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
import os

# I. Tạo dataframe rỗng
all_links = []
d = pd.DataFrame({
    'Tên trường': [],
    'Thành lập': [],
    'Hiệu trưởng': [],
    'Khẩu hiệu': [],
    'Địa chỉ': [],
    'Website': [],
    'Viết tắt': []
})

# II. Lấy các đường dẫn truy cập đến từng trường đại học
driver = webdriver.Chrome()
url = "https://vi.wikipedia.org/wiki/Danh_s%C3%A1ch_tr%C6%B0%E1%BB%9Dng_%C4%91%E1%BA%A1i_h%E1%BB%8Dc,_h%E1%BB%8Dc_vi%E1%BB%87n_v%C3%A0_cao_%C4%91%E1%BA%B3ng_t%E1%BA%A1i_Vi%E1%BB%87t_Nam"
driver.get(url)
time.sleep(3)

content_div = driver.find_element(By.ID, "mw-content-text")
a_tags = content_div.find_elements(By.TAG_NAME, "a")

links = []
names = []

for a in a_tags:
    try:
        name = a.text.strip()
        href = a.get_attribute("href")

        if not href or not name:
            continue

        # Lọc đúng trường Đại học / Học viện
        if ("Trường Đại học" in name or "Học viện" in name) and ("Cao đẳng" not in name):

            # Bỏ trùng link
            if href in links:
                continue

            links.append(href)
            names.append(name)

    except:
        continue

driver.quit()

# III. Lấy thông tin từ từng trang trường
count = 0
limit_number = 88
for i, link in enumerate(links):
    if count >= limit_number:
        break
    count += 1

    print(f"Trường thứ{i}: {link}")

    try:
        driver = webdriver.Chrome()
        driver.get(link)
        time.sleep(2)

        # Tên trường
        try:
            ten_truong = driver.find_element(By.TAG_NAME, "h1").text
        except:
            ten_truong = ""

        # Thành lập
        try:
            thanh_lap = driver.find_element(By.XPATH, "//th[contains(text(),'Thành lập')]/following-sibling::td").text
        except:
            thanh_lap = ""

        # Hiệu trưởng
        try:
            hieu_truong = driver.find_element(By.XPATH, "//th[contains(text(),'Hiệu trưởng')]/following-sibling::td").text
        except:
            hieu_truong = ""

        # Khẩu hiệu
        try:
            khau_hieu = driver.find_element(By.XPATH, "//th[contains(text(),'Khẩu hiệu')]/following-sibling::td").text
        except:
            khau_hieu = ""

        # Địa chỉ
        try:
            dia_chi = driver.find_element(By.XPATH, "//th[contains(text(),'Địa chỉ')]/following-sibling::td").text
        except:
            dia_chi = ""

        # Website
        try:
            website = driver.find_element(By.XPATH, "//th[contains(text(),'Website')]/following-sibling::td").text
        except:
            website = ""

        # Viết tắt
        try:
            viet_tat = driver.find_element(By.XPATH, "//th[contains(text(),'Tên viết tắt')]/following-sibling::td").text
        except:
            viet_tat = ""

        # Tạo dict thông tin
        uni = {
            'Tên trường': ten_truong,
            'Thành lập': thanh_lap,
            'Hiệu trưởng': hieu_truong,
            'Khẩu hiệu': khau_hieu,
            'Địa chỉ': dia_chi,
            'Website': website,
            'Viết tắt': viet_tat
        }

        # Chuyển sang dataframe
        df_uni = pd.DataFrame([uni])

        # Thêm vào dataframe lớn
        d = pd.concat([d, df_uni], ignore_index=True)

        driver.quit()
    except:
        pass

# IV. In kết quả
print(d)

# Định nghĩa thư mục lưu file
directory = 'data'

# Kiểm tra nếu thư mục chưa tồn tại, sẽ tạo mới
if not os.path.exists(directory):
    os.makedirs(directory)

# Định nghĩa đường dẫn file
file_name = os.path.join(directory, 'Universities.xlsx')

# Lưu DataFrame vào file Excel
d.to_excel(file_name, index=False)

# In thông báo xác nhận và đường dẫn đầy đủ
print(f'DataFrame đã được lưu vào file Excel thành công')