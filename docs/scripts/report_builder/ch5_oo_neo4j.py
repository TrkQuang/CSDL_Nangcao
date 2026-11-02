"""
Chương 5: Cơ sở dữ liệu Hướng đối tượng (ODMG 3.0) và Cơ sở dữ liệu Đồ thị chuyên dụng (Neo4j).
"""

from docx import Document
from .styles import (
    add_heading_1, add_heading_2, add_heading_3,
    add_paragraph, add_bullet, add_styled_table, add_code_block, add_figure, add_callout_box
)

def build_ch5(doc: Document):
    add_heading_1(doc, "CHƯƠNG 5: CSDL HƯỚNG ĐỐI TƯỢNG VÀ CSDL ĐỒ THỊ CHUYÊN DỤNG")

    # ========================================================
    # 5.1 CƠ SỞ DỮ LIỆU HƯỚNG ĐỐI TƯỢNG
    # ========================================================
    add_heading_2(doc, "5.1 Mô hình Hướng đối tượng: Lược đồ ODL, Truy vấn OQL và Ánh xạ JPQL")
    add_paragraph(doc, "Để khắc phục sự chia cắt giữa tư duy lập trình hướng đối tượng (OOP) của các ngôn ngữ hiện đại (như Java, C#, Python) và cấu trúc bảng quan hệ phẳng của RDBMS, nhóm đã xây dựng mô hình CSDL Hướng đối tượng hoàn chỉnh tuân thủ tiêu chuẩn công nghiệp ODMG 3.0 (Object Data Management Group):")

    add_figure(doc, "oo_model/class_diagram.png", "Hình 5.1: Sơ đồ 6 Lớp đối tượng ODMG 3.0 (UML Class Diagram) Hệ thống Mạng xã hội học tập", width_inches=6.4)

    add_heading_3(doc, "5.1.1 Lược đồ định nghĩa đối tượng ODL (Object Definition Language)")
    add_paragraph(doc, "Lược đồ ODL định nghĩa rõ ràng phạm vi thể hiện (extent), khóa định danh đối tượng (key), các thuộc tính đơn/phức hợp, các mối kết hợp đối ứng tự động (relationships với từ khóa inverse) và chữ ký các phương thức nghiệp vụ:")

    add_code_block(doc, "module SocialLearningNetwork {\n"
                        "    class NguoiDung (extent dsNguoiDung, key user_id) {\n"
                        "        attribute integer user_id;\n"
                        "        attribute string email;\n"
                        "        attribute string ho_ten;\n"
                        "        attribute set<string> so_thich;\n"
                        "        attribute set<string> mon_hoc;\n"
                        "        relationship set<BaiDang> cac_bai_dang inverse BaiDang::tac_gia;\n"
                        "        relationship set<BinhLuan> cac_binh_luan inverse BinhLuan::tac_gia;\n"
                        "        relationship set<NguoiDung> ds_ban_be inverse NguoiDung::ds_ban_be;\n"
                        "        void themBanBe(in NguoiDung u);\n"
                        "    };\n\n"
                        "    class BaiDang (extent dsBaiDang, key post_id) {\n"
                        "        attribute integer post_id;\n"
                        "        attribute string tieu_de;\n"
                        "        attribute string noi_dung;\n"
                        "        relationship NguoiDung tac_gia inverse NguoiDung::cac_bai_dang;\n"
                        "        relationship set<BinhLuan> cac_binh_luan inverse BinhLuan::bai_dang;\n"
                        "        void tangLuotThich();\n"
                        "    };\n\n"
                        "    class BaiThaoLuan extends BaiDang (extent dsBaiThaoLuan) {\n"
                        "        attribute boolean da_khoa;\n"
                        "        void dongThaoLuan();\n"
                        "    };\n\n"
                        "    class BaiTaiLieu extends BaiDang (extent dsBaiTaiLieu) {\n"
                        "        attribute string duong_dan_tep;\n"
                        "        attribute set<string> cac_the;\n"
                        "        void taiTepLen(in string url);\n"
                        "    };\n\n"
                        "    class BinhLuan (extent dsBinhLuan, key comment_id) {\n"
                        "        attribute integer comment_id;\n"
                        "        attribute string noi_dung;\n"
                        "        relationship NguoiDung tac_gia inverse NguoiDung::cac_binh_luan;\n"
                        "        relationship BaiDang bai_dang inverse BaiDang::cac_binh_luan;\n"
                        "        relationship BinhLuan binh_luan_cha inverse BinhLuan::cac_binh_luan_con;\n"
                        "        relationship set<BinhLuan> cac_binh_luan_con inverse BinhLuan::binh_luan_cha;\n"
                        "        set<BinhLuan> layCayCon();\n"
                        "    };\n"
                        "};",
                   "Trích đoạn Lược đồ ODL chuẩn ODMG 3.0")

    add_heading_3(doc, "5.1.2 Bộ 8 truy vấn OQL chuẩn ODMG 3.0")
    add_paragraph(doc, "Ngôn ngữ truy vấn đối tượng OQL (Object Query Language) cho phép điều hướng tự nhiên qua các mối liên kết (Path Navigation) bằng toán tử dấu chấm (.) mà không cần thực hiện các phép JOIN phức tạp:")

    oql_headers = ["Mã OQL", "Mục đích phân tích", "Câu lệnh truy vấn OQL (Chuẩn ODMG 3.0)", "Kết quả kiểm chứng"]
    oql_data = [
        ["OQL1", "Điều hướng 1-nhiều", "SELECT p.tieu_de FROM dsBaiDang p WHERE p.tac_gia.email = 'an@sgu.edu.vn'", "2 bài viết của sinh viên An."],
        ["OQL2", "Tập hợp đa trị", "SELECT u.ho_ten FROM dsNguoiDung u WHERE 'CSDLNC' IN u.mon_hoc", "Danh sách học viên theo học môn CSDLNC."],
        ["OQL3", "Truy vấn phân cấp cây", "SELECT c.noi_dung FROM dsBinhLuan c WHERE c.binh_luan_cha.comment_id = 1", "Các phản hồi trực tiếp cho bình luận gốc 1."],
        ["OQL4", "Đa hình kế thừa", "SELECT p.tieu_de FROM dsBaiDang p WHERE p IS_OF_CLASS(BaiTaiLieu)", "Lọc ra chính xác các bài viết có tệp tài liệu."],
        ["OQL5", "Hàm gộp đối tượng", "SELECT g.ten_nhom, COUNT(g.cac_thanh_vien) FROM dsNhomHocTap g", "Số lượng thành viên của từng nhóm."],
        ["OQL6", "Điều hướng sâu", "SELECT c.tac_gia.ho_ten FROM dsBaiDang p, p.cac_binh_luan c WHERE p.post_id = 1", "Tên tất cả người tham gia thảo luận bài 1."],
        ["OQL7", "Lồng đối tượng", "SELECT u.ho_ten, (SELECT b.tieu_de FROM u.cac_bai_dang b) FROM dsNguoiDung u", "Cấu trúc lồng ghép thông tin người và bài viết."],
        ["OQL8", "Lọc theo phương thức", "SELECT b.post_id FROM dsBaiThaoLuan b WHERE b.da_khoa = true", "Các chủ đề thảo luận đang bị khóa."],
    ]
    add_styled_table(doc, oql_headers, oql_data, [0.8, 1.6, 3.2, 1.8])

    add_heading_3(doc, "5.1.3 Phân tích chuyên sâu 5 khía cạnh Lệch pha trở kháng (Impedance Mismatch)")
    add_paragraph(doc, "Khi lập trình viên sử dụng các framework ORM (như Hibernate, EclipseLink, Entity Framework) để kết nối mã nguồn Java/C# với cơ sở dữ liệu quan hệ, hệ thống phải đối mặt với Hiện tượng Lệch pha trở kháng (Object-Relational Impedance Mismatch) qua 5 khía cạnh bản chất:")

    imp_headers = ["Khía cạnh lệch pha", "Mô hình Hướng đối tượng (OOP / ODL)", "Mô hình Quan hệ (RDBMS / SQL)", "Giải pháp dung hòa trong ORM / JPA"]
    imp_data = [
        ["1. Tính định danh\n(Object Identity)", "Mỗi đối tượng có một OID duy nhất trong bộ nhớ; hai đối tượng phân biệt bằng tham chiếu (u1 == u2).", "Bản ghi phân biệt bằng Khóa chính (Primary Key); không có khái niệm OID vật lý.", "Sử dụng annotation @Id và @GeneratedValue; cài đặt lại phương thức equals() và hashCode() theo khóa chính."],
        ["2. Tính đóng gói\n(Encapsulation)", "Dữ liệu được che giấu (private attributes); thao tác qua phương thức nghiệp vụ công khai (public methods).", "Dữ liệu phơi bày hoàn toàn qua các cột bảng; câu lệnh SQL có thể can thiệp trực tiếp vào từng giá trị.", "Sử dụng các getter/setter an toàn; thiết lập các Database Triggers để cưỡng chế tính toàn vẹn ở tầng máy chủ."],
        ["3. Tính kế thừa\n(Inheritance)", "Hỗ trợ tự nhiên quan hệ kế thừa IS-A, tính đa hình (Polymorphism) và ghi đè phương thức.", "Không có khái niệm kế thừa; chỉ có quan hệ liên kết bảng thông qua Khóa ngoại (Foreign Key).", "Cung cấp 3 chiến lược ánh xạ: @Inheritance(strategy = InheritanceType.SINGLE_TABLE | JOINED | TABLE_PER_CLASS)."],
        ["4. Kiểu phức hợp\n(Type Mapping)", "Hỗ trợ các kiểu dữ liệu phong phú: Set<String>, List<File>, cấu trúc lồng nhau tùy biến.", "Mô hình 1NF yêu cầu mọi thuộc tính phải là nguyên tử (Atomic); không cho phép mảng hay bảng con trong 1 ô.", "Sử dụng bảng phụ @ElementCollection @CollectionTable hoặc lưu dưới dạng cột bán cấu trúc JSONB."],
        ["5. Điều hướng quan hệ\n(Navigation vs JOIN)", "Điều hướng tự nhiên qua con trỏ tham chiếu (u.getPosts().get(0).getComments()).", "Bắt buộc phải thực hiện các phép JOIN toán học giữa các bảng dựa trên giá trị khóa chung.", "Cơ chế Lazy Loading vs Eager Loading; tiềm ẩn vấn đề hiệu năng kinh điển N+1 Selects Problem nếu cấu hình sai."],
    ]
    add_styled_table(doc, imp_headers, imp_data, [1.4, 2.0, 2.0, 2.0])

    # ========================================================
    # 5.2 CƠ SỞ DỮ LIỆU ĐỒ THỊ CHUYÊN DỤNG NEO4J
    # ========================================================
    add_heading_2(doc, "5.2 CSDL Đồ thị chuyên dụng Neo4j & Đối chiếu Cypher")
    add_paragraph(doc, "Để đánh giá toàn diện năng lực xử lý dữ liệu mạng xã hội, nhóm đã triển khai song song máy chủ Cơ sở dữ liệu đồ thị Neo4j 5.x Community trên nền tảng Docker:")
    add_bullet(doc, "Cổng 7474: Giao diện trực quan đồ thị Neo4j Browser (http://localhost:7474).")
    add_bullet(doc, "Cổng 7687: Giao thức nhị phân Bolt phục vụ kết nối ứng dụng với độ trễ tối thiểu.")
    add_bullet(doc, "Mô hình Property Graph: Các đỉnh (Nodes) có nhãn :User, :Post, :Group; các cạnh (Relationships) định kiểu :FRIEND_WITH, :FOLLOWS, :MEMBER_OF, :POSTED, :IN_GROUP mang các thuộc tính (properties) như since, role, created_at.")

    add_paragraph(doc, "Dữ liệu từ PostgreSQL được trích xuất và nạp vào Neo4j thông qua kịch bản Cypher chuẩn tắc (neo4j/cypher/import_nodes_edges.cypher), tạo nên đồ thị mạng xã hội học tập trực quan và phong phú:")

    add_figure(doc, "neo4j/screenshots/01_neo4j_full_graph.png", "Hình 5.2: Toàn cảnh Đồ thị Mạng xã hội học tập hiển thị trên Neo4j Browser (Graph View)", width_inches=6.2)

    add_heading_3(doc, "5.2.1 Hiện thực và đối chiếu 4 bài toán đồ thị trên Cypher và SQL đệ quy")
    add_paragraph(doc, "Nhóm đã hiện thực và đối soát kết quả giữa ngôn ngữ đồ thị Cypher và SQL đệ quy (WITH RECURSIVE) trên 4 bài toán cốt lõi:")

    add_paragraph(doc, "Cypher sử dụng cơ chế khớp mẫu (Pattern Matching) trực quan: MATCH (an:User {name: 'An'})-[:FRIEND_WITH]-(f:User)-[:FRIEND_WITH]-(fof:User) WHERE NOT (an)-[:FRIEND_WITH]-(fof) AND an <> fof RETURN fof.name, count(f) AS mutual_count. Kết quả trên cả hai hệ quản trị đều xác định đúng 2 bạn tiềm năng: Cúc (2 bạn chung) và Giang (1 bạn chung).", bold_prefix="Bài toán R1 - Bạn của bạn (Friends-of-Friends): ")

    add_figure(doc, "neo4j/screenshots/02_neo4j_friends_of_friends.png", "Hình 5.3: Kết quả trực quan hóa truy vấn Bạn của bạn (Friends-of-Friends) trên Neo4j Browser", width_inches=6.0)

    add_paragraph(doc, "Neo4j tích hợp sẵn thuật toán tìm đường đi ngắn nhất: MATCH (an:User {name: 'An'}), (giang:User {name: 'Giang'}), p = shortestPath((an)-[:FRIEND_WITH*]-(giang)) RETURN [n in nodes(p) | n.name] AS path, length(p) AS len. Kết quả trả về đường đi tối ưu: An -> Bình -> Giang (chiều dài 2 cạnh), hoàn toàn trùng khớp với kết quả thuật toán BFS trong PostgreSQL.", bold_prefix="Bài toán R2 - Đường đi ngắn nhất (Shortest Path): ")

    add_figure(doc, "neo4j/screenshots/03_neo4j_shortest_path.png", "Hình 5.4: Đường đi ngắn nhất giữa hai học viên An và Giang trên Neo4j Browser", width_inches=6.0)

    add_paragraph(doc, "Truy vấn chu trình trong Cypher: MATCH p = (a:User)-[:FRIEND_WITH*3..6]-(a) WHERE ALL(n IN nodes(p)[1..-1] WHERE size([m IN nodes(p) WHERE m = n]) = 1) RETURN [n in nodes(p) | n.name]. Cả hai hệ thống đều phát hiện chính xác 3 chu trình cơ bản trong mạng lưới kết bạn.", bold_prefix="Bài toán R3 - Phát hiện chu trình (Cycle Detection): ")

    add_figure(doc, "neo4j/screenshots/04_neo4j_cycle_detection.png", "Hình 5.5: Đồ thị trực quan hóa phát hiện chu trình (Cycle Detection) trên Neo4j Browser", width_inches=6.0)

    # ========================================================
    # 5.3 SO SÁNH ĐỐI CHIẾU TOÀN DIỆN POSTGRESQL VS NEO4J
    # ========================================================
    add_heading_2(doc, "5.3 So sánh đối chiếu toàn diện: PostgreSQL vs Neo4j")
    add_paragraph(doc, "Sự khác biệt cốt lõi giữa PostgreSQL và Neo4j nằm ở cơ chế duyệt liên kết ở tầng vật lý:")
    add_bullet(doc, "Neo4j sở hữu công nghệ Duyệt kề không dùng chỉ mục (Index-free Adjacency): Mỗi nút lưu trực tiếp con trỏ bộ nhớ (Physical Pointer) trỏ tới các cạnh và các nút lân cận. Việc duyệt qua một mối liên kết có độ phức tạp O(1) độc lập hoàn toàn với tổng số lượng nút trên toàn bộ đồ thị.", bold_prefix="Cơ chế của Neo4j: ")
    add_bullet(doc, "PostgreSQL không có con trỏ trực tiếp giữa các dòng; mỗi bước đệ quy (Recursive Iteration) đều phải thực hiện tìm kiếm trên cấu trúc cây chỉ mục B-Tree (Index Scan O(log N)) và ghép nối hai tập kết quả (Hash Join / Nested Loop Join). Khi độ sâu đồ thị k tăng lên, chi phí ghép nối tăng theo hàm mũ O(B^k) (với B là bậc phân nhánh).", bold_prefix="Cơ chế của PostgreSQL: ")

    neo_cmp_headers = ["Tiêu chí đánh giá", "PostgreSQL 18.6 (WITH RECURSIVE)", "Neo4j 5.x (Ngôn ngữ Cypher)", "Kết luận & Khuyến nghị kiến trúc"]
    neo_cmp_data = [
        ["Mô hình dữ liệu", "Bảng quan hệ 2 chiều (Relational Tables);\nquan hệ biểu diễn qua khóa ngoại FK.", "Đồ thị thuộc tính (Property Graph);\nĐỉnh (Node), Cạnh (Relationship), Thuộc tính.", "Neo4j trực quan và tự nhiên hơn cho dữ liệu liên kết chéo phức tạp."],
        ["Ngôn ngữ truy vấn", "SQL chuẩn tắc; sử dụng biểu thức bảng chung\nWITH RECURSIVE phức tạp, dài dòng.", "Cypher trực quan, mô phỏng hình học ASCII art\n(u)-[:FRIEND_WITH]->(v) cực kỳ ngắn gọn.", "Cypher dễ học, dễ bảo trì và ít lỗi cú pháp hơn khi viết truy vấn đồ thị."],
        ["Hiệu năng đồ thị nông\n(k = 1, 2 chặng)", "Cực nhanh (~0.05ms) nhờ chỉ mục B-Tree\nvà tối ưu hóa bộ nhớ đệm Buffer Cache.", "Rất nhanh (~0.04ms) nhờ con trỏ bộ nhớ\nIndex-free Adjacency.", "Hai hệ quản trị tương đương nhau ở đồ thị nông (bạn bè trực tiếp, bạn của bạn)."],
        ["Hiệu năng đồ thị sâu\n(k >= 3 chặng, toàn đồ thị)", "Chậm dần theo hàm mũ; tốn RAM lưu\nbảng tạm trung gian; dễ tràn bộ nhớ work_mem.", "Vẫn duy trì tốc độ cao do chỉ duyệt cục bộ\ntrên các con trỏ kề mà không quét toàn bảng.", "Neo4j vượt trội hoàn toàn khi phân tích đồ thị sâu, tìm cụm cộng đồng, lan truyền tin."],
        ["Tính toàn vẹn ACID &\nGiao dịch đồng thời", "Hoàn hảo: Hỗ trợ MVCC mạnh mẽ, các mức cô lập\nchặt chẽ (Serializable SSI), khóa dòng tinh tế.", "Hỗ trợ ACID đầy đủ cho từng cụm thao tác ghi\nnhưng cơ chế cô lập giao dịch đơn giản hơn.", "PostgreSQL an toàn và vượt trội hơn cho các giao dịch tài chính, thanh toán, điểm số."],
        ["Quản trị & Khả năng vận hành", "Rất trưởng thành (Mature), dễ sao lưu, phục hồi,\nphổ biến, tài nguyên dồi dào, chi phí thấp.", "Đòi hỏi chuyên môn quản trị đồ thị riêng biệt;\nchi phí bản quyền Enterprise cao.", "PostgreSQL dễ vận hành hơn trong hạ tầng doanh nghiệp hiện có."],
    ]
    add_styled_table(doc, neo_cmp_headers, neo_cmp_data, [1.4, 1.8, 1.8, 1.8])

    add_callout_box(doc, "KHUYẾN NGHỊ KIẾN TRÚC THỰC TẾ: MÔ HÌNH ĐA LƯU TRỮ (POLYGLOT PERSISTENCE)\n"
                         "Trong các hệ thống EdTech và mạng xã hội thực tế quy mô lớn, kiến trúc tối ưu không phải là thay thế hoàn toàn PostgreSQL bằng Neo4j, mà là kết hợp sức mạnh của cả hai:\n"
                         "• PostgreSQL đóng vai trò Nguồn dữ liệu tin cậy duy nhất (Single Source of Truth): Lưu trữ tài khoản người dùng, bài giảng, kết quả thi, thanh toán học phí và các chuỗi bình luận phân cấp (sử dụng Path Enumeration ltree).\n"
                         "• Neo4j đóng vai trò Cơ sở dữ liệu chuyên biệt phục vụ phân tích mạng xã hội (Graph Engine): Đồng bộ dữ liệu quan hệ bạn bè, tương tác học nhóm thông qua cơ chế CDC (Change Data Capture / Debezium / Kafka) để giải quyết các tác vụ gợi ý môn học, phát hiện nhóm học tập đồng đẳng và đề xuất lộ trình học tập thích ứng.",
                    "ĐỀ XUẤT KIẾN TRÚC ĐA MÔ HÌNH (POLYGLOT PERSISTENCE ARCHITECTURE)")

    doc.add_page_break()
