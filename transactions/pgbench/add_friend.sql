-- ============================================================================
-- FILE: transactions/pgbench/add_friend.sql
-- MỤC ĐÍCH: Kịch bản thử tải đồng thời bằng công cụ pgbench (PostgreSQL Benchmarking tool).
--           Giả lập nhiều kết nối đồng thời gọi thủ tục proc_add_friend để đo:
--           Thông lượng (TPS), Thời gian đáp ứng (Latency), và Số lỗi Deadlock/Serialization.
-- PHỤ TRÁCH: TV4.
-- ============================================================================

-- Khai báo biến ngẫu nhiên trong pgbench (user id từ 1 đến 100)
\set u1 random(1, 100)
\set u2 random(1, 100)

-- Kiểm tra nếu trùng thì cộng thêm 1
\if :u1 == :u2
    \set u2 :u1 + 1
\endif

BEGIN;

-- Gọi thủ tục kết bạn nguyên tử
CALL proc_add_friend(:u1, :u2);

COMMIT;

-- ----------------------------------------------------------------------------
-- [CÚ PHÁP CHẠY PGBENCH TRÊN TERMINAL]:
-- pgbench -h localhost -p 5432 -U postgres -d detai17_db -c 10 -j 2 -t 100 -f transactions/pgbench/add_friend.sql
-- (-c: số client đồng thời, -t: số transaction mỗi client, -f: file kịch bản)
-- ----------------------------------------------------------------------------
