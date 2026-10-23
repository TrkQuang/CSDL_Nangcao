-- ============================================================================
-- FILE: tree_models/path_enumeration/crud.sql
-- MỤC ĐÍCH: Thao tác chèn nút mới, cập nhật đường dẫn khi chuyển nhánh (ltree).
-- PHỤ TRÁCH: TV2.
-- YÊU CẦU: database/schema.sql + database/seed_test.sql (TV3),
--          tree_models/path_enumeration/schema.sql (TV2) trước.
-- GHÍCHÚ: Bảng dùng chung là comment_path(comment_id, post_id, path ltree).
--          Mọi thao tác đều ROLLBACK để giữ nguyên dữ liệu kiểm chứng.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- HÀM 1: pe_insert_child(p_parent_id, p_content)
--   Thêm node mới làm con của p_parent_id. Đường dẫn mới = path_cha || id_mới.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION pe_insert_child(p_parent_id INT, p_content TEXT)
RETURNS INT AS $$
DECLARE
    v_parent_path ltree;
    v_parent_post INT;
    v_new_id INT;
BEGIN
    SELECT path, post_id INTO v_parent_path, v_parent_post
    FROM comment_path WHERE comment_id = p_parent_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tìm thấy node cha: %', p_parent_id;
    END IF;

    INSERT INTO comment (post_id, parent_id, author_id, content)
    SELECT post_id, p_parent_id, author_id, p_content
    FROM comment WHERE comment_id = p_parent_id
    RETURNING comment_id INTO v_new_id;

    INSERT INTO comment_path (comment_id, post_id, path)
    VALUES (v_new_id, v_parent_post, v_parent_path || v_new_id::text::ltree);

    RETURN v_new_id;
END;
$$ LANGUAGE plpgsql;


-- ----------------------------------------------------------------------------
-- HÀM 2: pe_move_subtree(p_node_id, p_new_parent_id)
--   Di chuyển cả nhánh sang cha mới: đổi tiền tố path của MỌI hậu duệ.
--   Chống chu trình: cha mới không được là hậu duệ của đầu nhánh.
--   Cắt tiền tố bằng text() để tránh lỗi "invalid positions" của subpath()
--   khi path == node gốc của nhánh.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION pe_move_subtree(p_node_id INT, p_new_parent_id INT)
RETURNS INT AS $$
DECLARE
    v_node_path ltree;
    v_new_parent_path ltree;
    v_node_post INT;
    v_parent_post INT;
    v_would_cycle BOOLEAN;
    v_updated INT;
BEGIN
    SELECT path, post_id INTO v_node_path, v_node_post
    FROM comment_path WHERE comment_id = p_node_id;
    SELECT path, post_id INTO v_new_parent_path, v_parent_post
    FROM comment_path WHERE comment_id = p_new_parent_id;

    IF v_node_path IS NULL OR v_new_parent_path IS NULL THEN
        RAISE EXCEPTION 'Không tìm thấy node hoặc cha mới';
    END IF;
    IF v_node_post <> v_parent_post THEN
        RAISE EXCEPTION 'Không thể chuyển nhánh giữa hai bài viết khác nhau';
    END IF;

    -- Chống chu trình: cha mới không được là hậu duệ của đầu nhánh.
    SELECT EXISTS (
        SELECT 1 FROM comment_path WHERE path <@ v_node_path AND path = v_new_parent_path
    ) INTO v_would_cycle;

    IF v_would_cycle THEN
        RAISE EXCEPTION 'Không thể chuyển nhánh: cha mới nằm trong cây con của %', v_node_path;
    END IF;

    -- Đổi tiền tố cho mọi hậu duệ (gồm đầu nhánh).
    WITH upd AS (
        UPDATE comment_path cp
        SET path = (
            v_new_parent_path::text
            || CASE
                 WHEN substr(text(cp.path), length(v_node_path::text) + 2) = '' THEN ''
                 ELSE '.' || substr(text(cp.path), length(v_node_path::text) + 2)
               END
        )::ltree
        WHERE cp.path <@ v_node_path
        RETURNING cp.comment_id
    )
    SELECT COUNT(*) INTO v_updated FROM upd;

    -- Đồng bộ parent_id trong bảng comment.
    UPDATE comment SET parent_id = p_new_parent_id WHERE comment_id = p_node_id;

    RETURN v_updated;
END;
$$ LANGUAGE plpgsql;


-- ============================================================================
-- CÁC PHÉP THỬ (mỗi phép thử đều ROLLBACK để giữ nguyên seed_test)
-- ============================================================================

-- [THỬ 1] Thêm node mới làm con của node 2 (path '1.2' -> '1.2.<id>').
BEGIN;
SELECT pe_insert_child(2, 'CRUD path - child of 2') AS new_id;
SELECT comment_id, post_id, path FROM comment_path ORDER BY path;
ROLLBACK;

-- [THỬ 2] Di chuyển subtree('1.2') xuống làm con của node 4 ('4').
BEGIN;
SELECT pe_move_subtree(2, 4) AS updated_rows;
SELECT comment_id, path FROM comment_path ORDER BY path;
ROLLBACK;

-- [THỬ 3] Chống chu trình: chuyển node 2 xuống dưới hậu duệ node 3 phải bị từ chối.
BEGIN;
DO $$
DECLARE
    v_rejected BOOLEAN := false;
BEGIN
    BEGIN
        PERFORM pe_move_subtree(2, 3);
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
        PERFORM pe_move_subtree(2, 5);
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
DROP FUNCTION IF EXISTS pe_insert_child(INT, TEXT);
DROP FUNCTION IF EXISTS pe_move_subtree(INT, INT);
