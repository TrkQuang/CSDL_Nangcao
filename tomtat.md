# TÓM TẮT ĐỒ ÁN 17 - CƠ SỞ DỮ LIỆU NÂNG CAO

**Đề tài:** Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng mạng xã hội học tập  
**Mục tiêu:** Xây dựng giải pháp lưu trữ, truy vấn, tối ưu hóa và đánh giá hiệu năng dữ liệu phân cấp (Cây) và dữ liệu đồ thị (Graph) trên PostgreSQL, đối chiếu với CSDL đồ thị (Neo4j) và CSDL hướng đối tượng (ODL/OQL).

---

## 1. Các Trụ Cột Kỹ Thuật Chính

1. **Phân tích & Chuẩn hóa dữ liệu:**
   - 10 quy tắc nghiệp vụ cốt lõi (**BR1 – BR10**).
   - Mô hình thực thể kết hợp mở rộng (**EER Diagram**) với chuyên biệt hóa và quan hệ đệ quy.
   - Khảo sát phụ thuộc hàm (**FD**), tìm bao đóng, khóa, phủ tối tiểu, chuẩn hóa **3NF / BCNF**, xét **4NF** (phụ thuộc đa trị).
2. **Dữ liệu phân cấp (4 Tree Models trên RDBMS):**
   - **Adjacency List** (Danh sách kề - dùng `parent_id`).
   - **Path Enumeration** (Liệt kê đường dẫn - dùng extension `ltree`).
   - **Nested Set** (Tập lồng - dùng `lft`, `rgt`).
   - **Closure Table** (Bảng bao đóng - lưu cặp `ancestor`, `descendant`, `depth`).
   - Bộ 10 truy vấn chuẩn **Q1 – Q10** để kiểm chứng và đo lường so sánh.
3. **Dữ liệu đồ thị trên PostgreSQL (Recursive SQL):**
   - Quan hệ bạn bè (vô hướng qua view `friend_edge`) và theo dõi (có hướng).
   - Truy vấn đệ quy `WITH RECURSIVE`: Bạn của bạn (**FoF**), Đường đi ngắn nhất (**Shortest Path**), Phát hiện chu trình (**Cycle Detection**), Gợi ý kết bạn (**Recommendation**).
4. **SQL nâng cao & Lập trình CSDL:**
   - Bộ truy vấn **Q1 – Q8** (Subquery, NOT EXISTS, phép chia, Window functions, EXPLAIN ANALYZE).
   - **Trigger (Q9)**: Kiểm tra ràng buộc cây bình luận.
   - **Procedure (Q10)**: Kết bạn nguyên tử và cập nhật bộ đếm.
   - **Function / Procedure (Q11)**: Di chuyển nhánh, chặn chu trình.
   - **Dynamic SQL (Q12)**: Tìm kiếm linh hoạt & phòng chống SQL Injection.
   - **Embedded SQL**: Kết nối và thực thi qua Python (`psycopg2`).
5. **Giao dịch & Điều khiển đồng thời (Transactions):**
   - **T1**: Giao dịch thành công, cập nhật hai chiều nhất quán.
   - **T2**: Xử lý ngoại lệ, ROLLBACK và SAVEPOINT.
   - **T3**: Cạnh tranh đồng thời giữa 2 phiên, kiểm thử các mức cô lập (Read Committed, Repeatable Read, Serializable) và phát hiện Deadlock.
   - Thử tải bằng `pgbench`.
6. **Mô hình Hướng đối tượng & OQL:**
   - Thiết kế 6 lớp đối tượng, lược đồ **ODL**, 5–8 câu truy vấn **OQL**.
   - Ánh xạ sang **JPQL** và phân tích độ lệch pha trở kháng (Object-Relational Impedance Mismatch).
7. **Đối chiếu CSDL Đồ thị chuyên dụng (Neo4j & Cypher):**
   - Mô hình hóa đồ thị với Node (:User) và Relationship ([:FRIEND], [:FOLLOWS]).
   - Viết các câu Cypher tương đương với WITH RECURSIVE của PostgreSQL và so sánh hiệu năng/cú pháp.
8. **Thiết kế vật lý & Benchmark:**
   - Đánh giá chỉ mục (B-tree, GiST ltree, Composite index).
   - Benchmark trên các kích thước dữ liệu (1.000, 10.000, 100.000+ records) với `EXPLAIN (ANALYZE, BUFFERS)`.
