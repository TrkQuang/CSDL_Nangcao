-- ============================================================================
-- FILE: tree_models/path_enumeration/schema.sql
-- MỤC ĐÍCH: Chỉ mục cho mô hình Liệt kê đường dẫn dùng PostgreSQL extension `ltree`.
-- PHỤ TRÁCH: TV2.
-- YÊU CẦU: Chạy database/schema.sql của TV3 trước (đã tạo bảng comment_path
--           và bật extension ltree). File này KHÔNG tạo bảng mới, chỉ bổ sung
--           chỉ mục phục vụ truy vấn trên cột path kiểu ltree.
-- ============================================================================

-- Đảm bảo extension ltree tồn tại (idempotent, an toàn khi chạy lại).
CREATE EXTENSION IF NOT EXISTS ltree;

-- Chỉ mục GiST cho phép tìm kiếm cha/con trên ltree cực nhanh với toán tử <@ và @>
CREATE INDEX IF NOT EXISTS idx_comment_path_gist ON comment_path USING GIST (path);

-- Chỉ mục B-tree phục vụ sắp xếp/thứ tự phân cấp (ORDER BY path) và tra cứu chính xác.
CREATE INDEX IF NOT EXISTS idx_comment_path_btree ON comment_path USING BTREE (path);
