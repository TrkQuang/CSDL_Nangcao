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

### OQL-4: Lấy các bình luận GỐC của bài viết có `post_id = 1`
*Kỹ thuật:* Điều hướng quan hệ `dsBinhLuan` rồi lọc bình luận không có cha
(`c.binhLuanCha IS NULL`).
*Kỳ vọng (seed):* 2 bình luận gốc của bài 1 là `c1` và `c4`.
```sql
SELECT c
FROM c IN (SELECT b.dsBinhLuan FROM b IN dsBaiDang WHERE b.post_id = 1)
WHERE c.binhLuanCha IS NULL;
```

---

### OQL-5: Lấy các bài THẢO LUẬN thuộc nhóm học tập do `An` làm chủ nhóm
*Kỹ thuật:* Điều hướng `g.chuNhom` (quan hệ 1-1) kết hợp lọc trên phạm vi lớp con
`dsBaiThaoLuan` để chỉ lấy bài thảo luận.
*Kỳ vọng (seed):* Nhóm 1 ("CSDL nâng cao") do An(1) chủ trì -> bài thảo luận là
`p1` ("Ôn tập chuẩn hóa CSDL").
```sql
SELECT d
FROM d IN dsBaiThaoLuan
WHERE d.thuocNhom.chuNhom.full_name = 'An';
```

---

### OQL-6: Lấy danh sách bạn bè của `An`
*Kỹ thuật:* Điều hướng tập hợp quan hệ đối xứng `an.dsBanBe` (relationship set).
*Kỳ vọng (seed):* Bạn của An(1) là `Binh(2)` và `Chi(3)`.
```sql
SELECT f.full_name, f.email
FROM f IN (SELECT u.dsBanBe FROM u IN dsNguoiDung WHERE u.full_name = 'An');
```

---

### OQL-7: Thống kê số lượng bài viết của từng nhóm học tập
*Kỹ thuật:* Dùng hàm tập hợp `count(...)` kết hợp `GROUP BY`, điều hướng `g.dsBaiDang`.
*Kỳ vọng (seed):* Nhóm 1 có 2 bài (`p1`,`p2`); Nhóm 2 có 1 bài (`p3`).
```sql
SELECT g.name, count(g.dsBaiDang) AS soBaiDang
FROM g IN dsNhomHocTap
GROUP BY g.name;
```

---

### OQL-8: Lấy các bình luận có độ sâu `>= 3`
*Kỹ thuật:* Gọi phương thức đối tượng `c.doSau()` (tính độ sâu trong cây bình luận)
ngay trong mệnh đề `WHERE`.
*Kỳ vọng (seed):* Trên cây `c1 -> c2 -> c3`, chỉ `c3` có `doSau() = 3`.
```sql
SELECT c.content, c.doSau() AS doSau
FROM c IN dsBinhLuan
WHERE c.doSau() >= 3;
```

---

## Ghi chú kiểm chứng (TV2)
- Các câu OQL ở trên là **lý thuyết (chuẩn ODMG 3.0)**, không chạy trực tiếp trên
  PostgreSQL. Để đối chiếu kết quả, dùng bộ truy vấn SQL tương đương trong
  `database/seed_test.sql` (cùng dữ liệu người dùng/bài viết/bình luận).
- Điểm then chốt thể hiện sức mạnh OODBMS: OQL **gọi phương thức đối tượng**
  (`doSau()`, `soBanChung()`) và **điều hướng quan hệ** (`dsBanBe`, `dsBinhLuanCon`)
  trực tiếp — điều mà SQL quan hệ phải dùng `JOIN`/`WITH RECURSIVE` mới làm được.
