"""
FILE: benchmark/scripts/gen_tree_data.py
MỤC ĐÍCH: Sinh dữ liệu cây bình luận quy mô lớn (1k, 10k, 100k nodes) với seed cố định
          để đảm bảo khả năng tái lập kết quả thực nghiệm.
          Tự động tính toán các trường tương ứng cho cả 4 mô hình:
          1. parent_id (Adjacency List)
          2. path (ltree)
          3. lft, rgt (Nested Set)
          4. ancestor, descendant, depth (Closure Table)
PHỤ TRÁCH: TV5 (Hỗ trợ: TV2).
"""

import random
import sys

SEED = 42
random.seed(SEED)

def generate_tree(num_nodes: int = 1000, max_children: int = 5):
    """
    [VÍ DỤ MẪU]: Hàm sinh cấu trúc cây ngẫu nhiên và in mẫu 10 node đầu tiên
    """
    print(f"=== Sinh cây với {num_nodes} nút (Random Seed = {SEED}) ===")
    
    # Danh sách các nút: mỗi nút lưu (node_id, parent_id)
    nodes = [(1, None)] # Node gốc đầu tiên
    
    for node_id in range(2, num_nodes + 1):
        # Chọn ngẫu nhiên một nút cha trong số các nút đã có
        parent_id = random.choice([n[0] for n in nodes])
        nodes.append((node_id, parent_id))
        
    print(f"Đã tạo {len(nodes)} nút thành công.")
    print("Mẫu 10 nút đầu tiên (node_id, parent_id):")
    for item in nodes[:10]:
        print(f"  Node {item[0]} -> Parent {item[1]}")

    # TODO: TV5 bổ sung logic xuất file SQL INSERT hoặc CSV nạp nhanh bằng COPY:
    # - Duyệt cây theo chiều sâu (DFS) để gán lft, rgt cho Nested Set
    # - Tính chuỗi path nối các id cho ltree
    # - Tạo bảng bao đóng cho Closure Table

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    generate_tree(count)
