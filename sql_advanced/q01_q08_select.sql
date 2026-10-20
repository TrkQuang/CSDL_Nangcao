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
)
ORDER BY user_id;


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
)
ORDER BY u.user_id;


-- Q3: Tìm người tham gia TẤT CẢ các nhóm của chủ đề 'CSDL'
-- Kỹ thuật: Phép chia quan hệ (Relational Division) bằng NOT EXISTS lồng nhau.
-- Kết quả kỳ vọng trên seed_test: An, Binh, Chi, Dung.
EXPLAIN ANALYZE
SELECT u.user_id, u.full_name
FROM users u
WHERE NOT EXISTS (
    SELECT 1
    FROM study_group sg
    WHERE sg.topic = 'CSDL'
      AND NOT EXISTS (
          SELECT 1
          FROM group_member gm
          WHERE gm.group_id = sg.group_id
            AND gm.user_id = u.user_id
      )
)
ORDER BY u.user_id;

-- Q4: Tìm các nhóm học tập có từ 3 thành viên trở lên
-- Kỹ thuật: GROUP BY, HAVING COUNT(*) >= 3 kết hợp JOIN.
-- Kết quả kỳ vọng trên seed_test: nhóm 1 có 4 thành viên.
EXPLAIN ANALYZE
SELECT sg.group_id, sg.name, COUNT(*) AS member_count
FROM study_group sg
JOIN group_member gm ON gm.group_id = sg.group_id
GROUP BY sg.group_id, sg.name
HAVING COUNT(*) >= 3
ORDER BY sg.group_id;

-- Q5: Thống kê số lượng bình luận của mỗi bài viết (kể cả bài chưa có bình luận)
-- Kỹ thuật: LEFT JOIN và COALESCE / COUNT(comment_id).
-- Kết quả kỳ vọng trên seed_test: post 1 = 4, post 2 = 1, post 3 = 0.
EXPLAIN ANALYZE
SELECT p.post_id, p.title, COUNT(c.comment_id) AS comment_count
FROM post p
LEFT JOIN comment c ON c.post_id = p.post_id
GROUP BY p.post_id, p.title
ORDER BY p.post_id;

-- Q6: Xếp hạng bài viết theo lượt thích (reaction) trong từng nhóm học tập
-- Kỹ thuật: Hàm cửa sổ (Window Function) RANK() OVER (PARTITION BY group_id ORDER BY likes DESC).
-- Kết quả kỳ vọng trên seed_test: post 1 hạng 1 ở nhóm 1, post 2 hạng 2.
EXPLAIN ANALYZE
WITH post_likes AS (
    SELECT p.post_id, p.group_id, p.title,
           COUNT(*) FILTER (WHERE pr.kind = 'like') AS like_count
    FROM post p
    LEFT JOIN post_reaction pr ON pr.post_id = p.post_id
    GROUP BY p.post_id, p.group_id, p.title
)
SELECT post_id, group_id, title, like_count,
       RANK() OVER (
           PARTITION BY group_id
           ORDER BY like_count DESC
       ) AS like_rank
FROM post_likes
ORDER BY group_id, like_rank, post_id;

-- Q7: Một yêu cầu nghiệp vụ viết bằng 3 cách khác nhau (IN, EXISTS, JOIN)
-- Kỹ thuật: So sánh Execution Plan và chi phí Buffer/Cost của 3 cách viết.
-- Yêu cầu: tìm bài viết thuộc nhóm mà tác giả là thành viên.
-- Kết quả kỳ vọng: cả ba cách đều trả về post 1, 2, 3.
EXPLAIN ANALYZE
SELECT p.post_id, p.title
FROM post p
WHERE p.author_id IN (
    SELECT gm.user_id
    FROM group_member gm
    WHERE gm.group_id = p.group_id
)
ORDER BY p.post_id;

EXPLAIN ANALYZE
SELECT p.post_id, p.title
FROM post p
WHERE EXISTS (
    SELECT 1
    FROM group_member gm
    WHERE gm.group_id = p.group_id
      AND gm.user_id = p.author_id
)
ORDER BY p.post_id;

EXPLAIN ANALYZE
SELECT DISTINCT p.post_id, p.title
FROM post p
JOIN group_member gm
  ON gm.group_id = p.group_id
 AND gm.user_id = p.author_id
ORDER BY p.post_id;

-- Q8: Tìm số lượng bạn chung giữa 2 người dùng bất kỳ
-- Kỹ thuật: Tự kết nối (Self-join) trên VIEW friend_edge.
-- Kết quả kỳ vọng với user 1 và 4: Binh (2) là 1 bạn chung.
EXPLAIN ANALYZE
WITH params AS (
    SELECT 1::INT AS user_1, 4::INT AS user_2
)
SELECT COUNT(DISTINCT f1.b) AS mutual_friend_count
FROM friend_edge f1
JOIN friend_edge f2 ON f2.b = f1.b
CROSS JOIN params
WHERE f1.a = params.user_1
  AND f2.a = params.user_2;
