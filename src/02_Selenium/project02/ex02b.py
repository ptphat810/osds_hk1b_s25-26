from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os

# Đường dẫn đến file thực thi geckodriver
gecko_path = r"/02_Selenium/project02/geckodriver.exe"

# Khởi tạo đối tượng Service với đường dẫn geckodriver
ser = Service(gecko_path)

# Tạo tùy chọn
options = webdriver.FirefoxOptions()

# Set browser chạy ở chế độ headless (tùy chọn)
options.headless = False

# Khởi tạo driver
driver = webdriver.Firefox(service=ser, options=options)

# URL của trang web cần thu thập dữ liệu
url = 'https://gochek.vn/collections/all'

# Truy cập vào trang
driver.get(url)

# Tạm dừng vài giây để trang tải hoàn tất
time.sleep(3)

# Cuộn trang để tải thêm sản phẩm (tùy chọn)
body = driver.find_element(By.TAG_NAME, "body")
for _ in range(10):  # Cuộn trang xuống 10 lần
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

# Danh sách lưu trữ thông tin sản phẩm
product_names = []
product_prices = []  # Chỉ lưu giá hiện tại
product_images = []

# Lấy tất cả các sản phẩm
products = driver.find_elements(By.CSS_SELECTOR, '.product-block')

# Duyệt qua từng sản phẩm
for product in products:
    # Lấy tên sản phẩm
    try:
        name = product.find_element(By.CSS_SELECTOR, '.pro-name a').text
    except:
        name = ''

    # Lấy giá bán hiện tại
    try:
        price = product.find_element(By.CSS_SELECTOR, '.box-pro-prices .pro-price span').text
    except:
        price = ''

    # Lấy hình ảnh sản phẩm
    try:
        image_url = product.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
    except:
        image_url = ''

    # Thêm thông tin vào các danh sách
    if name:  # Nếu có tên sản phẩm
        product_names.append(name)
        product_prices.append(price)
        product_images.append(image_url)

# Tạo DataFrame từ danh sách đã thu thập
df = pd.DataFrame({
    "Tên sản phẩm": product_names,
    "Giá bán": product_prices,
    "Hình ảnh": product_images
})

# Định nghĩa thư mục lưu file
directory = 'data'

# Kiểm tra nếu thư mục chưa tồn tại, sẽ tạo mới
if not os.path.exists(directory):
    os.makedirs(directory)

# Định nghĩa đường dẫn file
file_name = os.path.join(directory, 'danh_sach_sp_gocheck.xlsx')

# Lưu DataFrame vào file Excel
df.to_excel(file_name, index=False)

# In thông báo xác nhận và đường dẫn đầy đủ
print(f'DataFrame đã được lưu vào file Excel thành công')

# Đóng trình duyệt sau khi hoàn tất
driver.quit()
