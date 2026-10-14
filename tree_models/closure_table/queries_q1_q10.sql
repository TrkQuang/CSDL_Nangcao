-- ============================================================================
-- FILE: tree_models/closure_table/queries_q1_q10.sql
-- MỤC ĐÍCH: Bộ 10 truy vấn chuẩn (Q1-Q10) cho Closure Table dùng phép JOIN đơn giản.
-- PHỤ TRÁCH: TV2 (Kiểm chứng: TV5).
-- YÊU CẦU: database/schema.sql + database/seed_test.sql (TV3), closure_table/schema.sql (TV2).
-- QUY ƯỚC THỐNG NHẤT (khớp 4 mô hình):
--   * Subtree/hậu duệ (Q2, Q8): TÍNH CẢ chính node -> subtree(1)={1,2,3}, count=3.
--   * Tổ tiên (Q3, Q9, Q10): KHÔNG tính chính node (nghiêm ngặt, depth>0) -> ancestors(3)={1,2}.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Q1: Lấy toàn bộ cây bài viết 1 theo thứ tự phân cấp kèm thụt đầu dòng (indent).
--     Độ sâu của node = khoảng cách xa nhất tới một nút GỐC (root).
--     Trong closure: level(node) = MAX(depth) trong các cặp (root, node).
-- ----------------------------------------------------------------------------
WITH RECURSIVE roots AS (
    SELECT comment_id FROM comment WHERE post_id = 1 AND parent_id IS NULL
),
level_of AS (
    SELECT cc.descendant AS comment_id, MAX(cc.depth) AS level
    FROM comment_closure cc
    WHERE cc.ancestor IN (SELECT comment_id FROM roots)
    GROUP BY cc.descendant
)
SELECT c.comment_id,
       c.parent_id,
       repeat('  ', l.level) || c.content AS indented_content,
       l.level
FROM level_of l
JOIN comment c ON c.comment_id = l.comment_id
WHERE c.post_id = 1
ORDER BY c.comment_id;


-- ----------------------------------------------------------------------------
-- Q2: Lấy toàn bộ hậu duệ (subtree) của nút comment_id = 1.
-- Kỳ vọng trên seed_test: {1, 2, 3} (tính cả chính nút 1).
-- ----------------------------------------------------------------------------
SELECT c.comment_id, c.content, cc.depth
FROM comment_closure cc
JOIN comment c ON cc.descendant = c.comment_id
WHERE cc.ancestor = 1
ORDER BY cc.depth;


-- ----------------------------------------------------------------------------
-- Q3: Lấy toàn bộ TỔ TIÊN NGHIÊM NGẶT của nút comment_id = 3 (từ gốc xuống cha trực tiếp).
-- Kỳ vọng trên seed_test: {1, 2} (KHÔNG tính chính nút 3 -> dùng depth > 0).
-- ----------------------------------------------------------------------------
SELECT c.comment_id, c.content, cc.depth
FROM comment_closure cc
JOIN comment c ON cc.ancestor = c.comment_id
WHERE cc.descendant = 3
  AND cc.depth > 0
ORDER BY cc.depth DESC;


-- ----------------------------------------------------------------------------
-- Q4: Lấy các node ở độ sâu k của bài viết 1 (gốc có depth = 1).
--     Trong closure: node đứng ở tầng k nghĩa là MAX(depth) từ root = k - 1.
--     Kỳ vọng với k = 2 trên seed_test: {2}.
-- ----------------------------------------------------------------------------
WITH RECURSIVE roots AS (
    SELECT comment_id FROM comment WHERE post_id = 1 AND parent_id IS NULL
),
level_of AS (
    SELECT cc.descendant AS comment_id, MAX(cc.depth) AS lvl
    FROM comment_closure cc
    WHERE cc.ancestor IN (SELECT comment_id FROM roots)
    GROUP BY cc.descendant
)
SELECT c.comment_id, c.content, l.lvl + 1 AS depth
FROM level_of l
JOIN comment c ON c.comment_id = l.comment_id
WHERE c.post_id = 1
  AND l.lvl + 1 = 2            -- đổi giá trị này để lấy tầng k (gốc = 1)
ORDER BY c.comment_id;


-- ----------------------------------------------------------------------------
-- Q5: Thêm một node mới làm con của node 2, rồi ROLLBACK.
--     Với Closure Table: sao chép MỌI cặp tổ tiên của node cha (2) cho node mới,
--     tăng depth thêm 1, rồi thêm cặp tự thân (new,new,0).
--     LƯU Ý: id mới do sequence sinh ra (có thể nhảy số sau các rollback trước),
--     nên PHẢI dùng RETURNING ... INTO để lấy id thật, KHÔNG hardcode.
-- ----------------------------------------------------------------------------
BEGIN;

DO $$
DECLARE
    v_new_id INT;
BEGIN
    INSERT INTO comment (post_id, parent_id, author_id, content)
    VALUES (1, 2, 2, 'Q5 closure - reply to comment 2')
    RETURNING comment_id INTO v_new_id;

    INSERT INTO comment_closure (ancestor, descendant, depth)
    SELECT ancestor, v_new_id, depth + 1
    FROM comment_closure
    WHERE descendant = 2
    UNION ALL
    SELECT v_new_id, v_new_id, 0;

    RAISE NOTICE 'Đã thêm comment_id = % kèm các cặp bao đóng tương ứng.', v_new_id;
END $$;

-- Kiểm tra: các cặp bao đóng của node vừa thêm (id lớn nhất trong transaction).
SELECT cc.ancestor, cc.descendant, cc.depth, c.content
FROM comment_closure cc
JOIN comment c ON c.comment_id = cc.descendant
WHERE cc.descendant = (SELECT MAX(comment_id) FROM comment)
ORDER BY cc.depth;

ROLLBACK;


-- ----------------------------------------------------------------------------
-- Q6: Xóa node 2 và toàn bộ cây con của nó, rồi ROLLBACK.
--     Xóa cây từ bảng comment gốc; FK ON DELETE CASCADE dọn các cặp Closure
--     tương ứng để bảng chuẩn và cấu trúc phụ không bị lệch nhau.
-- ----------------------------------------------------------------------------
BEGIN;

WITH RECURSIVE subtree(comment_id, post_id) AS (
    SELECT comment_id, post_id FROM comment WHERE comment_id = 2
    UNION
    SELECT c.comment_id, c.post_id
    FROM comment c
    JOIN subtree s ON c.parent_id = s.comment_id
    WHERE c.post_id = s.post_id
)
DELETE FROM comment
WHERE comment_id IN (SELECT comment_id FROM subtree);

SELECT count(*) AS remaining_closure_rows FROM comment_closure;

ROLLBACK;


-- ----------------------------------------------------------------------------
-- Q7: Di chuyển nhánh subtree(2) sang làm con của node 4, rồi ROLLBACK.
--     Closure Table: (1) chặn nếu cha mới (4) nằm trong subtree(2) -> chu trình;
--     (2) xóa liên kết tổ tiên NGHIÊM NGẶT cũ của đầu nhánh 2 trên mọi node con;
--     (3) nối lại với tổ tiên MỚI (gồm chính node 4).
-- ----------------------------------------------------------------------------
BEGIN;

DO $$
DECLARE
    v_node INT := 2;
    v_new_parent INT := 4;
    v_node_post INT;
    v_parent_post INT;
    v_would_cycle BOOLEAN;
BEGIN
    SELECT post_id INTO v_node_post FROM comment WHERE comment_id = v_node;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tìm thấy node cần di chuyển: %', v_node;
    END IF;

    SELECT post_id INTO v_parent_post FROM comment WHERE comment_id = v_new_parent;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tìm thấy cha mới: %', v_new_parent;
    END IF;
    IF v_node_post <> v_parent_post THEN
        RAISE EXCEPTION 'Không thể chuyển nhánh giữa hai bài viết khác nhau';
    END IF;

    -- Chống chu trình: cha mới không được nằm trong subtree của node di chuyển.
    SELECT EXISTS (
        SELECT 1 FROM comment_closure
        WHERE ancestor = v_node AND descendant = v_new_parent
    ) INTO v_would_cycle;

    IF v_would_cycle THEN
        RAISE EXCEPTION 'Không thể chuyển nhánh: cha mới % nằm trong cây con của nút %', v_new_parent, v_node;
    END IF;

    -- (2) Xóa các liên kết TỔ TIÊN NGHIÊM NGẶT cũ (của đầu nhánh 2, depth>0)
    --     trên MỌI node trong subtree(2).
    WITH subtree(descendant) AS (
        SELECT descendant FROM comment_closure WHERE ancestor = v_node
    ),
    old_ancestors(ancestor) AS (
        SELECT ancestor FROM comment_closure WHERE descendant = v_node AND depth > 0
    )
    DELETE FROM comment_closure cc
    USING subtree s
    WHERE cc.descendant = s.descendant
      AND cc.depth > 0
      AND cc.ancestor IN (SELECT ancestor FROM old_ancestors);

    -- (3) Nối lại: mỗi tổ tiên MỚI a của new_parent (gồm cả chính new_parent) với
    --     mỗi node d trong subtree(node), depth = a.depth + 1 + (khoảng cách node->d).
    WITH subtree(node, descendant, node_depth) AS (
        SELECT v_node, descendant, depth
        FROM comment_closure WHERE ancestor = v_node
    ),
    new_ancestors(ancestor, anc_depth) AS (
        SELECT ancestor, depth FROM comment_closure WHERE descendant = v_new_parent
    )
    INSERT INTO comment_closure (ancestor, descendant, depth)
    SELECT na.ancestor, s.descendant, na.anc_depth + 1 + s.node_depth
    FROM new_ancestors na
    CROSS JOIN subtree s
    ON CONFLICT (ancestor, descendant) DO NOTHING;

    -- Đồng bộ parent_id trực tiếp của đầu nhánh trong bảng comment (mô hình gốc).
    UPDATE comment SET parent_id = v_new_parent WHERE comment_id = v_node;
END $$;

SELECT * FROM comment_closure ORDER BY ancestor, descendant;

ROLLBACK;


-- ----------------------------------------------------------------------------
-- Q8: Đếm tổng số node trong cây con của comment_id = 1 (tính cả chính nút 1).
-- Kỳ vọng trên seed_test: 3.
-- ----------------------------------------------------------------------------
SELECT COUNT(*) AS subtree_node_count
FROM comment_closure
WHERE ancestor = 1;


-- ----------------------------------------------------------------------------
-- Q9: Lấy đường đi (breadcrumb) từ node 3 ngược về gốc, trình bày từ gốc -> node.
-- Kỳ vọng trên seed_test: 1 -> 2 -> 3 (gồm chính node 3).
-- ----------------------------------------------------------------------------
SELECT c.comment_id, c.content, cc.depth
FROM comment_closure cc
JOIN comment c ON cc.ancestor = c.comment_id
WHERE cc.descendant = 3
ORDER BY cc.depth DESC;


-- ----------------------------------------------------------------------------
-- Q10: Kiểm tra nhanh A có phải tổ tiên NGHIÊM NGẶT của B hay không.
-- Kỳ vọng: 1 là tổ tiên của 3 (true); 4 không là tổ tiên của 3 (false).
-- ----------------------------------------------------------------------------
WITH cases(ancestor_id, descendant_id) AS (
    VALUES (1, 3), (4, 3)
)
SELECT cases.ancestor_id,
       cases.descendant_id,
       EXISTS (
           SELECT 1
           FROM comment_closure cc
           WHERE cc.ancestor = cases.ancestor_id
             AND cc.descendant = cases.descendant_id
             AND cc.depth > 0          -- nghiêm ngặt: bỏ cặp tự thân
       ) AS is_ancestor
FROM cases
ORDER BY cases.ancestor_id;


-- ----------------------------------------------------------------------------
-- Các câu truy vấn Q1-Q10 cho Closure Table đã được triển khai.
-- ----------------------------------------------------------------------------
