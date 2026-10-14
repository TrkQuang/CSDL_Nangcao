# BIÊN BẢN HỌP NHÓM - TUẦN 6 (CHỐT ĐÓNG BĂNG SCHEMA & TÍCH HỢP HỆ THỐNG)

> **Môn học:** Cơ sở dữ liệu nâng cao  
> **Đề tài 17:** Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng mạng xã hội học tập  
> **Thời gian:** 19:30 – 21:00, Thứ Ba ngày 07/10/2026  
> **Địa điểm / Hình thức:** Trực tuyến qua Google Meet  
> **Người chủ trì & Ghi biên bản:** Trần Quang (TV1 - Leader)  
> **Thành viên tham dự:** Đầy đủ 5/5 thành viên.

---

## 1. BÁO CÁO TIẾN ĐỘ TUẦN 5 & KIỂM TRA MỐC ĐƯỜNG GĂNG TUẦN 6
- **Mốc quan trọng nhất của đồ án:** **ĐÓNG BĂNG SCHEMA TRƯỚC TUẦN 6**.
- **TV1 (Leader):**
  - Đã rà soát chéo giữa phần Phân tích nghiệp vụ / Chuẩn hóa (Task 1) và phần Cài đặt CSDL của TV3.
  - Xác nhận tất cả các bảng, khóa chính, khóa ngoại, ràng buộc CHECK, View `friend_edge` và 4 mô hình cây đều thống nhất và khớp với lý thuyết.
- **TV3:**
  - Chạy thử nghiệm thành công file `database/schema.sql`, `database/constraints.sql` và `database/seed_test.sql` trên PostgreSQL 15 sạch, không gặp bất kỳ lỗi cú pháp nào.
  - Đã nạp thành công 6 người dùng mẫu: An, Binh, Chi, Dung, Em, Phong cùng các liên kết bạn bè, nhóm, bài viết và cây bình luận.
- **TV2, TV4, TV5:**
  - Đồng thuận đóng băng lược đồ dữ liệu chung để tập trung triển khai các bài toán chuyên sâu (4 mô hình cây, đệ quy đồ thị, Cypher, Deadlock và Benchmark).

---

## 2. KẾT QUẢ ĐỐI SOÁT VÀ NGIỆM THU ĐẦU RA GIAI ĐOẠN 1
| Hạng mục | Người phụ trách | Trạng thái nghiệm thu | Đánh giá của Leader (TV1) |
| :--- | :---: | :---: | :--- |
| Đặc tả nghiệp vụ BR1–BR10 (`docs/spec.md`) | TV1 | **HOÀN THÀNH** | Đầy đủ 10 quy tắc, có cơ chế kỹ thuật và kịch bản vi phạm. |
| Bản vẽ EER (`docs/eer.drawio`) | TV1 | **HOÀN THÀNH** | Đầy đủ chuyên biệt hóa d/total, quan hệ đệ quy, thuộc tính đa trị, dẫn xuất. |
| Danh sách FD & Bao đóng (`normalization/fd_list.md`) | TV1 | **HOÀN THÀNH** | Có ví dụ phản chứng FD tình cờ, lý giải ràng buộc đệ quy. |
| Phủ tối tiểu, 3NF/BCNF, Chase (`closure_minimal_cover.md`) | TV1 | **HOÀN THÀNH** | Chứng minh hình thức chuẩn xác, bảo toàn thông tin và FD. |
| Phụ thuộc đa trị & 4NF (`normalization/mvd_4nf.sql`) | TV1 | **HOÀN THÀNH** | Mã SQL chạy sạch, chứng minh tích Descartes và phân rã 4NF. |
| DDL Schema chung (`database/schema.sql`) | TV3 | **HOÀN THÀNH** | Chốt đóng băng, không phát sinh lỗi phụ thuộc. |
| Dữ liệu kiểm chứng nhỏ (`database/seed_test.sql`) | TV3 & TV5 | **HOÀN THÀNH** | Đúng dữ liệu chuẩn để kiểm thử Q1–Q10 và R1–R4. |

---

## 3. KẾ HOẠCH CHO GIAI ĐOẠN 2 (TUẦN 7 – TUẦN 9)
- TV1: Tiếp tục cập nhật đề cương chi tiết báo cáo tổng kết (`report/de_tai_17_report_outline.md`), hỗ trợ TV2 và TV3 rà soát lý thuyết phần CSDL đối tượng (ODL/OQL) và SQL đệ quy.
- TV2: Hoàn tất đo lường Q1–Q10 trên cây phân cấp, viết xong ODL/OQL.
- TV3: Hiện thực 4 câu đệ quy đồ thị R1–R4 (bạn của bạn, đường đi ngắn nhất BFS, chu trình, gợi ý bạn bè).
- TV4: Thực nghiệm kích hoạt Deadlock T3 trên 2 terminal psql, nạp đồ thị vào Neo4j và chạy Cypher đối chiếu.
- TV5: Chạy các kịch bản benchmark trên tập dữ liệu 1k, 10k và 100k bản ghi; xuất file kết quả CSV.
