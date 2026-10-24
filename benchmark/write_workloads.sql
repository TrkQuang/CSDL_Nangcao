CREATE OR REPLACE FUNCTION benchmark_insert_leaf(p_model TEXT, p_parent INT)
RETURNS INT LANGUAGE plpgsql AS $$
DECLARE
    new_id INT;
    parent_post INT;
    parent_path ltree;
    right_bound INT;
BEGIN
    SELECT post_id INTO STRICT parent_post FROM comment WHERE comment_id = p_parent;
    INSERT INTO comment(post_id, author_id, parent_id, content)
    VALUES(parent_post, 1, p_parent, 'Benchmark inserted leaf')
    RETURNING comment_id INTO new_id;
    IF p_model = 'Path Enumeration' THEN
        SELECT path INTO STRICT parent_path FROM comment_path WHERE comment_id = p_parent;
        INSERT INTO comment_path VALUES(new_id, parent_post, parent_path || ('n' || new_id)::ltree);
    ELSIF p_model = 'Nested Set' THEN
        SELECT rgt INTO STRICT right_bound FROM comment_ns WHERE comment_id = p_parent;
        UPDATE comment_ns SET rgt = rgt + 2 WHERE post_id = parent_post AND rgt >= right_bound;
        UPDATE comment_ns SET lft = lft + 2 WHERE post_id = parent_post AND lft > right_bound;
        INSERT INTO comment_ns VALUES(new_id, parent_post, right_bound, right_bound + 1);
    ELSIF p_model = 'Closure Table' THEN
        INSERT INTO comment_closure
        SELECT ancestor, new_id, depth + 1 FROM comment_closure WHERE descendant = p_parent
        UNION ALL SELECT new_id, new_id, 0;
    ELSIF p_model <> 'Adjacency List' THEN
        RAISE EXCEPTION 'Unknown model: %', p_model;
    END IF;
    RETURN new_id;
END;
$$;

CREATE OR REPLACE FUNCTION benchmark_move_leaf(p_model TEXT, p_node INT, p_parent INT)
RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE
    node_post INT;
    parent_post INT;
    old_left INT;
    old_right INT;
    new_right INT;
BEGIN
    SELECT post_id INTO STRICT node_post FROM comment WHERE comment_id = p_node;
    SELECT post_id INTO STRICT parent_post FROM comment WHERE comment_id = p_parent;
    IF p_node = p_parent OR node_post <> parent_post
       OR EXISTS(SELECT 1 FROM comment WHERE parent_id = p_node) THEN
        RAISE EXCEPTION 'Move workload requires leaf and distinct parent in same post';
    END IF;
    IF p_model = 'Path Enumeration' THEN
        UPDATE comment_path node SET path = parent.path || ('n' || p_node)::ltree
        FROM comment_path parent WHERE node.comment_id = p_node AND parent.comment_id = p_parent;
    ELSIF p_model = 'Nested Set' THEN
        SELECT lft, rgt INTO STRICT old_left, old_right FROM comment_ns WHERE comment_id = p_node;
        IF old_right <> old_left + 1 THEN
            RAISE EXCEPTION 'Nested Set leaf interval invalid';
        END IF;
        UPDATE comment_ns SET lft = lft - 2 WHERE post_id = node_post AND lft > old_right;
        UPDATE comment_ns SET rgt = rgt - 2 WHERE post_id = node_post AND rgt > old_right;
        SELECT rgt INTO STRICT new_right FROM comment_ns WHERE comment_id = p_parent;
        UPDATE comment_ns SET rgt = rgt + 2
        WHERE post_id = node_post AND rgt >= new_right AND comment_id <> p_node;
        UPDATE comment_ns SET lft = lft + 2
        WHERE post_id = node_post AND lft >= new_right AND comment_id <> p_node;
        UPDATE comment_ns SET lft = new_right, rgt = new_right + 1 WHERE comment_id = p_node;
    ELSIF p_model = 'Closure Table' THEN
        DELETE FROM comment_closure WHERE descendant = p_node AND ancestor <> p_node;
        INSERT INTO comment_closure
        SELECT ancestor, p_node, depth + 1 FROM comment_closure WHERE descendant = p_parent;
    ELSIF p_model <> 'Adjacency List' THEN
        RAISE EXCEPTION 'Unknown model: %', p_model;
    END IF;
    UPDATE comment SET parent_id = p_parent WHERE comment_id = p_node;
END;
$$;

CREATE OR REPLACE FUNCTION benchmark_assert_leaf(p_model TEXT, p_node INT, p_parent INT)
RETURNS VOID LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS(SELECT 1 FROM comment WHERE comment_id = p_node AND parent_id = p_parent) THEN
        RAISE EXCEPTION 'Write did not update adjacency parent';
    END IF;
    IF p_model = 'Path Enumeration' AND NOT EXISTS (
        SELECT 1 FROM comment_path node JOIN comment_path parent ON parent.comment_id = p_parent
        WHERE node.comment_id = p_node AND node.path <@ parent.path
          AND nlevel(node.path) = nlevel(parent.path) + 1
    ) THEN
        RAISE EXCEPTION 'Write did not update ltree correctly';
    END IF;
    IF p_model = 'Closure Table' AND EXISTS (
        (SELECT ancestor, depth + 1 AS depth FROM comment_closure WHERE descendant = p_parent
         UNION ALL SELECT p_node, 0
         EXCEPT SELECT ancestor, depth FROM comment_closure WHERE descendant = p_node)
        UNION ALL
        (SELECT ancestor, depth FROM comment_closure WHERE descendant = p_node
         EXCEPT (SELECT ancestor, depth + 1 FROM comment_closure WHERE descendant = p_parent
                 UNION ALL SELECT p_node, 0))
    ) THEN
        RAISE EXCEPTION 'Write did not update closure correctly';
    END IF;
    IF p_model = 'Nested Set' THEN
        IF NOT EXISTS (
            SELECT 1 FROM comment_ns node JOIN comment_ns parent ON parent.comment_id = p_parent
            WHERE node.comment_id = p_node AND node.lft > parent.lft
              AND node.rgt < parent.rgt AND node.rgt = node.lft + 1
        ) OR EXISTS (
            SELECT 1 FROM comment child JOIN comment_ns node ON node.comment_id = child.comment_id
            JOIN comment_ns parent ON parent.comment_id = child.parent_id
            WHERE node.lft <= parent.lft OR node.rgt >= parent.rgt
        ) OR EXISTS (
            SELECT post_id, boundary FROM (
                SELECT post_id, lft AS boundary FROM comment_ns
                UNION ALL SELECT post_id, rgt FROM comment_ns
            ) endpoints GROUP BY post_id, boundary HAVING COUNT(*) <> 1
        ) THEN
            RAISE EXCEPTION 'Write violated Nested Set bounds';
        END IF;
    END IF;
END;
$$;
