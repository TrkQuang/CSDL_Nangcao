-- ============================================================================
-- FILE: recursive_sql/friends_of_friends.sql
-- MỤC ĐÍCH: Truy vấn Bạn của bạn (Friends-of-Friends - FoF) bằng WITH RECURSIVE.
--           Giới hạn độ sâu k bước, khử trùng lặp và loại bỏ chính bản thân.
-- PHỤ TRÁCH: TV3 (Hỗ trợ: TV4 | Kiểm chứng: TV2).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU R1]: Tìm bạn bè ở khoảng cách đúng 2 bước của An (user_id = 1)
-- Kết quả kỳ vọng trên seed_test: {Dung (4), Em (5)}
-- (Vì An kết bạn với Binh và Chi; Binh kết bạn Dung; Chi kết bạn Em)
-- ----------------------------------------------------------------------------
WITH RECURSIVE fof AS (
    -- Điểm neo: Bạn trực tiếp của An (độ sâu 1)
    SELECT 
        b AS friend_id, 
        1 AS depth, 
        ARRAY[1, b] AS path
    FROM friend_edge
    WHERE a = 1

    UNION ALL

    -- Bước đệ quy: Mở rộng sang bạn của bạn
    SELECT 
        fe.b AS friend_id, 
        f.depth + 1, 
        f.path || fe.b
    FROM friend_edge fe
    JOIN fof f ON fe.a = f.friend_id
    WHERE NOT (fe.b = ANY(f.path)) -- Chặn quay vòng về các nút đã đi qua
      AND f.depth < 2              -- Giới hạn độ sâu k = 2
)
SELECT DISTINCT 
    u.user_id, 
    u.full_name
FROM fof
JOIN users u ON fof.friend_id = u.user_id
WHERE fof.depth = 2 
  AND fof.friend_id <> 1
  -- Loại trừ những người ĐÃ LÀ BẠN TRỰC TIẾP của An
  AND fof.friend_id NOT IN (SELECT b FROM friend_edge WHERE a = 1);
