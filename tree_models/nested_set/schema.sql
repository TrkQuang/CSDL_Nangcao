-- ============================================================================
-- FILE: tree_models/nested_set/schema.sql
-- MỤC ĐÍCH: DDL bảng mô hình Tập lồng (Nested Set Model - lft, rgt)
-- PHỤ TRÁCH: TV2.
-- ============================================================================

CREATE TABLE IF NOT EXISTS comment_nested_set (
    comment_id INT PRIMARY KEY,
    post_id    INT NOT NULL,
    lft        INT NOT NULL,
    rgt        INT NOT NULL,
    content    TEXT NOT NULL,
    CHECK (lft < rgt)
);

-- Chỉ mục phức hợp quan trọng nhất cho mô hình Nested Set:
-- Phục vụ truy vấn khoảng [lft BETWEEN parent.lft AND parent.rgt]
CREATE INDEX IF NOT EXISTS idx_comment_ns_bounds ON comment_nested_set (post_id, lft, rgt);
