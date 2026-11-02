"""
Chương 1: Đặc tả nghiệp vụ, Thiết kế mức quan niệm (EER) và Ánh xạ kế thừa.
"""

from docx import Document
from .styles import (
    add_heading_1, add_heading_2, add_heading_3,
    add_paragraph, add_bullet, add_styled_table, add_figure, add_callout_box
)

def build_ch1(doc: Document):
    add_heading_1(doc, "CHƯƠNG 1: ĐẶC TẢ NGHIỆP VỤ & THIẾT KẾ MỨC QUAN NIỆM (EER)")

    # --- 1.1 ĐẶC TẢ 10 QUY TẮC NGHIỆP VỤ ---
    add_heading_2(doc, "1.1 Đặc tả 10 quy tắc nghiệp vụ then chốt (BR1 – BR10)")
    add_paragraph(doc, "Để xây dựng một mạng xã hội học tập vận hành tin cậy, hệ thống cần được ràng buộc chặt chẽ bởi các quy tắc nghiệp vụ (Business Rules - BR). Dưới đây là 10 quy tắc nghiệp vụ cốt lõi đã được nhóm chuẩn hóa, làm tiền đề thiết kế cấu trúc dữ liệu quan niệm và các ràng buộc DDL/Trigger tầng cơ sở dữ liệu:")

    br_data = [
        ["Mã BR", "Tên quy tắc nghiệp vụ", "Thực thể liên quan", "Nội dung đặc tả & Ràng buộc toàn vẹn tầng CSDL"],
        ["BR1", "Quản lý Hồ sơ Sinh viên", "NGUOI_DUNG", "Mỗi người dùng có một mã định danh duy nhất (user_id), địa chỉ email là duy nhất (UNIQUE) và hợp lệ cú pháp RFC 5322. Họ tên gồm 3 thành phần (họ, tên đệm, tên). Người dùng có thể khai báo nhiều sở thích (interests) và môn học quan tâm (subjects). Cột friend_count là thuộc tính dẫn xuất lưu tổng số bạn bè."],
        ["BR2", "Quan hệ Kết bạn Vô hướng", "KET_BAN (users, friendship)", "Quan hệ bạn bè là quan hệ hai chiều đối xứng (vô hướng). Để triệt tiêu trùng lặp và ngăn ngừa dị thường đảo cặp, tầng CSDL áp dụng quy ước chuẩn tắc: luôn lưu user_a < user_b kèm ràng buộc CHECK (user_a < user_b) và khóa chính tổ hợp PRIMARY KEY (user_a, user_b). Một người không thể tự kết bạn với chính mình."],
        ["BR3", "Quan hệ Theo dõi Có hướng", "THEO_DOI (user_follow)", "Người dùng A có thể theo dõi người dùng B mà không cần người dùng B đồng ý. Đây là quan hệ đồ thị có hướng (Directed Graph). Ràng buộc: follower_id <> followed_id, khóa chính tổ hợp (follower_id, followed_id). Một người có thể theo dõi nhiều người và có nhiều người theo dõi."],
        ["BR4", "Nhóm học tập & Quyền hạn", "NHOM_HOC_TAP, THAM_GIA", "Mỗi nhóm học tập có duy nhất một trưởng nhóm sáng lập (owner_id). Nhóm có tên, chủ đề và cờ phân loại riêng tư (is_private). Quan hệ tham gia nhóm (M:N) lưu trữ vai trò role ('owner', 'mod', 'member') và thời điểm tham gia joined_at. Một người dùng có thể là thành viên của nhiều nhóm."],
        ["BR5", "Đăng bài viết & Phân loại", "BAI_DANG, BAI_THAO_LUAN, BAI_TAI_LIEU", "Bài đăng có thể đăng trên trang cá nhân hoặc trong một nhóm học tập cụ thể. Bài đăng được phân loại chuyên môn hóa rời rạc thành hai loại: Bài thảo luận (chứa cờ is_closed biểu thị trạng thái khóa bình luận) hoặc Bài tài liệu (chứa file_url, định dạng, dung lượng và tập thẻ nhãn tags phục vụ tìm kiếm)."],
        ["BR6", "Thảo luận Phân cấp (Cây)", "BINH_LUAN", "Mỗi bài đăng có thể có nhiều bình luận. Bình luận có thể trả lời trực tiếp bài đăng (nút gốc cây, parent_id = NULL) hoặc trả lời một bình luận khác (nút con, parent_id <> NULL). Quan hệ này tạo thành cấu trúc cây phân cấp vô hạn cấp (N-ary Tree). Ràng buộc: không được phép xuất hiện chu trình cha-con (A là cha B và B là cha A)."],
        ["BR7", "Hệ thống Cảm xúc Tương tác", "CAM_XUC (post_reaction)", "Người dùng có thể bày tỏ cảm xúc trên bài viết với các loại: 'like', 'love', 'haha', 'wow', 'sad', 'angry'. Ràng buộc nghiệp vụ: Tại một thời điểm, mỗi người dùng chỉ được bày tỏ tối đa một cảm xúc trên một bài viết (Khóa chính tổ hợp: user_id, post_id). Cập nhật cảm xúc mới sẽ ghi đè loại cảm xúc cũ."],
        ["BR8", "Thư mục Tài liệu Nhóm", "THU_MUC", "Mỗi nhóm học tập sở hữu một cấu trúc cây thư mục để phân loại tài liệu chia sẻ. Thư mục gốc có parent_folder_id = NULL, các thư mục con tham chiếu đến thư mục cha trong cùng một nhóm. Ràng buộc: Tên thư mục con là duy nhất trong cùng một thư mục cha."],
        ["BR9", "Thống kê & Bộ đếm Dẫn xuất", "NGUOI_DUNG, BAI_DANG", "Để tối ưu hóa hiệu năng đọc feed bảng tin, các số liệu thống kê như friend_count (tổng bạn bè), comment_count (tổng bình luận) và reaction_count (tổng lượt thích) được phi chuẩn hóa có kiểm soát bằng các trường số nguyên, được duy trì nhất quán thông qua Database Triggers."],
        ["BR10", "Toàn vẹn Xóa & Khóa Thảo luận", "BINH_LUAN, NHOM_HOC_TAP", "Khi một bài thảo luận bị khóa (is_closed = TRUE), hệ thống từ chối mọi thao tác chèn bình luận mới (thực thi thông qua Trigger trg_check_comment_post_closed). Trưởng nhóm không thể bị xóa khỏi nhóm nếu chưa chuyển nhượng quyền owner cho thành viên khác."],
    ]
    add_styled_table(doc, br_data[0], br_data[1:], [0.8, 1.6, 1.4, 3.2])

    # --- 1.2 MÔ HÌNH THỰC THỂ - MỐI KẾT HỢP MỞ RỘNG (EER) ---
    add_heading_2(doc, "1.2 Mô hình thực thể - mối kết hợp mở rộng (EER)")
    add_paragraph(doc, "Dựa trên 10 quy tắc nghiệp vụ trên, nhóm đã tiến hành phân tích và xây dựng Sơ đồ Thực thể - Mối kết hợp mở rộng (Enhanced Entity-Relationship - EER Diagram). Mô hình EER cho phép biểu diễn trực quan các kiểu thuộc tính phức hợp, thuộc tính đa trị, các mối kết hợp đệ quy và cấu trúc chuyên môn hóa / khái quát hóa.")

    add_figure(doc, "docs/eer_diagram.png", "Hình 1.1: Sơ đồ Thực thể - Mối kết hợp mở rộng (EER Diagram) Hệ thống Mạng xã hội học tập", width_inches=6.5)

    add_heading_3(doc, "1.2.1 Phân tích chi tiết các thực thể và phân loại thuộc tính")
    add_bullet(doc, "Đại diện cho người học và giảng viên. Khóa chính là user_id. Email có ràng buộc duy nhất (U). Thuộc tính ho_ten là một thuộc tính phức hợp (Composite Attribute) được cấu thành từ 3 thuộc tính thành phần đơn trị: ho, ten_dem, ten. Thuộc tính so_thich (interests) và mon_hoc (subjects) là thuộc tính đa trị (Multi-valued Attributes, ký hiệu bằng hình oval viền đôi). Thuộc tính friend_count là thuộc tính dẫn xuất (Derived Attribute, hình oval nét đứt) được tính từ tổng số liên kết bạn bè.", bold_prefix="Thực thể NGUOI_DUNG (users): ")
    add_bullet(doc, "Không gian học tập cộng tác. Khóa chính là group_id. Các thuộc tính mô tả gồm name, topic và is_private (nhóm công khai hoặc riêng tư).", bold_prefix="Thực thể NHOM_HOC_TAP (study_group): ")
    add_bullet(doc, "Đóng vai trò là một siêu lớp (Superclass) trong mối quan hệ kế thừa. Chứa các thuộc tính dùng chung cho mọi bài đăng gồm post_id (Khóa chính), title, content, created_at.", bold_prefix="Thực thể BÀI ĐĂNG (post): ")
    add_bullet(doc, "Là phân lớp con (Subclass) của BÀI ĐĂNG. Chứa thuộc tính đặc thù is_closed (kiểu boolean, đánh dấu bài thảo luận đã đóng, cấm bình luận tiếp).", bold_prefix="Thực thể BÀI THẢO LUẬN ('thaoluan'): ")
    add_bullet(doc, "Là phân lớp con (Subclass) của BÀI ĐĂNG. Chứa các thuộc tính đặc thù phục vụ lưu trữ file gồm file_url (đường dẫn tài liệu), định dạng, dung lượng, và tập thuộc tính đa trị tap_nhan {tags} lưu các nhãn chuyên đề phân loại học tập.", bold_prefix="Thực thể BÀI TÀI LIỆU ('tailieu'): ")
    add_bullet(doc, "Đại diện cho các phản hồi thảo luận. Khóa chính là comment_id. Chứa các thuộc tính content, created_at. Thực thể này tham gia vào mối kết hợp đệ quy 1:N để hình thành cây bình luận đa cấp.", bold_prefix="Thực thể BÌNH LUẬN (comment): ")
    add_bullet(doc, "Đại diện cho cấu trúc phân loại tài liệu theo dạng cây trong nhóm. Khóa chính là folder_id, thuộc tính name.", bold_prefix="Thực thể THƯ MỤC (folder): ")

    add_heading_3(doc, "1.2.2 Phân tích các mối kết hợp và bản số (Cardinality & Modality)")
    add_bullet(doc, "Liên kết giữa NGUOI_DUNG và chính nó. Bản số (0, N) - (0, N). Có thuộc tính liên kết là since (thời điểm kết bạn).", bold_prefix="KẾT BẠN (M:N, Đệ quy vô hướng): ")
    add_bullet(doc, "Liên kết giữa NGUOI_DUNG và chính nó nhưng có phân biệt vai trò follower (người theo dõi) và followee (người được theo dõi).", bold_prefix="THEO DÕI (M:N, Đệ quy có hướng): ")
    add_bullet(doc, "Liên kết giữa NGUOI_DUNG và NHOM_HOC_TAP. Bản số (0, N) - (1, N). Thuộc tính liên kết gồm role ('owner'/'mod'/'member') và joined_at.", bold_prefix="THAM GIA (M:N) & SỞ HỮU (1:N): ")
    add_bullet(doc, "Liên kết 1:N giữa NGUOI_DUNG và BAI_DANG (mỗi bài có đúng 1 tác giả; 1 tác giả có thể có 0 hoặc nhiều bài).", bold_prefix="ĐĂNG BÀI (1:N): ")
    add_bullet(doc, "Liên kết 1:N giữa NHOM_HOC_TAP và BAI_DANG (bài đăng có thể thuộc về 1 nhóm hoặc độc lập).", bold_prefix="THUỘC NHÓM (1:N): ")
    add_bullet(doc, "Liên kết M:N giữa NGUOI_DUNG và BAI_DANG. Thuộc tính liên kết là kind ('like', 'love', 'haha',...).", bold_prefix="CẢM XÚC (M:N): ")
    add_bullet(doc, "Liên kết đệ quy 1:N giữa BINH_LUAN cha và BINH_LUAN con (thông qua thuộc tính parent_id).", bold_prefix="TRẢ LỜI BÌNH LUẬN (1:N, Đệ quy): ")
    add_bullet(doc, "Siêu lớp BAI_DANG phân rã thành 2 phân lớp con BAI_THAO_LUAN và BAI_TAI_LIEU. Ký hiệu chữ 'd' (Disjoint) trong vòng tròn biểu thị tính chất chuyên môn hóa rời rạc: một bài đăng tại một thời điểm chỉ có thể là bài thảo luận hoặc bài tài liệu, không thể đồng thời là cả hai.", bold_prefix="Chuyên môn hóa rời rạc (Disjoint Specialization 'd'): ")

    # --- 1.3 SO SÁNH 3 PHƯƠNG ÁN ÁNH XẠ KẾ THỪA ---
    add_heading_2(doc, "1.3 So sánh và lựa chọn 3 phương án ánh xạ kế thừa (Inheritance Mapping)")
    add_paragraph(doc, "Trong thiết kế cơ sở dữ liệu quan hệ, mối quan hệ kế thừa (IS-A) giữa siêu lớp BAI_DANG và các lớp con (BAI_THAO_LUAN, BAI_TAI_LIEU) không được hỗ trợ tự nhiên bởi mô hình quan hệ nguyên thủy. Có 3 phương án kiến trúc kinh điển để chuyển đổi từ mô hình quan niệm sang mô hình logic:")

    inherit_data = [
        ["Tiêu chí đánh giá", "Phương án 1: Bảng Đơn\n(Single Table)", "Phương án 2: Bảng Nối\n(Class Table / Joined Table)", "Phương án 3: Bảng Riêng Cụ Thể\n(Concrete Table / Table per Class)"],
        ["Số lượng bảng vật lý", "1 bảng duy nhất (post)\nchứa tất cả thuộc tính gộp.", "3 bảng riêng biệt:\npost, post_discussion, post_doc.", "2 bảng cụ thể:\npost_discussion, post_doc."],
        ["Hiệu năng đọc Feed\n(Polymorphic Query)", "Cực nhanh (O(1) Scan).\nKhông cần JOIN bảng phụ.", "Chậm hơn do bắt buộc phải LEFT JOIN\n3 bảng để lấy đầy đủ thuộc tính.", "Rất chậm khi truy vấn toàn bộ feed\nvì phải dùng UNION ALL hai bảng."],
        ["Lãng phí dung lượng đĩa\n(NULL Overhead)", "Có cột NULL (cột của lớp con\nnày sẽ NULL ở dòng của lớp con kia).", "Không lãng phí cột NULL.\nMỗi bảng chỉ chứa thuộc tính riêng.", "Không lãng phí cột NULL."],
        ["Tính toàn vẹn ràng buộc\n(NOT NULL Constraints)", "Kém hơn: Không thể đặt NOT NULL\ncho cột riêng ở mức schema DDL.", "Rất tốt: Dễ dàng đặt NOT NULL\nvà CHECK constraint trên từng bảng con.", "Rất tốt trên từng bảng con."],
        ["Khóa chính & Khóa ngoại", "Đơn giản: 1 khóa chính post_id\ncho toàn bộ hệ thống.", "Phức tạp: post_id ở bảng con vừa là\nkhóa chính vừa là khóa ngoại tới post.", "Khó quản lý khóa chính toàn cục\n(dễ bị trùng lặp ID giữa 2 bảng con)."],
        ["Khả năng mở rộng lớp con", "Dễ dàng: Thêm cột mới hoặc dùng JSONB\nmà không cần tạo bảng mới.", "Tốn chi phí: Mỗi lớp con mới phải tạo\n1 bảng và viết thêm các câu lệnh JOIN.", "Phải tạo bảng mới và sửa lại toàn bộ\ncác câu truy vấn dùng UNION ALL."],
    ]
    add_styled_table(doc, inherit_data[0], inherit_data[1:], [1.6, 1.8, 1.8, 1.8])

    add_callout_box(doc, "Quyết định kiến trúc của nhóm: Lựa chọn Phương án 1 (Single Table Inheritance) cho thực thể BAI_DANG, sử dụng cột phân loại post_type VARCHAR(20) CHECK (post_type IN ('thaoluan', 'tailieu')) kết hợp cột cờ is_closed và trường JSONB / file_url. Quyết định này xuất phát từ đặc thù mạng xã hội: thao tác đọc Bảng tin (Social Feed) diễn ra với tần suất áp đảo (95% tổng truy vấn). Bảng đơn giúp triệt tiêu hoàn toàn chi phí JOIN bảng phụ, tối ưu hóa bộ nhớ đệm (Buffer Cache) và tăng thông lượng TPS khi hệ thống chịu tải nặng.", "QUYẾT ĐỊNH THIẾT KẾ ÁNH XẠ KẾ THỪA")

    doc.add_page_break()
