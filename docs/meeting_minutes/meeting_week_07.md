# BIÊN BẢN HỌP NHÓM - TUẦN 7 (NGHIỆM THU 4 MÔ HÌNH CÂY & ĐỒNG BỘ SCHEMA)

> **Môn học:** Cơ sở dữ liệu nâng cao  
> **Đề tài 17:** Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng mạng xã hội học tập  
> **Thời gian:** 19:30 – 21:00, Thứ Ba ngày 14/10/2026  
> **Địa điểm / Hình thức:** Trực tuyến qua Google Meet  
> **Người chủ trì & Ghi biên bản:** Trần Quang (TV1 - Leader)  
> **Thành viên tham dự:** Đầy đủ 5/5 thành viên (Trần Quang, Hưng, Hữu, Chương, Quỳnh).

---

## 1. BÁO CÁO TIẾN ĐỘ TUẦN 6 & NỘI DUNG CUỘC HỌP
- **Trọng tâm cuộc họp:** Nghiệm thu gói công việc Task 2 (4 mô hình cây phân cấp) và đối soát sự đồng nhất dữ liệu với gói Task 3 (Schema chung).
- **TV2 (Hưng):**
  - Trình bày kết quả hiện thực 10 truy vấn chuẩn (Q1–Q10) trên 4 mô hình: Adjacency List, Path Enumeration (`ltree`), Nested Set, Closure Table.
  - Đã giải quyết triệt để vấn đề lệch tên bảng trước đây: các file `tree_models/*/schema.sql` hiện chỉ tạo thêm chỉ mục (INDEX) trên các bảng chuẩn do TV3 quản lý (`comment`, `comment_path`, `comment_ns`, `comment_closure`).
  - Viết xong bộ script PowerShell tự động kiểm thử `tree_models/_validate/validate.ps1` kiểm tra cả 4 mô hình đạt chuẩn `queries=OK, crud=OK`.
  - Trình bày thiết kế hướng đối tượng: sơ đồ 6 lớp `oo_model/class_diagram.drawio`, lược đồ ODL ODMG 3.0 `oo_model/schema.odl`, 8 truy vấn OQL và phân tích lệch pha trở kháng (Impedance Mismatch) trong `oo_model/jpql_mapping.md`.
- **TV3 (Hữu):**
  - Đã đối soát và xác nhận các bảng và ràng buộc của TV2 hoàn toàn khớp với `database/schema.sql` và `seed_test.sql`.
  - Hữu đang tiến hành hoàn tất bộ 12 câu SQL nâng cao (Q1–Q12) và 4 câu đệ quy đồ thị (R1–R4).
- **TV5 (Quỳnh):**
  - Nhận bàn giao quy ước tên bảng và cấu trúc chỉ mục từ TV2 và TV3 để hoàn thiện script sinh dữ liệu và benchmark tự động.

---

## 2. KẾT QUẢ NGHIỆM THU ĐẦU RA TUẦN 7
| Hạng mục bàn giao | Người thực hiện | Người nghiệm thu | Kết quả nghiệm thu |
| :--- | :---: | :---: | :--- |
| 4 mô hình cây Q1–Q10 & CRUD (`tree_models/`) | TV2 (Hưng) | TV3, TV1 | **HOÀN THÀNH (100%)** — Trả về kết quả đồng nhất trên seed test. |
| Kiểm thử tự động 4 cây (`_validate/validate.ps1`) | TV2 (Hưng) | Cả nhóm | **ĐẠT** — Tự động tạo DB kiểm thử và dọn dẹp sạch sẽ. |
| Tài liệu tổng kết TV2 (`tree_models/TONGKET-TV2.md`) | TV2 (Hưng) | TV1, TV5 | **ĐẠT** — Quy ước rõ ràng về định nghĩa subtree và tổ tiên. |
| Thiết kế CSDL hướng đối tượng (`oo_model/`) | TV2 (Hưng) | TV1 | **ĐẠT** — Đủ ODL 6 lớp, 8 câu OQL và ánh xạ JPQL. |

---

## 3. KẾ HOẠCH CHO TUẦN 8
- **TV3 (Hữu):** Hoàn tất và mở Pull Request cho gói Task 3 (SQL nâng cao, SQL đệ quy R1–R4, Giao dịch T1–T2 và file hồi quy `validate_task3.sql`).
- **TV4 (Chương):** Khởi động Neo4j, nạp đồ thị kiểm chứng, chụp ảnh trực quan màn hình Cypher; thực hiện kịch bản Deadlock T3 trên 2 terminal và chạy đo tải bằng `pgbench`.
- **TV5 (Quỳnh):** Bổ sung công cụ đo dung lượng đĩa `storage_sizes.sql`, script vẽ biểu đồ `plot_results.py` và hoàn thiện đo benchmark.
- **TV1 (Quang):** Review và merge PR Task 3, theo dõi sát tiến độ thực nghiệm của TV4 và TV5.
