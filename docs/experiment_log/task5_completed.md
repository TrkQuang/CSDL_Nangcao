# Nhật ký thực nghiệm Task 5

- Ngày: 2026-10-24; run ID: `20261024T071518041213Z`.
- Trạng thái: hoàn tất 360 lượt đo, không điền số mẫu.
- Môi trường và config: `benchmark/results/runs/20261024T071518041213Z/environment.json`.
- Commit nền: `33090e2edab8ffca1a22e4f9850c640a3e0bd8ae`. Có thay đổi chưa commit; xem manifest nguồn công bố.
- Seed và kiểm chứng: `seed_*.txt`, `validate_*.txt`, `validation.txt`, `fd_*.txt`, `tree_queries.txt` trong run gốc.
- Đầu ra: CSV, 9 biểu đồ, summary và 78 JSON (72 plan + 6 snapshot dung lượng/index).

## Quy trình

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

## Kiểm chứng

- Seed nhỏ: nạp schema, constraints, seed_test và Q9–Q12; `sql_advanced/validate_task3.sql` chạy thành công.
- Chạy CRUD và Q1–Q10 của cả 4 mô hình trên seed nhỏ, sau mỗi file kiểm chứng dữ liệu không đổi sau rollback.
- Ground truth: subtree(1) = {1,2,3}, ancestors(3) = {1,2}.
- `normalization/fd_check.sql`: mọi SELECT trả 0 dòng trên seed nhỏ và ba dataset lớn. Đây là kiểm chứng dữ liệu, không phải chứng minh FD từ lý thuyết; FD tình cờ vẫn không được coi là quy tắc nghiệp vụ.
- `benchmark/validate_dataset.sql`: so toàn bộ cặp closure với CTE, đường dẫn ltree, khoảng Nested Set, số node, post cha-con và friend_count.
- Kiểm chứng dataset trước và sau benchmark ở từng quy mô; 360 lượt đo hoàn tất, 72 nhóm, mỗi nhóm 5 lượt.
- Corpus CSV: 24 file cây/đồ thị đã kiểm tra nội dung, số dòng và SHA-256 trong `benchmark/results/generated_data_manifest.json`.
- Log gốc và kế hoạch thực thi: `benchmark/results/runs/20261024T071518041213Z/`.

## Kết quả và nhận xét

Xem số đầy đủ ở `report/task5_benchmark_results.md` và `benchmark/results/benchmark_summary.md`.

- Ở 100.000 node, pha thêm index, Q2 nhanh nhất trong lần đo này: **Closure Table**.
- Chi phí INSERT cao nhất trong cùng pha: **Nested Set**; UPDATE chuyển lá cao nhất: **Nested Set**.
- Tỉ số trước/sau > 1 là giảm thời gian; < 1 là chậm hơn. Index không bảo đảm tăng tốc mọi truy vấn.
- Closure Table đã có PK `(ancestor,descendant)`, nên baseline vẫn có đường truy cập theo ancestor; không được gọi đây là quét bảng hoàn toàn không index.
- Kết luận chỉ áp dụng cấu trúc cây, node truy vấn, máy và trạng thái cache này. Chưa đo cold-cache, cây dây chuyền, subtree lớn khi ghi hoặc throughput đồng thời.
- Phần pgbench/deadlock và Neo4j do thành viên khác phụ trách; Task 5 cung cấp corpus và số liệu PostgreSQL, không tự nhận đã chạy thay họ.
