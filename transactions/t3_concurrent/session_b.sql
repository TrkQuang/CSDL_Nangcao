
BEGIN;

-- >>> CHỜ Session A thực hiện xong BƯỚC A2 (khóa user_id = 1).

-- [BƯỚC B2] Khóa độc quyền hàng user_id = 2 (ngược thứ tự với Session A)
-- Hàng 2 bị giữ khóa ExclusiveLock bởi Session B
SELECT user_id, full_name, friend_count 
FROM users 
WHERE user_id = 2 
FOR UPDATE;

-- >>> CHUYỂN VỀ SESSION A và thực hiện BƯỚC A3 (Session A sẽ bị BLOCK chờ user 2).

-- [BƯỚC B3] Trong khi Session A đang bị treo chờ user 2, Session B thực hiện xin khóa user_id = 1:
-- Session B cần khóa user 1 (Session A đang giữ), Session A cần khóa user 2 (Session B đang giữ)
-- -> Tạo chu trình bế tắc trong Wait-For Graph (WFG): Session A -> Session B -> Session A
SELECT user_id, full_name, friend_count 
FROM users 
WHERE user_id = 1 
FOR UPDATE;

-- >>> KẾT QUẢ: PostgreSQL kích hoạt Deadlock Detector và hủy phiên này (hoặc phiên A):
-- ERROR:  deadlock detected
-- DETAIL: Process X waits for ExclusiveLock on tuple ... blocked by Process Y.
--         Process Y waits for ExclusiveLock on tuple ... blocked by Process X.
-- HINT:   See server log for query details.
-- CONTEXT: while locking tuple (0,1) in relation "users"

-- [BƯỚC B4] Xử lý sau khi bị ngắt
ROLLBACK;