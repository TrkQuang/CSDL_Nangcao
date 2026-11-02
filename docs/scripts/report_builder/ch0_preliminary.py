"""
Phần mở đầu, Trang bìa, Lời cảm ơn, Danh mục hình bảng (20 hình, hơn 50 bảng), và Lời mở đầu.
Mở rộng chi tiết phục vụ báo cáo quy mô lớn (~120 trang).
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from .styles import (
    add_heading_1, add_heading_2, add_heading_3,
    add_paragraph, add_bullet, add_styled_table, add_callout_box,
    C_PRIMARY, C_SECONDARY, C_MUTED
)

def build_ch0(doc: Document):
    # --- TRANG BÌA HỌC THUẬT ---
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_uni.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC SÀI GÒN\nKHOA CÔNG NGHỆ THÔNG TIN\n")
    r_uni.bold = True
    r_uni.font.name = "Times New Roman"
    r_uni.font.size = Pt(13)
    p_uni.add_run("—" * 25 + "\n\n")

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_report = p_title.add_run("BÁO CÁO TỔNG KẾT ĐỒ ÁN MÔN HỌC\nCƠ SỞ DỮ LIỆU NÂNG CAO\n\n")
    r_report.font.name = "Times New Roman"
    r_report.font.size = Pt(14)
    r_report.bold = True
    r_report.font.color.rgb = C_SECONDARY

    r_topic_label = p_title.add_run("ĐỀ TÀI SỐ 17:\n")
    r_topic_label.font.name = "Times New Roman"
    r_topic_label.font.size = Pt(13)
    r_topic_label.bold = True
    r_topic_label.font.color.rgb = RGBColor(0, 0, 0)

    r_topic_name = p_title.add_run("DỮ LIỆU PHÂN CẤP VÀ DỮ LIỆU ĐỒ THỊ TRONG CSDL QUAN HỆ:\nỨNG DỤNG MẠNG XÃ HỘI HỌC TẬP\n\n")
    r_topic_name.font.name = "Times New Roman"
    r_topic_name.font.size = Pt(16)
    r_topic_name.bold = True
    r_topic_name.font.color.rgb = C_PRIMARY

    doc.add_paragraph("\n")

    p_info = doc.add_paragraph()
    p_info.paragraph_format.left_indent = Inches(1.2)
    p_info.paragraph_format.line_spacing = 1.25

    def add_meta(label, val):
        r1 = p_info.add_run(label)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11.5)
        r1.bold = True
        r2 = p_info.add_run(val + "\n")
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11.5)

    add_meta("Giảng viên hướng dẫn: ", "Bộ môn Hệ thống Thông tin — Khoa CNTT")
    add_meta("Lớp học phần: ", "Cơ sở dữ liệu nâng cao — Học kỳ 1, Năm học 2026–2027")
    add_meta("Nhóm thực hiện: ", "Nhóm Đề tài 17 (5 thành viên)")
    p_info.add_run("Danh sách thành viên & Phân công vai trò:\n").bold = True
    p_info.add_run("  1. Trần Quang (Nhóm trưởng)  — MSSV: 3124410292 (TV1: Spec, EER, Chuẩn hóa, Điều phối)\n")
    p_info.add_run("  2. Thanh Hưng                 — TV2: 4 Mô hình Cây, ODL, OQL, JPQL\n")
    p_info.add_run("  3. Quang Hữu                  — TV3: Schema DDL, SQL Nâng cao Q1–Q12, Giao dịch T1–T2\n")
    p_info.add_run("  4. Chương Võ                  — TV4: CSDL Đồ thị Neo4j/Cypher, Deadlock T3, pgbench\n")
    p_info.add_run("  5. Như Quỳnh                  — MSSV: 3124410298 (TV5: Seed lớn, Chỉ mục, Benchmark 360 runs)\n\n")
    add_meta("Hệ quản trị CSDL: ", "PostgreSQL 16+ (PostgreSQL 18.6) & Neo4j 5.x Community")
    add_meta("Kho lưu trữ mã nguồn: ", "https://github.com/TrkQuang/CSDL_Nangcao.git")

    doc.add_paragraph("\n" * 2)
    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_date = p_date.add_run("THÀNH PHỐ HỒ CHÍ MINH — THÁNG 10 NĂM 2026")
    r_date.bold = True
    r_date.font.name = "Times New Roman"
    r_date.font.size = Pt(12)

    doc.add_page_break()

    # --- LỜI CẢM ƠN & LỜI CAM ĐOAN ---
    add_heading_1(doc, "LỜI CẢM ƠN VÀ CAM ĐOAN HỌC THUẬT")
    add_paragraph(doc, "Lời đầu tiên, tập thể nhóm sinh viên thực hiện Đề tài 17 xin trân trọng gửi lời cảm ơn sâu sắc nhất đến Quý Thầy, Cô bộ môn Hệ thống Thông tin — Khoa Công nghệ Thông tin, Trường Đại học Sài Gòn, những người đã tận tâm truyền đạt tri thức quý báu về thiết kế cơ sở dữ liệu nâng cao, tối ưu hóa truy vấn, kiến trúc lưu trữ vật lý và các mô hình dữ liệu hiện đại.")
    add_paragraph(doc, "Tập thể nhóm 5 thành viên xin cam đoan bằng danh dự học thuật:", bold_prefix="Lời cam đoan: ")
    add_bullet(doc, "Toàn bộ mã nguồn SQL, Cypher, PL/pgSQL, ODL, OQL, Python và PowerShell trong kho lưu trữ https://github.com/TrkQuang/CSDL_Nangcao.git đều do các thành viên trong nhóm trực tiếp nghiên cứu, lập trình và thực thi kiểm chứng.")
    add_bullet(doc, "Mọi số liệu thực nghiệm (360 phép đo Benchmark trên 1.000, 10.000, 100.000 nút; kết quả thử tải pgbench đạt ~3,440 TPS; dấu vết bế tắc Deadlock SQLSTATE 40P01; kết quả đo đạc dung lượng đĩa và buffer cache) đều được trích xuất trung thực từ hệ quản trị PostgreSQL 18.6 và Neo4j 5.x Community chạy trên môi trường thực tế.")

    doc.add_page_break()

    # --- MỤC LỤC TỔNG QUAN ---
    add_heading_1(doc, "MỤC LỤC TỔNG QUAN")
    toc_data = [
        ["Phần", "Tiêu đề nội dung", "Trang"],
        ["—", "LỜI CẢM ƠN VÀ CAM ĐOAN HỌC THUẬT", "2"],
        ["—", "DANH MỤC HÌNH ẢNH MINH HỌA (20 HÌNH)", "4"],
        ["—", "DANH MỤC BẢNG BIỂU ĐỐI SÁNH & THUẬT NGỮ", "5"],
        ["—", "LỜI MỞ ĐẦU (Bối cảnh, Tính cấp thiết & 3 Câu hỏi RQ1–RQ3)", "6"],
        ["CHƯƠNG 1", "ĐẶC TẢ NGHIỆP VỤ & THIẾT KẾ MỨC QUAN NIỆM (EER)", "10"],
        ["CHƯƠNG 2", "LÝ THUYẾT PHỤ THUỘC HÀM & CHUẨN HÓA DỮ LIỆU", "26"],
        ["CHƯƠNG 3", "DỮ LIỆU PHÂN CẤP (CÂY) TRÊN CƠ SỞ DỮ LIỆU QUAN HỆ", "46"],
        ["CHƯƠNG 4", "SQL NÂNG CAO, ĐỆ QUY ĐỒ THỊ & ĐIỀU KHIỂN ĐỒNG THỜI", "68"],
        ["CHƯƠNG 5", "CSDL HƯỚNG ĐỐI TƯỢNG VÀ CSDL ĐỒ THỊ CHUYÊN DỤNG", "86"],
        ["CHƯƠNG 6", "THIẾT KẾ VẬT LÝ, BENCHMARK & THỬ TẢI ĐỒNG THỜI", "102"],
        ["—", "KẾT LUẬN & HƯỚNG PHÁT TRIỂN", "116"],
        ["PHỤ LỤC", "BÁO CÁO LÀM VIỆC NHÓM & BẢNG ĐÓNG GÓP (CLO7)", "118"],
    ]
    add_styled_table(doc, toc_data[0], toc_data[1:], [1.0, 5.0, 0.8])

    # --- DANH MỤC HÌNH ẢNH MINH HỌA ---
    add_heading_2(doc, "DANH MỤC HÌNH ẢNH MINH HỌA (20 FIGURES)")
    fig_data = [
        ["Mã hình", "Tên hình ảnh và nội dung kỹ thuật minh họa", "Vị trí trong báo cáo"],
        ["Hình 1.1", "Sơ đồ Thực thể - Mối kết hợp mở rộng (EER Diagram) Mạng xã hội học tập", "Mục 1.2, Chương 1"],
        ["Hình 1.2", "Sơ đồ Lược đồ CSDL Quan hệ Vật lý (Physical Relational Schema) trên PostgreSQL 18.6", "Mục 1.2.3, Chương 1"],
        ["Hình 3.1", "Sơ đồ Trực quan hóa Cấu trúc Lưu trữ 4 Mô hình Cây trên Cây bình luận mẫu", "Mục 3.1, Chương 3"],
        ["Hình 4.1", "Sơ đồ Đồ thị Chờ khóa (Wait-For Graph - WFG) gây ra Bế tắc (Deadlock T3)", "Mục 4.4, Chương 4"],
        ["Hình 5.1", "Sơ đồ 6 Lớp đối tượng ODMG 3.0 (UML Class Diagram) và Ánh xạ kế thừa", "Mục 5.1, Chương 5"],
        ["Hình 5.2", "Toàn cảnh Đồ thị Mạng xã hội học tập hiển thị trên Neo4j Browser (Graph View)", "Mục 5.2, Chương 5"],
        ["Hình 5.3", "Kết quả trực quan hóa truy vấn Bạn của bạn (Friends-of-Friends) trên Neo4j", "Mục 5.2, Chương 5"],
        ["Hình 5.4", "Đường đi ngắn nhất giữa hai sinh viên (Shortest Path BFS) trên Neo4j Browser", "Mục 5.2, Chương 5"],
        ["Hình 5.5", "Phát hiện chu trình quan hệ bạn bè (Cycle Detection) trên Neo4j Browser", "Mục 5.2, Chương 5"],
        ["Hình 5.6", "Sơ đồ Kiến trúc Đa lưu trữ (Polyglot Persistence) kết hợp PostgreSQL và Neo4j", "Mục 5.3, Chương 5"],
        ["Hình 6.1", "Biểu đồ So sánh Dung lượng Lưu trữ Vật lý trên Đĩa (MB) giữa 4 Mô hình Cây tại 100k nút", "Mục 6.1, Chương 6"],
        ["Hình 6.2", "Biểu đồ Thời gian truy vấn đọc cây con (Q2) tại quy mô 1.000 nút (ms)", "Mục 6.2.1, Chương 6"],
        ["Hình 6.3", "Biểu đồ Thời gian truy vấn đọc cây con (Q2) tại quy mô 10.000 nút (ms)", "Mục 6.2.1, Chương 6"],
        ["Hình 6.4", "Biểu đồ Thời gian truy vấn đọc cây con (Q2) tại quy mô 100.000 nút (ms)", "Mục 6.2.1, Chương 6"],
        ["Hình 6.5", "Biểu đồ Thời gian ghi thêm nút lá mới (Insert Leaf) tại quy mô 1.000 nút (ms)", "Mục 6.2.2, Chương 6"],
        ["Hình 6.6", "Biểu đồ Thời gian ghi thêm nút lá mới (Insert Leaf) tại quy mô 10.000 nút (ms)", "Mục 6.2.2, Chương 6"],
        ["Hình 6.7", "Biểu đồ Thời gian ghi thêm nút lá mới (Insert Leaf) tại quy mô 100.000 nút (ms)", "Mục 6.2.2, Chương 6"],
        ["Hình 6.8", "Biểu đồ Thời gian cập nhật di chuyển nhánh cây con (Move Subtree) tại 1.000 nút (ms)", "Mục 6.2.3, Chương 6"],
        ["Hình 6.9", "Biểu đồ Thời gian cập nhật di chuyển nhánh cây con (Move Subtree) tại 10.000 nút (ms)", "Mục 6.2.3, Chương 6"],
        ["Hình 6.10", "Biểu đồ Thời gian cập nhật di chuyển nhánh cây con (Move Subtree) tại 100.000 nút (ms)", "Mục 6.2.3, Chương 6"],
    ]
    add_styled_table(doc, fig_data[0], fig_data[1:], [1.0, 4.8, 1.2])

    # --- DANH MỤC THUẬT NGỮ ĐỐI CHIẾU ANH - VIỆT ---
    add_heading_2(doc, "DANH MỤC THUẬT NGỮ VÀ VIẾT TẮT ĐỐI CHIẾU (GLOSSARY)")
    glossary_headers = ["Thuật ngữ / Viết tắt", "Tên tiếng Anh đầy đủ", "Ý nghĩa và Định nghĩa chuyên ngành"]
    glossary_data = [
        ["RDBMS", "Relational Database Management System", "Hệ quản trị cơ sở dữ liệu quan hệ (dựa trên mô hình E.F. Codd)."],
        ["EER", "Enhanced Entity-Relationship", "Mô hình Thực thể - Mối kết hợp mở rộng (hỗ trợ kế thừa, chuyên môn hóa)."],
        ["FD", "Functional Dependency", "Phụ thuộc hàm: mối ràng buộc ngữ nghĩa giữa các tập thuộc tính."],
        ["3NF", "Third Normal Form", "Dạng chuẩn 3: triệt tiêu phụ thuộc hàm bắc cầu giữa các thuộc tính không khóa."],
        ["BCNF", "Boyce-Codd Normal Form", "Dạng chuẩn Boyce-Codd: mọi vế trái của FD phi tầm thường đều là siêu khóa."],
        ["MVD", "Multi-Valued Dependency", "Phụ thuộc đa trị: một thuộc tính xác định độc lập một tập giá trị khác."],
        ["4NF", "Fourth Normal Form", "Dạng chuẩn 4: triệt tiêu phụ thuộc đa trị phi tầm thường."],
        ["MPTT", "Modified Preorder Tree Traversal", "Thuật toán duyệt cây trước có sửa đổi (Mô hình Tập lồng Nested Set)."],
        ["GiST", "Generalized Search Tree", "Chỉ mục cây tìm kiếm tổng quát trong PostgreSQL (tối ưu cho ltree)."],
        ["GIN", "Generalized Inverted Index", "Chỉ mục đảo ngược tổng quát trong PostgreSQL (tối ưu cho mảng, Full-Text)."],
        ["CTE", "Common Table Expression", "Biểu thức bảng chung trong SQL (hỗ trợ đệ quy WITH RECURSIVE)."],
        ["WFG", "Wait-For Graph", "Đồ thị Chờ khóa: đồ thị có hướng phát hiện bế tắc (Deadlock) giữa các phiên."],
        ["ODMG", "Object Data Management Group", "Hiệp hội chuẩn hóa CSDL hướng đối tượng (chuẩn ODL, OQL)."],
        ["ODL", "Object Definition Language", "Ngôn ngữ định nghĩa đối tượng độc lập với ngôn ngữ lập trình."],
        ["OQL", "Object Query Language", "Ngôn ngữ truy vấn đối tượng chuẩn ODMG."],
        ["JPA", "Java Persistence API", "Giao diện lập trình chuẩn ánh xạ đối tượng - quan hệ trong Java."],
        ["JPQL", "Java Persistence Query Language", "Ngôn ngữ truy vấn thực thể hướng đối tượng của JPA."],
        ["LPG", "Labeled Property Graph", "Mô hình đồ thị có nhãn thuộc tính (chuẩn mô hình của Neo4j)."],
        ["CDC", "Change Data Capture", "Kỹ thuật bắt và truyền phát biến động dữ liệu thời gian thực (Debezium/Kafka)."],
        ["MVCC", "Multi-Version Concurrency Control", "Điều khiển đồng thời đa phiên bản dòng dữ liệu."],
        ["HOT", "Heap-Only Tuples", "Kỹ thuật tối ưu hóa cập nhật trang dữ liệu không cần sửa chỉ mục."],
        ["TOAST", "The Oversized-Attribute Storage Technique", "Động cơ lưu trữ và nén dữ liệu quá khổ trong PostgreSQL."],
        ["SSI", "Serializable Snapshot Isolation", "Mức cô lập tuần tự hóa dựa trên phát hiện phụ thuộc đọc-ghi."],
        ["TPS", "Transactions Per Second", "Số lượng giao dịch xử lý thành công trong một giây."],
    ]
    add_styled_table(doc, glossary_headers, glossary_data, [1.6, 2.2, 3.2])

    doc.add_page_break()

    # --- LỜI MỞ ĐẦU ---
    add_heading_1(doc, "LỜI MỞ ĐẦU")
    add_heading_2(doc, "1.1 Tổng quan Lịch sử Tiến hóa các Mô hình Cơ sở Dữ liệu")
    add_paragraph(doc, "Để hiểu rõ bối cảnh và ý nghĩa học thuật của Đề tài 17, cần khảo sát toàn cảnh hơn nửa thế kỷ tiến hóa của công nghệ quản trị dữ liệu:")
    add_bullet(doc, "Xuất hiện vào cuối thập niên 1960 với hệ thống tiêu biểu là IBM IMS (Information Management System) phục vụ chương trình thám hiểm Apollo. Dữ liệu được tổ chức dưới dạng cấu trúc cây phân cấp nghiêm ngặt (1 nút cha có nhiều nút con, mỗi con chỉ có đúng 1 cha). Ưu điểm: Tốc độ truy xuất cực nhanh theo con trỏ vật lý. Nhược điểm: Cực kỳ cứng nhắc, không thể biểu diễn trực tiếp các quan hệ nhiều-nhiều (M:N) nếu không nhân bản dữ liệu.", bold_prefix="1. Mô hình Phân cấp (Hierarchical Model - 1968): ")
    add_bullet(doc, "Được chuẩn hóa bởi nhóm CODASYL DBTG (1971), mô hình mạng mở rộng mô hình phân cấp bằng cách cho phép một nút bản ghi có nhiều nút chủ (Record Owners), giải quyết được bài toán quan hệ M:N. Tuy nhiên, lập trình viên vẫn phải điều hướng dữ liệu thủ công qua các con trỏ vật lý (Navigation by Pointers), khiến việc bảo trì và thay đổi cấu trúc schema vô cùng tốn kém.", bold_prefix="2. Mô hình Mạng (Network Model - 1971): ")
    add_bullet(doc, "Được đề xuất bởi Tiến sĩ Edgar F. Codd (IBM Research) qua công trình mang tính cách mạng năm 1970. Codd đã tách biệt hoàn toàn mức logic độc lập với mức vật lý lưu trữ, mô hình hóa dữ liệu dưới dạng các bảng quan hệ 2 chiều dựa trên lý thuyết tập hợp và đại số quan hệ. Sự ra đời của ngôn ngữ SQL chuẩn hóa đã đưa RDBMS (Oracle, IBM DB2, PostgreSQL, MySQL) trở thành tiêu chuẩn công nghiệp áp đảo suốt 40 năm qua.", bold_prefix="3. Mô hình Quan hệ (Relational Model - 1970): ")
    add_bullet(doc, "Bùng nổ vào thập niên 1990 cùng sự thống trị của các ngôn ngữ lập trình OOP (C++, Smalltalk, Java). Các chuẩn ODMG (ODL, OQL) ra đời nhằm lưu trữ trực tiếp các đối tượng phức tạp mà không cần phân rã thành bảng. Dù có nhiều ưu thế lý thuyết, OODBMS thuần túy bị giới hạn bởi tính phức tạp và thiếu chuẩn hóa truy vấn tối ưu.", bold_prefix="4. Mô hình Hướng đối tượng (OODBMS / ODMG - 1990s): ")
    add_bullet(doc, "Chuẩn SQL:1999 và các hệ CSDL quan hệ hiện đại như PostgreSQL đã tích hợp các tính năng hướng đối tượng: kiểu dữ liệu mảng, kiểu bản ghi phức hợp composite, kế thừa bảng (Table Inheritance), và kiểu dữ liệu bán cấu trúc JSONB. RDBMS chuyển mình thành ORDBMS mạnh mẽ.", bold_prefix="5. Mô hình Quan hệ Hướng đối tượng (ORDBMS - SQL:1999): ")
    add_bullet(doc, "Sự bùng nổ của mạng xã hội, dữ liệu phân cấp lồng nhau và mạng lưới kết nối phức tạp đã thúc đẩy sự ra đời của các CSDL Đồ thị chuyên dụng (Neo4j, Amazon Neptune) và phong trào Đa lưu trữ (Polyglot Persistence): sử dụng đúng công cụ cho đúng bài toán dữ liệu.", bold_prefix="6. CSDL Đồ thị & Đa lưu trữ (Graph Databases & Polyglot Persistence - Hiện đại): ")

    add_heading_2(doc, "1. Bối cảnh đề tài và tính cấp thiết")
    add_paragraph(doc, "Trong kỷ nguyên chuyển đổi số giáo dục (EdTech), các nền tảng mạng xã hội học tập (như Stack Overflow, Piazza, Canvas, Coursera Community) đã trở thành hạ tầng tri thức không thể thiếu cho sinh viên, giảng viên và các nhà nghiên cứu. Khác với các hệ thống thông tin quản lý truyền thống (ERP, CRM) vốn chủ yếu xoay quanh các bảng dữ liệu hai chiều có cấu trúc phẳng, mạng xã hội học tập đặt ra những thách thức công nghệ rất đặc thù:")
    add_bullet(doc, "Cấu trúc dữ liệu phân cấp sâu (Hierarchical Tree Data): Các chuỗi bài thảo luận (Discussion Threads), chuỗi bình luận trả lời lồng nhau vô hạn cấp (Nested Comments), và hệ thống thư mục tài liệu nhóm học tập đòi hỏi khả năng truy xuất cây con, tìm đường dẫn tổ tiên và tái cấu trúc cây một cách tức thì.", bold_prefix="1. Phân cấp sâu: ")
    add_bullet(doc, "Cấu trúc dữ liệu đồ thị phức tạp (Graph Data): Quan hệ kết bạn hai chiều (Friendship Graph), quan hệ theo dõi có hướng (Follower/Followee), và các mạng lưới cộng tác nhóm tạo nên một đồ thị mạng xã hội quy mô lớn. Các nghiệp vụ như gợi ý bạn bè chung (Friends-of-Friends), tìm đường đi ngắn nhất giữa hai học viên (Shortest Path), và phát hiện nhóm học tập liên thông đòi hỏi việc duyệt đồ thị đa chặng.", bold_prefix="2. Đồ thị phức tạp: ")
    add_bullet(doc, "Tải tương tác đồng thời cao (High Concurrency & ACID Integrity): Khi hàng ngàn sinh viên cùng tham gia thảo luận, nộp bài, bình luận và bày tỏ cảm xúc tại một thời điểm, hệ thống đối mặt với nguy cơ xung đột khóa dòng (Lock Contention), bế tắc giao dịch (Deadlock), và hiện tượng bão hòa thông lượng.", bold_prefix="3. Đồng thời cao: ")

    add_heading_2(doc, "2. Mục tiêu nghiên cứu và 3 câu hỏi nghiên cứu cốt lõi")
    add_paragraph(doc, "Đồ án Đề tài 17 được triển khai nhằm mục tiêu giải quyết thấu đáo và định lượng 3 câu hỏi nghiên cứu (Research Questions - RQ) mang tính thời sự và học thuật chuyên sâu:")
    add_paragraph(doc, "Làm thế nào để mô hình hóa và lưu trữ dữ liệu dạng cây phân cấp trên một hệ quản trị CSDL quan hệ (PostgreSQL) để đạt hiệu năng tối ưu nhất giữa thao tác đọc cây con (Read-heavy) và thao tác ghi/di chuyển nhánh cây (Write-heavy)? Đâu là mô hình tối ưu giữa Adjacency List, Path Enumeration (ltree), Nested Set và Closure Table?", bold_prefix="Câu hỏi 1 (RQ1 - Hierarchical Data): ")
    add_paragraph(doc, "Khả năng xử lý các bài toán duyệt đồ thị mạng xã hội của SQL đệ quy (WITH RECURSIVE trong PostgreSQL) đạt đến giới hạn nào? Khi nào hệ thống bắt buộc phải tích hợp một Cơ sở dữ liệu đồ thị chuyên dụng (Neo4j với ngôn ngữ Cypher), và kiến trúc kết hợp đa mô hình (Polyglot Persistence) nên được thiết kế ra sao?", bold_prefix="Câu hỏi 2 (RQ2 - Graph vs Relational): ")
    add_paragraph(doc, "Cơ chế quản trị giao dịch đồng thời (ACID, MVCC, Lock Modes), hiện tượng bế tắc (Deadlock Detection với đồ thị WFG) và kỹ thuật thiết kế chỉ mục vật lý (B-Tree, GIN, GiST) ảnh hưởng như thế nào đến tính toàn vẹn dữ liệu và thông lượng giao dịch (TPS) trong môi trường thử tải cao (Stress Testing với pgbench)?", bold_prefix="Câu hỏi 3 (RQ3 - Concurrency & Physical Design): ")

    doc.add_page_break()
