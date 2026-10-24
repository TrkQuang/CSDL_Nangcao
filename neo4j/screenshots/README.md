# HƯỚNG DẪN CHỤP ẢNH TRỰC TIẾP TỪ NEO4J BROWSER & BẢNG GHI NHẬN

> **Mục đích:** Hướng dẫn thành viên nhóm chạy các câu truy vấn Cypher và chụp ảnh màn hình giao diện trực quan trực tiếp từ **Neo4j Browser** (`http://localhost:7474`), lưu bằng chứng thực tế vào thư mục `neo4j/screenshots/`.  
> **Người phụ trách:** TV4 (Chương) | Repository: `CSDL_Nangcao`.

---

## 1. Các Bước Thực Hiện Trên Neo4j Browser

### Bước 1: Khởi động Neo4j
- **Nếu dùng Docker:**
  ```bash
  docker run -d --name neo4j-detai17 -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password123 neo4j:5.18-community
  ```
- **Nếu dùng Neo4j Desktop:** Mở app, nhấn **Start** database DBMS, sau đó ấn nút **Open** (hoặc truy cập trình duyệt tại `http://localhost:7474`).
- **Đăng nhập:** User: `neo4j`, Password: `password123`.

### Bước 2: Nạp dữ liệu đồ thị (Import)
Copy toàn bộ nội dung file [import_nodes_edges.cypher](file:///d:/CSDL_Nangcao/neo4j/import/import_nodes_edges.cypher) dán vào thanh lệnh của Neo4j Browser và bấm **Run** (biểu tượng Play màu xanh):
```cypher
MATCH (n) DETACH DELETE n;
CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE;
CREATE (:User {id: 1, name: 'An', email: 'an@sgu.vn'});
CREATE (:User {id: 2, name: 'Binh', email: 'binh@sgu.vn'});
CREATE (:User {id: 3, name: 'Chi', email: 'chi@sgu.vn'});
CREATE (:User {id: 4, name: 'Dung', email: 'dung@sgu.vn'});
CREATE (:User {id: 5, name: 'Em', email: 'em@sgu.vn'});
CREATE (:User {id: 6, name: 'Phong', email: 'phong@sgu.vn'});
MATCH (a:User {id: 1}), (b:User {id: 2}) CREATE (a)-[:FRIEND]->(b);
MATCH (a:User {id: 1}), (c:User {id: 3}) CREATE (a)-[:FRIEND]->(c);
MATCH (b:User {id: 2}), (c:User {id: 3}) CREATE (b)-[:FRIEND]->(c);
MATCH (b:User {id: 2}), (d:User {id: 4}) CREATE (b)-[:FRIEND]->(d);
MATCH (c:User {id: 3}), (e:User {id: 5}) CREATE (c)-[:FRIEND]->(e);
MATCH (d:User {id: 4}), (e:User {id: 5}) CREATE (d)-[:FRIEND]->(e);
MATCH (b:User {id: 2}), (a:User {id: 1}) CREATE (b)-[:FOLLOWS]->(a);
MATCH (c:User {id: 3}), (a:User {id: 1}) CREATE (c)-[:FOLLOWS]->(a);
MATCH (e:User {id: 5}), (a:User {id: 1}) CREATE (e)-[:FOLLOWS]->(a);
MATCH (a:User {id: 1}), (d:User {id: 4}) CREATE (a)-[:FOLLOWS]->(d);
```

### Bước 3: Chạy 4 truy vấn và chụp ảnh màn hình
*(Lưu ý: Chuyển sang chế độ xem **Graph** (biểu tượng bong bóng đồ thị bên trái kết quả), chụp có cả dòng lệnh truy vấn và kết quả đồ thị trực quan)*

1. **Ảnh 1 - Toàn bộ đồ thị (`01_neo4j_full_graph.png`):**
   ```cypher
   MATCH (n)-[r]->(m) RETURN n, r, m;
   ```
2. **Ảnh 2 - Bạn của bạn R1 (`02_neo4j_friends_of_friends.png`):**
   ```cypher
   MATCH p = (an:User {name: 'An'})-[:FRIEND]-(mutual:User)-[:FRIEND]-(fof:User)
   WHERE fof <> an AND NOT (an)-[:FRIEND]-(fof)
   RETURN p;
   ```
3. **Ảnh 3 - Đường đi ngắn nhất R2 (`03_neo4j_shortest_path.png`):**
   ```cypher
   MATCH (an:User {name: 'An'}), (em:User {name: 'Em'})
   MATCH p = shortestPath((an)-[:FRIEND*..6]-(em))
   RETURN p;
   ```
4. **Ảnh 4 - Phát hiện chu trình R3 (`04_neo4j_cycle_detection.png`):**
   ```cypher
   MATCH p = (a:User)-[:FRIEND*3..5]-(a)
   WHERE ALL(n IN nodes(p)[1..-1] WHERE id(n) <> id(a))
     AND ALL(n IN nodes(p)[1..-1] WHERE a.id < n.id)
     AND (nodes(p)[1]).id < (nodes(p)[-2]).id
   RETURN p;
   ```

---

## 2. Bảng Ghi Nhận Kiểm Chứng Kết Quả (Đối Chiếu PostgreSQL)

| Tên file ảnh cần lưu | Đã chụp trực tiếp từ Browser? | Kết quả hiển thị trên đồ thị | Đối chiếu kết quả với PostgreSQL |
| :--- | :---: | :--- | :--- |
| `01_neo4j_full_graph.png` | **Chờ bạn chụp** | 6 Node User, 6 cạnh `:FRIEND`, 4 cạnh `:FOLLOWS` | Khớp 100% với dữ liệu bảng `users`, `friendship`, `follow` trong `seed_test.sql`. |
| `02_neo4j_friends_of_friends.png` | **Chờ bạn chụp** | An kết nối tới Dung (qua Binh) và Em (qua Chi) | Khớp 100% với câu đệ quy R1 `recursive_sql/friends_of_friends.sql`: `{Dung, Em}`. |
| `03_neo4j_shortest_path.png` | **Chờ bạn chụp** | Đường đi `An -> Chi -> Em` (độ dài 2) | Khớp 100% với câu đệ quy R2 `recursive_sql/shortest_path.sql`: `[1, 3, 5]` (độ dài 2). |
| `04_neo4j_cycle_detection.png` | **Chờ bạn chụp** | 3 chu trình khép kín: Tam giác `(1-2-3)`, Tứ giác `(2-3-5-4)`, Ngũ giác `(1-2-4-5-3)` | Khớp 100% với câu đệ quy R3 `recursive_sql/cycle_detection.sql`: 3 chu trình. |

---

> [!NOTE]
> Trong thời gian bạn chưa bật Neo4j Desktop, nhóm có thể dùng tạm 4 ảnh trực quan hóa đồ thị được mô phỏng chính xác bằng Python (`01_full_graph_visualization.png` .. `04_cycle_detection_visualization.png`). Khi bạn bật Neo4j Browser chụp xong, chỉ cần lưu đè với 4 tên file có tiền tố `0X_neo4j_...` vào thư mục này!
