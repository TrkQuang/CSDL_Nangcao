"""
Chương 1: Đặc tả nghiệp vụ, Thiết kế mức quan niệm (EER), Thiết kế lược đồ vật lý và Ánh xạ kế thừa.
Bản mở rộng quy mô lớn phục vụ Báo cáo tổng kết toàn diện (~120 trang).
"""

from docx import Document
from .styles import (
    add_heading_1, add_heading_2, add_heading_3,
    add_paragraph, add_bullet, add_styled_table, add_code_block, add_figure, add_callout_box
)

def build_ch1(doc: Document):
    add_heading_1(doc, "CHƯƠNG 1: ĐẶC TẢ NGHIỆP VỤ & THIẾT KẾ MỨC QUAN NIỆM (EER)")

    # --- 1.1 TỔNG QUAN HỆ THỐNG VÀ BỐI CẢNH NGHIỆP VỤ ---
    add_heading_2(doc, "1.1 Bối cảnh nghiệp vụ và Mục tiêu xây dựng Hệ thống")
    add_paragraph(doc, "Trong kỷ nguyên số hóa giáo dục đại học, nhu cầu xây dựng một môi trường học tập cộng tác tương tác cao, kết nối trực tiếp sinh viên, giảng viên và các nhóm nghiên cứu là một đòi hỏi cấp thiết. Các hệ thống Quản lý Học tập truyền thống (Learning Management Systems - LMS) như Moodle hay Canvas thường mang tính thứ bậc cứng nhắc, thiếu sự linh hoạt trong tương tác đa chiều giữa người học. Ngược lại, các nền tảng mạng xã hội thương mại như Facebook, Reddit lại thiếu vắng các cơ chế kiểm soát chất lượng học thuật, quản lý phân loại tài liệu chuyên sâu và bảo đảm tính toàn vẹn dữ liệu học tập.")
    add_paragraph(doc, "Hệ thống Mạng xã hội Học tập (Social Learning Network System - SLNS) được thiết kế nhằm dung hòa hai không gian trên: mang lại trải nghiệm tương tác trực quan, tức thời của mạng xã hội hiện đại, đồng thời duy trì kỷ luật cấu trúc, tính toàn vẹn ngữ nghĩa và khả năng truy vấn quan hệ phức tạp của một hệ thống cơ sở dữ liệu học thuật quy mô lớn.")

    # --- 1.2 ĐẶC TẢ 10 QUY TẮC NGHIỆP VỤ CHI TIẾT ---
    add_heading_2(doc, "1.2 Đặc tả 10 quy tắc nghiệp vụ then chốt (BR1 – BR10)")
    add_paragraph(doc, "Một hệ thống mạng xã hội học thuật không thể vận hành ổn định nếu thiếu các quy tắc nghiệp vụ (Business Rules - BR) chặt chẽ. Dưới đây là 10 quy tắc nghiệp vụ cốt lõi, được phân tích thấu đáo từ góc độ ngữ nghĩa thực tế đến các cơ chế cưỡng chế toàn vẹn (Integrity Constraints) tại tầng Cơ sở dữ liệu quan hệ PostgreSQL 18.6:")

    add_paragraph(doc, "Mỗi người dùng trong hệ thống (sinh viên, giảng viên, quản trị viên) được định danh duy nhất bởi một mã số nguyên tự tăng user_id. Địa chỉ thư điện tử (email) bắt buộc phải là duy nhất trên toàn hệ thống (UNIQUE) và tuân thủ định dạng chuẩn quốc tế RFC 5322. Họ tên người dùng được lưu trữ dưới dạng thuộc tính phức hợp gồm 3 thành phần: họ, tên đệm và tên nhằm phục vụ sắp xếp danh sách sinh viên theo thứ tự từ điển tiếng Việt. Mỗi tài khoản có thể khai báo một hoặc nhiều sở thích học thuật (như 'Trí tuệ nhân tạo', 'Khoa học dữ liệu', 'Phát triển Web') và danh sách các môn học đang theo học. Cột friend_count là thuộc tính dẫn xuất, lưu trữ số lượng bạn bè hiện tại để tối ưu hóa việc tải trang cá nhân.", bold_prefix="Quy tắc 1 (BR1 - Quản lý Hồ sơ Người dùng): ")
    add_bullet(doc, "Ràng buộc mức DDL: email VARCHAR(255) NOT NULL UNIQUE, full_name VARCHAR(150) NOT NULL, password_hash VARCHAR(255) NOT NULL.")
    add_bullet(doc, "Ràng buộc kiểm tra CHECK: CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$') kiểm tra định dạng email hợp lệ.")
    add_bullet(doc, "Ràng buộc ngữ nghĩa: Người dùng không được phép đăng ký trùng email; mật khẩu bắt buộc phải được mã hóa một chiều bằng thuật toán an toàn (như BCrypt hoặc Argon2) trước khi lưu trữ.")

    add_paragraph(doc, "Quan hệ kết bạn giữa hai người dùng là quan hệ hai chiều đối xứng (vô hướng). Nếu người dùng A là bạn của người dùng B thì hiển nhiên người dùng B cũng là bạn của người dùng A. Trong cơ sở dữ liệu quan hệ, việc lưu trữ cả hai cặp (A, B) và (B, A) sẽ dẫn đến dư thừa dữ liệu 100%, lãng phí tài nguyên bộ nhớ đệm và tiềm ẩn nguy cơ bất nhất quán (một chiều bị xóa còn chiều kia vẫn tồn tại). Do đó, hệ thống áp dụng Quy ước Chuẩn tắc (Canonical Representation): luôn luôn lưu trữ với điều kiện user_a < user_b.", bold_prefix="Quy tắc 2 (BR2 - Quan hệ Kết bạn Vô hướng Đối xứng): ")
    add_bullet(doc, "Ràng buộc mức DDL: PRIMARY KEY (user_a, user_b), CHECK (user_a < user_b).")
    add_bullet(doc, "Ràng buộc nghiệp vụ: Một người dùng không thể tự kết bạn với chính mình (user_a <> user_b). Khi người dùng tìm kiếm danh sách bạn bè của ID X, truy vấn SQL sẽ quét trên cả hai cột: WHERE user_a = X OR user_b = X.")
    add_bullet(doc, "Chỉ mục tối ưu: Khởi tạo 2 chỉ mục B-Tree: CREATE INDEX idx_friend_a ON friendship(user_a) và CREATE INDEX idx_friend_b ON friendship(user_b) để tối ưu hóa phép quét hợp (BitmapOr Index Scan).")

    add_paragraph(doc, "Khác với quan hệ bạn bè đối xứng, quan hệ theo dõi (Follow) là quan hệ đồ thị có hướng (Directed Graph). Người dùng A có thể bấm theo dõi hoạt động học tập, bài viết chuyên đề của Giảng viên hoặc Sinh viên tiêu biểu B mà không cần người B chấp thuận hay theo dõi ngược lại.", bold_prefix="Quy tắc 3 (BR3 - Quan hệ Theo dõi Có hướng): ")
    add_bullet(doc, "Ràng buộc mức DDL: PRIMARY KEY (follower_id, followed_id), CHECK (follower_id <> followed_id).")
    add_bullet(doc, "Ràng buộc toàn vẹn tham chiếu: follower_id và followed_id đều là khóa ngoại tham chiếu đến bảng users(user_id) với hành vi ON DELETE CASCADE (khi tài khoản bị xóa, các quan hệ theo dõi liên quan tự động bị hủy bỏ).")

    add_paragraph(doc, "Người dùng có thể khởi tạo các không gian học tập cộng tác (study_group). Mỗi nhóm học tập thuộc về một chủ đề môn học xác định (topic) và được sáng lập bởi một Trưởng nhóm duy nhất (owner_id). Nhóm có thể được cấu hình ở chế độ Công khai (is_private = FALSE - mọi học viên có thể tìm thấy và tham gia) hoặc Riêng tư (is_private = TRUE - yêu cầu phê duyệt). Quan hệ thành viên (group_members) lưu trữ vai trò role ('owner', 'mod', 'member') và thời điểm tham gia (joined_at).", bold_prefix="Quy tắc 4 (BR4 - Nhóm Học tập & Phân quyền Thành viên): ")
    add_bullet(doc, "Ràng buộc mức DDL: owner_id INT REFERENCES users(user_id) ON DELETE RESTRICT, role VARCHAR(20) CHECK (role IN ('owner', 'mod', 'member')).")
    add_bullet(doc, "Ràng buộc toàn vẹn: Một nhóm học tập bắt buộc phải có tối thiểu một owner. Người dùng đang là owner duy nhất của một nhóm không được phép rời nhóm hoặc xóa tài khoản nếu chưa chuyển nhượng quyền sở hữu nhóm cho một thành viên khác.")

    add_paragraph(doc, "Bài đăng (post) là thực thể trung tâm của mạng xã hội, có thể được đăng trên trang cá nhân của tác giả hoặc trong một nhóm học tập cụ thể. Bài đăng được chia thành hai phân lớp chuyên biệt: Bài thảo luận (Discussion Post - tập trung vào việc đặt câu hỏi, tranh luận học thuật) và Bài tài liệu (Document Post - chứa tài liệu đính kèm, đường dẫn tệp, kích thước và các thẻ nhãn chuyên đề tags).", bold_prefix="Quy tắc 5 (BR5 - Đăng bài viết & Phân loại Nội dung): ")
    add_bullet(doc, "Ràng buộc mức DDL: post_type VARCHAR(20) CHECK (post_type IN ('thaoluan', 'tailieu')), author_id INT NOT NULL REFERENCES users(user_id).")
    add_bullet(doc, "Ràng buộc chuyên môn hóa: Bài thảo luận sở hữu cờ trạng thái is_closed BOOLEAN DEFAULT FALSE; Bài tài liệu bắt buộc phải có đường dẫn file_url NOT NULL khi post_type = 'tailieu'.")

    add_paragraph(doc, "Mỗi bài đăng mở ra một không gian thảo luận phân cấp. Một phản hồi có thể trả lời trực tiếp bài viết (bình luận gốc, parent_id = NULL) hoặc phản hồi lại một bình luận khác đã có (bình luận con cháu, parent_id <> NULL). Cấu trúc này tạo thành một cây phân cấp lồng nhau đa cấp vô hạn (N-ary Tree).", bold_prefix="Quy tắc 6 (BR6 - Chuỗi Thảo luận Bình luận Phân cấp): ")
    add_bullet(doc, "Ràng buộc mức DDL: parent_id INT REFERENCES comment(comment_id) ON DELETE CASCADE, post_id INT NOT NULL REFERENCES post(post_id) ON DELETE CASCADE.")
    add_bullet(doc, "Ràng buộc toàn vẹn cấu trúc: Bình luận con bắt buộc phải thuộc về cùng một post_id với bình luận cha. Không cho phép xuất hiện chu trình lặp cha-con (A là cha B và B là cha A).")

    add_paragraph(doc, "Hệ thống cảm xúc tương tác trên bài viết cho phép người dùng bày tỏ thái độ học thuật đối với nội dung chia sẻ (như 'like', 'love', 'haha', 'wow', 'sad', 'angry').", bold_prefix="Quy tắc 7 (BR7 - Hệ thống Cảm xúc Tương tác Độc quyền): ")
    add_bullet(doc, "Ràng buộc mức DDL: PRIMARY KEY (user_id, post_id), kind VARCHAR(20) CHECK (kind IN ('like', 'love', 'haha', 'wow', 'sad', 'angry')).")
    add_bullet(doc, "Ràng buộc độc quyền: Khóa chính tổ hợp (user_id, post_id) đảm bảo tại một thời điểm, mỗi người dùng chỉ được bày tỏ DUY NHẤT một loại cảm xúc trên một bài viết. Hành vi bày tỏ cảm xúc mới sẽ tự động cập nhật đè (UPSERT) lên cảm xúc cũ.")

    add_paragraph(doc, "Để tài liệu học tập trong nhóm không bị phân tán lộn xộn, mỗi nhóm học tập được trang bị một hệ thống cây thư mục lưu trữ (folder tree). Thư mục gốc có parent_folder_id = NULL, các thư mục con tham chiếu đến thư mục cha.", bold_prefix="Quy tắc 8 (BR8 - Cấu trúc Thư mục Tài liệu Nhóm): ")
    add_bullet(doc, "Ràng buộc mức DDL: group_id INT NOT NULL REFERENCES study_group(group_id) ON DELETE CASCADE, parent_id INT REFERENCES folder(folder_id) ON DELETE CASCADE.")
    add_bullet(doc, "Ràng buộc tính duy nhất: Trong cùng một thư mục cha, không được phép tồn tại hai thư mục con trùng tên (UNIQUE (group_id, parent_id, name)).")

    add_paragraph(doc, "Để giải quyết bài toán tải trang Bảng tin (Social Feed) với thông lượng hàng ngàn yêu cầu mỗi giây, các số liệu thống kê tổng hợp (như tổng số bạn bè friend_count của người dùng, tổng số bình luận comment_count và tổng số cảm xúc reaction_count của bài viết) được phi chuẩn hóa có kiểm soát dưới dạng các trường số nguyên.", bold_prefix="Quy tắc 9 (BR9 - Bộ đếm Thống kê Dẫn xuất & Phi chuẩn hóa): ")
    add_bullet(doc, "Ràng buộc toàn vẹn: Các giá trị bộ đếm bắt buộc phải >= 0 (CHECK (friend_count >= 0), CHECK (comment_count >= 0)).")
    add_bullet(doc, "Cơ chế duy trì: Toàn bộ quá trình tăng/giảm bộ đếm được tự động hóa tuyệt đối thông qua Database Triggers chạy trong cùng một giao dịch ACID với thao tác chèn/xóa bản ghi tương ứng.")

    add_paragraph(doc, "Hệ thống bảo đảm tính đóng băng của các bài thảo luận đã kết thúc. Khi một bài thảo luận được giảng viên hoặc tác giả đánh dấu đã đóng (is_closed = TRUE), hệ thống từ chối mọi thao tác chèn thêm bình luận mới.", bold_prefix="Quy tắc 10 (BR10 - Khóa Thảo luận & Toàn vẹn Xóa Tài khoản): ")
    add_bullet(doc, "Ràng buộc mức Trigger: Trigger trg_check_comment_post_closed kiểm tra trạng thái is_closed của post trước khi cho phép INSERT vào bảng comment.")
    add_bullet(doc, "Ràng buộc toàn vẹn xóa: Khóa ngoại owner_id trong bảng study_group áp dụng cơ chế ON DELETE RESTRICT nhằm ngăn chặn việc xóa tài khoản của người dùng khi họ vẫn đang là chủ sở hữu của nhóm học tập.")

    # --- 1.3 MÔ HÌNH EER HOÀN CHỈNH ---
    add_heading_2(doc, "1.3 Mô hình Thực thể - Mối kết hợp mở rộng (EER Diagram)")
    add_paragraph(doc, "Dựa trên 10 quy tắc nghiệp vụ trên, nhóm đã tiến hành phân tích mức quan niệm và thiết kế Sơ đồ Thực thể - Mối kết hợp mở rộng (Enhanced Entity-Relationship - EER Diagram). Sơ đồ EER được xây dựng theo chuẩn ký hiệu Chen mở rộng, thể hiện đầy đủ các thực thể, thuộc tính đơn/phức hợp/đa trị/dẫn xuất, các mối kết hợp 1:1, 1:N, M:N, các liên kết đệ quy và cấu trúc chuyên môn hóa rời rạc:")

    add_figure(doc, "docs/eer_diagram.png", "Hình 1.1: Sơ đồ Thực thể - Mối kết hợp mở rộng (EER Diagram) Hệ thống Mạng xã hội học tập", width_inches=6.5)

    add_heading_3(doc, "1.3.1 Phân tích chi tiết các thực thể và cấu trúc thuộc tính")
    add_paragraph(doc, "Mô hình quan niệm bao gồm 7 thực thể chính với cấu trúc thuộc tính được chuẩn mực hóa:")
    add_bullet(doc, "Khóa chính user_id (gạch chân). Thuộc tính email có ràng buộc duy nhất (U). Thuộc tính phức hợp ho_ten phân rã thành 3 thành phần đơn trị: ho, ten_dem, ten. Hai thuộc tính đa trị (Multi-valued Attributes, vẽ bằng hình oval viền đôi) gồm so_thich (interests) và mon_hoc (subjects). Thuộc tính dẫn xuất (Derived Attribute, vẽ bằng hình oval nét đứt) friend_count được tính toán từ các liên kết bạn bè.", bold_prefix="1. Thực thể NGƯỜI DÙNG (users): ")
    add_bullet(doc, "Khóa chính group_id. Thuộc tính mô tả: name (tên nhóm duy nhất), topic (chuyên đề học thuật), is_private (cờ phân loại riêng tư), và created_at.", bold_prefix="2. Thực thể NHÓM HỌC TẬP (study_group): ")
    add_bullet(doc, "Đóng vai trò Siêu lớp (Superclass) trong quan hệ kế thừa. Khóa chính post_id. Thuộc tính dùng chung gồm title (tiêu đề bài đăng), content (nội dung thảo luận), created_at.", bold_prefix="3. Thực thể BÀI ĐĂNG (post - Siêu lớp): ")
    add_bullet(doc, "Phân lớp con (Subclass) của BÀI ĐĂNG. Kế thừa toàn bộ thuộc tính của siêu lớp và bổ sung thuộc tính đặc thù is_closed (kiểu boolean, đánh dấu trạng thái khóa bình luận).", bold_prefix="4. Thực thể BÀI THẢO LUẬN ('thaoluan'): ")
    add_bullet(doc, "Phân lớp con (Subclass) của BÀI ĐĂNG. Kế thừa các thuộc tính của siêu lớp và bổ sung các thuộc tính phục vụ tệp đính kèm: file_url (đường dẫn lưu trữ tài liệu), và tập thuộc tính đa trị tap_nhan {tags} lưu các nhãn chuyên đề phân loại học tập.", bold_prefix="5. Thực thể BÀI TÀI LIỆU ('tailieu'): ")
    add_bullet(doc, "Đại diện cho các phản hồi phân cấp. Khóa chính comment_id. Thuộc tính mô tả: content (nội dung phản hồi) và created_at. Thực thể này tham gia vào mối kết hợp đệ quy 1:N để hình thành cây thảo luận đa cấp.", bold_prefix="6. Thực thể BÌNH LUẬN (comment): ")
    add_bullet(doc, "Khóa chính folder_id. Thuộc tính name (tên thư mục). Tham gia vào mối kết hợp đệ quy 1:N với chính nó để quản lý cây thư mục phân cấp trong nhóm.", bold_prefix="7. Thực thể THƯ MỤC (folder): ")

    add_heading_3(doc, "1.3.2 Phân tích các mối kết hợp, liên kết đệ quy và bản số")
    add_bullet(doc, "Liên kết đệ quy M:N giữa NGƯỜI DÙNG và chính nó. Cả hai phía đều có bản số (0, N). Thuộc tính liên kết since lưu trữ mốc thời gian kết bạn. Áp dụng ràng buộc chuẩn tắc user_a < user_b ở tầng vật lý để triệt tiêu trùng lặp.", bold_prefix="Mối kết hợp KẾT BẠN (M:N, Đệ quy vô hướng): ")
    add_bullet(doc, "Liên kết đệ quy M:N có hướng giữa NGƯỜI DÙNG và chính nó. Phân biệt rõ vai trò follower (người theo dõi) và followee (người được theo dõi).", bold_prefix="Mối kết hợp THEO DÕI (M:N, Đệ quy có hướng): ")
    add_bullet(doc, "Liên kết M:N giữa NGƯỜI DÙNG và NHÓM HỌC TẬP. Bản số phía người dùng là (0, N), phía nhóm là (1, N). Thuộc tính liên kết gồm role ('owner'/'mod'/'member') và joined_at.", bold_prefix="Mối kết hợp THAM GIA (M:N): ")
    add_bullet(doc, "Liên kết 1:N giữa NGƯỜI DÙNG và NHÓM HỌC TẬP. Một nhóm có đúng 1 chủ sở hữu (bản số 1, 1); một người dùng có thể là chủ sở hữu của 0 hoặc nhiều nhóm (bản số 0, N).", bold_prefix="Mối kết hợp SỞ HỮU (1:N): ")
    add_bullet(doc, "Liên kết 1:N giữa NGƯỜI DÙNG và BÀI ĐĂNG (mỗi bài có đúng 1 tác giả; 1 tác giả có thể có 0 hoặc nhiều bài).", bold_prefix="Mối kết hợp ĐĂNG BÀI (1:N): ")
    add_bullet(doc, "Liên kết 1:N giữa NHÓM HỌC TẬP và BÀI ĐĂNG (một bài đăng có thể thuộc về 1 nhóm hoặc đăng trên trang cá nhân; 1 nhóm có thể chứa nhiều bài đăng).", bold_prefix="Mối kết hợp THUỘC NHÓM (1:N): ")
    add_bullet(doc, "Liên kết M:N giữa NGƯỜI DÙNG và BÀI ĐĂNG. Thuộc tính liên kết kind ('like', 'love',...). Khóa chính tổ hợp (user_id, post_id) đảm bảo tính độc quyền cảm xúc.", bold_prefix="Mối kết hợp CẢM XÚC (M:N): ")
    add_bullet(doc, "Liên kết 1:N giữa BÀI ĐĂNG và BÌNH LUẬN (một bài đăng có thể có nhiều bình luận; mỗi bình luận thuộc về duy nhất một bài đăng).", bold_prefix="Mối kết hợp CÓ BÌNH LUẬN (1:N): ")
    add_bullet(doc, "Liên kết 1:N giữa NGƯỜI DÙNG và BÌNH LUẬN (mỗi bình luận do đúng một tác giả viết).", bold_prefix="Mối kết hợp VIẾT BÌNH LUẬN (1:N): ")
    add_bullet(doc, "Liên kết đệ quy 1:N trên thực thể BÌNH LUẬN. Một bình luận cha có thể có nhiều bình luận con (0, N); mỗi bình luận con tham chiếu đến đúng một bình luận cha (0, 1). Bình luận gốc có parent_id = NULL.", bold_prefix="Mối kết hợp TRẢ LỜI BÌNH LUẬN (1:N, Đệ quy): ")
    add_bullet(doc, "Liên kết 1:N giữa NHÓM HỌC TẬP và THƯ MỤC. Mỗi nhóm có thể có nhiều thư mục; mỗi thư mục thuộc về duy nhất một nhóm.", bold_prefix="Mối kết hợp CÓ THƯ MỤC (1:N): ")
    add_bullet(doc, "Liên kết đệ quy 1:N trên thực thể THƯ MỤC. Một thư mục cha có thể chứa nhiều thư mục con; mỗi thư mục con nằm trong đúng một thư mục cha.", bold_prefix="Mối kết hợp THƯ MỤC CON (1:N, Đệ quy): ")
    add_bullet(doc, "Mối quan hệ kế thừa giữa siêu lớp BÀI ĐĂNG và hai lớp con BÀI THẢO LUẬN, BÀI TÀI LIỆU được biểu diễn bằng hình tròn có chữ 'd' (Disjoint). Quy tắc nghiệp vụ quy định tính chất Rời rạc hoàn toàn: Một bài đăng chỉ có thể là Bài thảo luận hoặc Bài tài liệu, không thể đồng thời là cả hai.", bold_prefix="Chuyên môn hóa rời rạc (Disjoint Specialization 'd'): ")

    # --- 1.4 LƯỢC ĐỒ QUAN HỆ VẬT LÝ ---
    add_heading_3(doc, "1.3.3 Đối sánh các Ký hiệu Mô hình hóa EER (Chen, Crow's Foot, UML)")
    add_paragraph(doc, "Trong kỹ nghệ phần mềm và thiết kế CSDL, có 3 phong cách ký hiệu mô hình hóa quan niệm phổ biến:")

    notation_headers = ["Tiêu chí so sánh", "Ký hiệu Chen mở rộng (Chen Notation)", "Ký hiệu Crow's Foot (Martin Notation)", "Sơ đồ Lớp UML (Class Diagram)"]
    notation_data = [
        ["Biểu diễn Thực thể", "Hình chữ nhật có tên thực thể viết hoa.", "Hình chữ nhật chia 2 phần (Tên & Thuộc tính).", "Hình chữ nhật 3 ngăn (Tên, Thuộc tính, Phương thức)."],
        ["Biểu diễn Thuộc tính", "Các hình oval kết nối với thực thể bằng nét thẳng.", "Liệt kê trực tiếp bên trong hình chữ nhật thực thể.", "Liệt kê ở ngăn giữa, kèm kiểu dữ liệu (+/- private)."],
        ["Biểu diễn Mối kết hợp", "Hình thoi liên kết giữa các thực thể.", "Đường thẳng nối trực tiếp với ký hiệu chân quạ.", "Đường liên kết (Association) kèm tên vai trò."],
        ["Ký hiệu Bản số (Cardinality)", "Ghi cặp min-max (0,1), (1,N), (M,N) trên nhánh liên kết.", "Dùng biểu tượng trực quan: vòng tròn (0), gạch đứng (1), chân quạ (N).", "Ghi khoảng chỉ số: 0..1, 1..*, 0..*."],
        ["Biểu diễn Kế thừa (IS-A)", "Hình tròn chứa chữ 'd' (Disjoint) hoặc 'o' (Overlap).", "Không hỗ trợ trực tiếp (phải dùng bảng nối phụ).", "Mũi tên tam giác rỗng trỏ từ lớp con về siêu lớp."],
        ["Phạm vi ứng dụng tối ưu", "Tối ưu cho giảng dạy học thuật, làm rõ bản số và loại thuộc tính.", "Rất phổ biến trong các công cụ CASE thương mại (Erwin, Toad).", "Tối ưu cho lập trình hướng đối tượng và kiến trúc ORM."],
    ]
    add_styled_table(doc, notation_headers, notation_data, [1.4, 1.8, 1.8, 1.8])

    add_heading_2(doc, "1.4 Thiết kế Lược đồ CSDL Quan hệ Vật lý (Physical Relational Schema)")
    add_paragraph(doc, "Từ sơ đồ mức quan niệm EER, nhóm đã chuyển đổi và hoàn thiện Lược đồ quan hệ vật lý tối ưu trên PostgreSQL 18.6. Dưới đây là sơ đồ kiến trúc các bảng dữ liệu vật lý cùng hệ thống khóa chính (PK), khóa ngoại (FK) và các chỉ mục chuyên biệt:")

    add_figure(doc, "docs/relational_schema_diagram.png", "Hình 1.2: Sơ đồ Lược đồ CSDL Quan hệ Vật lý (Physical Relational Schema) trên PostgreSQL 18.6", width_inches=6.5)

    add_paragraph(doc, "Bảng tổng hợp đặc tả 13 bảng vật lý cốt lõi trong hệ thống:")

    tbl_spec_headers = ["Tên bảng vật lý", "Khóa chính (PK)", "Khóa ngoại (FK)", "Ràng buộc kiểm tra (CHECK)", "Mục đích nghiệp vụ"]
    tbl_spec_data = [
        ["users", "user_id (INT)", "—", "email định dạng hợp lệ;\nfriend_count >= 0", "Lưu trữ hồ sơ học viên, thông tin xác thực và bộ đếm bạn bè."],
        ["study_group", "group_id (INT)", "owner_id -> users", "name không rỗng", "Quản trị không gian nhóm học tập và chủ sở hữu sáng lập."],
        ["group_members", "(group_id, user_id)", "group_id -> study_group\nuser_id -> users", "role IN ('owner',\n'mod', 'member')", "Quản lý quan hệ thành viên và quyền hạn trong nhóm."],
        ["friendship", "(user_a, user_b)", "user_a -> users\nuser_b -> users", "user_a < user_b\n(Triệt tiêu trùng lặp)", "Lưu trữ quan hệ bạn bè hai chiều đối xứng theo quy ước chuẩn tắc."],
        ["user_follow", "(follower_id, followed_id)", "follower_id -> users\nfollowed_id -> users", "follower_id <> followed_id", "Lưu trữ quan hệ theo dõi học tập một chiều (đồ thị có hướng)."],
        ["post", "post_id (INT)", "author_id -> users\ngroup_id -> study_group", "post_type IN ('thaoluan',\n'tailieu'); counts >= 0", "Bảng đơn hợp nhất lưu trữ bài viết, cờ khóa và tệp đính kèm."],
        ["post_reaction", "(user_id, post_id)", "user_id -> users\npost_id -> post", "kind IN ('like', 'love',\n'haha', 'wow', 'sad', 'angry')", "Lưu trữ cảm xúc tương tác độc quyền của người dùng trên bài viết."],
        ["comment_adjacency", "comment_id (INT)", "post_id -> post\nauthor_id -> users\nparent_id -> comment_adj", "parent_id <> comment_id", "Mô hình cây 1: Danh sách kề truyền thống, tối ưu cho thao tác ghi."],
        ["comment_path_enum", "comment_id (INT)", "post_id -> post\nauthor_id -> users", "path NOT NULL (ltree)", "Mô hình cây 2: Liệt kê đường dẫn tiền tố kết hợp chỉ mục GiST."],
        ["comment_nested_set", "comment_id (INT)", "post_id -> post\nauthor_id -> users", "lft < rgt", "Mô hình cây 3: Tập lồng nhau, tối ưu cho các phép quét khoảng."],
        ["comment_closure", "(ancestor_id,\ndescendant_id)", "ancestor_id -> comment\ndescendant_id -> comment", "depth >= 0", "Mô hình cây 4: Bảng phụ bao đóng lưu tất cả các cặp tổ tiên - hậu duệ."],
        ["folder", "folder_id (INT)", "group_id -> study_group\nparent_id -> folder", "name không rỗng", "Quản lý cây thư mục tài liệu phân cấp trong từng nhóm học tập."],
        ["notification", "notif_id (INT)", "user_id -> users", "—", "Hệ thống thông báo đẩy thời gian thực về tương tác và kết bạn."],
    ]
    add_styled_table(doc, tbl_spec_headers, tbl_spec_data, [1.4, 1.2, 1.6, 1.3, 1.7])

    # --- 1.5 TỪ ĐIỂN DỮ LIỆU VẬT LÝ CHI TIẾT (DATA DICTIONARY) ---
    add_heading_2(doc, "1.5 Từ điển Dữ liệu Vật lý Toàn diện (Physical Data Dictionary)")
    add_paragraph(doc, "Để đảm bảo tính chuẩn xác cho quá trình cài đặt và bảo trì hệ thống, dưới đây là từ điển dữ liệu chi tiết của 6 bảng dữ liệu trọng yếu nhất trong hệ thống:")

    # Table 1: users
    add_heading_3(doc, "1.5.1 Bảng users (Hồ sơ người dùng)")
    dict_users_headers = ["Tên cột", "Kiểu dữ liệu", "Null?", "Mặc định", "Ràng buộc / Ghi chú", "Mô tả nghiệp vụ"]
    dict_users_data = [
        ["user_id", "SERIAL (INT)", "NO", "nextval()", "PRIMARY KEY", "Mã định danh duy nhất của người dùng"],
        ["email", "VARCHAR(255)", "NO", "None", "UNIQUE, CHECK format", "Địa chỉ hòm thư điện tử đăng nhập"],
        ["password_hash", "VARCHAR(255)", "NO", "None", "BCrypt hash", "Chuỗi mật khẩu băm bảo mật"],
        ["full_name", "VARCHAR(150)", "NO", "None", "NOT NULL", "Họ tên đầy đủ của học viên / giảng viên"],
        ["bio", "TEXT", "YES", "NULL", "—", "Tiểu sử và giới thiệu bản thân ngắn gọn"],
        ["avatar_url", "VARCHAR(500)", "YES", "NULL", "—", "Đường dẫn ảnh đại diện người dùng"],
        ["friend_count", "INT", "NO", "0", "CHECK (friend_count >= 0)", "Bộ đếm dẫn xuất tổng số bạn bè hiện tại"],
        ["created_at", "TIMESTAMPTZ", "NO", "CURRENT_TIMESTAMP", "—", "Thời điểm tạo lập tài khoản"],
    ]
    add_styled_table(doc, dict_users_headers, dict_users_data, [1.3, 1.2, 0.7, 1.3, 1.5, 2.2])

    # Table 2: study_group
    add_heading_3(doc, "1.5.2 Bảng study_group (Nhóm học tập chuyên đề)")
    dict_group_headers = ["Tên cột", "Kiểu dữ liệu", "Null?", "Mặc định", "Ràng buộc / Ghi chú", "Mô tả nghiệp vụ"]
    dict_group_data = [
        ["group_id", "SERIAL (INT)", "NO", "nextval()", "PRIMARY KEY", "Mã định danh duy nhất của nhóm học tập"],
        ["name", "VARCHAR(150)", "NO", "None", "UNIQUE", "Tên chuyên đề nhóm học tập"],
        ["description", "TEXT", "YES", "NULL", "—", "Mô tả mục tiêu và nội dung học thuật nhóm"],
        ["topic", "VARCHAR(100)", "NO", "None", "—", "Lĩnh vực chuyên môn (AI, Web, Data...)"],
        ["owner_id", "INT", "NO", "None", "FK -> users(user_id) ON DELETE RESTRICT", "Trưởng nhóm sáng lập không gian học tập"],
        ["is_private", "BOOLEAN", "NO", "FALSE", "—", "Cờ riêng tư (TRUE: cần duyệt, FALSE: mở)"],
        ["member_count", "INT", "NO", "1", "CHECK (member_count >= 1)", "Số lượng học viên tham gia nhóm"],
        ["created_at", "TIMESTAMPTZ", "NO", "CURRENT_TIMESTAMP", "—", "Thời điểm thành lập nhóm"],
    ]
    add_styled_table(doc, dict_group_headers, dict_group_data, [1.3, 1.2, 0.7, 1.3, 1.5, 2.2])

    # Table 3: post
    add_heading_3(doc, "1.5.3 Bảng post (Bài đăng đơn hợp nhất - Single Table Inheritance)")
    dict_post_headers = ["Tên cột", "Kiểu dữ liệu", "Null?", "Mặc định", "Ràng buộc / Ghi chú", "Mô tả nghiệp vụ"]
    dict_post_data = [
        ["post_id", "SERIAL (INT)", "NO", "nextval()", "PRIMARY KEY", "Mã định danh duy nhất của bài đăng"],
        ["author_id", "INT", "NO", "None", "FK -> users(user_id) ON DELETE CASCADE", "Tác giả biên soạn bài viết"],
        ["group_id", "INT", "YES", "NULL", "FK -> study_group(group_id) ON DELETE CASCADE", "Mã nhóm (NULL nếu đăng trên trang cá nhân)"],
        ["post_type", "VARCHAR(20)", "NO", "'thaoluan'", "CHECK IN ('thaoluan', 'tailieu')", "Bộ phân loại kiểu bài đăng đa hình"],
        ["title", "VARCHAR(255)", "NO", "None", "—", "Tiêu đề bài viết thảo luận / chia sẻ tài liệu"],
        ["content", "TEXT", "NO", "None", "—", "Nội dung chi tiết của bài đăng"],
        ["is_closed", "BOOLEAN", "YES", "FALSE", "Dành cho post_type = 'thaoluan'", "Cờ đánh dấu bài thảo luận đã kết thúc"],
        ["file_url", "VARCHAR(500)", "YES", "NULL", "Dành cho post_type = 'tailieu'", "Đường dẫn tải tài liệu chuyên đề đính kèm"],
        ["file_size_kb", "INT", "YES", "NULL", "CHECK (file_size_kb > 0)", "Dung lượng tệp tài liệu (tính bằng KB)"],
        ["comment_count", "INT", "NO", "0", "CHECK (comment_count >= 0)", "Bộ đếm dẫn xuất tổng số phản hồi"],
        ["reaction_count", "INT", "NO", "0", "CHECK (reaction_count >= 0)", "Bộ đếm dẫn xuất tổng số tương tác cảm xúc"],
        ["created_at", "TIMESTAMPTZ", "NO", "CURRENT_TIMESTAMP", "—", "Thời điểm đăng tải bài viết"],
    ]
    add_styled_table(doc, dict_post_headers, dict_post_data, [1.3, 1.2, 0.7, 1.3, 1.5, 2.2])

    # Table 4: friendship
    add_heading_3(doc, "1.5.4 Bảng friendship (Quan hệ kết bạn chuẩn tắc)")
    dict_friend_headers = ["Tên cột", "Kiểu dữ liệu", "Null?", "Mặc định", "Ràng buộc / Ghi chú", "Mô tả nghiệp vụ"]
    dict_friend_data = [
        ["user_a", "INT", "NO", "None", "PK, FK -> users, CHECK(user_a < user_b)", "ID người dùng thứ nhất (nhỏ hơn)"],
        ["user_b", "INT", "NO", "None", "PK, FK -> users, CHECK(user_a < user_b)", "ID người dùng thứ hai (lớn hơn)"],
        ["status", "VARCHAR(20)", "NO", "'accepted'", "CHECK IN ('pending', 'accepted')", "Trạng thái quan hệ kết bạn"],
        ["created_at", "TIMESTAMPTZ", "NO", "CURRENT_TIMESTAMP", "—", "Thời điểm thiết lập quan hệ kết bạn"],
    ]
    add_styled_table(doc, dict_friend_headers, dict_friend_data, [1.3, 1.2, 0.7, 1.3, 1.5, 2.2])

    # Table 5: post_reaction
    add_heading_3(doc, "1.5.5 Bảng post_reaction (Cảm xúc tương tác bài đăng)")
    dict_react_headers = ["Tên cột", "Kiểu dữ liệu", "Null?", "Mặc định", "Ràng buộc / Ghi chú", "Mô tả nghiệp vụ"]
    dict_react_data = [
        ["user_id", "INT", "NO", "None", "PK (Part 1), FK -> users(user_id)", "Người dùng thực hiện tương tác"],
        ["post_id", "INT", "NO", "None", "PK (Part 2), FK -> post(post_id)", "Bài viết nhận tương tác"],
        ["kind", "VARCHAR(20)", "NO", "'like'", "CHECK IN ('like','love','haha','wow','sad','angry')", "Loại cảm xúc độc quyền"],
        ["created_at", "TIMESTAMPTZ", "NO", "CURRENT_TIMESTAMP", "—", "Thời điểm bày tỏ cảm xúc"],
    ]
    add_styled_table(doc, dict_react_headers, dict_react_data, [1.3, 1.2, 0.7, 1.3, 1.5, 2.2])

    # Table 6: comment_path_enum
    add_heading_3(doc, "1.5.6 Bảng comment_path_enum (Mô hình cây Path Enumeration)")
    dict_ltree_headers = ["Tên cột", "Kiểu dữ liệu", "Null?", "Mặc định", "Ràng buộc / Ghi chú", "Mô tả nghiệp vụ"]
    dict_ltree_data = [
        ["comment_id", "SERIAL (INT)", "NO", "nextval()", "PRIMARY KEY", "Mã định danh duy nhất của bình luận"],
        ["post_id", "INT", "NO", "None", "FK -> post(post_id) ON DELETE CASCADE", "Bài đăng chứa chuỗi bình luận"],
        ["author_id", "INT", "NO", "None", "FK -> users(user_id) ON DELETE CASCADE", "Tác giả viết bình luận"],
        ["content", "TEXT", "NO", "None", "NOT NULL", "Nội dung phản hồi học thuật"],
        ["path", "LTREE", "NO", "None", "GIST INDEX, NOT NULL", "Đường dẫn tiền tố tổ tiên (VD: '1.4.12')"],
        ["depth", "INT", "NO", "1", "CHECK (depth >= 1)", "Độ sâu mức phân cấp của bình luận"],
        ["created_at", "TIMESTAMPTZ", "NO", "CURRENT_TIMESTAMP", "—", "Thời điểm gửi bình luận"],
    ]
    add_styled_table(doc, dict_ltree_headers, dict_ltree_data, [1.3, 1.2, 0.7, 1.3, 1.5, 2.2])

    # Table 7: group_members
    add_heading_3(doc, "1.5.7 Bảng group_members (Quan hệ thành viên nhóm học tập)")
    dict_gm_headers = ["Tên cột", "Kiểu dữ liệu", "Null?", "Mặc định", "Ràng buộc / Ghi chú", "Mô tả nghiệp vụ"]
    dict_gm_data = [
        ["group_id", "INT", "NO", "None", "PK (Part 1), FK -> study_group ON DELETE CASCADE", "Nhóm học tập tham gia"],
        ["user_id", "INT", "NO", "None", "PK (Part 2), FK -> users ON DELETE CASCADE", "Học viên là thành viên nhóm"],
        ["role", "VARCHAR(20)", "NO", "'member'", "CHECK IN ('owner', 'mod', 'member')", "Vai trò phân quyền trong nhóm"],
        ["joined_at", "TIMESTAMPTZ", "NO", "CURRENT_TIMESTAMP", "—", "Thời điểm phê duyệt gia nhập nhóm"],
    ]
    add_styled_table(doc, dict_gm_headers, dict_gm_data, [1.3, 1.2, 0.7, 1.3, 1.5, 2.2])

    # Table 8: user_follow
    add_heading_3(doc, "1.5.8 Bảng user_follow (Quan hệ theo dõi học thuật có hướng)")
    dict_uf_headers = ["Tên cột", "Kiểu dữ liệu", "Null?", "Mặc định", "Ràng buộc / Ghi chú", "Mô tả nghiệp vụ"]
    dict_uf_data = [
        ["follower_id", "INT", "NO", "None", "PK (Part 1), FK -> users ON DELETE CASCADE", "Người dùng thực hiện hành vi theo dõi"],
        ["followed_id", "INT", "NO", "None", "PK (Part 2), FK -> users ON DELETE CASCADE", "Người dùng được theo dõi (học viên/giảng viên)"],
        ["created_at", "TIMESTAMPTZ", "NO", "CURRENT_TIMESTAMP", "CHECK (follower_id <> followed_id)", "Thời điểm bấm theo dõi"],
    ]
    add_styled_table(doc, dict_uf_headers, dict_uf_data, [1.3, 1.2, 0.7, 1.3, 1.5, 2.2])

    # Table 9: comment_adjacency
    add_heading_3(doc, "1.5.9 Bảng comment_adjacency (Mô hình cây Danh sách kề)")
    dict_cadj_headers = ["Tên cột", "Kiểu dữ liệu", "Null?", "Mặc định", "Ràng buộc / Ghi chú", "Mô tả nghiệp vụ"]
    dict_cadj_data = [
        ["comment_id", "SERIAL (INT)", "NO", "nextval()", "PRIMARY KEY", "Mã định danh duy nhất của bình luận"],
        ["post_id", "INT", "NO", "None", "FK -> post(post_id) ON DELETE CASCADE", "Bài đăng chứa bình luận"],
        ["author_id", "INT", "NO", "None", "FK -> users(user_id) ON DELETE CASCADE", "Tác giả của bình luận"],
        ["parent_id", "INT", "YES", "NULL", "FK -> comment_adjacency(comment_id) ON DELETE CASCADE", "Khóa ngoại trỏ trực tiếp đến bình luận cha"],
        ["content", "TEXT", "NO", "None", "NOT NULL", "Nội dung phản hồi học thuật"],
        ["created_at", "TIMESTAMPTZ", "NO", "CURRENT_TIMESTAMP", "—", "Thời điểm tạo bình luận"],
    ]
    add_styled_table(doc, dict_cadj_headers, dict_cadj_data, [1.3, 1.2, 0.7, 1.3, 1.5, 2.2])

    # Table 10: comment_nested_set
    add_heading_3(doc, "1.5.10 Bảng comment_nested_set (Mô hình cây Tập lồng nhau)")
    dict_cns_headers = ["Tên cột", "Kiểu dữ liệu", "Null?", "Mặc định", "Ràng buộc / Ghi chú", "Mô tả nghiệp vụ"]
    dict_cns_data = [
        ["comment_id", "SERIAL (INT)", "NO", "nextval()", "PRIMARY KEY", "Mã định danh duy nhất của bình luận"],
        ["post_id", "INT", "NO", "None", "FK -> post(post_id) ON DELETE CASCADE", "Bài đăng chứa bình luận"],
        ["author_id", "INT", "NO", "None", "FK -> users(user_id) ON DELETE CASCADE", "Tác giả của bình luận"],
        ["lft", "INT", "NO", "None", "CHECK (lft > 0), INDEX (lft, rgt)", "Tọa độ duyệt trái theo thứ tự Pre-order"],
        ["rgt", "INT", "NO", "None", "CHECK (lft < rgt)", "Tọa độ duyệt phải theo thứ tự Pre-order"],
        ["content", "TEXT", "NO", "None", "NOT NULL", "Nội dung phản hồi học thuật"],
        ["created_at", "TIMESTAMPTZ", "NO", "CURRENT_TIMESTAMP", "—", "Thời điểm tạo bình luận"],
    ]
    add_styled_table(doc, dict_cns_headers, dict_cns_data, [1.3, 1.2, 0.7, 1.3, 1.5, 2.2])

    # Table 11: comment_closure
    add_heading_3(doc, "1.5.11 Bảng comment_closure (Bảng phụ Bao đóng tổ tiên - hậu duệ)")
    dict_ccl_headers = ["Tên cột", "Kiểu dữ liệu", "Null?", "Mặc định", "Ràng buộc / Ghi chú", "Mô tả nghiệp vụ"]
    dict_ccl_data = [
        ["ancestor_id", "INT", "NO", "None", "PK (Part 1), FK -> comment_closure_data", "Mã bình luận đóng vai trò tổ tiên"],
        ["descendant_id", "INT", "NO", "None", "PK (Part 2), FK -> comment_closure_data", "Mã bình luận đóng vai trò hậu duệ"],
        ["depth", "INT", "NO", "0", "CHECK (depth >= 0)", "Khoảng cách thế hệ (0: chính nó, 1: con, ...)"],
    ]
    add_styled_table(doc, dict_ccl_headers, dict_ccl_data, [1.3, 1.2, 0.7, 1.3, 1.5, 2.2])

    # Table 12: folder
    add_heading_3(doc, "1.5.12 Bảng folder (Cây thư mục tài liệu học tập)")
    dict_fld_headers = ["Tên cột", "Kiểu dữ liệu", "Null?", "Mặc định", "Ràng buộc / Ghi chú", "Mô tả nghiệp vụ"]
    dict_fld_data = [
        ["folder_id", "SERIAL (INT)", "NO", "nextval()", "PRIMARY KEY", "Mã định danh duy nhất của thư mục"],
        ["group_id", "INT", "NO", "None", "FK -> study_group(group_id) ON DELETE CASCADE", "Nhóm học tập sở hữu cây thư mục"],
        ["parent_id", "INT", "YES", "NULL", "FK -> folder(folder_id) ON DELETE CASCADE", "Thư mục cha (NULL nếu là thư mục gốc nhóm)"],
        ["name", "VARCHAR(150)", "NO", "None", "UNIQUE(group_id, parent_id, name)", "Tên thư mục tài liệu"],
        ["created_at", "TIMESTAMPTZ", "NO", "CURRENT_TIMESTAMP", "—", "Thời điểm tạo lập thư mục"],
    ]
    add_styled_table(doc, dict_fld_headers, dict_fld_data, [1.3, 1.2, 0.7, 1.3, 1.5, 2.2])

    # Table 13: notification
    add_heading_3(doc, "1.5.13 Bảng notification (Thông báo hệ thống thời gian thực)")
    dict_notif_headers = ["Tên cột", "Kiểu dữ liệu", "Null?", "Mặc định", "Ràng buộc / Ghi chú", "Mô tả nghiệp vụ"]
    dict_notif_data = [
        ["notif_id", "SERIAL (INT)", "NO", "nextval()", "PRIMARY KEY", "Mã định danh duy nhất của thông báo"],
        ["user_id", "INT", "NO", "None", "FK -> users(user_id) ON DELETE CASCADE", "Người dùng tiếp nhận thông báo"],
        ["message", "TEXT", "NO", "None", "NOT NULL", "Nội dung chi tiết của thông báo"],
        ["is_read", "BOOLEAN", "NO", "FALSE", "—", "Trạng thái đã đọc (TRUE/FALSE)"],
        ["created_at", "TIMESTAMPTZ", "NO", "CURRENT_TIMESTAMP", "—", "Thời điểm hệ thống phát sinh thông báo"],
    ]
    add_styled_table(doc, dict_notif_headers, dict_notif_data, [1.3, 1.2, 0.7, 1.3, 1.5, 2.2])

    # --- 1.6 SO SÁNH 3 PHƯƠNG ÁN ÁNH XẠ KẾ THỪA ---
    add_heading_2(doc, "1.6 So sánh và lựa chọn 3 phương án ánh xạ kế thừa (Inheritance Mapping)")
    add_paragraph(doc, "Một trong những quyết định kiến trúc then chốt ở mức thiết kế logic là lựa chọn chiến lược ánh xạ quan hệ kế thừa (IS-A) giữa siêu lớp BÀI ĐĂNG (post) và hai lớp con BÀI THẢO LUẬN, BÀI TÀI LIỆU vào các bảng quan hệ. Có 3 phương án kinh điển:")
    add_bullet(doc, "Gộp tất cả các thuộc tính của siêu lớp và mọi phân lớp con vào trong một bảng duy nhất (post). Bổ sung thêm một cột phân loại (Discriminator Column) post_type VARCHAR(20) CHECK (post_type IN ('thaoluan', 'tailieu')). Các thuộc tính đặc thù của lớp con này sẽ mang giá trị NULL ở các dòng thuộc lớp con khác.", bold_prefix="Phương án 1: Bảng Đơn (Single Table Inheritance): ")
    add_bullet(doc, "Mỗi lớp trong cây kế thừa được ánh xạ thành một bảng vật lý riêng biệt. Bảng siêu lớp post chứa các thuộc tính dùng chung. Các bảng con post_discussion và post_document chỉ chứa các thuộc tính đặc thù của riêng mình. Khóa chính của bảng con vừa là khóa chính vừa là khóa ngoại tham chiếu trực tiếp đến post(post_id).", bold_prefix="Phương án 2: Bảng Nối (Class Table / Joined Table Inheritance): ")
    add_bullet(doc, "Không tạo bảng cho siêu lớp trừu tượng. Mỗi lớp con cụ thể được ánh xạ thành một bảng hoàn chỉnh độc lập (post_discussion và post_document). Mỗi bảng con sao chép lại toàn bộ các cột thuộc tính của siêu lớp.", bold_prefix="Phương án 3: Bảng Riêng cho từng Lớp cụ thể (Concrete Table / Table per Class): ")

    add_paragraph(doc, "Bảng ma trận đối sánh chi tiết 7 tiêu chí kỹ thuật giữa 3 phương án:")

    inherit_headers = ["Tiêu chí đánh giá kỹ thuật", "Phương án 1: Bảng Đơn\n(Single Table)", "Phương án 2: Bảng Nối\n(Class Table / Joined Table)", "Phương án 3: Bảng Riêng Cụ Thể\n(Concrete Table / Table per Class)"]
    inherit_rows = [
        ["Số lượng bảng vật lý", "1 bảng duy nhất (post)", "3 bảng (post, post_discussion,\npost_document)", "2 bảng (post_discussion,\npost_document)"],
        ["Hiệu năng đọc Bảng tin Feed\n(Polymorphic Queries)", "TỐI ƯU TUYỆT ĐỐI O(1).\nChỉ cần SELECT trên 1 bảng,\nkhông tốn bất kỳ phép JOIN nào.", "KÉM. Bắt buộc phải LEFT JOIN\n3 bảng lại với nhau để lấy đầy đủ\nthông tin thuộc tính bài viết.", "RẤT KÉM. Bắt buộc phải dùng\nUNION ALL kết hợp cả 2 bảng con,\nkhông thể đánh chỉ mục xuyên suốt."],
        ["Hiệu năng đọc đơn hình\n(Query 1 lớp con cụ thể)", "Rất nhanh: Chỉ cần thêm điều kiện\nWHERE post_type = 'tailieu'.", "Nhanh: INNER JOIN giữa bảng post\nvà bảng con tương ứng.", "Cực nhanh: Chỉ cần SELECT trực tiếp\ntrên bảng con cụ thể đó."],
        ["Lãng phí dung lượng đĩa\n(NULL Values Overhead)", "Có lãng phí: Các dòng thảo luận\nsẽ bị NULL ở cột file_url, định dạng.", "KHÔNG LÃNG PHÍ: Mỗi bảng\nchỉ lưu trữ đúng thuộc tính của mình.", "KHÔNG LÃNG PHÍ: Không có bất kỳ\ncột NULL dư thừa nào."],
        ["Ràng buộc tính toàn vẹn DDL\n(NOT NULL Constraints)", "Hạn chế: Không thể đặt NOT NULL\ntrên các cột riêng ở mức schema DDL\n(phải dùng CHECK có điều kiện).", "HOÀN HẢO: Dễ dàng đặt NOT NULL\nvà CHECK constraints chặt chẽ\ntrên từng bảng con riêng biệt.", "HOÀN HẢO: Mọi thuộc tính bắt buộc\nđều được áp dụng NOT NULL\ntrực tiếp trên schema DDL."],
        ["Quản lý Khóa chính toàn cục\n(Global Primary Key)", "Rất đơn giản: Dùng 1 chuỗi tự tăng\npost_id duy nhất cho toàn hệ thống.", "Đơn giản: post_id ở bảng con tham chiếu\ntrực tiếp đến post_id của bảng cha.", "RẤT PHỨC TẠP: Cần sequence chung\nđể tránh trùng lặp post_id giữa 2 bảng."],
        ["Khả năng mở rộng lớp con mới\n(Schema Evolution)", "RẤT DỄ DÀNG: Chỉ cần thêm cột mới\nhoặc dùng cột mở rộng JSONB mà\nkhông cần tạo bảng hay sửa JOIN.", "TỐN KÉM: Mỗi lớp con mới đòi hỏi\ntạo 1 bảng vật lý và viết lại toàn bộ\ncác câu lệnh JOIN đa hình.", "TỐN KÉM: Mỗi lớp con mới phải tạo\n1 bảng và sửa lại toàn bộ câu lệnh\nUNION ALL trên toàn hệ thống."],
    ]
    add_styled_table(doc, inherit_headers, inherit_rows, [1.6, 1.8, 1.8, 1.8])

    add_callout_box(doc, "LUẬN CHỨNG LỰA CHỌN KIẾN TRÚC CỦA NHÓM:\n"
                         "Sau khi cân nhắc kỹ lưỡng đặc thù của mạng xã hội học tập, nhóm quyết định lựa chọn PHƯƠNG ÁN 1 (SINGLE TABLE INHERITANCE) cho thực thể BÀI ĐĂNG (post) vì các lý do thực tiễn sau:\n"
                         "1. Tỷ lệ truy vấn áp đảo: Thao tác tải Bảng tin (Social Feed) duyệt qua tất cả các bài viết đa hình chiếm tới hơn 90% tổng số truy vấn của người dùng. Phương án 1 loại bỏ hoàn toàn các phép JOIN bảng phụ, cho phép quét tuần tự hoặc quét chỉ mục cực nhanh với độ phức tạp O(1).\n"
                         "2. Cơ chế tối ưu hóa NULL của PostgreSQL: Trong kiến trúc lưu trữ đĩa của PostgreSQL, các trường mang giá trị NULL không chiếm dung lượng lưu trữ thực tế mà chỉ được biểu diễn bằng 1 bit trong phần mặt nạ bit Null Bitmap của tiêu đề dòng (Tuple Header). Do đó, chi phí lãng phí đĩa của Single Table trong PostgreSQL là gần như không đáng kể.\n"
                         "3. Khắc phục hạn chế ràng buộc bằng CHECK constraint: Nhóm sử dụng ràng buộc CHECK (post_type = 'tailieu' OR (file_url IS NULL)) để đảm bảo tính toàn vẹn nghiệp vụ mà không cần chia tách thành nhiều bảng vật lý phức tạp.",
                    "QUYẾT ĐỊNH THIẾT KẾ ÁNH XẠ KẾ THỪA CHO BÀI ĐĂNG")

    # --- 1.7 KỊCH BẢN DDL RÀNG BUỘC TOÀN VẸN VẬT LÝ ---
    add_heading_2(doc, "1.7 Kịch bản DDL Ràng buộc Toàn vẹn và Lược đồ Vật lý chuẩn (PostgreSQL 18.6)")
    add_paragraph(doc, "Dưới đây là trích đoạn mã DDL định nghĩa các ràng buộc toàn vẹn thực thể (PK), toàn vẹn tham chiếu (FK kèm ON DELETE rules) và toàn vẹn miền giá trị (CHECK constraints) được áp dụng trực tiếp vào cơ sở dữ liệu:")

    add_code_block(doc, "-- RÀNG BUỘC TOÀN VẸN BẢNG USERS\n"
                        "ALTER TABLE users \n"
                        "    ADD CONSTRAINT chk_user_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),\n"
                        "    ADD CONSTRAINT chk_user_friend_count CHECK (friend_count >= 0);\n\n"
                        "-- RÀNG BUỘC QUAN HỆ BẠN BÈ CHUẨN TẮC (TRIỆT TIÊU TRÙNG LẶP)\n"
                        "ALTER TABLE friendship\n"
                        "    ADD CONSTRAINT pk_friendship PRIMARY KEY (user_a, user_b),\n"
                        "    ADD CONSTRAINT chk_canonical_order CHECK (user_a < user_b),\n"
                        "    ADD CONSTRAINT fk_friend_user_a FOREIGN KEY (user_a) REFERENCES users(user_id) ON DELETE CASCADE,\n"
                        "    ADD CONSTRAINT fk_friend_user_b FOREIGN KEY (user_b) REFERENCES users(user_id) ON DELETE CASCADE;\n\n"
                        "-- RÀNG BUỘC THEO DÕI HỌC THUẬT (ĐỒ THỊ CÓ HƯỚNG)\n"
                        "ALTER TABLE user_follow\n"
                        "    ADD CONSTRAINT pk_user_follow PRIMARY KEY (follower_id, followed_id),\n"
                        "    ADD CONSTRAINT chk_no_self_follow CHECK (follower_id <> followed_id),\n"
                        "    ADD CONSTRAINT fk_follow_follower FOREIGN KEY (follower_id) REFERENCES users(user_id) ON DELETE CASCADE,\n"
                        "    ADD CONSTRAINT fk_follow_followed FOREIGN KEY (followed_id) REFERENCES users(user_id) ON DELETE CASCADE;\n\n"
                        "-- RÀNG BUỘC CHUYÊN MÔN HÓA BẢNG POST (SINGLE TABLE INHERITANCE)\n"
                        "ALTER TABLE post\n"
                        "    ADD CONSTRAINT chk_post_type CHECK (post_type IN ('thaoluan', 'tailieu')),\n"
                        "    ADD CONSTRAINT chk_document_file_url CHECK (post_type <> 'tailieu' OR file_url IS NOT NULL),\n"
                        "    ADD CONSTRAINT chk_post_counts CHECK (comment_count >= 0 AND reaction_count >= 0);\n\n"
                        "-- RÀNG BUỘC ĐỘC QUYỀN CẢM XÚC\n"
                        "ALTER TABLE post_reaction\n"
                        "    ADD CONSTRAINT pk_post_reaction PRIMARY KEY (user_id, post_id),\n"
                        "    ADD CONSTRAINT chk_reaction_kind CHECK (kind IN ('like', 'love', 'haha', 'wow', 'sad', 'angry'));",
                    "Kịch bản DDL thiết lập hệ thống ràng buộc toàn vẹn trên PostgreSQL 18.6")

    # --- 1.8 KỊCH BẢN DDL KHỞI TẠO TOÀN BỘ 13 BẢNG VẬT LÝ ---
    add_heading_2(doc, "1.8 Kịch bản DDL Khởi tạo Toàn bộ 13 Bảng Dữ liệu Vật lý (PostgreSQL 18.6)")
    add_paragraph(doc, "Dưới đây là mã nguồn DDL khởi tạo toàn bộ 13 bảng dữ liệu vật lý hoàn chỉnh, bao gồm các kiểu dữ liệu tối ưu, khóa chính tự tăng IDENTITY, khóa ngoại liên kết cascade, và các ràng buộc toàn vẹn miền giá trị:")

    add_code_block(doc, "-- ========================================================\n"
                        "-- PHÂN HỆ 1: NGƯỜI DÙNG & TƯƠNG TÁC XÃ HỘI BẠN BÈ\n"
                        "-- ========================================================\n"
                        "CREATE TABLE IF NOT EXISTS users (\n"
                        "    user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n"
                        "    email VARCHAR(255) NOT NULL UNIQUE,\n"
                        "    password_hash VARCHAR(255) NOT NULL,\n"
                        "    full_name VARCHAR(150) NOT NULL,\n"
                        "    bio TEXT,\n"
                        "    avatar_url VARCHAR(500),\n"
                        "    friend_count INT NOT NULL DEFAULT 0 CHECK (friend_count >= 0),\n"
                        "    reputation INT NOT NULL DEFAULT 0,\n"
                        "    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()\n"
                        ");\n\n"
                        "CREATE TABLE IF NOT EXISTS friendship (\n"
                        "    user_a INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,\n"
                        "    user_b INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,\n"
                        "    status VARCHAR(20) NOT NULL DEFAULT 'accepted' CHECK (status IN ('pending', 'accepted')),\n"
                        "    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),\n"
                        "    PRIMARY KEY (user_a, user_b),\n"
                        "    CONSTRAINT chk_canonical_friend CHECK (user_a < user_b)\n"
                        ");\n\n"
                        "CREATE TABLE IF NOT EXISTS user_follow (\n"
                        "    follower_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,\n"
                        "    followed_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,\n"
                        "    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),\n"
                        "    PRIMARY KEY (follower_id, followed_id),\n"
                        "    CONSTRAINT chk_no_self_follow CHECK (follower_id <> followed_id)\n"
                        ");\n\n"
                        "-- ========================================================\n"
                        "-- PHÂN HỆ 2: NHÓM HỌC TẬP & THÀNH VIÊN\n"
                        "-- ========================================================\n"
                        "CREATE TABLE IF NOT EXISTS study_group (\n"
                        "    group_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n"
                        "    name VARCHAR(150) NOT NULL UNIQUE,\n"
                        "    description TEXT,\n"
                        "    topic VARCHAR(100) NOT NULL,\n"
                        "    owner_id INT NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,\n"
                        "    is_private BOOLEAN NOT NULL DEFAULT FALSE,\n"
                        "    member_count INT NOT NULL DEFAULT 1 CHECK (member_count >= 1),\n"
                        "    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()\n"
                        ");\n\n"
                        "CREATE TABLE IF NOT EXISTS group_members (\n"
                        "    group_id INT NOT NULL REFERENCES study_group(group_id) ON DELETE CASCADE,\n"
                        "    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,\n"
                        "    role VARCHAR(20) NOT NULL DEFAULT 'member' CHECK (role IN ('owner', 'mod', 'member')),\n"
                        "    joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),\n"
                        "    PRIMARY KEY (group_id, user_id)\n"
                        ");\n\n"
                        "-- ========================================================\n"
                        "-- PHÂN HỆ 3: BÀI ĐĂNG ĐA HÌNH & TƯƠNG TÁC CẢM XÚC\n"
                        "-- ========================================================\n"
                        "CREATE TABLE IF NOT EXISTS post (\n"
                        "    post_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n"
                        "    author_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,\n"
                        "    group_id INT REFERENCES study_group(group_id) ON DELETE CASCADE,\n"
                        "    post_type VARCHAR(20) NOT NULL DEFAULT 'thaoluan' CHECK (post_type IN ('thaoluan', 'tailieu')),\n"
                        "    title VARCHAR(255) NOT NULL,\n"
                        "    content TEXT NOT NULL,\n"
                        "    is_closed BOOLEAN DEFAULT FALSE,\n"
                        "    file_url VARCHAR(500),\n"
                        "    file_size_kb INT CHECK (file_size_kb IS NULL OR file_size_kb > 0),\n"
                        "    metadata JSONB,\n"
                        "    comment_count INT NOT NULL DEFAULT 0 CHECK (comment_count >= 0),\n"
                        "    reaction_count INT NOT NULL DEFAULT 0 CHECK (reaction_count >= 0),\n"
                        "    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),\n"
                        "    CONSTRAINT chk_post_document_rule CHECK (post_type <> 'tailieu' OR file_url IS NOT NULL)\n"
                        ");\n\n"
                        "CREATE TABLE IF NOT EXISTS post_reaction (\n"
                        "    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,\n"
                        "    post_id INT NOT NULL REFERENCES post(post_id) ON DELETE CASCADE,\n"
                        "    kind VARCHAR(20) NOT NULL DEFAULT 'like' CHECK (kind IN ('like', 'love', 'haha', 'wow', 'sad', 'angry')),\n"
                        "    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),\n"
                        "    PRIMARY KEY (user_id, post_id)\n"
                        ");\n\n"
                        "-- ========================================================\n"
                        "-- PHÂN HỆ 4: THƯ MỤC & THÔNG BÁO\n"
                        "-- ========================================================\n"
                        "CREATE TABLE IF NOT EXISTS folder (\n"
                        "    folder_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n"
                        "    group_id INT NOT NULL REFERENCES study_group(group_id) ON DELETE CASCADE,\n"
                        "    parent_id INT REFERENCES folder(folder_id) ON DELETE CASCADE,\n"
                        "    name VARCHAR(150) NOT NULL,\n"
                        "    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),\n"
                        "    UNIQUE (group_id, parent_id, name)\n"
                        ");\n\n"
                        "CREATE TABLE IF NOT EXISTS notification (\n"
                        "    notif_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n"
                        "    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,\n"
                        "    message TEXT NOT NULL,\n"
                        "    is_read BOOLEAN NOT NULL DEFAULT FALSE,\n"
                        "    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()\n"
                        ");",
                    "Toàn bộ mã nguồn DDL khởi tạo các bảng vật lý cốt lõi trên PostgreSQL 18.6")

    doc.add_page_break()
