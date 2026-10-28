# BIÊN BẢN HỌP NHÓM - TUẦN 8 (TỔNG NGHIỆM THU KỸ THUẬT & HỢP NHẤT HỆ THỐNG)

> **Môn học:** Cơ sở dữ liệu nâng cao  
> **Đề tài 17:** Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng mạng xã hội học tập  
> **Thời gian:** 19:30 – 21:30, Thứ Ba ngày 21/10/2026 (và cập nhật chốt ngày 24/10/2026)  
> **Địa điểm / Hình thức:** Trực tuyến qua Google Meet  
> **Người chủ trì & Ghi biên bản:** Trần Quang (TV1 - Leader)  
> **Thành viên tham dự:** Đầy đủ 5/5 thành viên (Trần Quang, Hưng, Hữu, Chương, Quỳnh).

---

## 1. NỘI DUNG CUỘC HỌP & BÁO CÁO CÁC GÓI KỸ THUẬT

### 1.1 Nghiệm thu gói Task 3 (Hữu - TV3)
- TV3 đã hoàn thành xuất sắc toàn bộ gói SQL nâng cao và SQL đệ quy:
  - 8 truy vấn nâng cao `sql_advanced/q01_q08_select.sql` (phép chia quan hệ, subquery, window functions) có kèm `EXPLAIN ANALYZE`.
  - Trigger Q9, Procedure kết bạn nguyên tử Q10, Procedure chuyển nhánh chặn chu trình Q11, Dynamic SQL chống SQL Injection Q12.
  - Mã nguồn Python minh họa Embedded SQL với Cursor `sql_advanced/embedded/psycopg2_cursor.py`.
  - 4 bài toán đệ quy đồ thị `recursive_sql/` (FoF, BFS đường ngắn nhất, phát hiện chu trình, gợi ý bạn bè).
  - Kịch bản giao dịch T1 (thành công) và T2 (rollback và savepoint).
  - Đã tích hợp script hồi quy tự động `sql_advanced/validate_task3.sql` chạy sạch 100%. Leader đã duyệt và merge Pull Request #1 vào `main`.

### 1.2 Nghiệm thu gói Task 4 (Chương - TV4)
- TV4 đã hoàn thành toàn bộ khối lượng thực nghiệm trên hệ thống đồ thị và tương tranh:
  - Triển khai CSDL đồ thị Neo4j, nạp đồ thị 6 người dùng và các quan hệ `:FRIEND`, `:FOLLOWS`.
  - Chạy các câu Cypher tương đương R1–R4, khớp 100% kết quả với SQL đệ quy của TV3.
  - Đã chụp đủ 4 ảnh màn hình trực quan đồ thị từ Neo4j Browser lưu vào `neo4j/screenshots/`.
  - Kích hoạt thành công lỗi Deadlock (mã lỗi `40P01`) giữa Session A và Session B, lưu log nguyên văn vào `transactions/t3_concurrent/logs/deadlock_t3_log.txt`.
  - Thực nghiệm kiểm chứng các mức cô lập trên PostgreSQL, phát hiện xung đột và ghi vào `transactions/t3_concurrent/isolation_matrix.md`.
  - Viết script `run_pgbench.ps1`, thực hiện đo tải đồng thời với 5, 10, 20 clients, đạt thông lượng hơn 3.400 TPS và lưu log nguyên văn vào `transactions/pgbench/logs/`.
  - Leader đã hỗ trợ hợp nhất toàn bộ kết quả của TV4 vào nhánh chính `main` (commit `98f1729`).

### 1.3 Nghiệm thu gói Task 5 (Quỳnh - TV5)
- TV5 đã hoàn thiện toàn bộ bộ công cụ phục vụ thiết kế vật lý và benchmark:
  - File SQL đo dung lượng đĩa và chỉ mục `benchmark/storage_sizes.sql`.
  - Kịch bản Python tự động chạy `EXPLAIN (ANALYZE, BUFFERS)` lấy số liệu trung vị `run_benchmark.py`.
  - Script Python tự động vẽ biểu đồ cột `benchmark/scripts/plot_results.py`.
  - Script tự động tổng hợp bảng kết quả Markdown `benchmark/scripts/summarize_results.py`.

---

## 2. KẾT QUẢ ĐÁNH GIÁ TIẾN ĐỘ TOÀN NHÓM ĐẾN TUẦN 8
| Thành viên | Trọng tâm phụ trách | Trạng thái kỹ thuật | Trạng thái bàn giao | Đánh giá chung |
| :--- | :--- | :---: | :---: | :--- |
| **Trần Quang (TV1)** | Nghiệp vụ, EER, Chuẩn hóa, Điều phối | 100% Hoàn thành | Đã tích hợp | Xuất sắc |
| **Hưng (TV2)** | 4 Mô hình Cây, Thiết kế OO, ODL/OQL | 100% Hoàn thành | Đã nghiệm thu | Xuất sắc |
| **Hữu (TV3)** | Schema, SQL Nâng cao, Đệ quy, Transaction | 100% Hoàn thành | Đã merge PR #1 | Xuất sắc |
| **Chương (TV4)** | Neo4j, Cypher, Deadlock T3, pgbench | 100% Hoàn thành | Đã merge vào main | Rất tốt |
| **Quỳnh (TV5)** | Dữ liệu kiểm chứng, Chỉ mục, Tooling Benchmark | 95% Hoàn thành | Đã đẩy lên main | Rất tốt |

**Kết luận:** Giai đoạn lập trình và thực nghiệm kỹ thuật của đồ án đã **HOÀN TẤT 100%**. Hệ thống đáp ứng toàn diện mọi chuẩn đầu ra của môn học.

---

## 3. KẾ HOẠCH BÀN GIAO GIAI ĐOẠN CUỐI (TUẦN 9 – TUẦN 12)
1. **Trần Quang (TV1 - Leader):**
   - Chủ trì chắp bút hoàn thiện toàn bộ Báo cáo tổng kết đồ án (25–35 trang) trong thư mục `report/`.
   - Hoàn thiện Slide thuyết trình chính thức (khoảng 20–25 slides) trong thư mục `slides/`.
   - Phân chia kịch bản báo cáo 15 phút (mỗi thành viên 3 phút) và 5 phút demo hệ thống.
2. **Cả nhóm:**
   - Thực hiện kiểm tra chạy lại toàn bộ từ một kho lưu trữ sạch (Clean Clone Test) theo đúng hướng dẫn `README.md`.
   - Tham gia buổi tổng duyệt thử nghiệm (Dry-run) trước khi bước vào buổi bảo vệ chính thức trước hội đồng giảng viên.
