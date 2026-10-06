-- ============================================================================
-- FILE: normalization/fd_check.sql
-- MỤC ĐÍCH: Dùng truy vấn SQL để kiểm chứng tính đúng đắn của Phụ thuộc hàm (FD)
--           hoặc phát hiện dữ liệu vi phạm FD trên cơ sở dữ liệu thực tế.
-- PHỤ TRÁCH: TV5 (chạy kiểm thử dữ liệu) & TV1 (phân tích nghiệp vụ).
-- ĐẦU VÀO: Bảng dữ liệu có sẵn trong database.
-- ĐẦU RA: Nếu truy vấn trả về 0 dòng -> Dữ liệu hiện tại thỏa mãn FD.
--         Nếu trả về > 0 dòng -> Phát hiện vi phạm FD.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU 1]: Kiểm chứng FD: user_id -> email
-- Nguyên tắc: Một user_id không được có từ 2 email khác nhau trở lên.
-- ----------------------------------------------------------------------------
SELECT 
    user_id, 
    COUNT(DISTINCT email) AS email_count
FROM users
GROUP BY user_id
HAVING COUNT(DISTINCT email) > 1;
-- Kỳ vọng: Trả về 0 dòng (Thỏa mãn FD)


-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU 2]: Kiểm chứng FD tình cờ (accidental FD): full_name -> email
-- Mục tiêu chứng minh rằng full_name KHÔNG THỂ suy ra email trong thế giới thực.
-- ----------------------------------------------------------------------------
SELECT 
    full_name, 
    COUNT(DISTINCT email) AS email_count
FROM users
GROUP BY full_name
HAVING COUNT(DISTINCT email) > 1;
-- Nhận xét: Trên bộ dữ liệu seed_test nhỏ có thể ra 0 dòng, nhưng nếu thêm 2 người 
-- cùng tên 'Nguyen Van A' với 2 email khác nhau thì sẽ trả về dòng vi phạm.


-- ----------------------------------------------------------------------------
-- [TODO: TV5 viết thêm các câu kiểm chứng tiếp theo]
-- 1. Kiểm chứng FD: post_id -> group_id, author_id
-- 2. Kiểm chứng FD: comment_id -> post_id, author_id
-- 3. Kiểm chứng FD: group_id -> owner_id
-- ----------------------------------------------------------------------------
