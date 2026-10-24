-- ============================================================================
-- FILE: tree_models/adjacency_list/schema.sql
-- MỤC ĐÍCH: DDL bảng mô hình Danh sách kề (Adjacency List)
-- PHỤ TRÁCH: TV2.
-- ============================================================================


-- Chỉ mục tối ưu cho truy vấn tìm con theo cha
CREATE INDEX IF NOT EXISTS idx_comment_adj_parent ON comment(parent_id);
CREATE INDEX IF NOT EXISTS idx_comment_adj_post ON comment(post_id);
