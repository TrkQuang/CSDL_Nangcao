-- ============================================================================
-- FILE: normalization/mvd_4nf.sql
-- MỤC ĐÍCH: Minh họa và kiểm tra Phụ thuộc đa trị (Multi-valued Dependency - MVD)
--           và quá trình chuẩn hóa đạt Dạng chuẩn 4 (4NF).
-- PHỤ TRÁCH: TV1 (Lý thuyết) & TV3 (Hiện thực SQL).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [BỐI CẢNH LÝ THUYẾT]:
-- Giả sử xét quan hệ gộp: User_Skill_Hobby(user_id, skill, hobby)
-- Một người dùng có nhiều kỹ năng học tập (skill) và nhiều sở thích (hobby).
-- Kỹ năng và sở thích độc lập với nhau.
-- Khi đó xuất hiện MVD: 
--   user_id ->-> skill
--   user_id ->-> hobby
-- Bảng này ở 3NF/BCNF (khóa là toàn bộ thuộc tính) nhưng bị dư thừa dữ liệu (tích Descartes)
-- -> Vi phạm 4NF.
-- ----------------------------------------------------------------------------

-- [VÍ DỤ MẪU]: Bảng vi phạm 4NF (chưa tách MVD)
CREATE TABLE IF NOT EXISTS demo_user_skill_hobby_bad (
    user_id INT,
    skill   VARCHAR(50),
    hobby   VARCHAR(50),
    PRIMARY KEY (user_id, skill, hobby)
);

-- Khi user 1 có 2 kỹ năng (SQL, Python) và 2 sở thích (Đọc sách, Bơi lội):
-- Bảng phải lưu 2 x 2 = 4 dòng:
-- (1, 'SQL', 'Đọc sách'), (1, 'SQL', 'Bơi lội'), (1, 'Python', 'Đọc sách'), (1, 'Python', 'Bơi lội')

-- [GIẢI PHÁP 4NF]: Phân rã thành 2 quan hệ độc lập để đạt 4NF:
-- R1(user_id, skill)
-- R2(user_id, hobby)
CREATE TABLE IF NOT EXISTS demo_user_skill (
    user_id INT,
    skill   VARCHAR(50),
    PRIMARY KEY (user_id, skill)
);

CREATE TABLE IF NOT EXISTS demo_user_hobby (
    user_id INT,
    hobby   VARCHAR(50),
    PRIMARY KEY (user_id, hobby)
);

-- Số dòng lưu trữ giảm từ 4 xuống còn 2 + 2 = 4 (nếu N kỹ năng, M sở thích thì giảm từ N*M xuống N+M)
-- Triệt tiêu hoàn toàn dị thường cập nhật khi thêm một kỹ năng mới!
