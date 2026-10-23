# CHECKLIST KIỂM TRA & NGHIỆM THU NHIỆM VỤ THÀNH VIÊN 4 (CHƯƠNG)

> **Phụ trách:** CSDL Đồ thị Neo4j/Cypher, Thử tải đồng thời pgbench & Tương tranh Deadlock (T3)  
> **Repository:** `CSDL_Nangcao` | Đồ án 17 - CSDL Nâng cao

---

## BẢNG TIẾN ĐỘ THỰC HIỆN CHI TIẾT

| Hạng mục công việc | Trạng thái | Bằng chứng thực tế & File lưu trữ |
| :--- | :---: | :--- |
| **1. CSDL Đồ thị Neo4j & Cypher** | | |
| • Viết script nạp 6 nodes và cạnh quan hệ | ✅ **Hoàn thành** | [`neo4j/import/import_nodes_edges.cypher`](file:///d:/CSDL_Nangcao/neo4j/import/import_nodes_edges.cypher) |
| • Viết câu truy vấn Cypher đối chiếu R1 – R4 | ✅ **Hoàn thành** | [`neo4j/cypher/`](file:///d:/CSDL_Nangcao/neo4j/cypher/) (FoF, Shortest Path, Cycle, Recommendation) |
| • Đối chiếu kết quả Cypher với PostgreSQL | ✅ **Hoàn thành** | Khớp 100% với `recursive_sql/` (R1: {Dung, Em}, R2: [1,3,5], R3: 3 chu trình) |
| • Hướng dẫn chạy và mẫu lệnh chụp Neo4j Browser | ✅ **Hoàn thành** | [`neo4j/screenshots/README.md`](file:///d:/CSDL_Nangcao/neo4j/screenshots/README.md) |
| • Chụp 4 ảnh trực tiếp từ Neo4j Browser | ✅ **Hoàn thành** | Đã lưu đủ 4 ảnh trực tiếp từ Browser vào [`neo4j/screenshots/01..04_neo4j_*.png`](file:///d:/CSDL_Nangcao/neo4j/screenshots/) |
| | | |
| **2. Tương Tranh & Kích Hoạt Deadlock (T3)** | | |
| • Soạn thảo 2 phiên đối kháng Session A & B | ✅ **Hoàn thành** | [`session_a.sql`](file:///d:/CSDL_Nangcao/transactions/t3_concurrent/session_a.sql), [`session_b.sql`](file:///d:/CSDL_Nangcao/transactions/t3_concurrent/session_b.sql) |
| • Tái hiện thực tế Deadlock và lưu log nguyên bản | ✅ **Hoàn thành** | [`logs/deadlock_t3_log.txt`](file:///d:/CSDL_Nangcao/transactions/t3_concurrent/logs/deadlock_t3_log.txt) *(PID 16484, SQLSTATE `40P01`)* |
| • Kiểm chứng thực nghiệm 3 mức cô lập giao dịch | ✅ **Hoàn thành** | [`logs/isolation_experiments_log.txt`](file:///d:/CSDL_Nangcao/transactions/t3_concurrent/logs/isolation_experiments_log.txt) *(Non-Repeatable, Snapshot, SSI 40001)* |
| • Cập nhật ma trận và nhật ký thực tế | ✅ **Hoàn thành** | [`isolation_matrix.md`](file:///d:/CSDL_Nangcao/transactions/t3_concurrent/isolation_matrix.md) |
| | | |
| **3. Thử Tải Đồng Thời Bằng pgbench** | | |
| • Kịch bản pgbench gọi Stored Procedure an toàn | ✅ **Hoàn thành** | [`transactions/pgbench/add_friend.sql`](file:///d:/CSDL_Nangcao/transactions/pgbench/add_friend.sql) |
| • Script tự động chạy pgbench trên Windows | ✅ **Hoàn thành** | [`run_pgbench.ps1`](file:///d:/CSDL_Nangcao/run_pgbench.ps1) |
| • Chạy và lưu log gốc cho 5 kết nối (5 clients) | ✅ **Hoàn thành** | [`logs/pgbench_5_clients.txt`](file:///d:/CSDL_Nangcao/transactions/pgbench/logs/pgbench_5_clients.txt) *(3,452 TPS, Latency 1.45ms)* |
| • Chạy và lưu log gốc cho 10 kết nối (10 clients)| ✅ **Hoàn thành** | [`logs/pgbench_10_clients.txt`](file:///d:/CSDL_Nangcao/transactions/pgbench/logs/pgbench_10_clients.txt) *(4,555 TPS, Latency 2.19ms)* |
| • Chạy và lưu log gốc cho 20 kết nối (20 clients)| ✅ **Hoàn thành** | [`logs/pgbench_20_clients.txt`](file:///d:/CSDL_Nangcao/transactions/pgbench/logs/pgbench_20_clients.txt) *(2,617 TPS, Latency 7.64ms)* |
| • Báo cáo kết quả thử tải có nhãn ĐÃ KIỂM TRA | ✅ **Hoàn thành** | [`transactions/pgbench/results.md`](file:///d:/CSDL_Nangcao/transactions/pgbench/results.md) |

---

## TỔNG KẾT NGHIỆM THU:
🎉 **CHÚC MỪNG: BẠN ĐÃ HOÀN THÀNH 100% TẤT CẢ CÁC HẠNG MỤC CỦA TASK 4!**
1. Đồ thị Neo4j/Cypher: Toàn bộ script nạp, truy vấn R1–R4 và 4 ảnh chụp trực quan từ Neo4j Browser đã sẵn sàng.
2. Kiểm thử tương tranh Deadlock (T3): Script 2 phiên, log lỗi 40P01 thực tế và ma trận mức cô lập đầy đủ.
3. Thử tải đồng thời pgbench: Script chạy tự động, log gốc 3 mức tải và báo cáo phân tích chi tiết hoàn chỉnh.
4. Bước cuối cùng: Commit toàn bộ repo lên GitHub nhóm!

