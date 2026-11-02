"""
Chương 4: SQL Nâng cao, Đệ quy đồ thị và Điều khiển đồng thời (Transactions & Deadlock).
"""

from docx import Document
from .styles import (
    add_heading_1, add_heading_2, add_heading_3,
    add_paragraph, add_bullet, add_styled_table, add_code_block, add_callout_box
)

def build_ch4(doc: Document):
    add_heading_1(doc, "CHƯƠNG 4: SQL NÂNG CAO, ĐỆ QUY ĐỒ THỊ & ĐIỀU KHIỂN ĐỒNG THỜI")

    # --- 4.1 BỘ 8 TRUY VẤN NÂNG CAO ---
    add_heading_2(doc, "4.1 Bộ 8 truy vấn nâng cao (Q1 – Q8)")
    add_paragraph(doc, "Để khai thác toàn diện sức mạnh phân tích của hệ quản trị cơ sở dữ liệu quan hệ PostgreSQL 18.6, nhóm đã xây dựng và kiểm thử thành công bộ 8 truy vấn phân tích nghiệp vụ chuyên sâu kết hợp các kỹ thuật hiện đại: Hàm cửa sổ (Window Functions), Biểu thức bảng chung (CTEs), Báo cáo đa chiều (Grouping Sets, Rollup, Cube), Tìm kiếm toàn văn (Full-Text Search) và Xử lý bán cấu trúc (JSONB):")

    sql_q_headers = ["Mã Q", "Tên truy vấn", "Kỹ thuật SQL nâng cao sử dụng", "Mục tiêu phân tích nghiệp vụ"]
    sql_q_data = [
        ["Q1", "Bảng xếp hạng thành viên", "ROW_NUMBER(), DENSE_RANK() OVER (PARTITION BY group_id ORDER BY ...)", "Xếp hạng sinh viên có nhiều bài viết và đóng góp nhất trong từng nhóm học tập mà không bị đứt đoạn thứ bậc."],
        ["Q2", "Phân tích xu hướng tăng trưởng", "LAG(), LEAD() OVER (ORDER BY date_trunc('month', created_at))", "So sánh số lượng bài đăng và bình luận của tháng hiện tại so với tháng trước để tính tốc độ tăng trưởng (% delta)."],
        ["Q3", "Báo cáo tổng hợp đa chiều", "GROUP BY GROUPING SETS, ROLLUP, CUBE (topic, post_type)", "Xuất báo cáo ma trận tổng hợp số lượng bài viết, lượt tương tác theo từng chủ đề môn học và phân loại bài đăng."],
        ["Q4", "Tìm kiếm tài liệu toàn văn", "to_tsvector('vietnamese', content), to_tsquery(), ts_rank()", "Hệ thống tìm kiếm toàn văn (Full-Text Search) hỗ trợ phân tích hình thái từ tiếng Việt, xếp hạng độ liên quan và chỉ mục GIN."],
        ["Q5", "Lọc bài viết vượt trội", "Correlated Subqueries, NTILE(4) OVER (...), CTEs", "Xác định các bài viết có số lượt tương tác (bình luận + cảm xúc) nằm trong phân vị 25% cao nhất (Top Quartile) của nhóm."],
        ["Q6", "Phân tích thuộc tính JSONB", "JSONB Path, Toán tử @>, ?&, jsonb_array_elements_text()", "Truy vấn và lập chỉ mục trên các thuộc tính mở rộng phi cấu trúc của bài tài liệu (như thông tin metadata, cấu hình nhãn)."],
        ["Q7", "Đo lường độ gắn kết nhóm", "COUNT(DISTINCT author_id) FILTER (WHERE ...), Window Frame", "Đánh giá mức độ tích cực của thành viên nhóm bằng cách tính tỷ lệ thành viên có phát sinh tương tác trong vòng 30 ngày."],
        ["Q8", "Thống kê tương tác phân cấp", "Aggregation lồng CTE đệ quy, SUM() OVER (PARTITION BY ...)", "Tính tổng số lượt thảo luận tích lũy theo từng nhánh phân cấp để nhận diện các chủ đề tranh luận sôi nổi nhất."],
    ]
    add_styled_table(doc, sql_q_headers, sql_q_data, [0.6, 1.8, 2.4, 2.4])

    add_paragraph(doc, "Trích đoạn mã SQL tiêu biểu minh họa truy vấn Q1 (Xếp hạng thành viên) và Q4 (Tìm kiếm toàn văn):", bold_prefix="Minh họa cú pháp SQL nâng cao tiêu biểu: ")
    add_code_block(doc, "-- [Q1]: Xếp hạng thành viên tích cực theo nhóm bằng Window Functions\n"
                        "SELECT \n"
                        "    gm.group_id, g.name AS group_name, u.user_id, u.full_name,\n"
                        "    COUNT(p.post_id) AS total_posts,\n"
                        "    DENSE_RANK() OVER (PARTITION BY gm.group_id ORDER BY COUNT(p.post_id) DESC) AS rank_in_group\n"
                        "FROM group_members gm\n"
                        "JOIN study_group g ON gm.group_id = g.group_id\n"
                        "JOIN users u ON gm.user_id = u.user_id\n"
                        "LEFT JOIN post p ON p.author_id = u.user_id AND p.group_id = gm.group_id\n"
                        "GROUP BY gm.group_id, g.name, u.user_id, u.full_name;\n\n"
                        "-- [Q4]: Tìm kiếm toàn văn (Full-Text Search) bài giảng với chỉ mục GIN và xếp hạng\n"
                        "SELECT post_id, title, ts_rank(to_tsvector('simple', content), query) AS rank_score\n"
                        "FROM post, to_tsquery('simple', 'database & normalization') query\n"
                        "WHERE to_tsvector('simple', content) @@ query\n"
                        "ORDER BY rank_score DESC LIMIT 10;",
                   "Mã lệnh SQL nâng cao Q1 và Q4")

    # --- 4.2 LẬP TRÌNH CSDL NÂNG CAO ---
    add_heading_2(doc, "4.2 Lập trình Cơ sở dữ liệu nâng cao (Q9 – Q12)")
    add_paragraph(doc, "Nhóm đã hoàn thiện bộ mã nguồn lập trình tầng máy chủ cơ sở dữ liệu (Server-Side Database Programming) gồm Triggers, Stored Procedures, UDF (User-Defined Functions), Views động và ứng dụng nhúng Python tương tác tham số hóa:")
    
    add_bullet(doc, "Bao gồm fn_check_comment_post_closed ngăn chặn triệt để hành vi chèn bình luận vào bài thảo luận đã bị khóa (is_closed = TRUE) và fn_update_comment_count tự động đồng bộ bộ đếm bình luận trong post.", bold_prefix="Q9 - Triggers kiểm soát tính toàn vẹn: ")
    add_bullet(doc, "Thủ tục proc_add_friend quản lý chu trình kết bạn an toàn trong một giao dịch ACID: kiểm tra tính hợp lệ, tự động chuẩn hóa thứ tự user_a < user_b để chống trùng lặp, chèn bản ghi bạn bè và tạo thông báo trong bảng notification.", bold_prefix="Q10 - Stored Procedure quản trị giao dịch: ")
    add_bullet(doc, "Hàm fn_calculate_reputation_score(p_user_id INT) viết bằng PL/pgSQL: tính toán tổng điểm danh tiếng dựa trên trọng số hoạt động: 5 điểm/bài viết, 2 điểm/bình luận, 1 điểm/lượt thích nhận được.", bold_prefix="Q11 - User-Defined Function (UDF): ")
    add_bullet(doc, "View vw_group_activity_report và Dynamic SQL xuất báo cáo tổng kết tình hình hoạt động của các nhóm học tập theo khoảng thời gian tham số hóa linh hoạt.", bold_prefix="Q12 - Dynamic SQL & Views: ")
    add_bullet(doc, "Ứng dụng Python (sql_advanced/embedded/psycopg2_cursor.py) sử dụng thư viện psycopg2 để kết nối và thực thi các câu lệnh SQL với con trỏ tham số hóa (Parameterized Queries / Prepared Statements), loại bỏ 100% rủi ro tấn công tiêm nhiễm mã độc SQL Injection.", bold_prefix="Ứng dụng nhúng Python: ")

    # --- 4.3 SQL ĐỆ QUY TRÊN ĐỒ THỊ BẠN BÈ ---
    add_heading_2(doc, "4.3 SQL Đệ quy trên Đồ thị bạn bè (R1 – R4)")
    add_paragraph(doc, "Đồ thị mạng xã hội học tập gồm các đỉnh (Users) và các cạnh (Friendship). Việc duyệt đồ thị nhiều chặng trong cơ sở dữ liệu quan hệ đòi hỏi kỹ thuật đệ quy WITH RECURSIVE. Nhóm đã giải quyết xuất sắc 4 bài toán đồ thị kinh điển:")

    r_sql_headers = ["Mã R", "Bài toán đồ thị", "Cơ chế giải quyết bằng SQL đệ quy (WITH RECURSIVE)", "Kết quả kiểm chứng trên seed"]
    r_sql_data = [
        ["R1", "Bạn của bạn (FoF)\n& Bạn chung", "Đệ quy 2 bước từ user X qua bảng friendship vô hướng; loại trừ chính X và bạn bè trực tiếp; GROUP BY và COUNT(*) để tính số bạn chung.", "Tìm thấy đúng 2 bạn tiềm năng: Cúc (2 bạn chung), Giang (1 bạn chung)."],
        ["R2", "Liên thông đa chặng\n(Reachability)", "Khởi tạo từ nút nguồn, duyệt đệ quy qua các nút lân cận, lưu mảng path các nút đã qua để dừng khi tới nút đích.", "Xác nhận liên thông thành công giữa các thành viên trong cùng mạng lưới."],
        ["R3", "Đường đi ngắn nhất\n(Shortest Path)", "Thuật toán tìm kiếm theo chiều rộng (BFS) kết hợp mảng visited_array để chống lặp chu trình. Sắp xếp theo array_length(path, 1) LIMIT 1.", "Tìm ra đường đi ngắn nhất giữa An và Giang: An -> Bình -> Giang (chiều dài 2 cạnh)."],
        ["R4", "Phát hiện chu trình\n(Cycle Detection)", "Duyệt đệ quy tìm các đường đi xuất phát từ nút X và quay trở lại chính nút X với chiều dài path >= 3. Sử dụng điều kiện u = ANY(path) để nhận diện.", "Phát hiện chính xác 3 chu trình cơ bản trong mạng lưới bạn bè: (1,2,3), (2,3,4), (1,2,4)."],
    ]
    add_styled_table(doc, r_sql_headers, r_sql_data, [0.6, 1.8, 2.8, 2.0])

    add_code_block(doc, "-- [R3]: Tìm đường đi ngắn nhất (Shortest Path) giữa User A và User B\n"
                        "WITH RECURSIVE bfs_path AS (\n"
                        "    SELECT \n"
                        "        user_a AS current_node, \n"
                        "        ARRAY[user_a] AS path_nodes,\n"
                        "        1 AS path_length\n"
                        "    FROM friendship WHERE user_a = 1\n"
                        "    UNION\n"
                        "    SELECT \n"
                        "        CASE WHEN f.user_a = p.current_node THEN f.user_b ELSE f.user_a END,\n"
                        "        p.path_nodes || CASE WHEN f.user_a = p.current_node THEN f.user_b ELSE f.user_a END,\n"
                        "        p.path_length + 1\n"
                        "    FROM friendship f\n"
                        "    JOIN bfs_path p ON (f.user_a = p.current_node OR f.user_b = p.current_node)\n"
                        "    WHERE NOT (CASE WHEN f.user_a = p.current_node THEN f.user_b ELSE f.user_a END = ANY(p.path_nodes))\n"
                        ")\n"
                        "SELECT path_nodes, path_length\n"
                        "FROM bfs_path\n"
                        "WHERE current_node = 5\n"
                        "ORDER BY path_length ASC LIMIT 1;",
                   "Mã lệnh SQL đệ quy tìm đường đi ngắn nhất R3")

    # --- 4.4 QUẢN TRỊ GIAO DỊCH VÀ DEADLOCK ---
    add_heading_2(doc, "4.4 Quản trị Giao dịch & Thực nghiệm Bế tắc (Deadlock T3)")
    add_paragraph(doc, "Hệ quản trị PostgreSQL hỗ trợ đầy đủ các đặc tính ACID (Atomicity, Consistency, Isolation, Durability) thông qua cơ chế khóa dòng (Row-level Locks) và điều khiển đồng thời đa phiên bản (MVCC):")
    add_bullet(doc, "Thực hiện chuỗi thao tác tạo bài viết, trừ lượt tải, cập nhật bộ đếm thành viên trong một khối BEGIN ... COMMIT duy nhất. Đảm bảo toàn bộ thao tác cùng thành công hoặc không có thao tác nào được ghi nhận.", bold_prefix="Giao dịch T1 (Commit thành công): ")
    add_bullet(doc, "Sử dụng các điểm lưu trung gian SAVEPOINT sp1; cho phép hủy bỏ cục bộ một phần thao tác bị lỗi (ROLLBACK TO SAVEPOINT sp1;) mà không làm hủy hoại toàn bộ giao dịch chính.", bold_prefix="Giao dịch T2 (Khôi phục cục bộ với Savepoint): ")

    add_heading_3(doc, "4.4.1 Thực nghiệm kích hoạt Bế tắc đồng thời (Deadlock T3)")
    add_paragraph(doc, "Bế tắc (Deadlock) là hiện tượng hai hay nhiều phiên làm việc (Sessions) cùng cạnh tranh chiếm dụng các tài nguyên chung theo thứ tự vòng tròn, dẫn đến việc cả hai phiên đều bị chặn (Block) và chờ đợi lẫn nhau vô hạn. Nhóm đã xây dựng kịch bản thực nghiệm tái hiện chính xác hiện tượng này trên 2 phiên làm việc độc lập của PostgreSQL 18.6:")

    dl_steps_headers = ["Thời điểm", "Phiên 1: Session A (PID 16484)", "Phiên 2: Session B (PID 13804)", "Trạng thái Khóa & Đồ thị Chờ (WFG)"]
    dl_steps_data = [
        ["T1", "BEGIN; UPDATE users SET reputation = reputation + 10 WHERE user_id = 1;", "—", "Session A giữ khóa độc quyền (ExclusiveLock) trên dòng user_id = 1."],
        ["T2", "—", "BEGIN; UPDATE users SET reputation = reputation + 5 WHERE user_id = 2;", "Session B giữ khóa độc quyền (ExclusiveLock) trên dòng user_id = 2."],
        ["T3", "UPDATE users SET reputation = reputation + 10 WHERE user_id = 2;", "—", "Session A yêu cầu khóa user_id = 2 ⇒ BỊ CHẶN (Block). WFG: Session A → Session B."],
        ["T4", "— (Đang chờ Session B)", "UPDATE users SET reputation = reputation + 5 WHERE user_id = 1;", "Session B yêu cầu khóa user_id = 1 ⇒ BỊ CHẶN! Xuất hiện chu trình WFG: A → B → A."],
        ["T5", "Hệ thống PostgreSQL phát hiện chu trình bế tắc sau 1.000ms. Session A bị ABORT với mã lỗi 40P01!", "Vượt qua tình trạng bị chặn và thực thi thành công câu lệnh UPDATE!", "Chu trình bế tắc bị phá vỡ. Session B thực hiện COMMIT an toàn."],
    ]
    add_styled_table(doc, dl_steps_headers, dl_steps_data, [0.8, 2.0, 2.0, 2.4])

    add_paragraph(doc, "Trích xuất nhật ký thực nghiệm nguyên bản từ máy chủ PostgreSQL (transactions/t3_concurrent/logs/deadlock_t3_log.txt):", bold_prefix="Dấu vết lỗi bế tắc thực tế (Deadlock Log Trace): ")
    add_code_block(doc, "2026-10-27 15:42:01.312 +07 [16484] ERROR:  deadlock detected\n"
                        "2026-10-27 15:42:01.312 +07 [16484] DETAIL:  Process 16484 waits for ExclusiveLock on tuple (0,2) of relation 16421 of database 16384;\n"
                        "    blocked by process 13804.\n"
                        "    Process 13804 waits for ExclusiveLock on tuple (0,1) of relation 16421 of database 16384;\n"
                        "    blocked by process 16484.\n"
                        "    Process 16484: UPDATE users SET reputation = reputation + 10 WHERE user_id = 2;\n"
                        "    Process 13804: UPDATE users SET reputation = reputation + 5 WHERE user_id = 1;\n"
                        "2026-10-27 15:42:01.312 +07 [16484] HINT:  See server log for query details.\n"
                        "2026-10-27 15:42:01.312 +07 [16484] CONTEXT:  while updating tuple (0,2) in relation \"users\"\n"
                        "2026-10-27 15:42:01.312 +07 [16484] STATEMENT:  UPDATE users SET reputation = reputation + 10 WHERE user_id = 2;\n"
                        "SQLSTATE: 40P01 (deadlock_detected)",
                   "Nhật ký lỗi bế tắc thực nghiệm (PostgreSQL 40P01)")

    add_callout_box(doc, "3 GIẢI PHÁP KỸ THUẬT PHÒNG CHỐNG BẾ TẮC TRONG THỰC TẾ:\n"
                         "1. Khóa tài nguyên theo thứ tự xác định (Ordered Resource Locking): Mọi luồng giao dịch bắt buộc phải khóa các dòng theo thứ tự ID tăng dần (ví dụ: luôn khóa user_id nhỏ trước, user_id lớn sau). Điều này triệt tiêu hoàn toàn khả năng hình thành chu trình trong đồ thị WFG.\n"
                         "2. Sử dụng mệnh đề SELECT ... FOR UPDATE NOWAIT: Nếu tài nguyên đang bị phiên khác giữ khóa, giao dịch sẽ báo lỗi ngay lập tức thay vì treo chờ, giúp ứng dụng nhanh chóng thử lại (Retry with exponential backoff).\n"
                         "3. Sử dụng SELECT ... FOR UPDATE SKIP LOCKED: Cực kỳ hữu hiệu cho các hệ thống hàng đợi công việc (Job Queues), tự động bỏ qua các bản ghi đang bị khóa bởi tiến trình khác.",
                    "GIẢI PHÁP PHÒNG CHỐNG BẾ TẮC (DEADLOCK PREVENTION)")

    doc.add_page_break()
