from pymongo import MongoClient
from datetime import datetime

# 1. Kết nối đến MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['driveManagement']

# 2. Tạo collection
files_collection = db['files']

# Xóa dữ liệu cũ để tránh trùng khi chạy nhiều lần
files_collection.delete_many({})

# 3. Thêm dữ liệu
files_data = [
    { "file_id": 1, "name": "Report.pdf",        "size": 2048, "owner": "Nguyen Van A",  "created_at": datetime(2024, 1, 10), "shared": False },
    { "file_id": 2, "name": "Presentation.pptx", "size": 5120, "owner": "Tran Thi B",    "created_at": datetime(2024, 1, 15), "shared": True },
    { "file_id": 3, "name": "Image.png",         "size": 1024, "owner": "Le Van C",      "created_at": datetime(2024, 1, 20), "shared": False },
    { "file_id": 4, "name": "Spreadsheet.xlsx",  "size": 3072, "owner": "Pham Van D",    "created_at": datetime(2024, 1, 25), "shared": True },
    { "file_id": 5, "name": "Notes.txt",         "size": 512,  "owner": "Nguyen Thi E",  "created_at": datetime(2024, 1, 30), "shared": False }
]
files_collection.insert_many(files_data)

# 4. Truy vấn dữ liệu
# 4.1 Xem tất cả tệp
print("\nTất cả tệp:")
for file in files_collection.find():
    print(file)

# 4.2 Tệp có kích thước > 2000 KB
print("\nTệp có kích thước > 2000 KB:")
for file in files_collection.find({ "size": { "$gt": 2000 } }):
    print(file)

# 4.3 Đếm tổng số tệp
print("\nTổng số tệp:")
print(files_collection.count_documents({}))

# 4.4 Tất cả tệp được chia sẻ
print("\nTất cả tệp được chia sẻ:")
for file in files_collection.find({ "shared": True }):
    print(file)

# 4.5 Thống kê số lượng tệp theo chủ sở hữu
print("\nSố lượng tệp theo chủ sở hữu:")
owner_stats = files_collection.aggregate([
    { "$group": { "_id": "$owner", "count": { "$sum": 1 } } }
])
for item in owner_stats:
    print(item)

# 4.6 Tìm tất cả tệp của Nguyễn Văn A
print("\nTệp của Nguyen Van A:")
for file in files_collection.find({ "owner": "Nguyen Van A" }):
    print(file)

# 4.7 Tệp lớn nhất
print("\nTệp có kích thước lớn nhất:")
largest_file = files_collection.find().sort("size", -1).limit(1)
for file in largest_file:
    print(file)

# 4.8 Số lượng tệp có kích thước < 1000 KB
print("\nSố lượng tệp < 1000 KB:")
print(files_collection.count_documents({ "size": { "$lt": 1000 } }))

# 4.9 Tất cả tệp tạo trong tháng 1/2024
print("\nTệp tạo trong tháng 1/2024:")
for file in files_collection.find({
    "created_at": {
        "$gte": datetime(2024, 1, 1),
        "$lt": datetime(2024, 2, 1)
    }
}):
    print(file)

# 5. Cập nhật & Xóa theo yêu cầu chính
# 5.1 Update trạng thái chia sẻ file_id = 1
files_collection.update_one(
    { "file_id": 1 },
    { "$set": { "shared": True } }
)

# 5.2 Xóa tệp file_id = 3
files_collection.delete_one({ "file_id": 3 })

# 5.3 Cập nhật tên tệp file_id = 4
files_collection.update_one(
    { "file_id": 4 },
    { "$set": { "name": "New Spreadsheet.xlsx" } }
)

# 5.4 Xóa tất cả tệp có kích thước < 1000KB
files_collection.delete_many({ "size": { "$lt": 1000 } })

# Đóng kết nối
client.close()
