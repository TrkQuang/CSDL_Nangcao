# QUY TRÌNH THIẾT KẾ VẬT LÝ & ĐO LƯỜNG HIỆU NĂNG (BENCHMARK)

> **Mục đích thư mục:** Chứa các kịch bản sinh dữ liệu lớn, script tự động đo lường thời gian thực thi, chi phí I/O (Buffer hit/read) và dung lượng đĩa của 4 mô hình cây và đồ thị trước/sau khi đánh chỉ mục.  
> **Người phụ trách:** TV5 (Hỗ trợ: TV2, TV3, TV4).

---

## 1. Kế Hoạch Đánh Chỉ Mục (Index Design)

- **Mô hình Adjacency List:** B-tree trên `parent_id` và `post_id`.
- **Mô hình Path Enumeration:** GiST index trên cột `path` (`ltree`) phục vụ toán tử `<@` và `@>`.
- **Mô hình Nested Set:** Composite index trên `(post_id, lft, rgt)`.
- **Mô hình Closure Table:** Composite index trên `(ancestor, depth)` và `(descendant, ancestor)`.
- **Đồ thị bạn bè:** B-tree trên `(user_a, user_b)` và chỉ mục trên VIEW / bảng `friendship`.

---

## 2. Quy Trình Đo 5 Bước Chuẩn
1. **Chuẩn bị:** Khởi tạo dữ liệu với seed cố định; chạy `VACUUM ANALYZE;` để bộ tối ưu hóa truy vấn có thống kê mới nhất.
2. **Khởi động (Warm-up):** Chạy câu lệnh 1 lần để đưa các trang dữ liệu vào buffer cache (tránh lệch số đo do cold cache).
3. **Đo đạc:** Chạy lặp lại từ 5 đến 10 lần, lấy giá trị trung vị (Median Execution Time).
4. **Thu thập chỉ số:** Dùng `EXPLAIN (ANALYZE, BUFFERS)` để ghi nhận:
   - Execution Time (ms)
   - Planning Time (ms)
   - Shared Hit Blocks / Shared Read Blocks
5. **Đo dung lượng & chi phí ghi:** Dùng `pg_relation_size()` để đo dung lượng bảng và dung lượng từng chỉ mục; đo thời gian thực hiện thao tác INSERT/UPDATE.

---

## 3. Các Tập Dữ Liệu Thử Nghiệm

- **Quy mô Cây:** 1.000 nodes, 10.000 nodes, 100.000 nodes (độ sâu trung bình 5 - 15 cấp).
- **Quy mô Đồ thị:**
  - Nhỏ: 1.000 nodes, 5.000 edges.
  - Trung bình: 10.000 nodes, 50.000 edges.
  - Lớn: 100.000 nodes, 500.000 edges.
