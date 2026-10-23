# BẢNG PHÂN CÔNG NHIỆM VỤ CHI TIẾT - ĐỒ ÁN 17

> **Đề tài:** Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng mạng xã hội học tập  
> **Môn học:** Cơ sở dữ liệu nâng cao  
> **Repository:** [https://github.com/TrkQuang/CSDL_Nangcao.git](https://github.com/TrkQuang/CSDL_Nangcao.git)

---

## BẢNG TỔNG QUAN PHÂN CÔNG THÀNH VIÊN

| Mã Task | Thành viên | Vai trò | Trọng tâm phụ trách | File chính phụ trách |
| :---: | :--- | :--- | :--- | :--- |
| **Task 1** | **Trần Quang** *(Leader)* | Phân tích nghiệp vụ, EER, Chuẩn hóa, Tổng hợp báo cáo | BR1–BR10, EER, FD, Bao đóng, Khóa, Phủ tối tiểu, 3NF/BCNF/4NF, Báo cáo & Slide | `docs/spec.md`, `docs/eer.drawio`, `normalization/`, `report/`, `slides/` |
| **Task 2** | **Hưng** | 4 Mô hình dữ liệu cây & Thiết kế Hướng đối tượng | 4 Tree Models (Adjacency List, ltree, Nested Set, Closure Table), Q1–Q10, ODL/OQL, JPQL | `tree_models/`, `oo_model/` |
| **Task 3** | **Hữu** | DDL Schema, SQL Nâng cao, Đệ quy đồ thị & Transaction | Schema chung, Ràng buộc, Seed nhỏ, Q1–Q12 (Trigger/Proc/Func/Dynamic/Embedded), WITH RECURSIVE (R1–R4), T1–T3 | `database/schema.sql`, `sql_advanced/`, `recursive_sql/`, `transactions/t1_success.sql`, `transactions/t2_rollback_savepoint.sql` |
| **Task 4** | **Chương** | CSDL Đồ thị Neo4j/Cypher & Thử tải đồng thời | Cài đặt Neo4j, Import Graph, Cypher đối chiếu R1–R4, Kiểm thử tương tranh Deadlock T3, pgbench | `neo4j/`, `transactions/t3_concurrent/`, `transactions/pgbench/` |
| **Task 5** | **Quỳnh** | Dữ liệu kiểm chứng, Thiết kế vật lý, Chỉ mục & Benchmark | Kiểm chứng FD bằng SQL, Sinh dữ liệu lớn (1k, 10k, 100k), Kế hoạch Indexing, Tự động chạy Benchmark EXPLAIN ANALYZE | `normalization/fd_check.sql`, `database/seed_bench.sql`, `benchmark/`, `docs/experiment_log/` |

---

## CHI TIẾT TỪNG TASK: FILE PHỤ TRÁCH, CÔNG VIỆC VÀ VÍ DỤ

---

### TASK 1: TRẦN QUANG (LEADER)
*Phân tích nghiệp vụ, EER, Phụ thuộc hàm & Chuẩn hóa, Điều phối chung*

#### 1. Các file phụ trách chính:
- [docs/spec.md](file:///c:/Users/shuut/Documents/CSDL_NC/docs/spec.md): Đặc tả 10 quy tắc nghiệp vụ (**BR1 – BR10**) và Từ điển dữ liệu (**Data Dictionary**).
- [docs/eer.drawio](file:///c:/Users/shuut/Documents/CSDL_NC/docs/eer.drawio): Vẽ sơ đồ **EER** (Chuyên biệt hóa bài viết: thảo luận vs tài liệu; Quan hệ đệ quy kết bạn, theo dõi, bình luận).
- [normalization/fd_list.md](file:///c:/Users/shuut/Documents/CSDL_NC/normalization/fd_list.md): Xác định tập phụ thuộc hàm $F$, phân biệt FD đúng nghiệp vụ vs FD tình cờ.
- [normalization/closure_minimal_cover.md](file:///c:/Users/shuut/Documents/CSDL_NC/normalization/closure_minimal_cover.md): Tính bao đóng $X^+$, tìm khóa, tìm phủ tối tiểu $F_{min}$, phân rã 3NF/BCNF (chứng minh bảo toàn thông tin và phụ thuộc hàm).
- [normalization/mvd_4nf.sql](file:///c:/Users/shuut/Documents/CSDL_NC/normalization/mvd_4nf.sql): Phân tích phụ thuộc đa trị (MVD) và dạng chuẩn 4NF.
- [docs/meeting_minutes/meeting_template.md](file:///c:/Users/shuut/Documents/CSDL_NC/docs/meeting_minutes/meeting_template.md): Ghi biên bản họp nhóm hàng tuần (Chuẩn đầu ra CLO7).
- [report/de_tai_17_report_outline.md](file:///c:/Users/shuut/Documents/CSDL_NC/report/de_tai_17_report_outline.md) & [slides/slides_outline.md](file:///c:/Users/shuut/Documents/CSDL_NC/slides/slides_outline.md): Tổng hợp báo cáo hoàn chỉnh (20–30 trang) và slide thuyết trình.

#### 2. Công việc cần làm (CV):
1. Hoàn thiện nội dung các quy tắc nghiệp vụ từ BR3 đến BR10 trong `docs/spec.md`. Gắn từng quy tắc với cơ chế thực thi kỹ thuật (CHECK, Trigger, hay Code logic).
2. Dùng draw.io mở file `docs/eer.drawio` để vẽ hoàn chỉnh sơ đồ EER.
3. Trình bày chi tiết từng bước thuật toán:
   - Bao đóng $X^+$ cho các tập thuộc tính.
   - Tìm tất cả các khóa ứng viên của lược đồ tổng hợp.
   - Tìm phủ tối tiểu $F_{min}$ qua 3 bước (đơn vế phải, loại thuộc tính dư vế trái, loại FD dư).
   - Phân rã theo thuật toán tổng hợp Bernstein về 3NF, kiểm tra BCNF.
4. Điều phối lịch họp mỗi tuần, đôn đốc các thành viên nộp code đúng hạn đường găng.
5. Ghép nối các phần của TV2–TV5 vào file Word/Markdown báo cáo tổng kết.

#### 3. Ví dụ cụ thể:
- **Ví dụ phân biệt FD đúng vs FD tình cờ:**
  - *FD đúng nghiệp vụ:* $UserID \rightarrow Email$ (Một người dùng chỉ có một email duy nhất theo quy tắc BR1).
  - *FD tình cờ (Sai nghiệp vụ):* $FullName \rightarrow Email$ (Trên tập dữ liệu mẫu 6 người thì đúng vì mỗi người một tên, nhưng thực tế nhiều người có thể trùng tên nhau $\Rightarrow$ Không phải FD nghiệp vụ).
- **Ví dụ kiểm tra bảo toàn phụ thuộc hàm:**
  - Nếu phân rã $R$ thành $R_1, R_2, ...$, kiểm tra xem $(F_1 \cup F_2 \cup ...)^+ = F^+$ hay không.

---

### TASK 2: HƯNG
*Mô hình dữ liệu phân cấp (Cây) & Thiết kế hướng đối tượng (OO Model)*

#### 1. Các file phụ trách chính:
- **Thư mục 4 mô hình cây:** [tree_models/](file:///c:/Users/shuut/Documents/CSDL_NC/tree_models/)
  - [tree_models/adjacency_list/](file:///c:/Users/shuut/Documents/CSDL_NC/tree_models/adjacency_list/): `schema.sql`, `crud.sql`, `queries_q1_q10.sql`
  - [tree_models/path_enumeration/](file:///c:/Users/shuut/Documents/CSDL_NC/tree_models/path_enumeration/): `schema.sql`, `crud.sql`, `queries_q1_q10.sql`
  - [tree_models/nested_set/](file:///c:/Users/shuut/Documents/CSDL_NC/tree_models/nested_set/): `schema.sql`, `crud.sql`, `queries_q1_q10.sql`
  - [tree_models/closure_table/](file:///c:/Users/shuut/Documents/CSDL_NC/tree_models/closure_table/): `schema.sql`, `crud.sql`, `queries_q1_q10.sql`
- **Thư mục mô hình đối tượng:** [oo_model/](file:///c:/Users/shuut/Documents/CSDL_NC/oo_model/)
  - [oo_model/class_diagram.drawio](file:///c:/Users/shuut/Documents/CSDL_NC/oo_model/class_diagram.drawio): Vẽ sơ đồ 6 lớp đối tượng.
  - [oo_model/schema.odl](file:///c:/Users/shuut/Documents/CSDL_NC/oo_model/schema.odl): Lược đồ ODL chuẩn ODMG 3.0.
  - [oo_model/oql_queries.md](file:///c:/Users/shuut/Documents/CSDL_NC/oo_model/oql_queries.md): Soạn 5–8 truy vấn OQL kèm kết quả kỳ vọng.
  - [oo_model/jpql_mapping.md](file:///c:/Users/shuut/Documents/CSDL_NC/oo_model/jpql_mapping.md): Ánh xạ sang JPA/JPQL và phân tích lệch pha trở kháng (*Impedance Mismatch*).

#### 2. Công việc cần làm (CV):
1. Hiện thực hoàn chỉnh bộ 10 truy vấn chuẩn **Q1 – Q10** trên cả 4 mô hình cây:
   - Q1: Lấy toàn bộ cây có thụt đầu dòng (indent).
   - Q2: Lấy toàn bộ hậu duệ của một nút.
   - Q3: Lấy toàn bộ tổ tiên (breadcrumb).
   - Q4: Lấy các nút ở độ sâu xác định $k$.
   - Q5: Thêm nút mới.
   - Q6: Xóa nút và toàn bộ cây con.
   - Q7: Di chuyển nhánh (đổi cha) an toàn.
   - Q8: Đếm số nút trong cây con.
   - Q9: Lấy đường đi từ nút hiện tại về gốc.
   - Q10: Kiểm tra nhanh quan hệ tổ tiên - hậu duệ.
2. Kiểm tra để đảm bảo **cả 4 mô hình đều trả về kết quả giống nhau** trên bộ dữ liệu [seed_test.sql](file:///c:/Users/shuut/Documents/CSDL_NC/database/seed_test.sql).
3. Vẽ sơ đồ 6 lớp đối tượng (`NguoiDung`, `NhomHocTap`, `BaiDang`, `BaiThaoLuan`, `BaiTaiLieu`, `BinhLuan`) có kế thừa và phương thức.
4. Viết 8 câu OQL và chuyển đổi sang cú pháp JPQL (Java Persistence Query Language) tương đương.

#### 3. Ví dụ cụ thể:
- **Ví dụ Q2 (Lấy hậu duệ của bình luận `comment_id = 1`) trên 4 mô hình:**
  - *Adjacency List:* Dùng `WITH RECURSIVE subtree AS (...)`
  - *Path Enumeration:* `SELECT * FROM comment_path WHERE path <@ '1';`
  - *Nested Set:* `SELECT * FROM comment_ns WHERE lft BETWEEN parent.lft AND parent.rgt;`
  - *Closure Table:* `SELECT * FROM comment_closure WHERE ancestor = 1;`
  $\Rightarrow$ Cả 4 cách đều phải trả về tập kết quả: `{c1, c2, c3}`.
- **Ví dụ OQL gọi phương thức đối tượng:**
  ```sql
  -- Lấy các bình luận có độ sâu >= 3
  SELECT c.content FROM c IN dsBinhLuan WHERE c.doSau() >= 3;
  ```

---

### TASK 3: HỮU
*Schema CSDL, SQL Nâng cao, SQL Đệ quy Đồ thị & Transaction*

#### 1. Các file phụ trách chính:
- **Lược đồ và dữ liệu ban đầu:**
  - [database/schema.sql](file:///c:/Users/shuut/Documents/CSDL_NC/database/schema.sql): Lược đồ DDL quan hệ chung, bảng, view `friend_edge`. *(Chốt trước Tuần 6)*.
  - [database/constraints.sql](file:///c:/Users/shuut/Documents/CSDL_NC/database/constraints.sql): Các ràng buộc CHECK, FOREIGN KEY.
  - [database/seed_test.sql](file:///c:/Users/shuut/Documents/CSDL_NC/database/seed_test.sql): Nạp bộ dữ liệu kiểm chứng nhỏ (6 người dùng An, Binh, Chi, Dung, Em, Phong).
- **SQL nâng cao:** [sql_advanced/](file:///c:/Users/shuut/Documents/CSDL_NC/sql_advanced/)
  - `q01_q08_select.sql`: 8 câu truy vấn nâng cao (Subquery, NOT EXISTS, Phép chia, Window functions...).
  - `q09_trigger.sql`: Trigger đảm bảo bình luận cha cùng bài viết con (BR6).
  - `q10_procedure.sql`: Stored Procedure kết bạn nguyên tử cập nhật bộ đếm `friend_count`.
  - `q11_function.sql`: Procedure chuyển nhánh chặn chu trình.
  - `q12_dynamic.sql`: Dynamic SQL tìm kiếm bài viết và phân tích chống SQL Injection.
  - `embedded/psycopg2_cursor.py`: Khung code Python minh họa SQL nhúng dùng Cursor.
- **SQL đệ quy đồ thị:** [recursive_sql/](file:///c:/Users/shuut/Documents/CSDL_NC/recursive_sql/)
  - `friends_of_friends.sql`: R1 - Bạn của bạn độ sâu $k=2$.
  - `shortest_path.sql`: R2 - Tìm đường đi ngắn nhất (BFS).
  - `cycle_detection.sql`: R3 - Phát hiện chu trình độ dài 3 đến 5.
  - `recommendation.sql`: R4 - Gợi ý kết bạn theo số bạn chung.
- **Giao dịch:**
  - [transactions/t1_success.sql](file:///c:/Users/shuut/Documents/CSDL_NC/transactions/t1_success.sql): Giao dịch thành công trọn vẹn.
  - [transactions/t2_rollback_savepoint.sql](file:///c:/Users/shuut/Documents/CSDL_NC/transactions/t2_rollback_savepoint.sql): Ngoại lệ, ROLLBACK và SAVEPOINT.

#### 2. Công việc cần làm (CV):
1. Chốt và kiểm tra cú pháp chạy sạch không lỗi cho `database/schema.sql` và `seed_test.sql`.
2. Hoàn thiện các câu truy vấn từ Q3 đến Q8 trong `sql_advanced/q01_q08_select.sql` (kèm giải thích kết quả và lệnh `EXPLAIN ANALYZE`).
3. Viết Trigger Q9, Procedure Q10, Q11 có xử lý ngoại lệ đầy đủ.
4. Hiện thực 4 bài toán đệ quy R1–R4 trên đồ thị bạn bè, đảm bảo khớp với đáp án tính tay:
   - Bạn của bạn của An: `{Dung, Em}`.
   - Đường đi ngắn nhất An $\rightarrow$ Em: `[1, 3, 5]` (độ dài 2).
   - Phát hiện 3 chu trình: `(1-2-3)`, `(2-3-5-4)`, `(1-2-4-5-3)`.
   - Gợi ý bạn bè cho An: `Dung` (1 bạn chung), `Em` (1 bạn chung).
5. Xây dựng 2 kịch bản giao dịch T1 (thành công) và T2 (lỗi giữa chừng có rollback/savepoint).

#### 3. Ví dụ cụ thể:
- **Ví dụ Procedure Q10 (Kết bạn nguyên tử):**
  ```sql
  CALL proc_add_friend(1, 6);
  -- Kiểm tra: Bảng friendship có dòng (1, 6), friend_count của user 1 và 6 đều tăng 1.
  ```
- **Ví dụ Phép chia quan hệ Q3 (Người tham gia MỌI nhóm của chủ đề 'CSDL'):**
  Dùng 2 tầng `NOT EXISTS` lồng nhau: "Tìm sinh viên sao cho KHÔNG TỒN TẠI nhóm CSDL nào mà sinh viên đó KHÔNG tham gia".

---

### TASK 4: CHƯƠNG
*CSDL Đồ thị Neo4j/Cypher & Thử tải đồng thời (Concurrency / Load Testing)*

#### 1. Các file phụ trách chính:
- **Cơ sở dữ liệu đồ thị Neo4j:** [neo4j/](file:///c:/Users/shuut/Documents/CSDL_NC/neo4j/)
  - [neo4j/README.md](file:///c:/Users/shuut/Documents/CSDL_NC/neo4j/README.md): Hướng dẫn bật Neo4j Docker và tài khoản đăng nhập.
  - [neo4j/import/import_nodes_edges.cypher](file:///c:/Users/shuut/Documents/CSDL_NC/neo4j/import/import_nodes_edges.cypher): Nạp 6 Node User và các quan hệ `:FRIEND`, `:FOLLOWS`.
  - [neo4j/cypher/friends_of_friends.cypher](file:///c:/Users/shuut/Documents/CSDL_NC/neo4j/cypher/friends_of_friends.cypher): Cypher bạn của bạn.
  - [neo4j/cypher/shortest_path.cypher](file:///c:/Users/shuut/Documents/CSDL_NC/neo4j/cypher/shortest_path.cypher): Cypher tìm đường ngắn nhất.
  - [neo4j/cypher/cycle_detection.cypher](file:///c:/Users/shuut/Documents/CSDL_NC/neo4j/cypher/cycle_detection.cypher): Cypher tìm chu trình.
- **Thực nghiệm tương tranh & Thử tải:**
  - [transactions/t3_concurrent/session_a.sql](file:///c:/Users/shuut/Documents/CSDL_NC/transactions/t3_concurrent/session_a.sql): Kịch bản Phiên 1 (khóa user 1 rồi xin khóa user 2).
  - [transactions/t3_concurrent/session_b.sql](file:///c:/Users/shuut/Documents/CSDL_NC/transactions/t3_concurrent/session_b.sql): Kịch bản Phiên 2 (khóa user 2 rồi xin khóa user 1 $\rightarrow$ Gây Deadlock).
  - [transactions/t3_concurrent/isolation_matrix.md](file:///c:/Users/shuut/Documents/CSDL_NC/transactions/t3_concurrent/isolation_matrix.md): Bảng ghi nhận kết quả kiểm thử các mức cô lập.
  - [transactions/pgbench/add_friend.sql](file:///c:/Users/shuut/Documents/CSDL_NC/transactions/pgbench/add_friend.sql): File kịch bản thử tải đồng thời qua `pgbench`.

#### 2. Công việc cần làm (CV):
1. Chạy Neo4j Community bằng Docker hoặc Neo4j Desktop.
2. Thực thi file import để tạo đồ thị, sau đó chạy các câu Cypher và chụp ảnh màn hình kết quả trực quan (Graph visualization).
3. So sánh trực quan cú pháp và logic thực thi giữa Cypher (khai báo mẫu đường đi) và `WITH RECURSIVE` của PostgreSQL.
4. Mở 2 cửa sổ terminal psql riêng biệt (Session A và Session B), chạy kịch bản T3 từng bước để kích hoạt lỗi Deadlock (mã lỗi `40P01`).
5. Thử nghiệm trên các mức cô lập: Read Committed, Repeatable Read, Serializable; ghi nhận các hiện tượng (Dirty Read, Non-repeatable Read, Phantom Read, Serialization Anomaly) vào bảng ma trận.
6. Chạy lệnh `pgbench` với các mức tải: 5, 10, 20 kết nối đồng thời (`-c 10 -t 100`), ghi nhận TPS (Transactions Per Second) và độ trễ (Latency).

#### 3. Ví dụ cụ thể:
- **Ví dụ Đường đi ngắn nhất trên Neo4j vs PostgreSQL:**
  - *Neo4j:* `MATCH p = shortestPath((a:User {name:'An'})-[:FRIEND*..6]-(b:User {name:'Em'})) RETURN p;`
  - *PostgreSQL:* Phải viết CTE đệ quy BFS dài 25 dòng kèm mảng kiểm tra nút đã thăm.
  $\Rightarrow$ Đưa ra nhận xét: Neo4j tối ưu hơn về cú pháp và tốc độ duyệt đồ thị sâu.
- **Ví dụ Lệnh chạy pgbench đo tải:**
  ```bash
  pgbench -h localhost -p 5432 -U postgres -d detai17_db -c 10 -j 2 -t 100 -f transactions/pgbench/add_friend.sql
  ```

---

### TASK 5: QUỲNH
*Kiểm chứng dữ liệu, Thiết kế vật lý, Chỉ mục (Indexing) & Benchmark*

#### 1. Các file phụ trách chính:
- **Kiểm chứng phụ thuộc hàm bằng SQL:**
  - [normalization/fd_check.sql](file:///c:/Users/shuut/Documents/CSDL_NC/normalization/fd_check.sql): Viết truy vấn SQL kiểm chứng FD trên database.
- **Sinh dữ liệu lớn:**
  - [database/seed_bench.sql](file:///c:/Users/shuut/Documents/CSDL_NC/database/seed_bench.sql): Script SQL sinh dữ liệu lớn qua `generate_series`.
  - [benchmark/scripts/gen_tree_data.py](file:///c:/Users/shuut/Documents/CSDL_NC/benchmark/scripts/gen_tree_data.py): Script Python sinh cây phân cấp (1.000, 10.000, 100.000 nút) với seed cố định (`SEED = 42`).
  - [benchmark/scripts/gen_graph_data.py](file:///c:/Users/shuut/Documents/CSDL_NC/benchmark/scripts/gen_graph_data.py): Script Python sinh đồ thị mạng xã hội lớn.
- **Kế hoạch chỉ mục & Đo đạc hiệu năng:**
  - [benchmark/README.md](file:///c:/Users/shuut/Documents/CSDL_NC/benchmark/README.md): Bản mô tả kế hoạch đánh chỉ mục cho từng mô hình cây và đồ thị.
  - [benchmark/scripts/run_benchmark.py](file:///c:/Users/shuut/Documents/CSDL_NC/benchmark/scripts/run_benchmark.py): Script tự động chạy và lấy số đo `EXPLAIN (ANALYZE, BUFFERS)`.
  - [benchmark/results/benchmark_results.csv](file:///c:/Users/shuut/Documents/CSDL_NC/benchmark/results/benchmark_results.csv): Lưu trữ dữ liệu số đo thực tế.
  - [docs/experiment_log/log_template.md](file:///c:/Users/shuut/Documents/CSDL_NC/docs/experiment_log/log_template.md): Điền nhật ký thực nghiệm khoa học.

#### 2. Công việc cần làm (CV):
1. Chạy các câu SQL trong `fd_check.sql` để xác minh dữ liệu không vi phạm các FD đã đề ra ở Task 1.
2. Hoàn thiện script Python sinh dữ liệu cây và đồ thị với các quy mô: 1.000, 10.000 và 100.000 bản ghi.
3. Tạo chỉ mục theo kế hoạch:
   - Adjacency List: B-tree trên `parent_id`.
   - Path Enumeration: GiST index trên `path` (`ltree`).
   - Nested Set: Composite index trên `(post_id, lft, rgt)`.
   - Closure Table: Composite index trên `(ancestor, depth)` và `(descendant, ancestor)`.
4. Thực hiện đo đạc so sánh:
   - Chạy lệnh `EXPLAIN (ANALYZE, BUFFERS)` trước khi tạo chỉ mục và sau khi tạo chỉ mục.
   - Ghi lại thời gian chạy (Execution Time), Planning Time, và số trang đọc bộ nhớ (`shared hit`, `shared read`).
   - Đo dung lượng đĩa của bảng và chỉ mục bằng `pg_relation_size()`.
   - Đo chi phí ghi (thời gian INSERT/UPDATE cây khi có chỉ mục).
5. Lưu kết quả thô vào `benchmark_results.csv` và vẽ biểu đồ so sánh cột (Bar chart) để đưa vào báo cáo và slide.
6. Thực hiện chạy lại từ đầu toàn bộ dự án từ một máy sạch theo hướng dẫn trong [README.md](file:///c:/Users/shuut/Documents/CSDL_NC/README.md) để đảm bảo không bị lỗi phụ thuộc.

#### 3. Ví dụ cụ thể:
- **Ví dụ Đo lường trước/sau Index trên Nested Set:**
  ```sql
  -- Trước khi tạo index: Seq Scan, thời gian ~ 45ms, buffer hit = 800 blocks
  EXPLAIN (ANALYZE, BUFFERS) 
  SELECT * FROM comment_ns WHERE lft BETWEEN 2 AND 5;

  -- Tạo Composite Index
  CREATE INDEX idx_ns_bounds ON comment_ns (post_id, lft, rgt);

  -- Sau khi tạo index: Index Scan, thời gian ~ 0.35ms, buffer hit = 5 blocks
  EXPLAIN (ANALYZE, BUFFERS) 
  SELECT * FROM comment_ns WHERE lft BETWEEN 2 AND 5;
  ```
- **Ví dụ Đo dung lượng chỉ mục bằng hàm PostgreSQL:**
  ```sql
  SELECT pg_size_pretty(pg_relation_size('idx_ns_bounds')) AS index_size;
  ```

---

## MA TRẬN PHỐI HỢP & REVIEW CHÉO (CROSS-REVIEW)

Để đảm bảo các phần ghép nối thống nhất thành một đồ án hoàn chỉnh, nhóm áp dụng quy trình kiểm tra chéo:

```
[Trần Quang (TV1)] <--- Review chéo ---> [Hữu (TV3)]: Khớp Schema DDL & Chuẩn hóa
[Hưng (TV2)]       <--- Review chéo ---> [Quỳnh (TV5)]: Khớp Dữ liệu cây & Benchmark
[Chương (TV4)]     <--- Review chéo ---> [Hữu (TV3)]: Khớp Recursive SQL & Cypher
[Quỳnh (TV5)]      <--- Review chéo ---> [Chương (TV4)]: Khớp Số liệu thử tải & Deadlock
```

- **Quy tắc Git:** Mỗi thành viên làm việc trên nhánh riêng (`feature/task1-eer`, `feature/task2-tree-models`, ...). Khi hoàn thành, tạo Pull Request để người phụ trách review duyệt trước khi merge vào nhánh `main`.
