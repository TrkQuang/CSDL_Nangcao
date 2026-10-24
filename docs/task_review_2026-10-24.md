# Rà soát nhiệm vụ nhóm — 24/10/2026

## Phạm vi và phiên bản

- Đọc phân công `Phutrach.md`, README và các đầu ra thực tế, không chỉ dựa vào tên commit hay bảng tự đánh giá 100%.
- Đã fetch/pull `origin/main` từ `33090e2` lên `98f1729`, nhận 21 file cập nhật Task 4. Thay đổi Task 5 được giữ bằng stash rồi khôi phục, không xung đột.
- Kết quả Task 5 được đo trước lần pull này; commit nền và trạng thái nguồn được ghi riêng trong run/manifest, không gán lại số đo cũ cho commit mới.
- Rà soát bổ sung bằng cụm PostgreSQL 16.15 tạm, SCRAM, loopback; không sửa DB đang dùng. Cụm tạm đã dừng và xóa.
- Bằng chứng chạy bổ sung: `docs/review_evidence/2026-10-24/checks.json` và các log cùng thư mục.

## Kết luận theo thành viên

| Task | Người phụ trách | Đã có và đã kiểm tra | Trạng thái / phần còn lại |
| --- | --- | --- | --- |
| 1 | Trần Quang | BR1–BR10, EER, FD, bao đóng/khóa/phủ tối tiểu/3NF/BCNF/Chase, SQL 4NF, biên bản; thuật toán Python chạy thành công, EER là XML hợp lệ. | Phần phân tích/chuẩn hóa đã có. Báo cáo chung vẫn ghi “TÓM TẮT CÁC CHƯƠNG KỸ THUẬT TIẾP THEO”; cần ghép đầy đủ Task 2–5 và số đo thật. Chưa thấy báo cáo Word/PDF cuối và slide PPTX trong repo; Markdown hiện có chưa chứng minh bản nộp 20–30 trang đã hoàn tất. |
| 2 | Hưng | 4 mô hình Q1–Q10/CRUD, sơ đồ 6 lớp XML hợp lệ, ODL/OQL/JPQL; chạy lại cả 4 mô hình và validator PowerShell thành công sau sửa tích hợp. | Phần kỹ thuật cây đã chạy được. ODL/OQL/JPQL là tài liệu thiết kế, chưa có runtime OODBMS/JPA để tuyên bố chạy thực. Cần cập nhật vài quy ước trong tài liệu tổng kết cho khớp code. |
| 3 | Hữu | Schema/constraints/seed, Q1–Q12, R1–R4, T1/T2, embedded SQL; regression, truy vấn, giao dịch và Python cursor chạy lại đạt. | Đạt phạm vi kỹ thuật đã kiểm tra. T2 cố ý tạo hai lỗi CHECK để minh họa rollback/savepoint; không được coi hai lỗi này là lỗi chưa hoàn thành. |
| 4 | Chương | Đã pull Cypher R1–R4, 4 PNG, log deadlock/isolation, pgbench 5/10/20 clients; số TPS/latency trong bảng khớp log gốc. Chạy độc lập lại pgbench 500/1000/2000 transaction đều không thất bại và friend_count nhất quán; tái hiện 40P01. | Có code và minh chứng thực nghiệm. Lượt rà soát này không chạy lại Neo4j; không xác nhận tốc độ Neo4j từ ảnh graph. README ảnh và một số kết luận cần cập nhật như mục bên dưới. |
| 5 | Quỳnh | Seed/sinh dữ liệu, index, EXPLAIN JSON, đọc/INSERT/UPDATE/dung lượng, CSV, 9 biểu đồ, nhật ký, báo cáo và nội dung slide; đủ 360 số đo, 72 nhóm x 5 repeats; 24 CSV có manifest SHA-256. | Hoàn tất đầu ra Task 5 trên PostgreSQL theo phạm vi đã công bố. Leader cần ghép `report/task5_benchmark_results.md` và `slides/task5_benchmark.md` vào tài liệu chung. |

## Lỗi tích hợp đã sửa trong lần rà soát

1. Adjacency List: `schema.sql` trước đó tạo/index bảng `comment_adjacency`, trong khi toàn bộ truy vấn dùng `comment`. Đã đổi sang index trên bảng chung, không xóa bảng/dữ liệu cũ của người dùng.
2. Adjacency List: chạy `queries_q1_q10.sql` trước CRUD bị thiếu `al_insert_child`. Đã tái hiện và thêm `\ir crud.sql`; validator có thể chạy theo thứ tự cũ.
3. Q4 Adjacency List: thống nhất root `depth=1`, truy vấn depth 2, khớp quy ước các mô hình còn lại. `level=0` của Q1 vẫn dùng cho thụt dòng.
4. Validator/reset Task 2: bỏ hardcode PostgreSQL 18, hỗ trợ `-PsqlPath`, tự tìm PATH/Program Files. Sửa xử lý chuỗi rỗng khi database chưa tồn tại. Đã chạy validator trên PostgreSQL 16 với cả 4 mô hình thành công.
5. `run_pgbench.ps1`: thêm kiểm tra `$LASTEXITCODE`, không còn in “thành công” khi chương trình pgbench trả mã lỗi. Đã kiểm tra cú pháp PowerShell; kiểm thử tải độc lập dùng trực tiếp pgbench.exe.

Log thất bại trước sửa được giữ trong `adjacency_standalone.txt` và `tv2_validation.txt`. Kết quả sau sửa ở `tv2_validation_fixed.txt` và `checks.json`; không nhầm log cũ với lỗi còn tồn tại.

## Việc còn cần chốt trước nộp

### Trần Quang — ghép báo cáo và slide

- Ghép phần kỹ thuật Task 2–4 và `report/task5_benchmark_results.md` vào các chương tương ứng, thay vì giữ các chương sau ở dạng gạch đầu dòng.
- Thay số ví dụ trong `slides/slides_outline.md` khoảng 0,2–0,5 ms và 0,8–1,2 ms bằng bảng/biểu đồ thực nghiệm hiện tại. Ví dụ ở 100k node, có index: Adjacency 90,894 ms, ltree 15,048 ms, Nested Set 13,517 ms, Closure 8,841 ms; không áp dụng các số này cho mọi kích thước.
- Không kết luận Closure Table luôn ghi chậm hoặc Neo4j luôn nhanh hơn chỉ từ tài liệu minh họa. Lần đo Task 5 là đọc subtree và ghi lá, không phải ghi subtree lớn hay cold-cache.
- Bảng “100% / đã ký” trong báo cáo không thay thế việc xác nhận thành viên và bản nộp cuối; không tự xem đây là chữ ký thật.

### Hưng — thống nhất tài liệu bàn giao

- `TONGKET-TV2.md` vừa nói Q9 không tính node hiện tại, vừa mô tả breadcrumb 1→2→3; cần ghi Q9 gồm node, Q3/Q10 là tổ tiên nghiêm ngặt.
- Phần OQL/JPQL chưa có runtime thực, nên mô tả đúng là thiết kế/ánh xạ, không ghi “đã chạy” khi chưa có minh chứng.
- Đường dẫn máy cá nhân và liên kết `file:///...` trong tài liệu không dùng được trên máy thành viên khác; thay bằng đường dẫn tương đối khi hoàn thiện hồ sơ nộp.

### Chương — minh chứng Neo4j và giới hạn phép đo

- `CHECKLIST_TV4.md` nói đã có ảnh trực tiếp, nhưng `neo4j/screenshots/README.md` còn ghi “Chờ bạn chụp” và nói ảnh mô phỏng Python. Đã thấy 4 PNG trong repo; ảnh graph đơn lẻ không đủ xác nhận nguồn chụp hay ba hàng kết quả chu trình. Cần thống nhất mô tả và bổ sung query/result nếu cần nghiệm thu nguồn ảnh.
- 0 lỗi deadlock trong ba lần pgbench là kết quả quan sát, không phải chứng minh “triệt tiêu hoàn toàn” mọi deadlock của toàn hệ thống.
- pgbench chỉ chọn 6 user, tối đa 15 cặp; nhiều lần CALL là cặp đã tồn tại nhưng vẫn chạy cập nhật bộ đếm. Báo cáo đúng workload có cạnh trùng, không gọi toàn bộ transaction là tạo cạnh mới.
- Số đo chạy trên máy/môi trường Task 4 không gộp ngang với số Q2 của Task 5 để kết luận tốc độ hai DB. Chưa có kết quả đo PostgreSQL/Neo4j cùng workload lớn trong lượt rà soát này.

## Bằng chứng đã chạy bổ sung

- `normalization.txt`: Python tìm khóa `comment_id`, Chase lossless và kết quả kiểm tra BCNF.
- `sql_checks.txt`: schema, Q1–Q12, R1–R4, T1, 4NF, kiểm chứng mô hình cây.
- `embedded.txt`: cursor trả về Binh và Chi cho user 1 trên seed nhỏ.
- `t2_expected_errors.txt`: lỗi CHECK có chủ đích; assertion xác nhận post 99 bị rollback và post 100 giữ lại.
- `tv2_validation_fixed.txt`: validator gốc đã sửa, queries-first, tự tìm PostgreSQL 16.
- `deadlock.json`: deadlock thực tế với SQLSTATE `40P01`, transaction được rollback.
- `pgbench_5.txt`, `pgbench_10.txt`, `pgbench_20.txt`: chạy độc lập, 100 transaction/client, không ghi đè log gốc của Chương.
- `benchmark/results/runs/20261024T071518041213Z/`: run Task 5 chuẩn, 360 số đo, 78 JSON plan/storage, kiểm chứng trước/sau; cụm tạm đã dừng.

## Tổng kết

Không còn lý do chờ nhau để làm phần PostgreSQL. Task 2/3/4/5 đã có code và bằng chứng kiểm tra như trên; Task 1 còn khâu tổng hợp tài liệu chung. Nhóm vẫn cần chốt hồ sơ nộp, thống nhất mô tả Neo4j và thay số ví dụ trong slide, thay vì đánh dấu toàn bộ dự án hoàn thành 100% chỉ vì các commit đã được merge.
