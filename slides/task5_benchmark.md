# Task 5 — Nội dung slide benchmark

## Slide 1 — Dữ liệu và kiểm chứng
- Dữ liệu sinh: cây tam phân 1k/10k/100k, đồ thị SQL tương ứng 5k/50k/500k cạnh.
- 4 mô hình dùng cùng cây; seed nhỏ có đáp án tính tay.
- FD/BR và cấu trúc cây kiểm chứng trước/sau đo; 24 CSV có SHA-256.

## Slide 2 — Thiết kế chỉ mục và phương pháp
- Baseline giữ PK/UNIQUE; pha sau thêm B-tree, GiST và composite theo mô hình.
- 1 warm-up, 5 repeats, lấy median; EXPLAIN ANALYZE BUFFERS JSON.
- Đo đọc/dung lượng trước ghi. Ghi rollback, không phải COMMIT latency.
- INSERT lá dưới 2, UPDATE chuyển lá N dưới 2; không suy rộng sang chuyển subtree lớn.

## Slide 3 — Q2 tại 100k
- Chèn ảnh `benchmark/results/charts/q2_subtree_100000.png`.
- Mô hình nhanh nhất trong pha thêm index của lần đo: Closure Table.
- Xem bảng tại `report/task5_benchmark_results.md`; không nói index luôn nhanh hơn.

## Slide 4 — Chi phí ghi và dung lượng
- Chèn ảnh `benchmark/results/charts/insert_leaf_100000.png` và `update_moveleaf_100000.png`.
- INSERT cao nhất: Nested Set; UPDATE chuyển lá cao nhất: Nested Set.
- Bảng dung lượng index ở báo cáo; dung lượng total ở summary và raw snapshot.
- Chốt đánh đổi đọc/ghi/dung lượng, giới hạn warm-cache và một cấu trúc cây.

## Demo
Mở `benchmark/results/benchmark_summary.md`, biểu đồ 100k và một raw plan trong `benchmark/results/runs/20261027T115624004654Z/artifacts/`.
