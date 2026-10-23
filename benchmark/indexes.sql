-- ============================================================================
-- FILE: benchmark/indexes.sql
-- MUC DICH: Tao chi muc cho phep so sanh truoc/sau indexing.
-- CACH CHAY: psql -d ten_db -f benchmark/indexes.sql
-- GO BO: python benchmark/scripts/run_benchmark.py ... --drop-indexes
-- ============================================================================

-- Adjacency List: tim con cua mot node trong mot post.
CREATE INDEX IF NOT EXISTS idx_bench_comment_post_parent
    ON comment (post_id, parent_id);

-- Path Enumeration: @> (ancestor) va <@ (descendant).
CREATE INDEX IF NOT EXISTS idx_bench_comment_path_gist
    ON comment_path USING GIST (path);
CREATE INDEX IF NOT EXISTS idx_bench_comment_path_post
    ON comment_path (post_id);

-- Nested Set: quet khoang lft/rgt cua mot post.
CREATE INDEX IF NOT EXISTS idx_bench_comment_ns_post_lft_rgt
    ON comment_ns (post_id, lft, rgt);

-- Closure Table: lay hau due va truy vet to tien.
CREATE INDEX IF NOT EXISTS idx_bench_closure_ancestor_depth_descendant
    ON comment_closure (ancestor, depth, descendant);
CREATE INDEX IF NOT EXISTS idx_bench_closure_descendant_ancestor
    ON comment_closure (descendant, ancestor);

-- Graph: duyet canh hai huong qua friend_edge.
CREATE INDEX IF NOT EXISTS idx_bench_friendship_user_b
    ON friendship (user_b, user_a);

ANALYZE comment;
ANALYZE comment_path;
ANALYZE comment_ns;
ANALYZE comment_closure;
ANALYZE friendship;