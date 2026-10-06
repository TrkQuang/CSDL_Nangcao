# ĐỐI CHIẾU CƠ SỞ DỮ LIỆU ĐỒ THỊ NEO4J & CYPHER

> **Mục đích thư mục:** Cài đặt, nạp dữ liệu và viết các câu truy vấn đồ thị bằng ngôn ngữ Cypher trên Neo4j để đối chiếu trực tiếp với giải pháp `WITH RECURSIVE` trên PostgreSQL.  
> **Người phụ trách:** TV4 (Hỗ trợ: TV3 | Review: TV5).

---

## 1. Khởi Động Neo4j Bằng Docker (Khuyến nghị)

```bash
docker run -d \
    --name neo4j-detai17 \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/password123 \
    neo4j:5.18-community
```
- Giao diện Neo4j Browser: `http://localhost:7474`
- Tài khoản: `neo4j`, Mật khẩu: `password123`

---

## 2. Bảng Đối Chiếu Mô Hình Dữ Liệu: PostgreSQL vs Neo4j

| Thành phần | PostgreSQL (RDBMS) | Neo4j (Graph Database) |
| :--- | :--- | :--- |
| **Thực thể người dùng** | Một dòng trong bảng `users` | Node có nhãn `(:User {id, name, email})` |
| **Kết bạn (vô hướng)** | Một dòng trong bảng `friendship` (user_a < user_b) | Relationship hai chiều hoặc không định hướng `[:FRIEND]` |
| **Theo dõi (có hướng)** | Một dòng trong bảng `follow` | Relationship có hướng `(:User)-[:FOLLOWS]->(:User)` |
| **Duyệt bạn của bạn** | `WITH RECURSIVE` duyệt view `friend_edge` | Biểu thức đường đi biến thiên: `(u)-[:FRIEND*2]-(fof)` |
| **Đường đi ngắn nhất** | Duyệt đệ quy BFS thủ công kèm mảng `path` | Hàm tích hợp sẵn: `shortestPath(...)` |

---

## 3. Thứ Tự Thực Hiện
1. Chạy file [import_nodes_edges.cypher](file:///c:/Users/shuut/Documents/CSDL_NC/neo4j/import/import_nodes_edges.cypher) để nạp 6 user và các cạnh bạn bè tương ứng [seed_test.sql](file:///c:/Users/shuut/Documents/CSDL_NC/database/seed_test.sql).
2. Chạy lần lượt các câu Cypher trong thư mục `cypher/` và ghi lại thời gian thực thi đối chiếu với PostgreSQL.
