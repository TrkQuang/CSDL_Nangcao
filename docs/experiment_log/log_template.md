# NHẬT KÝ THỰC NGHIỆM (EXPERIMENT LOG)

> **Mục đích file:** Ghi chép chi tiết từng lần chạy đo đạc benchmark hoặc kiểm thử giao dịch concurrency/deadlock. Đảm bảo tính khoa học, khách quan và khả năng tái lập kết quả (reproducibility).  
> **Người phụ trách:** TV5 (Benchmark) & TV4 (Transaction/Concurrency).  
> **Quy tắc:** Mỗi lần đo ghi 1 bản ghi; chạy 1 lần làm nóng (warm-up) rồi đo 5–10 lần lấy giá trị trung vị (median).

---

## 1. Thông Tin Môi Trường Thử Nghiệm

- **Phần cứng:** CPU Intel Core i... / AMD Ryzen..., RAM ... GB, Ổ cứng SSD NVMe ...
- **Hệ điều hành:** Windows 11 / Ubuntu 22.04 LTS
- **Hệ quản trị CSDL:** PostgreSQL 16.x (shared_buffers = ..., work_mem = ...) / Neo4j 5.x Community
- **Công cụ đo:** `EXPLAIN (ANALYZE, BUFFERS)` / Python `time.perf_counter()` / `pgbench`

---

## 2. Bảng Nhật Ký Thực Nghiệm

| Mã TN | Ngày đo | Đối tượng đo | Kích thước dữ liệu | Chỉ mục sử dụng | Thời gian (ms) | Bộ đệm (Buffers Hit/Read) | Ghi chú & Nhận xét |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EXP-01** | 2026-10-15 | Q2: Lấy hậu duệ (Adjacency List) | 1.000 nodes, depth=6 | B-tree (parent_id) | 1.25 ms | Hit: 120, Read: 0 | Dùng WITH RECURSIVE, plan: CTE Scan |
| **EXP-02** | 2026-10-15 | Q2: Lấy hậu duệ (Nested Set) | 1.000 nodes, depth=6 | Composite (post_id, lft, rgt) | 0.35 ms | Hit: 15, Read: 0 | Dùng BETWEEN, plan: Index Only Scan |
| **EXP-03** | ... | ... | ... | ... | ... | ... | ... |

---

## 3. Mẫu Khai Báo Chi Tiết Cho Một Thí Nghiệm
```markdown
### Thí nghiệm: [Mã TN - Ví dụ: EXP-CONCUR-01]
- **Mục tiêu:** Đo lường xung đột và deadlock khi 2 giao dịch đồng thời gửi yêu cầu kết bạn chéo nhau.
- **Mức cô lập:** Read Committed vs Serializable.
- **Kịch bản:** Phiên 1 (An kết bạn Binh), Phiên 2 (Binh kết bạn An) cùng lúc.
- **Kết quả quan sát:** 
  - Read Committed: Một phiên bị chặn (RowShareLock), sau khi commit phát sinh UniqueViolation (23505).
  - Serializable: Phát sinh Serialization Failure (40001).
- **Kết luận:** Cần cơ chế khóa có thứ tự (FOR UPDATE sắp xếp theo user_id) hoặc bắt mã lỗi 40001 để retry.
```
