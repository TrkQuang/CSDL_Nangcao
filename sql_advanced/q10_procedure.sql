-- ============================================================================
-- FILE: sql_advanced/q10_procedure.sql
-- MỤC ĐÍCH: Thủ tục lưu trữ (Stored Procedure) kết bạn nguyên tử (Atomic Add Friend)
--           vừa thêm quan hệ friendship vừa đồng thời cập nhật đúng friend_count
--           của cả 2 người dùng trong 1 transaction an toàn.
-- PHỤ TRÁCH: TV3.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU]: Thủ tục proc_add_friend có chuẩn hóa thứ tự và chống tranh chấp
-- ----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE proc_add_friend(
    IN p_user1 INT,
    IN p_user2 INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_a INT;
    v_b INT;
BEGIN
    -- Kiểm tra tự kết bạn với chính mình
    IF p_user1 = p_user2 THEN
        RAISE EXCEPTION 'Không thể tự kết bạn với chính mình (user_id = %)!', p_user1;
    END IF;

    -- Chuẩn hóa thứ tự để luôn thỏa mãn user_a < user_b (BR2)
    IF p_user1 < p_user2 THEN
        v_a := p_user1;
        v_b := p_user2;
    ELSE
        v_a := p_user2;
        v_b := p_user1;
    END IF;

    -- Chèn vào bảng friendship (nếu đã kết bạn rồi thì bỏ qua)
    INSERT INTO friendship (user_a, user_b, since)
    VALUES (v_a, v_b, now())
    ON CONFLICT (user_a, user_b) DO NOTHING;

    -- Cập nhật đồng bộ bộ đếm bạn bè của cả 2 bên
    UPDATE users SET friend_count = (SELECT count(*) FROM friend_edge WHERE a = v_a) WHERE user_id = v_a;
    UPDATE users SET friend_count = (SELECT count(*) FROM friend_edge WHERE a = v_b) WHERE user_id = v_b;

    RAISE NOTICE 'Đã kết bạn thành công giữa user % và user %', v_a, v_b;
END;
$$;

-- ----------------------------------------------------------------------------
-- [LỆNH GỌI THỬ NGHIỆM]:
-- CALL proc_add_friend(1, 6);
-- ----------------------------------------------------------------------------
