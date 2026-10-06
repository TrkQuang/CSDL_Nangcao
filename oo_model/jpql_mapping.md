# ÁNH XẠ ODL/OQL SANG JPQL & PHÂN TÍCH LỆCH PHA TRỞ KHÁNG

> **Mục đích file:** Trình bày cơ chế ánh xạ từ lược đồ ODL sang các Entity Java JPA/Hibernate, chuyển dịch các câu OQL sang JPQL tương đương và phân tích hiện tượng lệch pha trở kháng (Object-Relational Impedance Mismatch).  
> **Người phụ trách:** TV2.

---

## 1. Ánh Xạ Kế Thừa Trong JPA (Inheritance Mapping)

So sánh 3 chiến lược ánh xạ quan hệ thừa kế từ `BaiDang` sang `BaiThaoLuan` và `BaiTaiLieu`:
1. **SINGLE_TABLE:** Gộp chung vào 1 bảng `post` kèm cột phân biệt `post_type` (PostgreSQL schema hiện tại đang dùng cách này).
2. **JOINED:** Tạo 3 bảng riêng: `post` (chứa thuộc tính chung), `post_discussion` và `post_document` (chứa thuộc tính riêng và FK trỏ về `post_id`).
3. **TABLE_PER_CLASS:** Mỗi lớp con là 1 bảng độc lập hoàn toàn.

---

## 2. Bảng Đối Chiếu Cú Pháp: OQL vs JPQL vs SQL

| Yêu cầu | OQL (ODMG) | JPQL (JPA/Hibernate) | SQL (PostgreSQL RDBMS) |
| :--- | :--- | :--- | :--- |
| **Lấy bài viết của User 1** | `SELECT u.dsBaiDaDang FROM u IN dsNguoiDung WHERE u.user_id = 1` | `SELECT p FROM Post p WHERE p.tacGia.userId = 1` | `SELECT * FROM post WHERE author_id = 1` |
| **Gọi phương thức tính toán** | `SELECT c.doSau() FROM c IN dsBinhLuan` | *Không hỗ trợ trực tiếp phương thức nghiệp vụ trong query* -> phải dùng Subquery / Custom Function | `WITH RECURSIVE ...` |

---

## 3. Phân Tích Độ Lệch Pha Trở Kháng (Impedance Mismatch)

- **Mô hình định danh:** OID (định danh đối tượng bằng con trỏ bộ nhớ) đối nghịch với Khóa chính (Primary Key giá trị) trong CSDL quan hệ.
- **Quan hệ lồng nhau & Đệ quy:** Trong OODBMS, một đối tượng chứa trực tiếp một `set` hoặc `list` các đối tượng khác. Trong RDBMS, buộc phải phân rã thành khóa ngoại và bảng trung gian (Junction Table).
- **Vấn đề N+1 Query:** Khi điều hướng quan hệ một-nhiều trong ORM, nếu không cấu hình Eager Fetch / JOIN FETCH sẽ phát sinh hàng trăm truy vấn phụ làm suy giảm hiệu năng nghiêm trọng.
