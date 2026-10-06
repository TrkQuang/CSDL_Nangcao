-- ============================================================================
-- FILE: tree_models/closure_table/queries_q1_q10.sql
-- MỤC ĐÍCH: Bộ 10 truy vấn chuẩn (Q1-Q10) cho Closure Table dùng phép JOIN đơn giản.
-- PHỤ TRÁCH: TV2 (Kiểm chứng: TV5).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU Q2]: Lấy toàn bộ hậu duệ của nút ancestor = 1
-- Kỳ vọng trên seed_test: 1, 2, 3
-- ----------------------------------------------------------------------------
SELECT c.comment_id, c.content, cc.depth
FROM comment_closure cc
JOIN comment c ON cc.descendant = c.comment_id
WHERE cc.ancestor = 1
ORDER BY cc.depth;


-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU Q3]: Lấy toàn bộ tổ tiên của nút descendant = 3
-- Kỳ vọng trên seed_test: 1, 2, 3
-- ----------------------------------------------------------------------------
SELECT c.comment_id, c.content, cc.depth
FROM comment_closure cc
JOIN comment c ON cc.ancestor = c.comment_id
WHERE cc.descendant = 3
ORDER BY cc.depth DESC;


-- ----------------------------------------------------------------------------
-- [TODO: TV2 triển khai tiếp các câu còn lại]
-- Q1: Lấy toàn bộ cây theo phân cấp
-- Q4: Node ở độ sâu k (WHERE ancestor = 1 AND depth = k)
-- Q5: Thêm node
-- Q6: Xóa node và subtree
-- Q7: Di chuyển nhánh
-- Q8: Đếm số node trong subtree (COUNT(*) WHERE ancestor = 1)
-- Q9: Đường đi từ node về root
-- Q10: Kiểm tra A là tổ tiên B (EXISTS (WHERE ancestor = A AND descendant = B))
-- ----------------------------------------------------------------------------
