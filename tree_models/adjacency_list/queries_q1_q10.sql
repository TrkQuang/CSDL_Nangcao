-- ============================================================================
-- FILE: tree_models/adjacency_list/queries_q1_q10.sql
-- MỤC ĐÍCH: Bộ 10 truy vấn chuẩn (Q1-Q10) cho mô hình Adjacency List dùng WITH RECURSIVE.
-- PHỤ TRÁCH: TV2 (Kiểm chứng kết quả khớp seed_test: TV5).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU Q1]: Lấy toàn bộ cây theo thứ tự phân cấp kèm thụt đầu dòng (indent)
-- ----------------------------------------------------------------------------
WITH RECURSIVE comment_tree AS (
    -- Điểm neo: Lấy các nút gốc (parent_id IS NULL)
    SELECT 
        comment_id, parent_id, content, 
        0 AS level, 
        ARRAY[comment_id] AS path_sort
    FROM comment
    WHERE post_id = 1 AND parent_id IS NULL

    UNION ALL

    -- Bước đệ quy: Tìm con trực tiếp
    SELECT 
        c.comment_id, c.parent_id, c.content, 
        ct.level + 1, 
        ct.path_sort || c.comment_id
    FROM comment c
    JOIN comment_tree ct ON c.parent_id = ct.comment_id
)
SELECT 
    comment_id,
    parent_id,
    repeat('  ', level) || content AS indented_content,
    level
FROM comment_tree
ORDER BY path_sort;


-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU Q2]: Lấy toàn bộ hậu duệ (subtree) của nút comment_id = 1
-- Kỳ vọng trên seed_test: {c1, c2, c3}
-- ----------------------------------------------------------------------------
WITH RECURSIVE subtree AS (
    SELECT comment_id, parent_id, content, 1 AS depth
    FROM comment
    WHERE comment_id = 1

    UNION ALL

    SELECT c.comment_id, c.parent_id, c.content, s.depth + 1
    FROM comment c
    JOIN subtree s ON c.parent_id = s.comment_id
)
SELECT * FROM subtree;


-- ----------------------------------------------------------------------------
-- Q3: Lấy toàn bộ tổ tiên của nút comment_id = 3 (từ gốc xuống cha trực tiếp)
-- Kỳ vọng trên seed_test: c1, c2
-- ----------------------------------------------------------------------------
WITH RECURSIVE ancestors AS (
    -- Bắt đầu từ cha trực tiếp của nút cần tìm; không tính chính nút đó
    SELECT p.comment_id, p.parent_id, p.content, 1 AS distance
    FROM comment target
    JOIN comment p ON p.comment_id = target.parent_id
    WHERE target.comment_id = 3

    UNION ALL

    -- Tiếp tục đi ngược lên cha của mỗi tổ tiên
    SELECT p.comment_id, p.parent_id, p.content, a.distance + 1
    FROM comment p
    JOIN ancestors a ON p.comment_id = a.parent_id
)
SELECT comment_id, parent_id, content
FROM ancestors
ORDER BY distance DESC;


-- ----------------------------------------------------------------------------
-- Q4: Lấy các nút ở độ sâu 2 của bài viết 1 (nút gốc có depth = 1)
-- Kỳ vọng trên seed_test: c2
-- ----------------------------------------------------------------------------
WITH RECURSIVE comment_tree AS (
    SELECT comment_id, post_id, parent_id, content, 1 AS depth,
           ARRAY[comment_id] AS visited
    FROM comment
    WHERE post_id = 1
      AND parent_id IS NULL

    UNION ALL

    SELECT c.comment_id, c.post_id, c.parent_id, c.content,
           tree.depth + 1,
           tree.visited || c.comment_id
    FROM comment c
    JOIN comment_tree tree
      ON c.parent_id = tree.comment_id
     AND c.post_id = tree.post_id
    WHERE NOT c.comment_id = ANY(tree.visited)
)
SELECT comment_id, parent_id, content, depth
FROM comment_tree
WHERE depth = 2
ORDER BY comment_id;


-- ----------------------------------------------------------------------------
-- Q5: Thử thêm một bình luận con cho comment_id = 2
-- RETURNING hiển thị dòng vừa thêm; ROLLBACK giữ nguyên seed_test sau khi thử.
-- ----------------------------------------------------------------------------
BEGIN;

INSERT INTO comment (post_id, parent_id, author_id, content)
VALUES (1, 2, 2, 'Q5 test - reply to comment 2')
RETURNING comment_id, post_id, parent_id, author_id, content;

ROLLBACK;


-- ----------------------------------------------------------------------------
-- Q6: Thử xóa comment_id = 2 và các hậu duệ
-- ON DELETE CASCADE xóa comment_id = 3; ROLLBACK khôi phục seed_test.
-- ----------------------------------------------------------------------------
BEGIN;

DELETE FROM comment
WHERE comment_id = 2
RETURNING comment_id, parent_id, content;

SELECT comment_id, parent_id, content
FROM comment
WHERE comment_id IN (2, 3)
ORDER BY comment_id;

ROLLBACK;


-- ----------------------------------------------------------------------------
-- Q7: Thử chuyển nhánh comment_id = 2 sang làm con của comment_id = 4
-- Chặn chính nó/hậu duệ làm cha mới và yêu cầu cả hai nút cùng bài viết.
-- ROLLBACK khôi phục quan hệ cha ban đầu sau khi kiểm tra.
-- ----------------------------------------------------------------------------
BEGIN;

DO $$
DECLARE
    v_node_id INT := 2;
    v_new_parent_id INT := 4;
    v_node_post_id INT;
    v_parent_post_id INT;
    v_would_create_cycle BOOLEAN;
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

    WITH RECURSIVE subtree AS (
        SELECT comment_id
        FROM comment
        WHERE comment_id = v_node_id

        UNION

        SELECT c.comment_id
        FROM comment c
        JOIN subtree s ON c.parent_id = s.comment_id
    )
    SELECT EXISTS (
        SELECT 1
        FROM subtree
        WHERE comment_id = v_new_parent_id
    )
    INTO v_would_create_cycle;

    IF v_would_create_cycle THEN
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

-- Với nhánh bắt đầu ở 2, chuyển xuống 3 sẽ tạo chu trình nên phải bị từ chối.
WITH RECURSIVE subtree AS (
    SELECT comment_id
    FROM comment
    WHERE comment_id = 2

    UNION

    SELECT c.comment_id
    FROM comment c
    JOIN subtree s ON c.parent_id = s.comment_id
)
SELECT EXISTS (
    SELECT 1
    FROM subtree
    WHERE comment_id = 3
) AS moving_under_3_would_create_cycle;

ROLLBACK;


-- ----------------------------------------------------------------------------
-- Q8: Đếm số nút trong cây con của comment_id = 1 (tính cả chính nút 1)
-- Kỳ vọng trên seed_test: 3 (các nút 1, 2, 3)
-- ----------------------------------------------------------------------------
WITH RECURSIVE subtree AS (
    SELECT comment_id
    FROM comment
    WHERE comment_id = 1

    UNION

    SELECT c.comment_id
    FROM comment c
    JOIN subtree s ON c.parent_id = s.comment_id
)
SELECT COUNT(*) AS subtree_node_count
FROM subtree;


-- ----------------------------------------------------------------------------
-- Q9: Lấy đường đi từ gốc đến comment_id = 3 (Breadcrumb)
-- Kỳ vọng trên seed_test: 1 -> 2 -> 3
-- ----------------------------------------------------------------------------
WITH RECURSIVE breadcrumb AS (
    SELECT comment_id, parent_id, content, 0 AS distance,
           ARRAY[comment_id] AS visited
    FROM comment
    WHERE comment_id = 3

    UNION ALL

    SELECT parent.comment_id, parent.parent_id, parent.content,
           breadcrumb.distance + 1,
           breadcrumb.visited || parent.comment_id
    FROM comment parent
    JOIN breadcrumb ON parent.comment_id = breadcrumb.parent_id
    WHERE NOT parent.comment_id = ANY(breadcrumb.visited)
)
SELECT comment_id, content
FROM breadcrumb
ORDER BY distance DESC;


-- ----------------------------------------------------------------------------
-- Q10: Kiểm tra tổ tiên nghiêm ngặt cho hai cặp nút
-- Kỳ vọng: 1 là tổ tiên của 3 (true); 4 không là tổ tiên của 3 (false).
-- ----------------------------------------------------------------------------
WITH RECURSIVE cases(ancestor_id, descendant_id) AS (
    VALUES (1, 3), (4, 3)
),
ancestors(ancestor_id, descendant_id, current_ancestor_id) AS (
    SELECT cases.ancestor_id, cases.descendant_id, child.parent_id
    FROM cases
    JOIN comment child ON child.comment_id = cases.descendant_id
    WHERE child.parent_id IS NOT NULL

    UNION

    SELECT ancestors.ancestor_id,
           ancestors.descendant_id,
           parent.parent_id
    FROM ancestors
    JOIN comment parent ON parent.comment_id = ancestors.current_ancestor_id
    WHERE parent.parent_id IS NOT NULL
)
SELECT cases.ancestor_id,
       cases.descendant_id,
       EXISTS (
           SELECT 1
           FROM ancestors
           WHERE ancestors.ancestor_id = cases.ancestor_id
             AND ancestors.descendant_id = cases.descendant_id
             AND ancestors.current_ancestor_id = cases.ancestor_id
       ) AS is_ancestor
FROM cases
ORDER BY cases.ancestor_id;


-- ----------------------------------------------------------------------------
-- Các câu truy vấn Q1-Q10 cho Adjacency List đã được triển khai.
-- ----------------------------------------------------------------------------
