# BIÊN BẢN HỌP NHÓM (MEETING MINUTES - CLO7)

> **Mục đích file:** Ghi lại tiến độ làm việc, phân công trách nhiệm, thảo luận khó khăn và quyết định kỹ thuật của nhóm qua từng tuần theo chuẩn đầu ra CLO7 (Làm việc nhóm).  
> **Người phụ trách ghi chép:** TV1 (Trưởng nhóm).  
> **Tần suất:** Hàng tuần (khoảng 30 phút/buổi).

---

## Mẫu Biên Bản Họp Tuần [X]

- **Thời gian:** ...  
- **Địa điểm / Hình thức:** Google Meet / Trực tiếp tại thư viện  
- **Thành viên tham dự:** TV1, TV2, TV3, TV4, TV5 (Có mặt đầy đủ / vắng ai)

### 1. Báo Cáo Tiến Độ (Đã Xong Trong Tuần)
| Thành viên | Nhiệm vụ được giao | Trạng thái (Xong / Chưa) | Ghi chú & Link PR/Commit |
| :--- | :--- | :--- | :--- |
| **TV1** | Đặc tả BR1-BR10, vẽ EER sơ bộ | Hoàn thành | PR #1, docs/spec.md |
| **TV2** | Nghiên cứu 4 mô hình cây | Đang làm | tree_models/ |
| **TV3** | Viết DDL schema.sql ban đầu | Hoàn thành | PR #2, database/schema.sql |
| **TV4** | Cài đặt môi trường Neo4j Docker | Hoàn thành | neo4j/ |
| **TV5** | Chuẩn bị dữ liệu kiểm chứng | Đang làm | database/seed_test.sql |

### 2. Thảo Luận Kỹ Thuật & Khó Khăn Phát Sinh
- *Vấn đề 1:* Xử lý quan hệ kết bạn vô hướng trên RDBMS nên dùng 1 dòng hay 2 dòng?
  - *Quyết định:* Chọn lưu 1 dòng có `CHECK (user_a < user_b)` để tiết kiệm dung lượng và tránh bất nhất quán; tạo view `friend_edge` để phục vụ duyệt đồ thị hai chiều.
- *Vấn đề 2:* ...

### 3. Kế Hoạch & Phân Công Cho Tuần Tới
- TV1: Tìm bao đóng, phủ tối tiểu, chuẩn hóa 3NF/BCNF.
- TV2: Hoàn thành DDL và CRUD cho Adjacency List và Path Enumeration.
- TV3: Cài đặt Trigger Q9 và Procedure Q10.
- TV4: Viết script import dữ liệu sang Neo4j.
- TV5: Kiểm thử bộ dữ liệu nhỏ trên 4 mô hình cây.
