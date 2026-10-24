// ============================================================================
// FILE: neo4j/cypher/shortest_path.cypher
// MỤC ĐÍCH: Tìm đường đi ngắn nhất (Shortest Path) giữa An và Em bằng Cypher.
// ĐỐI CHIẾU: Đối chiếu trực tiếp với recursive_sql/shortest_path.sql (R2) của PostgreSQL.
// PHỤ TRÁCH: TV4 (Chương).
//
// KẾT QUẢ KỲ VỌNG TRÊN SEED_TEST:
//   - Đường đi ID:   [1, 3, 5]
//   - Đường đi Tên:  ['An', 'Chi', 'Em']
//   - Độ dài đường:  2 bước (hops)
// ============================================================================

// 1. Tìm đường đi ngắn nhất giữa An (id = 1) và Em (id = 5) qua quan hệ FRIEND vô hướng
MATCH (an:User {name: 'An'}), (em:User {name: 'Em'})
MATCH p = shortestPath((an)-[:FRIEND*..6]-(em))
RETURN [n IN nodes(p) | n.id] AS path_ids,
       [n IN nodes(p) | n.name] AS path_names,
       length(p) AS path_length;

// 2. Phiên bản tổng quát: Tìm tất cả các đường ngắn nhất (nếu có nhiều đường cùng độ dài ngắn nhất)
// MATCH (start:User {id: 1}), (target:User {id: 5})
// MATCH p = allShortestPaths((start)-[:FRIEND*..6]-(target))
// RETURN [n IN nodes(p) | n.name] AS shortest_path, length(p) AS length;
