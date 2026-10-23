# DANH SÁCH PHỤ THUỘC HÀM (FUNCTIONAL DEPENDENCIES - FD)

> **Môn học:** Cơ sở dữ liệu nâng cao  
> **Đề tài 17:** Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng mạng xã hội học tập  
> **Người phụ trách:** TV1 - Trần Quang (Leader)  
> **Hỗ trợ:** TV5 (Quỳnh - Chạy kiểm chứng SQL) | **Review:** TV3 (Hữu - Kiểm tra ràng buộc DDL)  
> **Đầu ra:** Cơ sở toán học nền tảng để tìm bao đóng thuộc tính, xác định khóa chính/khóa ứng viên và thực hiện chuẩn hóa dữ liệu đạt 3NF, BCNF và 4NF.

---

## 1. LƯỢC ĐỒ QUAN HỆ TỔNG HỢP BAN ĐẦU (UNIVERSAL RELATION SCHEMA)

Trong thiết kế cơ sở dữ liệu, một sai lầm phổ biến của người mới bắt đầu hoặc khi lưu trữ dữ liệu dạng bảng phẳng (Denormalized Flat Table / Spreadsheet) là gộp tất cả các thuộc tính của các thực thể khác nhau vào một bảng duy nhất.

Xét lược đồ quan hệ tổng hợp `R` chứa thông tin bài viết, bình luận, tác giả và nhóm học tập:
```text
R = { comment_id, post_id, group_id, group_name, group_topic, author_id, author_name, author_email, parent_id, content, created_at }
```

### Các dị thường dữ liệu (Data Anomalies) phát sinh trên lược đồ phẳng R:

1. **Dị thường thêm (Insertion Anomaly):**
   - Giả sử một nhóm học tập mới vừa được thành lập (ví dụ nhóm "CSDL Nâng cao", chủ đề "Công nghệ thông tin") nhưng chưa có thành viên nào đăng bài viết hay để lại bình luận nào.
   - Do thuộc tính `comment_id` là khóa chính (hoặc thuộc tính định danh duy nhất của dòng), ta không thể thực hiện thao tác thêm nhóm mới này vào CSDL vì khóa chính không được phép nhận giá trị NULL (Entity Integrity Constraint).
   - Tương tự, một người dùng mới đăng ký tài khoản nhưng chưa bình luận bài nào cũng không thể lưu trữ thông tin trong `R`.

2. **Dị thường xóa (Deletion Anomaly):**
   - Giả sử bài viết mang mã `post_id = 5` chỉ có duy nhất một bình luận mang mã `comment_id = 10`. Nếu người dùng quyết định xóa bình luận này đi (`DELETE FROM R WHERE comment_id = 10`), toàn bộ bản ghi bị xóa bỏ.
   - Hậu quả: Hệ thống đồng thời làm mất luôn thông tin của bài viết `post_id = 5`, thông tin của nhóm học tập `group_id` và thông tin tác giả nếu những thông tin này chỉ tồn tại duy nhất ở dòng đó.

3. **Dị thường cập nhật (Update Anomaly):**
   - Thông tin của nhóm học tập (`group_name`, `group_topic`) và tác giả (`author_name`, `author_email`) bị lặp đi lặp lại trên hàng trăm, hàng nghìn dòng bình luận khác nhau thuộc cùng một nhóm hoặc cùng một tác giả.
   - Nếu nhóm học tập đổi tên hoặc tác giả đổi email, câu lệnh cập nhật bắt buộc phải quét và sửa đổi trên tất cả các dòng dữ liệu liên quan. Nếu xảy ra lỗi giữa chừng hoặc bỏ sót dù chỉ 1 dòng, CSDL sẽ rơi vào trạng thái mâu thuẫn, mất tính toàn vẹn (ví dụ cùng một `group_id = 1` nhưng dòng trên tên là "CSDL NC" dòng dưới lại ghi là "Cơ sở dữ liệu nâng cao").

---

## 2. TẬP PHỤ THUỘC HÀM HỢP LỆ THEO NGHIỆP VỤ (F)

Dựa trên 10 quy tắc nghiệp vụ (**BR1 – BR10**) đã đặc tả trong [docs/spec.md](file:///c:/Users/shuut/Documents/CSDL_NC/docs/spec.md), ta xác định được tập các phụ thuộc hàm cốt lõi `F = { f1, f2, f3, f4, f5 }` chi phối lược đồ `R`:

| Mã FD | Biểu diễn hình thức | Giải thích căn cứ nghiệp vụ |
| :---: | :--- | :--- |
| **f1** | `comment_id → post_id, author_id, parent_id, content, created_at` | Mỗi bình luận được định danh duy nhất bởi mã bình luận, thuộc về đúng một bài viết, do đúng một tác giả viết, có tối đa một bình luận cha trực tiếp, kèm nội dung và thời điểm đăng bài cụ thể. |
| **f2** | `post_id → group_id` | Mỗi bài viết đăng tải bắt buộc phải thuộc về đúng một nhóm học tập cụ thể (mỗi bài viết chỉ nằm trong một nhóm). |
| **f3** | `group_id → group_name, group_topic` | Mỗi nhóm học tập được định danh bởi mã nhóm; mã nhóm xác định duy nhất tên nhóm và chủ đề học thuật của nhóm. |
| **f4** | `author_id → author_name, author_email` | Mỗi người dùng (tác giả) có một mã định danh duy nhất; mã người dùng xác định duy nhất họ tên và email của người đó. |
| **f5** | `author_email → author_id, author_name` | Theo quy tắc **BR1**, mỗi người dùng đăng ký bằng một địa chỉ email duy nhất trên toàn hệ thống. Do đó, nếu biết email thì xác định ngược lại được mã tác giả và họ tên. |

---

## 3. PHÂN BIỆT RÕ RÀNG: FD NGHIỆP VỤ VS FD TÌNH CỜ ĐÚNG TRÊN DỮ LIỆU

> [!IMPORTANT]
> **Nguyên tắc vàng trong Chuẩn hóa CSDL:**
> Một phụ thuộc hàm `X → Y` chỉ được coi là một phụ thuộc hàm hợp lệ khi và chỉ khi nó là **quy tắc bất biến theo ngữ nghĩa nghiệp vụ thực tế**, tức là phải thỏa mãn trên **mọi trạng thái thể hiện hợp lệ của CSDL trong hiện tại và tương lai**.  
> Tuyệt đối không được coi một phụ thuộc hàm là đúng chỉ vì nó ngẫu nhiên thỏa mãn trên một tập dữ liệu mẫu hữu hạn!

### 3.1 Ví dụ về FD tình cờ (Accidental / Spurious Dependency - Sai nghiệp vụ):
1. **Xét phụ thuộc hàm: `author_name → author_email`**
   - *Trên bộ dữ liệu kiểm chứng nhỏ ([database/seed_test.sql](file:///c:/Users/shuut/Documents/CSDL_NC/database/seed_test.sql)):* Hệ thống chỉ có 6 người dùng thử nghiệm: An, Binh, Chi, Dung, Em, Phong. Mỗi người mang một tên khác nhau, nên nếu chạy câu truy vấn SQL kiểm tra vi phạm thì kết quả trả về là 0 dòng vi phạm.
   - *Phân tích thực tế nghiệp vụ:* Trong một trường đại học hay mạng xã hội thực tế có hàng nghìn sinh viên, việc hai người dùng trùng họ tên nhau (ví dụ: cùng tên "Nguyễn Văn A" nhưng có mã số sinh viên và email khác nhau: `a.nguyen1@fit.edu.vn` và `a.nguyen2@fit.edu.vn`) là hoàn toàn bình thường.
   - ⇒ Do đó, `author_name → author_email` là **FD sai nghiệp vụ**. Nếu đưa FD này vào thiết kế CSDL, hệ thống sẽ cấm người dùng thứ hai mang tên giống người dùng thứ nhất đăng ký tài khoản!

2. **Xét phụ thuộc hàm: `group_name → group_id`**
   - Nếu nghiệp vụ quy định tên nhóm học tập phải là duy nhất trên toàn hệ thống (`UNIQUE(name)`), thì đây là FD hợp lệ.
   - Nhưng nếu nghiệp vụ cho phép các giảng viên/sinh viên ở các khoa khác nhau cùng lập các nhóm mang tên "Ôn tập CSDL", thì hai nhóm khác nhau sẽ có cùng tên gọi ⇒ `group_name` không thể suy ra `group_id`. Đề tài 17 không đặt ràng buộc duy nhất trên tên nhóm, vì vậy FD này là **FD tình cờ**.

### 3.2 Cơ chế kiểm chứng bằng SQL (Proof by Counter-example):
Để chứng minh một FD `X → Y` bị vi phạm trên dữ liệu, ta dùng truy vấn gom nhóm:
```sql
SELECT X, COUNT(DISTINCT Y) AS distinct_y_count
FROM table_name
GROUP BY X
HAVING COUNT(DISTINCT Y) > 1;
```
- Nếu truy vấn trả về ≥ 1 dòng: Ta tìm được ít nhất một giá trị `X` suy ra nhiều giá trị `Y` khác nhau ⇒ Khẳng định chắc chắn `X không suy ra Y`.
- Nếu truy vấn trả về 0 dòng: Dữ liệu hiện tại **tạm thời chưa vi phạm**, nhưng **không thể dùng kết quả này để chứng minh** rằng FD đúng theo lý thuyết nếu không có lập luận nghiệp vụ bảo trợ.

---

## 4. TẠI SAO RÀNG BUỘC CÂY ĐỆ QUY KHÔNG PHẢI LÀ FD TRONG BẢNG PHẲNG?

Một thắc mắc lý thuyết thường gặp là: Theo quy tắc **BR6**, "Bình luận con bắt buộc phải thuộc cùng bài viết với bình luận cha", liệu ta có thể coi đây là một phụ thuộc hàm:
```text
parent_id → post_id   (???)
```

**Câu trả lời: KHÔNG**. Không thể đưa quan hệ này vào tập phụ thuộc hàm `F` của bảng phẳng `R` vì hai lý do kỹ thuật sau:
1. **Giá trị NULL ở bình luận gốc:** Với các bình luận gốc (top-level comment, không trả lời ai), thuộc tính `parent_id` nhận giá trị NULL. Định nghĩa chuẩn mực của phụ thuộc hàm trong mô hình quan hệ toán học không áp dụng trên các thuộc tính nhận giá trị NULL.
2. **Ràng buộc giữa các dòng khác nhau (Inter-row Dependency):** Thuộc tính `parent_id` của dòng hiện tại thực chất là giá trị `comment_id` của một **dòng khác** trong cùng bảng. Ràng buộc bảo đảm bình luận cha và con cùng thuộc một `post_id` là ràng buộc toàn vẹn giữa các dòng khác nhau trong quan hệ đệ quy, không phải là phụ thuộc hàm nội bộ trên các thuộc tính của cùng một bộ (tuple).
3. **Giải pháp chuẩn xác:** Ràng buộc này được cài đặt bằng **Trigger** `trg_check_comment_parent` (Câu truy vấn Q9) trên hệ quản trị CSDL, đảm bảo kiểm tra logic trước mọi thao tác INSERT hoặc UPDATE.
