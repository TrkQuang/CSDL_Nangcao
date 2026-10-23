-- ============================================================================
-- FILE: tree_models/adjacency_list/schema.sql
-- MỤC ĐÍCH: DDL bảng mô hình Danh sách kề (Adjacency List)
-- PHỤ TRÁCH: TV2.
-- ============================================================================

CREATE TABLE IF NOT EXISTS comment_adjacency (
    comment_id SERIAL PRIMARY KEY,
    post_id    INT NOT NULL,
    parent_id  INT REFERENCES comment_adjacency(comment_id) ON DELETE CASCADE,
    author_id  INT NOT NULL,
    content    TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Chỉ mục tối ưu cho truy vấn tìm con theo cha
CREATE INDEX IF NOT EXISTS idx_comment_adj_parent ON comment_adjacency(parent_id);
CREATE INDEX IF NOT EXISTS idx_comment_adj_post ON comment_adjacency(post_id);
