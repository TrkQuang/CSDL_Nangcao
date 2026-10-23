-- ============================================================================
-- FILE: tree_models/nested_set/queries_q1_q10.sql
-- MỤC ĐÍCH: Bộ 10 truy vấn chuẩn (Q1-Q10) cho mô hình Nested Set dùng BETWEEN.
-- PHỤ TRÁCH: TV2 (Kiểm chứng: TV5).
-- YÊU CẦU: database/schema.sql + database/seed_test.sql (TV3), nested_set/schema.sql (TV2).
-- QUY ƯỚC THỐNG NHẤT (khớp 4 mô hình):
--   * Subtree/hậu duệ (Q2, Q8): TÍNH CẢ chính node -> subtree(1)={1,2,3}, count=3.
--   * Tổ tiên (Q3, Q9, Q10): KHÔNG tính chính node (nghiêm ngặt) -> ancestors(3)={1,2}.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Q1: Lấy toàn bộ cây bài viết 1 theo thứ tự phân cấp (ORDER BY lft) kèm indent.
--     Nguyên lý: duyệt cây theo thứ tự tiền tự (pre-order) chính là ORDER BY lft.
--     Độ sâu (level) = số tổ tiên NGHIÊM NGẶT của node (gốc có level = 0).
--     Tính level bằng cách đếm bao nhiêu node khác có [lft,rgt] BAO QUAN node này.
-- ----------------------------------------------------------------------------
SELECT node.comment_id,
       node.post_id,
       repeat('  ', (
           SELECT (COUNT(*))::int
           FROM comment_ns anc
           WHERE anc.post_id = node.post_id
             AND anc.lft < node.lft
             AND anc.rgt > node.rgt
       )) || c.content AS indented_content,
       (
           SELECT (COUNT(*))::int
           FROM comment_ns anc
           WHERE anc.post_id = node.post_id
             AND anc.lft < node.lft
             AND anc.rgt > node.rgt
       ) AS level
FROM comment_ns node
JOIN comment c ON c.comment_id = node.comment_id
WHERE node.post_id = 1
ORDER BY node.lft;


-- ----------------------------------------------------------------------------
-- Q2: Lấy toàn bộ hậu duệ (subtree) của nút comment_id = 1.
-- Nguyên lý: Các con có lft nằm trong khoảng [parent.lft, parent.rgt].
-- Kỳ vọng trên seed_test: {1, 2, 3} (tính cả chính nút 1).
-- ----------------------------------------------------------------------------
SELECT c.comment_id, c.content, node.lft, node.rgt
FROM comment_ns node
JOIN comment_ns parent
  ON node.post_id = parent.post_id
 AND node.lft BETWEEN parent.lft AND parent.rgt
JOIN comment c ON node.comment_id = c.comment_id
WHERE parent.comment_id = 1
ORDER BY node.lft;


-- ----------------------------------------------------------------------------
-- Q3: Lấy toàn bộ TỔ TIÊN NGHIÊM NGẶT của nút comment_id = 3 (từ gốc xuống cha trực tiếp).
--     Nguyên lý: tổ tiên là các node có [lft,rgt] BAO QUAN node 3 (parent.lft < node.lft
--     AND parent.rgt > node.rgt). KHÔNG tính chính node 3.
-- Kỳ vọng trên seed_test: {1, 2}.
-- ----------------------------------------------------------------------------
SELECT parent.comment_id, parent.lft, parent.rgt, c.content
FROM comment_ns node
JOIN comment_ns parent
  ON parent.lft < node.lft AND parent.rgt > node.rgt
 AND parent.post_id = node.post_id
JOIN comment c ON c.comment_id = parent.comment_id
WHERE node.comment_id = 3
ORDER BY parent.lft;


-- ----------------------------------------------------------------------------
-- Q4: Lấy các node ở độ sâu k của bài viết 1 (gốc có depth = 1).
--     Trong Nested Set: depth = (số tổ tiên bao quanh) + 1.
--     Kỳ vọng với k = 2 trên seed_test: {2}.
-- ----------------------------------------------------------------------------
SELECT node.comment_id, c.content,
       (
           SELECT COUNT(*)
           FROM comment_ns anc
           WHERE anc.post_id = node.post_id
             AND anc.lft < node.lft
             AND anc.rgt > node.rgt
       ) + 1 AS depth
FROM comment_ns node
JOIN comment c ON c.comment_id = node.comment_id
WHERE node.post_id = 1
  AND (
           SELECT COUNT(*)
           FROM comment_ns anc
           WHERE anc.post_id = node.post_id
             AND anc.lft < node.lft
             AND anc.rgt > node.rgt
      ) + 1 = 2               -- đổi giá trị này để lấy tầng k (gốc = 1)
ORDER BY node.lft;


-- ----------------------------------------------------------------------------
-- Q5: Thêm một node mới làm con của node 2, rồi ROLLBACK.
--     Với Nested Set: (1) mở khoảng trống bằng cách dịch lft/rgt của các node
--     bên phải; (2) chèn node mới vào khoảng [R, R+1] ngay trước rgt của cha.
--     Ở đây chèn làm con CUỐI của node 2: vị trí chèn ngay trước rgt của cha (=5).
--     id mới lấy từ RETURNING (sequence có thể nhảy số sau các rollback trước).
-- ----------------------------------------------------------------------------
BEGIN;

DO $$
DECLARE
    v_parent_id INT := 2;
    v_parent_post INT;
    v_rgt INT;
    v_new_id INT;
BEGIN
    SELECT post_id, rgt INTO v_parent_post, v_rgt
    FROM comment_ns WHERE comment_id = v_parent_id;

    -- (1) Mở rộng khoảng trống: các node CÙNG BÀI VIẾT có lft > R hoặc rgt >= R bị dịch +2.
    UPDATE comment_ns SET rgt = rgt + 2 WHERE rgt >= v_rgt AND post_id = v_parent_post;
    UPDATE comment_ns SET lft = lft + 2 WHERE lft > v_rgt AND post_id = v_parent_post;

    -- Chèn node mới vào bảng comment để lấy id thật.
    INSERT INTO comment (post_id, parent_id, author_id, content)
    VALUES (v_parent_post, v_parent_id, 2, 'Q5 nested set - child of 2')
    RETURNING comment_id INTO v_new_id;

    -- (2) Chèn node mới vào khoảng [R, R+1].
    INSERT INTO comment_ns (comment_id, post_id, lft, rgt)
    VALUES (v_new_id, v_parent_post, v_rgt, v_rgt + 1);

    RAISE NOTICE 'Đã chèn comment_id = % vào khoảng [%, %].', v_new_id, v_rgt, v_rgt + 1;
END $$;

SELECT ns.comment_id, ns.post_id, ns.lft, ns.rgt, c.content
FROM comment_ns ns JOIN comment c ON c.comment_id = ns.comment_id
ORDER BY ns.lft;

ROLLBACK;


-- ----------------------------------------------------------------------------
-- Q6: Xóa node 2 và toàn bộ cây con của nó, rồi ROLLBACK.
--     Với Nested Set: xóa mọi node có lft trong [node.lft, node.rgt], rồi
--     "khép khoảng" bằng cách dịch ngược các node bên phải về đúng bề rộng subtree.
-- ----------------------------------------------------------------------------
BEGIN;

DO $$
DECLARE
    v_node INT := 2;
    v_post INT;
    v_lft INT;
    v_rgt INT;
    v_width INT;
BEGIN
    SELECT post_id, lft, rgt INTO v_post, v_lft, v_rgt FROM comment_ns WHERE comment_id = v_node;
    v_width := v_rgt - v_lft + 1;

    -- Xóa bình luận gốc và cây con; FK cascade dọn các dòng Nested Set tương ứng.
    WITH RECURSIVE subtree(comment_id) AS (
        SELECT comment_id
        FROM comment
        WHERE comment_id = v_node AND post_id = v_post

        UNION

        SELECT c.comment_id
        FROM comment c
        JOIN subtree s ON c.parent_id = s.comment_id
        WHERE c.post_id = v_post
    )
    DELETE FROM comment
    WHERE comment_id IN (SELECT comment_id FROM subtree);

    -- Khép khoảng: dịch các node bên phải CÙNG BÀI VIẾT lùi về đúng width.
    UPDATE comment_ns SET lft = lft - v_width WHERE lft > v_rgt AND post_id = v_post;
    UPDATE comment_ns SET rgt = rgt - v_width WHERE rgt > v_rgt AND post_id = v_post;

    RAISE NOTICE 'Đã xóa subtree(node %) bề rộng %.', v_node, v_width;
END $$;

SELECT ns.comment_id, ns.lft, ns.rgt, c.content
FROM comment_ns ns JOIN comment c ON c.comment_id = ns.comment_id
ORDER BY ns.lft;

ROLLBACK;


-- ----------------------------------------------------------------------------
-- Q7: Di chuyển nhánh subtree(2) sang làm con của node 4, rồi ROLLBACK.
--     Nested Set là thao tác ĐẮT nhất (dời ~nửa bảng). Để ĐÚNG và dễ kiểm chứng,
--     ta làm 2 bước:
--       (1) Chống chu trình: cha mới (4) không được nằm trong subtree(2).
--       (2) Cập nhật parent_id của đầu nhánh, rồi REBUILD toàn bộ lft/rgt của
--           bài viết bằng duyệt pre-order (WITH RECURSIVE) + đánh số.
--     (Đây là cách "tính lại từ đầu" - minh bạch; các hệ thực tế có thể dịch
--      in-place để tối ưu, nhưng rebuild đảm bảo tính đúng đắn tuyệt đối.)
-- ----------------------------------------------------------------------------
BEGIN;

DO $$
DECLARE
    v_node INT := 2;         -- đầu nhánh cần di chuyển
    v_new_parent INT := 4;   -- cha mới
    v_post INT;
    v_parent_post INT;
    v_would_cycle BOOLEAN;
BEGIN
    SELECT post_id INTO v_post FROM comment WHERE comment_id = v_node;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tìm thấy node cần di chuyển: %', v_node;
    END IF;

    SELECT post_id INTO v_parent_post FROM comment WHERE comment_id = v_new_parent;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tìm thấy cha mới: %', v_new_parent;
    END IF;
    IF v_parent_post <> v_post THEN
        RAISE EXCEPTION 'Không thể chuyển nhánh giữa hai bài viết khác nhau';
    END IF;

    -- (1) Chống chu trình: cha mới không được là hậu duệ của đầu nhánh.
    WITH RECURSIVE sub AS (
        SELECT comment_id FROM comment WHERE comment_id = v_node
        UNION
        SELECT c.comment_id FROM comment c JOIN sub ON c.parent_id = sub.comment_id
    )
    SELECT EXISTS (SELECT 1 FROM sub WHERE comment_id = v_new_parent)
    INTO v_would_cycle;

    IF v_would_cycle THEN
        RAISE EXCEPTION 'Không thể chuyển nhánh: cha mới % nằm trong cây con của nút %', v_new_parent, v_node;
    END IF;

    -- (2a) Cập nhật cha trực tiếp trong bảng comment (mô hình gốc).
    UPDATE comment SET parent_id = v_new_parent WHERE comment_id = v_node;

    -- (2b) Rebuild lft/rgt cho CẢ BÀI VIẾT theo thứ tự pre-order từ quan hệ cha-con.
    --      Dùng ord = mảng các comment_id trên đường đi (ổn định, duy nhất) để:
    --        rn  = thứ tự pre-order (ROW_NUMBER ORDER BY ord)
    --        sz  = số node trong subtree(gồm chính nó) = số node có ord "bị phủ" bởi ord này
    --      Công thức nested set chuẩn: lft = 2*rn - 1 ; rgt = 2*rn + 2*sz - 2.
    WITH RECURSIVE ordered AS (
        SELECT comment_id, parent_id, ARRAY[comment_id] AS ord
        FROM comment
        WHERE post_id = v_post AND parent_id IS NULL

        UNION ALL

        SELECT c.comment_id, c.parent_id, o.ord || c.comment_id
        FROM comment c
        JOIN ordered o ON c.parent_id = o.comment_id
        WHERE c.post_id = v_post
    ),
    pre AS (
        SELECT comment_id, ord, ROW_NUMBER() OVER (ORDER BY ord) AS rn
        FROM ordered
    ),
    sz AS (
        SELECT x.comment_id, COUNT(y.comment_id) AS sz
        FROM ordered x
        JOIN ordered y ON y.ord[1:array_length(x.ord, 1)] = x.ord
        GROUP BY x.comment_id
    )
    UPDATE comment_ns ns
    SET lft = 2 * p.rn - 1,
        rgt = 2 * p.rn + 2 * s.sz - 2
    FROM pre p
    JOIN sz s ON s.comment_id = p.comment_id
    WHERE ns.comment_id = p.comment_id;

    RAISE NOTICE 'Đã chuyển subtree(%) xuống làm con của % và rebuild lft/rgt.', v_node, v_new_parent;
END $$;

SELECT ns.comment_id, ns.lft, ns.rgt, c.content
FROM comment_ns ns JOIN comment c ON c.comment_id = ns.comment_id
ORDER BY ns.lft;

ROLLBACK;


-- ----------------------------------------------------------------------------
-- Q8: Đếm số lượng nút trong cây con của comment_id = 1.
-- Công thức đặc biệt của Nested Set: (rgt - lft + 1) / 2 mà KHÔNG CẦN đếm từng dòng!
-- Kỳ vọng trên seed_test: 3.
-- ----------------------------------------------------------------------------
SELECT 
    comment_id,
    (rgt - lft + 1) / 2 AS subtree_node_count
FROM comment_ns
WHERE comment_id = 1;


-- ----------------------------------------------------------------------------
-- Q9: Lấy đường đi (breadcrumb) từ node 3 ngược về gốc, trình bày từ gốc -> node.
--     Nguyên lý: lấy chính node 3 cùng các tổ tiên BAO QUAN nó (anc.lft <= node.lft
--     AND anc.rgt >= node.rgt), sắp theo lft tăng dần để ra thứ tự gốc -> node.
-- Kỳ vọng trên seed_test: 1 -> 2 -> 3 (gồm chính node 3).
-- ----------------------------------------------------------------------------
SELECT anc.comment_id, anc.lft, anc.rgt, c.content
FROM comment_ns node
JOIN comment_ns anc
  ON anc.lft <= node.lft AND anc.rgt >= node.rgt
 AND anc.post_id = node.post_id
JOIN comment c ON c.comment_id = anc.comment_id
WHERE node.comment_id = 3
ORDER BY anc.lft;


-- ----------------------------------------------------------------------------
-- Q10: Kiểm tra nhanh A có phải tổ tiên NGHIÊM NGẶT của B hay không.
--      Nguyên lý: A là tổ tiên của B khi A.lft < B.lft AND A.rgt > B.rgt (cùng bài viết).
-- Kỳ vọng: 1 là tổ tiên của 3 (true); 4 không là tổ tiên của 3 (false).
-- ----------------------------------------------------------------------------
WITH cases(ancestor_id, descendant_id) AS (
    VALUES (1, 3), (4, 3)
)
SELECT cases.ancestor_id,
       cases.descendant_id,
       EXISTS (
           SELECT 1
           FROM comment_ns a
           JOIN comment_ns b ON b.comment_id = cases.descendant_id
           WHERE a.comment_id = cases.ancestor_id
             AND a.post_id = b.post_id
             AND a.lft < b.lft
             AND a.rgt > b.rgt
       ) AS is_ancestor
FROM cases
ORDER BY cases.ancestor_id;


-- ----------------------------------------------------------------------------
-- Các câu truy vấn Q1-Q10 cho Nested Set đã được triển khai.
-- ----------------------------------------------------------------------------
