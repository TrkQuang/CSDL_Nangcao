"""
Chương 7: Kết luận & Hướng phát triển, cùng Phụ lục Báo cáo làm việc nhóm (CLO7).
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

    # --- THỐNG KÊ GIT COMMITS ---
    add_heading_2(doc, "2. Thống kê đóng góp trên Kho lưu trữ Git")
    add_paragraph(doc, "Toàn bộ quá trình hợp tác, tích hợp mã nguồn và tài liệu được ghi nhận minh bạch trên kho lưu trữ GitHub chính thức của đồ án: https://github.com/TrkQuang/CSDL_Nangcao.git")

    git_headers = ["Tài khoản Git", "Họ tên sinh viên", "Nhánh làm việc chính", "Các đầu ra sản phẩm chính bàn giao"]
    git_data = [
        ["TrkQuang", "Trần Quang", "main", "docs/spec.md, eer.drawio, closure_minimal_cover.md, fd_list.md, de_tai_17_report_outline.md, Báo cáo Word master, Slide PPTX."],
        ["ThanhHung1608 / jinkun0091", "Thanh Hưng", "TV2 (merge main)", "tree_models/ (adjacency, path_enum, nested_set, closure_table), oo_model/ (ODL, OQL, JPQL, class_diagram), Chuong_3_va_5.1.docx."],
        ["quanghuu0409", "Quang Hữu", "TV3 (merge main)", "database/schema.sql, constraints.sql, sql_advanced/ (q01-q12), embedded/psycopg2_cursor.py, recursive_sql/, transactions/t1, t2."],
        ["chuong4482", "Chương Võ", "origin/TV4 (merge main)", "neo4j/ (cypher, screenshots), transactions/pgbench/, transactions/t3_concurrent/, run_pgbench.ps1, Bao_cao_chuong_5.2_va_5.3.docx."],
        ["NhuQuynh2102", "Như Quỳnh", "TV5 (merge main)", "benchmark/ (scripts, results, 9 charts PNG), database/seed_large.sql, docs/bao_cao_chuong_6_Quynh.docx, fd_verification.sql."],
    ]
    add_styled_table(doc, git_headers, git_data, [1.4, 1.4, 1.2, 3.0])

    # --- TÓM TẮT 8 BIÊN BẢN HỌP TUẦN ---
    add_heading_2(doc, "3. Tóm tắt Nhật ký 8 cuộc họp nhóm hàng tuần (Team Meeting Minutes)")
    add_paragraph(doc, "Nhóm duy trì lịch họp định kỳ hàng tuần vào Chủ nhật hoặc thứ Hai để đánh giá tiến độ, thảo luận giải pháp kỹ thuật và phân công nhiệm vụ tuần tiếp theo. Dưới đây là tóm tắt biên bản 8 cuộc họp:")

    meeting_headers = ["Cuộc họp", "Thời gian", "Nội dung thảo luận chính", "Nghị quyết & Phân công công việc"]
    meeting_data = [
        ["Tuần 1", "07/09/2026", "Phân tích yêu cầu Đề tài 17; Lựa chọn công nghệ PostgreSQL 16+ và Neo4j; Bầu Trưởng nhóm.", "Trần Quang làm Leader; thống nhất kiến trúc Git repository và lịch họp tuần."],
        ["Tuần 2", "14/09/2026", "Thảo luận 10 quy tắc nghiệp vụ BR1–BR10; Phác thảo sơ đồ thực thể liên kết mở rộng EER.", "TV1 hoàn thiện docs/spec.md và vẽ sơ đồ eer.drawio; TV3 chuẩn bị khung schema.sql."],
        ["Tuần 3", "21/09/2026", "Phân tích lý thuyết phụ thuộc hàm F; Tính toán bao đóng, khóa ứng viên, phủ tối tiểu F_min.", "TV1 tính toán toán học; TV5 viết script SQL kiểm chứng các FD trên dữ liệu mẫu."],
        ["Tuần 4", "28/09/2026", "Thảo luận thuật toán tổng hợp 3NF (Bernstein), kiểm tra BCNF và bảng Chase Lossless Join.", "TV1 hoàn thành chứng minh Chase; TV3 triển khai DDL hoàn chỉnh có đủ khóa ngoại và CHECK."],
        ["Tuần 5", "05/10/2026", "Nghiên cứu 4 mô hình cây phân cấp; Thống nhất Ground Truth Rules (Subtree chứa gốc, Root depth = 1).", "TV2 lập trình 4 mô hình cây Q1–Q10; TV5 chuẩn bị bộ sinh dữ liệu 1k, 10k, 100k nút."],
        ["Tuần 6", "12/10/2026", "Thiết lập môi trường Neo4j Docker; Đối chiếu Cypher và SQL đệ quy; Lập trình SQL nâng cao Q1–Q12.", "TV4 viết Cypher và chụp ảnh Neo4j; TV3 hoàn thiện Window Functions và Stored Procedures."],
        ["Tuần 7", "19/10/2026", "Thực hiện 360 phép đo Benchmark hiệu năng cây; Tái hiện Deadlock T3 (40P01) và thử tải pgbench.", "TV5 xuất 9 biểu đồ hiệu năng; TV4 trích xuất log Deadlock và chạy pgbench 3 mức tải."],
        ["Tuần 8", "26/10/2026", "Tổng kết toàn bộ dự án; Tích hợp báo cáo Word master và Slide thuyết trình PPTX; Tổng duyệt.", "TV1 biên dịch Báo cáo tổng kết hoàn chỉnh và Slide bảo vệ; Cả nhóm duyệt nghiệm thu 100%."],
    ]
    add_styled_table(doc, meeting_headers, meeting_data, [0.8, 1.0, 2.7, 2.5])

    add_callout_box(doc, "XÁC NHẬN CỦA NHÓM TRƯỞNG:\n"
                         "Thay mặt toàn thể 5 thành viên nhóm Đề tài 17, tôi xin khẳng định toàn bộ nội dung trong Báo cáo tổng kết này là kết quả lao động học thuật nghiêm túc, trung thực và đoàn kết của tập thể nhóm. Mọi thành viên đều đã nỗ lực cống hiến 100% năng lực và hoàn thành xuất sắc các mục tiêu của môn học Cơ sở dữ liệu nâng cao.\n"
                         "Trân trọng kính trình Hội đồng Giảng viên đánh giá và nghiệm thu!",
                    "LỜI KẾT VÀ XÁC NHẬN CỦA NHÓM TRƯỞNG")
