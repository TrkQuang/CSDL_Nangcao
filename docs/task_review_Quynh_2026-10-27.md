# Rà soát và bàn giao phần Quỳnh — 27/10/2026

## Căn cứ và phạm vi

- `Phutrach.md`, `Phutrach.docx`: Quỳnh phụ trách TV5/Task 5, dữ liệu, FD, chỉ mục, benchmark, nhật ký và hỗ trợ tái lập.
- Đã đối chiếu bốn kế hoạch chính trong `kehoach_word/`, đặc tả, schema, chuẩn hóa, mô hình cây, SQL, graph, transaction và tài liệu tích hợp. Danh mục nguồn tại `review_evidence/2026-10-27/source_inventory.json`.
- Kế hoạch chung có các hướng mở rộng; không gán kết quả Neo4j/OQL/JPQL hoặc thử tải TV4 thành công việc do Quỳnh chạy. Không tuyên bố đã kiểm thử mọi nhánh của toàn bộ mã nguồn.

## Phần thiếu đã hoàn thiện

| Hạng mục | Thay đổi | Kiểm chứng |
| --- | --- | --- |
| FD chưa kiểm đủ thuộc tính, NULL và chưa làm runner dừng khi sai | Thêm assertion toàn dòng f1–f5, BR2/BR6/BR9 trong `normalization/fd_check.sql` | Seed nhỏ và ba quy mô đều đạt |
| Thiếu kiểm thử FD trên dữ liệu sai | Thêm `benchmark/scripts/validate_fd.py`; TEMP không constraint, rollback | 10 trường hợp đạt; runner tích hợp được kiểm tra lại riêng |
| Kế hoạch yêu cầu cây nhiều hình dạng | Thêm `--shape random/chain`, `--seed`; giới hạn chain 1k | 3 cây random 1k/10k/100k và chain 1k, đối chiếu 4 mô hình, tái sinh trùng byte |
| Cần số đo xác minh mới | Chạy đủ benchmark trên cụm SCRAM riêng | 360 dòng, 72 nhóm, mỗi nhóm 5 lần; 78 JSON, 9 biểu đồ |
| Thiếu chương báo cáo riêng và Word | Thêm báo cáo Chương 6 và script build/export | DOCX mở lại thành công, 12 bảng, 9 hình nhúng |

## Các lần chạy và nguồn số liệu

- Run công bố: `benchmark/results/runs/20261027T115624004654Z/`, hoàn thành lúc `2026-10-27T12:01:29.629789+00:00` (19:01:29 ngày 27/10/2026, UTC+7). Có đủ 360 số đo cho ba quy mô, bốn mô hình, hai pha index, ba workload, năm repeats.
- Run cũ 24/10 giữ nguyên thư mục riêng và CSV được archive trước khi công bố lần mới. Không trộn các lần đo.
- Run đầu `20261027T114929271216Z` dừng có chủ đích: assertion BR9 mới có kế hoạch chậm ở 100k. Đã sửa tổng hợp cạnh trước JOIN, dừng cụm riêng và chạy lại toàn bộ. Không đưa run dở vào kết quả. Log FD của run dở giữ tại `review_evidence/2026-10-27/interrupted_fd_100000.txt`.
- Runner đã được bổ sung gọi regression sau khi run công bố khởi động; vì vậy `fd_regression.json` của run công bố không được giả lập bổ sung. Bằng chứng regression nằm ở lượt SQL riêng và run smoke kiểm tích hợp cuối, trong `review_evidence/2026-10-27/runner_smoke/`.
- Run smoke chỉ có 1k, 1 repeat, 24 số đo nhằm kiểm tra runner sau sửa; không đưa vào CSV công bố 360 dòng.

## Kiểm tra đã chạy

- Python: parse/compile mã; PowerShell: parser các `.ps1`, không lỗi cú pháp.
- Cụm DB riêng cho smoke: schema, constraints, seed, Q1–Q12, bốn truy vấn recursive, 4NF, T1 và kiểm FD. Danh sách chính xác trong `smoke_result.json`; log SQL được giữ nguyên.
- Full runner: kiểm Task 3, CRUD và Q1–Q10 của bốn mô hình; kiểm cấu trúc trước/sau thao tác và trước/sau benchmark.
- CSV: 24 file cây/graph mặc định đối chiếu từng dòng, hash; 16 file bổ sung cho random/chain đối chiếu và tái lập byte.
- FD: kiểm dữ liệu hợp lệ, phản ví dụ từng FD, parent_id NULL/non-NULL, friend_count sai và rollback. Có cả kiểm runner tích hợp sau sửa.
- DOCX: xuất bằng python-docx, kiểm ZIP/XML, số bảng/hình và đối chiếu văn bản/bảng với Markdown. Chưa kiểm bố cục bằng Microsoft Word/LibreOffice; không coi kiểm cấu trúc thay thế duyệt in cuối.

## File bàn giao trong docs

- `bao_cao_chuong_6_Quynh.md`: chương đầy đủ, dữ liệu, FD, thiết kế vật lý, phương pháp, số đo, dung lượng, phân tích, tái lập, giới hạn và 9 biểu đồ.
- `bao_cao_chuong_6_Quynh.docx`: bản Word cùng nội dung, bảng và biểu đồ nhúng.
- `scripts/build_quynh_report.py`: dựng báo cáo từ run đã công bố, không điền số mẫu.
- `scripts/export_markdown_docx.py`: xuất Markdown sang Word; `scripts/requirements.txt` ghi phụ thuộc.
- `experiment_log/task5_completed.md`, `review_evidence/2026-10-27/`: nhật ký và minh chứng.

## Giới hạn và việc của thành viên khác

Phần cụ thể của Quỳnh đã có đầu ra và kiểm chứng. Chưa đo hiệu năng random/chain, cold-cache, chuyển subtree lớn hoặc graph R1–R4 trên ba cỡ trong cùng ma trận. Corpus random/chain là bổ sung dữ liệu, không phải số đo thời gian.

Phần tổng hợp toàn bộ báo cáo/slide, xác nhận chữ ký và phần Neo4j của TV4 vẫn do người phụ trách chốt; các lưu ý cũ tại `task_review_2026-10-24.md` không tự biến thành “đã xong” chỉ vì Task 5 được bàn giao. PostgreSQL chạy lại trên cụm mới với phụ thuộc có sẵn; không tuyên bố đã dựng máy sạch hoàn toàn hay chạy lại Neo4j/OQL/JPQL.
