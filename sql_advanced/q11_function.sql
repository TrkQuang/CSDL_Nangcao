-- ============================================================================
-- FILE: sql_advanced/q11_function.sql
-- MỤC ĐÍCH: Hàm / Thủ tục nâng cao: Di chuyển một nhánh bình luận hoặc thư mục
--           sang một nút cha mới, đồng thời bắt buộc chặn chu trình (Cycle Prevention)
--           bằng cách kiểm tra nút cha mới không được là hậu duệ của chính nó.
-- PHỤ TRÁCH: TV3.
-- ============================================================================

CREATE OR REPLACE PROCEDURE proc_move_comment(
    IN p_node_id INT,
    IN p_new_parent_id INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_is_descendant BOOLEAN;
BEGIN
    -- 1. Nếu chuyển thành nút gốc (parent = NULL) thì luôn hợp lệ
    IF p_new_parent_id IS NULL THEN
        UPDATE comment SET parent_id = NULL WHERE comment_id = p_node_id;
        RETURN;
    END IF;

    -- 2. Không thể tự làm con của chính mình
    IF p_node_id = p_new_parent_id THEN
        RAISE EXCEPTION 'Không thể chuyển nút % làm con của chính nó!', p_node_id;
    END IF;

    -- 3. Dùng WITH RECURSIVE kiểm tra xem p_new_parent_id có đang nằm trong cây con của p_node_id không
    WITH RECURSIVE subtree AS (
        SELECT comment_id FROM comment WHERE comment_id = p_node_id
        UNION ALL
        SELECT c.comment_id FROM comment c JOIN subtree s ON c.parent_id = s.comment_id
    )
    SELECT EXISTS (SELECT 1 FROM subtree WHERE comment_id = p_new_parent_id)
    INTO v_is_descendant;

    IF v_is_descendant THEN
        RAISE EXCEPTION 'Không thể chuyển nhánh: Nút cha mới (%) là hậu duệ của nút di chuyển (%) -> Sẽ tạo chu trình!',
            p_new_parent_id, p_node_id;
    END IF;

    -- 4. Nếu an toàn, thực hiện cập nhật
    UPDATE comment SET parent_id = p_new_parent_id WHERE comment_id = p_node_id;
    RAISE NOTICE 'Đã di chuyển nút % sang cha mới % thành công.', p_node_id, p_new_parent_id;
END;
$$;
