# BIÊN BẢN HỌP NHÓM - TUẦN 4 (PHỤ THUỘC HÀM, BAO ĐÓNG & TÌM KHÓA)

> **Môn học:** Cơ sở dữ liệu nâng cao  
> **Đề tài 17:** Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng mạng xã hội học tập  
> **Thời gian:** 19:30 – 20:30, Thứ Ba ngày 23/09/2026  
> **Địa điểm / Hình thức:** Trực tuyến qua Google Meet  
> **Người chủ trì & Ghi biên bản:** Trần Quang (TV1 - Leader)  
> **Thành viên tham dự:** Đầy đủ 5/5 thành viên.

---

## 1. BÁO CÁO TIẾN ĐỘ TUẦN 3
- **TV1:** Đã hoàn thiện tài liệu `normalization/fd_list.md`: chỉ ra 3 loại dị thường (Thêm, Xóa, Sửa) trên bảng phẳng $R$, xác định tập phụ thuộc hàm cốt lõi $F = \{f_1, f_2, f_3, f_4, f_5\}$; trình bày thuật toán CLOSURE($X, F$) và chứng minh $\{comment\_id\}$ là khóa duy nhất của $R$.
- **TV2:** Đã hoàn tất cài đặt cấu trúc cho cả 4 mô hình cây trong `tree_models/`.
- **TV3:** Đã nạp thử nghiệm bộ dữ liệu nhỏ 6 người dùng trong `database/seed_test.sql`.
- **TV4:** Đã kiểm tra tính tương đương của truy vấn Friends-of-friends trên Cypher.
- **TV5:** Đã chạy thử file `normalization/fd_check.sql` trên dữ liệu `seed_test.sql`, kết quả trả về 0 dòng vi phạm cho tất cả các FD nghiệp vụ.

---

## 2. THẢO LUẬN KỸ THUẬT & QUYẾT ĐỊNH
- **Vấn đề 1: Phân biệt FD nghiệp vụ vs FD tình cờ (TV1 & TV5 thảo luận)**
  - TV5 phát hiện khi chạy `SELECT full_name, count(distinct email) ...` kết quả trả về 0 dòng vi phạm. Có thể kết luận `full_name -> email` là FD không?
  - ⇒ **Kết luận của TV1:** Tuyệt đối không. Đây là FD tình cờ do tập dữ liệu kiểm chứng chỉ có 6 người tên khác nhau. Trong thực tế nhiều người hoàn toàn có thể trùng họ tên, nên không thể coi `full_name -> email` là FD nghiệp vụ. TV1 đã ghi chú rõ phần này vào `fd_list.md` và `fd_check.sql`.
- **Vấn đề 2: Ràng buộc đệ quy `parent_id -> post_id`**
  - Nhóm thống nhất không đưa quan hệ này vào tập FD phẳng vì `parent_id` có giá trị `NULL` ở bình luận gốc và đây là ràng buộc giữa các dòng khác nhau (inter-row), phải kiểm soát bằng Trigger (BR6).

---

## 3. KẾ HOẠCH CHO TUẦN 5
- TV1: Hoàn thành nốt phần lý thuyết chuẩn hóa nâng cao: Tìm phủ tối tiểu $F_{min}$ qua 3 bước, phân rã về 3NF/BCNF bằng thuật toán Bernstein, vẽ bảng Chase chứng minh Lossless Join, viết script minh họa MVD và dạng chuẩn 4NF (`normalization/mvd_4nf.sql`).
- TV2: Kiểm thử bộ 10 truy vấn Q1–Q10 trên cây kiểm chứng của bài viết 1, đối chiếu để kết quả của 4 mô hình trùng khớp 100%.
- TV3: Viết 8 truy vấn SQL nâng cao (Q1–Q8) trong `sql_advanced/q01_q08_select.sql`.
- TV4: Viết truy vấn đường đi ngắn nhất (Shortest Path) trên Neo4j Cypher.
- TV5: Bắt đầu viết script benchmark tự động lấy số đo `EXPLAIN ANALYZE`.
