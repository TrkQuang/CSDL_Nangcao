-- ============================================================================
-- FILE: database/seed_bench.sql
-- MUC DICH: Sinh du lieu benchmark tai lap bang PostgreSQL generate_series.
-- CACH CHAY:
--   psql -d ten_db -f database/schema.sql
--   psql -d ten_db -v bench_size=1000 -f database/seed_bench.sql
-- KICH THUOC HO TRO: 1000, 10000, 100000.
-- ============================================================================

\if :{?bench_size}
\else
  \set bench_size 1000
\endif

BEGIN;

SELECT 1 / (:'bench_size'::integer IN (1000, 10000, 100000))::integer AS valid_bench_size;

-- Xoa toan bo du lieu cu va reset sequence de ket qua co the lap lai.
TRUNCATE TABLE users RESTART IDENTITY CASCADE;

-- Nguoi dung: N dong, email duy nhat.
INSERT INTO users (user_id, full_name, email, created_at)
SELECT
    user_id,
    format('Benchmark User %s', user_id),
    format('bench_user_%s@sgu.vn', user_id),
    timestamptz '2026-01-01 00:00:00+07' + user_id * interval '1 second'
FROM generate_series(1, :'bench_size'::integer) AS user_id;
SELECT setval('users_user_id_seq', :'bench_size'::integer, true);

-- Muoi nhom va thanh vien; owner cua Group k la User k.
INSERT INTO study_group (group_id, name, topic, is_private, owner_id)
SELECT
    group_id,
    format('Benchmark Group %s', group_id),
    format('Topic %s', group_id),
    false,
    group_id
FROM generate_series(1, 10) AS group_id;
SELECT setval('study_group_group_id_seq', 10, true);

INSERT INTO group_member (group_id, user_id, role, joined_at)
SELECT
    ((user_id - 1) % 10) + 1,
    user_id,
    CASE WHEN user_id <= 10 THEN 'owner' ELSE 'member' END,
    timestamptz '2026-01-01 00:00:00+07'
FROM generate_series(1, :'bench_size'::integer) AS user_id;

-- Muoi bai viet. Post 1 la cay comment benchmark.
INSERT INTO post (post_id, group_id, author_id, post_type, title, content, created_at)
SELECT
    post_id,
    ((post_id - 1) % 10) + 1,
    ((post_id - 1) % :'bench_size'::integer) + 1,
    'thaoluan',
    format('Benchmark post %s', post_id),
    format('Noi dung benchmark %s', post_id),
    timestamptz '2026-01-01 00:00:00+07' + post_id * interval '1 minute'
FROM generate_series(1, 10) AS post_id;
SELECT setval('post_post_id_seq', 10, true);

-- Do thi vo huong: moi user ket noi 5 user ke sau theo vong tron.
-- ON CONFLICT loai cap trung va giu rang buoc user_a < user_b.
INSERT INTO friendship (user_a, user_b, since)
SELECT
    LEAST(user_id, neighbor_id),
    GREATEST(user_id, neighbor_id),
    timestamptz '2026-01-01 00:00:00+07'
FROM generate_series(1, :'bench_size'::integer) AS user_id
CROSS JOIN generate_series(1, 5) AS step(offset_value)
CROSS JOIN LATERAL (
    SELECT ((user_id - 1 + step.offset_value) % :'bench_size'::integer) + 1 AS neighbor_id
) AS neighbor
ON CONFLICT (user_a, user_b) DO NOTHING;

UPDATE users u
SET friend_count = degree.total
FROM (SELECT a, COUNT(*) AS total FROM friend_edge GROUP BY a) degree
WHERE degree.a = u.user_id;

-- Cay tam phan: do sau xap xi 7 (1k), 9 (10k), 11 (100k).
-- Cung mot cay dong bo cho Adjacency List, ltree, Nested Set, Closure Table.
INSERT INTO comment (comment_id, post_id, author_id, parent_id, content, created_at)
SELECT
    comment_id,
    1,
    ((comment_id - 1) % :'bench_size'::integer) + 1,
    CASE WHEN comment_id = 1 THEN NULL ELSE ((comment_id - 2) / 3) + 1 END,
    format('Benchmark comment %s', comment_id),
    timestamptz '2026-01-01 00:00:00+07' + comment_id * interval '1 second'
FROM generate_series(1, :'bench_size'::integer) AS comment_id;
SELECT setval('comment_comment_id_seq', :'bench_size'::integer, true);

CREATE INDEX idx_seed_comment_parent ON comment(parent_id);

-- Path Enumeration: ltree label dung n<id>; khong dung label bat dau bang so.
WITH RECURSIVE tree AS (
    SELECT c.comment_id, ARRAY[c.comment_id] AS node_path
    FROM comment c
    WHERE c.parent_id IS NULL
    UNION ALL
    SELECT c.comment_id, tree.node_path || c.comment_id
    FROM comment c
    JOIN tree ON c.parent_id = tree.comment_id
)
INSERT INTO comment_path (comment_id, post_id, path)
SELECT comment_id, 1, ('n' || array_to_string(node_path, '.n'))::ltree
FROM tree;

-- Nested Set: DFS pre-order tao lft; so hau due tao rgt.
WITH RECURSIVE tree AS (
    SELECT c.comment_id, ARRAY[c.comment_id] AS sort_path
    FROM comment c
    WHERE c.parent_id IS NULL
    UNION ALL
    SELECT c.comment_id, tree.sort_path || c.comment_id
    FROM comment c
    JOIN tree ON c.parent_id = tree.comment_id
), events AS (
    SELECT comment_id, false AS closing, sort_path || 0 AS event_path FROM tree
    UNION ALL
    SELECT comment_id, true, sort_path || 2147483647 FROM tree
), numbered AS (
    SELECT comment_id, closing, ROW_NUMBER() OVER (ORDER BY event_path) AS position
    FROM events
)
INSERT INTO comment_ns (comment_id, post_id, lft, rgt)
SELECT comment_id, 1,
       MIN(position)::integer, MAX(position)::integer
FROM numbered
GROUP BY comment_id;

-- Closure Table: tu moi nut den chinh no (depth 0) va den tat ca hau due.
WITH RECURSIVE closure AS (
    SELECT comment_id AS ancestor, comment_id AS descendant, 0 AS depth
    FROM comment
    UNION ALL
    SELECT closure.ancestor, child.comment_id, closure.depth + 1
    FROM closure
    JOIN comment child ON child.parent_id = closure.descendant
)
INSERT INTO comment_closure (ancestor, descendant, depth)
SELECT ancestor, descendant, depth
FROM closure;

DROP INDEX idx_seed_comment_parent;

ANALYZE users;
ANALYZE friendship;
ANALYZE comment;
ANALYZE comment_path;
ANALYZE comment_ns;
ANALYZE comment_closure;
COMMIT;

-- Kiem tra nhanh: ba bang node phai bang N; closure phai >= N.
SELECT
    :'bench_size'::integer AS requested_size,
    (SELECT COUNT(*) FROM comment) AS comment_count,
    (SELECT COUNT(*) FROM comment_path) AS path_count,
    (SELECT COUNT(*) FROM comment_ns) AS nested_set_count,
    (SELECT COUNT(*) FROM comment_closure) AS closure_row_count,
    (SELECT COUNT(*) FROM friendship) AS friendship_count;
