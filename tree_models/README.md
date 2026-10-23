# SO SÁNH 4 MÔ HÌNH LƯU TRỮ CÂY TRÊN RDBMS

> **Mục đích thư mục:** Nghiên cứu, triển khai và đánh giá thực nghiệm 4 mô hình lưu trữ dữ liệu phân cấp (Hierarchical / Tree Data) trên PostgreSQL.  
> **Người phụ trách chính:** TV2 (Hỗ trợ: TV5 | Review: TV3).  
> **Bộ 10 truy vấn chuẩn (Q1 – Q10):** Dùng chung cho cả 4 mô hình để so sánh tính tiện dụng cú pháp và hiệu năng.

---

## 1. Tổng Quan 4 Mô Hình

| Mô hình | Cơ chế biểu diễn | Ưu điểm | Nhược điểm |
| :--- | :--- | :--- | :--- |
| **Adjacency List** | Cột `parent_id` trỏ về cha | Thêm/sửa dễ, lưu trữ gọn | Đọc subtree cần đệ quy `WITH RECURSIVE` |
| **Path Enumeration** | Lưu đường dẫn (extension `ltree`) | Đọc subtree/ancestor rất nhanh bằng `<@`, `@>` | Cập nhật đường dẫn khi chuyển nhánh tốn kém |
| **Nested Set** | Lưu 2 giá trị khoảng `[lft, rgt]` | Đọc toàn bộ cây con bằng `BETWEEN`, không đệ quy | Chèn/xóa phải cập nhật lại một nửa số dòng trong bảng |
| **Closure Table** | Bảng quan hệ phụ `(ancestor, descendant, depth)` | Đọc cực nhanh, truy vấn linh hoạt, dễ chuyển nhánh | Tốn dung lượng lưu trữ ($O(N^2)$ trong trường hợp xấu) |

---

## 2. Danh Sách 10 Truy Vấn Chuẩn (Q1 – Q10)

- **Q1:** Lấy toàn bộ cây theo thứ tự phân cấp (indent/thụt đầu dòng).
- **Q2:** Lấy toàn bộ hậu duệ (subtree) của một node cho trước.
- **Q3:** Lấy toàn bộ tổ tiên (ancestors/breadcrumb) của một node.
- **Q4:** Lấy các node con ở độ sâu xác định $k$.
- **Q5:** Thêm một node mới vào cây làm con của một node cho trước.
- **Q6:** Xóa một node và toàn bộ cây con của nó.
- **Q7:** Di chuyển một nhánh (subtree) sang một cha mới (có chặn di chuyển vào chính con/cháu nó).
- **Q8:** Đếm tổng số node trong cây con của một node.
- **Q9:** Lấy đường đi từ node hiện tại ngược về node gốc.
- **Q10:** Kiểm tra nhanh xem node A có phải là tổ tiên của node B hay không.

---

## 3. Quy Trình Kiểm Thử & Nghiệm Thu
1. Mọi mô hình phải chạy trên cùng bộ dữ liệu [seed_test.sql](file:///c:/Users/shuut/Documents/CSDL_NC/database/seed_test.sql) của bài 1 (cây bình luận $c_1 \rightarrow c_2 \rightarrow c_3$).
2. Kết quả truy vấn Q1–Q10 của cả 4 mô hình **bắt buộc phải trùng khớp** trước khi mang đi đo hiệu năng với dữ liệu lớn.
