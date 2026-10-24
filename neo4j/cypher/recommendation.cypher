// ============================================================================
// FILE: neo4j/cypher/recommendation.cypher
// MỤC ĐÍCH: Gợi ý kết bạn (Friend Recommendation) cho An dựa trên số bạn chung (Mutual Friends).
// ĐỐI CHIẾU: Đối chiếu trực tiếp với recursive_sql/recommendation.sql (R4) của PostgreSQL.
// PHỤ TRÁCH: TV4 (Chương).
//
// KẾT QUẢ KỲ VỌNG TRÊN SEED_TEST:
//   - Dung (id = 4): 1 bạn chung (Binh)
//   - Em   (id = 5): 1 bạn chung (Chi)
// ============================================================================

MATCH (an:User {name: 'An'})-[:FRIEND]-(mutual:User)-[:FRIEND]-(candidate:User)
WHERE candidate <> an 
  AND NOT (an)-[:FRIEND]-(candidate)
RETURN candidate.id AS recommended_user_id,
       candidate.name AS recommended_user_name,
       count(DISTINCT mutual) AS mutual_friends_count,
       collect(DISTINCT mutual.name) AS mutual_friends
ORDER BY mutual_friends_count DESC, candidate.name ASC;

