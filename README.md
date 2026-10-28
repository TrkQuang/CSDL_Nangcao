# ĐỒ ÁN 17: DỮ LIỆU PHÂN CẤP VÀ DỮ LIỆU ĐỒ THỊ TRONG CSDL QUAN HỆ

## ỨNG DỤNG: MẠNG XÃ HỘI HỌC TẬP (SOCIAL LEARNING NETWORK)

> **Môn học:** Cơ sở dữ liệu nâng cao  
> **Hệ quản trị CSDL chính:** PostgreSQL 16+ (Hỗ trợ extension `ltree`)  
> **CSDL đối chiếu:** Neo4j Community Edition 5.x  
> **Ngôn ngữ kịch bản:** SQL (PL/pgSQL), Cypher, Python (Benchmark & Embedded SQL)

---

## 1. Mục Tiêu & Phạm Vi Đề Tài

Dự án tập trung giải quyết bài toán biểu diễn, lưu trữ, truy vấn và tối ưu hóa hai dạng cấu trúc dữ liệu phức tạp trên hệ quản trị CSDL quan hệ (RDBMS):
1. **Dữ liệu phân cấp (Cây - Hierarchical Tree Data):** Cây bình luận nhiều cấp của bài viết và cây thư mục tài liệu nhóm học tập. Hiện thực và so sánh 4 mô hình: *Adjacency List*, *Path Enumeration (ltree)*, *Nested Set*, và *Closure Table*.
2. **Dữ liệu đồ thị (Graph Data):** Mạng lưới quan hệ bạn bè (vô hướng) và theo dõi (có hướng). Triển khai truy vấn đệ quy bằng `WITH RECURSIVE` trên PostgreSQL (bạn của bạn, đường đi ngắn nhất, phát hiện chu trình, gợi ý bạn bè) và đối chiếu trực tiếp với CSDL đồ thị chuyên dụng *Neo4j / Cypher*.
3. **Mô hình Hướng đối tượng (OODBMS):** Thiết kế 6 lớp đối tượng, lược đồ *ODL*, viết truy vấn *OQL*, ánh xạ sang *JPQL* và phân tích độ lệch pha trở kháng (*Impedance Mismatch*).
4. **Giao dịch & Tương tranh (Transactions):** Kiểm thử tính nguyên tử, cơ chế cô lập, bế tắc (*Deadlock*) và thử tải đồng thời bằng *pgbench*.
5. **Thiết kế vật lý & Benchmark:** Đánh giá hiệu năng trước/sau khi đánh chỉ mục trên các quy mô dữ liệu (1k, 10k, 100k bản ghi).

---

## 2. Cấu Trúc Dự Án Chi Tiết

Repository được tổ chức theo cấu trúc module hóa chuẩn mực, phục vụ phân công nhóm và tự động hóa kiểm thử:

```
CSDL_NC/
├── README.md                            # Tài liệu trung tâm: hướng dẫn tổng thể và chạy lại từ đầu
├── tomtat.md                            # Bản tóm tắt tinh gọn các trụ cột kỹ thuật của Đề tài 17
│
├── docs/                                # Đặc tả tài liệu, mô hình và quy trình làm việc nhóm
│   ├── spec.md                          # 10 Quy tắc nghiệp vụ (BR1–BR10) và Từ điển dữ liệu
│   ├── eer.drawio                       # Sơ đồ EER Diagram (chuyên biệt hóa, quan hệ đệ quy)
│   ├── meeting_minutes/                 # Biên bản họp nhóm định kỳ (Minh chứng chuẩn đầu ra CLO7)
│   │   └── meeting_template.md          # Mẫu ghi chép biên bản họp hàng tuần
│   └── experiment_log/                  # Nhật ký thực nghiệm (Benchmark & Concurrency testing)
│       └── log_template.md              # Mẫu ghi chép các lần đo đạc
│
├── normalization/                       # Cơ sở toán học, phụ thuộc hàm và chuẩn hóa dữ liệu
│   ├── fd_list.md                       # Danh sách phụ thuộc hàm F, phân biệt FD nghiệp vụ vs tình cờ
│   ├── closure_minimal_cover.md         # Thuật toán bao đóng, tìm khóa, phủ tối tiểu, 3NF/BCNF
│   ├── fd_check.sql                     # Script SQL kiểm chứng phụ thuộc hàm trên dữ liệu thực tế
│   └── mvd_4nf.sql                      # Phân tích Phụ thuộc đa trị (MVD) và Dạng chuẩn 4 (4NF)
│
├── database/                            # Khởi tạo cơ sở dữ liệu quan hệ (PostgreSQL)
│   ├── schema.sql                       # Lược đồ DDL toàn bộ hệ thống (bảng, view, khóa ngoại)
│   ├── constraints.sql                  # Ràng buộc toàn vẹn nâng cao, CHECK, ASSERTION lý thuyết
│   ├── seed_test.sql                    # Bộ dữ liệu kiểm chứng nhỏ (Ground Truth) có đáp án tính tay
│   └── seed_bench.sql                   # Khung script SQL sinh dữ liệu lớn bằng generate_series
│
├── tree_models/                         # Nghiên cứu và so sánh 4 mô hình lưu trữ cây trên RDBMS
│   ├── README.md                        # Hướng dẫn lý thuyết và danh mục 10 truy vấn chuẩn (Q1–Q10)
│   ├── adjacency_list/                  # Mô hình 1: Danh sách kề (parent_id)
│   │   ├── schema.sql                   # DDL bảng và chỉ mục
│   │   ├── crud.sql                     # Thao tác Thêm, Xóa, Chuyển nhánh
│   │   └── queries_q1_q10.sql           # Bộ 10 câu truy vấn chuẩn dùng WITH RECURSIVE
│   ├── path_enumeration/               # Mô hình 2: Liệt kê đường dẫn (ltree extension)
│   │   ├── schema.sql                   # DDL bảng và GiST index
│   │   ├── crud.sql                     # Chèn nút và cập nhật đường dẫn khi chuyển nhánh
│   │   └── queries_q1_q10.sql           # Bộ 10 câu truy vấn dùng toán tử <@ và @>
│   ├── nested_set/                      # Mô hình 3: Tập lồng (lft, rgt)
│   │   ├── schema.sql                   # DDL bảng và Composite index
│   │   ├── crud.sql                     # Thủ tục cập nhật dời khoảng lft/rgt
│   │   └── queries_q1_q10.sql           # Bộ 10 câu truy vấn dùng mệnh đề BETWEEN
│   └── closure_table/                   # Mô hình 4: Bảng bao đóng (ancestor, descendant, depth)
│       ├── schema.sql                   # DDL bảng quan hệ bao đóng và chỉ mục
│       ├── crud.sql                     # Thao tác chèn nút và nhân bản dòng bao đóng
│       └── queries_q1_q10.sql           # Bộ 10 câu truy vấn thông qua JOIN đơn giản
│
├── sql_advanced/                        # SQL nâng cao & Lập trình thủ tục trên PostgreSQL
│   ├── q01_q08_select.sql               # 8 câu truy vấn nâng cao: Subquery, NOT EXISTS, Window functions...
│   ├── q09_trigger.sql                  # Trigger kiểm tra ràng buộc bình luận cha cùng bài viết (BR6)
│   ├── q10_procedure.sql                # Stored Procedure kết bạn nguyên tử cập nhật bộ đếm
│   ├── q11_function.sql                 # Hàm di chuyển nhánh cây bình luận kèm cơ chế chặn chu trình
│   ├── q12_dynamic.sql                  # SQL động (Dynamic SQL) và kỹ thuật chống SQL Injection
│   └── embedded/                        # Minh họa SQL nhúng (Embedded SQL)
│       ├── psycopg2_cursor.py           # Kết nối Python, dùng cursor và tham số hóa an toàn
│       └── requirements.txt             # Khai báo phụ thuộc thư viện Python
│
├── recursive_sql/                       # Truy vấn đệ quy trên đồ thị bằng WITH RECURSIVE
│   ├── friends_of_friends.sql           # R1: Tìm bạn của bạn (FoF) giới hạn k bước
│   ├── shortest_path.sql                # R2: Tìm đường đi ngắn nhất giữa 2 đỉnh bằng BFS
│   ├── cycle_detection.sql              # R3: Phát hiện và liệt kê chu trình trong đồ thị
│   └── recommendation.sql               # R4: Gợi ý kết bạn theo số lượng bạn chung
│
├── transactions/                        # Giao dịch, Điều khiển đồng thời và Thử tải
│   ├── t1_success.sql                   # T1: Giao dịch thành công, cập nhật đồng bộ hai chiều
│   ├── t2_rollback_savepoint.sql        # T2: Xử lý ngoại lệ, ROLLBACK và SAVEPOINT phục hồi cục bộ
│   ├── t3_concurrent/                   # T3: Thực nghiệm cạnh tranh giữa 2 phiên
│   │   ├── session_a.sql                # Kịch bản khóa dòng ở Phiên A
│   │   ├── session_b.sql                # Kịch bản khóa đối kháng ở Phiên B gây Deadlock (40P01)
│   │   └── isolation_matrix.md          # Ma trận khảo sát các mức cô lập trên PostgreSQL
│   └── pgbench/                         # Thử tải đồng thời
│       └── add_friend.sql               # Kịch bản gọi thủ tục kết bạn ngẫu nhiên bằng pgbench
│
├── oo_model/                            # Thiết kế Hướng đối tượng & Truy vấn OQL
│   ├── class_diagram.drawio             # Sơ đồ 6 lớp đối tượng
│   ├── schema.odl                       # Lược đồ ODL chuẩn ODMG 3.0
│   ├── oql_queries.md                   # Bộ 8 câu truy vấn OQL kèm kết quả kỳ vọng
│   └── jpql_mapping.md                  # Ánh xạ sang JPA/JPQL và phân tích Impedance Mismatch
│
├── neo4j/                               # CSDL Đồ thị chuyên dụng Neo4j & Ngôn ngữ Cypher
│   ├── README.md                        # Hướng dẫn thiết lập Neo4j bằng Docker và quy trình đối chiếu
│   ├── import/                          # Nạp dữ liệu
│   │   └── import_nodes_edges.cypher    # Cypher nạp các Node :User và Relationship :FRIEND, :FOLLOWS
│   ├── cypher/                          # Truy vấn Cypher tương đương với PostgreSQL
│   │   ├── friends_of_friends.cypher    # FoF bằng biểu thức đường đi biến thiên
│   │   ├── shortest_path.cypher         # Tìm đường ngắn nhất bằng hàm shortestPath()
│   │   ├── cycle_detection.cypher       # Phát hiện chu trình khép kín
│   │   └── recommendation.cypher        # Gợi ý kết bạn theo số bạn chung
│   └── screenshots/                     # Minh chứng đồ thị trực quan xuất từ Neo4j Browser
│       ├── 01_neo4j_full_graph.png      # Toàn cảnh đồ thị 6 người dùng
│       ├── 02_neo4j_friends_of_friends.png # Bạn của bạn trực quan
│       ├── 03_neo4j_shortest_path.png   # Đường đi ngắn nhất trực quan
│       └── 04_neo4j_cycle_detection.png # Chu trình đồ thị trực quan
│
├── benchmark/                           # Thiết kế vật lý & Công cụ đo lường hiệu năng tự động
│   ├── README.md                        # Chiến lược đánh chỉ mục và quy trình đo đạc 5 bước
│   ├── storage_sizes.sql                # Đo kích thước bảng và chỉ mục qua pg_relation_size()
│   ├── scripts/                         # Bộ script sinh dữ liệu và đo đạc tự động
│   │   ├── gen_tree_data.py             # Sinh cây phân cấp (1k, 10k, 100k nodes) với seed cố định
│   │   ├── gen_graph_data.py            # Sinh đồ thị mạng xã hội lớn
│   │   ├── run_benchmark.py             # Tự động chạy EXPLAIN ANALYZE BUFFERS và xuất CSV
│   │   ├── plot_results.py              # Tự động vẽ biểu đồ cột so sánh thời gian đọc cây
│   │   └── summarize_results.py         # Tự động tổng hợp bảng kết quả Markdown
│   └── results/                         # Kết quả thực nghiệm và số đo
│       └── benchmark_results.csv        # Bảng dữ liệu đo thời gian và buffer blocks
│
├── report/                              # Tài liệu báo cáo chính thức (25–35 trang)
│   └── de_tai_17_report_outline.md      # Báo cáo tổng kết hoàn chỉnh tích hợp toàn bộ các chương
│
└── slides/                              # Bài trình bày bảo vệ đồ án
    └── slides_outline.md                # Kịch bản 16 slides chi tiết phân bổ cho 5 thành viên
```

---

## 3. Phân Công Trách Nhiệm Nhóm (5 Thành Viên)

> Xem chi tiết danh sách file, công việc cụ thể và ví dụ mẫu cho từng người tại: 👉 [Phutrach.md](file:///c:/Users/shuut/Documents/CSDL_NC/Phutrach.md)

| Thành viên | Vai trò | Phụ trách chính & Đầu ra bắt buộc | Hạng mục hỗ trợ / Review |
| :--- | :--- | :--- | :--- |
| **Trần Quang** *(Leader)* | Nhóm trưởng; Phân tích & Chuẩn hóa | - Quy tắc nghiệp vụ BR1–BR10<br>- Sơ đồ EER Diagram<br>- FD, bao đóng, khóa, phủ tối tiểu, 3NF/BCNF, 4NF<br>- Tổng hợp báo cáo, slide và điều phối chung | Hỗ trợ: Hưng, Hữu<br>Review: Toàn bộ |
| **Hưng** | Dữ liệu phân cấp; Mô hình đối tượng | - 4 mô hình cây (Adjacency List, ltree, Nested Set, Closure Table)<br>- CRUD và bộ 10 truy vấn chuẩn Q1–Q10<br>- Thiết kế 6 lớp đối tượng, lược đồ ODL, truy vấn OQL và ánh xạ JPQL | Hỗ trợ: Quỳnh<br>Review: Hữu |
| **Hữu** | SQL nâng cao, Đệ quy & Giao dịch | - DDL schema.sql và ràng buộc<br>- SQL nâng cao Q1–Q12 (Trigger, Procedure, Function, Dynamic SQL, Embedded)<br>- WITH RECURSIVE (R1–R4)<br>- Kịch bản giao dịch T1–T3 | Hỗ trợ: Chương<br>Review: Trần Quang |
| **Chương** | Neo4j/Cypher; Thử tải đồng thời | - Khởi tạo Neo4j, nạp dữ liệu đồ thị<br>- Viết câu truy vấn Cypher đối chiếu với PostgreSQL<br>- Chạy thử tải đồng thời bằng pgbench, đo lường Deadlock và thông lượng | Hỗ trợ: Hữu, Quỳnh<br>Review: Hưng |
| **Quỳnh** | Dữ liệu, Chỉ mục & Benchmark | - Bộ dữ liệu kiểm chứng và kịch bản sinh dữ liệu lớn (seed_bench, SNAP)<br>- Kế hoạch chỉ mục (B-tree, GiST, Composite)<br>- Thực thi benchmark bằng EXPLAIN ANALYZE BUFFERS<br>- Tự động hóa đo lường và nhật ký thực nghiệm | Hỗ trợ: Cả nhóm<br>Review: Chương |

---

## 4. Hướng Dẫn Tái Lập Dự Án Từ Đầu (Step-by-Step)

Mọi giảng viên hoặc thành viên nhóm đều có thể chạy lại toàn bộ từ một môi trường sạch theo các bước sau:

### Bước 1: Khởi tạo Cơ sở dữ liệu PostgreSQL
```bash
# Đăng nhập PostgreSQL CLI
psql -U postgres

# Tạo cơ sở dữ liệu cho đề tài
CREATE DATABASE detai17_db;
\c detai17_db

# Kích hoạt extension ltree
CREATE EXTENSION IF NOT EXISTS ltree;
```

### Bước 2: Nạp lược đồ và bộ dữ liệu kiểm chứng chuẩn
```bash
# Nạp DDL lược đồ bảng và view
psql -U postgres -d detai17_db -f database/schema.sql

# Nạp ràng buộc mở rộng
psql -U postgres -d detai17_db -f database/constraints.sql

# Nạp bộ dữ liệu kiểm chứng nhỏ (Ground Truth)
psql -U postgres -d detai17_db -f database/seed_test.sql
```

### Bước 3: Kiểm chứng các truy vấn cơ bản
```bash
# Kiểm tra bộ đếm bạn bè và truy vấn đệ quy
psql -U postgres -d detai17_db -f recursive_sql/friends_of_friends.sql
psql -U postgres -d detai17_db -f recursive_sql/shortest_path.sql

# Kiểm tra các câu truy vấn cây trên mô hình Adjacency List
psql -U postgres -d detai17_db -f tree_models/adjacency_list/crud.sql
psql -U postgres -d detai17_db -f tree_models/adjacency_list/queries_q1_q10.sql
```

### Kiểm thử hồi quy Task 3

Sau khi nạp `schema.sql`, `constraints.sql`, `seed_test.sql` và các định nghĩa
Q9–Q12, chạy:

```powershell
psql -X -U postgres -d detai17_db -v ON_ERROR_STOP=1 -f sql_advanced/validate_task3.sql
```

Script kiểm tra seed, bộ đếm bạn bè, Q2/Q3/Q6, trigger Q9, procedure Q10,
chống chu trình Q11 và chống SQL injection ở Q12. Mọi thay đổi kiểm thử được
đặt trong transaction và kết thúc bằng `ROLLBACK`.

### Bước 4: Chạy đối chiếu trên Neo4j
```bash
# Khởi động Neo4j container
docker run -d --name neo4j-detai17 -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password123 neo4j:5.18-community

# Mở trình duyệt http://localhost:7474 và chạy nội dung file:
# 1. neo4j/import/import_nodes_edges.cypher
# 2. neo4j/cypher/friends_of_friends.cypher
```

### Bước 5: Chạy Benchmark và Đo lường
```bash
# Cài đặt thư viện Python
pip install -r benchmark/requirements.txt

# Chạy sinh dữ liệu cây mẫu
psql -U postgres -d detai17_db -v bench_size=1000 -f database/seed_bench.sql
$env:DATABASE_URL = 'postgresql://postgres:password@localhost:5432/detai17_db'

# Chạy khung đo hiệu năng tự động
python benchmark/scripts/run_benchmark.py --dataset-size 1000 --repeats 5 --mode both
python benchmark/scripts/plot_results.py
```

`run_benchmark.py` ghi metrics `EXPLAIN (ANALYZE, BUFFERS)` vao
`benchmark/results/benchmark_results.csv`; `plot_results.py` tao PNG trong
`benchmark/results/charts/`. Xem `benchmark/README.md` de co lenh day du cho
ba kich thuoc du lieu va mau nhat ky thi nghiem.

### Task 5: completed measurements and safe full reproduction

Full results (360 measurements, 1k/10k/100k, reads and writes):
`report/task5_benchmark_results.md`.
Experiment log: `docs/experiment_log/task5_completed.md`.
Slide content: `slides/task5_benchmark.md`.
Quỳnh's complete Chapter 6: `docs/bao_cao_chuong_6_Quynh.md` and
`docs/bao_cao_chuong_6_Quynh.docx` (12 tables, 9 embedded charts).
Latest verification: `docs/task_review_Quynh_2026-10-27.md`.

```powershell
python -m pip install -r benchmark/requirements.txt
python benchmark/scripts/run_complete.py --postgres-bin "C:/Program Files/PostgreSQL/16/bin"
```

This command creates a private password-protected PostgreSQL cluster, runs seed,
validation and all benchmarks, then stops/removes that cluster. Existing databases
are not changed. See `benchmark/README.md` for CSV corpus verification and publishing
the completed run as tables, charts, report, slides and experiment log.

### Review of all five tasks

See `docs/task_review_2026-10-24.md` for member-by-member status, reproduced
PostgreSQL checks, integration fixes and remaining report/slide/Neo4j evidence
items. Raw review logs are in `docs/review_evidence/2026-10-24/`.
