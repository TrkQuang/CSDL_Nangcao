-- ============================================================================
-- FILE: tree_models/closure_table/schema.sql
-- MỤC ĐÍCH: Chỉ mục cho mô hình Bảng bao đóng (Closure Table).
-- PHỤ TRÁCH: TV2.
-- YÊU CẦU: Chạy database/schema.sql của TV3 trước để tạo bảng comment_closure.
--           (Bảng comment_closure(ancestor, descendant, depth) do TV3 định nghĩa;
--            file này KHÔNG tạo bảng mới, chỉ bổ sung chỉ mục phục vụ truy vấn.)
-- ============================================================================

-- Truy vấn hậu duệ: WHERE ancestor = ? -> lọc nhanh theo ancestor.
CREATE INDEX IF NOT EXISTS idx_closure_ancestor ON comment_closure (ancestor, depth);

-- Truy vấn tổ tiên (đi ngược): WHERE descendant = ? -> lọc nhanh theo descendant.
CREATE INDEX IF NOT EXISTS idx_closure_descendant ON comment_closure (descendant, ancestor);

-- Lọc theo khoảng cách (depth) cho các truy vấn độ sâu / con trực tiếp.
CREATE INDEX IF NOT EXISTS idx_closure_depth ON comment_closure (depth);
