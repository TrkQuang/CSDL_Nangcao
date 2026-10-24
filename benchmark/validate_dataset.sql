BEGIN;

CREATE INDEX IF NOT EXISTS idx_validation_parent ON comment(parent_id);

DO $$
DECLARE
    node_count BIGINT;
BEGIN
    SELECT COUNT(*) INTO node_count FROM comment;
    IF (SELECT COUNT(*) FROM comment_path) <> node_count
       OR (SELECT COUNT(*) FROM comment_ns) <> node_count THEN
        RAISE EXCEPTION 'Tree model node counts disagree';
    END IF;
    IF EXISTS (
        SELECT 1 FROM comment child JOIN comment parent ON child.parent_id = parent.comment_id
        WHERE child.post_id <> parent.post_id
    ) THEN
        RAISE EXCEPTION 'Parent/child post mismatch';
    END IF;
    IF EXISTS (
        WITH RECURSIVE paths AS (
            SELECT comment_id, post_id, ARRAY[comment_id] AS ids
            FROM comment WHERE parent_id IS NULL
            UNION ALL
            SELECT child.comment_id, child.post_id, paths.ids || child.comment_id
            FROM comment child JOIN paths ON child.parent_id = paths.comment_id
        )
        SELECT 1 FROM paths JOIN comment_path stored USING(comment_id)
        WHERE stored.post_id <> paths.post_id
           OR regexp_replace(stored.path::text, 'n', '', 'g') <> array_to_string(paths.ids, '.')
    ) THEN
        RAISE EXCEPTION 'Path Enumeration differs from adjacency paths';
    END IF;
    IF EXISTS (
        WITH RECURSIVE expected(ancestor, descendant, depth) AS (
            SELECT comment_id, comment_id, 0 FROM comment
            UNION ALL
            SELECT expected.ancestor, child.comment_id, expected.depth + 1
            FROM expected JOIN comment child ON child.parent_id = expected.descendant
        )
        (SELECT * FROM expected EXCEPT SELECT * FROM comment_closure)
        UNION ALL
        (SELECT * FROM comment_closure EXCEPT SELECT * FROM expected)
    ) THEN
        RAISE EXCEPTION 'Closure Table differs from recursive adjacency';
    END IF;
    IF EXISTS (
        SELECT 1 FROM comment_closure relation
        JOIN comment_ns parent ON parent.comment_id = relation.ancestor
        JOIN comment_ns child ON child.comment_id = relation.descendant
        WHERE parent.post_id <> child.post_id OR parent.lft > child.lft OR parent.rgt < child.rgt
    ) OR EXISTS (
        SELECT 1 FROM comment_ns node
        JOIN (SELECT ancestor, COUNT(*) AS total FROM comment_closure GROUP BY ancestor) sizes
          ON sizes.ancestor = node.comment_id
        WHERE node.rgt - node.lft + 1 <> 2 * sizes.total
    ) OR EXISTS (
        SELECT post_id, boundary FROM (
            SELECT post_id, lft AS boundary FROM comment_ns
            UNION ALL SELECT post_id, rgt FROM comment_ns
        ) boundaries GROUP BY post_id, boundary HAVING COUNT(*) <> 1
    ) THEN
        RAISE EXCEPTION 'Nested Set interval invariants failed';
    END IF;
    IF EXISTS (
        SELECT 1 FROM users person LEFT JOIN (
            SELECT a, COUNT(*) AS total FROM friend_edge GROUP BY a
        ) counts ON counts.a = person.user_id
        WHERE person.friend_count <> COALESCE(counts.total, 0)
    ) THEN
        RAISE EXCEPTION 'friend_count differs from graph degree';
    END IF;
    IF node_count = 5 THEN
        IF (SELECT array_agg(descendant ORDER BY descendant) FROM comment_closure WHERE ancestor = 1)
            <> ARRAY[1,2,3]
           OR (SELECT array_agg(ancestor ORDER BY ancestor) FROM comment_closure WHERE descendant = 3 AND depth > 0)
            <> ARRAY[1,2] THEN
            RAISE EXCEPTION 'Manual ground truth failed';
        END IF;
    END IF;
    RAISE NOTICE 'PASS: % nodes; paths, closure pairs, nested intervals, friend_count verified', node_count;
END;
$$;

ROLLBACK;
