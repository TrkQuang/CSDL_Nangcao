// ============================================================================
// FILE: neo4j/import/import_nodes_edges.cypher
// MỤC ĐÍCH: Nạp bộ dữ liệu đồ thị kiểm chứng nhỏ vào Neo4j tương ứng với seed_test.sql.
// PHỤ TRÁCH: TV4.
// ============================================================================

// Xóa sạch dữ liệu cũ
MATCH (n) DETACH DELETE n;

// Tạo chỉ mục & ràng buộc duy nhất trên User(id)
CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE;

// 1. Tạo 6 Node User
CREATE (:User {id: 1, name: 'An', email: 'an@sgu.vn'});
CREATE (:User {id: 2, name: 'Binh', email: 'binh@sgu.vn'});
CREATE (:User {id: 3, name: 'Chi', email: 'chi@sgu.vn'});
CREATE (:User {id: 4, name: 'Dung', email: 'dung@sgu.vn'});
CREATE (:User {id: 5, name: 'Em', email: 'em@sgu.vn'});
CREATE (:User {id: 6, name: 'Phong', email: 'phong@sgu.vn'});

// 2. Tạo các quan hệ FRIEND vô hướng (tạo 1 cạnh FRIEND giữa mỗi cặp)
MATCH (a:User {id: 1}), (b:User {id: 2}) CREATE (a)-[:FRIEND]->(b);
MATCH (a:User {id: 1}), (c:User {id: 3}) CREATE (a)-[:FRIEND]->(c);
MATCH (b:User {id: 2}), (c:User {id: 3}) CREATE (b)-[:FRIEND]->(c);
MATCH (b:User {id: 2}), (d:User {id: 4}) CREATE (b)-[:FRIEND]->(d);
MATCH (c:User {id: 3}), (e:User {id: 5}) CREATE (c)-[:FRIEND]->(e);
MATCH (d:User {id: 4}), (e:User {id: 5}) CREATE (d)-[:FRIEND]->(e);

// 3. Tạo các quan hệ FOLLOWS có hướng
MATCH (b:User {id: 2}), (a:User {id: 1}) CREATE (b)-[:FOLLOWS]->(a);
MATCH (c:User {id: 3}), (a:User {id: 1}) CREATE (c)-[:FOLLOWS]->(a);
MATCH (e:User {id: 5}), (a:User {id: 1}) CREATE (e)-[:FOLLOWS]->(a);
MATCH (a:User {id: 1}), (d:User {id: 4}) CREATE (a)-[:FOLLOWS]->(d);
