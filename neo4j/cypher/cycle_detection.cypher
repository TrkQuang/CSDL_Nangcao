// ============================================================================
// FILE: neo4j/cypher/cycle_detection.cypher
// MỤC ĐÍCH: Phát hiện chu trình (Cycle Detection) độ dài 3 đến 5 trong đồ thị bạn bè.
// ĐỐI CHIẾU: Đối chiếu trực tiếp với recursive_sql/cycle_detection.sql (R3) của PostgreSQL.
// PHỤ TRÁCH: TV4 (Chương).
//
// KẾT QUẢ KỲ VỌNG TRÊN SEED_TEST: Đúng 3 chu trình cơ bản:
//   1. Tam giác:   [1, 2, 3, 1]          (Độ dài 3) - An, Binh, Chi
//   2. Tứ giác:    [2, 3, 5, 4, 2]       (Độ dài 4) - Binh, Chi, Em, Dung
//   3. Ngũ giác:   [1, 2, 4, 5, 3, 1]    (Độ dài 5) - An, Binh, Dung, Em, Chi
// ============================================================================

// Tìm chu trình khép kín độ dài từ 3 đến 5
// Khử trùng lặp do hoán vị vòng quanh (cyclic shift) và đối xứng 2 chiều:
// 1. Gốc a có id nhỏ nhất trong chu trình.
// 2. Các đỉnh trung gian không bị lặp.
// 3. Đỉnh thứ 2 có id < đỉnh kế cuối để chỉ đếm 1 chiều duyệt.
MATCH p = (a:User)-[:FRIEND*3..5]-(a)
WHERE ALL(n IN nodes(p)[1..-1] WHERE id(n) <> id(a))
  AND ALL(n IN nodes(p)[1..-1] WHERE a.id < n.id)
  AND (nodes(p)[1]).id < (nodes(p)[-2]).id
RETURN [n IN nodes(p) | n.id] AS cycle_ids,
       [n IN nodes(p) | n.name] AS cycle_names,
       length(p) AS path_length
ORDER BY path_length ASC, cycle_ids ASC;
