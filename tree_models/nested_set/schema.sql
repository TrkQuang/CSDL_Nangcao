-- ============================================================================
-- FILE: tree_models/nested_set/schema.sql
-- MỤC ĐÍCH: Chỉ mục cho mô hình Tập lồng (Nested Set Model - lft, rgt).
-- PHỤ TRÁCH: TV2.
-- YÊU CẦU: Chạy database/schema.sql của TV3 trước để tạo bảng comment_ns.
--           (Bảng comment_ns(comment_id, post_id, lft, rgt) do TV3 định nghĩa;
--            file này KHÔNG tạo bảng mới, chỉ bổ sung chỉ mục phục vụ truy vấn.)
-- ============================================================================

-- Chỉ mục phức hợp quan trọng nhất cho mô hình Nested Set:
-- Phục vụ truy vấn khoảng [node.lft BETWEEN parent.lft AND parent.rgt] và
-- đếm/lọc hậu duệ theo (post_id, lft, rgt).
CREATE INDEX IF NOT EXISTS idx_comment_ns_bounds ON comment_ns (post_id, lft, rgt);

-- Hỗ trợ tra cứu 1 nút theo comment_id và sắp xếp theo rgt.
CREATE INDEX IF NOT EXISTS idx_comment_ns_rgt ON comment_ns (rgt);
