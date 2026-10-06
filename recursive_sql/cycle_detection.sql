-- ============================================================================
-- FILE: recursive_sql/cycle_detection.sql
-- MỤC ĐÍCH: Phát hiện chu trình (Cycle Detection) trong đồ thị bạn bè và cây phân cấp.
--           Đối chiếu với số lượng chu trình đếm được bằng Cypher trên Neo4j.
-- PHỤ TRÁCH: TV3 (Hỗ trợ: TV4).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [VÍ DỤ MẪU R3]: Phát hiện và liệt kê các chu trình độ dài từ 3 đến 5
-- Kết quả kỳ vọng trên seed_test: 3 chu trình cơ bản:
--   - Tam giác: (1, 2, 3)
--   - Chu trình 4: (2, 3, 5, 4)
--   - Chu trình 5: (1, 2, 4, 5, 3)
-- ----------------------------------------------------------------------------
WITH RECURSIVE graph_cycle AS (
    -- Điểm neo: Bắt đầu từ mỗi đỉnh, quy ước bắt đầu từ min_id để tránh đếm trùng chiều
    SELECT 
        a AS start_node,
        b AS current_node,
        1 AS path_length,
        ARRAY[a, b] AS path
    FROM friend_edge
    WHERE a < b

    UNION ALL

    -- Bước đệ quy
    SELECT 
        gc.start_node,
        fe.b AS current_node,
        gc.path_length + 1,
        gc.path || fe.b
    FROM friend_edge fe
    JOIN graph_cycle gc ON fe.a = gc.current_node
    WHERE gc.path_length < 5
      AND (
          -- Trường hợp đóng vòng: quay về start_node khi độ dài >= 3
          (fe.b = gc.start_node AND gc.path_length >= 2)
          -- Hoặc nút chưa từng xuất hiện trên đường đi
          OR (NOT fe.b = ANY(gc.path) AND fe.b > gc.start_node)
      )
)
SELECT 
    path AS cycle_path,
    path_length
FROM graph_cycle
WHERE current_node = start_node
ORDER BY path_length;
