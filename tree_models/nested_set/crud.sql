-- ============================================================================
-- FILE: tree_models/nested_set/crud.sql
-- MỤC ĐÍCH: Thao tác Thêm, Xóa, Di chuyển khoảng [lft, rgt] trong Nested Set.
-- PHỤ TRÁCH: TV2.
-- YÊU CẦU: Chạy database/schema.sql + database/seed_test.sql (TV3),
--          tree_models/nested_set/schema.sql (TV2) trước.
-- LƯU Ý: Nested Set đọc rất nhanh nhưng GHI rất chậm do phải dời lft/rgt của
--        nhiều dòng (write amplification). Mỗi thao tác dưới đây đều ROLLBACK
--        để không làm thay đổi dữ liệu kiểm chứng.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- HÀM 1: ns_insert_child(p_parent_id, p_content)
--   Thêm node mới làm con CUỐI CÙNG của p_parent_id. Mở khoảng trống (dịch +2
--   mọi lft/rgt bên phải cha, CÙNG bài viết) rồi chèn node vào [R, R+1].
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION ns_insert_child(p_parent_id INT, p_content TEXT)
RETURNS INT AS $$
DECLARE
    v_parent_post INT;
    v_rgt INT;
    v_new_id INT;
BEGIN
    SELECT post_id, rgt INTO v_parent_post, v_rgt
    FROM comment_ns WHERE comment_id = p_parent_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tìm thấy node cha: %', p_parent_id;
    END IF;

    UPDATE comment_ns SET rgt = rgt + 2 WHERE rgt >= v_rgt AND post_id = v_parent_post;
    UPDATE comment_ns SET lft = lft + 2 WHERE lft > v_rgt AND post_id = v_parent_post;

    INSERT INTO comment (post_id, parent_id, author_id, content)
    VALUES (v_parent_post, p_parent_id, 2, p_content)
    RETURNING comment_id INTO v_new_id;

    INSERT INTO comment_ns (comment_id, post_id, lft, rgt)
    VALUES (v_new_id, v_parent_post, v_rgt, v_rgt + 1);

    RETURN v_new_id;
END;
$$ LANGUAGE plpgsql;


-- ----------------------------------------------------------------------------
-- HÀM 2: ns_delete_subtree(p_node_id)
--   Xóa node và toàn bộ cây con; khép khoảng bằng cách dịch các node bên phải
--   lùi về đúng bề rộng subtree (rgt - lft + 1). Trả về số node đã xóa.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION ns_delete_subtree(p_node_id INT)
RETURNS INT AS $$
DECLARE
    v_post INT; v_lft INT; v_rgt INT; v_width INT; v_deleted INT;
BEGIN
    SELECT post_id, lft, rgt INTO v_post, v_lft, v_rgt
    FROM comment_ns WHERE comment_id = p_node_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tìm thấy node cần xóa: %', p_node_id;
    END IF;
    v_width := v_rgt - v_lft + 1;

    WITH RECURSIVE subtree(comment_id) AS (
        SELECT comment_id
        FROM comment
        WHERE comment_id = p_node_id AND post_id = v_post

        UNION

        SELECT c.comment_id
        FROM comment c
        JOIN subtree s ON c.parent_id = s.comment_id
        WHERE c.post_id = v_post
    )
    DELETE FROM comment
    WHERE comment_id IN (SELECT comment_id FROM subtree);
    GET DIAGNOSTICS v_deleted = ROW_COUNT;

    UPDATE comment_ns SET lft = lft - v_width WHERE lft > v_rgt AND post_id = v_post;
    UPDATE comment_ns SET rgt = rgt - v_width WHERE rgt > v_rgt AND post_id = v_post;
    RETURN v_deleted;
END;
$$ LANGUAGE plpgsql;


-- ----------------------------------------------------------------------------
-- HÀM 3: ns_move_subtree(p_node_id, p_new_parent_id)
--   Di chuyển nhánh sang cha mới. Chống chu trình, cập nhật parent_id, rồi
--   REBUILD toàn bộ lft/rgt của bài viết theo pre-order. Trả về số node rebuild.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION ns_move_subtree(p_node_id INT, p_new_parent_id INT)
RETURNS INT AS $$
DECLARE
    v_post INT; v_parent_post INT; v_would_cycle BOOLEAN; v_count INT;
BEGIN
    SELECT post_id INTO v_post FROM comment WHERE comment_id = p_node_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tìm thấy node cần di chuyển: %', p_node_id;
    END IF;

    SELECT post_id INTO v_parent_post FROM comment WHERE comment_id = p_new_parent_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tìm thấy cha mới: %', p_new_parent_id;
    END IF;
    IF v_parent_post <> v_post THEN
        RAISE EXCEPTION 'Không thể chuyển nhánh giữa hai bài viết khác nhau';
    END IF;

    WITH RECURSIVE sub AS (
        SELECT comment_id FROM comment WHERE comment_id = p_node_id
        UNION
        SELECT c.comment_id FROM comment c JOIN sub ON c.parent_id = sub.comment_id
    )
    SELECT EXISTS (SELECT 1 FROM sub WHERE comment_id = p_new_parent_id)
    INTO v_would_cycle;

    IF v_would_cycle THEN
        RAISE EXCEPTION 'Không thể chuyển nhánh: cha mới % nằm trong cây con của %', p_new_parent_id, p_node_id;
    END IF;

    UPDATE comment SET parent_id = p_new_parent_id WHERE comment_id = p_node_id;

    WITH RECURSIVE ordered AS (
        SELECT comment_id, ARRAY[comment_id] AS ord
        FROM comment WHERE post_id = v_post AND parent_id IS NULL
        UNION ALL
        SELECT c.comment_id, o.ord || c.comment_id
        FROM comment c JOIN ordered o ON c.parent_id = o.comment_id
        WHERE c.post_id = v_post
    ),
    pre AS (SELECT comment_id, ROW_NUMBER() OVER (ORDER BY ord) AS rn FROM ordered),
    sz AS (
        SELECT x.comment_id, COUNT(y.comment_id) AS sz
        FROM ordered x JOIN ordered y ON y.ord[1:array_length(x.ord,1)] = x.ord
        GROUP BY x.comment_id
    ),
    upd AS (
        UPDATE comment_ns ns
        SET lft = 2*p.rn - 1, rgt = 2*p.rn + 2*s.sz - 2
        FROM pre p JOIN sz s ON s.comment_id = p.comment_id
        WHERE ns.comment_id = p.comment_id
        RETURNING ns.comment_id
    )
    SELECT COUNT(*) INTO v_count FROM upd;

    RETURN v_count;
END;
$$ LANGUAGE plpgsql;


-- ============================================================================
-- CÁC PHÉP THỬ (mỗi phép thử đều ROLLBACK để giữ nguyên seed_test)
-- ============================================================================

-- [THỬ 1] Thêm 1 node làm con của node 2 -> xem khoảng lft/rgt bị dịch.
BEGIN;
SELECT ns_insert_child(2, 'CRUD - child of 2') AS new_id;
SELECT ns.comment_id, ns.post_id, ns.lft, ns.rgt, c.content
FROM comment_ns ns JOIN comment c ON c.comment_id = ns.comment_id
ORDER BY ns.lft;
ROLLBACK;

-- [THỬ 2] Xóa subtree của node 2 (gồm 2 và 3) -> đếm node bị xóa và khép khoảng.
BEGIN;
SELECT ns_delete_subtree(2) AS deleted_nodes;
SELECT ns.comment_id, ns.lft, ns.rgt, c.content
FROM comment_ns ns JOIN comment c ON c.comment_id = ns.comment_id
ORDER BY ns.lft;
ROLLBACK;

-- [THỬ 3] Di chuyển subtree(2) xuống làm con của node 4 -> đếm node bị rebuild.
BEGIN;
SELECT ns_move_subtree(2, 4) AS rebuilt_nodes;
SELECT ns.comment_id, ns.lft, ns.rgt, c.content
FROM comment_ns ns JOIN comment c ON c.comment_id = ns.comment_id
ORDER BY ns.lft;
ROLLBACK;

-- [THỬ 4] Chống chu trình: chuyển node 2 xuống dưới chính hậu duệ của nó (node 3)
--           phải bị từ chối.
BEGIN;
DO $$
DECLARE
    v_rejected BOOLEAN := false;
BEGIN
    BEGIN
        PERFORM ns_move_subtree(2, 3);
    EXCEPTION
        WHEN raise_exception THEN
            v_rejected := SQLERRM LIKE 'Không thể chuyển nhánh:%';
    END;

    IF NOT v_rejected THEN
        RAISE EXCEPTION 'FAIL: di chuyển vào hậu duệ không bị chặn';
    END IF;
    RAISE NOTICE 'PASS: di chuyển vào hậu duệ đã bị chặn';
END $$;
ROLLBACK;

-- [THỬ 5] Từ chối di chuyển node sang bài viết khác.
BEGIN;
DO $$
DECLARE
    v_rejected BOOLEAN := false;
BEGIN
    BEGIN
        PERFORM ns_move_subtree(2, 5);
    EXCEPTION
        WHEN raise_exception THEN
            v_rejected := SQLERRM = 'Không thể chuyển nhánh giữa hai bài viết khác nhau';
    END;

    IF NOT v_rejected THEN
        RAISE EXCEPTION 'FAIL: cho phép di chuyển nhánh sang bài viết khác';
    END IF;
    RAISE NOTICE 'PASS: di chuyển xuyên bài viết đã bị chặn';
END $$;
ROLLBACK;

-- Dọn hàm thử (để file có thể chạy lại nhiều lần không lỗi "already exists").
DROP FUNCTION IF EXISTS ns_insert_child(INT, TEXT);
DROP FUNCTION IF EXISTS ns_delete_subtree(INT);
DROP FUNCTION IF EXISTS ns_move_subtree(INT, INT);
