"""
FILE: benchmark/scripts/gen_graph_data.py
MỤC ĐÍCH: Sinh dữ liệu đồ thị mạng xã hội (User Nodes và Friendship Edges)
          với quy mô tùy chọn (ví dụ: 10.000 users, 50.000 edges)
          phục vụ đo đạc hiệu năng WITH RECURSIVE vs Neo4j.
PHỤ TRÁCH: TV5 (Hỗ trợ: TV4).
"""

import random
import sys

SEED = 42
random.seed(SEED)

def generate_graph(num_users: int = 1000, num_edges: int = 5000):
    """
    [VÍ DỤ MẪU]: Sinh danh sách cạnh bạn bè vô hướng (user_a < user_b)
    """
    print(f"=== Sinh đồ thị {num_users} users, {num_edges} edges (Seed = {SEED}) ===")
    edges = set()
    
    attempts = 0
    max_attempts = num_edges * 10
    
    while len(edges) < num_edges and attempts < max_attempts:
        u1 = random.randint(1, num_users)
        u2 = random.randint(1, num_users)
        attempts += 1
        if u1 != u2:
            a, b = (u1, u2) if u1 < u2 else (u2, u1)
            edges.add((a, b))
            
    print(f"Đã tạo {len(edges)} cạnh bạn bè duy nhất.")
    print("Mẫu 5 cạnh đầu tiên (user_a, user_b):")
    for edge in list(edges)[:5]:
        print(f"  {edge[0]} <-> {edge[1]}")
        
    # TODO: TV5 viết hàm lưu ra file SQL hoặc file CSV để import vào PostgreSQL & Neo4j.

if __name__ == "__main__":
    generate_graph()
