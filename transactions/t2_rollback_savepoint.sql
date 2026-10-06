-- ============================================================================
-- FILE: transactions/t2_rollback_savepoint.sql
-- MỤC ĐÍCH: Kịch bản Giao dịch T2: Xử lý ngoại lệ, ROLLBACK toàn phần và SAVEPOINT cục bộ.
--           Chứng minh CSDL không để lại dữ liệu nửa vời khi có lỗi giữa chừng.
-- PHỤ TRÁCH: TV3.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [KỊCH BẢN 1]: Lỗi giữa chừng dẫn đến ROLLBACK toàn phần
-- ----------------------------------------------------------------------------
BEGIN;

-- Bước 1: Thêm một bài viết mới
INSERT INTO post (post_id, group_id, author_id, post_type, title, content)
VALUES (99, 1, 1, 'thaoluan', 'Bài viết thử nghiệm rollback', 'Nội dung test');

-- Bước 2: Cố tình vi phạm ràng buộc CHECK(user_a < user_b) hoặc vi phạm FK
INSERT INTO friendship (user_a, user_b)
VALUES (5, 2); -- LỖI: vi phạm CHECK (user_a < user_b) vì 5 > 2!

-- Khi bước 2 lỗi, toàn bộ transaction chuyển sang trạng thái ERROR.
-- Lệnh COMMIT sẽ bị từ chối:
-- COMMIT; -- Sẽ fail

-- Phục hồi lại trạng thái trước khi bắt đầu transaction:
ROLLBACK;

-- Kiểm chứng: Bài viết id 99 KHÔNG được lưu trong bảng post:
SELECT * FROM post WHERE post_id = 99; -- Trả về 0 dòng!


-- ----------------------------------------------------------------------------
-- [KỊCH BẢN 2]: Sử dụng Điểm lưu (SAVEPOINT) để phục hồi một phần
-- ----------------------------------------------------------------------------
BEGIN;

INSERT INTO post (post_id, group_id, author_id, post_type, title, content)
VALUES (100, 1, 1, 'thaoluan', 'Bài viết được giữ lại', 'Nội dung hợp lệ');

-- Đặt điểm lưu
SAVEPOINT sp_after_post;

-- Thao tác lỗi sau điểm lưu:
-- INSERT INTO friendship (user_a, user_b) VALUES (5, 2); -- Gây lỗi

-- Quay lui về điểm lưu:
-- ROLLBACK TO SAVEPOINT sp_after_post;

-- Kết thúc và commit phần hợp lệ phía trước:
COMMIT;
