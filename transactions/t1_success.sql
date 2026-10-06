-- ============================================================================
-- FILE: transactions/t1_success.sql
-- MỤC ĐÍCH: Kịch bản Giao dịch T1 (Thành công trọn vẹn):
--           Thực hiện kết bạn giữa 2 người dùng và cập nhật đồng bộ 2 bộ đếm friend_count.
--           Minh chứng tính nguyên tử (Atomicity) và tính nhất quán (Consistency).
-- PHỤ TRÁCH: TV3.
-- ============================================================================

-- Bắt đầu giao dịch
BEGIN;

-- 1. Thêm quan hệ kết bạn giữa User 1 và User 6
INSERT INTO friendship (user_a, user_b, since)
VALUES (1, 6, now());

-- 2. Cập nhật bộ đếm bạn bè của User 1
UPDATE users 
SET friend_count = (SELECT count(*) FROM friend_edge WHERE a = 1) 
WHERE user_id = 1;

-- 3. Cập nhật bộ đếm bạn bè của User 6
UPDATE users 
SET friend_count = (SELECT count(*) FROM friend_edge WHERE a = 6) 
WHERE user_id = 6;

-- Xác nhận lưu vĩnh viễn vào CSDL
COMMIT;

-- ----------------------------------------------------------------------------
-- [KIỂM CHỨNG TÍNH NHẤT QUÁN SAU COMMIT]:
-- Bộ đếm friend_count của user 1 và 6 phải tăng thêm 1 và khớp tuyệt đối số dòng trong friend_edge!
SELECT user_id, full_name, friend_count, 
       (SELECT count(*) FROM friend_edge WHERE a = u.user_id) AS actual_edge_count
FROM users u
WHERE user_id IN (1, 6);
