# DÀN Ý SLIDE THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN 17

> **Thời lượng thuyết trình:** 15 – 20 phút bảo vệ + 10 phút hỏi đáp Demo.  
> **Người phụ trách chuẩn bị:** Cả nhóm (TV1 tổng hợp).

---

## Cấu Trúc Các Slide (Khoảng 15 – 18 Slides)

1. **Slide 1: Trang tiêu đề**
   - Đề tài 17: Dữ liệu phân cấp và dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng mạng xã hội học tập
   - Giảng viên hướng dẫn & Danh sách thành viên (TV1 – TV5).
2. **Slide 2: Đặt vấn đề & Câu hỏi nghiên cứu**
   - Sự bùng nổ của dữ liệu dạng cây (bình luận, thư mục) và đồ thị (mạng lưới bạn bè).
   - Thách thức khi lưu trữ trên RDBMS truyền thống và hướng giải quyết.
3. **Slide 3: Đặc tả nghiệp vụ & Mô hình EER**
   - 10 quy tắc nghiệp vụ then chốt (BR1–BR10).
   - Sơ đồ EER với quan hệ đệ quy và chuyên biệt hóa.
4. **Slide 4: Phụ thuộc hàm & Chuẩn hóa dữ liệu**
   - Quá trình tìm bao đóng, phủ tối tiểu, phân rã 3NF / BCNF.
   - Minh chứng bảo toàn thông tin và phụ thuộc hàm.
5. **Slide 5: So sánh 4 mô hình lưu trữ cây trên RDBMS**
   - Trực quan hóa cấu trúc: Adjacency List, ltree, Nested Set, Closure Table.
   - Bảng đánh đổi lý thuyết (Trade-offs: Read vs Write vs Storage).
6. **Slide 6: Bộ 10 truy vấn cây (Q1 – Q10) & Tính đúng đắn**
   - Minh chứng cả 4 mô hình cho cùng kết quả trên bộ dữ liệu kiểm chứng.
7. **Slide 7: SQL nâng cao & Lập trình CSDL**
   - Điểm nhấn về Trigger kiểm tra cây, Stored Procedure kết bạn nguyên tử, Dynamic SQL chống injection.
8. **Slide 8: Truy vấn đệ quy trên đồ thị (WITH RECURSIVE)**
   - Bạn của bạn (FoF), Đường đi ngắn nhất (BFS), Phát hiện chu trình, Gợi ý bạn bè.
9. **Slide 9: Điều khiển đồng thời & Giao dịch**
   - Thí nghiệm tương tranh giữa 2 phiên: Bế tắc (Deadlock mã 40P01) và mức cô lập.
   - Biểu đồ thử tải bằng `pgbench`.
10. **Slide 10: Đối chiếu CSDL hướng đối tượng (ODL/OQL/JPQL)**
    - Thiết kế 6 lớp và bài toán lệch pha trở kháng (Impedance Mismatch).
11. **Slide 11: Đối chiếu CSDL đồ thị Neo4j & Cypher**
    - So sánh cú pháp Cypher trực quan vs WITH RECURSIVE của PostgreSQL.
12. **Slide 12: Thiết kế vật lý & Chiến lược Indexing**
    - Đánh giá các loại chỉ mục: B-tree, GiST ltree, Composite Index.
13. **Slide 13: Kết quả thực nghiệm & Benchmark**
    - Biểu đồ thời gian thực thi của 4 mô hình cây trên các quy mô 1k, 10k, 100k nodes.
    - So sánh thời gian truy vấn đồ thị: PostgreSQL vs Neo4j.
14. **Slide 14: Demo kịch bản thực tế**
    - Trình diễn trực tiếp trên Terminal / PgAdmin / Neo4j Browser.
15. **Slide 15: Kết luận & Bài học kinh nghiệm**
    - Tóm tắt câu trả lời cho các câu hỏi nghiên cứu ban đầu.
16. **Slide 16: Hỏi đáp (Q&A)**
