from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from getpass import getpass
import os

# --- Load config ---
load_dotenv('config.env')
username = os.getenv("USERNAME")
password = getpass("Nhập mật khẩu: ")

# --- Cấu hình Chrome ---
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service('C:/PATH_TO/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://fileforums.com/")

    # --- Chờ username input xuất hiện ---
    wait = WebDriverWait(driver, 30)  # tối đa 15 giây
    username_input = wait.until(EC.presence_of_element_located((By.ID, "navbar_username")))
    password_input = driver.find_element(By.ID, "navbar_password")
    login_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Log in']")

    # --- Điền thông tin ---
    username_input.clear()
    username_input.send_keys(username)
    password_input.clear()
    password_input.send_keys(password)

    # --- Click Log in ---
    login_button.click()

    # --- Chờ đăng nhập xong (ví dụ chờ profile xuất hiện) ---
    wait.until(EC.presence_of_element_located((By.ID, "navbar_userinfo")))  # Thay ID nếu khác
    print("Đăng nhập thành công!")

finally:
    driver.quit()
