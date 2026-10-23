# BIÊN BẢN HỌP NHÓM - TUẦN 5 (PHỦ TỐI TIỂU, 3NF/BCNF, BẢNG CHASE & 4NF)

> **Môn học:** Cơ sở dữ liệu nâng cao  
> **Đề tài 17:** Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng mạng xã hội học tập  
> **Thời gian:** 19:30 – 20:30, Thứ Ba ngày 30/09/2026  
> **Địa điểm / Hình thức:** Trực tuyến qua Google Meet  
> **Người chủ trì & Ghi biên bản:** Trần Quang (TV1 - Leader)  
> **Thành viên tham dự:** Đầy đủ 5/5 thành viên.

---

## 1. BÁO CÁO TIẾN ĐỘ TUẦN 4
- **TV1:** Đã hoàn thành xuất sắc tài liệu `normalization/closure_minimal_cover.md`:
  - Tìm phủ tối tiểu $F_{min}$ qua 3 bước (tách vế phải, loại bỏ vế trái dư, loại bỏ FD dư).
  - Phân rã theo thuật toán Bernstein thu được 4 quan hệ $R_1, R_2, R_3, R_4$ đạt cả 3NF và BCNF.
  - Chứng minh tính bảo toàn thông tin (Lossless Join) bằng cả 2 phương pháp: Phép nối nhị phân và Bảng ma trận Chase (Chase test matrix).
  - Chứng minh bảo toàn phụ thuộc hàm $(\bigcup \pi_{R_i}(F))^+ = F^+$.
  - Phân tích phi chuẩn hóa có kiểm soát trên 4 mô hình cây và cột `friend_count`.
  - Hoàn thiện script `normalization/mvd_4nf.sql` minh họa MVD $user\_id \twoheadrightarrow interest$, $user\_id \twoheadrightarrow subject$ và phân rã 4NF.
- **TV2:** Đã kiểm thử xong Q1–Q10 trên cây kiểm chứng bài 1; xác nhận cả 4 mô hình cây đều cho ra cùng kết quả: cây con của c1 là `{c1, c2, c3}`, tổ tiên của c3 là `{c1, c2}`, độ sâu c3 bằng 3.
- **TV3:** Đã hoàn thành 8 câu SQL nâng cao (Q1–Q8), có subquery, window functions và phép chia quan hệ.
- **TV4:** Đã đối chiếu xong câu truy vấn bạn của bạn trên Cypher và PostgreSQL đệ quy.
- **TV5:** Đã hoàn thiện kế hoạch đánh chỉ mục cho 4 mô hình cây trong `benchmark/README.md`.

---

## 2. THẢO LUẬN KỸ THUẬT & QUYẾT ĐỊNH
- **Đánh giá của TV3 về tính đồng bộ giữa Chuẩn hóa (TV1) và Schema DDL (TV3):**
  - TV3 đối chiếu 4 quan hệ con $R_1, R_2, R_3, R_4$ do TV1 phân rã với file `database/schema.sql`:
    - $R_1$: tương ứng bảng `comment` (có `comment_id`, `post_id`, `author_id`, `parent_id`, `content`, `created_at`).
    - $R_2$: được gộp vào bảng `post` (vì cùng có khóa `post_id`, bổ sung thêm các thuộc tính riêng của bài viết).
    - $R_3$: tương ứng bảng `study_group` (có `group_id`, `name`, `topic`).
    - $R_4$: tương ứng bảng `users` (có `user_id`, `full_name`, `email`).
  - ⇒ **Kết luận:** Lược đồ CSDL vật lý hoàn toàn khớp 100% với kết quả chuẩn hóa toán học!

---

## 3. KẾ HOẠCH CHO TUẦN 6 (MỐC ĐƯỜNG GĂNG CHỐT SCHEMA)
- TV1: Điều phối toàn bộ nhóm kiểm thử chạy lại từ đầu toàn bộ CSDL sạch để chuẩn bị chốt đóng băng `database/schema.sql`.
- TV2: Hoàn thiện nốt phần thiết kế hướng đối tượng: sơ đồ 6 lớp, lược đồ ODL và 8 câu OQL có kết quả kỳ vọng.
- TV3: Chốt và nộp `database/schema.sql`, `constraints.sql`, `seed_test.sql`; viết tiếp Trigger Q9 và Stored Procedure Q10.
- TV4: Bắt đầu viết kịch bản gây Deadlock T3 trên 2 phiên PostgreSQL (Session A và Session B).
- TV5: Bắt đầu chạy đo lường benchmark trên cây 1.000 và 10.000 nút.
