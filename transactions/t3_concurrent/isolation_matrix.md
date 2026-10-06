# MA TRẬN KIỂM THỬ CÁC MỨC CÔ LẬP TRÊN POSTGRESQL

> **Mục đích file:** Ghi lại kết quả kiểm chứng các hiện tượng bất thường (Dirty Read, Non-repeatable Read, Phantom Read, Serialization Anomaly) trên các mức cô lập của PostgreSQL.  
> **Người phụ trách:** TV4 (Thực nghiệm) & TV3 (Phân tích).

---

## 1. Bảng Khảo Sát Hiện Tượng Bất Thường Trên PostgreSQL

| Mức cô lập | Dirty Read | Non-Repeatable Read | Phantom Read | Serialization Anomaly |
| :--- | :--- | :--- | :--- | :--- |
| **Read Committed** (Mặc định) | Không xảy ra (PostgreSQL không hỗ trợ Read Uncommitted) | **Có xảy ra** | **Có xảy ra** | Có xảy ra |
| **Repeatable Read** | Không | **Không** (PostgreSQL dùng MVCC snapshot) | **Không** (PostgreSQL chặn được Phantom Read ở mức này) | Có thể xảy ra (Write Skew) |
| **Serializable** | Không | Không | Không | **Không** (Phát sinh lỗi mã `40001` khi có xung đột) |

---

## 2. Nhật Ký Quan Sát Lỗi Thực Tế

- **Mã lỗi `40P01`:** Deadlock detected (Phát hiện bế tắc giữa 2 phiên).
- **Mã lỗi `40001`:** Serialization failure (Không thể tuần tự hóa giao dịch do xung đột commit).
- **Mã lỗi `23505`:** Unique violation (Vi phạm ràng buộc duy nhất khi 2 phiên cùng insert khóa giống nhau).
