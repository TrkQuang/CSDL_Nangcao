-- ============================================================================
-- FILE: transactions/t3_concurrent/session_a.sql
-- MỤC ĐÍCH: Kịch bản Phiên 1 (Session A) trong thí nghiệm cạnh tranh đồng thời.
--           Chạy song song từng bước với Session B để quan sát Lock và Deadlock.
-- PHỤ TRÁCH: TV4 (Chạy thực nghiệm) & TV3 (Duyệt kịch bản).
-- ============================================================================

-- BƯỚC A1: Bắt đầu giao dịch với mức cô lập Read Committed (hoặc Serializable)
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- BƯỚC A2: Khóa hàng user 1 để cập nhật
SELECT * FROM users WHERE user_id = 1 FOR UPDATE;

-- (Chờ Session B thực hiện Bước B2 khóa user 2)

-- BƯỚC A3: Cố gắng khóa hàng user 2 (sẽ bị BLOCK nếu Session B đang giữ khóa user 2!)
SELECT * FROM users WHERE user_id = 2 FOR UPDATE;

-- BƯỚC A4: Khi xuất hiện Deadlock, PostgreSQL sẽ hủy 1 trong 2 phiên với mã lỗi 40P01
COMMIT;
