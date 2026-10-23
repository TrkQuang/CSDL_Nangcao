-- ============================================================================
-- FILE: tree_models/adjacency_list/crud.sql
-- MỤC ĐÍCH: Thao tác Thêm, Sửa, Xóa và Di chuyển nút trong mô hình Adjacency List.
-- PHỤ TRÁCH: TV2.
-- ============================================================================

-- [VÍ DỤ MẪU 1]: Thêm một bình luận con vào bình luận id = 1
INSERT INTO comment_adjacency (post_id, parent_id, author_id, content)
VALUES (1, 1, 2, 'Bình luận con mới thêm');

-- [VÍ DỤ MẪU 2]: Xóa một nút (nhờ ON DELETE CASCADE sẽ xóa cả cây con)
-- DELETE FROM comment_adjacency WHERE comment_id = 1;

-- [TODO: TV2]: Viết lệnh di chuyển nhánh (chuyển cha của node 2 sang cha 4)
-- Lưu ý: Cần kiểm tra để không chuyển vào chính con/cháu của nó!
