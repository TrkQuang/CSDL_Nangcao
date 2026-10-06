"""
FILE: benchmark/scripts/run_benchmark.py
MỤC ĐÍCH: Script tự động hóa quy trình benchmark:
          - Kết nối tới PostgreSQL
          - Chạy các câu truy vấn Q1-Q10 trên 4 mô hình cây
          - Thực thi lệnh EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
          - Trích xuất: Planning Time, Execution Time, Shared Hit/Read Blocks
          - Ghi kết quả vào file CSV results/benchmark_results.csv
PHỤ TRÁCH: TV5.
"""

import time
import os
import csv

def run_benchmark_skeleton():
    """
    [VÍ DỤ MẪU]: Khung thực thi đo lường và ghi kết quả ra CSV
    """
    print("=== Khung chạy Benchmark tự động cho Đề tài 17 ===")
    
    # Danh sách các câu đo mẫu
    benchmark_tasks = [
        {"model": "Adjacency List", "query": "Q2_Subtree", "data_size": "1000", "has_index": True},
        {"model": "Path Enumeration", "query": "Q2_Subtree", "data_size": "1000", "has_index": True},
        {"model": "Nested Set", "query": "Q2_Subtree", "data_size": "1000", "has_index": True},
        {"model": "Closure Table", "query": "Q2_Subtree", "data_size": "1000", "has_index": True},
    ]
    
    print("Danh sách các trường hợp cần đo:")
    for t in benchmark_tasks:
        print(f"- Mô hình: {t['model']:<18} | Truy vấn: {t['query']:<12} | N = {t['data_size']}")
        
    print("\n[TODO: TV5]: Sử dụng psycopg2 kết nối database, chạy EXPLAIN ANALYZE và trích xuất JSON plan.")

if __name__ == "__main__":
    run_benchmark_skeleton()
