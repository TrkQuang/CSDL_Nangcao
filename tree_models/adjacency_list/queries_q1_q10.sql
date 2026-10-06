-- ============================================================================
-- FILE: tree_models/adjacency_list/queries_q1_q10.sql
-- MỤC ĐÍCH: Bộ 10 truy vấn chuẩn (Q1-Q10) cho mô hình Adjacency List dùng WITH RECURSIVE.
-- PHỤ TRÁCH: TV2 (Kiểm chứng kết quả khớp seed_test: TV5).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU Q1]: Lấy toàn bộ cây theo thứ tự phân cấp kèm thụt đầu dòng (indent)
-- ----------------------------------------------------------------------------
WITH RECURSIVE comment_tree AS (
    -- Điểm neo: Lấy các nút gốc (parent_id IS NULL)
    SELECT 
        comment_id, parent_id, content, 
        0 AS level, 
        ARRAY[comment_id] AS path_sort
    FROM comment
    WHERE post_id = 1 AND parent_id IS NULL

    UNION ALL

    -- Bước đệ quy: Tìm con trực tiếp
    SELECT 
        c.comment_id, c.parent_id, c.content, 
        ct.level + 1, 
        ct.path_sort || c.comment_id
    FROM comment c
    JOIN comment_tree ct ON c.parent_id = ct.comment_id
)
SELECT 
    comment_id,
    parent_id,
    repeat('  ', level) || content AS indented_content,
    level
FROM comment_tree
ORDER BY path_sort;


-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU Q2]: Lấy toàn bộ hậu duệ (subtree) của nút comment_id = 1
-- Kỳ vọng trên seed_test: {c1, c2, c3}
-- ----------------------------------------------------------------------------
WITH RECURSIVE subtree AS (
    SELECT comment_id, parent_id, content, 1 AS depth
    FROM comment
    WHERE comment_id = 1

    UNION ALL

    SELECT c.comment_id, c.parent_id, c.content, s.depth + 1
    FROM comment c
    JOIN subtree s ON c.parent_id = s.comment_id
)
SELECT * FROM subtree;


-- ----------------------------------------------------------------------------
-- [TODO: TV2 triển khai tiếp các câu còn lại]
-- Q3: Lấy toàn bộ tổ tiên của nút comment_id = 3 (Kỳ vọng: c2, c1)
-- Q4: Lấy các nút ở độ sâu k
-- Q5: Thêm nút
-- Q6: Xóa nút và subtree
-- Q7: Di chuyển nhánh (chặn chu trình)
-- Q8: Đếm số nút trong cây con của comment_id = 1 (Kỳ vọng: 3)
-- Q9: Lấy đường đi từ nút về root (Breadcrumb)
-- Q10: Kiểm tra nhanh xem nút A có phải là tổ tiên của nút B không
-- ----------------------------------------------------------------------------
