# Task 5 — Dữ liệu, chỉ mục và benchmark

Ngày thực nghiệm: 2026-10-24. Người phụ trách: Quỳnh.

## Môi trường

- OS: Windows-10-10.0.19045-SP0
- CPU: Intel64 Family 6 Model 142 Stepping 9, GenuineIntel; 4 logical CPU.
- RAM: 17038536704 byte.
- Python: 3.15.0 (tags/v3.15.0:d220409, Oct  9 2026, 11:55:56) [MSC v.1951 64 bit (AMD64)]
- PostgreSQL: PostgreSQL 16.15, compiled by Visual C++ build 1944, 64-bit
- `effective_cache_size`: `524288` 8kB
- `jit`: `on`
- `max_connections`: `100`
- `shared_buffers`: `16384` 8kB
- `work_mem`: `4096` kB

## Thiết kế thực nghiệm

- Dữ liệu sinh, không dùng SNAP: cây tam phân breadth-first; đồ thị SQL dạng vòng, mỗi user nối 5 user kế tiếp, cạnh lưu một lần.
- CSV đồ thị dùng bộ sinh ngẫu nhiên seed 42; đây là corpus riêng để import/đối chiếu Neo4j, không phải đồ thị vòng SQL.
- Ba quy mô: 1.000, 10.000, 100.000 node. Mỗi trường hợp làm nóng 1 lần, đo 5 lần, báo cáo trung vị.
- Q2 lấy subtree node 2, gồm chính node; cả 4 mô hình phải trả cùng số lượng trước khi đo.
- Baseline giữ index PK/UNIQUE. Chỉ bỏ index phụ không gắn ràng buộc, không vô hiệu hóa PK/FK và không ép planner dùng index.
- Pha có index thêm toàn bộ `benchmark/indexes.sql`. Index `(post_id,parent_id)` khớp cả hai điều kiện JOIN trong CTE.
- Đo đọc và dung lượng trước pha ghi, tránh dung lượng bị phình bởi các UPDATE rollback.
- INSERT thêm lá dưới node 2; UPDATE chuyển lá cuối N dưới node 2. Mỗi mô hình tính cả cập nhật `comment` và bảng biểu diễn riêng.
- Mỗi phép ghi dùng SAVEPOINT/ROLLBACK. Kiểm chứng kết quả ghi ở lượt warm-up ngoài khoảng đo; sau benchmark kiểm chứng lại toàn bộ dataset.
- Ghi trong transaction rollback vẫn tạo WAL/dirty buffers/dead tuples. Kết quả là workload ghi ấm, không phải latency COMMIT hay chuyển subtree lớn.
- `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` lưu raw plan; root thường là Aggregate/Result, muốn biết index thực dùng phải xem node con.
- Lưu dung lượng bảng/index/total và danh sách index thực tế theo từng pha. Tất cả thay đổi index trong runner được rollback khi đóng kết nối.
- Cụm PostgreSQL tạm dùng SCRAM, chỉ nghe loopback, mật khẩu sinh ngẫu nhiên không ghi repo; tự dừng/xóa sau chạy, không thay đổi DB người dùng.

## Kiểm chứng đúng đắn

- Seed nhỏ: nạp schema, constraints, seed_test và Q9–Q12; `sql_advanced/validate_task3.sql` chạy thành công.
- Chạy CRUD và Q1–Q10 của cả 4 mô hình trên seed nhỏ, sau mỗi file kiểm chứng dữ liệu không đổi sau rollback.
- Ground truth: subtree(1) = {1,2,3}, ancestors(3) = {1,2}.
- `normalization/fd_check.sql`: mọi SELECT trả 0 dòng trên seed nhỏ và ba dataset lớn. Đây là kiểm chứng dữ liệu, không phải chứng minh FD từ lý thuyết; FD tình cờ vẫn không được coi là quy tắc nghiệp vụ.
- `benchmark/validate_dataset.sql`: so toàn bộ cặp closure với CTE, đường dẫn ltree, khoảng Nested Set, số node, post cha-con và friend_count.
- Kiểm chứng dataset trước và sau benchmark ở từng quy mô; 360 lượt đo hoàn tất, 72 nhóm, mỗi nhóm 5 lượt.
- Corpus CSV: 24 file cây/đồ thị đã kiểm tra nội dung, số dòng và SHA-256 trong `benchmark/results/generated_data_manifest.json`.
- Log gốc và kế hoạch thực thi: `benchmark/results/runs/20261024T071518041213Z/`.

## Kết quả Q2 đọc subtree — trung vị ms

| Số node | Mô hình | Chỉ mục ràng buộc (ms) | Thêm chỉ mục phụ (ms) | Tỉ số trước/sau |
| ---: | --- | ---: | ---: | ---: |
| 1,000 | Adjacency List | 1.474 | 3.085 | 0.48 |
| 1,000 | Path Enumeration | 0.245 | 0.543 | 0.45 |
| 1,000 | Nested Set | 0.316 | 0.197 | 1.60 |
| 1,000 | Closure Table | 0.081 | 0.126 | 0.64 |
| 10,000 | Adjacency List | 17.089 | 7.223 | 2.37 |
| 10,000 | Path Enumeration | 2.210 | 1.268 | 1.74 |
| 10,000 | Nested Set | 2.866 | 0.902 | 3.18 |
| 10,000 | Closure Table | 0.532 | 0.527 | 1.01 |
| 100,000 | Adjacency List | 233.665 | 90.894 | 2.57 |
| 100,000 | Path Enumeration | 48.384 | 15.048 | 3.22 |
| 100,000 | Nested Set | 59.007 | 13.517 | 4.37 |
| 100,000 | Closure Table | 7.658 | 8.841 | 0.87 |

## Chi phí INSERT lá — trung vị ms

| Số node | Mô hình | Chỉ mục ràng buộc (ms) | Thêm chỉ mục phụ (ms) | Tỉ số trước/sau |
| ---: | --- | ---: | ---: | ---: |
| 1,000 | Adjacency List | 0.513 | 0.135 | 3.80 |
| 1,000 | Path Enumeration | 0.452 | 0.182 | 2.48 |
| 1,000 | Nested Set | 22.382 | 22.666 | 0.99 |
| 1,000 | Closure Table | 1.582 | 0.219 | 7.22 |
| 10,000 | Adjacency List | 0.363 | 0.147 | 2.47 |
| 10,000 | Path Enumeration | 0.324 | 0.245 | 1.32 |
| 10,000 | Nested Set | 321.481 | 322.535 | 1.00 |
| 10,000 | Closure Table | 13.250 | 0.230 | 57.61 |
| 100,000 | Adjacency List | 0.304 | 0.182 | 1.67 |
| 100,000 | Path Enumeration | 0.293 | 0.213 | 1.38 |
| 100,000 | Nested Set | 2880.428 | 3403.259 | 0.85 |
| 100,000 | Closure Table | 127.713 | 0.301 | 424.30 |

## Chi phí UPDATE chuyển lá — trung vị ms

| Số node | Mô hình | Chỉ mục ràng buộc (ms) | Thêm chỉ mục phụ (ms) | Tỉ số trước/sau |
| ---: | --- | ---: | ---: | ---: |
| 1,000 | Adjacency List | 0.479 | 0.183 | 2.62 |
| 1,000 | Path Enumeration | 0.585 | 0.243 | 2.41 |
| 1,000 | Nested Set | 36.897 | 25.407 | 1.45 |
| 1,000 | Closure Table | 3.233 | 0.297 | 10.89 |
| 10,000 | Adjacency List | 1.813 | 0.160 | 11.33 |
| 10,000 | Path Enumeration | 1.739 | 0.223 | 7.80 |
| 10,000 | Nested Set | 950.372 | 933.786 | 1.02 |
| 10,000 | Closure Table | 18.589 | 0.339 | 54.83 |
| 100,000 | Adjacency List | 14.347 | 0.880 | 16.30 |
| 100,000 | Path Enumeration | 14.712 | 1.100 | 13.37 |
| 100,000 | Nested Set | 8036.136 | 10148.457 | 0.79 |
| 100,000 | Closure Table | 267.488 | 1.144 | 233.82 |

## Dung lượng index

| Số node | Bảng | Index trước (byte) | Index sau (byte) | Tăng (byte) |
| ---: | --- | ---: | ---: | ---: |
| 1,000 | comment | 40960 | 73728 | 32768 |
| 1,000 | comment_closure | 204800 | 589824 | 385024 |
| 1,000 | comment_ns | 57344 | 106496 | 49152 |
| 1,000 | comment_path | 40960 | 212992 | 172032 |
| 1,000 | friendship | 172032 | 303104 | 131072 |
| 10,000 | comment | 245760 | 425984 | 180224 |
| 10,000 | comment_closure | 2949120 | 7585792 | 4636672 |
| 10,000 | comment_ns | 319488 | 655360 | 335872 |
| 10,000 | comment_path | 245760 | 2310144 | 2064384 |
| 10,000 | friendship | 1589248 | 2727936 | 1138688 |
| 100,000 | comment | 2260992 | 3915776 | 1654784 |
| 100,000 | comment_closure | 38289408 | 95961088 | 57671680 |
| 100,000 | comment_ns | 3047424 | 6225920 | 3178496 |
| 100,000 | comment_path | 2260992 | 26419200 | 24158208 |
| 100,000 | friendship | 15736832 | 26992640 | 11255808 |

Dung lượng bảng, index và tổng đầy đủ có trong `benchmark/results/benchmark_summary.md` và raw JSON; bảng trên chỉ hiển thị index.

## Phân tích và giới hạn

- Ở 100.000 node, pha thêm index, Q2 nhanh nhất trong lần đo này: **Closure Table**.
- Chi phí INSERT cao nhất trong cùng pha: **Nested Set**; UPDATE chuyển lá cao nhất: **Nested Set**.
- Tỉ số trước/sau > 1 là giảm thời gian; < 1 là chậm hơn. Index không bảo đảm tăng tốc mọi truy vấn.
- Closure Table đã có PK `(ancestor,descendant)`, nên baseline vẫn có đường truy cập theo ancestor; không được gọi đây là quét bảng hoàn toàn không index.
- Kết luận chỉ áp dụng cấu trúc cây, node truy vấn, máy và trạng thái cache này. Chưa đo cold-cache, cây dây chuyền, subtree lớn khi ghi hoặc throughput đồng thời.
- Phần pgbench/deadlock và Neo4j do thành viên khác phụ trách; Task 5 cung cấp corpus và số liệu PostgreSQL, không tự nhận đã chạy thay họ.

## Tái lập

```powershell
python -m pip install -r benchmark/requirements.txt
python benchmark/scripts/run_complete.py --postgres-bin "C:\Program Files\PostgreSQL\16\bin"
python benchmark/scripts/gen_tree_data.py --sizes 1000 10000 100000
python benchmark/scripts/gen_graph_data.py --all
python benchmark/scripts/verify_generated_data.py
```

Runner in đường dẫn run mới khi hoàn tất. Chạy `publish_results.py --run-dir <đường_dẫn_run>` để cập nhật bảng, biểu đồ, log và tài liệu. Không cần mật khẩu DB đang dùng vì tạo cụm riêng.

## Minh chứng bàn giao

- CSV chuẩn: `benchmark/results/benchmark_results.csv`.
- Bảng tổng hợp: `benchmark/results/benchmark_summary.md`.
- Biểu đồ: `benchmark/results/charts/`, gồm Q2, INSERT, UPDATE cho cả ba quy mô.
- Nhật ký: `docs/experiment_log/task5_completed.md`.
- Slide nội dung: `slides/task5_benchmark.md`.
- Run gốc: `benchmark/results/runs/20261024T071518041213Z/`; dữ liệu 1k cũ được giữ riêng trong `benchmark/results/archive/`, không gộp vào lần đo này.
