-- ============================================================================
-- FILE: tree_models/path_enumeration/queries_q1_q10.sql
-- MỤC ĐÍCH: Bộ 10 truy vấn chuẩn (Q1-Q10) cho mô hình Path Enumeration (ltree).
-- PHỤ TRÁCH: TV2 (Kiểm chứng kết quả: TV5).
-- YÊU CẦU: database/schema.sql + database/seed_test.sql (TV3), path_enumeration/schema.sql (TV2).
-- QUY ƯỚC THỐNG NHẤT (khớp 4 mô hình):
--   * Subtree/hậu duệ (Q2, Q8): TÍNH CẢ chính node -> subtree(1)={1,2,3}, count=3.
--   * Tổ tiên (Q3, Q9, Q10): KHÔNG tính chính node (nghiêm ngặt) -> ancestors(3)={1,2}.
--   Lưu ý ltree: toán tử <@ và @> MẶC ĐỊNH tính cả node bằng chính nó, nên khi
--   cần tổ tiên/hậu duệ NGHIÊM NGẶT phải loại trừ thêm (dùng nlevel hoặc <> path).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Q1: Lấy toàn bộ cây bài viết 1 theo thứ tự phân cấp kèm thụt đầu dòng (indent).
--     Nguyên lý: ORDER BY path cho đúng thứ tự tiền tự; độ sâu = nlevel(path) - 1.
--     (nlevel đếm số nhãn trên đường đi, gốc '1' có nlevel = 1 -> level = 0.)
-- ----------------------------------------------------------------------------
SELECT cp.comment_id,
       c.content,
       repeat('  ', nlevel(cp.path) - 1) || c.content AS indented_content,
       nlevel(cp.path) - 1 AS level
FROM comment_path cp
JOIN comment c ON c.comment_id = cp.comment_id
WHERE cp.post_id = 1
ORDER BY cp.path;


-- ----------------------------------------------------------------------------
-- Q2: Lấy toàn bộ hậu duệ (subtree) của nút comment_id = 1 (path = '1').
-- Toán tử <@ : path IS DESCENDANT OF '1' (tính cả chính '1').
-- Kỳ vọng trên seed_test: {1, 2, 3}.
-- ----------------------------------------------------------------------------
SELECT c.comment_id, c.content, cp.path
FROM comment_path cp
JOIN comment c ON cp.comment_id = c.comment_id
WHERE cp.path <@ '1'
ORDER BY cp.path;


-- ----------------------------------------------------------------------------
-- Q3: Lấy toàn bộ TỔ TIÊN NGHIÊM NGẶT của nút comment_id = 3 (path = '1.2.3').
-- Toán tử @> : path IS ANCESTOR OF '1.2.3' (tính cả chính '1.2.3'); loại trừ
-- chính nó bằng nlevel(path) < nlevel('1.2.3').
-- Kỳ vọng trên seed_test: {1, 2} (KHÔNG tính node 3).
-- ----------------------------------------------------------------------------
SELECT c.comment_id, c.content, cp.path
FROM comment_path cp
JOIN comment c ON cp.comment_id = c.comment_id
WHERE cp.path @> '1.2.3'
  AND nlevel(cp.path) < nlevel('1.2.3'::ltree)
ORDER BY cp.path;


-- ----------------------------------------------------------------------------
-- Q4: Lấy các node ở độ sâu k của bài viết 1 (gốc có depth = 1).
--     Trong ltree: depth = nlevel(path) (gốc '1' có nlevel = 1).
--     Kỳ vọng với k = 2 trên seed_test: {2}.
-- ----------------------------------------------------------------------------
SELECT cp.comment_id, c.content, cp.path, nlevel(cp.path) AS depth
FROM comment_path cp
JOIN comment c ON c.comment_id = cp.comment_id
WHERE cp.post_id = 1
  AND nlevel(cp.path) = 2          -- đổi giá trị này để lấy tầng k (gốc = 1)
ORDER BY cp.path;


-- ----------------------------------------------------------------------------
-- Q5: Thêm một node mới làm con của node 2 (path = '1.2'), rồi ROLLBACK.
--     Với Path Enumeration: đường dẫn mới = path_cha || '.' || id_moi.
--     id mới lấy từ RETURNING (sequence có thể nhảy số sau các rollback trước).
-- ----------------------------------------------------------------------------
BEGIN;

DO $$
DECLARE
    v_parent INT := 2;
    v_parent_path ltree;
    v_parent_post INT;
    v_new_id INT;
BEGIN
    SELECT path, post_id INTO v_parent_path, v_parent_post
    FROM comment_path WHERE comment_id = v_parent;

    INSERT INTO comment (post_id, parent_id, author_id, content)
    VALUES (v_parent_post, v_parent, 2, 'Q5 path enum - child of 2')
    RETURNING comment_id INTO v_new_id;

    INSERT INTO comment_path (comment_id, post_id, path)
    VALUES (v_new_id, v_parent_post, v_parent_path || v_new_id::text::ltree);

    RAISE NOTICE 'Đã thêm comment_id = % với path = %.', v_new_id, v_parent_path || v_new_id::text::ltree;
END $$;

SELECT cp.comment_id, cp.post_id, cp.path, c.content
FROM comment_path cp JOIN comment c ON c.comment_id = cp.comment_id
ORDER BY cp.path;

ROLLBACK;


-- ----------------------------------------------------------------------------
-- Q6: Xóa node 2 và toàn bộ cây con của nó (path <@ '1.2'), rồi ROLLBACK.
--     Với Path Enumeration: xóa mọi node có path là hậu duệ của '1.2' (gồm chính nó).
-- ----------------------------------------------------------------------------
BEGIN;

DELETE FROM comment_path
WHERE path <@ '1.2';

-- Dọn luôn trong bảng comment gốc (để nhất quán dữ liệu minh họa).
DELETE FROM comment
WHERE comment_id IN (
    SELECT comment_id FROM comment WHERE comment_id = 2
    UNION
    SELECT cp.comment_id FROM comment_path cp WHERE cp.path <@ '1.2'
);

SELECT cp.comment_id, cp.path, c.content
FROM comment_path cp JOIN comment c ON c.comment_id = cp.comment_id
ORDER BY cp.path;

ROLLBACK;

-- ----------------------------------------------------------------------------
-- Q7: Di chuyển nhánh subtree('1.2') sang làm con của node 4 (path = '4'), rồi ROLLBACK.
--     Với Path Enumeration: mọi hậu duệ của '1.2' phải đổi tiền tố path từ '1.2'
--     thành '4'. Dùng hàm subpath(path, nlevel('1.2')) để lấy phần đuôi rồi nối '4'.
--     Chống chu trình: cha mới '4' không được nằm trong subtree('1.2').
-- ----------------------------------------------------------------------------
BEGIN;

DO $$
DECLARE
    v_node_path ltree := '1.2';
    v_new_parent_path ltree := '4';
    v_new_parent INT := 4;
    v_node_post INT;
    v_parent_post INT;
    v_would_cycle BOOLEAN;
BEGIN
    SELECT post_id INTO v_node_post FROM comment_path WHERE path = v_node_path;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tìm thấy nhánh cần di chuyển: %', v_node_path;
    END IF;

    SELECT post_id INTO v_parent_post FROM comment_path WHERE path = v_new_parent_path;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tìm thấy cha mới: %', v_new_parent_path;
    END IF;
    IF v_node_post <> v_parent_post THEN
        RAISE EXCEPTION 'Không thể chuyển nhánh giữa hai bài viết khác nhau';
    END IF;

    -- Chống chu trình: cha mới không được là hậu duệ của nhánh di chuyển.
    SELECT EXISTS (
        SELECT 1 FROM comment_path WHERE path <@ v_node_path AND path = v_new_parent_path
    ) INTO v_would_cycle;

    IF v_would_cycle THEN
        RAISE EXCEPTION 'Không thể chuyển nhánh: cha mới % nằm trong cây con của %', v_new_parent_path, v_node_path;
    END IF;

    -- Đổi tiền tố: cắt bỏ tiền tố '1.2' khỏi text(path), giữ phần đuôi, rồi nối '4'.
    -- Dùng text để tránh lỗi "invalid positions" của subpath() khi path == node gốc.
    --   path '1.2'   -> đuôi ''   -> '4'
    --   path '1.2.3' -> đuôi '3'  -> '4.3'
    UPDATE comment_path
    SET path = (
        v_new_parent_path::text
        || CASE
             WHEN substr(text(path), length(v_node_path::text) + 2) = '' THEN ''
             ELSE '.' || substr(text(path), length(v_node_path::text) + 2)
           END
    )::ltree
    WHERE path <@ v_node_path;

    -- Đồng bộ parent_id của đầu nhánh trong bảng comment.
    UPDATE comment SET parent_id = v_new_parent WHERE comment_id = 2;

    RAISE NOTICE 'Đã chuyển subtree(%) xuống làm con của %.', v_node_path, v_new_parent_path;
END $$;

SELECT cp.comment_id, cp.path, c.content
FROM comment_path cp JOIN comment c ON c.comment_id = cp.comment_id
ORDER BY cp.path;

ROLLBACK;


-- ----------------------------------------------------------------------------
-- Q8: Đếm tổng số node trong cây con của comment_id = 1 (tính cả chính nút 1).
-- Kỳ vọng trên seed_test: 3.
-- ----------------------------------------------------------------------------
SELECT COUNT(*) AS subtree_node_count
FROM comment_path
WHERE path <@ '1';


-- ----------------------------------------------------------------------------
-- Q9: Lấy đường đi (breadcrumb) từ node 3 ngược về gốc, trình bày từ gốc -> node.
--     Nguyên lý: các node là tổ tiên của '1.2.3' (gồm chính nó) sắp theo path.
-- Kỳ vọng trên seed_test: 1 -> 2 -> 3 (gồm chính node 3).
-- ----------------------------------------------------------------------------
SELECT c.comment_id, c.content, cp.path, nlevel(cp.path) AS depth
FROM comment_path cp
JOIN comment c ON c.comment_id = cp.comment_id
WHERE cp.path @> '1.2.3'
ORDER BY cp.path;


-- ----------------------------------------------------------------------------
-- Q10: Kiểm tra nhanh A có phải tổ tiên NGHIÊM NGẶT của B hay không.
--      Nguyên lý: A tổ tiên B khi path_B <@ path_A (và path_A <> path_B để nghiêm ngặt).
-- Kỳ vọng: 1 là tổ tiên của 3 (true); 4 không là tổ tiên của 3 (false).
-- ----------------------------------------------------------------------------
WITH cases(ancestor_id, descendant_id) AS (
    VALUES (1, 3), (4, 3)
)
SELECT cases.ancestor_id,
       cases.descendant_id,
       EXISTS (
           SELECT 1
           FROM comment_path a
           JOIN comment_path b ON b.comment_id = cases.descendant_id
           WHERE a.comment_id = cases.ancestor_id
             AND b.path <@ a.path
             AND b.path <> a.path          -- nghiêm ngặt: bỏ trường hợp chính nó
       ) AS is_ancestor
FROM cases
ORDER BY cases.ancestor_id;


-- ----------------------------------------------------------------------------
-- Các câu truy vấn Q1-Q10 cho Path Enumeration đã được triển khai.
-- ----------------------------------------------------------------------------
