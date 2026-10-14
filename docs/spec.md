# ĐẶC TẢ NGHIỆP VỤ & TỪ ĐIỂN DỮ LIỆU (SPEC.MD)

> **Môn học:** Cơ sở dữ liệu nâng cao  
> **Đề tài 17:** Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng mạng xã hội học tập  
> **Người phụ trách chính:** TV1 - Trần Quang *(Leader)*  
> **Hỗ trợ:** TV2 (Hưng), TV3 (Hữu) | **Review:** TV4 (Chương), TV5 (Quỳnh)  
> **Mục tiêu:** Cung cấp tài liệu đặc tả nghiệp vụ chuẩn xác, chặt chẽ làm căn cứ xây dựng mô hình EER, phân tích phụ thuộc hàm, chuẩn hóa CSDL và hiện thực các ràng buộc toàn vẹn trên hệ quản trị PostgreSQL.

---

## 1. DANH SÁCH 10 QUY TẮC NGHIỆP VỤ (BUSINESS RULES - BR1 ĐẾN BR10)

Mỗi quy tắc nghiệp vụ dưới đây được mô tả rõ bối cảnh, mục đích, cơ chế thực thi kỹ thuật trong CSDL PostgreSQL và kịch bản vi phạm kèm mã lỗi/phản hồi kỳ vọng.

---

### BR1: Tính duy nhất và định danh tài khoản người dùng
- **Mô tả nghiệp vụ:** Mỗi người dùng khi đăng ký tham gia mạng xã hội học tập phải cung cấp một địa chỉ email hợp lệ và duy nhất trên toàn hệ thống. Không cho phép hai tài khoản dùng chung một email.
- **Bối cảnh & Mục đích:** Đảm bảo định danh duy nhất cho việc xác thực, đăng nhập và liên lạc với người dùng; ngăn ngừa việc tạo tài khoản rác trùng lặp.
- **Cơ chế thực thi kỹ thuật:**
  - Ràng buộc mức cột: `UNIQUE(email)` và `NOT NULL` trên bảng `users`.
  - Định dạng email được kiểm soát thông qua ràng buộc kiểm tra: `CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')`.
- **Kịch bản kiểm thử vi phạm:**
  - Thực hiện `INSERT` người dùng mới với email đã tồn tại.
  - *Kết quả kỳ vọng:* PostgreSQL báo lỗi vi phạm khóa duy nhất (Error Code: `23505 - unique_violation`).

---

### BR2: Quan hệ kết bạn hai chiều (Vô hướng, Không đối xứng dòng, Không tự kết bạn)
- **Mô tả nghiệp vụ:** Quan hệ kết bạn giữa hai người dùng là quan hệ hai chiều đối xứng (nếu A là bạn của B thì B đương nhiên là bạn của A). Hệ thống không cho phép một người dùng tự kết bạn với chính mình. Mỗi cặp bạn bè chỉ được lưu trữ đúng **một bản ghi duy nhất** để tối ưu hóa không gian lưu trữ và đảm bảo tính nhất quán dữ liệu.
- **Bối cảnh & Mục đích:** Tránh dị thường lưu lặp hai chiều `(A, B)` và `(B, A)` gây sai lệch số lượng bạn bè và tốn dung lượng bảng.
- **Cơ chế thực thi kỹ thuật:**
  - Quy ước chuẩn hóa thứ tự định danh: `user_a < user_b`.
  - Khóa chính kết hợp: `PRIMARY KEY (user_a, user_b)`.
  - Ràng buộc toàn vẹn: `CHECK (user_a < user_b)` trên bảng `friendship`.
  - Thủ tục lưu trữ `proc_add_friend(u1, u2)` tự động hoán vị `LEAST(u1, u2)` và `GREATEST(u1, u2)` trước khi ghi dữ liệu.
  - View logic `friend_edge` thực hiện `UNION ALL` phục vụ các thuật toán duyệt đồ thị 2 chiều.
- **Kịch bản kiểm thử vi phạm:**
  - Chèn bản ghi `user_a = 5, user_b = 2` hoặc `user_a = 3, user_b = 3`.
  - *Kết quả kỳ vọng:* Lỗi vi phạm `CHECK constraint` (Error Code: `23514 - check_violation`).

---

### BR3: Quan hệ theo dõi học tập (Đồ thị có hướng, Không tự theo dõi)
- **Mô tả nghiệp vụ:** Người dùng có thể bấm theo dõi (Follow) một người dùng khác để nhận thông báo về các bài viết, tài liệu học tập của người đó. Quan hệ theo dõi là quan hệ có hướng (A theo dõi B không suy ra B theo dõi A). Một người dùng không được phép tự theo dõi chính mình và không thể theo dõi một người nhiều lần.
- **Bối cảnh & Mục đích:** Phục vụ tính năng mạng xã hội tri thức, phân biệt rõ giữa "bạn bè hai chiều" và "theo dõi một chiều".
- **Cơ chế thực thi kỹ thuật:**
  - Khóa chính kết hợp: `PRIMARY KEY (follower_id, followee_id)` trên bảng `follow`.
  - Khóa ngoại: `FOREIGN KEY (follower_id) REFERENCES users(user_id) ON DELETE CASCADE` và `FOREIGN KEY (followee_id) REFERENCES users(user_id) ON DELETE CASCADE`.
  - Ràng buộc kiểm tra: `CHECK (follower_id <> followee_id)`.
- **Kịch bản kiểm thử vi phạm:**
  - Thử chèn `follower_id = 1, followee_id = 1` hoặc chèn trùng cặp `(1, 2)` hai lần.
  - *Kết quả kỳ vọng:* Vi phạm `check_violation` hoặc `unique_violation`.

---

### BR4: Tính sở hữu và vai trò thành viên trong nhóm học tập
- **Mô tả nghiệp vụ:** Mỗi nhóm học tập (Study Group) được khởi tạo bởi đúng một người dùng - người này đóng vai trò là Chủ nhóm (Owner). Chủ nhóm bắt buộc phải là một thành viên của nhóm với vai trò `'owner'`. Vai trò của người dùng trong nhóm nhận một trong ba giá trị: `'owner'`, `'mod'`, `'member'`. Vai trò này là thuộc tính của mối kết hợp tham gia nhóm, không phải thuộc tính nội tại của người dùng.
- **Bối cảnh & Mục đích:** Đảm bảo nhóm học tập không bao giờ rơi vào trạng thái "vô chủ" và phân quyền quản trị rõ ràng.
- **Cơ chế thực thi kỹ thuật:**
  - Cột `owner_id INT NOT NULL REFERENCES users(user_id)` trên bảng `study_group`.
  - Bảng `group_member` có khóa chính `PRIMARY KEY (group_id, user_id)`.
  - Ràng buộc miền giá trị: `CHECK (role IN ('owner', 'mod', 'member'))`.
  - Trigger / Procedure tạo nhóm nguyên tử: Khi tạo nhóm mới trong `study_group`, tự động chèn một dòng vào `group_member` với `role = 'owner'`.
- **Kịch bản kiểm thử vi phạm:**
  - Cố tình chèn vào `group_member` một vai trò không hợp lệ như `'admin'` hay `'guest'`.
  - *Kết quả kỳ vọng:* Vi phạm ràng buộc miền giá trị `check_violation`.

---

### BR5: Ràng buộc quyền đăng bài viết trong nhóm học tập
- **Mô tả nghiệp vụ:** Chỉ những người dùng đã tham gia vào một nhóm học tập (có bản ghi trong `group_member`) mới có quyền đăng bài viết (thảo luận hoặc chia sẻ tài liệu) vào nhóm đó. Người ngoài nhóm không được phép đăng bài.
- **Bối cảnh & Mục đích:** Đảm bảo trật tự và an toàn nội dung cho các nhóm học tập chuyên đề, tránh việc người dùng lạ spam bài viết.
- **Cơ chế thực thi kỹ thuật:**
  - Trigger mức câu lệnh/dòng `trg_check_post_author_membership` trên bảng `post`: Trước khi `INSERT` một bài viết, truy vấn bảng `group_member` để kiểm tra sự tồn tại của cặp `(group_id, author_id)`. Nếu không tồn tại, phát sinh lỗi `RAISE EXCEPTION`.
  - Procedure đăng bài `proc_create_post(...)` kiểm tra quyền thành viên trước khi thực thi lệnh `INSERT`.
- **Kịch bản kiểm thử vi phạm:**
  - User 6 (chưa vào nhóm 1) cố tình gọi lệnh `INSERT INTO post (group_id, author_id, ...) VALUES (1, 6, ...)`.
  - *Kết quả kỳ vọng:* Trigger kích hoạt ngoại lệ `P0001 - raise_exception: 'Tac gia chua gia nhap nhom hoc tap nay'`.

---

### BR6: Tính toàn vẹn của phân cấp bình luận (Bình luận cha - con cùng bài viết, không chu trình)
- **Mô tả nghiệp vụ:** Bình luận phân cấp cho phép phản hồi một bình luận khác (`parent_id`). Bình luận con bắt buộc phải thuộc về cùng một bài viết (`post_id`) với bình luận cha của nó. Không được phép trả lời một bình luận thuộc bài viết khác. Bình luận không được phép trỏ cha đến chính nó hoặc tạo thành chu trình lặp vô tận.
- **Bối cảnh & Mục đích:** Ngăn ngừa phân mảnh dữ liệu cây bình luận giữa các bài viết khác nhau, bảo vệ cấu trúc cây phân cấp luôn là cây hợp lệ (Directed Acyclic Tree).
- **Cơ chế thực thi kỹ thuật:**
  - Khóa ngoại: `FOREIGN KEY (parent_id) REFERENCES comment(comment_id) ON DELETE CASCADE`.
  - Trigger `trg_check_comment_parent` (câu truy vấn Q9): Khi chèn/cập nhật `comment`, nếu `parent_id IS NOT NULL`, truy vấn `comment` cha để so sánh: `IF parent.post_id <> NEW.post_id THEN RAISE EXCEPTION`.
  - Ràng buộc: `CHECK (parent_id <> comment_id)`.
  - Procedure di chuyển nhánh bình luận `proc_move_comment` (câu truy vấn Q11) kiểm tra quan hệ tổ tiên trước khi chuyển cha để chặn triệt để chu trình.
- **Kịch bản kiểm thử vi phạm:**
  - Bình luận A thuộc Post 1, chèn Bình luận B thuộc Post 2 nhưng đặt `parent_id = A`.
  - *Kết quả kỳ vọng:* Trigger chặn và báo lỗi vi phạm logic phân cấp.

---

### BR7: Chuyên biệt hóa bài viết (Rời nhau, Toàn phần: Thảo luận vs Tài liệu)
- **Mô tả nghiệp vụ:** Mỗi bài viết đăng lên nhóm học tập bắt buộc phải thuộc **đúng một trong hai loại**: Bài viết Thảo luận (`thaoluan`) hoặc Bài viết Tài liệu (`tailieu`). Không tồn tại bài viết không phân loại, và một bài viết không thể vừa là thảo luận vừa là tài liệu cùng lúc (Quan hệ kế thừa Rời nhau - Disjoint và Toàn phần - Total).
  - *Bài thảo luận:* Có cờ đóng/mở thảo luận (`is_closed`).
  - *Bài tài liệu:* Bắt buộc có thông tin đường dẫn tập tin tài liệu (`file_url`), dung lượng (`file_size`) và tập nhãn chuyên đề (`tags`).
- **Bối cảnh & Mục đích:** Phân loại rõ ràng luồng tương tác: thảo luận học thuật và chia sẻ kho học liệu.
- **Cơ chế thực thi kỹ thuật:**
  - Áp dụng phương án ánh xạ kế thừa Bảng đơn (Single Table Inheritance) trên bảng `post`.
  - Cột phân loại: `post_type VARCHAR(10) NOT NULL CHECK (post_type IN ('thaoluan', 'tailieu'))`.
  - Ràng buộc điều kiện: Nếu `post_type = 'tailieu'` thì các trường tài liệu không được để trống (hoặc quản lý thông qua bảng mở rộng / view).
- **Kịch bản kiểm thử vi phạm:**
  - Chèn bài viết với `post_type = 'video'` hoặc `NULL`.
  - *Kết quả kỳ vọng:* Vi phạm `check_violation` hoặc `not_null_violation`.

---

### BR8: Ràng buộc tương tác cảm xúc bài viết (Tối đa 1 reaction / người / bài)
- **Mô tả nghiệp vụ:** Một người dùng chỉ được bày tỏ cảm xúc (like, helpful, bookmark...) tối đa một lần trên một bài viết. Nếu người dùng chọn lại cảm xúc khác, hệ thống sẽ cập nhật trạng thái cảm xúc chứ không tạo thêm dòng mới; nếu nhấn lại chính cảm xúc đó thì hủy cảm xúc.
- **Bối cảnh & Mục đích:** Ngăn ngừa việc một người dùng spam cảm xúc làm sai lệch chỉ số tương tác và độ tin cậy của bài đăng.
- **Cơ chế thực thi kỹ thuật:**
  - Khóa chính kết hợp: `PRIMARY KEY (post_id, user_id)` trên bảng `post_reaction`.
  - Ràng buộc loại cảm xúc: `CHECK (kind IN ('like', 'helpful', 'heart', 'bookmark'))`.
  - Thao tác cập nhật dùng cú pháp `INSERT ... ON CONFLICT (post_id, user_id) DO UPDATE SET kind = EXCLUDED.kind`.
- **Kịch bản kiểm thử vi phạm:**
  - Thực hiện `INSERT` hai dòng cùng cặp `(post_id, user_id)` bằng câu lệnh thông thường.
  - *Kết quả kỳ vọng:* Lỗi vi phạm khóa chính `unique_violation`.

---

### BR9: Tính nhất quán của thuộc tính dẫn xuất số lượng bạn bè (friend_count)
- **Mô tả nghiệp vụ:** Thuộc tính `friend_count` trong bảng `users` là một thuộc tính dẫn xuất (Derived Attribute), luôn phản ánh chính xác số lượng mối quan hệ bạn bè hợp lệ của người dùng đó (tương ứng với số dòng người dùng đó xuất hiện ở vị trí `user_a` hoặc `user_b` trong bảng `friendship`).
- **Bối cảnh & Mục đích:** Đây là kỹ thuật phi chuẩn hóa có kiểm soát (Controlled Denormalization) nhằm giúp các câu truy vấn hiển thị thông tin trang cá nhân đọc tức thì số bạn bè mà không cần quét bảng và chạy phép `COUNT()` tốn kém.
- **Cơ chế thực thi kỹ thuật:**
  - `friend_count INT NOT NULL DEFAULT 0 CHECK (friend_count >= 0)` trên bảng `users`.
  - Mọi thao tác kết bạn hoặc hủy kết bạn bắt buộc phải thực thi qua Stored Procedure `proc_add_friend(u1, u2)` hoặc `proc_remove_friend(u1, u2)` nằm trọn trong một Transaction nguyên tử (`BEGIN ... UPDATE users ... INSERT INTO friendship ... COMMIT;`).
  - Định kỳ chạy truy vấn đối soát dữ liệu (Audit Query) để kiểm tra: `SELECT u.user_id, u.friend_count, COUNT(f.*) FROM users u LEFT JOIN friend_edge f ON u.user_id = f.a GROUP BY u.user_id HAVING u.friend_count <> COUNT(f.*);`.
- **Kịch bản kiểm thử vi phạm:**
  - Trường hợp giao dịch bị ngắt quãng giữa chừng không dùng transaction khiến bảng `friendship` tăng dòng nhưng `users.friend_count` không đổi ⇒ Transaction Rollback bảo toàn tính toàn vẹn.

---

### BR10: Phân quyền truy cập nhóm học tập riêng tư (Public vs Private Group)
- **Mô tả nghiệp vụ:** Nhóm học tập có hai chế độ hiển thị: Công khai (`is_private = false`) và Riêng tư (`is_private = true`). Bài viết trong nhóm công khai cho phép mọi thành viên trong mạng xã hội xem. Bài viết trong nhóm riêng tư tuyệt đối chỉ hiển thị cho những người dùng đang là thành viên chính thức của nhóm đó.
- **Bối cảnh & Mục đích:** Bảo mật thông tin học tập, tài liệu nghiên cứu nội bộ và quyền riêng tư của các nhóm học tập nhỏ.
- **Cơ chế thực thi kỹ thuật:**
  - Cột cờ `is_private BOOLEAN NOT NULL DEFAULT false` trên bảng `study_group`.
  - Phân quyền mức CSDL thông qua View bảo mật hoặc Row-Level Security (RLS) của PostgreSQL:
    ```sql
    CREATE VIEW view_visible_posts AS
    SELECT p.* FROM post p
    JOIN study_group g ON p.group_id = g.group_id
    WHERE g.is_private = false 
       OR EXISTS (
           SELECT 1 FROM group_member gm 
           WHERE gm.group_id = g.group_id AND gm.user_id = current_setting('app.current_user_id')::INT
       );
    ```
- **Kịch bản kiểm thử vi phạm:**
  - Người dùng ngoài nhóm truy vấn bài viết của một nhóm có `is_private = true`.
  - *Kết quả kỳ vọng:* Tập kết quả rỗng (0 dòng trả về).

---

## 2. PHÂN TÍCH SO SÁNH 3 PHƯƠNG ÁN ÁNH XẠ KẾ THỪA (INHERITANCE MAPPING)

Bài toán chuyên biệt hóa thực thể `BAI_DANG` thành hai lớp con `BAI_THAO_LUAN` và `BAI_TAI_LIEU` (rời nhau, toàn phần theo BR7) có 3 phương án thiết kế vật lý kinh điển trên CSDL quan hệ:

| Tiêu chí so sánh | Phương án A: Single Table (Đang chọn) | Phương án B: Class Table (Bảng cha + Bảng con) | Phương án C: Concrete Table (Mỗi lớp một bảng) |
| :--- | :--- | :--- | :--- |
| **Cấu trúc bảng** | Duy nhất 1 bảng `post` chứa toàn bộ thuộc tính cha lẫn con + cột phân loại `post_type`. | Bảng cha `post` chứa thuộc tính chung; bảng con `post_thaoluan`, `post_tailieu` chứa thuộc tính riêng + FK trỏ về cha. | Không có bảng cha; hai bảng độc lập `post_thaoluan` và `post_tailieu` tự lặp lại các cột chung. |
| **Hiệu năng truy vấn đa hình (Lấy tất cả bài viết)** | **Cực nhanh**, quét trên 1 bảng duy nhất, không cần phép `JOIN` hay `UNION`. | Chậm hơn, phải `LEFT JOIN` bảng cha với tất cả các bảng con để lấy đủ thuộc tính. | Chậm và phức tạp, phải dùng phép `UNION ALL` kết hợp hai bảng. |
| **Tính toàn vẹn & Kiểm tra ràng buộc** | Chấp nhận một số cột mang giá trị `NULL` cho thuộc tính riêng; cần dùng `CHECK` phức hợp. | **Rất tốt**, các thuộc tính riêng của lớp con được đặt `NOT NULL` một cách tự nhiên. | Tốt cho từng lớp, nhưng khó đảm bảo tính duy nhất toàn cục của `post_id` trên cả hai lớp. |
| **Độ phức tạp khi thêm/sửa/xóa** | Đơn giản nhất, thao tác trên 1 dòng đơn lẻ. | Phức tạp hơn, thao tác thêm/xóa phải thực hiện trên 2 bảng trong 1 transaction. | Trung bình, nhưng khó hỗ trợ các quan hệ trỏ chung đến bài viết như `comment`, `post_reaction`. |
| **Lý do nhóm quyết định chọn** | **Chọn Phương án A:** Trong mạng xã hội học tập, thao tác xem danh sách bảng tin (newsfeed tổng hợp mọi loại bài viết) diễn ra liên tục với tần suất cao nhất. Hai lớp con có số lượng thuộc tính riêng tương đối ít, việc gộp bảng giúp loại bỏ triệt để chi phí `JOIN`, tối ưu hóa hiệu năng đọc dữ liệu. |

---

## 3. TỪ ĐIỂN DỮ LIỆU CHI TIẾT (DATA DICTIONARY)

Hệ thống bao gồm 10 bảng thực thể/quan hệ chính và 3 bảng cấu trúc cây bổ trợ:

### 3.1 Bảng `users` (Thông tin người dùng)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Giá Trị Mặc Định | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | `SERIAL` | `PRIMARY KEY` | Tự tăng | Mã định danh duy nhất của người dùng |
| `full_name` | `VARCHAR(100)` | `NOT NULL` | Không | Họ và tên đầy đủ |
| `email` | `VARCHAR(150)` | `NOT NULL, UNIQUE` | Không | Địa chỉ thư điện tử dùng để đăng nhập (BR1) |
| `friend_count` | `INT` | `NOT NULL, CHECK (friend_count >= 0)` | `0` | Số lượng bạn bè (thuộc tính dẫn xuất phi chuẩn hóa, BR9) |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL` | `now()` | Thời điểm tài khoản được khởi tạo |

### 3.2 Bảng `friendship` (Quan hệ bạn bè vô hướng)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Giá Trị Mặc Định | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- | :--- |
| `user_a` | `INT` | `FK -> users(user_id) ON DELETE CASCADE` | Không | Mã người dùng thứ nhất (nhỏ hơn `user_b`) |
| `user_b` | `INT` | `FK -> users(user_id) ON DELETE CASCADE` | Không | Mã người dùng thứ hai (lớn hơn `user_a`) |
| `since` | `TIMESTAMPTZ` | `NOT NULL` | `now()` | Thời điểm thiết lập quan hệ bạn bè |
| *Ràng buộc bảng:* | `PRIMARY KEY (user_a, user_b)`, `CHECK (user_a < user_b)` (BR2) | | |

### 3.3 Bảng `follow` (Quan hệ theo dõi học tập có hướng)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Giá Trị Mặc Định | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- | :--- |
| `follower_id` | `INT` | `FK -> users(user_id) ON DELETE CASCADE` | Không | Người bấm theo dõi |
| `followee_id` | `INT` | `FK -> users(user_id) ON DELETE CASCADE` | Không | Người được theo dõi |
| *Ràng buộc bảng:* | `PRIMARY KEY (follower_id, followee_id)`, `CHECK (follower_id <> followee_id)` (BR3) | | |

### 3.4 Bảng `study_group` (Nhóm học tập)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Giá Trị Mặc Định | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- | :--- |
| `group_id` | `SERIAL` | `PRIMARY KEY` | Tự tăng | Mã định danh duy nhất của nhóm |
| `name` | `VARCHAR(100)` | `NOT NULL` | Không | Tên nhóm học tập |
| `topic` | `VARCHAR(50)` | `NOT NULL` | Không | Chủ đề học thuật (ví dụ: 'CSDL', 'Toán', 'Lập trình') |
| `is_private` | `BOOLEAN` | `NOT NULL` | `false` | Cờ bảo mật: Công khai hoặc Riêng tư (BR10) |
| `owner_id` | `INT` | `NOT NULL, FK -> users(user_id)` | Không | Người sáng lập và quản lý nhóm (BR4) |

### 3.5 Bảng `group_member` (Thành viên nhóm học tập)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Giá Trị Mặc Định | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- | :--- |
| `group_id` | `INT` | `FK -> study_group(group_id) ON DELETE CASCADE` | Không | Mã nhóm học tập tham gia |
| `user_id` | `INT` | `FK -> users(user_id) ON DELETE CASCADE` | Không | Mã thành viên tham gia |
| `role` | `VARCHAR(10)` | `NOT NULL, CHECK (role IN ('owner','mod','member'))` | `'member'` | Vai trò trong nhóm (BR4) |
| `joined_at` | `TIMESTAMPTZ` | `NOT NULL` | `now()` | Ngày tham gia nhóm |
| *Ràng buộc bảng:* | `PRIMARY KEY (group_id, user_id)` | | |

### 3.6 Bảng `post` (Bài viết học tập - Kế thừa Bảng đơn)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Giá Trị Mặc Định | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- | :--- |
| `post_id` | `SERIAL` | `PRIMARY KEY` | Tự tăng | Mã bài viết duy nhất |
| `group_id` | `INT` | `NOT NULL, FK -> study_group(group_id)` | Không | Nhóm học tập chứa bài viết |
| `author_id` | `INT` | `NOT NULL, FK -> users(user_id)` | Không | Tác giả bài viết (phải là thành viên nhóm, BR5) |
| `post_type` | `VARCHAR(10)` | `NOT NULL, CHECK (post_type IN ('thaoluan','tailieu'))` | Không | Phân loại bài viết chuyên biệt hóa (BR7) |
| `title` | `VARCHAR(200)` | `NOT NULL` | Không | Tiêu đề bài đăng |
| `content` | `TEXT` | Có thể NULL | NULL | Nội dung chi tiết hoặc tóm tắt |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL` | `now()` | Thời điểm đăng bài |

### 3.7 Bảng `post_reaction` (Cảm xúc bài viết)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Giá Trị Mặc Định | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- | :--- |
| `post_id` | `INT` | `FK -> post(post_id) ON DELETE CASCADE` | Không | Mã bài viết được phản hồi |
| `user_id` | `INT` | `FK -> users(user_id) ON DELETE CASCADE` | Không | Người dùng bày tỏ cảm xúc |
| `kind` | `VARCHAR(10)` | `NOT NULL, CHECK (kind IN ('like','helpful','heart','bookmark'))` | `'like'` | Loại cảm xúc tương tác |
| *Ràng buộc bảng:* | `PRIMARY KEY (post_id, user_id)` (BR8: Mỗi người tối đa 1 reaction trên 1 bài) | | |

### 3.8 Bảng `comment` (Bình luận phân cấp - Mô hình Adjacency List)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Giá Trị Mặc Định | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- | :--- |
| `comment_id` | `SERIAL` | `PRIMARY KEY` | Tự tăng | Mã bình luận duy nhất |
| `post_id` | `INT` | `NOT NULL, FK -> post(post_id) ON DELETE CASCADE` | Không | Bài viết chứa bình luận |
| `author_id` | `INT` | `NOT NULL, FK -> users(user_id)` | Không | Tác giả của bình luận |
| `parent_id` | `INT` | `FK -> comment(comment_id) ON DELETE CASCADE` | NULL | Bình luận cha trực tiếp (NULL nếu là bình luận gốc, BR6) |
| `content` | `TEXT` | `NOT NULL` | Không | Nội dung thảo luận |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL` | `now()` | Thời điểm bình luận |

### 3.9 Các bảng phụ trợ so sánh 4 mô hình cây bình luận (Tree Models)
1. **`comment_path` (Path Enumeration / ltree):**
   - `comment_id INT PRIMARY KEY REFERENCES comment(comment_id) ON DELETE CASCADE`
   - `post_id INT NOT NULL REFERENCES post(post_id)`
   - `path ltree NOT NULL` (Đường dẫn tiền tố từ gốc đến nút, ví dụ: `'1.2.3'`).
2. **`comment_ns` (Nested Set / Khoảng bao lft, rgt):**
   - `comment_id INT PRIMARY KEY REFERENCES comment(comment_id) ON DELETE CASCADE`
   - `post_id INT NOT NULL REFERENCES post(post_id)`
   - `lft INT NOT NULL`, `rgt INT NOT NULL`, `CHECK (lft < rgt)` (Tọa độ biên duyệt cây tiền thứ tự).
3. **`comment_closure` (Closure Table / Bảng bao đóng quan hệ tổ tiên - hậu duệ):**
   - `ancestor INT REFERENCES comment(comment_id) ON DELETE CASCADE`
   - `descendant INT REFERENCES comment(comment_id) ON DELETE CASCADE`
   - `depth INT NOT NULL CHECK (depth >= 0)` (Khoảng cách cấp độ)
   - `PRIMARY KEY (ancestor, descendant)`.

### 3.10 Bảng `folder` (Cây thư mục tài liệu đối chứng)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Giá Trị Mặc Định | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- | :--- |
| `folder_id` | `SERIAL` | `PRIMARY KEY` | Tự tăng | Mã thư mục |
| `parent_id` | `INT` | `FK -> folder(folder_id) ON DELETE CASCADE` | NULL | Thư mục cha (NULL nếu là thư mục gốc) |
| `group_id` | `INT` | `NOT NULL, FK -> study_group(group_id)` | Không | Nhóm học tập sở hữu thư mục |
| `name` | `VARCHAR(100)` | `NOT NULL` | Không | Tên thư mục lưu trữ tài liệu |
