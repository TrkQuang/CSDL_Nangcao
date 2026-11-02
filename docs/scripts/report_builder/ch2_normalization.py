"""
Chương 2: Lý thuyết phụ thuộc hàm, Thuật toán chuẩn hóa và Phi chuẩn hóa có kiểm soát.
"""

from docx import Document
from .styles import (
    add_heading_1, add_heading_2, add_heading_3,
    add_paragraph, add_bullet, add_styled_table, add_code_block, add_callout_box
)

def build_ch2(doc: Document):
    add_heading_1(doc, "CHƯƠNG 2: LÝ THUYẾT PHỤ THUỘC HÀM & CHUẨN HÓA DỮ LIỆU")

    # --- 2.1 LƯỢC ĐỒ PHẲNG BAN ĐẦU VÀ CÁC DỊ THƯỜNG ---
    add_heading_2(doc, "2.1 Lược đồ quan hệ phẳng tổng hợp ban đầu và các dị thường")
    add_paragraph(doc, "Một cách tiếp cận ngây thơ khi thiết kế cơ sở dữ liệu là gộp toàn bộ các thuộc tính của người dùng, bài viết, nhóm học tập và bình luận vào trong một bảng phẳng duy nhất (Universal Relation Scheme). Giả sử hệ thống lưu trữ toàn bộ dữ liệu thảo luận trong lược đồ phẳng R như sau:")

    add_code_block(doc, "R = { comment_id, post_id, group_id, group_name, group_topic,\n"
                        "      author_id, author_name, author_email, comment_content,\n"
                        "      comment_created_at, post_title, post_content, post_created_at }",
                   "Lược đồ quan hệ phẳng tổng hợp ban đầu (Universal Relation R)")

    add_paragraph(doc, "Lược đồ phẳng R bộc lộ 4 vấn đề dị thường dữ liệu (Anomalies) và dư thừa nghiêm trọng:")
    add_bullet(doc, "Không thể thêm một thành viên mới (author_id) vào hệ thống nếu người đó chưa từng đăng bất kỳ bài viết nào hoặc chưa từng viết bình luận nào. Tương tự, không thể tạo một nhóm học tập mới (group_id) nếu nhóm đó chưa có bài đăng và bình luận (do comment_id không được phép mang giá trị NULL khi đóng vai trò định danh).", bold_prefix="1. Dị thường Thêm (Insertion Anomaly): ")
    add_bullet(doc, "Nếu một bài viết chỉ có duy nhất một bình luận, và bình luận đó bị xóa bỏ khỏi hệ thống, toàn bộ thông tin về bài viết (post_id, title, content), thông tin nhóm học tập (group_id, name) và thông tin tác giả bài viết sẽ bị xóa sạch khỏi cơ sở dữ liệu theo dòng bình luận đó.", bold_prefix="2. Dị thường Xóa (Deletion Anomaly): ")
    add_bullet(doc, "Khi một nhóm học tập đổi tên hoặc cập nhật chủ đề, hệ thống bắt buộc phải quét và cập nhật hàng ngàn, thậm chí hàng triệu dòng bình luận thuộc nhóm đó. Nếu xảy ra sự cố gián đoạn giữa chừng, dữ liệu sẽ rơi vào trạng thái bất nhất quán (Inconsistent State): cùng một mã nhóm group_id nhưng các dòng khác nhau lại chứa các tên nhóm khác nhau.", bold_prefix="3. Dị thường Sửa (Update Anomaly): ")
    add_bullet(doc, "Thông tin tác giả (author_name, email), thông tin bài đăng (title, content) và thông tin nhóm bị lặp đi lặp lại vô số lần trên mỗi dòng bình luận, gây lãng phí dung lượng đĩa và chiếm dụng tài nguyên bộ nhớ đệm (Buffer Cache) một cách không cần thiết.", bold_prefix="4. Dư thừa Dữ liệu (Data Redundancy): ")

    # --- 2.2 TẬP PHỤ THUỘC HÀM HỢP LỆ THEO NGHIỆP VỤ ---
    add_heading_2(doc, "2.2 Tập phụ thuộc hàm hợp lệ theo nghiệp vụ (F)")
    add_paragraph(doc, "Để chuẩn hóa lược đồ R một cách khoa học, nhóm xác định tập phụ thuộc hàm F phản ánh chính xác các quy tắc nghiệp vụ thực tế của mạng xã hội học tập:")

    fd_table_data = [
        ["Ký hiệu FD", "Biểu thức Phụ thuộc hàm", "Bản chất ngữ nghĩa nghiệp vụ"],
        ["FD1", "comment_id → post_id", "Mỗi bình luận thuộc về duy nhất một bài đăng."],
        ["FD2", "comment_id → author_id", "Mỗi bình luận do duy nhất một tác giả viết."],
        ["FD3", "comment_id → comment_content", "Mỗi bình luận có nội dung xác định tại thời điểm tạo."],
        ["FD4", "comment_id → comment_created_at", "Mỗi bình luận có thời điểm tạo duy nhất."],
        ["FD5", "post_id → group_id", "Mỗi bài viết thuộc về duy nhất một nhóm học tập."],
        ["FD6", "post_id → author_id", "Mỗi bài viết do duy nhất một tác giả sáng tạo."],
        ["FD7", "post_id → post_title", "Mỗi bài viết có một tiêu đề xác định."],
        ["FD8", "post_id → post_content", "Mỗi bài viết có một nội dung bài đăng xác định."],
        ["FD9", "post_id → post_created_at", "Mỗi bài viết có thời điểm đăng bài xác định."],
        ["FD10", "group_id → group_name", "Mỗi nhóm học tập có một tên gọi duy nhất."],
        ["FD11", "group_id → group_topic", "Mỗi nhóm học tập có một chủ đề học tập xác định."],
        ["FD12", "author_id → author_name", "Mỗi mã người dùng định danh duy nhất một họ tên."],
        ["FD13", "author_id → author_email", "Mỗi mã người dùng gắn liền với một email cá nhân."],
        ["FD14", "author_email → author_id", "Email là duy nhất, định danh ngược lại một người dùng."],
        ["FD15", "author_email → author_name", "Email xác định duy nhất họ tên của người dùng."],
    ]
    add_styled_table(doc, fd_table_data[0], fd_table_data[1:], [1.2, 2.8, 3.2])

    # --- 2.3 THUẬT TOÁN BAO ĐÓNG VÀ TÌM KHÓA ỨNG VIÊN ---
    add_heading_2(doc, "2.3 Thuật toán bao đóng thuộc tính và tìm khóa ứng viên")
    add_paragraph(doc, "Cơ sở toán học: Dựa trên Hệ tiên đề Armstrong (Armstrong's Axioms) gồm 3 luật suy dẫn tiên đề: Phản xạ (Reflexivity: Y ⊆ X ⇒ X → Y), Tăng trưởng (Augmentation: X → Y ⇒ XZ → YZ), Bắc cầu (Transitivity: X → Y ∧ Y → Z ⇒ X → Z) và 3 luật dẫn xuất: Hợp (Union), Phân rã (Decomposition), Giả bắc cầu (Pseudotransitivity).")
    
    add_paragraph(doc, "Thuật toán tính bao đóng thuộc tính X+ dưới tập phụ thuộc hàm F được thực hiện theo mã giả sau:", bold_prefix="Mã giả thuật toán CLOSURE(X, F):")
    add_code_block(doc, "Input: Tập thuộc tính X, Tập phụ thuộc hàm F\n"
                        "Output: Bao đóng X+\n"
                        "1. X+ := X;\n"
                        "2. repeat\n"
                        "3.    old_X := X+;\n"
                        "4.    for each (Y -> Z) in F do\n"
                        "5.       if Y ⊆ X+ then\n"
                        "6.          X+ := X+ ∪ Z;\n"
                        "7. until (X+ = old_X);\n"
                        "8. return X+;", "Thuật toán CLOSURE tính bao đóng thuộc tính")

    add_paragraph(doc, "Phân loại các thuộc tính của lược đồ phẳng R thành 4 tập phụ thuộc:", bold_prefix="Phân tích vị trí thuộc tính trong F: ")
    add_bullet(doc, "comment_id (Chỉ xuất hiện ở vế trái của các FD, không bao giờ xuất hiện ở vế phải).", bold_prefix="Tập L (Left only): ")
    add_bullet(doc, "group_name, group_topic, comment_content, comment_created_at, post_title, post_content, post_created_at (Chỉ xuất hiện ở vế phải, không bao giờ suy dẫn ra thuộc tính khác).", bold_prefix="Tập R (Right only): ")
    add_bullet(doc, "post_id, group_id, author_id, author_name, author_email (Xuất hiện ở cả vế trái và vế phải).", bold_prefix="Tập B (Both Left & Right): ")
    add_bullet(doc, "Rỗng (Mọi thuộc tính đều tham gia vào tập F).", bold_prefix="Tập N (Neither): ")

    add_paragraph(doc, "Theo định lý phân loại thuộc tính: Tập L bắt buộc phải thuộc về mọi khóa ứng viên của lược đồ R. Do đó, ta tính bao đóng của tập L = {comment_id}:")
    add_bullet(doc, "Khởi tạo: X+ = {comment_id}")
    add_bullet(doc, "Áp dụng FD1, FD2, FD3, FD4: X+ = {comment_id, post_id, author_id, comment_content, comment_created_at}")
    add_bullet(doc, "Áp dụng FD5, FD6, FD7, FD8, FD9 (vì post_id ∈ X+): X+ = X+ ∪ {group_id, post_title, post_content, post_created_at}")
    add_bullet(doc, "Áp dụng FD10, FD11 (vì group_id ∈ X+): X+ = X+ ∪ {group_name, group_topic}")
    add_bullet(doc, "Áp dụng FD12, FD13 (vì author_id ∈ X+): X+ = X+ ∪ {author_name, author_email}")
    add_bullet(doc, "Kết quả: {comment_id}+ = R (Toàn bộ tập thuộc tính của lược đồ quan hệ phẳng).")

    add_callout_box(doc, "Kết luận toán học: Vì {comment_id}+ = R và không có tập con thực sự nào của {comment_id} có thể tạo thành siêu khóa, suy ra K = {comment_id} là KHÓA ỨNG VIÊN DUY NHẤT (Candidate Key) của lược đồ phẳng R.", "KẾT QUẢ TÌM KHÓA ỨNG VIÊN")

    # --- 2.4 THUẬT TOÁN TÌM PHỦ TỐI TIỂU ---
    add_heading_2(doc, "2.4 Thuật toán tìm phủ tối tiểu (F_min)")
    add_paragraph(doc, "Tập phụ thuộc hàm F ban đầu có thể chứa các phụ thuộc dư thừa hoặc các thuộc tính dư thừa. Để làm cơ sở cho thuật toán phân rã 3NF tối ưu, ta tiến hành tìm phủ tối tiểu F_min qua 3 bước chặt chẽ:")
    
    add_paragraph(doc, "Mọi FD trong F đã có vế phải gồm đúng một thuộc tính đơn (được biểu diễn từ FD1 đến FD15).", bold_prefix="Bước 1 (Chuẩn hóa vế phải): ")
    add_paragraph(doc, "Mọi vế trái của các FD trong F đều chỉ gồm 1 thuộc tính đơn (comment_id, post_id, group_id, author_id, author_email). Do đó, vế trái không chứa bất kỳ thuộc tính dư thừa nào.", bold_prefix="Bước 2 (Loại bỏ thuộc tính dư thừa vế trái): ")
    add_paragraph(doc, "Lần lượt xét từng phụ thuộc hàm X → Y trong F, tạm thời loại bỏ nó ra khỏi tập F để được tập F', sau đó kiểm tra xem Y có còn thuộc về bao đóng X+ tính theo F' hay không. Nếu Y ∈ (X+)F', chứng tỏ phụ thuộc hàm đó bị dư thừa và có thể loại bỏ vĩnh viễn.", bold_prefix="Bước 3 (Loại bỏ phụ thuộc hàm dư thừa): ")

    add_bullet(doc, "Xét FD15: author_email → author_name. Tạm bỏ FD15. Tính (author_email)+ dưới F':\n"
                    "  - Theo FD14: author_email → author_id ⇒ X+ = {author_email, author_id}.\n"
                    "  - Theo FD12: author_id → author_name ⇒ X+ = {author_email, author_id, author_name}.\n"
                    "  - Nhận thấy author_name ∈ (author_email)+ ⇒ FD15 BỊ DƯ THỪA và được loại bỏ!")
    add_bullet(doc, "Xét FD6: post_id → author_id và FD2: comment_id → author_id. Tạm bỏ FD2. Tính (comment_id)+ dưới F':\n"
                    "  - Theo FD1: comment_id → post_id ⇒ X+ = {comment_id, post_id}.\n"
                    "  - Theo FD6: post_id → author_id ⇒ X+ = {comment_id, post_id, author_id}.\n"
                    "  - Nhận thấy author_id ∈ (comment_id)+ ⇒ FD2 là phụ thuộc bắc cầu thông qua post_id. Tuy nhiên, theo nghiệp vụ: Tác giả của bình luận có thể KHÁC tác giả của bài viết (người khác vào bình luận). Do đó, trong lược đồ phân rã, ta phân biệt comment_author_id và post_author_id. Đối với R, FD2 là cần thiết để xác định tác giả bình luận.")

    add_paragraph(doc, "Sau khi loại bỏ phụ thuộc dư thừa FD15, tập phủ tối tiểu F_min thu được gồm 14 phụ thuộc hàm độc lập:")
    add_code_block(doc, "F_min = {\n"
                        "  comment_id -> post_id,           comment_id -> author_id,\n"
                        "  comment_id -> comment_content,   comment_id -> comment_created_at,\n"
                        "  post_id -> group_id,             post_id -> author_id,\n"
                        "  post_id -> post_title,           post_id -> post_content,\n"
                        "  post_id -> post_created_at,\n"
                        "  group_id -> group_name,          group_id -> group_topic,\n"
                        "  author_id -> author_name,        author_id -> author_email,\n"
                        "  author_email -> author_id\n"
                        "}", "Tập phủ tối tiểu F_min hoàn chỉnh")

    # --- 2.5 PHÂN RÃ 3NF VÀ KIỂM TRA BCNF ---
    add_heading_2(doc, "2.5 Phân rã 3NF (Thuật toán Bernstein) & Kiểm tra BCNF")
    add_paragraph(doc, "Áp dụng thuật toán tổng hợp Bernstein (Bernstein's Synthesis Algorithm) trên tập phủ tối tiểu F_min:")
    add_bullet(doc, "Nhóm 1 (Cùng vế trái group_id): Tạo quan hệ R_group = { group_id, group_name, group_topic }. Khóa chính: group_id.")
    add_bullet(doc, "Nhóm 2 (Cùng vế trái author_id & author_email): Tạo quan hệ R_user = { author_id, author_email, author_name }. Khóa chính: author_id (author_email là khóa ứng viên).")
    add_bullet(doc, "Nhóm 3 (Cùng vế trái post_id): Tạo quan hệ R_post = { post_id, group_id, author_id, post_title, post_content, post_created_at }. Khóa chính: post_id.")
    add_bullet(doc, "Nhóm 4 (Cùng vế trái comment_id): Tạo quan hệ R_comment = { comment_id, post_id, author_id, comment_content, comment_created_at }. Khóa chính: comment_id.")
    add_bullet(doc, "Kiểm tra khóa ứng viên của R: Quan hệ R_comment đã chứa comment_id (khóa ứng viên của R), do đó không cần tạo thêm quan hệ phụ bổ sung.")

    add_paragraph(doc, "Kiểm tra điều kiện BCNF (Boyce-Codd Normal Form): Một lược đồ quan hệ đạt chuẩn BCNF nếu với mọi phụ thuộc hàm phi tầm thường X → A, X bắt buộc phải là một SIÊU KHÓA (Superkey).")
    add_bullet(doc, "Trong R_group: Khóa là group_id. Vế trái của mọi FD là group_id (siêu khóa) ⇒ ĐẠT BCNF.")
    add_bullet(doc, "Trong R_user: author_id → author_email, author_name (vế trái là khóa chính); author_email → author_id, author_name (vế trái là khóa ứng viên). Vế trái của mọi FD đều là siêu khóa ⇒ ĐẠT BCNF.")
    add_bullet(doc, "Trong R_post: Khóa là post_id. Vế trái của mọi FD là post_id (siêu khóa) ⇒ ĐẠT BCNF.")
    add_bullet(doc, "Trong R_comment: Khóa là comment_id. Vế trái của mọi FD là comment_id (siêu khóa) ⇒ ĐẠT BCNF.")

    # --- 2.6 CHỨNG MINH LOSSLESS JOIN (BẢNG CHASE) ---
    add_heading_2(doc, "2.6 Chứng minh Lossless Join (Bảng ma trận Chase) & Bảo toàn FD")
    add_paragraph(doc, "Để chứng minh phép phân rã R thành ρ = {R_group, R_user, R_post, R_comment} là phép nối không tổn thất thông tin (Lossless Join Property), ta lập Bảng ma trận Chase (Chase Tableau).")
    add_paragraph(doc, "Quy ước ký hiệu: Thuộc tính thứ j trong quan hệ Ri nếu có mặt thì mang giá trị ký hiệu aj, nếu không có mặt mang giá trị ký hiệu bij.")

    chase_headers = ["Quan hệ con", "c_id", "p_id", "g_id", "g_name", "g_topic", "a_id", "a_name", "a_email", "c_cont", "c_time", "p_title", "p_cont", "p_time"]
    chase_rows = [
        ["R_group", "b1,1", "b1,2", "a3", "a4", "a5", "b1,6", "b1,7", "b1,8", "b1,9", "b1,10", "b1,11", "b1,12", "b1,13"],
        ["R_user", "b2,1", "b2,2", "b2,3", "b2,4", "b2,5", "a6", "a7", "a8", "b2,9", "b2,10", "b2,11", "b2,12", "b2,13"],
        ["R_post", "b3,1", "a2", "a3", "b3,4", "b3,5", "a6", "b3,7", "b3,8", "b3,9", "b3,10", "a11", "a12", "a13"],
        ["R_comment", "a1", "a2", "b4,3", "b4,4", "b4,5", "a6", "b4,7", "b4,8", "a9", "a10", "b4,11", "b4,12", "b4,13"],
    ]
    add_styled_table(doc, chase_headers, chase_rows)

    add_paragraph(doc, "Quá trình biến đổi ma trận Chase thông qua các phụ thuộc hàm trong F_min:")
    add_bullet(doc, "Áp dụng FD post_id → group_id trên dòng R_post và R_comment: Vì hai dòng cùng có a2 ở cột p_id, nên phần tử b4,3 ở cột g_id của dòng R_comment được thay thế bằng a3.")
    add_bullet(doc, "Áp dụng FD group_id → group_name, group_topic trên dòng R_group và R_comment: Vì cùng có a3 ở cột g_id, các phần tử b4,4 và b4,5 của R_comment được thay thế bằng a4 và a5.")
    add_bullet(doc, "Áp dụng FD author_id → author_name, author_email trên dòng R_user và R_comment: Vì cùng có a6 ở cột a_id, các phần tử b4,7 và b4,8 của R_comment được thay thế bằng a7 và a8.")
    add_bullet(doc, "Áp dụng FD post_id → post_title, post_content, post_created_at trên dòng R_post và R_comment: Vì cùng có a2 ở cột p_id, các phần tử b4,11, b4,12, b4,13 của R_comment được thay thế bằng a11, a12, a13.")

    add_paragraph(doc, "Kết quả: Dòng thứ 4 (tương ứng quan hệ R_comment) đã trở thành dòng chứa TOÀN BỘ KÝ HIỆU {a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13}. Theo định lý Chase, điều này chứng minh đanh thép rằng:")
    add_callout_box(doc, "ĐỊNH LÝ ĐÃ ĐƯỢC CHỨNG MINH: Phép phân rã R thành {R_group, R_user, R_post, R_comment} là BẢO TOÀN THÔNG TIN 100% (Lossless Join) và BẢO TOÀN TOÀN BỘ PHỤ THUỘC HÀM (Dependency Preserving). Khi thực hiện NATURAL JOIN các bảng lại, ta thu được chính xác dữ liệu ban đầu mà không sinh ra bất kỳ bộ dữ liệu giả mạo (Spurious Tuples) nào.", "KẾT LUẬN CHỨNG MINH CHASE TABLEAU")

    # --- 2.7 PHỤ THUỘC ĐA TRỊ VÀ 4NF ---
    add_heading_2(doc, "2.7 Phụ thuộc đa trị (MVD) và Dạng chuẩn 4 (4NF)")
    add_paragraph(doc, "Trong mô hình thông tin sinh viên, một người dùng có thể sở hữu nhiều sở thích (interests) và nhiều môn học quan tâm (subjects). Giả sử ta lưu chung vào một bảng: User_Interests_Subjects(author_id, interest, subject).")
    add_paragraph(doc, "Hiện tượng: Giữa interest và subject hoàn toàn độc lập với nhau, không có mối liên hệ ngữ nghĩa trực tiếp. Tuy nhiên, nếu một sinh viên có 3 sở thích {'AI', 'Database', 'Cloud'} và 2 môn học {'CSDLNC', 'CTDL'}, bảng sẽ bị bùng nổ tổ hợp với 3 × 2 = 6 dòng dữ liệu (Dị thường tích Descartes - Cartesian Product Anomaly).")
    add_paragraph(doc, "Định nghĩa toán học Phụ thuộc đa trị (Multi-Valued Dependency - MVD): author_id ↠ interest và author_id ↠ subject. Do author_id không phải là siêu khóa của bảng 3 thuộc tính này, bảng đã vi phạm Dạng chuẩn 4 (4NF).")
    add_paragraph(doc, "Giải pháp chuẩn hóa đạt 4NF: Tách bảng thành hai quan hệ độc lập:")
    add_bullet(doc, "user_interests(author_id, interest) với khóa chính tổ hợp (author_id, interest).")
    add_bullet(doc, "user_subjects(author_id, subject) với khóa chính tổ hợp (author_id, subject).")

    # --- 2.8 PHI CHUẨN HÓA CÓ KIỂM SOÁT ---
    add_heading_2(doc, "2.8 Phân tích kỹ thuật phi chuẩn hóa có kiểm soát (Controlled Denormalization)")
    add_paragraph(doc, "Mặc dù chuẩn hóa 3NF/BCNF triệt tiêu hoàn toàn dư thừa và dị thường cập nhật, nhưng trong thực tế các ứng dụng mạng xã hội quy mô lớn, việc tuân thủ 100% chuẩn hóa có thể dẫn đến suy giảm nghiêm trọng hiệu năng đọc:")
    add_bullet(doc, "Trong bài toán hiển thị Bảng tin (Social Newsfeed), mỗi khi người dùng cuộn trang, hệ thống phải hiển thị số lượng bạn bè (friend_count), số lượng bình luận của bài viết (comment_count) và số lượng lượt thích (reaction_count).")
    add_bullet(doc, "Nếu tuân thủ chuẩn 3NF thuần túy, mỗi lượt tải feed sẽ phải kích hoạt hàng loạt câu lệnh COUNT(*) lặp lại trên các bảng hàng triệu dòng, gây nghẽn I/O và quá tải CPU.")
    add_paragraph(doc, "Giải pháp: Áp dụng kỹ thuật Phi chuẩn hóa có kiểm soát (Controlled Denormalization) bằng cách bổ sung các trường số nguyên friend_count trên bảng users, comment_count và reaction_count trên bảng post. Để ngăn chặn nguy cơ sai lệch số liệu, nhóm thiết kế các Database Trigger thực thi tự động trong cùng Transaction:")

    add_code_block(doc, "CREATE OR REPLACE FUNCTION fn_update_comment_count()\n"
                        "RETURNS TRIGGER AS $$\n"
                        "BEGIN\n"
                        "  IF TG_OP = 'INSERT' THEN\n"
                        "    UPDATE post SET comment_count = comment_count + 1 WHERE post_id = NEW.post_id;\n"
                        "  ELSIF TG_OP = 'DELETE' THEN\n"
                        "    UPDATE post SET comment_count = comment_count - 1 WHERE post_id = OLD.post_id;\n"
                        "  END IF;\n"
                        "  RETURN NULL;\n"
                        "END;\n"
                        "$$ LANGUAGE plpgsql;\n\n"
                        "CREATE TRIGGER trg_sync_comment_count\n"
                        "AFTER INSERT OR DELETE ON comment\n"
                        "FOR EACH ROW EXECUTE FUNCTION fn_update_comment_count();",
                   "Trigger đồng bộ bộ đếm bình luận tự động bảo toàn tính nhất quán")

    doc.add_page_break()
