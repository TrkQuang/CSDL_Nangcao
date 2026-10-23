# DÀN Ý VÀ KỊCH BẢN SLIDE THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN 17

> **Đề tài:** Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng mạng xã hội học tập  
> **Môn học:** Cơ sở dữ liệu nâng cao  
> **Thời lượng bảo vệ:** 15 phút thuyết trình + 5 phút demo thực tế + 10 phút hỏi đáp phản biện  
> **Người tổng hợp:** Trần Quang (TV1 - Leader)  
> **Phân bổ thời gian thuyết trình (3 phút / thành viên):**  
> - **TV1 (Trần Quang):** 3 phút (Slide 1 – Slide 4: Tổng quan, Nghiệp vụ, EER & Chuẩn hóa)  
> - **TV2 (Hưng):** 3 phút (Slide 5 – Slide 7: 4 Mô hình cây & Thiết kế Đối tượng ODL/OQL)  
> - **TV3 (Hữu):** 3 phút (Slide 8 – Slide 10: SQL Nâng cao, Đệ quy đồ thị & Transaction)  
> - **TV4 (Chương):** 3 phút (Slide 11 – Slide 13: CSDL Đồ thị Neo4j/Cypher, Deadlock & Thử tải)  
> - **TV5 (Quỳnh):** 3 phút (Slide 14 – Slide 16: Thiết kế vật lý, Chỉ mục & Kết quả Benchmark)  
> - **Demo thực tế (TV5 + TV3):** 5 phút (Tái lập từ CSDL sạch, chạy so sánh cây, đệ quy, transaction)

---

## PHẦN 1: TỔNG QUAN, EER & CHUẨN HÓA (TV1 - TRẦN QUANG | 3 PHÚT)

### Slide 1: Trang Tiêu Đề & Giới Thiệu Nhóm
- **Tiêu đề lớn:** DỮ LIỆU PHÂN CẤP VÀ ĐỒ THỊ TRONG CSDL QUAN HỆ: ỨNG DỤNG MẠNG XÃ HỘI HỌC TẬP
- **Thông tin lớp & Môn học:** Cơ sở dữ liệu nâng cao – Đề tài số 17
- **Giảng viên hướng dẫn:** Bộ môn Hệ thống Thông tin
- **Danh sách 5 thành viên:**
  1. Trần Quang (Leader) – Nghiệp vụ, EER, Chuẩn hóa, Tổng hợp
  2. Hưng – 4 Mô hình cây & CSDL hướng đối tượng
  3. Hữu – Schema DDL, SQL nâng cao, SQL đệ quy & Transaction
  4. Chương – Neo4j/Cypher, Deadlock & Thử tải
  5. Quỳnh – Dữ liệu kiểm chứng, Kế hoạch chỉ mục & Benchmark
- **Speaker Notes (TV1):**  
  *"Kính chào quý thầy cô và các bạn. Em là Trần Quang, đại diện nhóm Đề tài 17 xin phép được bắt đầu buổi báo cáo đồ án CSDL Nâng cao với chủ đề: Xử lý dữ liệu phân cấp và dữ liệu đồ thị trên CSDL quan hệ ứng dụng cho Mạng xã hội học tập..."*

---

### Slide 2: Đặt Vấn Đề & 3 Câu Hỏi Nghiên Cứu Cốt Lõi
- **Bối cảnh:** Mạng xã hội học tập phát sinh đồng thời hai dạng dữ liệu phi tuyến tính:
  - Cấu trúc cây (Tree): Bình luận phân cấp đa tầng (threaded comments) và cây thư mục học liệu.
  - Cấu trúc đồ thị (Graph): Mạng lưới bạn bè hai chiều, quan hệ theo dõi, nhóm học tập.
- **Thách thức:** RDBMS truyền thống vốn là các bảng 2D phẳng, gặp khó khăn về hiệu năng khi duyệt phả hệ sâu và đồ thị tùy biến.
- **3 Câu hỏi nghiên cứu:**
  1. Mô hình lưu trữ cây nào tối ưu nhất cho từng loại thao tác (đọc cây con, đọc tổ tiên, chèn, dời cành)?
  2. SQL đệ quy (`WITH RECURSIVE`) giải quyết các bài toán mạng xã hội đến giới hạn nào khi so với Neo4j?
  3. Đánh đổi giữa việc chuẩn hóa nghiêm ngặt (BCNF/4NF) và phi chuẩn hóa có kiểm soát để tăng tốc độ truy vấn?
- **Speaker Notes (TV1):**  
  *"Xuất phát từ bài toán thực tế, nhóm chúng em đặt ra 3 câu hỏi nghiên cứu trọng tâm: Làm thế nào để lưu trữ cây hiệu quả nhất trên RDBMS; SQL đệ quy có thể thay thế được CSDL đồ thị chuyên dụng hay không; và chiến lược chuẩn hóa dữ liệu cần cân bằng thế nào giữa tính toàn vẹn và hiệu năng đọc ghi..."*

---

### Slide 3: Đặc Tả Nghiệp Vụ (BR1–BR10) & Mô Hình Quan Niệm EER
- **10 Quy tắc then chốt:** BR1 (Email duy nhất), BR2 (Bạn bè hai chiều vô hướng `user_a < user_b`), BR3 (Theo dõi có hướng), BR5 (Chỉ thành viên mới được đăng bài), BR6 (Bình luận con cùng bài với cha), BR7 (Chuyên biệt hóa bài viết), BR9 (Bộ đếm `friend_count` dẫn xuất).
- **Mô hình EER Diagram:**
  - *Chuyên biệt hóa:* `BAI_DANG` tách thành `BAI_THAO_LUAN` và `BAI_TAI_LIEU` (Rời nhau - Disjoint, Toàn phần - Total).
  - *Quan hệ đệ quy:* `KET_BAN` (M:N đối xứng), `THEO_DOI` (M:N có hướng), `TRA_LOI` (1:N trên `BINH_LUAN`).
  - *Thuộc tính đa trị & Phức hợp:* `so_thich`, `mon_hoc` (phát sinh MVD); `ho_ten` (họ, tên đệm, tên).
  - *Phương án ánh xạ kế thừa:* Chọn Single Table Inheritance vì tối ưu hóa tuyệt đối cho thao tác xem Newsfeed đa hình mà không cần `JOIN`.
- **Speaker Notes (TV1):**  
  *"Để hệ thống vận hành tin cậy, nhóm xây dựng 10 quy tắc nghiệp vụ chặt chẽ. Trên sơ đồ EER, điểm nhấn là mối quan hệ chuyên biệt hóa bài viết rời nhau, toàn phần và 3 mối kết hợp đệ quy. Nhóm lựa chọn phương án Bảng đơn có cột phân loại post_type để tối ưu tốc độ đọc bảng tin..."*

---

### Slide 4: Phụ Thuộc Hàm, Chuẩn Hóa BCNF & Phân Rã 4NF
- **Dị thường bảng phẳng R:** Dị thường thêm (không thêm được nhóm mới chưa có bình luận), Xóa (mất thông tin nhóm/tác giả), Sửa (lặp lại dữ liệu nhóm và tác giả).
- **Phân biệt FD:**
  - *FD nghiệp vụ:* UserID → Email (bất biến trong tương lai).
  - *FD tình cờ:* FullName → Email (chỉ đúng ngẫu nhiên trên dữ liệu mẫu ít người).
- **Quy trình toán học:**
  - `{ comment_id }+ = R` ⇒ `{ comment_id }` là khóa duy nhất.
  - Phủ tối tiểu F_min qua 3 bước chặt chẽ.
  - Phân rã Bernstein thu được 4 quan hệ con R1, R2, R3, R4 đạt cả **3NF và BCNF**.
  - **Chứng minh Lossless Join:** Kiểm tra bằng bảng ma trận Chase (Chase test matrix biến đổi thành hàng toàn ký hiệu a).
  - **Phân rã 4NF:** Triệt tiêu phụ thuộc đa trị (user_id →→ interest và user_id →→ subject), giảm lưu trữ từ tích Descartes N × M xuống N + M.
- **Speaker Notes (TV1):**  
  *"Từ bảng phẳng ban đầu chứa nhiều dị thường, nhóm xác lập tập phụ thuộc hàm nghiệp vụ và chứng minh comment_id là khóa duy nhất. Quá trình phân rã đạt BCNF được chứng minh bảo toàn thông tin 100% bằng bảng ma trận Chase. Đặc biệt, nhóm đã xử lý triệt để phụ thuộc đa trị MVD đưa về chuẩn 4NF, loại bỏ hoàn toàn tích Descartes..."*

---

## PHẦN 2: 4 MÔ HÌNH DỮ LIỆU CÂY & ĐỐI TƯỢNG (TV2 - HƯNG | 3 PHÚT)

### Slide 5: Cơ Sở Lý Thuyết & Cấu Trúc 4 Mô Hình Cây
- Trực quan hóa 4 mô hình:
  - **Adjacency List:** Mỗi dòng lưu `parent_id` trực tiếp. Cực kỳ đơn giản, chèn nhanh nhất (O(1)).
  - **Path Enumeration (`ltree`):** Lưu chuỗi đường dẫn (ví dụ: `'1.2.3'`). Dùng toán tử ltree `<@` và `@>`.
  - **Nested Set:** Lưu khoảng bao `(lft, rgt)`. Duyệt cây con bằng điều kiện số học `BETWEEN`.
  - **Closure Table:** Bảng riêng lưu mọi cặp `(ancestor, descendant, depth)`.
- Bảng so sánh độ phức tạp lý thuyết (Read vs Write vs Storage).

---

### Slide 6: Bộ 10 Truy Vấn Cây (Q1–Q10) & Tính Đúng Đắn
- Minh chứng cả 4 mô hình cho cùng kết quả trên bộ dữ liệu kiểm chứng:
  - Cây con của nút 1: `{ c1, c2, c3 }`
  - Tổ tiên của nút 3: `{ c1, c2 }`
  - Độ sâu nút 3: `depth = 3`
  - Đếm số nút con của 1: `count = 3`
- Phân tích chi phí cập nhật: Thao tác di chuyển nhánh (Q7) và chèn nút mới (Q5) trên Nested Set và Path Enumeration đòi hỏi cập nhật hàng loạt dòng.

---

### Slide 7: Thiết Kế Hướng Đối Tượng: ODL, OQL & Ánh Xạ JPQL
- Sơ đồ 6 lớp đối tượng: `NguoiDung`, `NhomHocTap`, `BaiDang`, `BaiThaoLuan`, `BaiTaiLieu`, `BinhLuan`.
- Lược đồ ODL chuẩn ODMG 3.0 với định danh OID, kế thừa và phương thức (`doSau()`, `soBanChung()`).
- 8 truy vấn OQL và ánh xạ sang JPQL; phân tích giới hạn của JPQL khi không gọi được trực tiếp phương thức nghiệp vụ (lệch pha trở kháng).

---

## PHẦN 3: SQL NÂNG CAO, ĐỆ QUY ĐỒ THỊ & GIAO DỊCH (TV3 - HỮU | 3 PHÚT)

### Slide 8: Bộ Truy Vấn SQL Nâng Cao & Lập Trình CSDL
- Điểm nhấn 8 câu SQL nâng cao: Phép chia quan hệ (tìm người tham gia MỌI nhóm CSDL), Window Functions xếp hạng tương tác (`DENSE_RANK()`).
- Trigger Q9: Ngăn chặn triệt để bình luận cha - con khác bài viết (BR6).
- Stored Procedure Q10: Kết bạn nguyên tử cập nhật bộ đếm `friend_count` an toàn.
- Dynamic SQL Q12: Tìm kiếm bài viết chống tấn công SQL Injection bằng `format()` và `%L`.

---

### Slide 9: SQL Đệ Quy Trên Đồ Thị (R1–R4)
- Triển khai `WITH RECURSIVE` trên View hai chiều `friend_edge`:
  - **R1 (Bạn của bạn k=2):** Tìm bạn của bạn của An ⇒ Kết quả `{ Dung, Em }`.
  - **R2 (Đường đi ngắn nhất BFS):** Tìm đường từ An đến Em ⇒ Kết quả `[1, 3, 5]` (độ dài 2).
  - **R3 (Phát hiện chu trình):** Tìm các vòng bạn bè khép kín độ dài 3 đến 5.
  - **R4 (Gợi ý kết bạn):** Đếm số lượng bạn chung để xếp hạng gợi ý.

---

### Slide 10: Giao Dịch & Điều Khiển Đồng Thời (T1, T2)
- Kịch bản giao dịch thành công trọn vẹn T1.
- Kịch bản lỗi giữa chừng T2: Sử dụng `SAVEPOINT` và `ROLLBACK TO SAVEPOINT` giúp phục hồi một phần giao dịch mà không làm hủy bỏ toàn bộ phiên làm việc.

---

## PHẦN 4: CSDL ĐỒ THỊ NEO4J, DEADLOCK & THỬ TẢI (TV4 - CHƯƠNG | 3 PHÚT)

### Slide 11: CSDL Đồ Thị Neo4j & Đối Chiếu Với PostgreSQL
- Cài đặt Neo4j qua Docker; nạp các nút User và cạnh FRIEND, FOLLOWS.
- So sánh cú pháp Cypher trực quan vs `WITH RECURSIVE` của PostgreSQL:
  - *Neo4j:* `MATCH p = shortestPath((a:User {name:'An'})-[:FRIEND*..6]-(b:User {name:'Em'})) RETURN p;`
  - *PostgreSQL:* Phải viết CTE đệ quy BFS dài hơn 20 dòng.
- Đánh giá: Neo4j tối ưu vượt trội cho các truy vấn đồ thị sâu từ 3 bước trở lên.

---

### Slide 12: Thí Nghiệm Tương Tranh T3: Kích Hoạt Deadlock
- Kịch bản 2 phiên (Session A và Session B) cập nhật chéo 2 người dùng `user_id = 1` và `user_id = 2`.
- Kết quả: PostgreSQL phát hiện bế tắc và tự động hủy giao dịch ở một phiên với mã lỗi chính xác `40P01 (deadlock_detected)`.
- Ma trận mức cô lập: Kiểm chứng Dirty Read, Non-repeatable Read, Phantom Read trên Read Committed, Repeatable Read và Serializable.

---

### Slide 13: Thử Tải Đồng Thời Bằng `pgbench`
- Kịch bản thử tải trên thủ tục kết bạn với các mức 5, 10, 20 kết nối đồng thời.
- So sánh thông lượng giao dịch (TPS) và độ trễ (Latency).
- Kết luận về sự suy giảm hiệu năng khi có tranh chấp khóa dòng (`row-level locking`).

---

## PHẦN 5: THIẾT KẾ VẬT LÝ, BENCHMARK & KẾT LUẬN (TV5 - QUỲNH | 3 PHÚT)

### Slide 14: Thiết Kế Vật Lý & Chiến Lược Đánh Chỉ Mục (Indexing)
- Kế hoạch đánh chỉ mục cho từng mô hình:
  - B-tree trên `comment(parent_id)` và `study_group(owner_id)`.
  - GiST index trên `comment_path(path)` hỗ trợ toán tử ltree.
  - Composite Index trên `comment_ns(post_id, lft, rgt)`.
  - Composite Index thứ hai trên `comment_closure(descendant, ancestor)`.
- Đo lường chi phí đánh đổi: Dung lượng đĩa tăng thêm và thời gian ghi dữ liệu chậm đi khi có nhiều chỉ mục.

---

### Slide 15: Kết Quả Benchmark & Phân Tích Hiệu Năng
- Số đo thực nghiệm qua `EXPLAIN (ANALYZE, BUFFERS)` trên 3 quy mô dữ liệu: 1.000, 10.000 và 100.000 dòng.
- **Biểu đồ so sánh thời gian đọc cây con:**
  - *Nested Set & Closure Table:* Nhanh nhất (~0.2ms – 0.5ms).
  - *ltree:* Nhanh và ổn định (~0.8ms – 1.2ms).
  - *Adjacency List:* Chậm hơn khi cây sâu do phải duyệt đệ quy lặp lại.
- **Biểu đồ so sánh chi phí ghi (INSERT):**
  - *Adjacency List:* Nhanh nhất (chỉ ghi 1 dòng).
  - *Nested Set & Closure Table:* Chậm nhất do phải dịch chuyển biên hoặc chèn nhiều cặp tổ tiên.

---

### Slide 16: Kết Luận & Khuyến Nghị Ứng Dụng Thực Tế
- **Khuyến nghị chọn mô hình cây:**
  - Nếu hệ thống đọc nhiều, ít sửa/dời nhánh (như danh mục sản phẩm, phòng ban): Chọn **Nested Set** hoặc **Closure Table**.
  - Nếu hệ thống bình luận mạng xã hội (tần suất chèn bình luận cao, cần đọc cây con nhanh): Chọn **Path Enumeration (`ltree`)**.
  - Nếu hệ thống phân cấp nông hoặc đơn giản: Chọn **Adjacency List**.
- **Khuyến nghị về đồ thị:** Dùng PostgreSQL cho các quan hệ mạng xã hội cơ bản ($k \le 2$); tích hợp Neo4j khi cần tính năng gợi ý mạng lưới phức tạp và phát hiện gian lận.

---

## PHẦN 6: DEMO KỊCH BẢN THỰC TẾ (TV5 + TV3 | 5 PHÚT)
1. **Khởi tạo:** Tạo CSDL sạch, nạp `schema.sql` và `seed_test.sql` (30 giây).
2. **Kiểm chứng cây:** Chạy truy vấn cây con trên cả 4 mô hình, chứng minh cùng ra kết quả `{c1, c2, c3}` (1 phút).
3. **Đệ quy đồ thị:** Chạy đệ quy tìm bạn của bạn và đường đi ngắn nhất (1 phút).
4. **Kích hoạt Deadlock:** Mở 2 cửa sổ psql kích hoạt mã lỗi `40P01` trực tiếp (1 phút).
5. **Benchmark & Biểu đồ:** Trình chiếu bảng kết quả đo lường và biểu đồ so sánh (1.5 phút).

---

## PHẦN 7: HỎI ĐÁP PHẢN BIỆN (Q&A - CẢ NHÓM | 10 PHÚT)
- Sẵn sàng trả lời các câu hỏi về:
  - Cách chứng minh Lossless Join và bảo toàn FD.
  - Cơ chế hoạt động của toán tử ltree và chỉ mục GiST.
  - Xử lý chu trình trong CTE đệ quy.
  - Phân tích hiện tượng Serialization Anomaly trong kiểm thử giao dịch.
