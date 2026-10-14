# BIÊN BẢN HỌP NHÓM - TUẦN 3 (CHỐT ĐẶC TẢ NGHIỆP VỤ & EER)

> **Môn học:** Cơ sở dữ liệu nâng cao  
> **Đề tài 17:** Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng mạng xã hội học tập  
> **Thời gian:** 19:30 – 20:30, Thứ Ba ngày 16/09/2026  
> **Địa điểm / Hình thức:** Trực tuyến qua Google Meet  
> **Người chủ trì & Ghi biên bản:** Trần Quang (TV1 - Leader)  
> **Thành viên tham dự:** Đầy đủ 5/5 thành viên.

---

## 1. BÁO CÁO TIẾN ĐỘ TUẦN 2
- **TV1:** Đã hoàn thiện toàn bộ đặc tả chi tiết 10 quy tắc nghiệp vụ BR1–BR10 trong `docs/spec.md`, hoàn thiện bản vẽ EER Diagram trong `docs/eer.drawio` với chuyên biệt hóa Disjoint/Total và quan hệ đệ quy.
- **TV2:** Đã viết xong khung truy vấn Q1–Q10 cho Adjacency List và ltree.
- **TV3:** Đã viết dự thảo `database/schema.sql` gồm các bảng `users`, `friendship`, `study_group`, `post`, `comment`.
- **TV4:** Đã viết xong file script Cypher import dữ liệu đồ thị mẫu.
- **TV5:** Đã tạo danh sách kiểm tra các FD bằng SQL trong `normalization/fd_check.sql`.

---

## 2. THẢO LUẬN KỸ THUẬT & QUYẾT ĐỊNH
- **Vấn đề 1: Lựa chọn phương án ánh xạ kế thừa cho bài viết (Post Specialization)**
  - TV1 trình bày phân tích 3 phương án: Single Table (bảng đơn có `post_type`), Class Table (bảng cha + bảng con), Concrete Table (mỗi lớp 1 bảng).
  - *Đánh giá:* Mạng xã hội học tập cần truy vấn đa hình (hiển thị newsfeed tổng hợp mọi bài viết) liên tục. Nếu dùng Class Table sẽ tốn chi phí `JOIN`, Concrete Table phải `UNION`. Thuộc tính riêng của hai lớp con rất ít (`khoa_binh_luan` cho thảo luận; `file_url`, `tags` cho tài liệu).
  - ⇒ **Quyết định:** Thống nhất chọn **Phương án A (Single Table Inheritance)** trên bảng `post`, có cột phân loại `post_type CHECK (post_type IN ('thaoluan', 'tailieu'))`.
- **Vấn đề 2: Ràng buộc quyền đăng bài (BR5) và bình luận cha con (BR6)**
  - BR5 (chỉ thành viên nhóm mới được đăng bài vào nhóm): TV3 sẽ cài đặt bằng Trigger trên bảng `post`.
  - BR6 (bình luận con phải cùng bài viết với cha): TV3 sẽ cài đặt Trigger `trg_check_comment_parent` (câu truy vấn Q9).

---

## 3. KẾ HOẠCH CHO TUẦN 4
- TV1: Khởi động công đoạn Chuẩn hóa CSDL: Lập danh sách tập phụ thuộc hàm $F$, tính bao đóng thuộc tính $X^+$, phân tích các dị thường dữ liệu trên bảng phẳng $R$ và xác định khóa ứng viên.
- TV2: Hoàn thiện nốt 2 mô hình cây còn lại (Nested Set và Closure Table).
- TV3: Tinh chỉnh các ràng buộc trong `schema.sql` và chuẩn bị viết bộ SQL nâng cao Q1–Q8.
- TV4: Bắt đầu viết các câu Cypher tương ứng với bài toán Friends-of-Friends và Shortest Path.
- TV5: Bắt đầu hoàn thiện script Python sinh cây phân cấp (`gen_tree_data.py`).
