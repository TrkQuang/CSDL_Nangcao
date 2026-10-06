// ============================================================================
// FILE: neo4j/cypher/shortest_path.cypher
// MỤC ĐÍCH: Tìm đường đi ngắn nhất giữa An và Em bằng hàm shortestPath của Neo4j.
// PHỤ TRÁCH: TV4.
// KẾT QUẢ KỲ VỌNG: Đường đi [An, Chi, Em], độ dài 2.
// ============================================================================

MATCH p = shortestPath((an:User {name: 'An'})-[:FRIEND*..6]-(em:User {name: 'Em'}))
RETURN [n IN nodes(p) | n.name] AS path_names,
       length(p) AS path_length;
