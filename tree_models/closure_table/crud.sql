-- ============================================================================
-- FILE: tree_models/closure_table/crud.sql
-- MỤC ĐÍCH: Thao tác chèn nút mới và cập nhật các dòng bao đóng.
-- PHỤ TRÁCH: TV2.
-- ============================================================================

-- [VÍ DỤ MẪU]: Thêm nút mới (id = 10) làm con của nút id = 2
-- Bước 1: Nhân bản tất cả các quan hệ của tổ tiên của nút 2 và tăng depth lên 1
-- Bước 2: Thêm quan hệ tự thân (self-reference): (10, 10, 0)
INSERT INTO comment_closure_table (ancestor, descendant, depth)
SELECT ancestor, 10, depth + 1
FROM comment_closure_table
WHERE descendant = 2
UNION ALL
SELECT 10, 10, 0;

-- [TODO: TV2]: Viết thao tác di chuyển một nhánh trong Closure Table
-- (Xóa các liên kết tổ tiên cũ và nối lại với các tổ tiên mới).
