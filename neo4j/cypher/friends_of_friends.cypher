// ============================================================================
// FILE: neo4j/cypher/friends_of_friends.cypher
// MỤC ĐÍCH: Truy vấn Bạn của bạn (Friends-of-Friends - FoF) độ sâu k = 2 của An.
// ĐỐI CHIẾU: Đối chiếu trực tiếp với recursive_sql/friends_of_friends.sql (R1) của PostgreSQL.
// PHỤ TRÁCH: TV4 (Chương).
//
// KẾT QUẢ KỲ VỌNG TRÊN SEED_TEST:
//   - Dung (id = 4) qua bạn trung gian Binh (id = 2)
//   - Em (id = 5) qua bạn trung gian Chi (id = 3)
// ============================================================================

MATCH (an:User {name: 'An'})-[:FRIEND]-(mutual:User)-[:FRIEND]-(fof:User)
WHERE fof <> an 
  AND NOT (an)-[:FRIEND]-(fof)
RETURN DISTINCT fof.id AS friend_of_friend_id,
       fof.name AS friend_of_friend_name,
       collect(DISTINCT mutual.name) AS connected_via
ORDER BY fof.id;
