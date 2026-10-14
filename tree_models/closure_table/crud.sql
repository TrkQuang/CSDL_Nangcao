-- ============================================================================
-- FILE: tree_models/closure_table/crud.sql
-- MỤC ĐÍCH: Thao tác chèn nút mới và DI CHUYỂN nhánh trong Closure Table.
-- PHỤ TRÁCH: TV2.
-- YÊU CẦU: database/schema.sql + database/seed_test.sql (TV3),
--          tree_models/closure_table/schema.sql (TV2) trước.
-- GHÍCHÚ: Bảng dùng chung là comment_closure(ancestor, descendant, depth).
--          Mọi thao tác đều ROLLBACK để giữ nguyên dữ liệu kiểm chứng.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- HÀM 1: ct_insert_child(p_parent_id, p_content)
--   Thêm node mới làm con của p_parent_id.
--   Bước: (1) chèn vào bảng comment lấy id thật; (2) nhân bản MỌI cặp tổ tiên của
--         cha cho node mới (depth+1); (3) thêm cặp tự thân (new,new,0).
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION ct_insert_child(p_parent_id INT, p_content TEXT)
RETURNS INT AS $$
DECLARE
    v_new_id INT;
BEGIN
    -- (1) Chèn node mới vào bảng comment gốc (lấy id thật từ sequence).
    INSERT INTO comment (post_id, parent_id, author_id, content)
    SELECT post_id, p_parent_id, author_id, p_content
    FROM comment WHERE comment_id = p_parent_id
    RETURNING comment_id INTO v_new_id;

    -- (2) Nhân bản mọi cặp tổ tiên của cha, tăng depth thêm 1.
    INSERT INTO comment_closure (ancestor, descendant, depth)
    SELECT ancestor, v_new_id, depth + 1
    FROM comment_closure
    WHERE descendant = p_parent_id;

    -- (3) Cặp tự thân.
    INSERT INTO comment_closure (ancestor, descendant, depth)
    VALUES (v_new_id, v_new_id, 0);

    RETURN v_new_id;
END;
$$ LANGUAGE plpgsql;


-- ----------------------------------------------------------------------------
-- HÀM 2: ct_move_subtree(p_node_id, p_new_parent_id)
--   Di chuyển cả nhánh sang cha mới. Chống chu trình, rồi:
--     (1) Xóa liên kết TỔ TIÊN NGHIÊM NGẶT cũ của đầu nhánh trên mọi node con;
--     (2) Nối lại với tổ tiên MỚI (gồm chính cha mới và tổ tiên của nó).
--   Trả về số dòng bao đóng bị chèn lại.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION ct_move_subtree(p_node_id INT, p_new_parent_id INT)
RETURNS INT AS $$
DECLARE
    v_node_post INT;
    v_parent_post INT;
    v_would_cycle BOOLEAN;
    v_inserted INT;
BEGIN
    SELECT post_id INTO v_node_post FROM comment WHERE comment_id = p_node_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tìm thấy node cần di chuyển: %', p_node_id;
    END IF;

    SELECT post_id INTO v_parent_post FROM comment WHERE comment_id = p_new_parent_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tìm thấy cha mới: %', p_new_parent_id;
    END IF;
    IF v_node_post <> v_parent_post THEN
        RAISE EXCEPTION 'Không thể chuyển nhánh giữa hai bài viết khác nhau';
    END IF;

    -- Chống chu trình: cha mới không được nằm trong subtree của đầu nhánh.
    SELECT EXISTS (
        SELECT 1 FROM comment_closure WHERE ancestor = p_node_id AND descendant = p_new_parent_id
    ) INTO v_would_cycle;

    IF v_would_cycle THEN
        RAISE EXCEPTION 'Không thể chuyển nhánh: cha mới % nằm trong cây con của %', p_new_parent_id, p_node_id;
    END IF;

    -- (1) Xóa các liên kết TỔ TIÊN NGHIÊM NGẶT cũ (của đầu nhánh, depth>0)
    --     trên MỌI node trong subtree(p_node_id).
    WITH subtree(descendant) AS (
        SELECT descendant FROM comment_closure WHERE ancestor = p_node_id
    ),
    old_ancestors(ancestor) AS (
        SELECT ancestor FROM comment_closure WHERE descendant = p_node_id AND depth > 0
    )
    DELETE FROM comment_closure cc
    USING subtree s
    WHERE cc.descendant = s.descendant
      AND cc.depth > 0
      AND cc.ancestor IN (SELECT ancestor FROM old_ancestors);

    -- (2) Nối lại: mỗi tổ tiên MỚI a của new_parent (gồm cả chính new_parent) với
    --     mỗi node d trong subtree(node), depth = a.depth + 1 + (khoảng cách node->d).
    WITH subtree(node, descendant, node_depth) AS (
        SELECT p_node_id, descendant, depth FROM comment_closure WHERE ancestor = p_node_id
    ),
    new_ancestors(ancestor, anc_depth) AS (
        SELECT ancestor, depth FROM comment_closure WHERE descendant = p_new_parent_id
    ),
    ins AS (
        INSERT INTO comment_closure (ancestor, descendant, depth)
        SELECT na.ancestor, s.descendant, na.anc_depth + 1 + s.node_depth
        FROM new_ancestors na CROSS JOIN subtree s
        ON CONFLICT (ancestor, descendant) DO NOTHING
        RETURNING descendant
    )
    SELECT COUNT(*) INTO v_inserted FROM ins;

    -- Đồng bộ parent_id trực tiếp trong bảng comment.
    UPDATE comment SET parent_id = p_new_parent_id WHERE comment_id = p_node_id;

    RETURN v_inserted;
END;
$$ LANGUAGE plpgsql;


-- ============================================================================
-- CÁC PHÉP THỬ (mỗi phép thử đều ROLLBACK để giữ nguyên seed_test)
-- ============================================================================

-- [THỬ 1] Thêm node mới làm con của node 2 -> xem các cặp bao đóng được nhân bản.
BEGIN;
SELECT ct_insert_child(2, 'CRUD closure - child of 2') AS new_id;
SELECT ancestor, descendant, depth FROM comment_closure
WHERE descendant = (SELECT MAX(comment_id) FROM comment)
ORDER BY depth DESC;
ROLLBACK;

-- [THỬ 2] Di chuyển subtree(2) xuống làm con của node 4 -> xem liên kết đổi.
BEGIN;
SELECT ct_move_subtree(2, 4) AS inserted_rows;
SELECT ancestor, descendant, depth FROM comment_closure
ORDER BY ancestor, descendant;
ROLLBACK;

-- [THỬ 3] Chống chu trình: chuyển node 2 xuống dưới hậu duệ node 3 phải bị từ chối.
BEGIN;
DO $$
DECLARE
    v_rejected BOOLEAN := false;
BEGIN
    BEGIN
        PERFORM ct_move_subtree(2, 3);
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

-- [THỬ 4] Từ chối di chuyển node sang bài viết khác.
BEGIN;
DO $$
DECLARE
    v_rejected BOOLEAN := false;
BEGIN
    BEGIN
        PERFORM ct_move_subtree(2, 5);
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

-- Dọn hàm thử để file chạy lại được.
DROP FUNCTION IF EXISTS ct_insert_child(INT, TEXT);
DROP FUNCTION IF EXISTS ct_move_subtree(INT, INT);
