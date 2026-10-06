-- ============================================================================
-- FILE: transactions/t3_concurrent/session_b.sql
-- MỤC ĐÍCH: Kịch bản Phiên 2 (Session B) chạy đối kháng với Session A.
-- PHỤ TRÁCH: TV4.
-- ============================================================================

-- BƯỚC B1: Bắt đầu giao dịch cùng mức cô lập
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- BƯỚC B2: Khóa hàng user 2 (ngược thứ tự với Session A)
SELECT * FROM users WHERE user_id = 2 FOR UPDATE;

-- (Chờ Session A thực hiện Bước A3)

-- BƯỚC B3: Cố gắng khóa hàng user 1 -> Tạo chu trình chờ khóa (Deadlock)!
SELECT * FROM users WHERE user_id = 1 FOR UPDATE;

-- Kết thúc: Một trong 2 phiên sẽ nhận thông báo:
-- ERROR: deadlock detected
-- DETAIL: Process X waits for ExclusiveLock on tuple ...
COMMIT;
