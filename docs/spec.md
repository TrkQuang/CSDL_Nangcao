# ĐẶC TẢ NGHIỆP VỤ & TỪ ĐIỂN DỮ LIỆU (SPEC.MD)

> **Mục đích file:** Tài liệu hóa các quy tắc nghiệp vụ (Business Rules - BR1 đến BR10) và từ điển dữ liệu (Data Dictionary).  
> **Người phụ trách chính:** TV1 (Hỗ trợ: TV2, TV3 | Review: TV4).  
> **Đầu vào:** Đề bài Đề tài 17 - Mạng xã hội học tập.  
> **Đầu ra:** Cơ sở để thiết kế mô hình EER, chuẩn hóa quan hệ và thiết lập ràng buộc toàn vẹn trên database.

---

## 1. Danh Sách Quy Tắc Nghiệp Vụ (BR1 – BR10)

Mỗi quy tắc cần được gán với cơ chế thực thi kỹ thuật cụ thể (Constraint, Trigger, Stored Procedure, Application Logic).

### [VÍ DỤ MẪU]
- **BR1: Tính duy nhất của tài khoản người dùng**
  - *Mô tả:* Mỗi người dùng đăng ký vào hệ thống bằng một địa chỉ email duy nhất.
  - *Cơ chế thực thi:* `UNIQUE(email)` trên bảng `users`.
- **BR2: Quan hệ kết bạn hai chiều (Vô hướng)**
  - *Mô tả:* Kết bạn là quan hệ đối xứng hai chiều. Một cặp người dùng chỉ lưu duy nhất 1 bản ghi với quy ước `user_a < user_b` để tránh trùng lặp dữ liệu, không được tự kết bạn với chính mình.
  - *Cơ chế thực thi:* Khóa chính `PRIMARY KEY (user_a, user_b)`, ràng buộc `CHECK (user_a < user_b)` và hàm chuẩn hóa `add_friend`.

---

### [CÁC QUY TẮC CẦN HOÀN THIỆN TIẾP (TODO)]
- **BR3:** Theo dõi (Follow) là quan hệ có hướng... *(Gợi ý: PK(follower_id, followee_id), CHECK(follower_id <> followee_id))*
- **BR4:** Mỗi nhóm học tập (Study Group) có duy nhất 1 chủ nhóm (Owner)... *(Gợi ý: group_member.role, ràng buộc toàn vẹn)*
- **BR5:** Quyền đăng bài trong nhóm học tập... *(Gợi ý: chỉ thành viên nhóm mới được đăng bài - Trigger hoặc Procedure)*
- **BR6:** Phân cấp bình luận (Comment hierarchy)... *(Gợi ý: bình luận cha phải cùng bài viết với con, không tạo chu trình)*
- **BR7:** Chuyên biệt hóa bài viết (Thảo luận vs Tài liệu)... *(Gợi ý: CHECK(post_type IN ('thaoluan', 'tailieu')))*
- **BR8:** Tương tác bài viết (Reaction)... *(Gợi ý: mỗi người chỉ like/react tối đa 1 lần trên 1 bài)*
- **BR9:** Phân cấp thư mục tài liệu (Folder hierarchy)... *(Gợi ý: thư mục cha cùng nhóm, không lặp)*
- **BR10:** Tính toàn vẹn của bộ đếm bạn bè... *(Gợi ý: friend_count được duy trì đồng bộ bằng Transaction hoặc Trigger)*

---

## 2. Từ Điển Dữ Liệu (Data Dictionary)

Liệt kê chi tiết các thực thể, kiểu dữ liệu, ràng buộc (Null/Not Null, Default, PK, FK).

| Tên Bảng | Tên Thuộc Tính | Kiểu Dữ Liệu | Ràng Buộc | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- | :--- |
| `users` | `user_id` | `SERIAL` | `PRIMARY KEY` | Mã định danh người dùng |
| `users` | `full_name` | `VARCHAR(100)` | `NOT NULL` | Họ và tên |
| `users` | `email` | `VARCHAR(150)` | `NOT NULL, UNIQUE` | Địa chỉ email đăng nhập |
| `users` | `friend_count` | `INT` | `DEFAULT 0, >= 0` | Số lượng bạn bè (thuộc tính dẫn xuất) |
| *(bổ sung tiếp)* | ... | ... | ... | ... |
