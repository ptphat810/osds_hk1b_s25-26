from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver import ActionChains
import time
import pandas as pd
import os

# Đường dẫn đến file thực thi geckodriver
gecko_path = r"C:/DATA/HUT/CMP1044/OSDS/02_ThuThapDuLieu_Selenium/project02/geckodriver.exe"

# Khởi tởi đối tượng dịch vụ với đường geckodriver
ser = Service(gecko_path)

# Tạo tùy chọn
options = webdriver.firefox.options.Options()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
# Thiết lập firefox chỉ hiện thị giao diện
options.headless = False

# Khởi tạo driver
driver = webdriver.Firefox(options=options, service=ser)

# Tạo url
url = 'https://nhathuoclongchau.com.vn/thuc-pham-chuc-nang/vitamin-khoang-chat'

# Truy cập
driver.get(url)

# Tạm dừng khoảng 1 giây
time.sleep(1)

# Tìm phần tử body của trang để gửi phím mũi tên xuống
body = driver.find_element(By.TAG_NAME, "body")
time.sleep(3)

for k in range(10):
    try:
        # Lấy tất cả các button trên trang
        buttons = driver.find_elements(By.TAG_NAME, "button")

        # Duyệt qua từng button
        for button in buttons:
            # Kiểm tra nếu nội dung của button chứa "Xem thêm" và "sản phẩm"
            if "Xem thêm" in button.text and "sản phẩm" in button.text:
                # Đợi spinner biến mất trước khi click
                WebDriverWait(driver, 20).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "custom-estore-spinner"))
                )
                # Đảm bảo phần tử có thể click
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))

                # Cuộn đến button để đảm bảo nó nằm trong viewport
                driver.execute_script("arguments[0].scrollIntoView(true);", button)

                # Dùng JavaScript để click vào button
                driver.execute_script("arguments[0].click();", button)
                break  # Thoát khỏi vòng lặp nếu đã click thành công

    except Exception as e:
        print(f"Lỗi: {e}")

# Nhấn phím mũi tên xuống nhiều lần để cuộn xuống từ từ
for i in range(50):  # Lặp 50 lần, mỗi lần cuộn xuống một ít
    body.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.01)  # Tạm dừng 0.01 giây giữa mỗi lần cuộn để trang tải nội dung

# Tạm dừng thêm vài giây để trang tải hết nội dung ở cuối trang
time.sleep(1)

# Tạo các list để chứa dữ liệu sản phẩm
stt = []
ten_san_pham = []
gia_ban = []
hinh_anh = []

# Tìm tất cả các button có nội dung là "Chọn mua"
buttons = driver.find_elements(By.XPATH, "//button[text()='Chọn mua']")

print(len(buttons))

# Lấy từng sản phẩm
for i, bt in enumerate(buttons, 1):
    # Quay ngược 3 lần để tìm div cha
    parent_div = bt
    for _ in range(3):
        parent_div = parent_div.find_element(By.XPATH, "./..")  # Quay ngược 1 lần

    sp = parent_div

    # Lấy tên sản phẩm
    try:
        tsp = sp.find_element(By.TAG_NAME, 'h3').text
    except:
        tsp = ''

    # Lấy giá sản phẩm
    try:
        gsp = sp.find_element(By.CLASS_NAME, 'text-blue-5').text
    except:
        gsp = ''

    # Lấy hình ảnh
    try:
        ha = sp.find_element(By.TAG_NAME, 'img').get_attribute('src')
    except:
        ha = ''

    # Chỉ thêm vào danh sách nếu có tên sản phẩm
    if len(tsp) > 0:
        stt.append(i)
        ten_san_pham.append(tsp)
        gia_ban.append(gsp)
        hinh_anh.append(ha)

# Tạo DataFrame để lưu kết quả
df = pd.DataFrame({
    "STT": stt,
    "Tên sản phẩm": ten_san_pham,
    "Giá bán": gia_ban,
    "Hình ảnh": hinh_anh
})


# Định nghĩa thư mục lưu file
directory = 'data'

# Kiểm tra nếu thư mục chưa tồn tại, sẽ tạo mới
if not os.path.exists(directory):
    os.makedirs(directory)

# Định nghĩa đường dẫn file
file_name = os.path.join(directory, 'danh_sach_sp_3.xlsx')

# Lưu DataFrame vào file Excel
df.to_excel(file_name, index=False)

# In thông báo xác nhận và đường dẫn đầy đủ
print(f'DataFrame đã được lưu vào file Excel thành công')

# Đóng trình duyệt sau khi hoàn tất
driver.quit()
