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
| **OQL-4: Bình luận gốc của bài 1** | `SELECT c FROM c IN (SELECT b.dsBinhLuan FROM b IN dsBaiDang WHERE b.post_id = 1) WHERE c.binhLuanCha IS NULL` | `SELECT c FROM BinhLuan c WHERE c.baiDang.postId = 1 AND c.binhLuanCha IS NULL` | `SELECT * FROM comment WHERE post_id = 1 AND parent_id IS NULL` |
| **OQL-5: Bài thảo luận của nhóm do An chủ trì** | `SELECT d FROM d IN dsBaiThaoLuan WHERE d.thuocNhom.chuNhom.full_name = 'An'` | `SELECT d FROM BaiThaoLuan d WHERE d.thuocNhom.chuNhom.fullName = 'An'` (đa hình JPA `TYPE(d)` = BaiThaoLuan) | `SELECT p.* FROM post p JOIN study_group g ON p.group_id = g.group_id JOIN users u ON g.owner_id = u.user_id WHERE u.full_name = 'An' AND p.post_type = 'thaoluan'` |
| **OQL-6: Bạn bè của An** | `SELECT f.full_name FROM f IN (SELECT u.dsBanBe FROM u IN dsNguoiDung WHERE u.full_name = 'An')` | `SELECT f.fullName FROM NguoiDung u JOIN u.dsBanBe f WHERE u.fullName = 'An'` | `SELECT v.full_name FROM friendship e JOIN users v ON v.user_id IN (e.user_b, e.user_a) ...` (2 chiều qua view `friend_edge`) |
| **OQL-7: Đếm bài viết mỗi nhóm** | `SELECT g.name, count(g.dsBaiDang) FROM g IN dsNhomHocTap GROUP BY g.name` | `SELECT g.name, COUNT(p) FROM NhomHocTap g LEFT JOIN g.dsBaiDang p GROUP BY g.name` | `SELECT g.name, count(p.post_id) FROM study_group g LEFT JOIN post p ON p.group_id = g.group_id GROUP BY g.name` |
| **OQL-8: Bình luận độ sâu >= 3** | `SELECT c FROM c IN dsBinhLuan WHERE c.doSau() >= 3` | *Không gọi được `doSau()`* -> tính sẵn cột dẫn xuất `depth` hoặc dùng native recursive query | `WITH RECURSIVE t AS (... depth ...) SELECT ... WHERE depth >= 3` |

> **Nhận xét then chốt (impedance mismatch):** Ở cột JPQL, các thao tác *điều hướng
> quan hệ* (`u.dsBanBe`, `b.dsBinhLuan`) ánh xạ gần 1-1 với OQL; nhưng *gọi phương
> thức nghiệp vụ* (`doSau()`, `soBanChung()`) thì JPQL **không** cho phép — phải
> chuyển thành cột dẫn xuất, `JOIN FETCH`, hoặc native SQL đệ quy. Đây chính là
> điểm lệch pha giữa mô hình đối tượng (hành vi gắn với dữ liệu) và mô hình quan hệ.

---

## 3. Phân Tích Độ Lệch Pha Trở Kháng (Impedance Mismatch)

- **Mô hình định danh:** OID (định danh đối tượng bằng con trỏ bộ nhớ) đối nghịch với Khóa chính (Primary Key giá trị) trong CSDL quan hệ.
- **Quan hệ lồng nhau & Đệ quy:** Trong OODBMS, một đối tượng chứa trực tiếp một `set` hoặc `list` các đối tượng khác. Trong RDBMS, buộc phải phân rã thành khóa ngoại và bảng trung gian (Junction Table).
- **Vấn đề N+1 Query:** Khi điều hướng quan hệ một-nhiều trong ORM, nếu không cấu hình Eager Fetch / JOIN FETCH sẽ phát sinh hàng trăm truy vấn phụ làm suy giảm hiệu năng nghiêm trọng.
