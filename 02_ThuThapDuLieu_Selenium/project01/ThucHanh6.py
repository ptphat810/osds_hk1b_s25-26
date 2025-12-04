from pygments.formatters.html import webify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
import os

# I. Tạo dataframe rỗng
all_links = []
d = pd.DataFrame({'name': [], 'birth': [], 'death': [] , 'nationality': []})

# II. Lấy các đường dẫn truy cập đến painter
for i in range(70,71):
    driver = webdriver.Chrome()
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22"+chr(i)+"%22"
    driver.get(url)
    try:
        time.sleep(3)

        # Lấy div chứa nội dung chính
        content_div = driver.find_element(By.ID, "mw-content-text")

        # Lấy tất cả thẻ <ul> trong content_div
        ul_tags = content_div.find_elements(By.TAG_NAME, "ul")

        links = []
        titles = []

        for ul in ul_tags:
            li_tags = ul.find_elements(By.TAG_NAME, "li")
            for li in li_tags:
                try:
                    a_tag = li.find_element(By.TAG_NAME, "a")
                    href = a_tag.get_attribute("href")
                    title = a_tag.get_attribute("title")

                    # Loại bỏ các link tới danh sách chữ cái khác
                    if "List_of_painters_by_name_beginning_with" in href:
                        continue

                    links.append(href)
                    titles.append(title)
                except:
                    continue
    except:
        print("Error")
driver.quit()

# III. Lấy thông tin của từng họa sĩ
count = 0
for link in links:
    if (count > 10):
        break
    count = count + 1

    print(link)
    try:

        driver = webdriver.Chrome()
        url = link
        driver.get(url)
        time.sleep(2)
        # Lấy tên họa sĩ
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""

        # Lấy ngày sinh
        try:
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            birth = birth_element.text
            birth = re.findall(r'[0-9]{1,2}+\s+[A-Za-z]+\s+[0-9]{4}', birth)[0]  # regex
        except:
            birth = ""

        # Lấy ngày mất
        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            death = death_element.text
            death = re.findall(r'[0-9]{1,2}+\s+[A-Za-z]+\s+[0-9]{4}', death)[0]
        except:
            death = ""

        # Lấy quốc tịch
        try:
            nationality_element = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td")
            nationality = nationality_element.text
        except:
            nationality = ""

        # Tạo dict thông tin của họa sĩ
        painter = {'name': name, 'birth': birth, 'death': death, 'nationality': nationality}

        # Chuyển đổi dict thanh dataframe
        painter_df = pd.DataFrame([painter])

        # Thêm thông tin vào df
        d = pd.concat([d, painter_df], ignore_index=True)

        # Dong webdriver
        driver.quit()
    except:
        pass

# IV. In thong tin
print(d)

# Định nghĩa thư mục lưu file
directory = 'data'

# Kiểm tra nếu thư mục chưa tồn tại, sẽ tạo mới
if not os.path.exists(directory):
    os.makedirs(directory)

# Định nghĩa đường dẫn file
file_name = os.path.join(directory, 'Painters.xlsx')

# Lưu DataFrame vào file Excel
d.to_excel(file_name)

# In thông báo xác nhận và đường dẫn đầy đủ
print(f'DataFrame đã được lưu vào file Excel thành công')