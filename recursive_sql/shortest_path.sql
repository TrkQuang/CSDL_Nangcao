-- ============================================================================
-- FILE: recursive_sql/shortest_path.sql
-- MỤC ĐÍCH: Tìm đường đi ngắn nhất (Shortest Path) giữa 2 người dùng trong mạng xã hội
--           bằng thuật toán tìm kiếm theo chiều rộng (BFS) qua WITH RECURSIVE.
-- PHỤ TRÁCH: TV3.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU R2]: Tìm đường đi ngắn nhất từ An (user_id = 1) đến Em (user_id = 5)
-- Kết quả kỳ vọng trên seed_test: Đường đi [1, 3, 5] với độ dài là 2
-- ----------------------------------------------------------------------------
WITH RECURSIVE bfs_path AS (
    -- Điểm neo: Bắt đầu từ An (id = 1)
    SELECT 
        1 AS current_node, 
        5 AS target_node, 
        0 AS path_length, 
        ARRAY[1] AS path_nodes

    UNION ALL

    -- Bước đệ quy: Đi theo các cạnh bạn bè
    SELECT 
        fe.b AS current_node, 
        bp.target_node, 
        bp.path_length + 1, 
        bp.path_nodes || fe.b
    FROM friend_edge fe
    JOIN bfs_path bp ON fe.a = bp.current_node
    WHERE NOT (fe.b = ANY(bp.path_nodes)) -- Tránh chu trình
      AND bp.current_node <> bp.target_node -- Dừng khi đã tới đích
      AND bp.path_length < 6                -- Giới hạn bán kính tối đa
)
SELECT 
    path_nodes AS shortest_path, 
    path_length
FROM bfs_path
WHERE current_node = target_node
ORDER BY path_length ASC
LIMIT 1;
