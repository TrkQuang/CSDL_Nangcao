-- ============================================================================
-- FILE: tree_models/path_enumeration/crud.sql
-- MỤC ĐÍCH: Thao tác chèn nút mới, cập nhật đường dẫn khi chuyển nhánh trong ltree.
-- PHỤ TRÁCH: TV2.
-- ============================================================================

-- [VÍ DỤ MẪU 1]: Thêm nút con mới vào nút có path '1.2'
-- Đường dẫn mới sẽ là: path_cha || '.' || id_moi
INSERT INTO comment_path (comment_id, post_id, path)
VALUES (10, 1, '1.2.10');

-- [TODO: TV2]: Viết script chuyển nhánh:
-- Cập nhật lại toàn bộ hậu duệ khi nút '1.2' chuyển sang làm con của nút '4'
-- Dùng hàm subpath() của extension ltree để đổi tiền tố path.
