# TỔNG KẾT PHẦN TV2 — 4 MÔ HÌNH CÂY & THIẾT KẾ HƯỚNG ĐỐI TƯỢNG

> Đề tài 17 · Người thực hiện: **Hưng (TV2)** · Review chéo: **Hữu (TV3)** · Nhận bàn giao: **Quỳnh (TV5)**
> Trạng thái: **Đã hoàn thành & kiểm chứng** trên PostgreSQL 18.6 với seed TV3.

---

## 1. Phạm vi đã hoàn thành

| Hạng mục | File | Trạng thái |
| :--- | :--- | :--- |
| 4 mô hình cây — Q1–Q10 | `tree_models/{adjacency_list,closure_table,nested_set,path_enumeration}/queries_q1_q10.sql` | ✅ Đủ 10/10, khớp đáp án tay |
| 4 mô hình cây — CRUD + di chuyển | `tree_models/*/crud.sql` | ✅ Có chống chu trình, ROLLBACK an toàn |
| Index riêng từng mô hình | `tree_models/*/schema.sql` | ✅ Chỉ tạo INDEX trên bảng dùng chung của TV3 |
| Lược đồ hướng đối tượng | `oo_model/schema.odl` | ✅ 6 lớp, extent, inverse, phương thức |
| Truy vấn OQL | `oo_model/oql_queries.md` | ✅ OQL-1 → OQL-8 (ODMG 3.0) |
| Ánh xạ JPQL + impedance | `oo_model/jpql_mapping.md` | ✅ Bảng OQL/JPQL/SQL + phân tích lệch pha |
| Sơ đồ 6 lớp | `oo_model/class_diagram.drawio` | ✅ XML hợp lệ (6 vertex, 8 cạnh) |
| Script kiểm thử tự động | `tree_models/_validate/` | ✅ `validate.ps1` chạy sạch 4/4 mô hình |

---

## 2. QUY ƯỚC THỐNG NHẤT (đã chốt — 4 mô hình đồng nhất)

- **Subtree / hậu duệ (Q2, Q8):** TÍNH CẢ chính node → `subtree(1) = {1,2,3}`, `count = 3`.
- **Tổ tiên (Q3, Q9, Q10):** KHÔNG tính chính node (nghiêm ngặt) → `ancestors(3) = {1,2}`.
  - Closure: lọc `depth > 0`. · Nested Set: `lft/rgt` bao quanh nghiêm ngặt. ·
    Path Enumeration: `nlevel(path) < nlevel(đích)` hoặc `path <> path_đích`.
- **Độ sâu Q4:** nút gốc `depth = 1`.

---

## 3. ⚠️ THAY ĐỔI QUAN TRỌNG CẦN NHÓM BIẾT

**Sửa lệch tên bảng giữa `schema.sql` (TV2) và schema chung (TV3).**
Trước đây 3 file `tree_models/*/schema.sql` tạo bảng TRÙNG tên khác
(`comment_closure_table`, `comment_nested_set`, `comment_path_demo`) trong khi
các query lại chạy trên bảng của TV3. Nay các file này **chỉ tạo INDEX** trên
đúng bảng dùng chung:

| Mô hình | Bảng dùng chung (TV3) | Index TV2 tạo |
| :--- | :--- | :--- |
| Adjacency List | `comment` | `idx_comment_adj_parent`, `idx_comment_adj_post` |
| Closure Table | `comment_closure` | `idx_closure_ancestor`, `idx_closure_descendant`, `idx_closure_depth` |
| Nested Set | `comment_ns` | `idx_comment_ns_bounds`, `idx_comment_ns_rgt` |
| Path Enumeration | `comment_path` | `idx_comment_path_gist`, `idx_comment_path_btree` |

→ **TV5 lưu ý:** khi đo benchmark, dùng đúng tên bảng này; không còn bảng thừa.

---

## 4. Cách chạy kiểm thử (bàn giao TV5)

```powershell
cd e:\SQL-NangCao\CSDL_Nangcao\tree_models\_validate
powershell -ExecutionPolicy Bypass -File .\validate.ps1
```

Script tạo database riêng `de17_tv2_validation`, không reset/xóa database khác.
Nếu database kiểm thử đã tồn tại, script dừng; chỉ thêm `-ResetDatabase` khi
đồng ý xóa và tạo lại đúng database kiểm thử này. Cấu hình đăng nhập PostgreSQL
bằng `pgpass.conf` hoặc biến môi trường bên ngoài repo, không ghi mật khẩu vào script.

Kết quả mẫu:
```
adjacency_list  queries=OK  crud=OK
closure_table   queries=OK  crud=OK
nested_set      queries=OK  crud=OK
path_enumeration  queries=OK  crud=OK
```

**Thứ tự nạp cho 1 mô hình bất kỳ:**
1. `database/schema.sql` (TV3)
2. `database/seed_test.sql` (TV3)
3. `tree_models/<model>/schema.sql` (TV2 — chỉ index)
4. `tree_models/<model>/queries_q1_q10.sql` (TV2)
5. `tree_models/<model>/crud.sql` (TV2)

---

## 5. Đối chiếu đáp án chuẩn (Ground Truth, đã verify)

| Truy vấn | Kỳ vọng | Cả 4 mô hình |
| :--- | :--- | :--- |
| Q1 cây phân cấp | 1(0)→2(1)→3(2), 4(0) | ✅ |
| Q2 subtree(1) | {1,2,3} | ✅ |
| Q3 ancestors(3) | {1,2} | ✅ |
| Q4 depth 2 | {2} | ✅ |
| Q8 count(1) | 3 | ✅ |
| Q9 breadcrumb(3) | 1→2→3 | ✅ |
| Q10 is_ancestor | (1,3)=T, (4,3)=F | ✅ |
| CRUD move 2→4 | node 4 bao 2 (và 3) | ✅ |
| CRUD move vào hậu duệ | bị từ chối | ✅ |

---

## 6. Ghi chú kỹ thuật theo từng mô hình (điểm bàn luận khi bảo vệ)

- **Adjacency List:** ghi rẻ (1 dòng), đọc cần `WITH RECURSIVE`.
- **Closure Table:** đọc nhanh (1 JOIN), move phải xóa–nối lại nhiều dòng bao đóng.
- **Nested Set:** đọc rất nhanh (`BETWEEN`/công thức `(rgt-lft+1)/2`), ghi đắt
  (dịch lft/rgt). Hàm `ns_move_subtree` rebuild theo pre-order để đảm bảo đúng.
- **Path Enumeration (ltree):** `<@`/`@>` nhanh với GiST; move đổi tiền tố path
  toàn bộ hậu duệ (dùng cắt `text()` tránh lỗi `subpath` "invalid positions").
- **OODBMS (ODL/OQL):** thể hiện điều hướng quan hệ & gọi phương thức (`doSau()`,
  `soBanChung()`) — điểm mà SQL quan hệ phải dùng `JOIN`/`WITH RECURSIVE`; phân
  tích lệch pha trở kháng (impedance mismatch) trong `jpql_mapping.md`.

---

## 7. Việc còn lại (ngoài code TV2)

- [ ] Tạo nhánh `feature/task2-tree-models`, commit + mở PR cho **TV3** review.
- [ ] Xác nhận **TV5** chạy được `_validate/validate.ps1` từ máy sạch và dùng
      đúng tên bảng khi đo `EXPLAIN ANALYZE`.
