"""
Lấy các đường dẫn truy cập đến painter bat dau bang chu 'P'
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Khởi tạo Webdriver
driver = webdriver.Chrome()

# Mở trang
url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22P%22"
driver.get(url)

# Đợi khoảng chừng 2 giây
time.sleep(2)

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

# In ra kết quả
for title, link in zip(titles, links):
    print(title, link)

# Đóng webdriver
driver.quit()

# ===========================================================================
# # Lấy ra tất cả các thẻ ul
# ul_tags = driver.find_elements(By.TAG_NAME, "ul")
# print(len(ul_tags))
#
# # Chọn thẻ ul thứ 21
# ul_painters = ul_tags[20] # list start with index=0
#
# # Lấy ra tất cả các thẻ <li> thuộc ul_painters
# li_tags = ul_painters.find_elements(By.TAG_NAME, "li")
#
# # Tạo danh sách các url
# links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
# titles = [tag.find_element(By.TAG_NAME, "a").get_attribute("title") for tag in li_tags]
#
# # In ra url
# for link in links:
#     print(link)
#
# # In ra title
# for title in titles:
#     print(title)
#
# # Đóng webdriver
# driver.quit()
