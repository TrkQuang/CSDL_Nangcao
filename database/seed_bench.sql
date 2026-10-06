-- ============================================================================
-- FILE: database/seed_bench.sql
-- MỤC ĐÍCH: Script SQL sinh dữ liệu quy mô lớn (1.000, 10.000, 100.000+ dòng)
--           dùng trực tiếp hàm generate_series của PostgreSQL.
--           Phục vụ đo hiệu năng benchmark chỉ mục và so sánh 4 mô hình cây.
-- PHỤ TRÁCH: TV5 (Hỗ trợ: TV3).
-- ============================================================================

-- [VÍ DỤ MẪU]: Sinh nhanh 1.000 người dùng mẫu
/*
INSERT INTO users (full_name, email, created_at)
SELECT 
    'User_' || i,
    'user_' || i || '@test.sgu.vn',
    now() - (i || ' minutes')::interval
FROM generate_series(100, 1099) AS i;
*/

-- ----------------------------------------------------------------------------
-- [TODO: TV5 hoàn thiện script sinh dữ liệu benchmark]
-- 1. Sinh ngẫu nhiên quan hệ bạn bè (Graph edges) đảm bảo tỉ lệ phân bố bậc
-- 2. Sinh cây bình luận phân cấp có độ sâu từ 5 đến 15 cấp
-- 3. Đồng bộ dữ liệu sang 4 bảng mô hình cây:
--    - comment (Adjacency List)
--    - comment_path (Path Enumeration)
--    - comment_ns (Nested Set)
--    - comment_closure (Closure Table)
-- ----------------------------------------------------------------------------
