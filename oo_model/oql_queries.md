# TRUY VẤN ĐỐI TƯỢNG (OBJECT QUERY LANGUAGE - OQL)

> **Mục đích file:** Xây dựng danh sách 5–8 câu truy vấn OQL chuẩn ODMG 3.0 thao tác trên lược đồ đối tượng trong [schema.odl](file:///c:/Users/shuut/Documents/CSDL_NC/oo_model/schema.odl), kèm kết quả kỳ vọng trên dữ liệu kiểm chứng.  
> **Người phụ trách:** TV2 (Review: TV1).

---

## Danh Sách Truy Vấn OQL

### [VÍ DỤ MẪU 1]: OQL-1: Lấy danh sách tên người dùng và các bài viết họ đã đăng
*Kỹ thuật:* Điều hướng qua thuộc tính quan hệ (Path navigation `u.dsBaiDaDang`).
```sql
SELECT u.full_name, u.dsBaiDaDang.title
FROM u IN dsNguoiDung;
```

---

### [VÍ DỤ MẪU 2]: OQL-2: Tìm tất cả tài liệu có kích thước lớn hơn 10MB
*Kỹ thuật:* Truy vấn trên phạm vi lớp con (Extent of Subclass `dsBaiTaiLieu`).
```sql
SELECT doc.title, doc.file_format, doc.file_size_kb
FROM doc IN dsBaiTaiLieu
WHERE doc.file_size_kb > 10240;
```

---

### [VÍ DỤ MẪU 3]: OQL-3: Gọi phương thức đối tượng đếm số bạn chung
*Kỹ thuật:* Gọi phương thức `soBanChung()` trực tiếp trong câu OQL.
```sql
SELECT u.full_name, u.soBanChung(an)
FROM u IN dsNguoiDung,
     an IN dsNguoiDung
WHERE an.user_id = 1 AND u.user_id <> 1;
```

---

### [TODO: TV2 bổ sung tiếp các truy vấn OQL 4 - 8]
- **OQL-4:** Lấy các bình luận gốc của bài viết có `post_id = 1` (`c.binhLuanCha IS NULL`).
- **OQL-5:** Lấy các bài thảo luận thuộc nhóm học tập do `An` làm chủ nhóm.
- **OQL-6:** Lấy danh sách bạn bè của `An` (`an.dsBanBe`).
- **OQL-7:** Thống kê số lượng bài viết của từng nhóm học tập (`count(g.dsBaiDang)`).
- **OQL-8:** Lấy các bình luận có độ sâu `c.doSau() >= 3`.
