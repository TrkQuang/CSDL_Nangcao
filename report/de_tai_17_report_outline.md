# ĐỀ CƯƠNG BÁO CÁO ĐỒ ÁN 17 (20–30 TRANG)

> **Mục đích file:** Cấu trúc chi tiết của quyển Báo cáo đồ án tốt nghiệp môn CSDL Nâng cao.  
> **Người phụ trách tổng hợp:** TV1 (Toàn bộ nhóm đóng góp phần mình).  
> **Chuẩn đầu ra môn học:** Đáp ứng đầy đủ các chuẩn CLO1 đến CLO7.

---

## MỤC LỤC BÁO CÁO ĐỀ XUẤT

### LỜI MỞ ĐẦU
- Bối cảnh đề tài và lý do chọn ứng dụng Mạng xã hội học tập.
- Mục tiêu và câu hỏi nghiên cứu cốt lõi:
  1. Mô hình lưu trữ cây nào tối ưu nhất cho bài toán bình luận phân cấp trên RDBMS?
  2. SQL đệ quy (`WITH RECURSIVE`) trên RDBMS đáp ứng truy vấn đồ thị đến giới hạn nào khi so sánh với CSDL đồ thị chuyên dụng (Neo4j)?
  3. Lợi ích và đánh đổi của việc lưu trữ đối tượng (ODL/OQL) so với mô hình quan hệ (RDBMS)?

---

### CHƯƠNG 1: ĐẶC TẢ NGHIỆP VỤ & MÔ HÌNH HÓA DỮ LIỆU (CLO1, CLO2)
1.1 Đặc tả 10 quy tắc nghiệp vụ (**BR1 – BR10**) và cơ chế thực thi kỹ thuật.  
1.2 Mô hình thực thể kết hợp mở rộng (**EER**): Chuyên biệt hóa (Disjoint, Total), quan hệ đệ quy, thuộc tính dẫn xuất.  
1.3 Từ điển dữ liệu chi tiết.

---

### CHƯƠNG 2: PHỤ THUỘC HÀM & CHUẨN HÓA DỮ LIỆU (CLO2, CLO3)
2.1 Khảo sát các dị thường trên lược đồ tổng hợp ban đầu.  
2.2 Tập phụ thuộc hàm $F$ xuất phát từ nghiệp vụ (Phân biệt FD nghiệp vụ vs FD tình cờ).  
2.3 Thuật toán bao đóng thuộc tính, tìm tất cả khóa ứng viên.  
2.4 Thuật toán phủ tối tiểu $F_{min}$.  
2.5 Phân rã đạt chuẩn 3NF và BCNF (Chứng minh nối không mất thông tin và bảo toàn phụ thuộc hàm).  
2.6 Phụ thuộc đa trị (MVD) và dạng chuẩn 4NF.  
2.7 Kiểm chứng phụ thuộc hàm bằng SQL trên dữ liệu thực tế.

---

### CHƯƠNG 3: DỮ LIỆU PHÂN CẤP TRÊN HỆ CSDL QUAN HỆ (CLO4, CLO5)
3.1 Cơ sở lý thuyết 4 mô hình lưu trữ cây:
   - Adjacency List
   - Path Enumeration (`ltree`)
   - Nested Set (`lft`, `rgt`)
   - Closure Table
3.2 Hiện thực bộ 10 truy vấn chuẩn (**Q1 – Q10**) trên từng mô hình.  
3.3 Kiểm thử tính đúng đắn trên bộ dữ liệu kiểm chứng nhỏ ([seed_test.sql](file:///c:/Users/shuut/Documents/CSDL_NC/database/seed_test.sql)).

---

### CHƯƠNG 4: SQL NÂNG CAO, ĐỆ QUY ĐỒ THỊ & GIAO DỊCH (CLO4, CLO6)
4.1 Hiện thực 8 truy vấn SQL nâng cao (**Q1 – Q8**) và phân tích kế hoạch thực thi.  
4.2 Lập trình CSDL: Trigger kiểm tra cây (**Q9**), Stored Procedure kết bạn nguyên tử (**Q10**), Di chuyển nhánh chặn chu trình (**Q11**), SQL động và phòng chống SQL Injection (**Q12**).  
4.3 Truy vấn đệ quy trên đồ thị (**R1 – R4**): Bạn của bạn, Đường đi ngắn nhất, Phát hiện chu trình, Gợi ý kết bạn.  
4.4 Điều khiển đồng thời và Giao dịch:
   - Giao dịch T1 (Thành công), T2 (Rollback và Savepoint).
   - Thí nghiệm tương tranh T3: Deadlock và ma trận mức cô lập.
   - Thử tải đồng thời bằng `pgbench`.

---

### CHƯƠNG 5: ĐỐI CHIẾU MÔ HÌNH HƯỚNG ĐỐI TƯỢNG VÀ CSDL ĐỒ THỊ (CLO4)
5.1 Thiết kế 6 lớp đối tượng, lược đồ **ODL** và bộ truy vấn **OQL**.  
5.2 Ánh xạ sang **JPQL** và phân tích độ lệch pha trở kháng (Impedance Mismatch).  
5.3 Cài đặt đồ thị trên **Neo4j** và viết truy vấn **Cypher** đối chiếu với PostgreSQL.

---

### CHƯƠNG 6: THỰC NGHIỆM, BENCHMARK & ĐÁNH GIÁ HIỆU NĂNG (CLO5)
6.1 Thiết kế vật lý và chiến lược đánh chỉ mục.  
6.2 Kịch bản sinh dữ liệu (1.000, 10.000, 100.000 dòng).  
6.3 Kết quả đo đạc: Thời gian thực thi, I/O Buffer, dung lượng lưu trữ, chi phí ghi dữ liệu.  
6.4 Thảo luận kết quả, biểu đồ so sánh và khuyến nghị ứng dụng thực tế.

---

### KẾT LUẬN & HƯỚNG PHÁT TRIỂN
- Tóm tắt kết quả đạt được.
- Đóng góp của đề tài.
- Các hạn chế và hướng mở rộng.

---

### PHỤ LỤC & TÀI LIỆU THAM KHẢO
- Phụ lục A: Bảng phân công chi tiết và mức độ đóng góp (CLO7).
- Phụ lục B: Biên bản họp nhóm và nhật ký thực nghiệm.
