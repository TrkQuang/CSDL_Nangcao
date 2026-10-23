# BIÊN BẢN HỌP NHÓM - TUẦN 2 (KHẢO SÁT & KẾ HOẠCH DỮ LIỆU)

> **Môn học:** Cơ sở dữ liệu nâng cao  
> **Đề tài 17:** Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng mạng xã hội học tập  
> **Thời gian:** 19:30 – 20:30, Thứ Ba ngày 09/09/2026  
> **Địa điểm / Hình thức:** Trực tuyến qua Google Meet  
> **Người chủ trì & Ghi biên bản:** Trần Quang (TV1 - Leader)  
> **Thành viên tham dự:** Đầy đủ 5/5 thành viên.

---

## 1. BÁO CÁO TIẾN ĐỘ TUẦN 1
- **TV1:** Đã tạo khung tài liệu `docs/spec.md`, sơ thảo các quy tắc nghiệp vụ về người dùng, bạn bè, nhóm và bài viết.
- **TV2:** Đã nắm rõ lý thuyết 4 mô hình cây: Adjacency List (cha-con trực tiếp), ltree (chuỗi tiền tố), Nested Set (khoảng bao), Closure Table (ma trận tổ tiên).
- **TV3:** Lên danh sách các bảng cốt lõi: `users`, `friendship`, `study_group`, `post`, `comment`.
- **TV4:** Đã kéo thành công Docker image `neo4j:5-community` và chạy thử giao diện Neo4j Browser ở cổng 7474.
- **TV5:** Đề xuất dùng `generate_series` kết hợp hàm băm để sinh dữ liệu kiểm thử tái lập được với `SEED = 42`.

---

## 2. THẢO LUẬN KỸ THUẬT & QUYẾT ĐỊNH
- **Vấn đề 1: Quan hệ bạn bè đối xứng nên lưu 1 dòng hay 2 dòng?**
  - *Phương án A:* Lưu 2 dòng `(u1, u2)` và `(u2, u1)`. Ưu điểm: truy vấn bạn của `u1` chỉ cần `WHERE user_a = u1`. Nhược điểm: tốn gấp đôi dung lượng, dễ bị lệch pha (có A kết bạn với B nhưng thiếu dòng B kết bạn với A).
  - *Phương án B:* Lưu 1 dòng duy nhất có ràng buộc `user_a < user_b` và tạo View hai chiều `friend_edge` bằng `UNION ALL`.
  - ⇒ **Quyết định:** Chọn **Phương án B**. Tiết kiệm dung lượng bảng gốc, đảm bảo tính nhất quán tuyệt đối, và View `friend_edge` hoàn toàn đáp ứng tốt cho các thuật toán duyệt đồ thị đệ quy.
- **Vấn đề 2: Kế hoạch đồng bộ giữa 4 mô hình cây**
  - *Quyết định:* Để đảm bảo tính công bằng khi benchmark, cả 4 mô hình cây đều lấy dữ liệu gốc từ bảng `comment` (Adjacency List) rồi đồng bộ sang `comment_path`, `comment_ns`, `comment_closure`. Cả 4 bảng phải cho cùng tập kết quả trên bộ dữ liệu nhỏ `seed_test.sql`.

---

## 3. KẾ HOẠCH CHO TUẦN 3
- TV1: Hoàn thiện chi tiết đặc tả 10 quy tắc nghiệp vụ BR1–BR10 trong `docs/spec.md`, vẽ hoàn chỉnh sơ đồ EER trên `docs/eer.drawio`.
- TV2: Soạn thảo khung DDL và các câu truy vấn Q1–Q10 cho 4 mô hình cây.
- TV3: Soạn thảo file `database/schema.sql` và `database/constraints.sql` dựa trên đặc tả của TV1.
- TV4: Xây dựng script Cypher nạp các nút User và quan hệ FRIEND, FOLLOWS.
- TV5: Chuẩn bị kịch bản sinh dữ liệu mẫu 6 người dùng thử nghiệm (An, Binh, Chi, Dung, Em, Phong).
