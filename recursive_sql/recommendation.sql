-- ============================================================================
-- FILE: recursive_sql/recommendation.sql
-- MỤC ĐÍCH: Gợi ý kết bạn (Friend Recommendation) dựa trên số lượng bạn chung
--           (Mutual Friends Count), sắp xếp giảm dần theo mức độ tương đồng.
-- PHỤ TRÁCH: TV3.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU R4]: Gợi ý kết bạn cho An (user_id = 1)
-- Kết quả kỳ vọng trên seed_test:
--   - Dung (id = 4): 1 bạn chung (Binh)
--   - Em (id = 5): 1 bạn chung (Chi)
-- ----------------------------------------------------------------------------
SELECT 
    c.user_id AS recommended_user_id,
    c.full_name AS recommended_user_name,
    COUNT(DISTINCT m.b) AS mutual_friends_count
FROM friend_edge an_friends       -- Bạn trực tiếp của An (m)
JOIN friend_edge candidate_friends -- Bạn của bạn (c)
  ON an_friends.b = candidate_friends.a
JOIN users c 
  ON candidate_friends.b = c.user_id
JOIN friend_edge m 
  ON m.a = 1 AND m.b = candidate_friends.a
WHERE an_friends.a = 1
  AND candidate_friends.b <> 1  -- Không tự gợi ý chính mình
  -- Chưa phải là bạn trực tiếp của An
  AND candidate_friends.b NOT IN (SELECT b FROM friend_edge WHERE a = 1)
GROUP BY c.user_id, c.full_name
ORDER BY mutual_friends_count DESC, c.full_name ASC;
