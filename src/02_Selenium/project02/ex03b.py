from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os
import time

# Load email & password từ .env
load_dotenv('config.env')
email = os.getenv('MY_EMAIL')
password = os.getenv('MY_PASSWORD')

# Đường dẫn đến file thực thi geckodriver
gecko_path = r"/02_Selenium/project02/geckodriver.exe"

# Khởi tởi đối tượng dịch vụ với đường geckodriver
ser = Service(gecko_path)

# Tạo tùy chọn
options = webdriver.FirefoxOptions()
options.headless = False
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"

# Khởi tạo driver
driver = webdriver.Firefox(options = options, service=ser)

# Tạo url
url = "https://apps.lms.hutech.edu.vn/authn/login?next"

# Truy cập
driver.get(url)

try:
    # Chờ trường email xuất hiện
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "emailOrUsername"))
    )
    password_input = driver.find_element(By.ID, "password")

    # Điền thông tin đăng nhập
    email_input.send_keys(email)
    time.sleep(3)
    password_input.send_keys(password)

    # Click nút đăng nhập
    login_button = driver.find_element(By.ID, "sign-in")
    login_button.click()

    print("Đăng nhập thành công!")

except TimeoutException:
    print("Không tìm thấy trường đăng nhập hoặc nút đăng nhập")

finally:
    time.sleep(5)
    driver.quit()
