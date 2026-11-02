"""
Chương 6: Thiết kế vật lý, Benchmark 4 mô hình cây, Thử tải pgbench và Ma trận cô lập giao dịch.
"""

from docx import Document
from .styles import (
    add_heading_1, add_heading_2, add_heading_3,
    add_paragraph, add_bullet, add_styled_table, add_code_block, add_figure, add_callout_box
)

def build_ch6(doc: Document):
    add_heading_1(doc, "CHƯƠNG 6: THIẾT KẾ VẬT LÝ, BENCHMARK & THỬ TẢI ĐỒNG THỜI")

    # ========================================================
    # 6.1 THIẾT KẾ VẬT LÝ VÀ CHỈ MỤC
    # ========================================================
    add_heading_2(doc, "6.1 Kế hoạch Đánh chỉ mục & Đo lường dung lượng đĩa")
    add_paragraph(doc, "Thiết kế vật lý (Physical Database Design) là cầu nối quyết định việc chuyển hóa cấu trúc logic thành hiệu năng thực tế. Trong PostgreSQL 18.6, nhóm đã áp dụng chiến lược phân tầng chỉ mục chuyên biệt:")
    add_bullet(doc, "Áp dụng trên toàn bộ các cột khóa ngoại (author_id, group_id, post_id, parent_id) và các cột tìm kiếm đẳng thức/khoảng. Hỗ trợ tìm kiếm logarit O(log N) và loại bỏ hoàn toàn hiện tượng Quét toàn bảng (Seq Scan) gây lãng phí CPU.", bold_prefix="Chỉ mục B-Tree truyền thống: ")
    add_bullet(doc, "Áp dụng trên cột đường dẫn path ltree của bảng comment_path_enum. Chỉ mục GiST lập chỉ mục các mẫu tiền tố phân cấp, tăng tốc các toán tử con (<@) và tổ tiên (@>) lên gấp hàng trăm lần.", bold_prefix="Chỉ mục GiST (Generalized Search Tree): ")
    add_bullet(doc, "Áp dụng trên cột mảng thẻ nhãn tags của bài tài liệu và vector từ khóa to_tsvector phục vụ tìm kiếm toàn văn Full-Text Search. Cho phép tra cứu trực tiếp các tài liệu chứa tập thẻ bất kỳ mà không cần quét tuần tự.", bold_prefix="Chỉ mục GIN (Generalized Inverted Index): ")

    add_paragraph(doc, "Đo lường dung lượng lưu trữ vật lý thực tế trên đĩa cứng tại quy mô 100.000 bản ghi bình luận (trích xuất thông qua các hàm pg_relation_size và pg_total_relation_size):", bold_prefix="Bảng đo lường dung lượng vật lý đĩa cứng (100.000 bản ghi): ")

    storage_headers = ["Tên bảng vật lý", "Dung lượng Bảng (Heap)", "Chỉ mục cơ sở (PK)", "Chỉ mục bổ sung", "Tổng dung lượng vật lý"]
    storage_data = [
        ["comment_adjacency", "11.84 MB (12,414,976 B)", "2.21 MB (2,318,336 B)", "2.21 MB (parent_id)", "16.26 MB (17,051,648 B)"],
        ["comment_path_enum", "13.48 MB (14,131,200 B)", "2.21 MB (2,318,336 B)", "5.02 MB (GiST path)", "20.71 MB (21,716,992 B)"],
        ["comment_nested_set", "12.21 MB (12,804,096 B)", "2.21 MB (2,318,336 B)", "2.58 MB (lft, rgt)", "17.00 MB (17,825,792 B)"],
        ["comment_closure\n(Bảng phụ liên kết)", "58.39 MB (61,227,008 B)\n[1,067,146 dòng cặp!]", "22.45 MB (23,543,808 B)\n(Unique ancestor, desc)", "11.78 MB (descendant_id)", "92.62 MB (97,119,232 B)"],
    ]
    add_styled_table(doc, storage_headers, storage_data, [1.5, 1.4, 1.3, 1.3, 1.3])

    add_callout_box(doc, "PHÁT HIỆN QUAN TRỌNG VỀ DUNG LƯỢNG:\n"
                         "Tại quy mô 100.000 bình luận, trong khi 3 mô hình Adjacency, Path Enum và Nested Set chỉ tiêu tốn từ 16 MB đến 21 MB đĩa cứng, thì mô hình CLOSURE TABLE tiêu tốn tới 92.62 MB (gấp gần 6 lần Adjacency List). Lý do là số lượng cặp quan hệ tổ tiên - hậu duệ trong bảng bao đóng bùng nổ lên tới 1,067,146 dòng dữ liệu! Đây là sự đánh đổi không gian lưu trữ lấy tốc độ đọc mà các kiến trúc sư phần mềm bắt buộc phải cân nhắc khi triển khai thực tế.",
                    "ĐÁNH ĐỔI KHÔNG GIAN BỘ NHỚ CỦA CLOSURE TABLE")

    # ========================================================
    # 6.2 ĐÁNH GIÁ HIỆU NĂNG 4 MÔ HÌNH CÂY (BENCHMARK)
    # ========================================================
    add_heading_2(doc, "6.2 Đánh giá hiệu năng 4 mô hình cây phân cấp (Benchmark Suite)")
    add_paragraph(doc, "Nhóm nghiên cứu đã thiết kế và triển khai một hệ thống đo lường hiệu năng tự động (Benchmark Suite) hoàn chỉnh và nghiêm ngặt:")
    add_bullet(doc, "Quy mô thử nghiệm: Khảo sát tại 3 cấp độ dữ liệu thực tế gồm 1.000 nút (Cây nhỏ), 10.000 nút (Cây trung bình) và 100.000 nút (Cây lớn).")
    add_bullet(doc, "Phương pháp đo: Thực hiện 360 phép đo độc lập trên môi trường PostgreSQL 18.6 thực tế; mỗi phép đo được chạy warm-up cache nhiều lượt để đảm bảo dữ liệu ổn định trong RAM; trích xuất kế hoạch thực thi chi tiết bằng EXPLAIN (ANALYZE, BUFFERS, TIMING, FORMAT JSON).")
    add_bullet(doc, "3 tác vụ kiểm thử trọng yếu: (1) Đọc toàn bộ cây con Q2; (2) Ghi chèn thêm nút lá mới Insert Leaf; (3) Cập nhật di chuyển nhánh cây con Move Subtree sang cha mới.")

    # --- 6.2.1 ĐỌC CÂY CON Q2 ---
    add_heading_3(doc, "6.2.1 Đánh giá tác vụ Đọc cây con (Truy vấn Q2 - Subtree Read)")
    add_paragraph(doc, "Bảng tổng hợp thời gian thực thi (Execution Time tính bằng mili-giây ms) của truy vấn Q2 trước và sau khi bổ sung chỉ mục chuyên biệt:")

    q2_bm_headers = ["Quy mô nút", "Mô hình cây", "Thời gian Baseline (ms)", "Thời gian Có chỉ mục (ms)", "Tốc độ cải thiện (Tỉ số)"]
    q2_bm_data = [
        ["1.000", "Adjacency List", "0.082 ms", "0.076 ms", "1.08x nhanh hơn"],
        ["1.000", "Path Enumeration", "0.024 ms", "0.022 ms", "1.09x nhanh hơn"],
        ["1.000", "Nested Set", "0.019 ms", "0.018 ms", "1.06x nhanh hơn"],
        ["1.000", "Closure Table", "0.017 ms", "0.016 ms", "1.06x nhanh hơn"],
        ["10.000", "Adjacency List", "0.640 ms", "0.580 ms", "1.10x nhanh hơn"],
        ["10.000", "Path Enumeration", "0.045 ms", "0.038 ms", "1.18x nhanh hơn"],
        ["10.000", "Nested Set", "0.032 ms", "0.029 ms", "1.10x nhanh hơn"],
        ["10.000", "Closure Table", "0.028 ms", "0.026 ms", "1.08x nhanh hơn"],
        ["100.000", "Adjacency List", "3.470 ms", "2.490 ms", "1.39x nhanh hơn"],
        ["100.000", "Path Enumeration", "0.150 ms", "0.140 ms", "1.07x nhanh hơn"],
        ["100.000", "Nested Set", "0.052 ms", "0.048 ms", "1.08x nhanh hơn"],
        ["100.000", "Closure Table", "0.042 ms", "0.039 ms", "1.08x nhanh hơn"],
    ]
    add_styled_table(doc, q2_bm_headers, q2_bm_data, [1.0, 1.6, 1.4, 1.4, 1.4])

    add_paragraph(doc, "Dưới đây là 3 biểu đồ trực quan hóa thời gian đọc cây con Q2 tại các quy mô dữ liệu từ 1.000 đến 100.000 nút:")

    add_figure(doc, "benchmark/results/charts/q2_subtree_1000.png", "Hình 6.1: So sánh thời gian truy vấn đọc cây con (Q2) tại quy mô 1.000 nút (ms)", width_inches=5.8)
    add_figure(doc, "benchmark/results/charts/q2_subtree_10000.png", "Hình 6.2: So sánh thời gian truy vấn đọc cây con (Q2) tại quy mô 10.000 nút (ms)", width_inches=5.8)
    add_figure(doc, "benchmark/results/charts/q2_subtree_100000.png", "Hình 6.3: So sánh thời gian truy vấn đọc cây con (Q2) tại quy mô 100.000 nút (ms)", width_inches=5.8)

    add_paragraph(doc, "Nhận xét chuyên sâu về thao tác Đọc: Closure Table và Nested Set là hai mô hình có tốc độ đọc cây con nhanh nhất và ổn định nhất (~0.04ms ở 100.000 nút) vì chúng chuyển hóa bài toán đệ quy thành một phép quét theo khoảng đơn giản (Index Range Scan) hoặc một phép JOIN trực tiếp. Path Enumeration với chỉ mục GiST bám sát rất gần (~0.14ms). Trong khi đó, Adjacency List chậm hơn rõ rệt (2.49ms ở 100k nút, chậm hơn gần 60 lần) do bắt buộc phải thực hiện CTE đệ quy lặp nhiều vòng để tìm từng thế hệ con cháu.")

    # --- 6.2.2 GHI THÊM NÚT LÁ ---
    add_heading_3(doc, "6.2.2 Đánh giá tác vụ Ghi chèn thêm nút lá mới (Insert Leaf)")
    add_paragraph(doc, "Bảng tổng hợp thời gian thực thi thao tác chèn thêm một phản hồi lá mới vào cây:")

    ins_bm_headers = ["Quy mô nút", "Mô hình cây", "Baseline (ms)", "Có chỉ mục (ms)", "Nhận xét hiệu năng ghi"]
    ins_bm_data = [
        ["1.000", "Adjacency List", "0.050 ms", "0.052 ms", "Cực nhanh O(1). Chỉ chèn 1 dòng."],
        ["1.000", "Path Enumeration", "0.070 ms", "0.075 ms", "Đọc path cha + nối chuỗi ltree."],
        ["1.000", "Nested Set", "0.480 ms", "0.520 ms", "Phải UPDATE lft, rgt các nút bên phải."],
        ["1.000", "Closure Table", "0.140 ms", "0.160 ms", "Chèn dòng dữ liệu + các cặp quan hệ."],
        ["10.000", "Adjacency List", "0.055 ms", "0.058 ms", "Duy trì O(1) ổn định tuyệt đối."],
        ["10.000", "Path Enumeration", "0.085 ms", "0.092 ms", "Hiệu năng ghi rất tốt."],
        ["10.000", "Nested Set", "4.120 ms", "4.350 ms", "Chậm gấp 75 lần Adjacency List!"],
        ["10.000", "Closure Table", "0.190 ms", "0.210 ms", "Tốn thêm chi phí chèn bảng phụ."],
        ["100.000", "Adjacency List", "0.065 ms", "0.070 ms", "Vẫn duy trì 0.07ms (O(1))."],
        ["100.000", "Path Enumeration", "0.110 ms", "0.125 ms", "Rất tốt (0.12ms)."],
        ["100.000", "Nested Set", "41.500 ms", "43.800 ms", "Cực kỳ chậm (Chậm gấp 600 lần!)"],
        ["100.000", "Closure Table", "0.260 ms", "0.290 ms", "Duy trì ~0.28ms."],
    ]
    add_styled_table(doc, ins_bm_headers, ins_bm_data, [1.0, 1.6, 1.2, 1.2, 1.8])

    add_figure(doc, "benchmark/results/charts/insert_leaf_1000.png", "Hình 6.4: Thời gian ghi thêm nút lá mới (Insert Leaf) tại quy mô 1.000 nút (ms)", width_inches=5.8)
    add_figure(doc, "benchmark/results/charts/insert_leaf_10000.png", "Hình 6.5: Thời gian ghi thêm nút lá mới (Insert Leaf) tại quy mô 10.000 nút (ms)", width_inches=5.8)
    add_figure(doc, "benchmark/results/charts/insert_leaf_100000.png", "Hình 6.6: Thời gian ghi thêm nút lá mới (Insert Leaf) tại quy mô 100.000 nút (ms)", width_inches=5.8)

    add_paragraph(doc, "Nhận xét chuyên sâu về thao tác Ghi: Đây là điểm yếu chí mạng của mô hình NESTED SET. Do cấu trúc khoảng đóng lồng nhau, khi chèn một nút lá vào giữa cây, toàn bộ các nút nằm bên phải vị trí chèn đều phải được dịch chuyển bằng câu lệnh UPDATE lft = lft + 2, rgt = rgt + 2. Ở quy mô 100.000 nút, thời gian ghi của Nested Set bùng nổ lên tới gần 44 mili-giây (chậm hơn 600 lần so với Adjacency List) và gây khóa diện rộng trên toàn bảng, triệt tiêu khả năng xử lý đồng thời. Ngược lại, Adjacency List và Path Enumeration thể hiện ưu thế vượt trội với độ phức tạp ghi O(1).")

    # --- 6.2.3 CẬP NHẬT DI CHUYỂN NHÁNH CÂY ---
    add_heading_3(doc, "6.2.3 Đánh giá tác vụ Cập nhật di chuyển nhánh cây con (Move Subtree)")
    add_paragraph(doc, "Bảng tổng hợp thời gian thực thi thao tác di chuyển một nhánh bình luận con sang một bình luận cha mới:")

    move_bm_headers = ["Quy mô nút", "Mô hình cây", "Thời gian Baseline (ms)", "Thời gian Có chỉ mục (ms)", "Độ phức tạp & Hành vi cập nhật"]
    move_bm_data = [
        ["1.000", "Adjacency List", "0.040 ms", "0.042 ms", "O(1): Chỉ UPDATE 1 dòng parent_id."],
        ["1.000", "Path Enumeration", "0.140 ms", "0.155 ms", "Đổi tiền tố chuỗi của toàn nhánh con."],
        ["1.000", "Nested Set", "1.150 ms", "1.250 ms", "Tính toán offset và cập nhật 2 khoảng."],
        ["1.000", "Closure Table", "0.420 ms", "0.460 ms", "Xóa cặp cũ và chèn lại cặp mới."],
        ["10.000", "Adjacency List", "0.048 ms", "0.050 ms", "Vẫn O(1) độc lập với số nút."],
        ["10.000", "Path Enumeration", "0.240 ms", "0.260 ms", "Cập nhật nhanh với chỉ mục GiST."],
        ["10.000", "Nested Set", "12.400 ms", "13.100 ms", "Thời gian tăng mạnh theo quy mô."],
        ["10.000", "Closure Table", "0.820 ms", "0.880 ms", "Khối lượng thao tác ghi khá lớn."],
        ["100.000", "Adjacency List", "0.058 ms", "0.062 ms", "Vẫn chỉ mất ~0.06ms!"],
        ["100.000", "Path Enumeration", "0.520 ms", "0.560 ms", "Hoàn thành trong ~0.55ms."],
        ["100.000", "Nested Set", "132.000 ms", "138.500 ms", "Cực chậm (Hơn 138 mili-giây!)"],
        ["100.000", "Closure Table", "1.350 ms", "1.450 ms", "Hoàn thành trong ~1.40ms."],
    ]
    add_styled_table(doc, move_bm_headers, move_bm_data, [1.0, 1.6, 1.4, 1.4, 1.4])

    add_figure(doc, "benchmark/results/charts/update_moveleaf_1000.png", "Hình 6.7: Thời gian cập nhật di chuyển nhánh cây con (Move Subtree) tại 1.000 nút (ms)", width_inches=5.8)
    add_figure(doc, "benchmark/results/charts/update_moveleaf_10000.png", "Hình 6.8: Thời gian cập nhật di chuyển nhánh cây con (Move Subtree) tại 10.000 nút (ms)", width_inches=5.8)
    add_figure(doc, "benchmark/results/charts/update_moveleaf_100000.png", "Hình 6.9: Thời gian cập nhật di chuyển nhánh cây con (Move Subtree) tại 100.000 nút (ms)", width_inches=5.8)

    # ========================================================
    # 6.3 THỬ TẢI ĐỒNG THỜI BẰNG PGBENCH
    # ========================================================
    add_heading_2(doc, "6.3 Thử tải đồng thời bằng công cụ pgbench")
    add_paragraph(doc, "Để kiểm chứng năng lực chịu tải và độ bền vững của hệ thống trong môi trường tương tác cao, nhóm sử dụng công cụ thử tải tiêu chuẩn pgbench tích hợp sẵn của PostgreSQL. Kịch bản thử tải thực thi giao dịch thủ tục proc_add_friend (transactions/pgbench/add_friend.sql) với việc sinh ngẫu nhiên 2 mã sinh viên độc lập, chuẩn hóa thứ tự khóa và ghi log.")
    add_paragraph(doc, "Toàn bộ quá trình thử tải được tự động hóa bằng script run_pgbench.ps1 trên 3 mức tải đồng thời: 5 Clients, 10 Clients, và 20 Clients:")

    pgbench_headers = ["Mức tải đồng thời", "Số luồng (-j)", "Tổng giao dịch", "Giao dịch thành công", "Số lỗi / Deadlock", "Độ trễ trung bình", "Thông lượng (TPS)"]
    pgbench_data = [
        ["5 Clients", "2 luồng", "500 txn", "500 (100%)", "0 lỗi (0 Deadlock)", "1.451 ms", "3,445.89 TPS"],
        ["10 Clients", "2 luồng", "1,000 txn", "1,000 (100%)", "0 lỗi (0 Deadlock)", "2.905 ms", "3,442.34 TPS"],
        ["20 Clients", "2 luồng", "2,000 txn", "2,000 (100%)", "0 lỗi (0 Deadlock)", "5.817 ms", "3,438.12 TPS"],
    ]
    add_styled_table(doc, pgbench_headers, pgbench_data, [1.1, 1.0, 1.1, 1.2, 1.2, 1.1, 1.1])

    add_paragraph(doc, "Phân tích quy luật biến thiên Thông lượng (TPS) và Độ trễ (Latency):")
    add_bullet(doc, "Thông lượng TPS duy trì cực kỳ ổn định ở mức ~3,440 giao dịch/giây trên toàn bộ các mức tải. Điều này chứng minh máy chủ cơ sở dữ liệu đã khai thác tối đa năng lực xử lý của CPU và Disk I/O mà không bị nghẽn khóa.", bold_prefix="Tính ổn định của TPS: ")
    add_bullet(doc, "Độ trễ trung bình (Latency) tăng hoàn toàn tuyến tính theo số lượng client đồng thời: 1.45ms (5 clients) → 2.90ms (10 clients, gấp đôi) → 5.81ms (20 clients, gấp đôi tiếp). Đây là minh chứng mẫu mực cho Định luật Little (Little's Law) trong lý thuyết hàng đợi (Queueing Theory): N = X × R (Số kết nối tăng gấp đôi thì thời gian phản hồi tăng gấp đôi khi hệ thống đã đạt ngưỡng thông lượng tối đa).", bold_prefix="Quy luật độ trễ: ")
    add_bullet(doc, "Tỷ lệ lỗi bằng 0 tuyệt đối (0 Transactions failed, 0 Deadlocks). Thủ tục proc_add_friend đã bảo vệ hệ thống hoàn hảo trước nguy cơ xung đột khóa dòng.", bold_prefix="Tính toàn vẹn: ")

    # ========================================================
    # 6.4 MA TRẬN KIỂM THỬ MỨC CÔ LẬP GIAO DỊCH
    # ========================================================
    add_heading_2(doc, "6.4 Ma trận Kiểm thử Mức cô lập Giao dịch")
    add_paragraph(doc, "Tiêu chuẩn ANSI SQL-92 định nghĩa 4 hiện tượng dị thường giao dịch: Dirty Read (Đọc bẩn dữ liệu chưa commit), Non-Repeatable Read (Đọc không lặp lại do phiên khác UPDATE), Phantom Read (Đọc bóng ma do phiên khác INSERT thêm dòng), và Serialization Anomaly (Dị thường ghi lệch Write Skew). Nhóm đã tiến hành kiểm nghiệm thực tế 3 mức cô lập trong PostgreSQL 18.6:")

    iso_headers = ["Mức cô lập\n(Isolation Level)", "Dirty Read\n(Đọc bẩn)", "Non-Repeatable Read\n(Đọc không lặp lại)", "Phantom Read\n(Đọc bóng ma)", "Serialization Anomaly\n(Write Skew)", "Kết quả kiểm chứng thực nghiệm"]
    iso_data = [
        ["Read Committed\n(Mặc định PostgreSQL)", "Không xảy ra\n(Được ngăn chặn)", "XẢY RA\n(Quan sát thấy)", "XẢY RA\n(Quan sát thấy)", "XẢY RA\n(Quan sát thấy)", "Phiên 1 thấy dữ liệu thay đổi ngay khi Phiên 2 thực hiện COMMIT."],
        ["Repeatable Read\n(Snapshot Isolation)", "Không xảy ra\n(Được ngăn chặn)", "Không xảy ra\n(Được ngăn chặn)", "Không xảy ra\n(Được ngăn chặn trong PG!)", "XẢY RA\n(Quan sát thấy)", "PostgreSQL dùng Snapshot Isolation nên chặn được cả Phantom Read."],
        ["Serializable\n(SSI với Predicate Locks)", "Không xảy ra\n(Được ngăn chặn)", "Không xảy ra\n(Được ngăn chặn)", "Không xảy ra\n(Được ngăn chặn)", "Không xảy ra\n(Được ngăn chặn triệt để)", "Nếu phát hiện xung đột Write Skew, phiên sau bị ABORT với mã lỗi 40001!"],
    ]
    add_styled_table(doc, iso_headers, iso_data, [1.4, 1.0, 1.1, 1.1, 1.1, 1.9])

    add_paragraph(doc, "Trích đoạn nhật ký thực nghiệm chứng minh cơ chế ngăn chặn Write Skew của mức Serializable (transactions/t3_concurrent/logs/isolation_experiments_log.txt):", bold_prefix="Dấu vết lỗi tuần tự hóa (Serialization Failure Log): ")
    add_code_block(doc, "=== [THỰC NGHIỆM SERIALIZABLE: WRITE SKEW DETECTION] ===\n"
                        "Session 1: BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;\n"
                        "Session 2: BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;\n"
                        "Session 1: SELECT SUM(points) FROM student_rewards WHERE group_id = 1; -- Kết quả: 80\n"
                        "Session 2: SELECT SUM(points) FROM student_rewards WHERE group_id = 1; -- Kết quả: 80\n"
                        "Session 1: INSERT INTO student_rewards VALUES (1, 'award_A', 15); -- Hợp lệ (Tổng = 95 <= 100)\n"
                        "Session 2: INSERT INTO student_rewards VALUES (2, 'award_B', 15); -- Hợp lệ (Tổng = 95 <= 100)\n"
                        "Session 1: COMMIT; -- Thành công!\n"
                        "Session 2: COMMIT; -- BỊ LỖI TUẦN TỰ HÓA!\n"
                        "ERROR:  could not serialize access due to read/write dependencies among transactions\n"
                        "DETAIL:  Reason code = Canceled on identification as a pivot, during commit attempt.\n"
                        "HINT:  The transaction might succeed if retried.\n"
                        "SQLSTATE: 40001 (serialization_failure)",
                   "Nhật ký lỗi tuần tự hóa SSI trong PostgreSQL (SQLSTATE 40001)")

    add_callout_box(doc, "ĐÚC KẾT VỀ MỨC CÔ LẬP GIAO DỊCH:\n"
                         "• Trong phần lớn các bài toán mạng xã hội học tập thông thường (như hiển thị bài đăng, bình luận, kết bạn), mức cô lập mặc định READ COMMITTED kết hợp các ràng buộc UNIQUE và khóa theo thứ tự định sẵn là hoàn toàn đủ để bảo đảm toàn vẹn với hiệu năng cao nhất (~3,440 TPS).\n"
                         "• Đối với các nghiệp vụ nhạy cảm đòi hỏi kiểm tra điều kiện tổng hợp ràng buộc chéo (như giới hạn tổng số học bổng, giới hạn ngân sách nhóm), hệ thống bắt buộc phải kích hoạt mức cô lập SERIALIZABLE hoặc sử dụng câu lệnh SELECT ... FOR UPDATE khóa tường minh, đi kèm cơ chế tự động thử lại (Retry Loop) phía ứng dụng khi bắt được mã lỗi SQLSTATE 40001.",
                    "HƯỚNG DẪN THỰC THI MỨC CÔ LẬP CHO CÁC PHÂN HỆ NGHIỆP VỤ")

    doc.add_page_break()
