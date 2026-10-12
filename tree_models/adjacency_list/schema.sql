-- ============================================================================
-- FILE: tree_models/adjacency_list/schema.sql
-- MỤC ĐÍCH: Tạo chỉ mục cho mô hình Adjacency List trên bảng comment dùng chung.
-- PHỤ TRÁCH: TV2.
-- YÊU CẦU: Chạy database/schema.sql trước để tạo bảng comment.
-- ============================================================================

-- Hỗ trợ tìm các bình luận con theo parent_id và liệt kê theo bài viết.
CREATE INDEX IF NOT EXISTS idx_comment_adj_parent ON comment(parent_id);
CREATE INDEX IF NOT EXISTS idx_comment_adj_post ON comment(post_id);
