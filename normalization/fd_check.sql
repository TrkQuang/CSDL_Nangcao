-- ============================================================================
-- FILE: normalization/fd_check.sql
-- ĐỀ TÀI: Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ (Mạng XH Học Tập)
-- MỤC ĐÍCH: Dùng truy vấn SQL để kiểm chứng tính đúng đắn của Phụ thuộc hàm (FD)
--           hoặc phát hiện dữ liệu vi phạm FD trên cơ sở dữ liệu thực tế.
-- PHỤ TRÁCH: TV1 - Trần Quang (Xây dựng câu hỏi & Lập luận) & TV5 - Quỳnh (Thực thi kiểm chứng)
-- NGUYÊN TẮC:
--   Nếu truy vấn trả về 0 dòng  -> Dữ liệu hiện tại thỏa mãn phụ thuộc hàm.
--   Nếu truy vấn trả về >= 1 dòng -> Phát hiện vi phạm tính phụ thuộc hàm (hoặc tìm ra phản ví dụ).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. KIỂM CHỨNG CÁC PHỤ THUỘC HÀM HỢP LỆ THEO NGHIỆP VỤ (FD1 - FD5)
-- ----------------------------------------------------------------------------

-- [FD1.1]: user_id -> email
-- Ý nghĩa: Mỗi user_id chỉ được liên kết với duy nhất 1 địa chỉ email.
SELECT 
    'FD1.1 (user_id -> email)' AS test_name,
    user_id, 
    COUNT(DISTINCT email) AS distinct_emails
FROM users
GROUP BY user_id
HAVING COUNT(DISTINCT email) > 1;
-- Kỳ vọng: 0 dòng.

-- [FD1.2]: email -> user_id (Quy tắc BR1: Email là duy nhất)
SELECT 
    'FD1.2 (email -> user_id)' AS test_name,
    email, 
    COUNT(DISTINCT user_id) AS distinct_users
FROM users
GROUP BY email
HAVING COUNT(DISTINCT user_id) > 1;
-- Kỳ vọng: 0 dòng.

-- [FD2]: post_id -> group_id, author_id, post_type
-- Ý nghĩa: Mỗi bài viết chỉ thuộc về đúng 1 nhóm học tập và 1 tác giả.
SELECT 
    'FD2 (post_id -> group_id, author_id)' AS test_name,
    post_id, 
    COUNT(DISTINCT group_id) AS distinct_groups,
    COUNT(DISTINCT author_id) AS distinct_authors
FROM post
GROUP BY post_id
HAVING COUNT(DISTINCT group_id) > 1 OR COUNT(DISTINCT author_id) > 1;
-- Kỳ vọng: 0 dòng.

-- [FD3]: group_id -> name, topic, owner_id
-- Ý nghĩa: Mỗi nhóm chỉ có duy nhất 1 tên nhóm, 1 chủ đề và 1 chủ nhóm.
SELECT 
    'FD3 (group_id -> name, topic, owner_id)' AS test_name,
    group_id, 
    COUNT(DISTINCT name) AS distinct_names,
    COUNT(DISTINCT owner_id) AS distinct_owners
FROM study_group
GROUP BY group_id
HAVING COUNT(DISTINCT name) > 1 OR COUNT(DISTINCT owner_id) > 1;
-- Kỳ vọng: 0 dòng.

-- [FD4]: comment_id -> post_id, author_id, parent_id
-- Ý nghĩa: Mỗi bình luận chỉ nằm trong đúng 1 bài viết và do 1 người viết.
SELECT 
    'FD4 (comment_id -> post_id, author_id)' AS test_name,
    comment_id, 
    COUNT(DISTINCT post_id) AS distinct_posts,
    COUNT(DISTINCT author_id) AS distinct_authors
FROM comment
GROUP BY comment_id
HAVING COUNT(DISTINCT post_id) > 1 OR COUNT(DISTINCT author_id) > 1;
-- Kỳ vọng: 0 dòng.


-- ----------------------------------------------------------------------------
-- 2. KIỂM CHỨNG PHỤ THUỘC HÀM TÌNH CỜ (ACCIDENTAL FD - SAI NGHIỆP VỤ)
-- ----------------------------------------------------------------------------

-- [FD Tình cờ 1]: full_name -> email
-- Nghiệp vụ thực tế cho phép nhiều người trùng họ tên.
-- Trên tập dữ liệu seed_test ban đầu (An, Binh, Chi...), kết quả có thể ra 0 dòng.
-- Truy vấn sau giúp kiểm tra xem hiện tại đã có hai người trùng tên hay chưa:
SELECT 
    'Accidental FD (full_name -> email)' AS test_name,
    full_name, 
    COUNT(DISTINCT email) AS email_count
FROM users
GROUP BY full_name
HAVING COUNT(DISTINCT email) > 1;
-- Nhận xét: Dù truy vấn này có trả về 0 dòng thì cũng KHÔNG THỂ coi full_name -> email là FD hợp lệ!

-- [FD Tình cờ 2]: name -> group_id (Tên nhóm xác định mã nhóm)
SELECT 
    'Accidental FD (group_name -> group_id)' AS test_name,
    name, 
    COUNT(DISTINCT group_id) AS group_count
FROM study_group
GROUP BY name
HAVING COUNT(DISTINCT group_id) > 1;


-- ----------------------------------------------------------------------------
-- 3. KIỂM TRA TÍNH TOÀN VẸN CỦA CÁC RÀNG BUỘC NGHIỆP VỤ ĐẶC BIỆT
-- ----------------------------------------------------------------------------

-- [Kiểm tra BR6]: Bình luận cha và con phải cùng bài viết (post_id)
SELECT 
    'BR6 Check (Parent and Child post_id match)' AS test_name,
    c.comment_id AS child_id,
    c.post_id AS child_post_id,
    p.comment_id AS parent_id,
    p.post_id AS parent_post_id
FROM comment c
JOIN comment p ON c.parent_id = p.comment_id
WHERE c.post_id <> p.post_id;
-- Kỳ vọng: 0 dòng (Nếu > 0 dòng: Vi phạm tính toàn vẹn cây bình luận).

-- [Kiểm tra BR2]: Cặp bạn bè phải tuân thủ user_a < user_b
SELECT 
    'BR2 Check (Friendship user_a < user_b)' AS test_name,
    user_a, 
    user_b
FROM friendship
WHERE user_a >= user_b;
-- Kỳ vọng: 0 dòng.

-- [Kiểm tra BR9]: Đồng bộ friend_count trên bảng users với bảng friendship
SELECT 
    'BR9 Check (users.friend_count sync with friendship)' AS test_name,
    u.user_id,
    u.friend_count AS stored_count,
    COUNT(e.b) AS calculated_count
FROM users u
LEFT JOIN friend_edge e ON u.user_id = e.a
GROUP BY u.user_id, u.friend_count
HAVING u.friend_count <> COUNT(e.b);
-- Kỳ vọng: 0 dòng (Nếu > 0 dòng: Bộ đếm dẫn xuất bị lệch pha).
