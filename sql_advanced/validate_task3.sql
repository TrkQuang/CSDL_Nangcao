-- ============================================================================
-- FILE: sql_advanced/validate_task3.sql
-- MỤC ĐÍCH: Kiểm thử hồi quy các phần Task 3 trên seed_test.
-- YÊU CẦU: schema.sql, constraints.sql, seed_test.sql và q09-q12 đã được nạp.
-- ============================================================================

BEGIN;

DO $$
DECLARE
    v_count BIGINT;
    v_value BIGINT;
BEGIN
    SELECT COUNT(*) INTO v_count FROM users;
    IF v_count <> 6 THEN
        RAISE EXCEPTION 'Seed users failed: expected 6, got %', v_count;
    END IF;

    SELECT COUNT(*) INTO v_count
    FROM users
    WHERE friend_count = (
        SELECT COUNT(*) FROM friend_edge WHERE a = users.user_id
    );
    IF v_count <> 6 THEN
        RAISE EXCEPTION 'friend_count is inconsistent for % users', 6 - v_count;
    END IF;

    SELECT COUNT(*) INTO v_count
    FROM users u
    WHERE NOT EXISTS (SELECT 1 FROM post p WHERE p.author_id = u.user_id)
      AND NOT EXISTS (SELECT 1 FROM comment c WHERE c.author_id = u.user_id);
    IF v_count <> 1 THEN
        RAISE EXCEPTION 'Q2 failed: expected one inactive user, got %', v_count;
    END IF;

    SELECT COUNT(*) INTO v_count
    FROM study_group sg
    JOIN group_member gm ON gm.group_id = sg.group_id
    WHERE sg.topic = 'CSDL';
    IF v_count <> 4 THEN
        RAISE EXCEPTION 'Q3 seed cardinality failed: expected 4 memberships, got %', v_count;
    END IF;

    SELECT COUNT(*) INTO v_value
    FROM post_reaction pr
    WHERE pr.post_id = 1 AND pr.kind = 'like';
    IF v_value <> 3 THEN
        RAISE EXCEPTION 'Q6 failed: expected 3 likes for post 1, got %', v_value;
    END IF;
END;
$$;

-- Q9: parent khác bài viết phải bị từ chối.
DO $$
BEGIN
    BEGIN
        INSERT INTO comment (post_id, author_id, parent_id, content)
        VALUES (2, 1, 1, 'invalid cross-post parent');
        RAISE EXCEPTION 'Q9 failed: cross-post parent was accepted';
    EXCEPTION
        WHEN raise_exception THEN
            IF SQLERRM = 'Q9 failed: cross-post parent was accepted' THEN
                RAISE;
            END IF;
    END;
END;
$$;

-- Q9: parent trỏ vào chính comment cũng phải bị từ chối.
DO $$
BEGIN
    BEGIN
        INSERT INTO comment (comment_id, post_id, author_id, parent_id, content)
        VALUES (90, 1, 1, 90, 'invalid self parent');
        RAISE EXCEPTION 'Q9 failed: self-parent was accepted';
    EXCEPTION
        WHEN raise_exception THEN
            IF SQLERRM = 'Q9 failed: self-parent was accepted' THEN
                RAISE;
            END IF;
    END;
END;
$$;

-- Q10: thêm bạn mới phải cập nhật hai bộ đếm.
CALL proc_add_friend(1, 6);

DO $$
DECLARE
    v_count BIGINT;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM friendship
    WHERE user_a = 1 AND user_b = 6;
    IF v_count <> 1 THEN
        RAISE EXCEPTION 'Q10 failed: friendship (1,6) missing';
    END IF;

    IF (SELECT friend_count FROM users WHERE user_id = 1) <>
       (SELECT COUNT(*) FROM friend_edge WHERE a = 1)
       OR (SELECT friend_count FROM users WHERE user_id = 6) <>
       (SELECT COUNT(*) FROM friend_edge WHERE a = 6) THEN
        RAISE EXCEPTION 'Q10 failed: friend counters are inconsistent';
    END IF;
END;
$$;

-- Q11: chuyển vào hậu duệ phải bị từ chối.
DO $$
BEGIN
    BEGIN
        CALL proc_move_comment(1, 3);
        RAISE EXCEPTION 'Q11 failed: cycle move was accepted';
    EXCEPTION
        WHEN raise_exception THEN
            IF SQLERRM = 'Q11 failed: cycle move was accepted' THEN
                RAISE;
            END IF;
    END;
END;
$$;

-- Q11: không được chuyển sang cha thuộc bài viết khác.
DO $$
BEGIN
    BEGIN
        CALL proc_move_comment(1, 5);
        RAISE EXCEPTION 'Q11 failed: cross-post move was accepted';
    EXCEPTION
        WHEN raise_exception THEN
            IF SQLERRM = 'Q11 failed: cross-post move was accepted' THEN
                RAISE;
            END IF;
    END;
END;
$$;

-- Q12: dữ liệu tìm kiếm có ký tự SQL không được thực thi như mã lệnh.
DO $$
DECLARE
    v_count BIGINT;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM fn_search_posts_dynamic($q$x' OR 1=1 --$q$);
    IF v_count <> 0 THEN
        RAISE EXCEPTION 'Q12 failed: injection-like input returned % rows', v_count;
    END IF;
END;
$$;

ROLLBACK;

\echo 'Task 3 regression checks passed'
