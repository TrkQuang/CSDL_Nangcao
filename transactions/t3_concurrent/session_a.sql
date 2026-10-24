-- ============================================================================
-- FILE: transactions/t3_concurrent/session_a.sql
-- MỤC ĐÍCH: Kịch bản Phiên 1 (Session A) trong thí nghiệm tranh chấp đồng thời gây bế tắc.
--           Chạy song song từng bước (step-by-step) với Session B để kích hoạt lỗi Deadlock (40P01).
-- PHỤ TRÁCH: TV4 (Chương).
-- ============================================================================

-- [BƯỚC A1] Khởi tạo giao dịch
BEGIN;

-- [BƯỚC A2] Khóa độc quyền hàng user_id = 1
-- Hàng 1 bị giữ khóa ExclusiveLock bởi Session A
SELECT user_id, full_name, friend_count 
FROM users 
WHERE user_id = 1 
FOR UPDATE;

-- >>> DỪNG LẠI TẠI ĐÂY!
-- >>> CHUYỂN SANG SESSION B và thực hiện BƯỚC B2 (khóa user_id = 2).

-- [BƯỚC A3] Sau khi Session B đã khóa user_id = 2, Session A thực hiện xin khóa user_id = 2:
-- Lệnh này sẽ bị BLOCK (treo) vì Session B đang nắm giữ khóa user 2!
SELECT user_id, full_name, friend_count 
FROM users 
WHERE user_id = 2 
FOR UPDATE;

-- >>> CHUYỂN TIẾP SANG SESSION B và thực hiện BƯỚC B3 (xin khóa user_id = 1).
-- >>> Sau ~1 giây (deadlock_timeout), 1 trong 2 phiên sẽ bị PostgreSQL ngắt và báo lỗi:
-- >>> ERROR:  deadlock detected (SQLSTATE 40P01)

-- [BƯỚC A4] Kết thúc phiên (COMMIT nếu là phiên sống sót, hoặc ROLLBACK nếu là phiên bị hủy)
COMMIT;
