// ============================================================================
// FILE: neo4j/cypher/friends_of_friends.cypher
// MỤC ĐÍCH: Truy vấn Bạn của bạn (FoF) độ sâu 2 của An bằng Cypher.
// PHỤ TRÁCH: TV4.
// KẾT QUẢ KỲ VỌNG: Dung, Em
// ============================================================================

MATCH (an:User {name: 'An'})-[:FRIEND*2]-(fof:User)
WHERE fof <> an 
  AND NOT (an)-[:FRIEND]-(fof)
RETURN DISTINCT fof.id AS friend_of_friend_id, fof.name AS friend_of_friend_name;
