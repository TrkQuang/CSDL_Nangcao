-- ============================================================================
-- FILE: normalization/mvd_4nf.sql
-- ĐỀ TÀI: Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ (Mạng XH Học Tập)
-- MỤC ĐÍCH: Phân tích lý thuyết Phụ thuộc đa trị (Multi-valued Dependency - MVD),
--           chứng minh vi phạm Dạng chuẩn 4 (4NF) gây bùng nổ tích Descartes,
--           và hiện thực giải pháp phân rã chuẩn hóa 4NF bằng mã SQL hoàn chỉnh.
-- PHỤ TRÁCH: TV1 - Trần Quang (Lý thuyết & Thiết kế) & TV3 - Hữu (Hỗ trợ SQL)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. CƠ SỞ LÝ THUYẾT VỀ PHỤ THUỘC ĐA TRỊ (MVD) & DẠNG CHUẨN 4 (4NF)
-- ----------------------------------------------------------------------------
-- * Định nghĩa MVD:
--   Cho lược đồ quan hệ R và X, Y ⊆ R. Ta nói X phụ thuộc đa trị vào Y (ký hiệu: X ->-> Y)
--   nếu với mỗi cặp bộ t1, t2 trong r(R) thỏa mãn t1[X] = t2[X], thì tồn tại các bộ t3, t4
--   sao cho:
--     t3[X] = t4[X] = t1[X]
--     t3[Y] = t1[Y] và t4[Y] = t2[Y]
--     t3[R \ (XY)] = t2[R \ (XY)] và t4[R \ (XY)] = t1[R \ (XY)]
--
-- * Bối cảnh nghiệp vụ trong Mạng xã hội học tập:
--   Mỗi người dùng (user_id) có một tập hợp các sở thích học tập (interest: 'Python', 'Neo4j')
--   và một tập hợp các môn học quan tâm (subject: 'CSDL', 'Web').
--   Sở thích học tập và môn học quan tâm hoàn toàn ĐỘC LẬP với nhau (không có bất kỳ
--   ràng buộc nào nói rằng thích Python thì chỉ được học CSDL).
--   Do đó, xuất hiện hai phụ thuộc đa trị độc lập:
--     user_id ->-> interest
--     user_id ->-> subject
-- ----------------------------------------------------------------------------

-- Xóa bảng cũ nếu tồn tại để kịch bản chạy sạch
DROP TABLE IF EXISTS demo_user_profile_bad CASCADE;
DROP TABLE IF EXISTS user_interest CASCADE;
DROP TABLE IF EXISTS user_subject CASCADE;

-- ----------------------------------------------------------------------------
-- 2. BẢNG GỘP VI PHẠM 4NF (CHƯA TÁCH MVD)
-- ----------------------------------------------------------------------------
-- Trong bảng này, khóa chính bắt buộc phải là toàn bộ cả 3 thuộc tính: (user_id, interest, subject).
-- Bảng này đã đạt 1NF, 2NF, 3NF và thậm chí cả BCNF (vì không có FD không tầm thường nào),
-- nhưng lại VI PHẠM 4NF vì tồn tại MVD không tầm thường mà vế trái (user_id) không phải là siêu khóa!

CREATE TABLE demo_user_profile_bad (
    user_id  INT NOT NULL,
    interest VARCHAR(50) NOT NULL,
    subject  VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id, interest, subject)
);

-- Minh họa: User 1 có 2 sở thích ('Python', 'Neo4j') và 2 môn học ('CSDL', 'Web').
-- Để đảm bảo tính toàn vẹn của MVD, bảng bắt buộc phải lưu 2 x 2 = 4 dòng (Tích Descartes):
INSERT INTO demo_user_profile_bad (user_id, interest, subject) VALUES
(1, 'Python', 'CSDL'),
(1, 'Python', 'Web'),
(1, 'Neo4j',  'CSDL'),
(1, 'Neo4j',  'Web');

-- Hãy quan sát sự dư thừa:
-- Cặp ('Python', 'CSDL') và ('Python', 'Web') lặp lại 'Python' 2 lần!
-- Nếu một sinh viên có N = 10 sở thích và M = 10 môn học, bảng gộp phải lưu N x M = 100 dòng!
-- Dị thường cập nhật: Khi User 1 bổ sung thêm sở thích thứ 3 là 'Machine Learning', 
-- ta bắt buộc phải chèn thêm 2 dòng mới cho cả 2 môn học 'CSDL' và 'Web'.
-- Nếu chỉ chèn 1 dòng: (1, 'Machine Learning', 'CSDL') mà quên chèn (1, 'Machine Learning', 'Web'),
-- dữ liệu sẽ lập tức rơi vào trạng thái bất nhất quán (vi phạm định nghĩa MVD)!

SELECT '=== DỮ LIỆU BẢNG BỊ TÍCH DESCARTES (VI PHẠM 4NF) ===' AS title;
SELECT * FROM demo_user_profile_bad ORDER BY user_id, interest, subject;


-- ----------------------------------------------------------------------------
-- 3. GIẢI PHÁP CHUẨN HÓA ĐẠT DẠNG CHUẨN 4 (4NF DECOMPOSITION)
-- ----------------------------------------------------------------------------
-- Định lý Fagin: Phép tách R(X, Y, Z) thành R1(X, Y) và R2(X, Z) là bảo toàn thông tin 
-- (Lossless Join) khi và chỉ khi X ->-> Y hoặc X ->-> Z.
--
-- Ta phân rã demo_user_profile_bad thành 2 quan hệ độc lập:
--   R1: user_interest(user_id, interest) với PK (user_id, interest)
--   R2: user_subject(user_id, subject)   với PK (user_id, subject)

CREATE TABLE user_interest (
    user_id  INT NOT NULL,
    interest VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id, interest)
);

CREATE TABLE user_subject (
    user_id  INT NOT NULL,
    subject  VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id, subject)
);

-- Nạp dữ liệu vào 2 bảng đã chuẩn hóa:
INSERT INTO user_interest (user_id, interest) VALUES
(1, 'Python'),
(1, 'Neo4j');

INSERT INTO user_subject (user_id, subject) VALUES
(1, 'CSDL'),
(1, 'Web');

-- ----------------------------------------------------------------------------
-- 4. KIỂM TRÁC TÍNH BẢO TOÀN THÔNG TIN & ĐÁNH GIÁ HIỆU QUẢ LƯU TRỮ
-- ----------------------------------------------------------------------------

-- Số dòng lưu trữ:
-- Bảng gộp: 4 dòng
-- Bảng 4NF: 2 + 2 = 4 dòng (nhưng với N=10, M=10 thì bảng 4NF chỉ tốn 10 + 10 = 20 dòng, tiết kiệm 80% dung lượng!)
-- Khi thêm sở thích mới 'Machine Learning': Chỉ cần chèn ĐÚNG 1 DÒNG vào user_interest:
INSERT INTO user_interest (user_id, interest) VALUES (1, 'Machine Learning');

-- Chứng minh phép nối tự nhiên tái tạo lại chính xác dữ liệu tích Descartes ban đầu (Lossless):
SELECT '=== TÁI LẬP DỮ LIỆU TỰ NHIÊN TỪ 2 BẢNG 4NF ===' AS title;
SELECT 
    i.user_id, 
    i.interest, 
    s.subject
FROM user_interest i
JOIN user_subject s ON i.user_id = s.user_id
WHERE i.user_id = 1
ORDER BY i.interest, s.subject;

-- KẾT LUẬN:
-- Việc chuẩn hóa đạt 4NF đã triệt tiêu hoàn toàn sự lặp lại dữ liệu của tích Descartes,
-- loại bỏ dị thường cập nhật và giảm độ phức tạp khi người dùng thay đổi hồ sơ cá nhân.
