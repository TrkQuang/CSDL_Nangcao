
-- Khai báo ngẫu nhiên 2 user_id phân biệt trong khoảng [1, 6] (seed_test.sql)
\set u1 random(1, 6)
\set delta random(1, 5)
\set u2 (:u1 + :delta - 1) % 6 + 1

-- Thực thi khối giao dịch gọi Stored Procedure kết bạn nguyên tử
BEGIN;
CALL proc_add_friend(:u1, :u2);
COMMIT;
