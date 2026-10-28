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

# CHƯƠNG 3: DỮ LIỆU PHÂN CẤP (CÂY) TRÊN CƠ SỞ DỮ LIỆU QUAN HỆ

## 3.1 Cơ sở lý thuyết và cấu trúc 4 mô hình lưu trữ cây
Trong hệ thống mạng xã hội học tập, cấu trúc cây phân cấp xuất hiện ở luồng bình luận lồng nhau (threaded comments) dưới bài viết và cây thư mục học liệu. Để giải quyết hạn chế của mô hình quan hệ 2 chiều phẳng, nhóm đã hiện thực và đối chiếu 4 giải pháp kinh điển:

| Mô hình | Cấu trúc lưu trữ | Ưu điểm cốt lõi | Nhược điểm cốt lõi | Chỉ mục tối ưu |
| :--- | :--- | :--- | :--- | :--- |
| **1. Adjacency List** *(Danh sách kề)* | Mỗi dòng lưu `parent_id` trỏ về bình luận cha trực tiếp. | Cấu trúc tối giản, chèn nút mới cực nhanh ($O(1)$), không phát sinh dung lượng dư thừa. | Đọc cây con hoặc tổ tiên bắt buộc dùng đệ quy `WITH RECURSIVE`, chi phí tăng theo độ sâu cây. | `B-tree (post_id, parent_id)` |
| **2. Path Enumeration** *(PostgreSQL `ltree`)* | Lưu toàn bộ chuỗi phả hệ từ gốc đến nút hiện tại (ví dụ: `'1.2.5'`). | Đọc cây con, tổ tiên cực nhanh qua toán tử `<@`, `@>` không cần đệ quy. | Chi phí cập nhật chuỗi path khi di chuyển nhánh; chuỗi đường dẫn bị giới hạn độ dài. | `GiST (path)` |
| **3. Nested Set** *(Tập lồng nhau)* | Lưu cặp số thứ tự duyệt cây tiền thứ tự `(lft, rgt)`. | Đọc toàn bộ cây con bằng 1 phép so sánh số học `BETWEEN` ($O(1)$ về mặt logic truy vấn). | Chi phí ghi cực đắt: chèn/xóa/chuyển nhánh phải đánh số lại $O(N)$ nút trong cây. | `Composite (post_id, lft, rgt)` |
| **4. Closure Table** *(Bảng bao đóng)* | Dùng bảng phụ `comment_closure` lưu mọi cặp `(ancestor, descendant, depth)`. | Đọc cây con, tổ tiên, tính khoảng cách bằng 1 phép `JOIN` đơn giản. Tách biệt cấu trúc cây và thuộc tính nghiệp vụ. | Tốn dung lượng đĩa nhất ($O(N^2)$ trong trường hợp cây thoái hóa thành danh sách liên kết). | `Composite (ancestor, depth)` & `(descendant, ancestor)` |

---

## 3.2 Hiện thực bộ 10 truy vấn chuẩn (Q1 – Q10)
Để đảm bảo tính khoa học và công bằng khi đánh giá, cả 4 mô hình đều hiện thực cùng một bộ 10 truy vấn chuẩn và đối chứng trên bộ dữ liệu kiểm chứng [database/seed_test.sql](file:///c:/Users/shuut/Documents/CSDL_Nangcao/database/seed_test.sql):

- **Q1 (Toàn bộ cây có thụt dòng):**
  - *Adjacency List:* Dùng CTE đệ quy tăng dần `level`, nối chuỗi `REPEAT('  ', level) || content`.
  - *Path Enumeration:* Dùng hàm `nlevel(path)` của module `ltree` để tính khoảng cách thụt lề.
  - *Nested Set:* Dùng phép `COUNT` số nút bao quanh nút hiện tại để suy ra độ sâu.
  - *Closure Table:* `JOIN` với bảng bao đóng lọc theo nút gốc (`ancestor = root`) và lấy `depth`.
- **Q2 (Lấy toàn bộ hậu duệ / cây con của nút $X$):**
  - *Adjacency List:* `WITH RECURSIVE subtree AS (...) SELECT ... JOIN subtree ON child.parent_id = subtree.comment_id`.
  - *Path Enumeration:* `SELECT * FROM comment_path WHERE path <@ (SELECT path FROM comment_path WHERE comment_id = X)`.
  - *Nested Set:* `SELECT child.* FROM comment_ns child, comment_ns root WHERE root.comment_id = X AND child.lft BETWEEN root.lft AND root.rgt`.
  - *Closure Table:* `SELECT c.* FROM comment_closure cc JOIN comment c ON cc.descendant = c.comment_id WHERE cc.ancestor = X`.
- **Q3 (Lấy toàn bộ tổ tiên - Breadcrumb):**
  - *Path Enumeration:* Dùng toán tử `@>` tìm các nút mà đường dẫn là tiền tố của nút hiện tại.
  - *Closure Table:* `SELECT * FROM comment_closure WHERE descendant = X AND depth > 0 ORDER BY depth DESC`.
- **Q4 (Lấy các nút ở độ sâu xác định $k$):** Lọc theo `depth = k` hoặc `nlevel(path) = k`.
- **Q5 (Thêm nút mới):** Chèn vào cây; với Nested Set phải dịch `lft`/`rgt` các nút phía sau; với Closure Table phải nhân bản mọi tổ tiên của cha thêm 1 bước.
- **Q6 (Xóa nút và toàn bộ cây con):** Xóa cascade; với Closure Table xóa toàn bộ liên kết có `descendant` nằm trong cây con.
- **Q7 (Di chuyển nhánh an toàn - Move Subtree):** Kiểm tra chống chu trình (không cho phép chuyển một nút làm con của chính hậu duệ của nó).
- **Q8 (Đếm số lượng nút con):** Trên Nested Set tính trực tiếp bằng công thức $(rgt - lft - 1) / 2$ mà không cần quét bảng; trên Closure Table dùng `COUNT(*) WHERE ancestor = X AND depth > 0`.
- **Q9 (Đường dẫn từ gốc đến nút hiện tại):** Lấy danh sách ID các nút tổ tiên theo thứ tự từ trên xuống.
- **Q10 (Kiểm tra quan hệ tổ tiên - hậu duệ):** Trả về kiểu Boolean (`true/false`) xác định nhanh nút $A$ có phải tổ tiên của nút $B$ hay không.

---

## 3.3 Quy ước thống nhất và Kiểm chứng kết quả logic
Theo biên bản nghiệm thu kỹ thuật [tree_models/TONGKET-TV2.md](file:///c:/Users/shuut/Documents/CSDL_Nangcao/tree_models/TONGKET-TV2.md), nhóm thống nhất quy ước:
1. **Truy vấn cây con (Q2, Q8):** Tính cả chính nút gốc được chỉ định $\Rightarrow$ `subtree(1) = {1, 2, 3}`, số lượng = 3.
2. **Truy vấn tổ tiên (Q3, Q9, Q10):** Lọc nghiêm ngặt, không tính chính nút đó $\Rightarrow$ `ancestors(3) = {1, 2}`.
3. **Độ sâu cây:** Nút gốc có `depth = 1`.

Bộ script kiểm thử tự động [tree_models/_validate/validate.ps1](file:///c:/Users/shuut/Documents/CSDL_Nangcao/tree_models/_validate/validate.ps1) đã chạy quét sạch sẽ 4/4 mô hình trên PostgreSQL, trả về kết quả đồng nhất 100%:
```text
adjacency_list    queries=OK  crud=OK
closure_table     queries=OK  crud=OK
nested_set        queries=OK  crud=OK
path_enumeration  queries=OK  crud=OK
```

---

# CHƯƠNG 4: SQL NÂNG CAO, ĐỆ QUY ĐỒ THỊ & ĐIỀU KHIỂN ĐỒNG THỜI

## 4.1 Bộ 8 truy vấn nâng cao (Q1 – Q8)
Nhóm đã hiện thực đầy đủ các kỹ thuật truy vấn phức tạp trong [sql_advanced/q01_q08_select.sql](file:///c:/Users/shuut/Documents/CSDL_Nangcao/sql_advanced/q01_q08_select.sql):

1. **Q1 (Scalar Subquery):** Tìm người dùng có số lượng bạn bè vượt mức trung bình hệ thống:
   ```sql
   SELECT user_id, full_name, friend_count 
   FROM users 
   WHERE friend_count > (SELECT AVG(friend_count) FROM users);
   ```
2. **Q2 (Double NOT EXISTS):** Tìm sinh viên chưa từng đăng bài viết nào và chưa từng bình luận (phát hiện tài khoản không hoạt động).
3. **Q3 (Phép chia quan hệ - Relational Division):** Tìm sinh viên tham gia **TẤT CẢ** các nhóm học tập thuộc chủ đề `'CSDL'`. Đây là dạng truy vấn kinh điển được hiện thực bằng 2 tầng `NOT EXISTS` lồng nhau:
   ```sql
   SELECT u.user_id, u.full_name
   FROM users u
   WHERE NOT EXISTS (
       SELECT 1 FROM study_group sg WHERE sg.topic = 'CSDL'
       AND NOT EXISTS (
           SELECT 1 FROM group_member gm 
           WHERE gm.group_id = sg.group_id AND gm.user_id = u.user_id
       )
   );
   ```
4. **Q4 (HAVING với điều kiện gộp):** Lọc nhóm học tập có tỷ lệ bài thảo luận chiếm trên 60% tổng số bài đăng.
5. **Q5 (Window Function `DENSE_RANK`):** Xếp hạng người dùng tích cực theo số lượng bài viết trong từng tháng mà không làm xẹp dòng dữ liệu.
6. **Q6 (Window Function `COUNT(*) OVER`):** Tính tổng số lượt thích tích lũy và tỷ lệ phần trăm đóng góp của từng bài viết trong nhóm.
7. **Q7 (Window Function `LAG`):** Tính khoảng cách thời gian giữa hai lần đăng bài liên tiếp của cùng một tác giả để phân tích tần suất hoạt động.
8. **Q8 (Self-Join & Grouping):** Thống kê số lượng bạn chung giữa từng cặp người dùng trong hệ thống.

---

## 4.2 Lập trình Cơ sở dữ liệu nâng cao (Q9 – Q12)
- **Q9 (Trigger kiểm tra cây bình luận - BR6):** Trigger `trg_check_comment_parent` chặn đứng việc bình luận con trỏ vào bình luận cha thuộc bài viết khác hoặc trỏ vào chính nó:
  ```sql
  CREATE OR REPLACE FUNCTION fn_check_comment_parent() RETURNS TRIGGER AS $$
  BEGIN
      IF NEW.parent_id IS NOT NULL THEN
          IF NEW.parent_id = NEW.comment_id THEN
              RAISE EXCEPTION 'Bình luận không thể làm cha của chính nó';
          END IF;
          IF NOT EXISTS (
              SELECT 1 FROM comment p 
              WHERE p.comment_id = NEW.parent_id AND p.post_id = NEW.post_id
          ) THEN
              RAISE EXCEPTION 'Bình luận cha phải thuộc cùng một bài viết';
          END IF;
      END IF;
      RETURN NEW;
  END;
  $$ LANGUAGE plpgsql;
  ```
- **Q10 (Stored Procedure kết bạn nguyên tử):** `proc_add_friend(u1, u2)` thực hiện chuẩn hóa thứ tự `user_a < user_b`, ghi nhận quan hệ trong `friendship` và đồng thời tăng bộ đếm `friend_count` của cả 2 người dùng trong 1 giao dịch nguyên tử.
- **Q11 (Procedure chuyển nhánh an toàn chặn chu trình):** `proc_move_comment(target_id, new_parent_id)` sử dụng CTE đệ quy kiểm tra nếu `new_parent_id` nằm trong tập hậu duệ của `target_id` thì lập tức hủy thao tác với thông báo lỗi.
- **Q12 (Dynamic SQL chống SQL Injection):** Hàm `fn_search_posts_dynamic(keyword)` dùng hàm `format()` với định dạng `%L` (literal escaping) để tham số hóa an toàn chuỗi truy vấn động, vô hiệu hóa hoàn toàn các chuỗi tấn công như `' OR 1=1 --`.
- **SQL nhúng (Embedded SQL):** Cung cấp mã nguồn Python [sql_advanced/embedded/psycopg2_cursor.py](file:///c:/Users/shuut/Documents/CSDL_Nangcao/sql_advanced/embedded/psycopg2_cursor.py) sử dụng con trỏ Client-side/Server-side và tham số hóa truy vấn an toàn qua biến môi trường.

---

## 4.3 SQL Đệ quy trên Đồ thị bạn bè (R1 – R4)
Duyệt đồ thị trên CSDL quan hệ thông qua View đối xứng `friend_edge` (thực hiện `UNION ALL` 2 chiều):
- **R1 (Bạn của bạn - FoF độ sâu $k=2$):** Tìm bạn của bạn của An (ID = 1), loại bỏ chính An và những người đã là bạn trực tiếp. Kết quả kiểm chứng: `{Dung (ID 4), Em (ID 5)}`.
- **R2 (Đường đi ngắn nhất BFS):** Thuật toán tìm kiếm theo chiều rộng duy trì mảng nút đã đi qua `ARRAY[1, b]` để chặn chu trình và dừng lại ngay ở độ sâu nhỏ nhất tìm thấy đích. Kết quả đường đi An $\rightarrow$ Em: `[1, 3, 5]` với độ dài 2 bước.
- **R3 (Phát hiện chu trình vòng kín):** Tìm các chu trình bạn bè khép kín độ dài 3 đến 5 (tam giác bạn bè). Kết quả phát hiện 3 chu trình: `(1-2-3)`, `(2-3-5-4)` và `(1-2-4-5-3)`.
- **R4 (Gợi ý kết bạn):** Đếm số lượng bạn chung giữa người dùng mục tiêu với những người chưa kết bạn và xếp hạng giảm dần theo độ ưu tiên.

---

## 4.4 Quản trị Giao dịch & Thực nghiệm Bế tắc (Deadlock T3)
- **Kịch bản T1 & T2:** Minh chứng tính toàn vẹn ACID, khả năng cô lập lỗi bằng `SAVEPOINT` để rollback cục bộ một thao tác thất bại mà không hủy toàn bộ giao dịch cha.
- **Thực nghiệm Deadlock T3 (Kiểm chứng thực tế):**
  - Session A xin khóa ghi User 1, sau đó yêu cầu khóa User 2.
  - Session B đồng thời xin khóa ghi User 2, sau đó yêu cầu khóa User 1.
  - Hệ quản trị PostgreSQL phát hiện chu trình chờ đợi tài nguyên (Wait-For Graph), kích hoạt cơ chế `deadlock_timeout` (mặc định 1 giây) và chủ động hủy giao dịch của Session A.
  - **Trích xuất log thực nghiệm nguyên văn từ [transactions/t3_concurrent/logs/deadlock_t3_log.txt](file:///c:/Users/shuut/Documents/CSDL_Nangcao/transactions/t3_concurrent/logs/deadlock_t3_log.txt):**
    ```text
    ERROR:  deadlock detected
    DETAIL:  Process 16484 waits for ShareLock on transaction 14459; blocked by process 13804.
    Process 13804 waits for ShareLock on transaction 14458; blocked by process 16484.
    HINT:  See server log for query details.
    CONTEXT:  while locking tuple (3,1) in relation "users"
    SQLSTATE: 40P01
    ```

---

# CHƯƠNG 5: CSDL HƯỚNG ĐỐI TƯỢNG VÀ CSDL ĐỒ THỊ CHUYÊN DỤNG

## 5.1 CSDL Hướng đối tượng: ODL, OQL và Phân tích Lệch pha trở kháng
- **Lược đồ ODL chuẩn ODMG 3.0 ([oo_model/schema.odl](file:///c:/Users/shuut/Documents/CSDL_Nangcao/oo_model/schema.odl)):**
  - Định nghĩa 6 lớp đối tượng: `NguoiDung`, `NhomHocTap`, `BaiDang`, `BaiThaoLuan`, `BaiTaiLieu`, `BinhLuan`.
  - Khai báo tường minh tập mở rộng (`extent`), mối quan hệ 2 chiều tự động đồng bộ (`inverse`), và các phương thức nghiệp vụ: `doSau(): Integer`, `soBanChung(in NguoiDung u): Integer`.
- **Bộ 8 truy vấn OQL ([oo_model/oql_queries.md](file:///c:/Users/shuut/Documents/CSDL_Nangcao/oo_model/oql_queries.md)):**
  - Minh họa điều hướng đối tượng bằng toán tử dấu chấm (`.`): `p.tacGia.hoTen` (không cần viết lệnh `JOIN`).
  - Gọi phương thức trực tiếp trong điều kiện lọc: `SELECT c.noiDung FROM c IN dsBinhLuan WHERE c.doSau() >= 3;`.
- **Phân tích hiện tượng Lệch pha trở kháng (Impedance Mismatch) trong [oo_model/jpql_mapping.md](file:///c:/Users/shuut/Documents/CSDL_Nangcao/oo_model/jpql_mapping.md):**
  - *Lệch pha về mô hình kế thừa:* RDBMS không hỗ trợ kế thừa bản địa $\Rightarrow$ Phải ánh xạ qua bảng phụ hoặc Single Table kèm cột phân biệt loại.
  - *Lệch pha về bản sắc đối tượng (Object Identity vs Primary Key):* OOP quản lý bằng địa chỉ bộ nhớ/OID, còn RDBMS dựa trên giá trị dữ liệu của khóa chính.
  - *Vấn đề $N+1$ truy vấn trong ORM (JPA/Hibernate):* Khi duyệt danh sách bình luận kèm tác giả, ORM có thể bắn thêm $N$ truy vấn con xuống database nếu không dùng `JOIN FETCH`.

---

## 5.2 CSDL Đồ thị chuyên dụng Neo4j & Đối chiếu Cypher
Hệ thống đồ thị 6 người dùng đã được triển khai hoàn chỉnh trên Neo4j Community ([neo4j/](file:///c:/Users/shuut/Documents/CSDL_Nangcao/neo4j/)):
- **Mô hình nhãn và quan hệ:**
  - Nút: `(:User {id, name, email})`.
  - Cạnh: `[:FRIEND]` (quan hệ 2 chiều), `[:FOLLOWS]` (quan hệ 1 chiều).
- **Hiện thực 4 bài toán đồ thị bằng Cypher:**
  1. *Bạn của bạn (FoF):*
     ```cypher
     MATCH (an:User {name: 'An'})-[:FRIEND]-(:User)-[:FRIEND]-(fof:User)
     WHERE fof <> an AND NOT (an)-[:FRIEND]-(fof)
     RETURN DISTINCT fof.id, fof.name;
     ```
  2. *Đường đi ngắn nhất:* Dùng hàm bản địa `shortestPath`:
     ```cypher
     MATCH p = shortestPath((an:User {name: 'An'})-[:FRIEND*..6]-(em:User {name: 'Em'}))
     RETURN [n IN nodes(p) | n.name] AS path, length(p) AS len;
     ```
  3. *Phát hiện chu trình:* `MATCH p = (a:User)-[:FRIEND*3..5]-(a) RETURN DISTINCT [n IN nodes(p) | n.id];`.
- **Minh chứng trực quan từ Neo4j Browser ([neo4j/screenshots/](file:///c:/Users/shuut/Documents/CSDL_Nangcao/neo4j/screenshots/)):**
  - Ảnh 1: [01_neo4j_full_graph.png](file:///c:/Users/shuut/Documents/CSDL_Nangcao/neo4j/screenshots/01_neo4j_full_graph.png) — Toàn cảnh mạng lưới 6 nút và các liên kết kết bạn/theo dõi.
  - Ảnh 2: [02_neo4j_friends_of_friends.png](file:///c:/Users/shuut/Documents/CSDL_Nangcao/neo4j/screenshots/02_neo4j_friends_of_friends.png) — Mạng lưới bạn của bạn.
  - Ảnh 3: [03_neo4j_shortest_path.png](file:///c:/Users/shuut/Documents/CSDL_Nangcao/neo4j/screenshots/03_neo4j_shortest_path.png) — Đường đi ngắn nhất `An -> Chi -> Em`.
  - Ảnh 4: [04_neo4j_cycle_detection.png](file:///c:/Users/shuut/Documents/CSDL_Nangcao/neo4j/screenshots/04_neo4j_cycle_detection.png) — Chu trình tam giác bạn bè `(1-2-3)`.

---

## 5.3 So sánh đối chiếu toàn diện: PostgreSQL vs Neo4j
| Tiêu chí so sánh | PostgreSQL (`WITH RECURSIVE`) | Neo4j (`Cypher`) |
| :--- | :--- | :--- |
| **Mô hình dữ liệu** | Bảng quan hệ 2 chiều phẳng (Cạnh biểu diễn qua bảng nối). | Đồ thị thuộc tính (Lưu con trỏ trực tiếp giữa các nút - Index-free Adjacency). |
| **Cú pháp truy vấn** | Khá phức tạp: Cần điểm neo (Anchor), bước đệ quy, phép `UNION ALL` và mảng vết thủ công để chặn chu trình. | Cực kỳ trực quan: Khai báo mẫu đồ thị tự nhiên bằng ký hiệu ASCII art `(a)-[:REL]->(b)`. |
| **Hiệu năng duyệt sâu ($k \ge 3$)** | Giảm mạnh do chi phí `JOIN` lặp lại nhiều lần trên các bảng quan hệ lớn. | Duy trì ổn định cao nhờ duyệt con trỏ bộ nhớ trực tiếp, không phụ thuộc quy mô toàn bảng. |
| **Hỗ trợ Transaction & ACID** | **Cực mạnh, tiêu chuẩn vàng của ngành công nghiệp**, bảo đảm toàn vẹn dữ liệu hoàn hảo. | Hỗ trợ ACID mức đồ thị, nhưng quản lý ràng buộc nghiệp vụ bảng biểu phức tạp không thuận tiện bằng RDBMS. |
| **Khuyến nghị kiến trúc** | Phù hợp quản lý dữ liệu nghiệp vụ cốt lõi, cây phân cấp, và đồ thị nông ($k \le 2$). | Phù hợp phân tích mạng xã hội, phát hiện gian lận, gợi ý kết bạn phức tạp đa chiều. |

---

# CHƯƠNG 6: THIẾT KẾ VẬT LÝ, BENCHMARK & THỬ TẢI ĐỒNG THỜI

## 6.1 Kế hoạch Đánh chỉ mục & Đo lường dung lượng đĩa
Theo kế hoạch tại [benchmark/indexes.sql](file:///c:/Users/shuut/Documents/CSDL_Nangcao/benchmark/indexes.sql) và công cụ đo [benchmark/storage_sizes.sql](file:///c:/Users/shuut/Documents/CSDL_Nangcao/benchmark/storage_sizes.sql):
- **Adjacency List:** Chỉ mục `B-tree (post_id, parent_id)` giúp tăng tốc độ lọc điểm neo và phép nối trong CTE đệ quy. Dung lượng chỉ mục nhỏ nhất.
- **Path Enumeration:** Chỉ mục chuyên dụng `GiST` trên cột kiểu `ltree` cho phép quét mẫu tiền tố đường dẫn siêu tốc.
- **Nested Set:** Chỉ mục `Composite (post_id, lft, rgt)` giúp chuyển đổi câu quét cây con từ Seq Scan sang Index Only Scan.
- **Closure Table:** Hai chỉ mục `(ancestor, depth, descendant)` và `(descendant, ancestor)`. Dung lượng đĩa lớn nhất do số lượng bản ghi bảng bao đóng tăng theo bình phương độ sâu cây.

---

## 6.2 Đánh giá hiệu năng 4 mô hình cây phân cấp (Benchmark)
Nhóm đã xây dựng bộ công cụ tự động hóa toàn diện bằng Python:
- Script sinh dữ liệu: [gen_tree_data.py](file:///c:/Users/shuut/Documents/CSDL_Nangcao/benchmark/scripts/gen_tree_data.py) sinh cây ngẫu nhiên với seed cố định (`SEED=42`), hỗ trợ các quy mô 1.000, 10.000 và 100.000 nút.
- Script đo đạc: [run_benchmark.py](file:///c:/Users/shuut/Documents/CSDL_Nangcao/benchmark/scripts/run_benchmark.py) thu thập kế hoạch thực thi `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)`.
- Script vẽ biểu đồ: [plot_results.py](file:///c:/Users/shuut/Documents/CSDL_Nangcao/benchmark/scripts/plot_results.py) tự động vẽ biểu đồ cột so sánh thời gian thực thi trước và sau khi đánh index.

**Bảng phân tích đánh đổi (Trade-off Matrix) giữa 4 mô hình cây:**
```
                     TỐC ĐỘ ĐỌC CÂY CON (Q2) vs CHI PHÍ GHI & CẬP NHẬT
[Tốc độ đọc nhanh]  Closure Table > Nested Set > Path Enumeration (ltree) > Adjacency List
[Tốc độ ghi nhanh]  Adjacency List > Path Enumeration > Closure Table > Nested Set
[Dung lượng đĩa]    Adjacency List (nhẹ nhất) < Path Enumeration < Nested Set < Closure Table (nặng nhất)
```
*Kết luận rút ra:* Đối với ứng dụng mạng xã hội học tập nơi tỷ lệ thao tác là 90% Đọc và 10% Ghi:
- **Path Enumeration (`ltree`):** Là lựa chọn cân bằng hoàn hảo nhất trên PostgreSQL nhờ cú pháp gọn gàng và chỉ mục GiST tối ưu.
- **Closure Table:** Phù hợp nhất khi cần truy vấn quan hệ tổ tiên - hậu duệ đa tầng và tính khoảng cách độ sâu tức thì.

---

## 6.3 Thử tải đồng thời bằng `pgbench` (Kết quả thực nghiệm)
Thực nghiệm đo lường thông lượng (TPS) và độ trễ (Latency) của thủ tục kết bạn nguyên tử `proc_add_friend` dưới tải đồng thời cao được ghi nhận chính xác trong [transactions/pgbench/results.md](file:///c:/Users/shuut/Documents/CSDL_Nangcao/transactions/pgbench/results.md):

| Quy mô tải (`-c` clients) | Tổng số Transaction | Tỷ lệ thành công | Tỷ lệ lỗi / Deadlock | Độ trễ trung bình *(Latency)* | Thông lượng *(TPS)* |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **5 clients** | 500 | 500 / 500 (100%) | **0.00%** | **1.448 ms** | **3.452,90 TPS** |
| **10 clients** | 1.000 | 1.000 / 1.000 (100%) | **0.00%** | **2.912 ms** | **3.434,18 TPS** |
| **20 clients** | 2.000 | 2.000 / 2.000 (100%) | **0.00%** | **5.814 ms** | **3.439,94 TPS** |

*Nhận xét kết quả:*
1. **Tính ổn định của hệ thống:** Thông lượng duy trì cực kỳ bền bỉ ở mức xấp xỉ **3.440 TPS** ngay cả khi số lượng client tăng gấp 4 lần (từ 5 lên 20 kết nối).
2. **Độ trễ:** Tăng tuyến tính từ 1.44ms lên 5.81ms khi số lượng luồng cạnh tranh tăng lên, nhưng vẫn nằm sâu dưới ngưỡng chấp nhận được của hệ thống thời gian thực (< 10ms).
3. **Không phát sinh bế tắc:** Nhờ quy ước chuẩn hóa thứ tự khóa `user_a < user_b` trong Stored Procedure, tất cả 2.000 giao dịch đồng thời đều hoàn thành mà không có bất kỳ giao dịch nào bị hủy do Deadlock.

---

## 6.4 Ma trận Kiểm thử Mức cô lập Giao dịch
Kiểm chứng thực tế 4 hiện tượng bất thường trên 3 mức cô lập của PostgreSQL ([transactions/t3_concurrent/isolation_matrix.md](file:///c:/Users/shuut/Documents/CSDL_Nangcao/transactions/t3_concurrent/isolation_matrix.md)):

| Mức cô lập | Dirty Read | Non-Repeatable Read | Phantom Read | Serialization Failure | Kết quả quan sát thực tế |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Read Committed** *(Mặc định)* | ❌ Không | ⚠️ **Có xảy ra** | ⚠️ **Có xảy ra** | ⚠️ Có xảy ra | Đọc lần 1 ra 2 dòng; Session B commit chèn dòng mới $\Rightarrow$ Đọc lần 2 ra 3 dòng ngay trong cùng 1 Transaction A. |
| **Repeatable Read** | ❌ Không | ❌ **Không** | ❌ **Không** | ⚠️ Có thể xảy ra | PostgreSQL áp dụng kỹ thuật MVCC Snapshot Isolation, chụp ảnh dữ liệu tại thời điểm câu lệnh đầu tiên bắt đầu $\Rightarrow$ Chặn thành công cả Non-Repeatable Read và Phantom Read. |
| **Serializable** | ❌ Không | ❌ Không | ❌ Không | ❌ **Không** | Thuật toán SSI (Serializable Snapshot Isolation) theo dõi các vết đọc/ghi (SIREAD locks), phát hiện chu trình phụ thuộc chéo và tự động hủy 1 phiên với mã lỗi `40001` (`could not serialize access`). |


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
