-- ============================================================================
-- FILE: tree_models/path_enumeration/schema.sql
-- MỤC ĐÍCH: DDL bảng mô hình Liệt kê đường dẫn dùng PostgreSQL extension `ltree`.
-- PHỤ TRÁCH: TV2.
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS ltree;

CREATE TABLE IF NOT EXISTS comment_path_demo (
    comment_id SERIAL PRIMARY KEY,
    post_id    INT NOT NULL,
    path       ltree NOT NULL,
    content    TEXT NOT NULL
);

-- Chỉ mục GiST cho phép tìm kiếm cha/con trên ltree cực nhanh với toán tử <@ và @>
CREATE INDEX IF NOT EXISTS idx_comment_path_gist ON comment_path_demo USING GIST (path);
CREATE INDEX IF NOT EXISTS idx_comment_path_btree ON comment_path_demo USING BTREE (path);
