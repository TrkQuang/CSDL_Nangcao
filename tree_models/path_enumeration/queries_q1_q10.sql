-- ============================================================================
-- FILE: tree_models/path_enumeration/queries_q1_q10.sql
-- MỤC ĐÍCH: Bộ 10 truy vấn chuẩn (Q1-Q10) cho mô hình Path Enumeration (ltree).
-- PHỤ TRÁCH: TV2 (Kiểm chứng kết quả: TV5).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU Q2]: Lấy toàn bộ hậu duệ của nút comment_id = 1 (path = '1')
-- Toán tử <@ : path IS DESCENDANT OF '1'
-- Kỳ vọng trên seed_test: 1, 2, 3
-- ----------------------------------------------------------------------------
SELECT c.comment_id, c.content, cp.path
FROM comment_path cp
JOIN comment c ON cp.comment_id = c.comment_id
WHERE cp.path <@ '1'
ORDER BY cp.path;


-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU Q3]: Lấy toàn bộ tổ tiên của nút comment_id = 3 (path = '1.2.3')
-- Toán tử @> : path IS ANCESTOR OF '1.2.3'
-- Kỳ vọng trên seed_test: 1, 2, 3
-- ----------------------------------------------------------------------------
SELECT c.comment_id, c.content, cp.path
FROM comment_path cp
JOIN comment c ON cp.comment_id = c.comment_id
WHERE cp.path @> '1.2.3'
ORDER BY cp.path;


-- ----------------------------------------------------------------------------
-- [TODO: TV2 triển khai tiếp các câu còn lại]
-- Q1: Toàn bộ cây theo thứ tự phân cấp (ORDER BY path, độ sâu dùng nlevel(path))
-- Q4: Node ở độ sâu k (nlevel(path) = k)
-- Q5: Thêm node
-- Q6: Xóa node và subtree (WHERE path <@ 'x')
-- Q7: Di chuyển nhánh
-- Q8: Đếm số node trong subtree (COUNT(*) WHERE path <@ '1')
-- Q9: Đường đi từ node về root
-- Q10: Kiểm tra A có phải tổ tiên B (path_B <@ path_A)
-- ----------------------------------------------------------------------------
