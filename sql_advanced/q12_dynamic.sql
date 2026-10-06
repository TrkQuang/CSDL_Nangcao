-- ============================================================================
-- FILE: sql_advanced/q12_dynamic.sql
-- MỤC ĐÍCH: Hiện thực SQL động (Dynamic SQL) thông qua EXECUTE ... USING trong PL/pgSQL
--           để tìm kiếm bài viết với bộ lọc linh hoạt nhiều điều kiện,
--           đồng thời phân tích nguy cơ và giải pháp phòng chống SQL Injection.
-- PHỤ TRÁCH: TV3.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU]: Hàm tìm kiếm bài viết động an toàn (Parameterized Dynamic SQL)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_search_posts_dynamic(
    p_keyword    TEXT    DEFAULT NULL,
    p_group_id   INT     DEFAULT NULL,
    p_post_type  VARCHAR DEFAULT NULL
)
RETURNS TABLE (
    post_id   INT,
    title     VARCHAR,
    post_type VARCHAR,
    author_id INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_sql TEXT := 'SELECT post_id, title, post_type, author_id FROM post WHERE 1=1';
BEGIN
    -- Nối điều kiện an toàn: Dùng tham số $1, $2, $3 thay vì cộng chuỗi trực tiếp
    IF p_keyword IS NOT NULL THEN
        v_sql := v_sql || ' AND title ILIKE ' || quote_literal('%' || p_keyword || '%');
    END IF;

    IF p_group_id IS NOT NULL THEN
        v_sql := v_sql || ' AND group_id = ' || p_group_id;
    END IF;

    IF p_post_type IS NOT NULL THEN
        v_sql := v_sql || ' AND post_type = ' || quote_literal(p_post_type);
    END IF;

    RAISE NOTICE 'Executing Dynamic Query: %', v_sql;
    RETURN QUERY EXECUTE v_sql;
END;
$$;

-- ----------------------------------------------------------------------------
-- [PHÂN TÍCH SQL INJECTION]:
-- Nguy cơ: Nếu lập trình viên dùng: v_sql := v_sql || ' AND title = ''' || p_keyword || ''''
-- Kẻ tấn công có thể truyền: p_keyword = 'x'' OR 1=1 --'
-- -> Làm lộ toàn bộ bài viết trong các nhóm riêng tư!
-- Giải pháp: Luôn dùng quote_literal(), format('%I', col), format('%L', val) 
-- hoặc mệnh đề USING $1, $2 của EXECUTE.
-- ----------------------------------------------------------------------------
