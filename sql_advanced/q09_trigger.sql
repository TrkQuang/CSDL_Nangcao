-- ============================================================================
-- FILE: sql_advanced/q09_trigger.sql
-- MỤC ĐÍCH: Hiện thực Trigger nghiệp vụ (Q9):
--           Đảm bảo bình luận cha và bình luận con phải cùng thuộc về 1 bài viết (BR6).
-- PHỤ TRÁCH: TV3.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU]: Hàm kiểm tra và Trigger gắn vào bảng comment
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_check_comment_parent()
RETURNS TRIGGER AS $$
DECLARE
    v_parent_post_id INT;
BEGIN
    -- Nếu là bình luận gốc (parent_id IS NULL) thì luôn hợp lệ
    IF NEW.parent_id IS NULL THEN
        RETURN NEW;
    END IF;

    -- Lấy post_id của bình luận cha
    SELECT post_id INTO v_parent_post_id
    FROM comment
    WHERE comment_id = NEW.parent_id;

    -- Kiểm tra nếu không tìm thấy cha hoặc cha khác bài viết
    IF v_parent_post_id IS NULL THEN
        RAISE EXCEPTION 'Bình luận cha (id = %) không tồn tại!', NEW.parent_id;
    END IF;

    IF v_parent_post_id <> NEW.post_id THEN
        RAISE EXCEPTION 'Bình luận con (bài %) không thể trả lời bình luận cha (bài %)!',
            NEW.post_id, v_parent_post_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_check_comment_parent ON comment;

CREATE TRIGGER trg_check_comment_parent
BEFORE INSERT OR UPDATE OF parent_id, post_id ON comment
FOR EACH ROW
EXECUTE FUNCTION fn_check_comment_parent();

-- ----------------------------------------------------------------------------
-- [KỊCH BẢN KIỂM THỬ TRIGGER]:
-- Test 1 (Hợp lệ): Thêm bình luận con vào bài 1, cha c1 (cũng bài 1) -> Thành công.
-- Test 2 (Vi phạm): Thêm bình luận vào bài 2 nhưng parent_id = 1 (thuộc bài 1) -> Bị chặn và báo lỗi!
-- ----------------------------------------------------------------------------
