# Hướng dẫn kiểm thử phần TV2 (tree_models)

> Thư mục `_validate/` chứa script hỗ trợ **tự động** đưa DB về seed gốc và chạy
> kiểm thử toàn bộ 4 mô hình cây. Dùng cho TV5 khi nhận bàn giao benchmark.

## Yêu cầu
- PostgreSQL 18 đã cài (mặc định `C:\Program Files\PostgreSQL\18\bin\psql.exe`).
- PostgreSQL service đang chạy và user `postgres` có quyền tạo database.
- Xác thực bằng `%APPDATA%\postgresql\pgpass.conf` hoặc biến môi trường
  `PGPASSWORD` được thiết lập bên ngoài repository. Không ghi mật khẩu vào script.

## Cách chạy nhanh (Windows)
```powershell
cd E:\SQL-NangCao\CSDL_Nangcao\tree_models\_validate
powershell -ExecutionPolicy Bypass -File .\validate.ps1
```
Mặc định script tạo database riêng `de17_tv2_validation`; nếu database đã tồn tại,
script sẽ dừng và không xóa dữ liệu. Chỉ dùng `-ResetDatabase` khi bạn đồng ý xóa
và tạo lại đúng database validation đó:

```powershell
powershell -ExecutionPolicy Bypass -File .\validate.ps1 -ResetDatabase
```

`validate.ps1` nạp schema và seed dùng chung, tạo index bốn mô hình, sau đó chạy
Q1–Q10 và CRUD của từng mô hình với `ON_ERROR_STOP`. Khi một lệnh lỗi, script
dừng và báo lỗi; kết quả lệnh chạy được ghi vào `validation_result.txt`.
Database validation được giữ lại để có thể kiểm tra thủ công.

## Đối chiếu đáp án chuẩn (Ground Truth)
Sau khi chạy, đối chiếu tay các kết quả sau (các phép thử có thay đổi dữ liệu đều
được rollback):

| Truy vấn | Đáp án đúng (bài 1: c1→c2→c3, gốc c4) |
| :--- | :--- |
| Q1 cây phân cấp | 1(level0) → 2(level1) → 3(level2), 4(level0) |
| Q2 subtree(1) | {1, 2, 3} (tính cả nút 1) |
| Q3 ancestors(3) | {1, 2} (KHÔNG tính nút 3) |
| Q4 depth 2 | {2} |
| Q8 count(1) | 3 |
| Q9 breadcrumb(3) | 1 → 2 → 3 |
| Q10 is_ancestor | (1,3)=true ; (4,3)=false |
| CRUD move 2→4 | node 4 bao node 2 (và 3) |
| CRUD move vào hậu duệ | bị TỪ CHỐI (PASS) |

## Script
- `validate.ps1` — chạy toàn bộ (khuyến nghị).
- `reset_db.ps1` — reset riêng database validation; bắt buộc xác nhận rõ:
  `powershell -ExecutionPolicy Bypass -File .\reset_db.ps1 -ConfirmReset`.
