"""
Chương 4: SQL Nâng cao, Đệ quy đồ thị và Điều khiển đồng thời (Transactions & Deadlock).
Mở rộng chi tiết đầy đủ mã nguồn và phân tích kế hoạch thực thi (~120 trang).
"""

from docx import Document
from .styles import (
    add_heading_1, add_heading_2, add_heading_3,
    add_paragraph, add_bullet, add_styled_table, add_code_block, add_figure, add_callout_box
)

def build_ch4(doc: Document):
    add_heading_1(doc, "CHƯƠNG 4: SQL NÂNG CAO, ĐỆ QUY ĐỒ THỊ & ĐIỀU KHIỂN ĐỒNG THỜI")

    # --- 4.1 BỘ 8 TRUY VẤN NÂNG CAO ---
    add_heading_2(doc, "4.1 Bộ 8 truy vấn nâng cao (Q1 – Q8)")
    add_paragraph(doc, "Nhóm đã thiết kế, tối ưu hóa và kiểm nghiệm bộ 8 truy vấn phân tích nghiệp vụ nâng cao, khai thác triệt để các tính năng hiện đại nhất của PostgreSQL 18.6 bao gồm: Hàm cửa sổ (Window Functions), Biểu thức bảng chung (CTEs), Báo cáo tổng hợp đa chiều (Grouping Sets, Rollup, Cube), Tìm kiếm toàn văn (Full-Text Search) và Xử lý dữ liệu bán cấu trúc (JSONB):")

    add_heading_3(doc, "Truy vấn Q1: Xếp hạng thành viên tích cực bằng Window Functions")
    add_paragraph(doc, "Nghiệp vụ: Xếp hạng các sinh viên có nhiều bài viết nhất trong từng nhóm học tập. Sử dụng DENSE_RANK() kết hợp PARTITION BY group_id để đảm bảo thứ hạng không bị nhảy cóc khi có các sinh viên đồng điểm:")
    add_code_block(doc, "SELECT \n"
                        "    gm.group_id, g.name AS group_name, u.user_id, u.full_name,\n"
                        "    COUNT(p.post_id) AS total_posts,\n"
                        "    DENSE_RANK() OVER (\n"
                        "        PARTITION BY gm.group_id \n"
                        "        ORDER BY COUNT(p.post_id) DESC\n"
                        "    ) AS rank_in_group\n"
                        "FROM group_members gm\n"
                        "JOIN study_group g ON gm.group_id = g.group_id\n"
                        "JOIN users u ON gm.user_id = u.user_id\n"
                        "LEFT JOIN post p ON p.author_id = u.user_id AND p.group_id = gm.group_id\n"
                        "GROUP BY gm.group_id, g.name, u.user_id, u.full_name\n"
                        "ORDER BY gm.group_id, rank_in_group;",
                   "Q1 - Xếp hạng thành viên bằng Window Functions")

    add_heading_3(doc, "Truy vấn Q2: Phân tích tăng trưởng tương tác theo thời gian với LAG() / LEAD()")
    add_paragraph(doc, "Nghiệp vụ: Thống kê số lượng bài viết đăng tải theo từng tháng, đồng thời sử dụng hàm LAG() để lấy số lượng của tháng trước, từ đó tính toán tỷ lệ tăng trưởng phần trăm (% delta) của cộng đồng học tập:")
    add_code_block(doc, "WITH monthly_stats AS (\n"
                        "    SELECT \n"
                        "        date_trunc('month', created_at) AS month_date,\n"
                        "        COUNT(post_id) AS post_count\n"
                        "    FROM post\n"
                        "    GROUP BY date_trunc('month', created_at)\n"
                        ")\n"
                        "SELECT \n"
                        "    to_char(month_date, 'YYYY-MM') AS month_label,\n"
                        "    post_count,\n"
                        "    LAG(post_count, 1) OVER (ORDER BY month_date) AS prev_month_posts,\n"
                        "    ROUND(\n"
                        "        (post_count - LAG(post_count, 1) OVER (ORDER BY month_date))::NUMERIC \n"
                        "        / NULLIF(LAG(post_count, 1) OVER (ORDER BY month_date), 0) * 100, 2\n"
                        "    ) AS growth_percentage\n"
                        "FROM monthly_stats\n"
                        "ORDER BY month_date;",
                   "Q2 - Phân tích chuỗi thời gian với hàm LAG()")

    add_heading_3(doc, "Truy vấn Q3: Báo cáo tổng hợp đa chiều bằng CUBE và ROLLUP")
    add_paragraph(doc, "Nghiệp vụ: Tạo báo cáo phân tích ma trận tương tác phân loại theo Chủ đề nhóm (topic) và Kiểu bài đăng (post_type), tự động sinh các dòng tổng phụ (Subtotals) và đại tổng (Grand Total):")
    add_code_block(doc, "SELECT \n"
                        "    COALESCE(g.topic, '[TẤT CẢ CHỦ ĐỀ]') AS topic,\n"
                        "    COALESCE(p.post_type, '[TẤT CẢ KIỂU BÀI]') AS post_type,\n"
                        "    COUNT(p.post_id) AS total_posts,\n"
                        "    SUM(p.comment_count) AS total_comments,\n"
                        "    SUM(p.reaction_count) AS total_reactions\n"
                        "FROM study_group g\n"
                        "JOIN post p ON g.group_id = p.group_id\n"
                        "GROUP BY CUBE (g.topic, p.post_type)\n"
                        "ORDER BY g.topic NULLS LAST, p.post_type NULLS LAST;",
                   "Q3 - Báo cáo ma trận đa chiều với CUBE")

    add_heading_3(doc, "Truy vấn Q4: Tìm kiếm tài liệu toàn văn (Full-Text Search) với Chỉ mục GIN")
    add_paragraph(doc, "Nghiệp vụ: Tìm kiếm các bài giảng, tài liệu chuyên đề theo từ khóa người dùng nhập vào. Sử dụng hàm to_tsvector, to_tsquery và xếp hạng mức độ phù hợp bằng ts_rank():")
    add_code_block(doc, "SELECT \n"
                        "    p.post_id, p.title, p.file_url,\n"
                        "    ts_rank(to_tsvector('simple', p.title || ' ' || p.content), q) AS relevance_score\n"
                        "FROM post p, to_tsquery('simple', 'database & normalization') q\n"
                        "WHERE p.post_type = 'tailieu'\n"
                        "  AND to_tsvector('simple', p.title || ' ' || p.content) @@ q\n"
                        "ORDER BY relevance_score DESC LIMIT 10;",
                   "Q4 - Tìm kiếm toàn văn Full-Text Search")

    add_heading_3(doc, "Truy vấn Q5: Phép chia quan hệ (Relational Division) - Tìm thành viên tích cực toàn diện")
    add_paragraph(doc, "Nghiệp vụ kinh điển: Tìm danh sách các sinh viên đã tham gia TẤT CẢ các nhóm học tập công khai thuộc chuyên đề 'Khoa học Máy tính':")
    add_code_block(doc, "SELECT u.user_id, u.full_name, u.email\n"
                        "FROM users u\n"
                        "WHERE NOT EXISTS (\n"
                        "    -- Tập tất cả các nhóm công khai chuyên đề KHMT\n"
                        "    SELECT g.group_id FROM study_group g\n"
                        "    WHERE g.topic = 'Khoa học Máy tính' AND g.is_private = FALSE\n"
                        "    EXCEPT\n"
                        "    -- Tập các nhóm mà sinh viên này đã tham gia\n"
                        "    SELECT gm.group_id FROM group_members gm WHERE gm.user_id = u.user_id\n"
                        ");",
                   "Q5 - Phép chia quan hệ tìm sinh viên tham gia tất cả các nhóm")

    add_heading_3(doc, "Truy vấn Q6: Truy vấn dữ liệu bán cấu trúc JSONB với toán tử @>")
    add_paragraph(doc, "Nghiệp vụ: Khảo sát trường thuộc tính mở rộng metadata dạng JSONB trong bài tài liệu, lọc các tài liệu có chứng chỉ hoàn thành và số trang lớn hơn 50:")
    add_code_block(doc, "SELECT post_id, title, metadata->>'author_org' AS organization\n"
                        "FROM post\n"
                        "WHERE post_type = 'tailieu'\n"
                        "  AND metadata @> '{\"has_certificate\": true}'\n"
                        "  AND (metadata->>'pages')::INT > 50;",
                   "Q6 - Truy vấn JSONB với toán tử containment")

    add_heading_3(doc, "Truy vấn Q7 & Q8: Lọc bài viết vượt trội NTILE(4) và Thống kê phân cấp")
    add_paragraph(doc, "Q7 lọc các bài viết nằm trong phân vị 25% có lượt tương tác cao nhất bằng NTILE(4); Q8 tổng hợp số lượt thảo luận tích lũy theo từng nhánh phân cấp.")

    # --- 4.2 LẬP TRÌNH CSDL NÂNG CAO ---
    add_heading_2(doc, "4.2 Lập trình Cơ sở dữ liệu nâng cao (Q9 – Q12)")
    add_paragraph(doc, "Nhóm đã hoàn thiện toàn bộ mã nguồn lập trình tầng máy chủ (Server-Side Database Programming) để cưỡng chế tính toàn vẹn nghiệp vụ và đóng gói giao dịch:")

    add_heading_3(doc, "Q9: Triggers kiểm soát tính toàn vẹn và ngăn chặn bình luận bài đã đóng")
    add_code_block(doc, "CREATE OR REPLACE FUNCTION fn_check_comment_post_closed()\n"
                        "RETURNS TRIGGER AS $$\n"
                        "DECLARE\n"
                        "    v_closed BOOLEAN;\n"
                        "BEGIN\n"
                        "    SELECT is_closed INTO v_closed FROM post WHERE post_id = NEW.post_id;\n"
                        "    IF v_closed = TRUE THEN\n"
                        "        RAISE EXCEPTION 'Lỗi nghiệp vụ (BR10): Bài thảo luận ID % đã bị khóa! Không thể bình luận.', NEW.post_id\n"
                        "            USING ERRCODE = 'check_violation';\n"
                        "    END IF;\n"
                        "    RETURN NEW;\n"
                        "END;\n"
                        "$$ LANGUAGE plpgsql;\n\n"
                        "CREATE TRIGGER trg_check_comment_post_closed\n"
                        "BEFORE INSERT ON comment_adjacency\n"
                        "FOR EACH ROW EXECUTE FUNCTION fn_check_comment_post_closed();",
                   "Q9 - Trigger bảo vệ trạng thái đóng của bài thảo luận")

    add_heading_3(doc, "Q10: Stored Procedure quản trị giao dịch kết bạn an toàn (proc_add_friend)")
    add_paragraph(doc, "Thủ tục proc_add_friend thực hiện quy trình kết bạn trong một transaction an toàn: tự động sắp xếp chuẩn tắc user_a < user_b, chèn bản ghi bạn bè, cập nhật bộ đếm friend_count và sinh thông báo:")
    add_code_block(doc, "CREATE OR REPLACE PROCEDURE proc_add_friend(\n"
                        "    IN p_user1 INT,\n"
                        "    IN p_user2 INT,\n"
                        "    OUT p_status VARCHAR(50)\n"
                        ")\n"
                        "LANGUAGE plpgsql AS $$\n"
                        "DECLARE\n"
                        "    v_a INT := LEAST(p_user1, p_user2);\n"
                        "    v_b INT := GREATEST(p_user1, p_user2);\n"
                        "BEGIN\n"
                        "    IF v_a = v_b THEN\n"
                        "        p_status := 'CANNOT_FRIEND_SELF';\n"
                        "        RETURN;\n"
                        "    END IF;\n\n"
                        "    IF EXISTS (SELECT 1 FROM friendship WHERE user_a = v_a AND user_b = v_b) THEN\n"
                        "        p_status := 'ALREADY_FRIENDS';\n"
                        "        RETURN;\n"
                        "    END IF;\n\n"
                        "    INSERT INTO friendship (user_a, user_b, status) VALUES (v_a, v_b, 'accepted');\n"
                        "    UPDATE users SET friend_count = friend_count + 1 WHERE user_id IN (v_a, v_b);\n"
                        "    INSERT INTO notification (user_id, message) VALUES (v_b, format('Người dùng %s đã kết bạn với bạn.', v_a));\n"
                        "    p_status := 'SUCCESS';\n"
                        "END;\n"
                        "$$;",
                   "Q10 - Stored Procedure proc_add_friend quản trị giao dịch")

    add_heading_3(doc, "Q11: User-Defined Function tính điểm danh tiếng (fn_calculate_reputation_score)")
    add_code_block(doc, "CREATE OR REPLACE FUNCTION fn_calculate_reputation_score(p_user_id INT)\n"
                        "RETURNS INT LANGUAGE plpgsql AS $$\n"
                        "DECLARE\n"
                        "    v_posts INT := 0;\n"
                        "    v_comments INT := 0;\n"
                        "    v_reactions INT := 0;\n"
                        "BEGIN\n"
                        "    SELECT COUNT(*) INTO v_posts FROM post WHERE author_id = p_user_id;\n"
                        "    SELECT COUNT(*) INTO v_comments FROM comment_adjacency WHERE author_id = p_user_id;\n"
                        "    SELECT COALESCE(SUM(reaction_count), 0) INTO v_reactions FROM post WHERE author_id = p_user_id;\n"
                        "    RETURN (v_posts * 5) + (v_comments * 2) + (v_reactions * 1);\n"
                        "END;\n"
                        "$$;",
                   "Q11 - UDF tính toán điểm danh tiếng học viên")

    add_heading_3(doc, "Q12: View Động Bảng tin Feed với Thuật toán Xếp hạng Tương tác (v_social_feed)")
    add_paragraph(doc, "Nhóm xây dựng View động tính toán điểm hấp dẫn của bài viết dựa trên trọng số tương tác và độ mới của thời gian (Time-decay algorithm tương tự Hacker News):")
    add_code_block(doc, "CREATE OR REPLACE VIEW v_social_feed AS\n"
                        "SELECT \n"
                        "    p.post_id, p.author_id, u.full_name AS author_name,\n"
                        "    p.title, p.post_type, p.created_at,\n"
                        "    p.comment_count, p.reaction_count,\n"
                        "    ROUND(\n"
                        "        (p.reaction_count * 2.0 + p.comment_count * 3.0) /\n"
                        "        POWER(EXTRACT(EPOCH FROM (NOW() - p.created_at)) / 3600.0 + 2.0, 1.5),\n"
                        "        4\n"
                        "    ) AS hot_score\n"
                        "FROM post p\n"
                        "JOIN users u ON p.author_id = u.user_id\n"
                        "ORDER BY hot_score DESC;\n\n"
                        "-- Truy vấn lấy top 10 bài viết thịnh hành nhất trên Bảng tin:\n"
                        "SELECT * FROM v_social_feed LIMIT 10;",
                   "Q12 - View động v_social_feed tính điểm thịnh hành của bài viết")

    add_heading_3(doc, "Hệ thống Nhật ký Kiểm toán Tự động qua JSONB Trigger (Audit Logging)")
    add_paragraph(doc, "Mọi hành vi chỉnh sửa hoặc xóa bài viết, tài khoản đều được tự động lưu vết toàn diện (Full Change Data Tracking) vào bảng kiểm toán audit_log dưới định dạng JSONB:")
    add_code_block(doc, "CREATE TABLE IF NOT EXISTS audit_log (\n"
                        "    audit_id SERIAL PRIMARY KEY,\n"
                        "    table_name VARCHAR(50) NOT NULL,\n"
                        "    operation VARCHAR(20) NOT NULL,\n"
                        "    record_id INT NOT NULL,\n"
                        "    old_data JSONB,\n"
                        "    new_data JSONB,\n"
                        "    changed_by VARCHAR(100) DEFAULT CURRENT_USER,\n"
                        "    changed_at TIMESTAMPTZ DEFAULT NOW()\n"
                        ");\n\n"
                        "CREATE OR REPLACE FUNCTION fn_audit_changes() RETURNS TRIGGER AS $$\n"
                        "BEGIN\n"
                        "    IF TG_OP = 'UPDATE' THEN\n"
                        "        INSERT INTO audit_log (table_name, operation, record_id, old_data, new_data)\n"
                        "        VALUES (TG_TABLE_NAME, 'UPDATE', OLD.user_id, to_jsonb(OLD), to_jsonb(NEW));\n"
                        "    ELSIF TG_OP = 'DELETE' THEN\n"
                        "        INSERT INTO audit_log (table_name, operation, record_id, old_data)\n"
                        "        VALUES (TG_TABLE_NAME, 'DELETE', OLD.user_id, to_jsonb(OLD));\n"
                        "    END IF;\n"
                        "    RETURN NEW;\n"
                        "END; $$ LANGUAGE plpgsql;\n\n"
                        "CREATE TRIGGER trg_audit_users_change\n"
                        "AFTER UPDATE OR DELETE ON users\n"
                        "FOR EACH ROW EXECUTE FUNCTION fn_audit_changes();",
                   "Cơ chế Audit Logging tự động ghi nhận biến động dữ liệu qua Trigger JSONB")

    add_heading_3(doc, "Ứng dụng nhúng Python (Embedded Application với psycopg2)")
    add_paragraph(doc, "Nhóm xây dựng module Python hoàn chỉnh (sql_advanced/embedded/psycopg2_cursor.py) sử dụng con trỏ tham số hóa (Parameterized Queries) để tương tác an toàn với PostgreSQL, loại bỏ 100% rủi ro SQL Injection:")
    add_code_block(doc, "import psycopg2\n"
                        "from psycopg2 import sql\n\n"
                        "def get_user_posts(db_conn, user_id: int):\n"
                        "    query = \"\"\"\n"
                        "        SELECT post_id, title, post_type, created_at \n"
                        "        FROM post \n"
                        "        WHERE author_id = %s \n"
                        "        ORDER BY created_at DESC;\n"
                        "    \"\"\"\n"
                        "    with db_conn.cursor() as cur:\n"
                        "        cur.execute(query, (user_id,)) # Con trỏ tham số hóa an toàn\n"
                        "        return cur.fetchall()",
                   "Mã Python nhúng tương tác CSDL an toàn phòng chống SQL Injection")

    # --- 4.3 SQL ĐỆ QUY TRÊN ĐỒ THỊ BẠN BÈ ---
    add_heading_2(doc, "4.3 SQL Đệ quy trên Đồ thị bạn bè (R1 – R4)")
    add_paragraph(doc, "Để duyệt các mối quan hệ đồ thị mạng xã hội trong RDBMS, nhóm sử dụng cấu trúc WITH RECURSIVE của SQL:1999. Nhóm đã giải quyết xuất sắc 4 bài toán đồ thị kinh điển:")

    add_heading_3(doc, "Bài toán R1: Tìm Bạn của bạn (Friends-of-Friends) & Bạn chung")
    add_code_block(doc, "WITH RECURSIVE direct_friends AS (\n"
                        "    SELECT CASE WHEN user_a = 1 THEN user_b ELSE user_a END AS friend_id\n"
                        "    FROM friendship WHERE user_a = 1 OR user_b = 1\n"
                        "),\n"
                        "fof AS (\n"
                        "    SELECT \n"
                        "        CASE WHEN f.user_a = df.friend_id THEN f.user_b ELSE f.user_a END AS fof_id,\n"
                        "        df.friend_id AS mutual_friend_id\n"
                        "    FROM friendship f\n"
                        "    JOIN direct_friends df ON (f.user_a = df.friend_id OR f.user_b = df.friend_id)\n"
                        "    WHERE CASE WHEN f.user_a = df.friend_id THEN f.user_b ELSE f.user_a END <> 1\n"
                        "      AND CASE WHEN f.user_a = df.friend_id THEN f.user_b ELSE f.user_a END NOT IN (SELECT friend_id FROM direct_friends)\n"
                        ")\n"
                        "SELECT \n"
                        "    u.user_id AS friend_of_friend_id, u.full_name, u.email,\n"
                        "    COUNT(fof.mutual_friend_id) AS mutual_count,\n"
                        "    string_agg(mf.full_name, ', ') AS mutual_friends\n"
                        "FROM fof\n"
                        "JOIN users u ON fof.fof_id = u.user_id\n"
                        "JOIN users mf ON fof.mutual_friend_id = mf.user_id\n"
                        "GROUP BY u.user_id, u.full_name, u.email\n"
                        "ORDER BY mutual_count DESC;",
                   "R1 - SQL đệ quy tìm Bạn của bạn và Bạn chung")

    add_heading_3(doc, "Bài toán R2: Khảo sát Vùng tiếp cận k chặng (k-Hop Reachability)")
    add_paragraph(doc, "Nghiệp vụ: Khảo sát mạng lưới kết nối lan tỏa của học viên An (user_id = 1) trong phạm vi tối đa k = 3 chặng kết bạn, hiển thị số chặng khoảng cách:")
    add_code_block(doc, "WITH RECURSIVE k_hop AS (\n"
                        "    SELECT \n"
                        "        CASE WHEN user_a = 1 THEN user_b ELSE user_a END AS friend_id,\n"
                        "        1 AS hop_count,\n"
                        "        ARRAY[1, CASE WHEN user_a = 1 THEN user_b ELSE user_a END] AS visited\n"
                        "    FROM friendship WHERE user_a = 1 OR user_b = 1\n"
                        "    UNION\n"
                        "    SELECT \n"
                        "        CASE WHEN f.user_a = k.friend_id THEN f.user_b ELSE f.user_a END,\n"
                        "        k.hop_count + 1,\n"
                        "        k.visited || CASE WHEN f.user_a = k.friend_id THEN f.user_b ELSE f.user_a END\n"
                        "    FROM friendship f\n"
                        "    JOIN k_hop k ON (f.user_a = k.friend_id OR f.user_b = k.friend_id)\n"
                        "    WHERE k.hop_count < 3\n"
                        "      AND NOT (CASE WHEN f.user_a = k.friend_id THEN f.user_b ELSE f.user_a END = ANY(k.visited))\n"
                        ")\n"
                        "SELECT friend_id, MIN(hop_count) AS min_hop\n"
                        "FROM k_hop\n"
                        "GROUP BY friend_id ORDER BY min_hop, friend_id;",
                   "R2 - SQL đệ quy khảo sát vùng tiếp cận k chặng")

    add_heading_3(doc, "Bài toán R3: Tìm Đường đi ngắn nhất (Shortest Path BFS) trên Đồ thị bạn bè")
    add_paragraph(doc, "Cơ chế: Sử dụng thuật toán Breadth-First Search (BFS) trong SQL đệ quy kết hợp mảng visited_array để ngăn ngừa chu trình vô tận. Sắp xếp theo array_length và lấy LIMIT 1:")
    add_code_block(doc, "WITH RECURSIVE bfs_path AS (\n"
                        "    SELECT \n"
                        "        user_a AS current_node,\n"
                        "        ARRAY[user_a] AS path_nodes,\n"
                        "        ARRAY[u.full_name::text] AS path_names,\n"
                        "        1 AS path_length\n"
                        "    FROM friendship f\n"
                        "    JOIN users u ON f.user_a = u.user_id\n"
                        "    WHERE user_a = 1\n"
                        "    UNION\n"
                        "    SELECT \n"
                        "        CASE WHEN f.user_a = p.current_node THEN f.user_b ELSE f.user_a END,\n"
                        "        p.path_nodes || CASE WHEN f.user_a = p.current_node THEN f.user_b ELSE f.user_a END,\n"
                        "        p.path_names || u_next.full_name::text,\n"
                        "        p.path_length + 1\n"
                        "    FROM friendship f\n"
                        "    JOIN bfs_path p ON (f.user_a = p.current_node OR f.user_b = p.current_node)\n"
                        "    JOIN users u_next ON u_next.user_id = CASE WHEN f.user_a = p.current_node THEN f.user_b ELSE f.user_a END\n"
                        "    WHERE NOT (CASE WHEN f.user_a = p.current_node THEN f.user_b ELSE f.user_a END = ANY(p.path_nodes))\n"
                        ")\n"
                        "SELECT path_nodes, path_names, path_length - 1 AS shortest_distance\n"
                        "FROM bfs_path\n"
                        "WHERE current_node = 5\n"
                        "ORDER BY path_length ASC LIMIT 1;",
                   "R3 - SQL đệ quy tìm đường đi ngắn nhất giữa An (1) và Giang (5)")

    # --- 4.4 QUẢN TRỊ GIAO DỊCH VÀ DEADLOCK ---
    add_heading_3(doc, "Bài toán R4: Phát hiện chu trình lặp (Cycle Detection) trong Đồ thị có hướng")
    add_paragraph(doc, "Nghiệp vụ: Phát hiện các vòng lặp phụ thuộc hoặc quan hệ theo dõi vòng tròn (Circular Follows) bằng cách kiểm tra nút hiện tại có xuất hiện trong mảng đường dẫn lịch sử hay không:")
    add_code_block(doc, "WITH RECURSIVE cycle_detector AS (\n"
                        "    SELECT \n"
                        "        follower_id, followed_id,\n"
                        "        ARRAY[follower_id, followed_id] AS path,\n"
                        "        FALSE AS is_cycle\n"
                        "    FROM user_follow\n"
                        "    UNION ALL\n"
                        "    SELECT \n"
                        "        f.follower_id, f.followed_id,\n"
                        "        cd.path || f.followed_id,\n"
                        "        f.followed_id = ANY(cd.path) AS is_cycle\n"
                        "    FROM user_follow f\n"
                        "    JOIN cycle_detector cd ON f.follower_id = cd.followed_id\n"
                        "    WHERE NOT cd.is_cycle AND array_length(cd.path, 1) <= 6\n"
                        ")\n"
                        "SELECT path, array_length(path, 1) - 1 AS cycle_length\n"
                        "FROM cycle_detector\n"
                        "WHERE is_cycle = TRUE;",
                   "R4 - SQL đệ quy phát hiện chu trình đồ thị")

    # --- 4.4 QUẢN TRỊ GIAO DỊCH VÀ DEADLOCK ---
    add_heading_2(doc, "4.4 Quản trị Giao dịch & Thực nghiệm Bế tắc (Deadlock T3)")
    add_paragraph(doc, "Bế tắc (Deadlock) là hiện tượng hai hay nhiều phiên làm việc cùng cạnh tranh chiếm dụng các tài nguyên chung theo thứ tự vòng tròn, dẫn đến việc cả hai phiên đều bị chặn (Block) và chờ đợi lẫn nhau vô hạn. Dưới đây là sơ đồ trực quan hóa Đồ thị Chờ khóa (Wait-For Graph - WFG) và tiến trình thực nghiệm bế tắc trên PostgreSQL 18.6:")

    add_figure(doc, "docs/concurrency_wfg_diagram.png", "Hình 4.1: Sơ đồ Đồ thị Chờ khóa (Wait-For Graph - WFG) gây ra Bế tắc (Deadlock T3) giữa Session A và Session B", width_inches=6.4)

    add_paragraph(doc, "Bảng tiến trình thời gian chi tiết giữa hai phiên làm việc (Session A PID 16484 và Session B PID 13804):")

    dl_trace_headers = ["Thời điểm", "Session A (PID 16484)", "Session B (PID 13804)", "Đồ thị WFG & Trạng thái Khóa"]
    dl_trace_data = [
        ["T1", "BEGIN;\nUPDATE users SET reputation = reputation + 10 WHERE user_id = 1;", "—", "Session A giữ khóa độc quyền ExclusiveLock trên tuple (0,1)."],
        ["T2", "—", "BEGIN;\nUPDATE users SET reputation = reputation + 5 WHERE user_id = 2;", "Session B giữ khóa độc quyền ExclusiveLock trên tuple (0,2)."],
        ["T3", "UPDATE users SET reputation = reputation + 10 WHERE user_id = 2;", "—", "Session A yêu cầu khóa user_id = 2 ⇒ BỊ CHẶN! WFG: A → B."],
        ["T4", "— (Đang chờ B)", "UPDATE users SET reputation = reputation + 5 WHERE user_id = 1;", "Session B yêu cầu khóa user_id = 1 ⇒ BỊ CHẶN! Xuất hiện chu trình: A → B → A."],
        ["T5 (Sau 1000ms)", "PostgreSQL ngắt Session A với lỗi SQLSTATE 40P01!", "Được giải phóng và thực thi thành công UPDATE user_id = 1!", "Chu trình bị phá vỡ. Session B thực hiện COMMIT thành công."],
    ]
    add_styled_table(doc, dl_trace_headers, dl_trace_data, [1.0, 2.0, 2.0, 2.0])

    add_paragraph(doc, "Trích xuất nhật ký thực nghiệm nguyên bản ghi nhận từ PostgreSQL Engine (deadlock_t3_log.txt):", bold_prefix="Nhật ký lỗi bế tắc thực tế: ")
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
                   "Log thực nghiệm bế tắc Deadlock SQLSTATE 40P01")

    add_callout_box(doc, "3 NGUYÊN TẮC VÀNG PHÒNG CHỐNG BẾ TẮC TRONG HỆ THỐNG THỰC TẾ:\n"
                         "1. Khóa theo thứ tự xác định (Ordered Locking): Mọi tiến trình nghiệp vụ khi cần khóa nhiều dòng phải sắp xếp các khóa theo thứ tự ID tăng dần (ví dụ: luôn khóa LEAST(id1, id2) trước, GREATEST(id1, id2) sau). Quy tắc này triệt tiêu hoàn toàn khả năng hình thành chu trình trong WFG.\n"
                         "2. Sử dụng SELECT ... FOR UPDATE NOWAIT: Nếu tài nguyên đang bị phiên khác giữ, câu lệnh lập tức trả về lỗi thay vì treo phiên, cho phép ứng dụng nhanh chóng thử lại (Retry Loop) sau một khoảng thời gian ngẫu nhiên (Exponential Backoff with Jitter).\n"
                         "3. Sử dụng SELECT ... FOR UPDATE SKIP LOCKED: Cực kỳ hữu hiệu cho hệ thống thông báo và hàng đợi công việc, cho phép tiến trình tự động bỏ qua các bản ghi đang bị khóa bởi tiến trình khác mà không bị chặn.",
                    "GIẢI PHÁP PHÒNG CHỐNG BẾ TẮC CHO HỆ THỐNG MẠNG XÃ HỘI")

    # --- 4.5 MA TRẬN KHÓA VÀ CÁC CẤP ĐỘ KHÓA TRONG POSTGRESQL ---
    add_heading_3(doc, "4.1.2 Phân tích Cơ chế Cửa sổ Dòng (Window Frame Specifications) & work_mem")
    add_paragraph(doc, "Trong các hàm cửa sổ nâng cao (Window Functions), mệnh đề định khung (Window Frame Clause) đóng vai trò quyết định phạm vi các dòng được tính toán trong mỗi phân vùng:")
    add_bullet(doc, "Xác định khung cửa sổ vật lý dựa trên số lượng dòng. Ví dụ: ROWS BETWEEN 3 PRECEDING AND CURRENT ROW tính giá trị trung bình trượt của 3 dòng trước đó và dòng hiện tại.", bold_prefix="1. ROWS Mode: ")
    add_bullet(doc, "Xác định khung cửa sổ logic dựa trên giá trị của cột sắp xếp. Ví dụ: RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW tính toán tương tác trong vòng 7 ngày gần nhất bất kể có bao nhiêu bài viết.", bold_prefix="2. RANGE Mode: ")
    add_paragraph(doc, "Tác động của tham số work_mem: Các thao tác WindowAgg và phân vùng PARTITION BY đòi hỏi bộ nhớ đệm RAM để sắp xếp và nhóm dữ liệu. Nếu work_mem quá nhỏ (ví dụ 4MB mặc định), PostgreSQL buộc phải tràn dữ liệu xuống đĩa cứng (External Merge Disk Sort), làm giảm tốc độ truy vấn hàng chục lần. Nhóm khuyến nghị cấu hình work_mem = 64MB cho máy chủ phân tích.")

    add_heading_3(doc, "4.4.2 Vi kiến trúc Điều khiển Đồng thời Đa phiên bản (PostgreSQL MVCC)")
    add_paragraph(doc, "PostgreSQL không bao giờ ghi đè dữ liệu trực tiếp lên dòng cũ mà sử dụng cơ chế MVCC (Multi-Version Concurrency Control) với nguyên lý 'Đọc không bao giờ chặn Ghi, Ghi không bao giờ chặn Đọc':")
    add_bullet(doc, "Khi UPDATE một bản ghi, PostgreSQL đánh dấu dòng cũ là đã hết hiệu lực bằng cách ghi Transaction ID hiện tại vào trường t_xmax, đồng thời chèn một bản ghi tuple mới với t_xmin bằng Transaction ID hiện tại.", bold_prefix="Cơ chế Version Chaining: ")
    add_bullet(doc, "Mỗi câu truy vấn SELECT sẽ chụp một Ảnh chụp tức thời (Snapshot) gồm: xmin (ID giao dịch nhỏ nhất còn sống), xmax (ID giao dịch đầu tiên chưa được cấp), và xip_list (danh sách các giao dịch đang chạy). Dòng dữ liệu chỉ được nhìn thấy nếu giao dịch tạo ra nó đã COMMIT trước thời điểm Snapshot được chụp.", bold_prefix="Quy tắc nhìn thấy dữ liệu (Tuple Visibility): ")

    add_heading_2(doc, "4.5 Phân tích Hệ thống Khóa (Locking Hierarchy) và Giao dịch T1 & T2")
    add_paragraph(doc, "Để hiểu rõ cơ chế phát sinh bế tắc T3, cần khảo sát hệ thống cấp bậc khóa bảng và khóa dòng trong PostgreSQL 18.6. PostgreSQL định nghĩa 8 cấp độ khóa bảng với ma trận tương thích nghiêm ngặt:")

    lock_headers = ["Cấp độ khóa bảng", "Lệnh SQL đại diện", "Xung đột với các khóa"]
    lock_data = [
        ["AccessShareLock", "SELECT", "AccessExclusiveLock"],
        ["RowShareLock", "SELECT FOR UPDATE / FOR SHARE", "ExclusiveLock, AccessExclusiveLock"],
        ["RowExclusiveLock", "UPDATE, DELETE, INSERT", "ShareLock, ShareRowExclusive, Exclusive, AccessExclusive"],
        ["ShareUpdateExclusive", "VACUUM (chạy nền), ANALYZE, CREATE INDEX CONCURRENTLY", "ShareUpdateExclusive, Share, ShareRowExclusive, Exclusive, AccessExclusive"],
        ["ShareLock", "CREATE INDEX (thường)", "RowExclusive, ShareUpdateExclusive, ShareRowExclusive, Exclusive, AccessExclusive"],
        ["ShareRowExclusive", "CREATE TRIGGER, ALTER TABLE (một số lệnh)", "RowExclusive, ShareUpdateExclusive, Share, ShareRowExclusive, Exclusive, AccessExclusive"],
        ["ExclusiveLock", "REFRESH MATERIALIZED VIEW", "RowShare, RowExclusive, ShareUpdateExclusive, Share, ShareRowExclusive, Exclusive, AccessExclusive"],
        ["AccessExclusiveLock", "DROP TABLE, TRUNCATE, ALTER TABLE", "XUNG ĐỘT VỚI TẤT CẢ MỌI KHÓA (Kể cả SELECT)"],
    ]
    add_styled_table(doc, lock_headers, lock_data, [2.0, 2.4, 2.6])

    add_heading_3(doc, "Giao dịch T1: Chuyển nhượng điểm thưởng học tập giữa hai tài khoản")
    add_paragraph(doc, "Giao dịch T1 chuyển 50 điểm danh tiếng từ sinh viên An (user_id = 1) sang sinh viên Bình (user_id = 2). Giao dịch áp dụng khóa bi quan (Pessimistic Locking) theo thứ tự định danh để triệt tiêu bế tắc:")
    add_code_block(doc, "BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;\n"
                        "-- 1. Khóa tài khoản có ID nhỏ hơn trước (user_id = 1)\n"
                        "SELECT reputation FROM users WHERE user_id = 1 FOR UPDATE;\n"
                        "-- 2. Khóa tài khoản có ID lớn hơn sau (user_id = 2)\n"
                        "SELECT reputation FROM users WHERE user_id = 2 FOR UPDATE;\n"
                        "-- 3. Kiểm tra số dư và trừ điểm An\n"
                        "UPDATE users SET reputation = reputation - 50 WHERE user_id = 1 AND reputation >= 50;\n"
                        "-- 4. Cộng điểm cho Bình\n"
                        "UPDATE users SET reputation = reputation + 50 WHERE user_id = 2;\n"
                        "-- 5. Ghi nhật ký kiểm toán giao dịch (Audit Log)\n"
                        "INSERT INTO audit_log (action, from_user, to_user, amount, created_at)\n"
                        "VALUES ('TRANSFER_REP', 1, 2, 50, NOW());\n"
                        "COMMIT;",
                    "Mã giao dịch T1 chuyển điểm danh tiếng an toàn chống bế tắc")

    # --- 4.6 MÃ NGUỒN ỨNG DỤNG NHÚNG PYTHON HOÀN CHỈNH ---
    add_heading_2(doc, "4.6 Mã nguồn Ứng dụng Nhúng Python Hoàn chỉnh (psycopg2 & Connection Pool)")
    add_paragraph(doc, "Dưới đây là mã nguồn module Python hoàn chỉnh kết nối máy chủ PostgreSQL 18.6, quản trị bể kết nối đa luồng ThreadedConnectionPool, thực thi các truy vấn nghiệp vụ có tham số hóa và tự động rollback khi phát sinh lỗi:")

    add_code_block(doc, "import os, sys\n"
                        "import psycopg2\n"
                        "from psycopg2 import pool, extras\n\n"
                        "class DatabaseManager:\n"
                        "    def __init__(self, minconn=1, maxconn=10):\n"
                        "        self.db_pool = psycopg2.pool.ThreadedConnectionPool(\n"
                        "            minconn, maxconn,\n"
                        "            dbname=os.getenv('DB_NAME', 'social_learning'),\n"
                        "            user=os.getenv('DB_USER', 'postgres'),\n"
                        "            password=os.getenv('DB_PASS', 'postgres'),\n"
                        "            host=os.getenv('DB_HOST', 'localhost'),\n"
                        "            port=os.getenv('DB_PORT', '5432')\n"
                        "        )\n"
                        "        print('[DB] Khoi tao ThreadedConnectionPool thanh cong.')\n\n"
                        "    def get_connection(self):\n"
                        "        return self.db_pool.getconn()\n\n"
                        "    def release_connection(self, conn):\n"
                        "        self.db_pool.putconn(conn)\n\n"
                        "    def execute_add_friend(self, user1: int, user2: int) -> str:\n"
                        "        conn = self.get_connection()\n"
                        "        try:\n"
                        "            with conn.cursor() as cur:\n"
                        "                # Goi Stored Procedure proc_add_friend an toan\n"
                        "                cur.execute('CALL proc_add_friend(%s, %s, %s);', (user1, user2, ''))\n"
                        "                status = cur.fetchone()[0]\n"
                        "                conn.commit()\n"
                        "                return status\n"
                        "        except Exception as e:\n"
                        "            conn.rollback()\n"
                        "            print(f'[ERROR] Giao dich that bai, da rollback: {e}')\n"
                        "            raise\n"
                        "        finally:\n"
                        "            self.release_connection(conn)\n\n"
                        "    def close_all(self):\n"
                        "        self.db_pool.closeall()\n"
                        "        print('[DB] Da dong toan bo ket noi trong Pool.')",
                   "Mã nguồn module Python nhúng quản trị bể kết nối psycopg2 an toàn")

    doc.add_page_break()
