-- ============================================================================
-- FILE: tree_models/adjacency_list/crud.sql
-- MỤC ĐÍCH: Ví dụ thêm, xóa và di chuyển bình luận trong Adjacency List.
-- PHỤ TRÁCH: TV2.
-- YÊU CẦU: Chạy database/schema.sql và database/seed_test.sql trước.
-- Các ví dụ đều ROLLBACK để không làm thay đổi dữ liệu kiểm chứng.
-- ============================================================================

-- Thêm một bình luận con cho comment_id = 1.
BEGIN;

INSERT INTO comment (post_id, parent_id, author_id, content)
VALUES (1, 1, 2, 'CRUD test - reply to comment 1')
RETURNING comment_id, post_id, parent_id, author_id, content;

ROLLBACK;


-- Xóa comment_id = 2; ON DELETE CASCADE cũng xóa các hậu duệ của nó.
BEGIN;

DELETE FROM comment
WHERE comment_id = 2
RETURNING comment_id, parent_id, content;

ROLLBACK;


-- Chuyển nhánh comment_id = 2 sang làm con của comment_id = 4.
-- Kiểm tra cùng bài viết và chặn cha mới nằm trong cây con của nút di chuyển.
BEGIN;

DO $$
DECLARE
    v_node_id INT := 2;
    v_new_parent_id INT := 4;
    v_node_post_id INT;
    v_parent_post_id INT;
BEGIN
    SELECT post_id
    INTO v_node_post_id
    FROM comment
    WHERE comment_id = v_node_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tìm thấy bình luận cần di chuyển: %', v_node_id;
    END IF;

    SELECT post_id
    INTO v_parent_post_id
    FROM comment
    WHERE comment_id = v_new_parent_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tìm thấy cha mới: %', v_new_parent_id;
    END IF;

    IF v_node_post_id <> v_parent_post_id THEN
        RAISE EXCEPTION 'Bình luận cha và con phải thuộc cùng một bài viết';
    END IF;

    IF EXISTS (
        WITH RECURSIVE subtree(comment_id) AS (
            SELECT v_node_id

            UNION

            SELECT c.comment_id
            FROM comment c
            JOIN subtree s ON c.parent_id = s.comment_id
        )
        SELECT 1
        FROM subtree
        WHERE comment_id = v_new_parent_id
    ) THEN
        RAISE EXCEPTION
            'Không thể chuyển nhánh: cha mới % nằm trong cây con của nút %',
            v_new_parent_id, v_node_id;
    END IF;

    UPDATE comment
    SET parent_id = v_new_parent_id
    WHERE comment_id = v_node_id;
END;
$$;

SELECT comment_id, parent_id, content
FROM comment
WHERE comment_id IN (1, 2, 3, 4)
ORDER BY comment_id;

ROLLBACK;
