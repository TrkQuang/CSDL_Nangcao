// ============================================================================
// FILE: neo4j/cypher/cycle_detection.cypher
// MỤC ĐÍCH: Phát hiện chu trình độ dài 3 đến 5 trong đồ thị bạn bè bằng Cypher.
// PHỤ TRÁCH: TV4.
// ============================================================================

// Tìm chu trình khép kín bắt đầu và kết thúc tại cùng một Node
MATCH p = (a:User)-[:FRIEND*3..5]-(a)
WITH [n IN nodes(p) | n.id] AS cycle_ids, length(p) AS len
RETURN DISTINCT cycle_ids, len
ORDER BY len;
