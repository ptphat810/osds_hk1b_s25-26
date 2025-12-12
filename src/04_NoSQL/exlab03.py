from pymongo import MongoClient
from datetime import datetime

# 1. Kết nối đến MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['tiktok']

# 2. Tạo collection
users_collection = db['users']
videos_collection = db['videos']

# Xóa dữ liệu cũ để tránh trùng khi chạy nhiều lần
users_collection.delete_many({})
videos_collection.delete_many({})

# 3. Thêm dữ liệu
# Người dùng
users_data = [
    { 'user_id': 1, 'username': 'user1', 'full_name': 'Nguyen Van A', 'followers': 1500, 'following': 200 },
    { 'user_id': 2, 'username': 'user2', 'full_name': 'Tran Thi B', 'followers': 2000, 'following': 300 },
    { 'user_id': 3, 'username': 'user3', 'full_name': 'Le Van C', 'followers': 500, 'following': 100 }
]
users_collection.insert_many(users_data)

# Videos
videos_data = [
    { 'video_id': 1, 'user_id': 1, 'title': 'Video 1', 'views': 10000, 'likes': 500, 'created_at': datetime(2024, 1, 1) },
    { 'video_id': 2, 'user_id': 2, 'title': 'Video 2', 'views': 20000, 'likes': 1500, 'created_at': datetime(2024, 1, 5) },
    { 'video_id': 3, 'user_id': 3, 'title': 'Video 3', 'views': 5000, 'likes': 200, 'created_at': datetime(2024, 1, 10) }
]
videos_collection.insert_many(videos_data)

# 4. Truy vấn dữ liệu
# 4.1 Xem tất cả người dùng
print("\nTất cả người dùng:")
for user in users_collection.find():
    print(user)

# 4.2 Tìm video có nhiều lượt xem nhất
print("\nVideo nhiều lượt xem nhất:")
top_video = videos_collection.find().sort("views", -1).limit(1)
for video in top_video:
    print(video)

# 4.3 Tìm tất cả video của user1
print("\nTất cả video của user1:")
for video in videos_collection.find({"user_id": 1}):
    print(video)

# 4.4 Tính trung bình lượt thích
print("\nTrung bình likes của tất cả video:")
avg_likes = videos_collection.aggregate([
    { "$group": { "_id": None, "averageLikes": { "$avg": "$likes" } } }
])
for result in avg_likes:
    print(result)

# 4.5 Tìm người dùng có hơn 1000 followers
print("\nNgười dùng có hơn 1000 followers:")
for user in users_collection.find({ "followers": { "$gt": 1000 } }):
    print(user)

# 5. Cập nhật dữ liệu
# 5.1 Update followers user_id = 1 lên 2000
users_collection.update_one(
    { "user_id": 1 },
    { "$set": { "followers": 2000 } }
)

# 5.2 Xóa video video_id = 3
videos_collection.delete_one({ "video_id": 3 })

# 6. Xem lại dữ liệu sau khi cập nhật/xóa
print("\nDữ liệu người dùng sau khi cập nhật:")
for user in users_collection.find():
    print(user)

print("\nDữ liệu video sau khi xóa:")
for video in videos_collection.find():
    print(video)

# Đóng kết nối
client.close()
