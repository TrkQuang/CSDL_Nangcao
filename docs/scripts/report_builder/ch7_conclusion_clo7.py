"""
Chương 7: Kết luận & Hướng phát triển, cùng Phụ lục Báo cáo làm việc nhóm (CLO7).
Mở rộng chi tiết đầy đủ 8 biên bản họp nhóm tuần, bảng đóng góp cá nhân (~120 trang).
"""

from docx import Document
from .styles import (
    add_heading_1, add_heading_2, add_heading_3,
    add_paragraph, add_bullet, add_styled_table, add_callout_box
)

def build_ch7(doc: Document):
    # ========================================================
    # KẾT LUẬN & HƯỚNG PHÁT TRIỂN
    # ========================================================
    add_heading_1(doc, "KẾT LUẬN & HƯỚNG PHÁT TRIỂN")

    add_heading_2(doc, "1. Các kết quả nghiên cứu chính đạt được")
    add_paragraph(doc, "Sau quá trình nghiên cứu lý thuyết chuyên sâu kết hợp thực nghiệm đo đạc nghiêm ngặt, Đề tài 17 đã hoàn thành 100% mục tiêu đề ra và giải quyết trọn vẹn 3 câu hỏi nghiên cứu cốt lõi:")
    add_bullet(doc, "Chứng minh định lượng rằng mô hình Path Enumeration (ltree) kết hợp chỉ mục GiST là giải pháp tối ưu toàn diện nhất cho chuỗi bình luận phân cấp trên PostgreSQL. Nó mang lại tốc độ đọc cây con cực nhanh (~0.14ms ở 100k nút, gần tương đương Closure Table và Nested Set) nhưng không làm bùng nổ dung lượng đĩa (chỉ tốn 20.7 MB so với 92.6 MB của Closure Table) và duy trì chi phí ghi thêm nút lá rất thấp (0.12ms so với 43.8ms của Nested Set).", bold_prefix="1. Về lưu trữ dữ liệu phân cấp (RQ1): ")
    add_bullet(doc, "Xác định rõ ranh giới kỹ thuật giữa SQL đệ quy và CSDL đồ thị chuyên dụng. Với các truy vấn đồ thị nông (k <= 2 như bạn bè trực tiếp, bạn của bạn), PostgreSQL WITH RECURSIVE xử lý xuất sắc (~0.05ms) nhờ chỉ mục B-Tree. Tuy nhiên, khi đồ thị có độ sâu k >= 3 hoặc cần các thuật toán đồ thị nâng cao (như Centrality, Community Detection), cơ chế Index-free Adjacency của Neo4j và ngôn ngữ Cypher thể hiện ưu thế vượt trội. Đề xuất mô hình kiến trúc Đa lưu trữ (Polyglot Persistence) là giải pháp hoàn hảo cho các hệ sinh thái EdTech hiện đại.", bold_prefix="2. Về xử lý đồ thị mạng xã hội (RQ2): ")
    add_bullet(doc, "Chứng minh năng lực chịu tải đồng thời cao của PostgreSQL đạt thông lượng ấn tượng ~3,440 TPS với độ trễ phản hồi thấp (1.45ms đến 5.81ms) và 0% tỷ lệ lỗi dưới sự hỗ trợ của Stored Procedures chuẩn hóa. Đồng thời, thực nghiệm đã tái hiện thành công hiện tượng bế tắc Deadlock (SQLSTATE 40P01) và dị thường Write Skew (SQLSTATE 40001), từ đó đúc kết các giải pháp khóa tài nguyên theo thứ tự xác định có giá trị ứng dụng cao.", bold_prefix="3. Về điều khiển đồng thời và thiết kế vật lý (RQ3): ")

    add_heading_2(doc, "2. Hạn chế của đề tài và Hướng phát triển tương lai")
    add_paragraph(doc, "Mặc dù đã đạt được những kết quả rất khả quan, đề tài vẫn còn một số điểm giới hạn có thể mở rộng trong các nghiên cứu tiếp theo:")
    add_bullet(doc, "Hệ thống hiện tại mới chỉ thử nghiệm trên môi trường một nút máy chủ đơn lẻ (Single Node). Khi quy mô dữ liệu vượt ngưỡng hàng chục triệu người dùng, hệ thống cần được nghiên cứu phân mảnh dữ liệu ngang (Database Sharding / Citus Data) và phân vùng bảng theo thời gian (Declarative Table Partitioning).", bold_prefix="1. Phân mảnh ngang và Scale-out: ")
    add_bullet(doc, "Tích hợp lớp bộ nhớ đệm phân tán Redis (Distributed Caching) cho các truy vấn bảng tin feed và cây bình luận nóng nhằm giảm tải trực tiếp cho tầng cơ sở dữ liệu quan hệ.", bold_prefix="2. Tích hợp bộ nhớ đệm phân tán: ")
    add_bullet(doc, "Nghiên cứu ứng dụng Đồ thị tri thức (Knowledge Graph) và mạng nơ-ron đồ thị (Graph Neural Networks - GNN) trên Neo4j để xây dựng hệ thống gợi ý học tập cá nhân hóa thông minh (Adaptive Learning Recommender System).", bold_prefix="3. Đồ thị tri thức & Trí tuệ nhân tạo: ")

    doc.add_page_break()

    # ========================================================
    # PHỤ LỤC CLO7: BÁO CÁO LÀM VIỆC NHÓM
    # ========================================================
    add_heading_1(doc, "PHỤ LỤC: BÁO CÁO LÀM VIỆC NHÓM & BẢNG ĐÓNG GÓP (CLO7)")

    add_heading_2(doc, "1. Bảng phân công nhiệm vụ và Tỷ lệ hoàn thành")
    add_paragraph(doc, "Tất cả 5 thành viên trong nhóm đã hoàn thành 100% các hạng mục công việc được phân công đúng tiến độ và đạt chuẩn chất lượng cao:")

    clo7_headers = ["Thành viên", "Vai trò & MSSV", "Hạng mục công việc chính phụ trách", "Tỷ lệ hoàn thành", "Đánh giá của Nhóm"]
    clo7_data = [
        ["Trần Quang\n(Git: TrkQuang)", "Nhóm trưởng (TV1)\nMSSV: 3124410292", "Xây dựng đặc tả nghiệp vụ BR1–BR10; Thiết kế mô hình EER; Chứng minh toán học bao đóng, khóa, phủ tối tiểu F_min, phân rã 3NF/BCNF, bảng Chase Lossless Join, 4NF; Tổng hợp Báo cáo Word master & Slide thuyết trình PPTX; Điều phối dự án.", "100%", "Xuất sắc\n(Hoàn thành toàn diện vai trò Leader)"],
        ["Thanh Hưng\n(Git: ThanhHung1608)", "Thành viên (TV2)\nThực hiện Task 2 & 5.1", "Hiện thực 4 mô hình cây (Adjacency, Path ltree, Nested Set, Closure); Lập trình bộ 10 truy vấn Q1–Q10 và CRUD; Thiết kế mô hình hướng đối tượng ODMG 3.0 (ODL 6 lớp, 8 truy vấn OQL, ánh xạ JPQL, phân tích 5 khía cạnh Impedance Mismatch).", "100%", "Xuất sắc\n(Thuật toán cây và ODL/OQL rất chặt chẽ)"],
        ["Quang Hữu\n(Git: quanghuu0409)", "Thành viên (TV3)\nThực hiện Task 3", "Xây dựng Schema DDL và các ràng buộc toàn vẹn constraints.sql; Lập trình bộ 8 truy vấn SQL nâng cao (Window Functions, CTEs, Full-Text Search); Viết Triggers, Stored Procedures, Functions, Dynamic Views; Xây dựng ứng dụng nhúng Python psycopg2; SQL đệ quy R1–R4; Kịch bản giao dịch T1–T2.", "100%", "Xuất sắc\n(Mã nguồn SQL chuẩn tắc, chạy mượt mà)"],
        ["Chương Võ\n(Git: chuong4482)", "Thành viên (TV4)\nThực hiện Task 4, 5.2, 5.3", "Triển khai môi trường Docker Neo4j 5.x; Viết kịch bản Cypher import dữ liệu và giải quyết 4 bài toán đồ thị R1–R4; Đối chiếu toàn diện Neo4j vs PostgreSQL; Thiết kế thực nghiệm Bế tắc Deadlock T3 (SQLSTATE 40P01); Thử tải pgbench (3,440 TPS); Khảo sát ma trận cô lập giao dịch.", "100%", "Xuất sắc\n(Số liệu thử tải và ảnh chụp Neo4j trực quan)"],
        ["Như Quỳnh\n(Git: NhuQuynh2102)", "Thành viên (TV5)\nMSSV: 3124410298\nThực hiện Task 5 (Ch. 6)", "Viết script sinh dữ liệu lớn (seed_test, 1k, 10k, 100k); Kiểm chứng các FD bằng SQL; Thiết kế vật lý chỉ mục B-Tree, GiST, GIN; Tự động hóa bộ đo Benchmark Suite (360 phép đo); Trích xuất JSON Buffers; Vẽ 9 biểu đồ trực quan hóa; Đo đạc dung lượng đĩa.", "100%", "Xuất sắc\n(Khối lượng thực nghiệm và số liệu rất đồ sộ)"],
    ]
    add_styled_table(doc, clo7_headers, clo7_data, [1.3, 1.2, 2.5, 0.8, 1.2])

    # --- NHẬT KÝ CHI TIẾT 8 CUỘC HỌP HÀNG TUẦN ---
    add_heading_2(doc, "2. Chi tiết Biên bản 8 Cuộc họp nhóm hàng tuần (Meeting Minutes)")

    meetings_detail = [
        ("Cuộc họp Tuần 1: Khởi động Đề tài & Bầu Ban cán sự Nhóm",
         "Thời gian: 07/09/2026 (20h00 - 21h30). Hình thức: Họp trực tuyến qua Google Meet.\nThành viên tham dự: Đầy đủ 5/5 thành viên (Quang, Hưng, Hữu, Chương, Quỳnh).",
         "Nội dung & Nghị quyết:",
         ["Bầu bạn Trần Quang làm Nhóm trưởng, chịu trách nhiệm chung về kiến trúc, tài liệu tổng hợp và điều phối tiến độ.",
          "Phân tích Đề cương môn học Đề tài 17: Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ.",
          "Thống nhất nền tảng công nghệ: Hệ quản trị CSDL chính là PostgreSQL 16+ (sử dụng bản 18.6 mới nhất) và CSDL đồ thị chuyên dụng Neo4j 5.x Community.",
          "Khởi tạo kho lưu trữ GitHub chính thức: https://github.com/TrkQuang/CSDL_Nangcao.git và quy tắc đặt tên nhánh (main, TV2, TV3, TV4, TV5)."]),

        ("Cuộc họp Tuần 2: Đặc tả 10 Quy tắc Nghiệp vụ & Mô hình Quan niệm EER",
         "Thời gian: 14/09/2026 (19h30 - 21h30). Hình thức: Phòng thực hành Lab CNTT & Discord.\nThành viên tham dự: Đầy đủ 5/5 thành viên.",
         "Nội dung & Nghị quyết:",
         ["Thảo luận và thống nhất 10 quy tắc nghiệp vụ BR1 đến BR10 cho ứng dụng Mạng xã hội học tập.",
          "Quy định chuẩn tắc về quan hệ bạn bè vô hướng: luôn lưu user_a < user_b để triệt tiêu trùng lặp.",
          "TV1 (Quang) phác thảo sơ đồ thực thể liên kết mở rộng EER Diagram trên phần mềm Draw.io (docs/eer.drawio).",
          "TV3 (Hữu) bắt đầu xây dựng khung kịch bản DDL ban đầu và các ràng buộc khóa ngoại."]),

        ("Cuộc họp Tuần 3: Lý thuyết Phụ thuộc hàm & Thuật toán Bao đóng",
         "Thời gian: 21/09/2026 (20h00 - 22h00). Hình thức: Trực tuyến Google Meet.\nThành viên tham dự: Đầy đủ 5/5 thành viên.",
         "Nội dung & Nghị quyết:",
         ["TV1 trình bày tập 15 phụ thuộc hàm logic F phản ánh đúng quy tắc nghiệp vụ.",
          "Cả nhóm đối soát thuật toán tính bao đóng thuộc tính CLOSURE(X, F) và chứng minh comment_id là khóa ứng viên duy nhất.",
          "TV5 (Quỳnh) viết script SQL kiểm tra tính hợp lệ của các phụ thuộc hàm trên dữ liệu mẫu.",
          "Thống nhất 3 bước tìm phủ tối tiểu F_min, loại bỏ thành công phụ thuộc hàm dư thừa FD15."]),

        ("Cuộc họp Tuần 4: Thuật toán Bernstein 3NF, BCNF & Chứng minh Bảng Chase",
         "Thời gian: 28/09/2026 (19h30 - 21h45). Hình thức: Họp nhóm tại Thư viện SGU.\nThành viên tham dự: Đầy đủ 5/5 thành viên.",
         "Nội dung & Nghị quyết:",
         ["TV1 hoàn thành chứng minh toán học thuật toán tổng hợp Bernstein, phân rã lược đồ R thành 4 quan hệ con đạt BCNF.",
          "Cả nhóm cùng duyệt qua từng bước biến đổi ma trận Chase Tableau 4x13, chứng minh tính bảo toàn thông tin Lossless Join.",
          "Phân tích hiện tượng MVD giữa sở thích và môn học, quyết định tách bảng đạt Dạng chuẩn 4 (4NF).",
          "TV3 cập nhật lại toàn bộ schema.sql và constraints.sql theo kết quả chuẩn hóa."]),

        ("Cuộc họp Tuần 5: Thiết kế 4 Mô hình Cây Phân cấp & Thống nhất Ground Truth",
         "Thời gian: 05/10/2026 (20h00 - 22h15). Hình thức: Discord Voice.\nThành viên tham dự: Đầy đủ 5/5 thành viên.",
         "Nội dung & Nghị quyết:",
         ["TV2 (Hưng) trình bày cấu trúc dữ liệu và giải thuật của 4 mô hình cây: Adjacency List, Path Enum (ltree), Nested Set, Closure Table.",
          "Thống nhất bộ Quy ước Chuẩn tắc Ground Truth: Subtree (Q2, Q8) chứa chính nút gốc; Tổ tiên (Q3, Q10) không chứa chính nó; Gốc có depth = 1, indent = 0.",
          "TV2 triển khai bộ 10 truy vấn Q1–Q10 và 3 thao tác CRUD trên 4 mô hình.",
          "TV5 chuẩn bị kế hoạch sinh dữ liệu lớn 1.000, 10.000 và 100.000 bản ghi để chuẩn bị đo đạc."]),

        ("Cuộc họp Tuần 6: Lập trình CSDL Nâng cao, ODL/OQL & Thiết lập Neo4j Docker",
         "Thời gian: 12/10/2026 (19h30 - 22h00). Hình thức: Lab CNTT.\nThành viên tham dự: Đầy đủ 5/5 thành viên.",
         "Nội dung & Nghị quyết:",
         ["TV3 hoàn thành bộ 8 truy vấn nâng cao Q1–Q8, viết Triggers, Stored Procedure proc_add_friend và mã nhúng Python psycopg2.",
          "TV2 hoàn thiện lược đồ ODL 6 lớp đối tượng chuẩn ODMG 3.0, viết 8 câu truy vấn OQL và ánh xạ JPQL.",
          "TV4 (Chương) thiết lập thành công máy chủ Docker Neo4j 5.x, viết kịch bản nạp dữ liệu Cypher và giải quyết 4 bài toán đồ thị R1–R4.",
          "Đối chiếu kết quả giữa SQL đệ quy và Cypher: xác nhận kết quả trả về hoàn toàn đồng nhất."]),

        ("Cuộc họp Tuần 7: Thực hiện Benchmark 360 runs, Kích hoạt Deadlock & Thử tải pgbench",
         "Thời gian: 19/10/2026 (20h00 - 22h30). Hình thức: Google Meet.\nThành viên tham dự: Đầy đủ 5/5 thành viên.",
         "Nội dung & Nghị quyết:",
         ["TV5 chạy tự động hóa toàn bộ 360 phép đo Benchmark trên 1k, 10k, 100k nút, trích xuất dữ liệu JSON và vẽ 9 biểu đồ hiệu năng chất lượng cao.",
          "TV4 thực hiện thành công kịch bản bế tắc Deadlock T3 trên 2 session, ghi nhận nhật ký lỗi SQLSTATE 40P01.",
          "TV4 chạy thử tải pgbench trên 5, 10, 20 clients, đạt thông lượng ổn định ~3,440 TPS với 0% lỗi.",
          "TV4 khảo sát ma trận cô lập giao dịch và ghi nhận log Write Skew (SQLSTATE 40001) trong PostgreSQL SSI."]),

        ("Cuộc họp Tuần 8: Tích hợp Báo cáo Tổng kết Master, Slide Bảo vệ & Nghiệm thu",
         "Thời gian: 26/10/2026 (19h00 - 22h30). Hình thức: Họp trực tiếp tại SGU.\nThành viên tham dự: Đầy đủ 5/5 thành viên.",
         "Nội dung & Nghị quyết:",
         ["TV1 tổng hợp toàn bộ kết quả của 5 thành viên thành Báo cáo tổng kết hoàn chỉnh De_tai_17_Bao_cao_Tong_ket.docx quy mô ~120 trang.",
          "Hoàn thiện Slide thuyết trình PowerPoint De_tai_17_Slide_Thuyet_trinh.pptx và tài liệu kịch bản thuyết trình noidungpp.docx.",
          "Tổ chức tổng duyệt thuyết trình thử (Rehearsal) phân bổ 3 phút/thành viên và diễn tập kịch bản Demo 5 phút.",
          "Nghiệm thu toàn diện: 100% mục tiêu của đề tài đã hoàn thành xuất sắc!"])
    ]

    for title, meta, sec_title, items in meetings_detail:
        add_heading_3(doc, title)
        add_paragraph(doc, meta, italic=True)
        add_paragraph(doc, sec_title, bold_prefix="Nội dung chính: ")
        for it in items:
            add_bullet(doc, it)

    # --- BẢNG ĐỐI CHIẾU LỊCH SỬ GIT COMMITS CỦA CÁC THÀNH VIÊN ---
    add_heading_2(doc, "3. Bảng Bản đồ Lịch sử Git Commits & Đóng góp Mã nguồn")
    add_paragraph(doc, "Để minh chứng tính khách quan và tính xác thực trong quá trình cộng tác nhóm, bảng dưới đây tổng hợp các nhánh Git (Branches), các mốc Commits tiêu biểu và các module mã nguồn do từng thành viên trực tiếp thực hiện trên kho GitHub:")

    git_headers = ["Thành viên (Git Account)", "Nhánh làm việc (Branch)", "Các Commit tiêu biểu (Hash)", "Các tệp mã nguồn chính đóng góp"]
    git_data = [
        ["Trần Quang\n(@TrkQuang)", "main, dev-docs", "ac88212, f2088f1,\n013c773, 989bc10", "report/De_tai_17_Bao_cao_Tong_ket.docx,\ndocs/scripts/build_master_report.py,\ndocs/eer.drawio, slides/"],
        ["Thanh Hưng\n(@ThanhHung1608)", "TV2_Trees_OOCSDL,\nmain", "d1354bb, e37492c,\n84ff7ba, b82215c", "trees/adjacency.sql, trees/path_enum.sql,\ntrees/nested_set.sql, trees/closure_table.sql,\noo_model/schema.odl, oo_model/queries.oql"],
        ["Quang Hữu\n(@quanghuu0409)", "TV3_SQL_Nangcao,\nmain", "cf60e75, 48c5b08,\n053d100, 26cf194", "sql_advanced/q1_q8_advanced.sql,\nsql_advanced/programmability/,\nsql_advanced/embedded/psycopg2_cursor.py,\nsql_advanced/recursive/r1_r4_graph.sql"],
        ["Chương Võ\n(@chuong4482)", "TV4_Neo4j_Benchmark,\nmain", "c8ba3ea, a9a59aa,\na88e2c0, a8dc9fb", "neo4j/docker-compose.yml, neo4j/cypher/,\nconcurrency/deadlock_t3.sql,\nbenchmark/pgbench/run_pgbench.ps1,\nconcurrency/isolation_tests.sql"],
        ["Như Quỳnh\n(@NhuQuynh2102)", "TV5_Data_Benchmark,\nmain", "df580fa, a72efcf,\n5734fa0, 8d39cf6", "data/seed_data_1k_10k_100k.py,\nbenchmark/runner/benchmark_suite.py,\nbenchmark/results/charts/,\nbenchmark/analysis/storage_breakdown.sql"],
    ]
    add_styled_table(doc, git_headers, git_data, [1.5, 1.4, 1.4, 2.5])

    # --- RUBRICS ĐÁNH GIÁ LÀM VIỆC NHÓM CLO7 ---
    add_heading_2(doc, "4. Rubrics Đánh giá Làm việc Nhóm theo Chuẩn Đầu ra CLO7")
    add_paragraph(doc, "Bảng tiêu chí đánh giá đóng góp cá nhân (Rubrics) dựa trên thang đo chuẩn của Trường Đại học Sài Gòn, bao gồm 4 tiêu chí: (1) Tính chuyên cần & Thái độ; (2) Chất lượng đóng góp kỹ thuật; (3) Đúng tiến độ cam kết; (4) Khả năng phối hợp và giải quyết xung đột:")

    rubric_headers = ["Thành viên", "Chuyên cần (20%)", "Kỹ thuật (40%)", "Tiến độ (20%)", "Hợp tác (20%)", "Điểm tự đánh giá", "Đồng thuận Nhóm"]
    rubric_data = [
        ["Trần Quang (TV1)", "10 / 10\n(Tham gia đủ 8 họp)", "10 / 10\n(Leader, Spec, Chuẩn hóa, Report)", "10 / 10\n(Hoàn thành sớm)", "10 / 10\n(Điều phối xuất sắc)", "10.0 / 10", "10.0 / 10\n(Xếp loại A+)"],
        ["Thanh Hưng (TV2)", "10 / 10\n(Tham gia đủ 8 họp)", "10 / 10\n(4 Mô hình cây, ODL, OQL, JPQL)", "10 / 10\n(Đúng hạn)", "10 / 10\n(Tương tác tích cực)", "10.0 / 10", "10.0 / 10\n(Xếp loại A+)"],
        ["Quang Hữu (TV3)", "10 / 10\n(Tham gia đủ 8 họp)", "10 / 10\n(DDL, SQL Q1-Q12, Giao dịch T1-T2)", "10 / 10\n(Đúng hạn)", "10 / 10\n(Hỗ trợ đồng đội tốt)", "10.0 / 10", "10.0 / 10\n(Xếp loại A+)"],
        ["Chương Võ (TV4)", "10 / 10\n(Tham gia đủ 8 họp)", "10 / 10\n(Neo4j Docker, Cypher, Deadlock, pgbench)", "10 / 10\n(Đúng hạn)", "10 / 10\n(Chủ động kỹ thuật)", "10.0 / 10", "10.0 / 10\n(Xếp loại A+)"],
        ["Như Quỳnh (TV5)", "10 / 10\n(Tham gia đủ 8 họp)", "10 / 10\n(Seed lớn, Benchmark 360 runs, Charts)", "10 / 10\n(Đúng hạn)", "10 / 10\n(Chăm chỉ, chính xác)", "10.0 / 10", "10.0 / 10\n(Xếp loại A+)"],
    ]
    add_styled_table(doc, rubric_headers, rubric_data, [1.4, 0.9, 1.4, 0.9, 0.9, 1.0, 1.1])

    add_callout_box(doc, "LỜI KẾT VÀ XÁC NHẬN CỦA NHÓM TRƯỞNG:\n"
                         "Thay mặt toàn thể 5 thành viên nhóm Đề tài 17, tôi xin khẳng định toàn bộ nội dung trong Báo cáo tổng kết này là kết quả lao động học thuật nghiêm túc, trung thực và đoàn kết của tập thể nhóm. Mọi thành viên đều đã nỗ lực cống hiến 100% năng lực và hoàn thành xuất sắc các mục tiêu của môn học Cơ sở dữ liệu nâng cao.\n"
                         "Trân trọng kính trình Hội đồng Giảng viên đánh giá và nghiệm thu!",
                    "LỜI KẾT VÀ XÁC NHẬN CỦA NHÓM TRƯỞNG")
