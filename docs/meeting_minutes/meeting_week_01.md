# BIÊN BẢN HỌP NHÓM - TUẦN 1 (KHỞI ĐỘNG DỰ ÁN)

> **Môn học:** Cơ sở dữ liệu nâng cao  
> **Đề tài 17:** Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng mạng xã hội học tập  
> **Thời gian:** 19:30 – 20:30, Thứ Ba ngày 02/09/2026  
> **Địa điểm / Hình thức:** Trực tuyến qua Google Meet  
> **Người chủ trì & Ghi biên bản:** Trần Quang (TV1 - Leader)  
> **Thành viên tham dự:** Đầy đủ 5/5 thành viên (Trần Quang, Hưng, Hữu, Chương, Quỳnh).

---

## 1. MỤC TIÊU CUỘC HỌP
- Công bố đề tài được giao: **Đề tài 17 - Mạng xã hội học tập**.
- Thảo luận và thống nhất mục tiêu cốt lõi: So sánh 4 mô hình lưu trữ cây trên RDBMS, so sánh SQL đệ quy (`WITH RECURSIVE`) với CSDL đồ thị (Neo4j), thiết kế CSDL hướng đối tượng (ODL/OQL) và kiểm thử giao dịch đồng thời.
- Phân chia vai trò chính thức cho 5 thành viên theo chuẩn đầu ra môn học (CLO1 đến CLO7).
- Khởi tạo Repository GitHub, quy ước luồng làm việc Git (Gitflow) và cam kết lịch họp định kỳ.

---

## 2. PHÂN CÔNG VAI TRÒ CHÍNH THỨC
| Mã TV | Họ và Tên | Vai trò | Trọng tâm phụ trách |
| :---: | :--- | :--- | :--- |
| **TV1** | **Trần Quang** | *Trưởng nhóm (Leader)* | Điều phối chung, Phân tích nghiệp vụ, Sơ đồ EER, Chuẩn hóa dữ liệu (FD, bao đóng, khóa, phủ tối tiểu, 3NF/BCNF/4NF), Tổng hợp Báo cáo & Slide. |
| **TV2** | **Hưng** | *Kỹ thuật Phân cấp & Đối tượng* | Nghiên cứu và hiện thực 4 mô hình cây (Adjacency List, ltree, Nested Set, Closure Table) với bộ truy vấn Q1–Q10; Thiết kế 6 lớp đối tượng ODL, OQL và ánh xạ sang JPQL. |
| **TV3** | **Hữu** | *Kỹ thuật SQL & Transaction* | Phụ trách DDL `schema.sql`, ràng buộc toàn vẹn, dữ liệu kiểm chứng nhỏ `seed_test.sql`, SQL nâng cao Q1–Q12, SQL đệ quy R1–R4, Giao dịch T1–T3. |
| **TV4** | **Chương** | *Kỹ thuật Đồ thị & Thử tải* | Cài đặt CSDL đồ thị Neo4j bằng Docker, chuyển đổi dữ liệu và viết truy vấn Cypher đối chiếu R1–R4; Thực nghiệm tranh chấp đồng thời Deadlock T3 và đo tải `pgbench`. |
| **TV5** | **Quỳnh** | *Kỹ thuật Benchmark & Tái lập* | Xây dựng script kiểm chứng FD bằng SQL, sinh dữ liệu lớn (1k, 10k, 100k), thiết kế vật lý và kế hoạch chỉ mục (Indexing), đo đạc hiệu năng tự động qua `EXPLAIN ANALYZE`. |

---

## 3. THẢO LUẬN & QUYẾT ĐỊNH KỸ THUẬT
- **Quyết định 1:** Chọn hệ quản trị CSDL quan hệ chính là **PostgreSQL** (phiên bản 15+), do hỗ trợ rất mạnh extension `ltree` cho phân cấp, `pg_trgm` cho tìm kiếm văn bản và cú pháp `WITH RECURSIVE` chuẩn mực.
- **Quyết định 2:** Khởi tạo repository GitHub tại [https://github.com/TrkQuang/CSDL_Nangcao.git](https://github.com/TrkQuang/CSDL_Nangcao.git). Mỗi thành viên phát triển trên nhánh riêng dạng `feature/task<X>-<ten_task>`, khi hoàn thành tạo Pull Request (PR) có ít nhất 1 thành viên review chéo trước khi Leader merge vào `main`.
- **Quyết định 3:** Định kỳ họp ngắn 30 – 45 phút vào tối Thứ Ba hàng tuần để cập nhật tiến độ (Đã làm gì, sắp làm gì, gặp vướng mắc gì).

---

## 4. KẾ HOẠCH CHO TUẦN 2
- TV1: Soạn thảo bản mô tả phạm vi bài toán mạng xã hội học tập, dự thảo 10 quy tắc nghiệp vụ BR1–BR10.
- TV2: Tìm hiểu cú pháp và nguyên lý hoạt động của 4 mô hình lưu trữ cây.
- TV3: Khảo sát các bảng dữ liệu cần có cho schema chung.
- TV4: Thử nghiệm cài đặt Neo4j 5.x qua Docker trên máy cá nhân.
- TV5: Tìm hiểu các công cụ sinh dữ liệu ngẫu nhiên có kiểm soát (Python `faker` / script SQL `generate_series`).
