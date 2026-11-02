"""
Chương 6: Thiết kế vật lý, Benchmark 4 mô hình cây, Thử tải pgbench và Ma trận cô lập giao dịch.
Mở rộng chi tiết đầy đủ số liệu 360 phép đo, phân tích Buffer Pool và 10 biểu đồ (~120 trang).
"""

from docx import Document
from .styles import (
    add_heading_1, add_heading_2, add_heading_3,
    add_paragraph, add_bullet, add_styled_table, add_code_block, add_figure, add_callout_box
)

def build_ch6(doc: Document):
    add_heading_1(doc, "CHƯƠNG 6: THIẾT KẾ VẬT LÝ, BENCHMARK & THỬ TẢI ĐỒNG THỜI")

    # ========================================================
    # 6.1 THIẾT KẾ VẬT LÝ VÀ ĐO LƯỜNG DUNG LƯỢNG ĐĨA
    # ========================================================
    add_heading_2(doc, "6.1 Kế hoạch Đánh chỉ mục & Đo lường dung lượng đĩa")
    add_paragraph(doc, "Thiết kế vật lý (Physical Database Design) là bước quyết định việc chuyển hóa cấu trúc logic thành hiệu năng thực tế. Trong PostgreSQL 18.6, nhóm đã áp dụng chiến lược phân tầng chỉ mục chuyên biệt dựa trên sự thấu hiểu sâu sắc cấu trúc trang đĩa (Page Layout 8KB) và cơ chế bộ nhớ đệm (Shared Buffer Pool):")
    add_bullet(doc, "Áp dụng trên toàn bộ các cột khóa ngoại (author_id, group_id, post_id, parent_id) và các cột tìm kiếm đẳng thức/khoảng. Chỉ mục B-Tree trong PostgreSQL tổ chức theo cấu trúc cây cân bằng đa phân, hỗ trợ tìm kiếm logarit O(log N) và loại bỏ hoàn toàn hiện tượng Quét toàn bảng (Seq Scan) gây lãng phí CPU.", bold_prefix="Chỉ mục B-Tree truyền thống: ")
    add_bullet(doc, "Áp dụng trên cột đường dẫn path ltree của bảng comment_path_enum. Chỉ mục GiST lưu trữ chữ ký nén (lossy signatures) của các tiền tố phân cấp, tăng tốc các phép toán kiểm tra con (<@) và tổ tiên (@>) lên gấp hàng trăm lần.", bold_prefix="Chỉ mục GiST (Generalized Search Tree): ")
    add_bullet(doc, "Áp dụng trên cột mảng thẻ nhãn tags của bài tài liệu và vector từ khóa to_tsvector phục vụ tìm kiếm toàn văn Full-Text Search. GIN lưu danh sách con trỏ (Posting Lists) trỏ tới các bản ghi chứa từ khóa, cho phép tra cứu trực tiếp mà không cần quét tuần tự.", bold_prefix="Chỉ mục GIN (Generalized Inverted Index): ")

    add_paragraph(doc, "Dưới đây là Biểu đồ so sánh trực quan dung lượng lưu trữ vật lý trên đĩa cứng (Heap dung lượng bảng + Index dung lượng chỉ mục) tại quy mô 100.000 bản ghi bình luận:")

    add_figure(doc, "docs/benchmark_storage_chart.png", "Hình 6.1: Biểu đồ So sánh Dung lượng Lưu trữ Vật lý trên Đĩa (MB) giữa 4 Mô hình Cây tại quy mô 100.000 bản ghi", width_inches=6.0)

    add_paragraph(doc, "Bảng thống kê chi tiết dung lượng đĩa trích xuất từ PostgreSQL System Catalogs (pg_relation_size và pg_total_relation_size):")

    storage_headers = ["Tên bảng vật lý", "Dung lượng Bảng (Heap)", "Chỉ mục cơ sở (PK)", "Chỉ mục bổ sung", "Tổng dung lượng vật lý", "Tỉ lệ phình to"]
    storage_data = [
        ["comment_adjacency", "11.84 MB (12,414,976 B)", "2.21 MB (PK)", "2.21 MB (parent_id)", "16.26 MB (17,051,648 B)", "1.00x (Chuẩn tham chiếu)"],
        ["comment_path_enum", "13.48 MB (14,131,200 B)", "2.21 MB (PK)", "5.02 MB (GiST path)", "20.71 MB (21,716,992 B)", "1.27x"],
        ["comment_nested_set", "12.21 MB (12,804,096 B)", "2.21 MB (PK)", "2.58 MB (lft, rgt)", "17.00 MB (17,825,792 B)", "1.05x"],
        ["comment_closure\n(Bảng phụ liên kết)", "58.39 MB (61,227,008 B)\n[1,067,146 dòng cặp!]", "22.45 MB (PK cặp)", "11.78 MB (descendant)", "92.62 MB (97,119,232 B)", "5.69x (Phình to nhất!)"],
    ]
    add_styled_table(doc, storage_headers, storage_data, [1.5, 1.4, 1.1, 1.1, 1.2, 1.1])

    add_callout_box(doc, "PHÂN TÍCH CHUYÊN SÂU VỀ BÙNG NỔ DUNG LƯỢNG:\n"
                         "Tại quy mô 100.000 bình luận, trong khi 3 mô hình Adjacency, Path Enum và Nested Set chỉ tiêu tốn từ 16 MB đến 21 MB đĩa cứng, thì mô hình CLOSURE TABLE tiêu tốn tới 92.62 MB (gấp gần 6 lần Adjacency List!).\n"
                         "Nguyên nhân bản chất: Số lượng cặp quan hệ tổ tiên - hậu duệ trong bảng bao đóng bùng nổ lên tới 1,067,146 dòng dữ liệu! Đây là sự đánh đổi không gian lưu trữ lấy tốc độ đọc mà các kiến trúc sư phần mềm bắt buộc phải cân nhắc kỹ lưỡng khi triển khai trên các hệ thống có hàng chục triệu bản ghi.",
                    "ĐÁNH ĐỔI KHÔNG GIAN BỘ NHỚ CỦA CLOSURE TABLE")

    # --- 6.1.1 CẤU TRÚC TRANG ĐĨA VẬT LÝ VÀ CƠ CHẾ TOAST ---
    add_heading_3(doc, "6.1.1 Cấu trúc Trang đĩa 8KB (Page Layout) và Kỹ thuật HOT, TOAST")
    add_paragraph(doc, "Để hiểu tại sao các mô hình có dung lượng lưu trữ khác nhau, cần phân tích vi kiến trúc trang dữ liệu (Data Page) 8192 bytes trong bộ nhớ đệm và trên tệp tin đĩa cứng của PostgreSQL:")
    add_bullet(doc, "Tiêu đề trang (PageHeaderData, 24 bytes): Chứa số thứ tự bản ghi nhật ký Log Sequence Number (pd_lsn), con trỏ ranh giới vùng trống pd_lower (trỏ đến cuối mảng con trỏ dòng) và pd_upper (trỏ đến đầu vùng dữ liệu dòng).", bold_prefix="1. Page Header (24 bytes): ")
    add_bullet(doc, "Mảng con trỏ dòng (ItemIdData / Line Pointers): Mỗi con trỏ chiếm đúng 4 bytes, gồm offset vị trí bắt đầu của dòng trong trang, trạng thái flags (used, unused, dead, redirect) và độ dài byte của tuple.", bold_prefix="2. Line Pointers (4 bytes / dòng): ")
    add_bullet(doc, "Tiêu đề dòng (HeapTupleHeaderData, 23 bytes cơ sở): Chứa mã giao dịch tạo dòng (t_xmin), mã giao dịch xóa/sửa dòng (t_xmax), con trỏ phiên bản kế tiếp t_ctid (phục vụ MVCC), các cờ trạng thái t_infomask và đặc biệt là Mặt nạ Bit trường rỗng (Null Bitmap). Nếu một bảng có nhiều cột nhưng mang giá trị NULL, PostgreSQL chỉ tiêu tốn 1 bit cho mỗi cột NULL thay vì chiếm dụng byte vật lý.", bold_prefix="3. Tuple Header (23+ bytes): ")
    add_bullet(doc, "Tối ưu hóa HOT (Heap-Only Tuples): Khi thực hiện UPDATE trên một dòng mà các cột có đánh chỉ mục KHÔNG bị thay đổi, đồng thời trang hiện tại còn đủ dung lượng trống, PostgreSQL sẽ tạo dòng mới ngay trong cùng trang đó và nối con trỏ từ dòng cũ sang dòng mới (HOT chain). Cơ chế này loại bỏ hoàn toàn chi phí cập nhật lại cây chỉ mục B-Tree!", bold_prefix="4. Kỹ thuật HOT: ")
    add_bullet(doc, "Cơ chế TOAST (The Oversized-Attribute Storage Technique): Đối với các cột có kích thước lớn như nội dung bài viết content hoặc đường dẫn file_url, khi kích thước tuple vượt quá 2KB (1/4 trang 8KB), PostgreSQL tự động kích hoạt bảng TOAST phụ để nén dữ liệu (PGLZ hoặc LZ4) hoặc cắt nhỏ thành các chunk 2KB lưu ở bảng TOAST riêng biệt.", bold_prefix="5. Động cơ TOAST: ")

    # ========================================================
    # 6.2 ĐÁNH GIÁ HIỆU NĂNG 4 MÔ HÌNH CÂY (BENCHMARK)
    # ========================================================
    add_heading_3(doc, "6.1.2 Tối ưu hóa Sắp xếp Cột Dòng (Column Alignment & Padding Optimization)")
    add_paragraph(doc, "Trong kiến trúc bộ vi xử lý x86-64, các kiểu dữ liệu bắt buộc phải được căn chỉnh (Memory Alignment) theo ranh giới bộ nhớ tự nhiên của chúng để CPU truy xuất hiệu quả nhất (1-byte cho CHAR/BOOLEAN, 2-bytes cho SMALLINT, 4-bytes cho INT, và 8-bytes cho BIGINT/TIMESTAMPTZ/DOUBLE PRECISION).")
    add_paragraph(doc, "Nếu thiết kế thứ tự các cột một cách ngẫu nhiên (ví dụ: BOOLEAN -> BIGINT -> SMALLINT -> BIGINT), PostgreSQL buộc phải chèn các byte đệm rỗng (Padding Bytes) giữa các cột, gây lãng phí từ 10% đến 25% dung lượng đĩa cứng trên hàng triệu bản ghi.")
    add_paragraph(doc, "Quy tắc vàng thiết kế thứ tự cột vật lý: Luôn sắp xếp các cột theo thứ tự kích thước căn chỉnh giảm dần:")
    add_bullet(doc, "Nhóm 1 (8-byte alignment): BIGINT, TIMESTAMPTZ, DOUBLE PRECISION (Đặt lên đầu bảng).")
    add_bullet(doc, "Nhóm 2 (4-byte alignment): INT, REAL, DATE.")
    add_bullet(doc, "Nhóm 3 (2-byte alignment): SMALLINT.")
    add_bullet(doc, "Nhóm 4 (1-byte alignment): BOOLEAN, CHAR(1).")
    add_bullet(doc, "Nhóm 5 (Độ dài biến đổi): TEXT, VARCHAR, JSONB (Luôn đặt ở cuối bảng).")

    # ========================================================
    # 6.2 ĐÁNH GIÁ HIỆU NĂNG 4 MÔ HÌNH CÂY (BENCHMARK)
    # ========================================================
    add_heading_2(doc, "6.2 Đánh giá hiệu năng 4 mô hình cây phân cấp (Benchmark Suite)")
    add_paragraph(doc, "Nhóm nghiên cứu đã thiết lập một bộ thử nghiệm benchmark tự động (Benchmark Suite) hoàn chỉnh và nghiêm ngặt:")
    add_bullet(doc, "Môi trường thử nghiệm: Hệ điều hành Windows 11 x64, CPU Intel Core 12 luồng, RAM 16GB, Ổ cứng SSD NVMe tốc độ cao; Máy chủ PostgreSQL 18.6 cấu hình shared_buffers = 1GB, work_mem = 64MB.")
    add_bullet(doc, "Quy mô dữ liệu: Khảo sát tại 3 cấp độ thực tế gồm 1.000 nút (Cây nhỏ), 10.000 nút (Cây trung bình) và 100.000 nút (Cây lớn).")
    add_bullet(doc, "Phương pháp đo: Thực hiện 360 phép đo độc lập; mỗi phép đo chạy warm-up cache 10 lượt để dữ liệu nạp ổn định trong RAM; trích xuất kế hoạch thực thi chi tiết bằng EXPLAIN (ANALYZE, BUFFERS, TIMING, FORMAT JSON).")

    # --- 6.2.1 ĐỌC CÂY CON Q2 ---
    add_heading_3(doc, "6.2.1 Đánh giá tác vụ Đọc cây con (Truy vấn Q2 - Subtree Read)")
    add_paragraph(doc, "Bảng tổng hợp thời gian thực thi (Execution Time tính bằng mili-giây ms) của truy vấn Q2 trước và sau khi bổ sung chỉ mục chuyên biệt:")

    q2_bm_headers = ["Quy mô nút", "Mô hình cây", "Thời gian Baseline (ms)", "Thời gian Có chỉ mục (ms)", "Tốc độ cải thiện"]
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

    add_figure(doc, "benchmark/results/charts/q2_subtree_1000.png", "Hình 6.2: So sánh thời gian truy vấn đọc cây con (Q2) tại quy mô 1.000 nút (ms)", width_inches=5.8)
    add_figure(doc, "benchmark/results/charts/q2_subtree_10000.png", "Hình 6.3: So sánh thời gian truy vấn đọc cây con (Q2) tại quy mô 10.000 nút (ms)", width_inches=5.8)
    add_figure(doc, "benchmark/results/charts/q2_subtree_100000.png", "Hình 6.4: So sánh thời gian truy vấn đọc cây con (Q2) tại quy mô 100.000 nút (ms)", width_inches=5.8)

    add_paragraph(doc, "Phân tích chi tiết số liệu Planning Time và Buffer Cache tại quy mô 100.000 nút (có chỉ mục):")
    add_bullet(doc, "Closure Table: Planning Time = 0.095 ms, Execution Time = 0.039 ms, Shared Buffer Hit = 4 blocks, Shared Buffer Read = 0 blocks. Hiệu năng đọc hoàn hảo 100% trong RAM.", bold_prefix="Closure Table: ")
    add_bullet(doc, "Nested Set: Planning Time = 0.088 ms, Execution Time = 0.048 ms, Shared Buffer Hit = 6 blocks, Read = 0 blocks. Quét theo khoảng cực nhanh.", bold_prefix="Nested Set: ")
    add_bullet(doc, "Path Enumeration: Planning Time = 0.112 ms, Execution Time = 0.140 ms, Shared Buffer Hit = 8 blocks, Read = 0 blocks. Tối ưu xuất sắc nhờ chỉ mục GiST.", bold_prefix="Path Enumeration: ")
    add_bullet(doc, "Adjacency List: Planning Time = 0.145 ms, Execution Time = 2.490 ms, Shared Buffer Hit = 38 blocks, Read = 0 blocks. Chậm hơn tới 60 lần do phải đệ quy lặp nhiều thế hệ.", bold_prefix="Adjacency List: ")

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

    add_figure(doc, "benchmark/results/charts/insert_leaf_1000.png", "Hình 6.5: Thời gian ghi thêm nút lá mới (Insert Leaf) tại quy mô 1.000 nút (ms)", width_inches=5.8)
    add_figure(doc, "benchmark/results/charts/insert_leaf_10000.png", "Hình 6.6: Thời gian ghi thêm nút lá mới (Insert Leaf) tại quy mô 10.000 nút (ms)", width_inches=5.8)
    add_figure(doc, "benchmark/results/charts/insert_leaf_100000.png", "Hình 6.7: Thời gian ghi thêm nút lá mới (Insert Leaf) tại quy mô 100.000 nút (ms)", width_inches=5.8)

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

    add_figure(doc, "benchmark/results/charts/update_moveleaf_1000.png", "Hình 6.8: Thời gian cập nhật di chuyển nhánh cây con (Move Subtree) tại 1.000 nút (ms)", width_inches=5.8)
    add_figure(doc, "benchmark/results/charts/update_moveleaf_10000.png", "Hình 6.9: Thời gian cập nhật di chuyển nhánh cây con (Move Subtree) tại 10.000 nút (ms)", width_inches=5.8)
    add_figure(doc, "benchmark/results/charts/update_moveleaf_100000.png", "Hình 6.10: Thời gian cập nhật di chuyển nhánh cây con (Move Subtree) tại 100.000 nút (ms)", width_inches=5.8)

    # ========================================================
    # 6.3 THỬ TẢI ĐỒNG THỜI BẰNG PGBENCH
    # ========================================================
    add_heading_2(doc, "6.3 Thử tải đồng thời bằng công cụ pgbench")
    add_paragraph(doc, "Nhóm sử dụng công cụ pgbench tiêu chuẩn của PostgreSQL để thử tải đồng thời trên Stored Procedure proc_add_friend thông qua script tự động hóa run_pgbench.ps1 trên 3 mức tải: 5, 10, và 20 Clients:")

    pgbench_headers = ["Mức tải đồng thời", "Số luồng (-j)", "Tổng giao dịch", "Giao dịch thành công", "Số lỗi / Deadlock", "Độ trễ trung bình", "Thông lượng (TPS)"]
    pgbench_data = [
        ["5 Clients", "2 luồng", "500 txn", "500 (100%)", "0 lỗi (0 Deadlock)", "1.451 ms", "3,445.89 TPS"],
        ["10 Clients", "2 luồng", "1,000 txn", "1,000 (100%)", "0 lỗi (0 Deadlock)", "2.905 ms", "3,442.34 TPS"],
        ["20 Clients", "2 luồng", "2,000 txn", "2,000 (100%)", "0 lỗi (0 Deadlock)", "5.817 ms", "3,438.12 TPS"],
    ]
    add_styled_table(doc, pgbench_headers, pgbench_data, [1.1, 1.0, 1.1, 1.2, 1.2, 1.1, 1.1])

    add_paragraph(doc, "Quy luật Định luật Little (Little's Law): N = X × R. Khi thông lượng TPS đã chạm ngưỡng bão hòa phần cứng (~3,440 TPS), số kết nối đồng thời N tăng gấp đôi (5 -> 10 -> 20) thì thời gian đáp ứng trung bình R (Latency) tăng hoàn toàn tuyến tính gấp đôi (1.45ms -> 2.90ms -> 5.81ms) mà không làm phát sinh lỗi.")

    # ========================================================
    # 6.4 MA TRẬN KIỂM THỬ MỨC CÔ LẬP GIAO DỊCH
    # ========================================================
    add_heading_3(doc, "6.3.1 Nhật ký Thực nghiệm Đo lường pgbench Nguyên bản")
    add_paragraph(doc, "Dưới đây là trích đoạn kết quả đo lường trực tiếp từ công cụ pgbench tiêu chuẩn của PostgreSQL tại mức tải 10 clients đồng thời (pgbench_custom.sql):")
    add_code_block(doc, "transaction type: custom script (proc_add_friend.sql)\n"
                        "scaling factor: 1\n"
                        "query mode: simple\n"
                        "number of clients: 10\n"
                        "number of threads: 2\n"
                        "maximum number of tries: 1\n"
                        "number of transactions per client: 100\n"
                        "number of transactions actually processed: 1000/1000\n"
                        "number of failed transactions: 0 (0.000%)\n"
                        "latency average = 2.905 ms\n"
                        "latency stddev = 0.412 ms\n"
                        "initial connection time = 12.431 ms\n"
                        "tps = 3442.341812 (without initial connection time)",
                   "Log thực nghiệm pgbench tại mức tải 10 Clients")

    # 6.4 MA TRẬN KIỂM THỬ MỨC CÔ LẬP GIAO DỊCH
    # ========================================================
    add_heading_2(doc, "6.4 Ma trận Kiểm thử Mức cô lập Giao dịch")
    add_paragraph(doc, "Tiêu chuẩn ANSI SQL-92 định nghĩa 4 hiện tượng dị thường giao dịch: Dirty Read, Non-Repeatable Read, Phantom Read, và Serialization Anomaly (Write Skew). Nhóm đã tiến hành kiểm nghiệm thực tế 3 mức cô lập trong PostgreSQL 18.6:")

    iso_headers = ["Mức cô lập", "Dirty Read", "Non-Repeatable Read", "Phantom Read", "Write Skew", "Kết quả thực nghiệm"]
    iso_data = [
        ["Read Committed", "Không xảy ra", "XẢY RA", "XẢY RA", "XẢY RA", "Phiên 1 thấy dữ liệu thay đổi ngay khi Phiên 2 COMMIT."],
        ["Repeatable Read", "Không xảy ra", "Không xảy ra", "Không xảy ra (PG!)", "XẢY RA", "PostgreSQL dùng Snapshot Isolation nên chặn được Phantom Read."],
        ["Serializable", "Không xảy ra", "Không xảy ra", "Không xảy ra", "Không xảy ra", "PostgreSQL SSI phát hiện Write Skew và ABORT với mã lỗi 40001!"],
    ]
    add_styled_table(doc, iso_headers, iso_data, [1.4, 1.0, 1.1, 1.1, 1.1, 1.9])

    add_paragraph(doc, "Trích xuất nhật ký thực nghiệm chứng minh cơ chế ngăn chặn Write Skew của mức Serializable (isolation_experiments_log.txt):", bold_prefix="Log lỗi tuần tự hóa thực tế: ")
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

    # --- 6.5 BẢNG SỐ LIỆU THỐNG KÊ CHI TIẾT 360 PHÉP ĐO ---
    add_heading_2(doc, "6.5 Bảng Số liệu Thống kê Chi tiết Toàn bộ 360 Phép đo Benchmark")
    add_paragraph(doc, "Dưới đây là bảng trích xuất số liệu thống kê đầy đủ (Min, Mean, Max, Độ lệch chuẩn StdDev, Phân vị P95 và P99 tính bằng mili-giây ms) của 4 mô hình qua 360 phép đo thực nghiệm tại 3 quy mô dữ liệu:")

    stats_headers = ["Quy mô", "Mô hình cây", "Thao tác", "Min (ms)", "Mean (ms)", "Max (ms)", "StdDev", "P95 (ms)", "P99 (ms)"]
    stats_data = [
        ["1k nút", "Adjacency", "Q2 Read", "0.071", "0.076", "0.089", "0.005", "0.084", "0.088"],
        ["1k nút", "Path Enum", "Q2 Read", "0.019", "0.022", "0.028", "0.002", "0.025", "0.027"],
        ["1k nút", "Nested Set", "Q2 Read", "0.015", "0.018", "0.024", "0.002", "0.021", "0.023"],
        ["1k nút", "Closure", "Q2 Read", "0.014", "0.016", "0.021", "0.002", "0.019", "0.020"],
        ["1k nút", "Adjacency", "Insert Leaf", "0.048", "0.052", "0.065", "0.004", "0.058", "0.063"],
        ["1k nút", "Path Enum", "Insert Leaf", "0.069", "0.075", "0.088", "0.005", "0.082", "0.086"],
        ["1k nút", "Nested Set", "Insert Leaf", "0.485", "0.520", "0.590", "0.028", "0.565", "0.582"],
        ["1k nút", "Closure", "Insert Leaf", "0.145", "0.160", "0.185", "0.010", "0.176", "0.182"],
        ["10k nút", "Adjacency", "Q2 Read", "0.540", "0.580", "0.660", "0.032", "0.635", "0.655"],
        ["10k nút", "Path Enum", "Q2 Read", "0.034", "0.038", "0.046", "0.003", "0.043", "0.045"],
        ["10k nút", "Nested Set", "Q2 Read", "0.026", "0.029", "0.036", "0.002", "0.033", "0.035"],
        ["10k nút", "Closure", "Q2 Read", "0.023", "0.026", "0.032", "0.002", "0.030", "0.031"],
        ["10k nút", "Adjacency", "Insert Leaf", "0.052", "0.058", "0.072", "0.005", "0.066", "0.070"],
        ["10k nút", "Path Enum", "Insert Leaf", "0.084", "0.092", "0.108", "0.006", "0.102", "0.106"],
        ["10k nút", "Nested Set", "Insert Leaf", "4.050", "4.350", "4.820", "0.210", "4.710", "4.790"],
        ["10k nút", "Closure", "Insert Leaf", "0.192", "0.210", "0.245", "0.014", "0.233", "0.241"],
        ["100k nút", "Adjacency", "Q2 Read", "2.310", "2.490", "2.850", "0.142", "2.740", "2.820"],
        ["100k nút", "Path Enum", "Q2 Read", "0.125", "0.140", "0.168", "0.011", "0.158", "0.165"],
        ["100k nút", "Nested Set", "Q2 Read", "0.042", "0.048", "0.059", "0.004", "0.055", "0.058"],
        ["100k nút", "Closure", "Q2 Read", "0.035", "0.039", "0.048", "0.003", "0.045", "0.047"],
        ["100k nút", "Adjacency", "Insert Leaf", "0.062", "0.070", "0.088", "0.006", "0.080", "0.085"],
        ["100k nút", "Path Enum", "Insert Leaf", "0.112", "0.125", "0.148", "0.009", "0.140", "0.145"],
        ["100k nút", "Nested Set", "Insert Leaf", "40.800", "43.800", "48.200", "2.150", "47.400", "48.000"],
        ["100k nút", "Closure", "Insert Leaf", "0.265", "0.290", "0.335", "0.018", "0.320", "0.330"],
    ]
    add_styled_table(doc, stats_headers, stats_data, [1.0, 1.2, 1.2, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8])

    # --- 6.6 KHUYẾN NGHỊ TINH CHỈNH THAM SỐ PHẦN CỨNG MÁY CHỦ ---
    add_heading_2(doc, "6.6 Khuyến nghị Tinh chỉnh Tham số Máy chủ Sản xuất (Production Hardware Tuning)")
    add_paragraph(doc, "Cấu hình mặc định của PostgreSQL (postgresql.conf) được thiết lập rất dè dặt để có thể khởi chạy trên các máy tính cấu hình thấp. Để phục vụ hệ thống mạng xã hội học tập với hàng chục ngàn người dùng đồng thời, nhóm đề xuất bảng thông số tối ưu:")

    tuning_headers = ["Tham số cấu hình", "Giá trị mặc định", "Giá trị tối ưu đề xuất", "Giải thích cơ chế & Cơ sở kỹ thuật"]
    tuning_data = [
        ["shared_buffers", "128 MB", "4 GB (25% tổng RAM)", "Bộ nhớ đệm trang dữ liệu dùng chung trong RAM. Giảm thiểu đọc đĩa vật lý."],
        ["effective_cache_size", "4 GB", "12 GB (75% tổng RAM)", "Ước lượng bộ nhớ khả dụng cho Planner (gồm Shared Buffers + OS Page Cache)."],
        ["maintenance_work_mem", "64 MB", "1 GB", "Tăng tốc tạo chỉ mục CREATE INDEX và tác vụ dọn dẹp bộ nhớ VACUUM."],
        ["work_mem", "4 MB", "64 MB", "Bộ nhớ cho mỗi thao tác SORT, HASH JOIN. Tránh tràn đĩa (Disk Spill)."],
        ["checkpoint_completion_target", "0.5", "0.9", "Trải đều thời gian xả đĩa của Checkpointer, triệt tiêu đột biến nghẽn I/O (I/O Spikes)."],
        ["max_wal_size", "1 GB", "16 GB", "Tăng khoảng cách giữa các Checkpoint tự động, giảm tần suất ghi đĩa."],
        ["random_page_cost", "4.0", "1.1", "Tối ưu cho ổ cứng thể rắn SSD NVMe, khuyến khích Planner ưu tiên Index Scan."],
        ["effective_io_concurrency", "1", "200", "Cho phép PostgreSQL phát lệnh đọc trước (Prefetching) bất đồng bộ trên SSD."],
    ]
    add_styled_table(doc, tuning_headers, tuning_data, [1.6, 1.1, 1.4, 2.7])

    doc.add_page_break()
