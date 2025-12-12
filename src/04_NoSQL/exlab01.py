from pymongo import MongoClient
from datetime import datetime

# 1. Kết nối đến MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['facebookData']

# 2. Tạo collection
users_collection = db['users']
posts_collection = db['posts']
comments_collection = db['comments']

# Xóa dữ liệu cũ để tránh trùng khi chạy nhiều lần
users_collection.delete_many({})
posts_collection.delete_many({})
comments_collection.delete_many({})

# 3. Thêm dữ liệu
# Người dùng
users_data = [
    { "user_id": 1, "name": "Nguyen Van A", "email": "a@gmail.com", "age": 25 },
    { "user_id": 2, "name": "Tran Thi B", "email": "b@gmail.com", "age": 30 },
    { "user_id": 3, "name": "Le Van C", "email": "c@gmail.com", "age": 22 }
]
users_collection.insert_many(users_data)

# Bài đăng
posts_data = [
    { "post_id": 1, "user_id": 1, "content": "Hôm nay thật đẹp trời!", "created_at": datetime(2024, 10, 1) },
    { "post_id": 2, "user_id": 2, "content": "Mình vừa xem một bộ phim hay!", "created_at": datetime(2024, 10, 2) },
    { "post_id": 3, "user_id": 1, "content": "Chúc mọi người một ngày tốt lành!", "created_at": datetime(2024, 10, 3) }
]
posts_collection.insert_many(posts_data)

# Bình luận
comments_data = [
    { "comment_id": 1, "post_id": 1, "user_id": 2, "content": "Thật tuyệt vời!", "created_at": datetime(2024, 10, 1) },
    { "comment_id": 2, "post_id": 2, "user_id": 3, "content": "Mình cũng muốn xem bộ phim này!", "created_at": datetime(2024, 10, 2) },
    { "comment_id": 3, "post_id": 3, "user_id": 1, "content": "Cảm ơn bạn!", "created_at": datetime(2024, 10, 3) }
]
comments_collection.insert_many(comments_data)

# 4. Truy vấn dữ liệu
# 4.1 Xem tất cả người dùng
print("\nTất cả người dùng:")
for user in users_collection.find():
    print(user)

# 4.2 Xem tất cả bài đăng của user 1
print("\nTất cả bài đăng của user_id = 1:")
for post in posts_collection.find({"user_id": 1}):
    print(post)

# 4.3 Xem tất cả bình luận của post 1
print("\nTất cả bình luận của post_id = 1:")
for cmt in comments_collection.find({"post_id": 1}):
    print(cmt)

# 4.4 Truy vấn người dùng có tuổi > 25
print("\nNgười dùng có độ tuổi > 25:")
for user in users_collection.find({ "age": { "$gt": 25 } }):
    print(user)

# 4.5 Tất cả bài đăng trong tháng 10/2024
print("\nTất cả bài đăng trong tháng 10/2024:")
for post in posts_collection.find({
    "created_at": { "$gte": datetime(2024, 10, 1), "$lt": datetime(2024, 11, 1) }
}):
    print(post)

# 5. Cập nhật dữ liệu
# 5.1 Update bài đăng post_id = 1
posts_collection.update_one(
    { "post_id": 1 },
    { "$set": { "content": "Hôm nay thời tiết thật đẹp!" } }
)

# 5.2 Xóa bình luận comment_id = 2
comments_collection.delete_one({ "comment_id": 2 })

# 6. Xem lại dữ liệu sau khi cập nhật/xóa
print("\nDữ liệu bài đăng sau khi cập nhật:")
for post in posts_collection.find():
    print(post)

print("\nDữ liệu bình luận sau khi xóa:")
for cmt in comments_collection.find():
    print(cmt)

# Đóng kết nối
client.close()
