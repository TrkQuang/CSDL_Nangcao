-- ============================================================================
-- FILE: database/constraints.sql
-- MỤC ĐÍCH: Tập trung các ràng buộc toàn vẹn nâng cao (Advanced Constraints),
--           khóa ngoại (FK), CHECK constraints, và các ràng buộc lý thuyết
--           (như CREATE ASSERTION - phân tích cách thay thế bằng Trigger).
-- PHỤ TRÁCH: TV3 (Hỗ trợ: TV1).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU 1]: Ràng buộc kiểm tra vai trò thành viên nhóm
-- ----------------------------------------------------------------------------
ALTER TABLE group_member 
    DROP CONSTRAINT IF EXISTS chk_group_role;

ALTER TABLE group_member 
    ADD CONSTRAINT chk_group_role 
    CHECK (role IN ('owner', 'mod', 'member'));


-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU 2]: Phân tích Ràng buộc phức tạp liên bảng (Inter-table Constraint)
-- Yêu cầu: "Một người chỉ được đăng bài hoặc bình luận vào nhóm mà họ là thành viên".
-- Theo chuẩn SQL: dùng CREATE ASSERTION (tuy nhiên PostgreSQL chưa hỗ trợ cú pháp này).
-- ----------------------------------------------------------------------------
/*
-- Cú pháp lý thuyết:
CREATE ASSERTION assert_author_must_be_member CHECK (
    NOT EXISTS (
        SELECT 1 FROM post p
        WHERE NOT EXISTS (
            SELECT 1 FROM group_member gm 
            WHERE gm.group_id = p.group_id AND gm.user_id = p.author_id
        )
    )
);
*/

-- Giải pháp thay thế thực tế trên PostgreSQL: Dùng TRIGGER hoặc Stored Procedure
-- (Được hiện thực chi tiết trong sql_advanced/q09_trigger.sql)

-- ----------------------------------------------------------------------------
-- [TODO: TV3 bổ sung các ràng buộc khác]
-- - Ràng buộc kiểm tra không tự kết bạn với chính mình
-- - Ràng buộc kiểm tra loại bài viết post_type hợp lệ
-- ----------------------------------------------------------------------------
