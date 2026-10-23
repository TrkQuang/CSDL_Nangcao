-- ============================================================================
-- FILE: tree_models/adjacency_list/crud.sql
-- MUC DICH: CRUD cho mo hinh Adjacency List tren bang comment(parent_id).
-- YEU CAU: Chay database/schema.sql + database/seed_test.sql truoc.
-- Moi vi du dung ROLLBACK de giu nguyen du lieu kiem chung.
-- ============================================================================

-- Th?m node con cu?i c?ng. Tr? v? comment_id m?i.
CREATE OR REPLACE FUNCTION al_insert_child(p_parent_id INT, p_content TEXT)
RETURNS INT AS $$
DECLARE
    v_new_id INT;
BEGIN
    INSERT INTO comment (post_id, parent_id, author_id, content)
    SELECT post_id, comment_id, author_id, p_content
    FROM comment
    WHERE comment_id = p_parent_id
    RETURNING comment_id INTO v_new_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Khong tim thay node cha: %', p_parent_id;
    END IF;
    RETURN v_new_id;
END;
$$ LANGUAGE plpgsql;

-- X?a node v? to?n b? subtree nh? kh?a ngo?i parent_id ON DELETE CASCADE.
CREATE OR REPLACE FUNCTION al_delete_subtree(p_node_id INT)
RETURNS INT AS $$
DECLARE
    v_deleted INT;
BEGIN
    WITH RECURSIVE subtree(comment_id) AS (
        SELECT comment_id FROM comment WHERE comment_id = p_node_id
        UNION ALL
        SELECT child.comment_id
        FROM comment child
        JOIN subtree ON child.parent_id = subtree.comment_id
    )
    SELECT COUNT(*) INTO v_deleted FROM subtree;

    IF v_deleted = 0 THEN
        RAISE EXCEPTION 'Khong tim thay node can xoa: %', p_node_id;
    END IF;

    DELETE FROM comment WHERE comment_id = p_node_id;
    RETURN v_deleted;
END;
$$ LANGUAGE plpgsql;

-- Chuy?n node c?ng subtree sang cha m?i. Ch?n chuy?n v?o ch?nh n?/con ch?u.
CREATE OR REPLACE FUNCTION al_move_subtree(p_node_id INT, p_new_parent_id INT)
RETURNS VOID AS $$
DECLARE
    v_node_post INT;
    v_parent_post INT;
    v_would_cycle BOOLEAN;
BEGIN
    IF p_node_id = p_new_parent_id THEN
        RAISE EXCEPTION 'Node khong the la cha cua chinh no: %', p_node_id;
    END IF;

    SELECT post_id INTO v_node_post FROM comment WHERE comment_id = p_node_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Khong tim thay node can di chuyen: %', p_node_id;
    END IF;
    SELECT post_id INTO v_parent_post FROM comment WHERE comment_id = p_new_parent_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Khong tim thay cha moi: %', p_new_parent_id;
    END IF;
    IF v_node_post <> v_parent_post THEN
        RAISE EXCEPTION 'Khong the chuyen nhanh giua hai bai viet khac nhau';
    END IF;

    WITH RECURSIVE subtree(comment_id) AS (
        SELECT comment_id FROM comment WHERE comment_id = p_node_id
        UNION ALL
        SELECT child.comment_id
        FROM comment child
        JOIN subtree ON child.parent_id = subtree.comment_id
    )
    SELECT EXISTS (SELECT 1 FROM subtree WHERE comment_id = p_new_parent_id)
    INTO v_would_cycle;

    IF v_would_cycle THEN
        RAISE EXCEPTION 'Khong the chuyen nhanh: cha moi % nam trong subtree cua %', p_new_parent_id, p_node_id;
    END IF;

    UPDATE comment SET parent_id = p_new_parent_id WHERE comment_id = p_node_id;
END;
$$ LANGUAGE plpgsql;

BEGIN;
SELECT al_insert_child(2, 'B?nh lu?n con m?i th?m') AS new_comment_id;
SELECT al_move_subtree(2, 4);
SELECT al_delete_subtree(2) AS deleted_node_count;
ROLLBACK;
