-- ============================================================================
-- FILE: tree_models/nested_set/crud.sql
-- MỤC ĐÍCH: Thao tác Thêm, Xóa, Cập nhật khoảng [lft, rgt] trong Nested Set.
-- PHỤ TRÁCH: TV2.
-- LƯU Ý: Nested Set đọc rất nhanh nhưng ghi rất chậm do phải dời khoảng lft/rgt!
-- ============================================================================

-- [VÍ DỤ MẪU]: Quy trình thêm 1 nút mới làm con của nút có rgt = R
-- Bước 1: Mở rộng khoảng trống bằng cách tăng lft và rgt của các nút bên phải lên 2
-- UPDATE comment_nested_set SET rgt = rgt + 2 WHERE rgt >= R;
-- UPDATE comment_nested_set SET lft = lft + 2 WHERE lft > R;
-- Bước 2: Chèn nút mới vào vị trí [R, R + 1]
-- INSERT INTO comment_nested_set (comment_id, post_id, lft, rgt, content)
-- VALUES (new_id, post_id, R, R + 1, 'content');

-- [TODO: TV2]: Viết Stored Procedure hoàn chỉnh đóng gói thao tác Thêm và Xóa một nhánh
-- để phục vụ đo lường số dòng bị cập nhật (write amplification).
