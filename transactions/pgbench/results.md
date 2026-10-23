# BÁO CÁO KẾT QUẢ THỬ TẢI ĐỒNG THỜI BẰNG PGBENCH (KẾT QUẢ ĐÃ KIỂM TRA)

> **Mục đích:** Đo lường thông lượng (TPS) và độ trễ (Latency) của thủ tục lưu trữ kết bạn nguyên tử (`proc_add_friend`) dưới các mức tải đồng thời 5, 10, 20 clients.  
> **Trạng thái:** **ĐÃ KIỂM TRA & LƯU LOG GỐC** (Verified from actual test run).  
> **Người phụ trách:** TV4 (Chương) | Repository: `CSDL_Nangcao`.

---

## 1. Cấu Hình Máy Kiểm Thử & Tham Số Môi Trường

- **Hệ điều hành:** Windows 11 x64
- **Hệ quản trị CSDL:** PostgreSQL 16.15 (64-bit)
- **Database kiểm thử:** `detai17_db` (bộ dữ liệu `seed_test.sql`)
- **Kịch bản pgbench:** [add_friend.sql](file:///d:/CSDL_Nangcao/transactions/pgbench/add_friend.sql)
- **Mức cô lập:** `READ COMMITTED` (mặc định của PostgreSQL)
- **Số giao dịch mỗi client (`-t`):** 100 transactions/client
- **Quy mô kết nối đồng thời (`-c`):** 5, 10, 20 clients
- **Số luồng worker (`-j`):** 2 threads

---

## 2. Bảng Tổng Hợp Kết Quả Đo Đạc Thực Tế

| Số kết nối đồng thời (`-c`) | Tổng số Transaction (`-c * -t`) | Số Transaction thành công | Tỷ lệ thất bại / Deadlock | Độ trễ trung bình *(Latency)* | Thông lượng *(TPS excluding connections)* | File log gốc lưu trữ |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **5 clients** | 500 | 500 / 500 | **0.000%** (0 lỗi) | **1.448 ms** | **3,452.90 TPS** | [pgbench_5_clients.txt](file:///d:/CSDL_Nangcao/transactions/pgbench/logs/pgbench_5_clients.txt) |
| **10 clients** | 1,000 | 1,000 / 1,000 | **0.000%** (0 lỗi) | **2.195 ms** | **4,555.68 TPS** | [pgbench_10_clients.txt](file:///d:/CSDL_Nangcao/transactions/pgbench/logs/pgbench_10_clients.txt) |
| **20 clients** | 2,000 | 2,000 / 2,000 | **0.000%** (0 lỗi) | **7.641 ms** | **2,617.57 TPS** | [pgbench_20_clients.txt](file:///d:/CSDL_Nangcao/transactions/pgbench/logs/pgbench_20_clients.txt) |

---

## 3. Trích Xuất Đầu Ra Nguyên Bản Từ Các File Log

### 3.1. Mức tải 5 clients (Trích từ `transactions/pgbench/logs/pgbench_5_clients.txt`)
```text
transaction type: transactions\pgbench\add_friend.sql
scaling factor: 1
query mode: simple
number of clients: 5
number of threads: 2
maximum number of tries: 1
number of transactions per client: 100
number of transactions actually processed: 500/500
number of failed transactions: 0 (0.000%)
latency average = 1.448 ms
initial connection time = 134.474 ms
tps = 3452.895598 (without initial connection time)
```

### 3.2. Mức tải 10 clients (Trích từ `transactions/pgbench/logs/pgbench_10_clients.txt`)
```text
transaction type: transactions\pgbench\add_friend.sql
scaling factor: 1
query mode: simple
number of clients: 10
number of threads: 2
maximum number of tries: 1
number of transactions per client: 100
number of transactions actually processed: 1000/1000
number of failed transactions: 0 (0.000%)
latency average = 2.195 ms
initial connection time = 228.701 ms
tps = 4555.684127 (without initial connection time)
```

### 3.3. Mức tải 20 clients (Trích từ `transactions/pgbench/logs/pgbench_20_clients.txt`)
```text
transaction type: transactions\pgbench\add_friend.sql
scaling factor: 1
query mode: simple
number of clients: 20
number of threads: 2
maximum number of tries: 1
number of transactions per client: 100
number of transactions actually processed: 2000/2000
number of failed transactions: 0 (0.000%)
latency average = 7.641 ms
initial connection time = 624.824 ms
tps = 2617.568070 (without initial connection time)
```

---

## 4. Phân Tích Kỹ Thuật

1. **Hiệu năng & Khả năng mở rộng:**
   - Khi tăng từ 5 lên 10 clients, TPS tăng từ **3,452 TPS** lên **4,555 TPS** do hệ thống tận dụng tối đa 2 luồng worker và bộ nhớ đệm shared buffers.
   - Khi tăng tiếp lên 20 clients, TPS đạt **2,617 TPS** và độ trễ tăng lên **7.641 ms**. Đây là đặc trưng tự nhiên của tranh chấp khóa hàng (Row-level Lock Contention) khi nhiều kết nối cùng gọi câu lệnh `UPDATE users SET friend_count = ...` trên số ít 6 người dùng.
2. **Triệt tiêu hoàn toàn rủi ro Deadlock:**
   - Ở cả 3 mức tải, tỷ lệ giao dịch thất bại duy trì tuyệt đối ở mức **0.000%**.
   - Điều này chứng minh thuật toán quy chuẩn thứ tự khóa `v_a := LEAST(p_user1, p_user2)` và `v_b := GREATEST(p_user1, p_user2)` trong Stored Procedure `proc_add_friend` đã triệt tiêu hoàn toàn chu trình bế tắc trong đồ thị WFG.
