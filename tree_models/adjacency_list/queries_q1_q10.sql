-- ============================================================================
-- FILE: tree_models/adjacency_list/queries_q1_q10.sql
-- M?C ??CH: Q1-Q10 cho Adjacency List tr?n comment(parent_id).
-- QUY ??C: Q2/Q8 t?nh c? node; Q3/Q10 l? t? ti?n nghi?m ng?t.
-- Y?U C?U: Ch?y database/schema.sql + database/seed_test.sql tr??c.
-- ============================================================================

-- Q1. To?n b? c?y post 1, th? t? ph?n c?p.
WITH RECURSIVE tree AS (
    SELECT comment_id, parent_id, content, 0 AS level, ARRAY[comment_id] AS sort_path
    FROM comment WHERE post_id = 1 AND parent_id IS NULL
    UNION ALL
    SELECT child.comment_id, child.parent_id, child.content, tree.level + 1,
           tree.sort_path || child.comment_id
    FROM comment child JOIN tree ON child.parent_id = tree.comment_id
)
SELECT comment_id, parent_id, repeat('  ', level) || content AS indented_content, level
FROM tree ORDER BY sort_path;

-- Q2. Subtree node 1, g?m node 1.
WITH RECURSIVE subtree AS (
    SELECT comment_id, parent_id, content, 0 AS depth FROM comment WHERE comment_id = 1
    UNION ALL
    SELECT child.comment_id, child.parent_id, child.content, subtree.depth + 1
    FROM comment child JOIN subtree ON child.parent_id = subtree.comment_id
)
SELECT * FROM subtree ORDER BY depth, comment_id;

-- Q3. T? ti?n nghi?m ng?t node 3, t? root t?i cha tr?c ti?p.
WITH RECURSIVE ancestors AS (
    SELECT parent.comment_id, parent.parent_id, parent.content, 1 AS distance
    FROM comment node JOIN comment parent ON parent.comment_id = node.parent_id
    WHERE node.comment_id = 3
    UNION ALL
    SELECT parent.comment_id, parent.parent_id, parent.content, ancestors.distance + 1
    FROM ancestors JOIN comment parent ON parent.comment_id = ancestors.parent_id
)
SELECT * FROM ancestors ORDER BY distance DESC;

-- Q4. Node ? ?? s?u k=1 c?a post 1; g?c c? depth=0.
WITH RECURSIVE tree AS (
    SELECT comment_id, parent_id, content, 0 AS depth FROM comment WHERE post_id = 1 AND parent_id IS NULL
    UNION ALL
    SELECT child.comment_id, child.parent_id, child.content, tree.depth + 1
    FROM comment child JOIN tree ON child.parent_id = tree.comment_id
)
SELECT * FROM tree WHERE depth = 1 ORDER BY comment_id;

-- Q5. Th?m node con node 2, sau ?? rollback.
BEGIN;
SELECT al_insert_child(2, 'Q5: node m?i') AS new_comment_id;
ROLLBACK;

-- Q6. X?a subtree node 2, sau ?? rollback.
BEGIN;
SELECT al_delete_subtree(2) AS deleted_node_count;
ROLLBACK;

-- Q7. Chuy?n node 2 sang node 4, ch?ng chu tr?nh, sau ?? rollback.
BEGIN;
SELECT al_move_subtree(2, 4);
SELECT comment_id, parent_id FROM comment WHERE comment_id = 2;
ROLLBACK;

-- Q8. ??m node subtree 1, k? v?ng seed_test: 3.
WITH RECURSIVE subtree(comment_id) AS (
    SELECT comment_id FROM comment WHERE comment_id = 1
    UNION ALL
    SELECT child.comment_id FROM comment child JOIN subtree ON child.parent_id = subtree.comment_id
)
SELECT COUNT(*) AS subtree_node_count FROM subtree;

-- Q9. Breadcrumb node 3 t? root t?i node.
WITH RECURSIVE breadcrumb AS (
    SELECT comment_id, parent_id, content, 0 AS distance FROM comment WHERE comment_id = 3
    UNION ALL
    SELECT parent.comment_id, parent.parent_id, parent.content, breadcrumb.distance + 1
    FROM breadcrumb JOIN comment parent ON parent.comment_id = breadcrumb.parent_id
)
SELECT comment_id, content, distance AS distance_from_node
FROM breadcrumb ORDER BY distance DESC;

-- Q10. A c? l? t? ti?n nghi?m ng?t c?a B? K? v?ng (1,3)=true; (4,3)=false.
WITH RECURSIVE cases(ancestor_id, descendant_id) AS (
    VALUES (1, 3), (4, 3)
), ancestors AS (
    SELECT cases.ancestor_id, cases.descendant_id, node.parent_id
    FROM cases JOIN comment node ON node.comment_id = cases.descendant_id
    UNION ALL
    SELECT ancestors.ancestor_id, ancestors.descendant_id, parent.parent_id
    FROM ancestors JOIN comment parent ON parent.comment_id = ancestors.parent_id
)
SELECT cases.ancestor_id, cases.descendant_id,
       EXISTS (
           SELECT 1 FROM ancestors
           WHERE ancestors.ancestor_id = cases.ancestor_id
             AND ancestors.descendant_id = cases.descendant_id
             AND ancestors.parent_id = cases.ancestor_id
       ) AS is_ancestor
FROM cases ORDER BY ancestor_id;
