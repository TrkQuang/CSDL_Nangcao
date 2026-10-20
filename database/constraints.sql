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
-- Ràng buộc liên bảng: tác giả bài viết phải là thành viên của nhóm
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_check_post_author_membership()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM group_member gm
        WHERE gm.group_id = NEW.group_id
          AND gm.user_id = NEW.author_id
    ) THEN
        RAISE EXCEPTION
            'Tác giả % chưa là thành viên của nhóm %',
            NEW.author_id, NEW.group_id;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_check_post_author_membership ON post;

CREATE TRIGGER trg_check_post_author_membership
BEFORE INSERT OR UPDATE OF group_id, author_id ON post
FOR EACH ROW
EXECUTE FUNCTION fn_check_post_author_membership();

-- Không cho phép xóa hoặc đổi vai trò owner khiến nhóm mất chủ.
CREATE OR REPLACE FUNCTION fn_protect_group_owner()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'DELETE' AND OLD.role = 'owner' THEN
        -- Cho phép ON DELETE CASCADE khi nhóm cha đã bị xóa.
        IF EXISTS (
            SELECT 1
            FROM study_group sg
            WHERE sg.group_id = OLD.group_id
        ) THEN
            RAISE EXCEPTION
                'Không thể xóa owner của nhóm %; chuyển quyền trước',
                OLD.group_id;
        END IF;
    END IF;

    IF TG_OP = 'UPDATE'
       AND OLD.role = 'owner'
       AND (NEW.role <> 'owner'
            OR NEW.user_id <> OLD.user_id
            OR NEW.group_id <> OLD.group_id) THEN
        RAISE EXCEPTION
            'Không thể thay đổi thành viên owner của nhóm %; chuyển quyền trước',
            OLD.group_id;
    END IF;

    IF TG_OP IN ('INSERT', 'UPDATE')
       AND NEW.role = 'owner'
       AND NOT EXISTS (
           SELECT 1
           FROM study_group sg
           WHERE sg.group_id = NEW.group_id
             AND sg.owner_id = NEW.user_id
       ) THEN
        RAISE EXCEPTION
            'Thành viên owner phải trùng owner_id của nhóm %',
            NEW.group_id;
    END IF;

    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_protect_group_owner ON group_member;

CREATE TRIGGER trg_protect_group_owner
BEFORE INSERT OR UPDATE OR DELETE ON group_member
FOR EACH ROW
EXECUTE FUNCTION fn_protect_group_owner();
