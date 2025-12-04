"""
Lay tat ca cac ten painter bang dau bang moi chu cai (A-Z)
"""

from builtins import range
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Khởi tạo Webdriver
driver = webdriver.Chrome()

for i in range(65, 91):
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

        # In ra kết quả
        print(f"Các tên painter bắt đầu bằng chữ {chr(i)}")
        for title, link in zip(titles, links):
            print(title, link)
    except:
        print("Error!")

driver.quit()

# ===========================================================================
#
#         # Lấy ra tất cả các ul
#         ul_tags = driver.find_elements(By.TAG_NAME, "ul")
#         print(len(ul_tags))
#
#         # Chọn ul thứ 21
#         ul_painters = ul_tags[20]   # list start with index=0
#
#         # Lấy ra tất cả các thẻ <li> thuộc ul_painters
#         li_tags = ul_painters.find_elements(By.TAG_NAME, "li")
#
#         # Tạo danh sách các url
#         titles = [tag.find_element(By.TAG_NAME, "a").get_attribute("title") for tag in li_tags]
#
#         # In ra title
#         for title in titles:
#             print(title)
#
#     except:
#         print("Error!")
# # Đóng webdriver
# driver.quit()
