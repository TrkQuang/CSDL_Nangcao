-- ============================================================================
-- FILE: tree_models/closure_table/schema.sql
-- MỤC ĐÍCH: DDL bảng mô hình Bảng bao đóng (Closure Table)
-- PHỤ TRÁCH: TV2.
-- ============================================================================

-- Bảng quan hệ lưu tất cả các cặp tổ tiên - hậu duệ cùng khoảng cách depth
CREATE TABLE IF NOT EXISTS comment_closure_table (
    ancestor   INT NOT NULL,
    descendant INT NOT NULL,
    depth      INT NOT NULL,
    PRIMARY KEY (ancestor, descendant)
);

-- Chỉ mục hỗ trợ truy vấn ngược từ descendant lên ancestor (tìm cha/tổ tiên)
CREATE INDEX IF NOT EXISTS idx_closure_descendant ON comment_closure_table (descendant, ancestor);
CREATE INDEX IF NOT EXISTS idx_closure_depth ON comment_closure_table (depth);
