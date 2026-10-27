# Task 5 — Dữ liệu, chỉ mục và benchmark

Ngày thực nghiệm: 2026-10-27. Người phụ trách: Quỳnh.

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
- Log gốc và kế hoạch thực thi: `benchmark/results/runs/20261027T115624004654Z/`.

## Kết quả Q2 đọc subtree — trung vị ms

| Số node | Mô hình | Chỉ mục ràng buộc (ms) | Thêm chỉ mục phụ (ms) | Tỉ số trước/sau |
| ---: | --- | ---: | ---: | ---: |
| 1,000 | Adjacency List | 1.461 | 1.235 | 1.18 |
| 1,000 | Path Enumeration | 0.502 | 0.131 | 3.83 |
| 1,000 | Nested Set | 0.317 | 0.160 | 1.98 |
| 1,000 | Closure Table | 0.103 | 0.091 | 1.13 |
| 10,000 | Adjacency List | 17.052 | 5.901 | 2.89 |
| 10,000 | Path Enumeration | 2.136 | 0.913 | 2.34 |
| 10,000 | Nested Set | 2.864 | 1.121 | 2.55 |
| 10,000 | Closure Table | 0.519 | 0.516 | 1.01 |
| 100,000 | Adjacency List | 231.705 | 85.509 | 2.71 |
| 100,000 | Path Enumeration | 36.880 | 13.381 | 2.76 |
| 100,000 | Nested Set | 52.214 | 13.147 | 3.97 |
| 100,000 | Closure Table | 7.148 | 6.814 | 1.05 |

## Chi phí INSERT lá — trung vị ms

| Số node | Mô hình | Chỉ mục ràng buộc (ms) | Thêm chỉ mục phụ (ms) | Tỉ số trước/sau |
| ---: | --- | ---: | ---: | ---: |
| 1,000 | Adjacency List | 0.298 | 0.157 | 1.90 |
| 1,000 | Path Enumeration | 0.291 | 0.216 | 1.35 |
| 1,000 | Nested Set | 20.560 | 22.932 | 0.90 |
| 1,000 | Closure Table | 1.051 | 0.390 | 2.69 |
| 10,000 | Adjacency List | 0.252 | 0.145 | 1.74 |
| 10,000 | Path Enumeration | 0.505 | 0.207 | 2.44 |
| 10,000 | Nested Set | 258.811 | 324.625 | 0.80 |
| 10,000 | Closure Table | 8.618 | 0.359 | 24.01 |
| 100,000 | Adjacency List | 0.279 | 0.197 | 1.42 |
| 100,000 | Path Enumeration | 0.275 | 0.260 | 1.06 |
| 100,000 | Nested Set | 2427.696 | 3391.805 | 0.72 |
| 100,000 | Closure Table | 142.623 | 0.490 | 291.07 |

## Chi phí UPDATE chuyển lá — trung vị ms

| Số node | Mô hình | Chỉ mục ràng buộc (ms) | Thêm chỉ mục phụ (ms) | Tỉ số trước/sau |
| ---: | --- | ---: | ---: | ---: |
| 1,000 | Adjacency List | 0.425 | 0.222 | 1.91 |
| 1,000 | Path Enumeration | 0.421 | 0.300 | 1.40 |
| 1,000 | Nested Set | 21.769 | 46.006 | 0.47 |
| 1,000 | Closure Table | 1.581 | 0.673 | 2.35 |
| 10,000 | Adjacency List | 2.261 | 0.247 | 9.15 |
| 10,000 | Path Enumeration | 1.693 | 0.284 | 5.96 |
| 10,000 | Nested Set | 837.115 | 933.816 | 0.90 |
| 10,000 | Closure Table | 20.177 | 0.246 | 82.02 |
| 100,000 | Adjacency List | 13.560 | 0.684 | 19.82 |
| 100,000 | Path Enumeration | 16.477 | 0.742 | 22.21 |
| 100,000 | Nested Set | 8226.932 | 9180.796 | 0.90 |
| 100,000 | Closure Table | 352.790 | 0.854 | 413.10 |

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
| 10,000 | comment_path | 245760 | 2301952 | 2056192 |
| 10,000 | friendship | 1589248 | 2727936 | 1138688 |
| 100,000 | comment | 2260992 | 3915776 | 1654784 |
| 100,000 | comment_closure | 38289408 | 95961088 | 57671680 |
| 100,000 | comment_ns | 3047424 | 6225920 | 3178496 |
| 100,000 | comment_path | 2260992 | 26370048 | 24109056 |
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
- Run gốc: `benchmark/results/runs/20261027T115624004654Z/`; dữ liệu 1k cũ được giữ riêng trong `benchmark/results/archive/`, không gộp vào lần đo này.
