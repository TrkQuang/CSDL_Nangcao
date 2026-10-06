-- ============================================================================
-- FILE: database/schema.sql
-- MỤC ĐÍCH: Định nghĩa Lược đồ CSDL chung (DDL) cho Đề tài 17 trên PostgreSQL.
--           Bao gồm bảng người dùng, quan hệ bạn bè/theo dõi, nhóm, bài viết,
--           bình luận và 4 mô hình lưu trữ cây.
-- PHỤ TRÁCH CHÍNH: TV3 (Hỗ trợ: TV5 | Review: TV1).
-- THỜI HẠN: Cần chốt trước tuần 6.
-- ============================================================================

-- Bật extension cần thiết (cho mô hình Path Enumeration)
CREATE EXTENSION IF NOT EXISTS ltree;

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU 1]: Bảng Người dùng (users)
-- Ràng buộc: Email duy nhất, friend_count là thuộc tính dẫn xuất không âm
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id      SERIAL PRIMARY KEY,
    full_name    VARCHAR(100) NOT NULL,
    email        VARCHAR(150) NOT NULL UNIQUE,
    friend_count INT NOT NULL DEFAULT 0 CHECK (friend_count >= 0),
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU 2]: Quan hệ Kết bạn vô hướng (friendship) và View 2 chiều
-- Quy ước: user_a < user_b để mỗi cặp bạn bè chỉ lưu đúng 1 dòng (BR2)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS friendship (
    user_a INT REFERENCES users(user_id) ON DELETE CASCADE,
    user_b INT REFERENCES users(user_id) ON DELETE CASCADE,
    since  TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_a, user_b),
    CHECK (user_a < user_b)
);

-- View hỗ trợ duyệt đồ thị hai chiều đối xứng
CREATE OR REPLACE VIEW friend_edge AS
    SELECT user_a AS a, user_b AS b FROM friendship
    UNION ALL
    SELECT user_b, user_a FROM friendship;

-- ----------------------------------------------------------------------------
-- [TODO: TV3 triển khai khung các bảng tiếp theo]
-- ----------------------------------------------------------------------------

-- 1. Bảng theo dõi có hướng (follow: follower_id, followee_id)
CREATE TABLE IF NOT EXISTS follow (
    follower_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    followee_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    PRIMARY KEY (follower_id, followee_id),
    CHECK (follower_id <> followee_id)
);

-- 2. Bảng nhóm học tập (study_group: group_id, name, topic, is_private, owner_id)
CREATE TABLE IF NOT EXISTS study_group (
    group_id   SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    topic      VARCHAR(50)  NOT NULL,
    is_private BOOLEAN NOT NULL DEFAULT false,
    owner_id   INT NOT NULL REFERENCES users(user_id)
);

-- 3. Bảng thành viên nhóm (group_member: group_id, user_id, role, joined_at)
CREATE TABLE IF NOT EXISTS group_member (
    group_id  INT REFERENCES study_group(group_id) ON DELETE CASCADE,
    user_id   INT REFERENCES users(user_id) ON DELETE CASCADE,
    role      VARCHAR(10) NOT NULL DEFAULT 'member' CHECK (role IN ('owner','mod','member')),
    joined_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (group_id, user_id)
);

-- 4. Bảng bài viết (post: post_id, group_id, author_id, post_type, title, content, created_at)
CREATE TABLE IF NOT EXISTS post (
    post_id    SERIAL PRIMARY KEY,
    group_id   INT NOT NULL REFERENCES study_group(group_id),
    author_id  INT NOT NULL REFERENCES users(user_id),
    post_type  VARCHAR(10) NOT NULL CHECK (post_type IN ('thaoluan','tailieu')),
    title      VARCHAR(200) NOT NULL,
    content    TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 5. Bảng cảm xúc (post_reaction: post_id, user_id, kind)
CREATE TABLE IF NOT EXISTS post_reaction (
    post_id INT REFERENCES post(post_id) ON DELETE CASCADE,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    kind    VARCHAR(10) NOT NULL DEFAULT 'like',
    PRIMARY KEY (post_id, user_id)
);

-- 6. Mô hình cây 1: Adjacency List (comment)
CREATE TABLE IF NOT EXISTS comment (
    comment_id SERIAL PRIMARY KEY,
    post_id    INT NOT NULL REFERENCES post(post_id) ON DELETE CASCADE,
    author_id  INT NOT NULL REFERENCES users(user_id),
    parent_id  INT REFERENCES comment(comment_id) ON DELETE CASCADE,
    content    TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 7. Mô hình cây 2: Path Enumeration (comment_path)
CREATE TABLE IF NOT EXISTS comment_path (
    comment_id INT PRIMARY KEY REFERENCES comment(comment_id) ON DELETE CASCADE,
    post_id    INT NOT NULL REFERENCES post(post_id),
    path       ltree NOT NULL
);

-- 8. Mô hình cây 3: Nested Set (comment_ns)
CREATE TABLE IF NOT EXISTS comment_ns (
    comment_id INT PRIMARY KEY REFERENCES comment(comment_id) ON DELETE CASCADE,
    post_id    INT NOT NULL REFERENCES post(post_id),
    lft        INT NOT NULL,
    rgt        INT NOT NULL,
    CHECK (lft < rgt)
);

-- 9. Mô hình cây 4: Closure Table (comment_closure)
CREATE TABLE IF NOT EXISTS comment_closure (
    ancestor   INT REFERENCES comment(comment_id) ON DELETE CASCADE,
    descendant INT REFERENCES comment(comment_id) ON DELETE CASCADE,
    depth      INT NOT NULL,
    PRIMARY KEY (ancestor, descendant)
);

-- 10. Cây thư mục tài liệu đối chứng (folder)
CREATE TABLE IF NOT EXISTS folder (
    folder_id SERIAL PRIMARY KEY,
    parent_id INT REFERENCES folder(folder_id) ON DELETE CASCADE,
    group_id  INT NOT NULL REFERENCES study_group(group_id),
    name      VARCHAR(100) NOT NULL
);
