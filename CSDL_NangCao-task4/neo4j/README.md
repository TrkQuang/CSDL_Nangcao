# ĐỐI CHIẾU CƠ SỞ DỮ LIỆU ĐỒ THỊ NEO4J & CYPHER

> **Mục đích:** Cài đặt, nạp dữ liệu và viết các câu truy vấn đồ thị bằng ngôn ngữ Cypher trên Neo4j để đối chiếu trực tiếp với giải pháp `WITH RECURSIVE` trên PostgreSQL (R1 - R4).  
> **Người phụ trách:** TV4 (Chương) | Hỗ trợ: TV3 (Hữu) | Review: TV5 (Quỳnh).

---

## 1. Khởi Động Neo4j Bằng Docker Hoặc Neo4j Desktop

### Cách 1: Sử dụng Docker (Khuyến nghị)
```bash
docker run -d \
    --name neo4j-detai17 \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/password123 \
    neo4j:5.18-community
```
- Giao diện Neo4j Browser: `http://localhost:7474`
- Tài khoản: `neo4j` | Mật khẩu: `password123`

### Cách 2: Sử dụng Neo4j Desktop
1. Tạo một DBMS mới (phiên bản Neo4j 5.x).
2. Đặt mật khẩu là `password123` và ấn **Start**.
3. Mở **Neo4j Browser** và paste các câu lệnh Cypher vào thanh lệnh.

---

## 2. Bảng Đối Chiếu Mô Hình Dữ Liệu: PostgreSQL vs Neo4j

| Thành phần | PostgreSQL (RDBMS) | Neo4j (Graph Database) |
| :--- | :--- | :--- |
| **Thực thể người dùng** | Một dòng trong bảng `users` | Node có nhãn `(:User {id, name, email})` |
| **Kết bạn (vô hướng)** | Một dòng trong bảng `friendship` (user_a < user_b) | Relationship `[:FRIEND]` (duyệt không định hướng) |
| **Theo dõi (có hướng)** | Một dòng trong bảng `follow` (follower -> followee) | Relationship có hướng `(:User)-[:FOLLOWS]->(:User)` |
| **Duyệt bạn của bạn (R1)** | `WITH RECURSIVE` duyệt qua view `friend_edge` (25 dòng) | Biểu thức đường đi ngắn gọn: `(u)-[:FRIEND*2]-(fof)` (4 dòng) |
| **Đường đi ngắn nhất (R2)** | Thuật toán BFS đệ quy thủ công kèm mảng `path_nodes` | Hàm tích hợp cực nhanh: `shortestPath(...)` |
| **Tìm chu trình (R3)** | Đệ quy theo dõi mảng đường đi, chặn hoán vị và đảo chiều | Mẫu đường đi khép kín: `(a)-[:FRIEND*3..5]-(a)` |
| **Gợi ý kết bạn (R4)** | Self-join qua view `friend_edge` và group by | Khớp mẫu qua nút trung gian `(u)-[:FRIEND]-(m)-[:FRIEND]-(c)` |

---

## 3. Thứ Tự Thực Hiện Chi Tiết

1. **Nạp dữ liệu:** Chạy file [import_nodes_edges.cypher](file:///c:/Users/shuut/Documents/CSDL_NC/neo4j/import/import_nodes_edges.cypher) để nạp 6 User và các quan hệ `:FRIEND`, `:FOLLOWS` tương ứng với bộ [seed_test.sql](file:///c:/Users/shuut/Documents/CSDL_NC/database/seed_test.sql).
2. **Thực thi các câu truy vấn Cypher đối chiếu:**
   - **R1 - Bạn của bạn:** [friends_of_friends.cypher](file:///c:/Users/shuut/Documents/CSDL_NC/neo4j/cypher/friends_of_friends.cypher) $\rightarrow$ Kết quả: `{Dung, Em}`.
   - **R2 - Đường đi ngắn nhất:** [shortest_path.cypher](file:///c:/Users/shuut/Documents/CSDL_NC/neo4j/cypher/shortest_path.cypher) $\rightarrow$ Kết quả: `[An, Chi, Em]` (độ dài 2).
   - **R3 - Phát hiện chu trình:** [cycle_detection.cypher](file:///c:/Users/shuut/Documents/CSDL_NC/neo4j/cypher/cycle_detection.cypher) $\rightarrow$ Kết quả: 3 chu trình `[1-2-3]`, `[2-3-5-4]`, `[1-2-4-5-3]`.
   - **R4 - Gợi ý kết bạn:** [recommendation.cypher](file:///c:/Users/shuut/Documents/CSDL_NC/neo4j/cypher/recommendation.cypher) $\rightarrow$ Kết quả: Dung (1 bạn chung), Em (1 bạn chung).
3. **Trực quan hóa đồ thị (Graph Visualization):**
   - Đã tạo sẵn 4 ảnh chụp màn hình trực quan trong thư mục [screenshots/](file:///c:/Users/shuut/Documents/CSDL_NC/neo4j/screenshots/).
   - Có thể chạy lại script vẽ đồ thị tự động:
     ```bash
     python neo4j/render_graph_visuals.py
     ```

---

## 4. Nhận Xét & Kết Luận So Sánh

1. **Về mặt cú pháp (Syntactic Elegance):**
   - Cypher sử dụng mô hình trực quan theo hình vẽ (ASCII art) như `(a)-[:FRIEND]->(b)`, giúp câu truy vấn đồ thị ngắn gọn hơn từ 3-5 lần so với cú pháp `WITH RECURSIVE` phức tạp của PostgreSQL.
2. **Về mặt thuật toán & Hiệu năng:**
   - Neo4j hỗ trợ cấu trúc **Index-free Adjacency** (mỗi đỉnh lưu trực tiếp con trỏ tới các đỉnh kề trong bộ nhớ), loại bỏ hoàn toàn chi phí Index Scan và Join bảng đắt đỏ của RDBMS.
   - Các thuật toán đồ thị chuyên dụng như `shortestPath` (Dijkstra/BFS) được tối ưu hóa ở tầng C++ / Java lõi, mang lại tốc độ vượt trội khi đồ thị mở rộng lên hàng triệu nút và cạnh.
