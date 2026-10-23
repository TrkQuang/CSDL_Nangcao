-- ============================================================================
-- FILE: database/seed_test.sql
-- MỤC ĐÍCH: Bộ dữ liệu kiểm chứng nhỏ (Ground Truth Dataset) có đáp án tính tay.
--           Dùng để xác thực tính đúng đắn của TẤT CẢ các truy vấn cây (Q1-Q10),
--           truy vấn đệ quy đồ thị (R1-R4), và SQL nâng cao (Q1-Q12) trước khi đo đạc.
-- PHỤ TRÁCH: TV3 (Soạn thảo) & TV5 (Kiểm thử đối chiếu).
-- ============================================================================

-- Làm sạch dữ liệu cũ
TRUNCATE users, friendship, follow, study_group, group_member, post, post_reaction, comment, comment_path, comment_ns, comment_closure, folder RESTART IDENTITY CASCADE;

-- 1. Nạp người dùng (id 1..6)
-- Đồ thị bạn bè: An(1)-Binh(2), An(1)-Chi(3), Binh(2)-Chi(3), Binh(2)-Dung(4), Chi(3)-Em(5), Dung(4)-Em(5). Phong(6) cô lập.
INSERT INTO users(user_id, full_name, email) VALUES
    (1, 'An', 'an@sgu.vn'),
    (2, 'Binh', 'binh@sgu.vn'),
    (3, 'Chi', 'chi@sgu.vn'),
    (4, 'Dung', 'dung@sgu.vn'),
    (5, 'Em', 'em@sgu.vn'),
    (6, 'Phong', 'phong@sgu.vn');
SELECT setval('users_user_id_seq', 6);

-- 2. Nạp kết bạn (vô hướng: user_a < user_b)
-- Tam giác: (1,2,3); Chu trình 4: (2,3,5,4); Chu trình 5: (1,2,4,5,3)
INSERT INTO friendship(user_a, user_b) VALUES 
    (1, 2),
    (1, 3),
    (2, 3),
    (2, 4),
    (3, 5),
    (4, 5);

-- Cập nhật bộ đếm bạn bè ban đầu
UPDATE users u 
SET friend_count = (SELECT count(*) FROM friend_edge WHERE a = u.user_id);

-- 3. Nạp theo dõi (có hướng)
INSERT INTO follow(follower_id, followee_id) VALUES 
    (2, 1),
    (3, 1),
    (5, 1),
    (1, 4);

-- 4. Nhóm học tập
INSERT INTO study_group(group_id, name, topic, owner_id) VALUES 
    (1, 'CSDL nâng cao', 'CSDL', 1),
    (2, 'Lập trình Web', 'Web', 5);
SELECT setval('study_group_group_id_seq', 2);

-- 5. Thành viên nhóm
INSERT INTO group_member(group_id, user_id, role) VALUES
    (1, 1, 'owner'),
    (1, 2, 'member'),
    (1, 3, 'member'),
    (1, 4, 'member'),
    (2, 5, 'owner'),
    (2, 2, 'member');

-- 6. Bài viết
INSERT INTO post(post_id, group_id, author_id, post_type, title, content) VALUES
    (1, 1, 1, 'thaoluan', 'Ôn tập chuẩn hóa CSDL', 'Nội dung ôn tập 3NF, BCNF'),
    (2, 1, 2, 'tailieu', 'Slide bài giảng chương 5', 'Link download slide'),
    (3, 2, 5, 'thaoluan', 'Bài tập lớn Web', 'Thảo luận kiến trúc MVC');
SELECT setval('post_post_id_seq', 3);

-- 7. Cảm xúc bài viết
INSERT INTO post_reaction(post_id, user_id, kind) VALUES 
    (1, 2, 'like'),
    (1, 3, 'like'),
    (1, 4, 'like'),
    (2, 1, 'like'),
    (2, 3, 'like');

-- 8. Cây bình luận bài viết 1:
-- Cấu trúc cây: c1 (gốc) -> c2 (con c1) -> c3 (con c2); c4 (gốc thứ hai)
-- Cây bình luận bài 2: c5 (gốc)
INSERT INTO comment(comment_id, post_id, author_id, parent_id, content) VALUES
    (1, 1, 2, NULL, 'c1 - Bình luận gốc 1 bài 1'),
    (2, 1, 3, 1,    'c2 - Phản hồi c1'),
    (3, 1, 1, 2,    'c3 - Phản hồi c2'),
    (4, 1, 4, NULL, 'c4 - Bình luận gốc 2 bài 1'),
    (5, 2, 1, NULL, 'c5 - Bình luận gốc bài 2');
SELECT setval('comment_comment_id_seq', 5);

-- 9. Nạp cấu trúc cho 3 mô hình cây còn lại trên cùng dữ liệu bình luận:
-- Mô hình 2: Path Enumeration (ltree)
INSERT INTO comment_path(comment_id, post_id, path) VALUES
    (1, 1, '1'),
    (2, 1, '1.2'),
    (3, 1, '1.2.3'),
    (4, 1, '4'),
    (5, 2, '5');

-- Mô hình 3: Nested Set (lft, rgt)
INSERT INTO comment_ns(comment_id, post_id, lft, rgt) VALUES
    (1, 1, 1, 6),
    (2, 1, 2, 5),
    (3, 1, 3, 4),
    (4, 1, 7, 8),
    (5, 2, 1, 2);

-- Mô hình 4: Closure Table (ancestor, descendant, depth)
INSERT INTO comment_closure(ancestor, descendant, depth) VALUES
    (1, 1, 0), (1, 2, 1), (1, 3, 2),
    (2, 2, 0), (2, 3, 1),
    (3, 3, 0),
    (4, 4, 0),
    (5, 5, 0);

-- ============================================================================
-- ĐÁP ÁN TÍNH TAY KIỂM CHỨNG:
-- 1. Bạn của bạn (khoảng cách 2) của An(1): {Dung(4), Em(5)}
-- 2. Đường đi ngắn nhất An(1) -> Em(5): [1, 3, 5] (độ dài 2)
-- 3. Số chu trình đồ thị bạn bè: 3 chu trình (1-2-3, 2-3-5-4, 1-2-4-5-3)
-- 4. Gợi ý bạn bè cho An: Dung (1 bạn chung: Binh), Em (1 bạn chung: Chi)
-- 5. Cây bình luận bài 1:
--    - Hậu duệ của c1: {c1, c2, c3}
--    - Tổ tiên của c3: {c1, c2}
--    - Độ sâu của c3: 3
--    - Số nút trong cây con của c1: 3
-- ============================================================================
