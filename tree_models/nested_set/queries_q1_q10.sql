-- ============================================================================
-- FILE: tree_models/nested_set/queries_q1_q10.sql
-- MỤC ĐÍCH: Bộ 10 truy vấn chuẩn (Q1-Q10) cho mô hình Nested Set dùng BETWEEN.
-- PHỤ TRÁCH: TV2 (Kiểm chứng: TV5).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU Q2]: Lấy toàn bộ hậu duệ của nút comment_id = 1
-- Nguyên lý: Các con có lft nằm trong khoảng [parent.lft, parent.rgt]
-- Kỳ vọng trên seed_test: 1, 2, 3
-- ----------------------------------------------------------------------------
SELECT c.comment_id, c.content, node.lft, node.rgt
FROM comment_ns node
JOIN comment_ns parent ON node.lft BETWEEN parent.lft AND parent.rgt
JOIN comment c ON node.comment_id = c.comment_id
WHERE parent.comment_id = 1
ORDER BY node.lft;


-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU Q8]: Đếm số lượng nút trong cây con của comment_id = 1
-- Công thức đặc biệt của Nested Set: (rgt - lft + 1) / 2 mà KHÔNG CẦN đếm từng dòng!
-- ----------------------------------------------------------------------------
SELECT 
    comment_id,
    (rgt - lft + 1) / 2 AS subtree_node_count
FROM comment_ns
WHERE comment_id = 1;


-- ----------------------------------------------------------------------------
-- [TODO: TV2 triển khai tiếp các câu còn lại]
-- Q1: Lấy toàn bộ cây theo thứ tự phân cấp (ORDER BY lft)
-- Q3: Lấy tổ tiên của nút comment_id = 3 (parent.lft < node.lft AND parent.rgt > node.rgt)
-- Q4: Node ở độ sâu k
-- Q5: Thêm node
-- Q6: Xóa node và subtree
-- Q7: Di chuyển nhánh
-- Q9: Đường đi từ node về root
-- Q10: Kiểm tra A là tổ tiên B (A.lft < B.lft AND A.rgt > B.rgt)
-- ----------------------------------------------------------------------------
