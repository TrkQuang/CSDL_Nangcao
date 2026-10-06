-- ============================================================================
-- FILE: sql_advanced/q01_q08_select.sql
-- MỤC ĐÍCH: Hiện thực 8 câu truy vấn SQL nâng cao từ Q1 đến Q8 theo chuẩn đầu ra.
--           Mỗi câu cần có: Phát biểu nghiệp vụ, Câu lệnh SQL, Kết quả kỳ vọng trên
--           dữ liệu seed_test, và Phân tích kế hoạch thực thi EXPLAIN ANALYZE.
-- PHỤ TRÁCH: TV3 (Review: TV4).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU Q1]: Tìm người có số lượng bạn bè nhiều hơn mức trung bình toàn hệ thống
-- Kỹ thuật: Truy vấn con vô hướng (Scalar Subquery) trong mệnh đề WHERE
-- Kết quả kỳ vọng: Binh (3 bạn), Chi (3 bạn) do mức TB = (2+3+3+2+2+0)/6 = 2.0
-- ----------------------------------------------------------------------------
EXPLAIN ANALYZE
SELECT 
    user_id, 
    full_name, 
    friend_count
FROM users
WHERE friend_count > (
    SELECT AVG(friend_count) FROM users
);


-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU Q2]: Tìm người dùng chưa từng đăng bài viết nào VÀ chưa từng bình luận
-- Kỹ thuật: Phủ định kép dùng NOT EXISTS
-- Kết quả kỳ vọng: Phong (id = 6)
-- ----------------------------------------------------------------------------
EXPLAIN ANALYZE
SELECT 
    u.user_id, 
    u.full_name
FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM post p WHERE p.author_id = u.user_id
)
AND NOT EXISTS (
    SELECT 1 FROM comment c WHERE c.author_id = u.user_id
);


-- ----------------------------------------------------------------------------
-- [TODO: TV3 triển khai tiếp từ Q3 đến Q8]
-- ----------------------------------------------------------------------------

-- Q3: Tìm người tham gia TẤT CẢ các nhóm của chủ đề 'CSDL'
-- Kỹ thuật: Phép chia quan hệ (Relational Division) bằng NOT EXISTS lồng nhau.
-- TODO: Viết câu SQL...

-- Q4: Tìm các nhóm học tập có từ 3 thành viên trở lên
-- Kỹ thuật: GROUP BY, HAVING COUNT(*) >= 3 kết hợp JOIN.
-- TODO: Viết câu SQL...

-- Q5: Thống kê số lượng bình luận của mỗi bài viết (kể cả bài chưa có bình luận)
-- Kỹ thuật: LEFT JOIN và COALESCE / COUNT(comment_id).
-- TODO: Viết câu SQL...

-- Q6: Xếp hạng bài viết theo lượt thích (reaction) trong từng nhóm học tập
-- Kỹ thuật: Hàm cửa sổ (Window Function) RANK() OVER (PARTITION BY group_id ORDER BY likes DESC).
-- TODO: Viết câu SQL...

-- Q7: Một yêu cầu nghiệp vụ viết bằng 3 cách khác nhau (IN, EXISTS, JOIN)
-- Kỹ thuật: So sánh Execution Plan và chi phí Buffer/Cost của 3 cách viết.
-- TODO: Viết 3 cách và so sánh...

-- Q8: Tìm số lượng bạn chung giữa 2 người dùng bất kỳ
-- Kỹ thuật: Tự kết nối (Self-join) trên VIEW friend_edge.
-- TODO: Viết câu SQL...
