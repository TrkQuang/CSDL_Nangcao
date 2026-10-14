# BÁO CÁO TỔNG KẾT ĐỒ ÁN MÔN HỌC: CƠ SỞ DỮ LIỆU NÂNG CAO

# ĐỀ TÀI 17: DỮ LIỆU PHÂN CẤP VÀ DỮ LIỆU ĐỒ THỊ TRONG CƠ SỞ DỮ LIỆU QUAN HỆ: ỨNG DỤNG MẠNG XÃ HỘI HỌC TẬP

> **Giảng viên hướng dẫn:** Bộ môn Hệ thống Thông tin / Khoa CNTT  
> **Nhóm thực hiện:** Nhóm Đề tài 17 (5 thành viên)  
> **Trưởng nhóm & Tổng hợp báo cáo:** **Trần Quang** (TV1 - Leader)  
> **Thành viên nhóm:**  
> 1. **Trần Quang** - TV1 *(Phân tích nghiệp vụ, EER, Chuẩn hóa 3NF/BCNF/4NF, Báo cáo & Slide)*  
> 2. **Hưng** - TV2 *(4 Mô hình cây phân cấp, Q1–Q10, Thiết kế Đối tượng ODL/OQL/JPQL)*  
> 3. **Hữu** - TV3 *(DDL Schema, SQL Nâng cao Q1–Q12, SQL Đệ quy R1–R4, Giao dịch T1–T3)*  
> 4. **Chương** - TV4 *(CSDL Đồ thị Neo4j/Cypher, Tương tranh Deadlock, Thử tải pgbench)*  
> 5. **Quỳnh** - TV5 *(Kiểm chứng dữ liệu, Thiết kế vật lý, Chỉ mục, Tự động hóa Benchmark)*  
> 
> **Repository mã nguồn dự án:** [https://github.com/TrkQuang/CSDL_Nangcao.git](https://github.com/TrkQuang/CSDL_Nangcao.git)

---

## MỤC LỤC TỔNG QUAN

- **LỜI MỞ ĐẦU**
  1. Bối cảnh đề tài và tính cấp thiết
  2. Mục tiêu nghiên cứu và 3 câu hỏi nghiên cứu cốt lõi
  3. Phạm vi ứng dụng và phương pháp tiếp cận
- **CHƯƠNG 1: ĐẶC TẢ NGHIỆP VỤ & THIẾT KẾ MỨC QUAN NIỆM (EER)**
  1.1 Đặc tả chi tiết 10 quy tắc nghiệp vụ then chốt (BR1 – BR10)  
  1.2 Mô hình thực thể - mối kết hợp mở rộng (EER)  
  1.3 Phân tích so sánh 3 phương án ánh xạ kế thừa (Inheritance Mapping)  
  1.4 Từ điển dữ liệu hoàn chỉnh (Data Dictionary)
- **CHƯƠNG 2: LÝ THUYẾT PHỤ THUỘC HÀM & CHUẨN HÓA DỮ LIỆU**
  2.1 Lược đồ quan hệ phẳng tổng hợp ban đầu và các dị thường dữ liệu  
  2.2 Tập phụ thuộc hàm hợp lệ theo nghiệp vụ (Phân biệt FD nghiệp vụ vs FD tình cờ)  
  2.3 Thuật toán bao đóng thuộc tính và tìm tất cả khóa ứng viên  
  2.4 Thuật toán tìm phủ tối tiểu F_min qua 3 bước  
  2.5 Phân rã đạt chuẩn 3NF (Thuật toán tổng hợp Bernstein) và kiểm tra BCNF  
  2.6 Chứng minh tính bảo toàn thông tin (Bảng ma trận Chase) & Bảo toàn phụ thuộc hàm  
  2.7 Phụ thuộc đa trị (MVD) và dạng chuẩn 4 (4NF)  
  2.8 Phân tích kỹ thuật phi chuẩn hóa có kiểm soát (Controlled Denormalization)
- **CHƯƠNG 3: DỮ LIỆU PHÂN CẤP (CÂY) TRÊN CSDL QUAN HỆ**
  3.1 Cơ sở lý thuyết và cấu trúc 4 mô hình lưu trữ cây  
  3.2 Hiện thực bộ 10 truy vấn chuẩn (Q1 – Q10)  
  3.3 Kiểm thử tính đúng đắn trên bộ dữ liệu mẫu đối chứng
- **CHƯƠNG 4: SQL NÂNG CAO, ĐỆ QUY ĐỒ THỊ & ĐIỀU KHIỂN ĐỒNG THỜI**
  4.1 Bộ 8 truy vấn nâng cao (Q1 – Q8) và lập trình CSDL (Q9 – Q12)  
  4.2 SQL đệ quy trên đồ thị bạn bè (R1 – R4)  
  4.3 Điều khiển đồng thời, Giao dịch (T1, T2) và Thí nghiệm Deadlock (T3)  
  4.4 Thử tải đồng thời bằng pgbench
- **CHƯƠNG 5: CSDL HƯỚNG ĐỐI TƯỢNG VÀ CSDL ĐỒ THỊ CHUYÊN DỤNG**
  5.1 Mô hình hướng đối tượng: Lược đồ ODL, truy vấn OQL và ánh xạ JPQL  
  5.2 CSDL đồ thị Neo4j: Cài đặt, import dữ liệu và truy vấn Cypher  
  5.3 So sánh đối chiếu toàn diện giữa Cypher và WITH RECURSIVE
- **CHƯƠNG 6: THỰC NGHIỆM, BENCHMARK & ĐÁNH GIÁ HIỆU NĂNG**
  6.1 Thiết kế vật lý và chiến lược đánh chỉ mục  
  6.2 Kết quả đo lường và phân tích hiệu năng  
  6.3 Thảo luận kết quả và khuyến nghị kiến trúc
- **KẾT LUẬN & HƯỚNG PHÁT TRIỂN**
- **PHỤ LỤC: BÁO CÁO LÀM VIỆC NHÓM (CLO7) & BIÊN BẢN HỌP**

---

# LỜI MỞ ĐẦU

### 1. Bối cảnh đề tài và tính cấp thiết
Trong kỷ nguyên giáo dục trực tuyến và học tập cộng đồng, mạng xã hội học tập (Learning Social Network) đã trở thành một nền tảng không thể thiếu giúp sinh viên, giảng viên kết nối, trao đổi tri thức và chia sẻ tài liệu học thuật. Khác với các hệ thống thông tin quản lý truyền thống (chỉ thao tác trên các bảng dữ liệu dạng lưới quan hệ đơn giản), mạng xã hội học tập đòi hỏi hệ quản trị cơ sở dữ liệu phải xử lý đồng thời hai dạng cấu trúc dữ liệu phức tạp:
1. **Dữ liệu phân cấp dạng cây (Tree / Hierarchical Data):** Thể hiện ở các luồng bình luận phản hồi đa cấp (threaded comments) dưới bài giảng, bài tập; hoặc cấu trúc thư mục lồng nhau lưu trữ học liệu.
2. **Dữ liệu mạng lưới dạng đồ thị (Graph / Network Data):** Thể hiện ở mạng lưới liên kết bạn bè hai chiều, quan hệ theo dõi một chiều, quan hệ tham gia nhóm học tập, cùng các bài toán lan truyền tri thức như: tìm bạn của bạn, tìm đường đi ngắn nhất, phát hiện vòng bạn bè khép kín (chu trình), và thuật toán gợi ý kết bạn.

Mặc dù Hệ quản trị cơ sở dữ liệu quan hệ (RDBMS) như PostgreSQL vẫn là sự lựa chọn hàng đầu của doanh nghiệp nhờ tính toàn vẹn dữ liệu nghiêm ngặt (ACID), mô hình bảng quan hệ hai chiều phẳng vốn không được thiết kế tự nhiên cho các cấu trúc phân cấp sâu và duyệt đồ thị tùy ý.

### 2. Mục tiêu nghiên cứu và 3 câu hỏi nghiên cứu cốt lõi
Đề tài tập trung trả lời 3 câu hỏi nghiên cứu lớn:
- **Câu hỏi 1 (Về dữ liệu phân cấp):** Trong 4 giải pháp lưu trữ cây kinh điển trên CSDL quan hệ (*Adjacency List, Path Enumeration / ltree, Nested Set, Closure Table*), mô hình nào tối ưu nhất cho từng loại thao tác (đọc cây con, đọc tổ tiên, chèn thêm nút, di chuyển nhánh, xóa cành)? Chi phí đánh đổi về không gian đĩa và tốc độ ghi dữ liệu ra sao khi kích thước cây tăng từ 1.000 lên 100.000 nút?
- **Câu hỏi 2 (Về dữ liệu đồ thị):** SQL đệ quy (`WITH RECURSIVE`) trên hệ CSDL quan hệ đáp ứng các bài toán duyệt đồ thị (bạn của bạn, đường đi ngắn nhất, phát hiện chu trình) đến giới hạn nào? Khi nào một hệ thống cần chuyển đổi sang hoặc tích hợp hệ CSDL đồ thị chuyên dụng (*Neo4j / Cypher*)?
- **Câu hỏi 3 (Về mô hình dữ liệu đối tượng & Giao dịch):** Khả năng biểu diễn dữ liệu của mô hình hướng đối tượng (*ODL / OQL*) giải quyết vấn đề lệch pha trở kháng (*Impedance Mismatch*) thế nào khi so với mô hình quan hệ? Cơ chế kiểm soát đồng thời (*Concurrency Control*) xử lý các hiện tượng bất thường (Deadlock, Lost Update, Phantom Read) ra sao dưới các mức cô lập khác nhau?

---

# CHƯƠNG 1: ĐẶC TẢ NGHIỆP VỤ & THIẾT KẾ MỨC QUAN NIỆM (EER)

## 1.1 Đặc tả 10 quy tắc nghiệp vụ then chốt (BR1 – BR10)
Để đảm bảo cơ sở dữ liệu hoạt động chính xác và phản ánh đúng ngữ nghĩa thực tế của Mạng xã hội học tập, nhóm TV1 đã khảo sát và thiết lập hệ thống 10 quy tắc nghiệp vụ bắt buộc:

1. **BR1 (Email người dùng duy nhất):** Mỗi người dùng đăng ký vào hệ thống bằng một địa chỉ email duy nhất. Không cho phép hai tài khoản trùng email.  
   *Cơ chế kỹ thuật:* Ràng buộc `UNIQUE(email)` và `NOT NULL` trên bảng `users`.
2. **BR2 (Quan hệ bạn bè vô hướng đối xứng):** Kết bạn là quan hệ đối xứng hai chiều. Hệ thống không cho phép một người tự kết bạn với chính mình. Mỗi cặp bạn bè chỉ lưu trữ đúng một bản ghi với quy ước `user_a < user_b` để tránh dư thừa và mâu thuẫn dữ liệu.  
   *Cơ chế kỹ thuật:* Khóa chính `PRIMARY KEY (user_a, user_b)`, ràng buộc `CHECK (user_a < user_b)`, và Stored Procedure `proc_add_friend` tự động hoán vị. View logic `friend_edge` dùng `UNION ALL` hỗ trợ thuật toán duyệt hai chiều.
3. **BR3 (Quan hệ theo dõi có hướng):** Theo dõi là quan hệ một chiều, không cho phép một người tự theo dõi chính mình.  
   *Cơ chế kỹ thuật:* Khóa chính `PRIMARY KEY (follower_id, followee_id)`, `CHECK (follower_id <> followee_id)` trên bảng `follow`.
4. **BR4 (Chủ nhóm và vai trò thành viên):** Mỗi nhóm học tập được sáng lập bởi một chủ nhóm (`owner_id`) và người này bắt buộc phải là thành viên nhóm với vai trò `'owner'`. Vai trò của thành viên trong nhóm nhận một trong ba giá trị: `'owner'`, `'mod'`, `'member'`.  
   *Cơ chế kỹ thuật:* `owner_id REFERENCES users(user_id)`, `group_member.role CHECK (role IN ('owner','mod','member'))`.
5. **BR5 (Quyền đăng bài trong nhóm):** Chỉ những người dùng đã là thành viên chính thức của nhóm mới có quyền đăng bài viết vào nhóm đó.  
   *Cơ chế kỹ thuật:* Trigger `trg_check_post_author_membership` trên bảng `post` kiểm tra cặp `(group_id, author_id)` trong `group_member` trước khi cho phép chèn.
6. **BR6 (Toàn vẹn phân cấp bình luận):** Bình luận con bắt buộc phải thuộc cùng bài viết với bình luận cha của nó. Không được phép trả lời một bình luận thuộc bài viết khác; không được tạo chu trình cha-con.  
   *Cơ chế kỹ thuật:* Trigger `trg_check_comment_parent` (câu Q9) kiểm tra `parent.post_id = NEW.post_id` và Stored Procedure `proc_move_comment` (câu Q11) chặn chu trình.
7. **BR7 (Chuyên biệt hóa bài viết rời nhau, toàn phần):** Mỗi bài viết bắt buộc phải thuộc đúng một trong hai loại: Bài thảo luận (`thaoluan`) hoặc Bài chia sẻ tài liệu (`tailieu`).  
   *Cơ chế kỹ thuật:* Áp dụng mô hình Single Table Inheritance, cột `post_type CHECK (post_type IN ('thaoluan','tailieu'))`.
8. **BR8 (Tương tác cảm xúc duy nhất):** Mỗi người dùng chỉ được bày tỏ cảm xúc tối đa một lần trên một bài viết.  
   *Cơ chế kỹ thuật:* Khóa chính kết hợp `PRIMARY KEY (post_id, user_id)` trên bảng `post_reaction`.
9. **BR9 (Đồng bộ bộ đếm bạn bè):** Thuộc tính `users.friend_count` luôn phản ánh chính xác số lượng bạn bè thực tế của người dùng trong bảng `friendship`.  
   *Cơ chế kỹ thuật:* Cập nhật đồng bộ trong cùng một Transaction khi gọi `proc_add_friend` hoặc `proc_remove_friend`.
10. **BR10 (Bảo mật nhóm riêng tư):** Nhóm học tập riêng tư (`is_private = true`) chỉ cho phép thành viên nhóm xem nội dung bài viết và thảo luận.  
    *Cơ chế kỹ thuật:* Quản lý qua View logic hoặc chính sách bảo mật cấp dòng (Row-Level Security - RLS).

---

## 1.2 Mô hình thực thể - mối kết hợp mở rộng (EER)
Sơ đồ EER được xây dựng chi tiết trong file [docs/eer.drawio](file:///c:/Users/shuut/Documents/CSDL_NC/docs/eer.drawio), bao gồm:
- **Các thực thể mạnh:** `NGUOI_DUNG` (users), `NHOM_HOC_TAP` (study_group), `BAI_DANG` (post), `BINH_LUAN` (comment), `THU_MUC` (folder).
- **Chuyên biệt hóa (Specialization):** Thực thể `BAI_DANG` được chuyên biệt hóa thành hai thực thể con `BAI_THAO_LUAN` và `BAI_TAI_LIEU` với ràng buộc Rời nhau (Disjoint - ký hiệu chữ `d`) và Toàn phần (Total Participation - ký hiệu đường nối kép).
- **Các mối kết hợp đệ quy (Recursive Relationships):**
  - Mối kết hợp `KET_BAN` trên `NGUOI_DUNG` (đối xứng, vô hướng, bản số M:N).
  - Mối kết hợp `THEO_DOI` trên `NGUOI_DUNG` (có hướng, vai trò `follower` và `followee`, bản số M:N).
  - Mối kết hợp `TRA_LOI` trên `BINH_LUAN` (bản số 1:N, thuộc tính khóa ngoại `parent_id`).
  - Mối kết hợp `THU_MUC_CON` trên `THU_MUC` (bản số 1:N).
- **Thuộc tính đa trị & Phức hợp:**
  - Thuộc tính phức hợp `ho_ten` trên `NGUOI_DUNG` gồm 3 thuộc tính con: `ho`, `ten_dem`, `ten`.
  - Thuộc tính đa trị `so_thich` và `mon_hoc` trên `NGUOI_DUNG` (nguồn gốc phát sinh phụ thuộc đa trị MVD và chuẩn 4NF).
  - Thuộc tính đa trị `tap_nhan` trên `BAI_TAI_LIEU`.
  - Thuộc tính dẫn xuất `friend_count` trên `NGUOI_DUNG` (ký hiệu elip nét đứt).

---

## 1.3 So sánh 3 phương án ánh xạ kế thừa (Inheritance Mapping)
| Tiêu chí | Phương án A: Single Table (Nhóm chọn) | Phương án B: Class Table | Phương án C: Concrete Table |
| :--- | :--- | :--- | :--- |
| **Cấu trúc DDL** | 1 bảng `post` duy nhất chứa cột chung, cột riêng và cột `post_type`. | Bảng cha `post` + 2 bảng con `post_thaoluan`, `post_tailieu`. | 2 bảng độc lập `post_thaoluan`, `post_tailieu` không có bảng cha. |
| **Truy vấn đa hình (Newsfeed)** | **Rất nhanh (1 lần quét bảng, 0 phép JOIN)**. | Chậm hơn (cần `LEFT JOIN` với cả 2 bảng con). | Chậm và phức tạp (phải dùng `UNION ALL`). |
| **Lưu trữ & Ràng buộc** | Có thể chứa các cột NULL; cần dùng CHECK có điều kiện. | Không chứa NULL thừa; kiểm tra ràng buộc riêng rất tự nhiên. | Khó bảo đảm tính duy nhất toàn cục của mã bài viết `post_id`. |
| **Lý do lựa chọn** | Nhóm chọn Phương án A vì tần suất xem bảng tin tổng hợp trên mạng xã hội là áp đảo. Hai lớp con có số thuộc tính riêng rất ít. |

---

# CHƯƠNG 2: LÝ THUYẾT PHỤ THUỘC HÀM & CHUẨN HÓA DỮ LIỆU

## 2.1 Lược đồ quan hệ phẳng tổng hợp ban đầu và các dị thường
Xuất phát từ lược đồ bảng phẳng lưu trữ gộp:
```text
R = { comment_id, post_id, group_id, group_name, group_topic, author_id, author_name, author_email, parent_id, content, created_at }
```

Khi dữ liệu chưa chuẩn hóa, hệ thống phát sinh 3 dị thường dữ liệu nghiêm trọng:
1. **Dị thường thêm:** Không thể thêm một nhóm học tập mới hoặc một tác giả mới vào hệ thống nếu họ chưa đăng bất kỳ bình luận nào (do `comment_id` là khóa chính, không được phép mang giá trị NULL).
2. **Dị thường xóa:** Khi xóa hết bình luận của một bài viết, thông tin của bài viết, tác giả và nhóm học tập bị xóa mất vĩnh viễn nếu chúng chỉ tồn tại trên các dòng đó.
3. **Dị thường cập nhật:** Tên nhóm và email tác giả bị lặp lại hàng nghìn lần trên các dòng bình luận. Nếu nhóm đổi tên mà một số dòng cập nhật thất bại, CSDL sẽ rơi vào trạng thái bất nhất quán.

---

## 2.2 Tập phụ thuộc hàm hợp lệ theo nghiệp vụ (F)
Dựa trên 10 quy tắc nghiệp vụ, nhóm xác lập tập phụ thuộc hàm `F = { f1, f2, f3, f4, f5 }`:
- `f1: comment_id → post_id, author_id, parent_id, content, created_at`
- `f2: post_id → group_id`
- `f3: group_id → group_name, group_topic`
- `f4: author_id → author_name, author_email`
- `f5: author_email → author_id, author_name`

> **Phân biệt FD nghiệp vụ vs FD tình cờ:**  
> Truy vấn SQL trên bộ dữ liệu nhỏ có thể cho thấy `full_name → email` không có dòng vi phạm. Tuy nhiên đây chỉ là **FD tình cờ đúng trên tập mẫu hữu hạn**. Trong thực tế, nhiều người hoàn toàn có thể trùng họ tên nên đây là FD sai nghiệp vụ. Một FD chỉ hợp lệ khi nó đúng trong mọi trạng thái tương lai của thế giới thực.

---

## 2.3 Thuật toán bao đóng thuộc tính và tìm khóa ứng viên
- **Tính bao đóng {comment_id}+:**
  1. Khởi tạo: `X(0) = { comment_id }`
  2. Áp dụng `f1` ⇒ `X(1) = { comment_id, post_id, author_id, parent_id, content, created_at }`
  3. Áp dụng `f2` ⇒ `X(2) = X(1) ∪ { group_id }`
  4. Áp dụng `f3` ⇒ `X(3) = X(2) ∪ { group_name, group_topic }`
  5. Áp dụng `f4` ⇒ `X(4) = X(3) ∪ { author_name, author_email } = R`
- **Tìm khóa ứng viên:**
  - Tập nguồn (chỉ ở vế trái): `L = { comment_id }`
  - Tập đích (chỉ ở vế phải): `R_attr = { parent_id, content, created_at, group_topic }`
  - Tập trung gian: `M = { post_id, group_id, group_name, author_id, author_name, author_email }`
  - Vì `L+ = { comment_id }+ = R`, tập nguồn `L` chính là siêu khóa tối tiểu và là **khóa ứng viên duy nhất** của `R`.

---

## 2.4 Thuật toán tìm phủ tối tiểu (F_min)
1. **Bước 1 (Đơn vế phải):** Tách thành 10 FD đơn:
   - `comment_id → post_id`, `comment_id → author_id`, `comment_id → parent_id`, `comment_id → content`, `comment_id → created_at`
   - `post_id → group_id`
   - `group_id → group_name`, `group_id → group_topic`
   - `author_id → author_name`, `author_id → author_email`
2. **Bước 2 (Loại thuộc tính dư vế trái):** Mọi vế trái đều chỉ có 1 thuộc tính đơn ⇒ Không có thuộc tính dư.
3. **Bước 3 (Loại FD dư thừa):** Lần lượt tính bao đóng khi bỏ từng FD; không có FD nào dư thừa.
- **Kết quả:** Phủ tối tiểu `F_min` gồm đúng 10 FD trên, gộp theo vế trái ta được lại 4 nhóm chính `f1, f2, f3, f4`.

---

## 2.5 Phân rã 3NF (Thuật toán Bernstein) & Kiểm tra BCNF
- Lược đồ `R` ban đầu đạt 1NF, 2NF (vì khóa đơn thuộc tính), nhưng **vi phạm nghiêm trọng 3NF** do các phụ thuộc bắc cầu qua các thuộc tính không khóa:
  ```text
  comment_id → post_id → group_id → group_name
  comment_id → author_id → author_name
  ```
- **Áp dụng thuật toán tổng hợp Bernstein:**
  - `R1(comment_id, post_id, author_id, parent_id, content, created_at)` với khóa chính là `comment_id`
  - `R2(post_id, group_id)` với khóa chính là `post_id`
  - `R3(group_id, group_name, group_topic)` với khóa chính là `group_id`
  - `R4(author_id, author_name, author_email)` với khóa chính là `author_id`
- **Kiểm tra BCNF:** Trong mỗi quan hệ con `R1, R2, R3, R4`, mọi định thức vế trái đều là siêu khóa của quan hệ chứa nó. Do đó, cả 4 quan hệ đều đạt chuẩn **BCNF**.

---

## 2.6 Chứng minh Lossless Join (Bảng ma trận Chase) & Bảo toàn FD
- **Phương pháp nối nhị phân:**
  - `R1 ∩ R2 = { post_id }` là khóa của `R2` ⇒ `R1 ⋈ R2` không mất mát.
  - `(R1 ⋈ R2) ∩ R3 = { group_id }` là khóa của `R3` ⇒ `(R1 ⋈ R2) ⋈ R3` không mất mát.
  - `(R1 ⋈ R2 ⋈ R3) ∩ R4 = { author_id }` là khóa của `R4` ⇒ `R1 ⋈ R2 ⋈ R3 ⋈ R4 = R` không mất mát.
- **Bảng ma trận Chase:** Biến đổi 4 hàng của bảng Chase thông qua các FD của `F`. Sau 3 bước áp dụng `f2, f3, f4`, hàng thứ nhất `R1` chuyển đổi thành hàng chứa toàn bộ ký hiệu `a` trên cả 11 thuộc tính ⇒ **Xác nhận 100% Lossless Join**.
- **Bảo toàn phụ thuộc hàm:** Mọi FD trong `F_min` đều nằm trọn trong các quan hệ con tương ứng ⇒ Bảo toàn 100% phụ thuộc hàm.

---

## 2.7 Phụ thuộc đa trị (MVD) và Dạng chuẩn 4 (4NF)
- **Lý thuyết:** Khi một thực thể có hai thuộc tính đa trị độc lập nhau (ví dụ: một sinh viên có nhiều sở thích học tập và quan tâm nhiều môn học), bảng gộp `R(user_id, interest, subject)` sẽ bị vi phạm chuẩn 4NF do tồn tại 2 MVD: `user_id →→ interest` và `user_id →→ subject`.
- **Hậu quả:** Bảng gộp sinh ra tích Descartes giữa số sở thích và số môn học. Một sinh viên có 10 sở thích và 10 môn học sẽ tốn `10 × 10 = 100` dòng lưu trữ.
- **Giải pháp 4NF:** Phân rã thành 2 bảng độc lập:
  - `user_interest(user_id, interest)`
  - `user_subject(user_id, subject)`  
  Số dòng lưu trữ giảm từ 100 dòng xuống chỉ còn `10 + 10 = 20` dòng (tiết kiệm 80%), triệt tiêu hoàn toàn dị thường cập nhật. Toàn bộ mã kiểm chứng đã được hiện thực trong [normalization/mvd_4nf.sql](file:///c:/Users/shuut/Documents/CSDL_NC/normalization/mvd_4nf.sql).

---

## 2.8 Phân tích kỹ thuật phi chuẩn hóa có kiểm soát (Controlled Denormalization)
Để tối ưu hóa hiệu năng trong hệ thống mạng xã hội, nhóm áp dụng kỹ thuật phi chuẩn hóa có kiểm soát:
1. `users.friend_count`: Lưu sẵn số lượng bạn bè để hiển thị trang cá nhân không cần quét hàm `COUNT()`, kiểm soát bằng Transaction nguyên tử trong Stored Procedure `proc_add_friend`.
2. `comment_path.path` (`ltree`): Lưu sẵn đường dẫn phả hệ để đọc cây con bằng toán tử `<@` không cần đệ quy.
3. `comment_ns (lft, rgt)`: Lưu khoảng bao thứ tự để đọc cây con bằng toán tử số học `BETWEEN`.
4. `comment_closure`: Lưu trước mọi cặp tổ tiên - hậu duệ kèm độ sâu `depth`.

---

# TÓM TẮT CÁC CHƯƠNG KỸ THUẬT TIẾP THEO (TV2 – TV5)

### CHƯƠNG 3: DỮ LIỆU PHÂN CẤP (CÂY) TRÊN CSDL QUAN HỆ (TV2 - Hưng)
- So sánh toàn diện 4 mô hình: Adjacency List, Path Enumeration (`ltree`), Nested Set, Closure Table.
- Hiện thực hoàn chỉnh bộ 10 truy vấn chuẩn (Q1–Q10) trên từng mô hình.
- Minh chứng cả 4 mô hình đều trả về kết quả giống nhau trên bộ dữ liệu kiểm chứng nhỏ: cây con của c1 là `{ c1, c2, c3 }`, tổ tiên của c3 là `{ c1, c2 }`, độ sâu c3 bằng 3.

### CHƯƠNG 4: SQL NÂNG CAO, ĐỆ QUY ĐỒ THỊ & GIAO DỊCH (TV3 - Hữu)
- 8 truy vấn nâng cao: Subquery, NOT EXISTS lồng nhau (phép chia quan hệ), Window Functions.
- Lập trình CSDL: Trigger kiểm tra cây (Q9), Stored Procedure kết bạn nguyên tử (Q10), Di chuyển nhánh chặn chu trình (Q11), Dynamic SQL chống injection (Q12), ví dụ SQL nhúng qua Cursor.
- 4 bài toán đệ quy đồ thị (R1–R4): Bạn của bạn (k=2), Đường đi ngắn nhất BFS, Phát hiện chu trình, Gợi ý kết bạn.
- Giao dịch T1 (Thành công), T2 (Rollback và Savepoint).

### CHƯƠNG 5: CSDL HƯỚNG ĐỐI TƯỢNG VÀ CSDL ĐỒ THỊ (TV2 & TV4)
- Thiết kế 6 lớp đối tượng, lược đồ ODL chuẩn ODMG 3.0, 8 câu truy vấn OQL và ánh xạ JPQL.
- Phân tích sự lệch pha trở kháng (Impedance Mismatch).
- CSDL đồ thị Neo4j: Nạp dữ liệu qua Cypher, đối chiếu cú pháp ngắn gọn và tốc độ duyệt đồ thị sâu của Neo4j so với `WITH RECURSIVE` của PostgreSQL.

### CHƯƠNG 6: THỰC NGHIỆM, BENCHMARK & ĐÁNH GIÁ HIỆU NĂNG (TV5 & TV4)
- Thiết kế vật lý: Chiến lược đánh chỉ mục B-tree, GiST ltree, Composite Index.
- Đo lường trước và sau chỉ mục qua `EXPLAIN (ANALYZE, BUFFERS)` trên các quy mô 1.000, 10.000 và 100.000 bản ghi.
- Thử nghiệm tương tranh T3: Gây Deadlock (mã lỗi `40P01`), ma trận kiểm thử các mức cô lập (Read Committed, Repeatable Read, Serializable).
- Thử tải đồng thời bằng `pgbench` với các mức 5, 10, 20 kết nối.

---

# KẾT LUẬN & HƯỚNG PHÁT TRIỂN

### 1. Kết quả đạt được
1. Đã xây dựng thành công lược đồ CSDL quan hệ chuẩn hóa đạt BCNF và 4NF cho ứng dụng Mạng xã hội học tập, thiết lập đầy đủ các ràng buộc toàn vẹn và trigger bảo vệ.
2. Đã hiện thực và đối chiếu thực nghiệm 4 mô hình dữ liệu cây trên cùng một bộ dữ liệu, chỉ ra rõ ưu và nhược điểm của từng phương pháp:
   - *Closure Table & Nested Set:* Đọc cây con nhanh nhất nhưng chi phí ghi và cập nhật nhánh rất đắt.
   - *Path Enumeration (`ltree`):* Cân bằng hoàn hảo giữa hiệu năng đọc, ghi và sự tiện lợi nhờ hỗ trợ bản địa của PostgreSQL.
   - *Adjacency List:* Cấu trúc đơn giản nhất, chèn nhanh nhất, nhưng đọc cây con phụ thuộc vào độ phức tạp của CTE đệ quy.
3. Đã làm rõ ranh giới giữa SQL đệ quy trên CSDL quan hệ và CSDL đồ thị chuyên dụng Neo4j: Với các truy vấn đồ thị ngắn (độ sâu `k ≤ 2`), PostgreSQL xử lý rất tốt; nhưng khi độ sâu đồ thị tăng và có yêu cầu tìm đường đi phức tạp, Neo4j thể hiện ưu thế vượt trội về cả sự trong sáng của cú pháp Cypher lẫn hiệu năng xử lý.

### 2. Hạn chế và hướng phát triển
- Hạn chế: Chưa triển khai phân tán (sharding) cho bảng Closure Table khi dữ liệu vượt ngưỡng hàng triệu nút; kịch bản thử tải trên máy cá nhân bị giới hạn bởi tài nguyên CPU/RAM.
- Hướng mở rộng: Nghiên cứu tích hợp hệ thống đa mô hình (Polyglot Persistence): dùng PostgreSQL quản lý giao dịch nghiệp vụ cốt lõi và Neo4j phụ trách tính năng gợi ý kết bạn thời gian thực.

---

# PHỤ LỤC: BÁO CÁO LÀM VIỆC NHÓM & BẢNG ĐÓNG GÓP (CLO7)

| Mã TV | Thành viên | Vai trò | Tỷ lệ đóng góp | Chữ ký xác nhận |
| :---: | :--- | :--- | :---: | :---: |
| **TV1** | **Trần Quang** | *Trưởng nhóm; Phân tích, EER, Chuẩn hóa, Tổng hợp báo cáo & slide* | 100% | *(Đã ký)* |
| **TV2** | **Hưng** | *4 Mô hình cây phân cấp, Q1–Q10, Thiết kế Đối tượng ODL/OQL* | 100% | *(Đã ký)* |
| **TV3** | **Hữu** | *DDL Schema, SQL Nâng cao Q1–Q12, SQL Đệ quy R1–R4, Transaction* | 100% | *(Đã ký)* |
| **TV4** | **Chương** | *CSDL Đồ thị Neo4j/Cypher, Tương tranh Deadlock T3, Thử tải pgbench* | 100% | *(Đã ký)* |
| **TV5** | **Quỳnh** | *Kiểm chứng dữ liệu, Chỉ mục, Tự động hóa Benchmark EXPLAIN ANALYZE* | 100% | *(Đã ký)* |

*Tất cả các thành viên đã tham gia đầy đủ các buổi họp hàng tuần, thực hiện review chéo mã nguồn và kiểm tra chạy lại toàn bộ hệ thống từ kho lưu trữ Git sạch.*
