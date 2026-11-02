"""
Chương 3: Dữ liệu phân cấp (Cây) trên Cơ sở dữ liệu quan hệ (4 Mô hình lưu trữ).
"""

from docx import Document
from .styles import (
    add_heading_1, add_heading_2, add_heading_3,
    add_paragraph, add_bullet, add_styled_table, add_code_block, add_callout_box
)

def build_ch3(doc: Document):
    add_heading_1(doc, "CHƯƠNG 3: DỮ LIỆU PHÂN CẤP (CÂY) TRÊN CƠ SỞ DỮ LIỆU QUAN HỆ")

    # --- 3.1 CƠ SỞ LÝ THUYẾT VÀ CẤU TRÚC 4 MÔ HÌNH ---
    add_heading_2(doc, "3.1 Cơ sở lý thuyết và cấu trúc lưu trữ của 4 mô hình cây")
    add_paragraph(doc, "Mô hình quan hệ (Relational Model) truyền thống dựa trên đại số tập hợp phẳng và không hỗ trợ tự nhiên các cấu trúc dữ liệu đệ quy dạng cây (Hierarchical Trees). Để quản lý chuỗi thảo luận lồng nhau vô hạn cấp (Nested Comments) trong mạng xã hội học tập, nhóm nghiên cứu đã triển khai, đo đạc và đánh giá 4 mô hình lưu trữ kinh điển:")

    add_bullet(doc, "Mỗi dòng lưu một con trỏ tham chiếu đến nút cha trực tiếp (parent_id INT REFERENCES comment_adjacency(comment_id)). Nút gốc có parent_id = NULL. Đây là mô hình tự nhiên và trực quan nhất.", bold_prefix="1. Danh sách kề (Adjacency List): ")
    add_bullet(doc, "Lưu trữ toàn bộ chuỗi đường dẫn từ gốc đến nút hiện tại dưới dạng kiểu dữ liệu chuyên dụng ltree trong PostgreSQL (ví dụ: '1.3.5.7'). Mô hình này tận dụng cơ chế khớp mẫu tiền tố và cấu trúc chỉ mục GiST nâng cao.", bold_prefix="2. Liệt kê đường dẫn (Path Enumeration / ltree): ")
    add_bullet(doc, "Biểu diễn cây dưới dạng các khoảng lồng nhau theo thứ tự duyệt trước (Pre-order Traversal). Mỗi nút lưu hai số nguyên (lft, rgt). Mọi hậu duệ của nút X đều có giá trị lft nằm trong khoảng giữa lft và rgt của X (lft_X < lft_descendant < rgt_descendant < rgt_X).", bold_prefix="3. Tập lồng (Nested Set): ")
    add_bullet(doc, "Tách biệt hoàn toàn bảng dữ liệu thực thể và cấu trúc phân cấp. Cấu trúc cây được lưu trong một bảng phụ riêng biệt comment_closure(ancestor_id, descendant_id, depth), lưu trữ toàn bộ các cặp quan hệ tổ tiên - hậu duệ khả dĩ trong cây (kể cả quan hệ phản xạ depth = 0).", bold_prefix="4. Bảng bao đóng (Closure Table): ")

    add_paragraph(doc, "Để minh họa sự khác biệt về cấu trúc dữ liệu, bảng dưới đây thể hiện cách biểu diễn của một cây bình luận mẫu gồm 6 nút (c1 là gốc; c2, c3 trả lời c1; c4 trả lời c2; c5, c6 trả lời c3):")

    tree_struct_headers = ["ID", "Nội dung", "1. Adjacency List\n(parent_id)", "2. Path Enum\n(path ltree)", "3. Nested Set\n(lft, rgt)", "4. Closure Table\n(ancestor, descendant, depth)"]
    tree_struct_data = [
        ["c1", "Bình luận gốc bài viết", "NULL", "'1'", "(1, 12)", "(1,1,0)"],
        ["c2", "Trả lời bình luận c1", "1", "'1.2'", "(2, 5)", "(1,2,1), (2,2,0)"],
        ["c4", "Trả lời bình luận c2", "2", "'1.2.4'", "(3, 4)", "(1,4,2), (2,4,1), (4,4,0)"],
        ["c3", "Trả lời bình luận c1", "1", "'1.3'", "(6, 11)", "(1,3,1), (3,3,0)"],
        ["c5", "Trả lời bình luận c3", "3", "'1.3.5'", "(7, 8)", "(1,5,2), (3,5,1), (5,5,0)"],
        ["c6", "Trả lời bình luận c3", "3", "'1.3.6'", "(9, 10)", "(1,6,2), (3,6,1), (6,6,0)"],
    ]
    add_styled_table(doc, tree_struct_headers, tree_struct_data, [0.6, 1.8, 1.1, 1.1, 1.0, 1.6])

    add_heading_3(doc, "3.1.1 Bảng dùng chung và chỉ mục chuyên biệt cho từng mô hình")
    add_paragraph(doc, "Cả 4 mô hình đều dùng chung các bảng nghiệp vụ nền tảng: users, study_group, post. Tuy nhiên, ở tầng lưu trữ cây bình luận và thiết kế vật lý, mỗi mô hình đòi hỏi các chỉ mục chuyên biệt để đạt hiệu năng tối đa:")

    index_spec_headers = ["Mô hình cây", "Bảng lưu trữ chính", "Chỉ mục chuyên biệt bắt buộc", "Mục đích tối ưu hóa"]
    index_spec_data = [
        ["Adjacency List", "comment_adjacency", "CREATE INDEX idx_adj_parent ON comment_adjacency(parent_id);", "Tối ưu hóa phép JOIN đệ quy CTE tìm các nút con."],
        ["Path Enumeration", "comment_path_enum", "CREATE INDEX idx_path_gist ON comment_path_enum USING GIST (path);", "Tối ưu hóa các toán tử khớp mẫu tiền tố <@ (con) và @> (cha)."],
        ["Nested Set", "comment_nested_set", "CREATE INDEX idx_ns_lft_rgt ON comment_nested_set(lft, rgt);", "Tối ưu hóa các phép quét tìm cây con theo khoảng BETWEEN lft AND rgt."],
        ["Closure Table", "comment_closure\n(bảng phụ liên kết)", "CREATE UNIQUE INDEX idx_cl_pair ON comment_closure(ancestor_id, descendant_id);\nCREATE INDEX idx_cl_desc ON comment_closure(descendant_id);", "Tối ưu hóa truy vấn tìm cây con qua ancestor_id và tìm đường dẫn tổ tiên qua descendant_id."],
    ]
    add_styled_table(doc, index_spec_headers, index_spec_data, [1.3, 1.6, 2.5, 1.8])

    # --- 3.2 HIỆN THỰC BỘ 10 TRUY VẤN VÀ CRUD ---
    add_heading_2(doc, "3.2 Quy ước thống nhất (Ground Truth Rules) & Hiện thực bộ 10 truy vấn chuẩn (Q1–Q10)")
    add_paragraph(doc, "Để đảm bảo tính khách quan và khoa học khi đánh giá đối sánh, nhóm thiết lập Quy ước Chuẩn tắc Thống nhất (Ground Truth Rules) áp dụng đồng bộ trên toàn bộ 4 mô hình:")
    add_bullet(doc, "Subtree (Truy vấn Q2 và Q8): Cây con của một nút X BẮT BUỘC BAO GỒM CHÍNH NÚT X (tức là nút X được tính là gốc của cây con đó).", bold_prefix="Quy tắc 1 (Subtree inclusiveness): ")
    add_bullet(doc, "Strict Ancestor (Truy vấn Q3 và Q10): Đường dẫn tổ tiên của nút X KHÔNG BAO GỒM CHÍNH NÚT X (chỉ bao gồm cha, ông,... của X).", bold_prefix="Quy tắc 2 (Strict ancestor): ")
    add_bullet(doc, "Độ sâu (Depth) của nút gốc (Root) được quy ước là 1 (Depth = 1). Mức thụt đầu dòng (Indent Level) của nút gốc được quy ước là 0 (Level = 0).", bold_prefix="Quy tắc 3 (Root depth & indent): ")

    add_paragraph(doc, "Dưới đây là bảng tổng hợp đặc tả bộ 10 truy vấn chuẩn Q1 – Q10 và 3 thao tác CRUD trên 4 mô hình:")

    q_spec_headers = ["Mã Q", "Tên truy vấn chuẩn", "Đặc tả nghiệp vụ", "Kỹ thuật giải quyết trên 4 mô hình"]
    q_spec_data = [
        ["Q1", "Duyệt toàn bộ cây", "Lấy toàn cây bài viết theo thứ tự hiển thị kèm thụt lề.", "Adjacency dùng CTE đệ quy; Path dùng ORDER BY path; Nested Set dùng ORDER BY lft; Closure dùng đệ quy hoặc kết hợp bảng chính."],
        ["Q2", "Lấy toàn bộ cây con", "Lấy bình luận X và toàn bộ phản hồi dưới nó.", "Adjacency dùng CTE đệ quy; Path dùng path <@ 'path_X'; Nested Set dùng lft BETWEEN p_lft AND p_rgt; Closure dùng ancestor_id = X."],
        ["Q3", "Lấy đường dẫn tổ tiên", "Lấy chuỗi bình luận cha dẫn tới bình luận X.", "Adjacency dùng CTE đệ quy ngược; Path dùng path @> 'path_X'; Nested Set dùng lft < p_lft AND rgt > p_rgt; Closure dùng descendant_id = X."],
        ["Q4", "Tính độ sâu nút", "Xác định cấp bậc phân cấp của bình luận X (Gốc = 1).", "Adjacency đếm số vòng đệ quy; Path dùng nlevel(path); Nested Set đếm số khoảng cha bao bọc; Closure dùng MAX(depth) + 1."],
        ["Q5", "Lấy các nút lá", "Tìm các bình luận không có bất kỳ phản hồi nào.", "Adjacency dùng NOT EXISTS; Path dùng NOT EXISTS khớp tiền tố; Nested Set dùng rgt = lft + 1; Closure dùng NOT EXISTS con."],
        ["Q6", "Đếm số con trực tiếp", "Đếm số lượng phản hồi cấp 1 của bình luận X.", "Adjacency đếm WHERE parent_id = X; Path dùng nlevel(path) = nlevel(path_X) + 1; Nested Set đếm con trực tiếp; Closure dùng WHERE depth = 1."],
        ["Q7", "Lấy các con trực tiếp", "Liệt kê danh sách các phản hồi cấp 1 của X.", "Tương tự Q6 nhưng trả về chi tiết các cột dữ liệu thay vì hàm COUNT()."],
        ["Q8", "Đếm tổng số hậu duệ", "Đếm tổng số phản hồi trong toàn bộ cây con của X.", "Adjacency dùng CTE COUNT; Path dùng COUNT với toán tử <@; Nested Set tính nhanh bằng công thức (rgt - lft + 1) / 2; Closure COUNT(*) với ancestor_id = X."],
        ["Q9", "Lấy nút cha trực tiếp", "Tìm bình luận cha trực tiếp của bình luận X.", "Adjacency lấy parent_id; Path dùng subpath(path, 0, nlevel-1); Nested Set tìm khoảng cha nhỏ nhất; Closure dùng descendant = X AND depth = 1."],
        ["Q10", "Kiểm tra tổ tiên - con", "Kiểm tra bình luận A có phải là tổ tiên của B hay không.", "Adjacency dùng CTE lặp; Path dùng path_A @> path_B; Nested Set kiểm tra lft_A < lft_B AND rgt_A > rgt_B; Closure kiểm tra EXISTS(A, B)."],
        ["C1", "Thêm nút lá mới", "Chèn một phản hồi mới vào dưới bình luận cha X.", "Adjacency: INSERT đơn giản; Path: lấy path cha và nối thêm ID; Nested Set: dịch chuyển cập nhật toàn cây; Closure: chèn các cặp tổ tiên."],
        ["C2", "Di chuyển nhánh cây", "Chuyển một bình luận con và toàn bộ cây con sang cha mới.", "Adjacency: UPDATE 1 dòng parent_id; Path: đổi chuỗi tiền tố; Nested Set: tính offset và dịch chuyển phức tạp; Closure: xóa và chèn lại các cặp."],
        ["C3", "Xóa nhánh cây con", "Xóa một bình luận và toàn bộ các phản hồi con cháu.", "Adjacency: DELETE CASCADE hoặc CTE; Path: DELETE với <@; Nested Set: DELETE BETWEEN và thu hẹp khoảng; Closure: DELETE cặp liên kết."],
    ]
    add_styled_table(doc, q_spec_headers, q_spec_data, [0.6, 1.4, 2.2, 3.0])

    # --- MINH HỌA MÃ LỆNH Q2 TIÊU BIỂU ---
    add_paragraph(doc, "Minh họa câu lệnh SQL thực thi truy vấn Q2 (Lấy toàn bộ cây con của bình luận id = 2) trên 4 mô hình:", bold_prefix="Minh họa hiện thực truy vấn Q2: ")

    add_code_block(doc, "-- [1] ADJACENCY LIST (Dùng CTE đệ quy WITH RECURSIVE):\n"
                        "WITH RECURSIVE subtree AS (\n"
                        "    SELECT comment_id, parent_id, content, 1 AS depth\n"
                        "    FROM comment_adjacency WHERE comment_id = 2\n"
                        "    UNION ALL\n"
                        "    SELECT c.comment_id, c.parent_id, c.content, s.depth + 1\n"
                        "    FROM comment_adjacency c JOIN subtree s ON c.parent_id = s.comment_id\n"
                        ")\n"
                        "SELECT * FROM subtree;\n\n"
                        "-- [2] PATH ENUMERATION (Dùng toán tử ltree <@):\n"
                        "SELECT comment_id, path, content\n"
                        "FROM comment_path_enum\n"
                        "WHERE path <@ (SELECT path FROM comment_path_enum WHERE comment_id = 2);\n\n"
                        "-- [3] NESTED SET (Dùng phép so sánh khoảng lft BETWEEN):\n"
                        "SELECT child.comment_id, child.lft, child.rgt, child.content\n"
                        "FROM comment_nested_set child, comment_nested_set parent\n"
                        "WHERE parent.comment_id = 2 AND child.lft BETWEEN parent.lft AND parent.rgt;\n\n"
                        "-- [4] CLOSURE TABLE (Dùng JOIN trực tiếp bảng bao đóng):\n"
                        "SELECT c.comment_id, c.content, cl.depth\n"
                        "FROM comment_closure cl\n"
                        "JOIN comment_closure_data c ON cl.descendant_id = c.comment_id\n"
                        "WHERE cl.ancestor_id = 2;",
                   "So sánh cú pháp SQL truy vấn Q2 trên 4 mô hình")

    # --- 3.3 KIỂM THỬ TÍNH ĐÚNG ĐẮN VÀ SO SÁNH ---
    add_heading_2(doc, "3.3 Kiểm thử tính đúng đắn logic và Ma trận đối chiếu toàn diện")
    add_paragraph(doc, "Nhóm đã tiến hành kiểm chứng tự động toàn bộ 10 truy vấn Q1–Q10 và 3 phép thử CRUD trên tập dữ liệu chuẩn seed_test.sql. Kết quả đối soát xác nhận cả 4 mô hình đều trả về kết quả 100% đồng nhất và hoàn toàn khớp với Ground Truth:")

    val_headers = ["Phép thử", "Mục tiêu kiểm chứng", "Kết quả chuẩn kỳ vọng", "Adjacency", "Path Enum", "Nested Set", "Closure"]
    val_rows = [
        ["Q1", "Duyệt toàn bộ cây", "6 nút theo đúng thứ tự phân cấp", "Đạt", "Đạt", "Đạt", "Đạt"],
        ["Q2 (id=2)", "Cây con của c2", "{c2, c4} (bao gồm chính nó)", "Đạt", "Đạt", "Đạt", "Đạt"],
        ["Q2 (id=3)", "Cây con của c3", "{c3, c5, c6} (bao gồm chính nó)", "Đạt", "Đạt", "Đạt", "Đạt"],
        ["Q3 (id=4)", "Tổ tiên của c4", "{c1, c2} (không chứa c4)", "Đạt", "Đạt", "Đạt", "Đạt"],
        ["Q4 (id=1)", "Độ sâu nút gốc c1", "Depth = 1", "Đạt", "Đạt", "Đạt", "Đạt"],
        ["Q4 (id=4)", "Độ sâu nút lá c4", "Depth = 3", "Đạt", "Đạt", "Đạt", "Đạt"],
        ["Q5", "Danh sách nút lá", "{c4, c5, c6}", "Đạt", "Đạt", "Đạt", "Đạt"],
        ["Q6 (id=3)", "Số con trực tiếp c3", "2 (c5 và c6)", "Đạt", "Đạt", "Đạt", "Đạt"],
        ["Q8 (id=1)", "Tổng số hậu duệ c1", "6 (toàn bộ cây)", "Đạt", "Đạt", "Đạt", "Đạt"],
        ["Q9 (id=4)", "Nút cha của c4", "c2", "Đạt", "Đạt", "Đạt", "Đạt"],
        ["Q10 (1, 4)", "c1 có là tổ tiên c4?", "TRUE", "Đạt", "Đạt", "Đạt", "Đạt"],
    ]
    add_styled_table(doc, val_headers, val_rows, [0.8, 1.8, 2.0, 0.6, 0.6, 0.6, 0.6])

    add_paragraph(doc, "Bảng tổng hợp so sánh độ phức tạp thuật toán (Big-O Complexity) và đặc tính kỹ thuật:")

    bigo_headers = ["Tiêu chí kỹ thuật", "Adjacency List", "Path Enumeration (ltree)", "Nested Set", "Closure Table"]
    bigo_rows = [
        ["Đọc toàn bộ cây (Q1)", "O(N) (Cần CTE đệ quy)", "O(N log N) (Chỉ cần ORDER BY)", "O(N) (Quét theo thứ tự lft)", "O(N) (JOIN bảng phụ)"],
        ["Đọc cây con (Q2)", "O(K) (Đệ quy K vòng lặp)", "O(log N + K) (Chỉ mục GiST)", "O(log N + K) (Khoảng BETWEEN)", "O(log N + K) (Phép JOIN đơn giản)"],
        ["Đọc đường dẫn tổ tiên (Q3)", "O(D) (D là độ sâu cây)", "O(log N + D) (Toán tử @>)", "O(log N + D) (Khoảng bao bọc)", "O(log N + D) (JOIN descendant)"],
        ["Thêm nút lá mới (Insert)", "O(1) (Cực nhanh, chèn 1 dòng)", "O(1) (Lấy path cha + nối chuỗi)", "O(N) (Phải dịch chuyển lft, rgt)", "O(D) (Chèn D+1 cặp quan hệ)"],
        ["Di chuyển nhánh cây (Move)", "O(1) (UPDATE 1 dòng parent_id)", "O(K) (Đổi tiền tố chuỗi ltree)", "O(N) (Tính offset & tái cấu trúc)", "O(K × D) (Xóa & chèn lại cặp)"],
        ["Xóa nhánh cây con (Delete)", "O(1) (với CASCADE) hoặc O(K)", "O(K) (DELETE với toán tử <@)", "O(N) (Thu hẹp khoảng trống)", "O(K × D) (Xóa liên kết)"],
        ["Chi phí dung lượng lưu trữ", "Thấp nhất: O(N) (1 cột INT)", "Thấp: O(N) (Chuỗi ltree)", "Thấp: O(N) (2 cột INT lft, rgt)", "Cao nhất: O(N^2) (Bảng phụ O(N·D))"],
        ["Mức độ phức tạp cài đặt", "Rất đơn giản, trực quan", "Trung bình (cần extension ltree)", "Rất phức tạp khi cập nhật ghi", "Trung bình (cần trigger duy trì)"],
    ]
    add_styled_table(doc, bigo_headers, bigo_rows, [1.6, 1.4, 1.4, 1.4, 1.4])

    add_callout_box(doc, "KHUYẾN NGHỊ KIẾN TRÚC CHO THỰC TẾ:\n"
                         "1. Nếu ứng dụng có tỷ lệ Ghi cao hoặc cần di chuyển nhánh cây linh hoạt: Chọn ADJACENCY LIST (chi phí ghi O(1), không lo khóa bảng).\n"
                         "2. Nếu hệ thống mạng xã hội đọc Feed áp đảo (Read-heavy) và chạy trên PostgreSQL: Chọn PATH ENUMERATION (ltree) kết hợp chỉ mục GiST, đây là sự cân bằng hoàn hảo nhất giữa tốc độ đọc cực nhanh và chi phí ghi chấp nhận được mà không làm bùng nổ dung lượng đĩa như Closure Table.\n"
                         "3. Nếu cây dữ liệu tĩnh, hiếm khi cập nhật (như danh mục phân loại): NESTED SET là lựa chọn tối ưu.\n"
                         "4. Nếu cây có độ sâu hữu hạn nhỏ và yêu cầu tốc độ đọc tức thì bằng các phép JOIN phẳng: CLOSURE TABLE là lựa chọn thích hợp.",
                    "KHUYẾN NGHỊ LỰA CHỌN MÔ HÌNH LƯU TRỮ PHÂN CẤP")

    doc.add_page_break()
