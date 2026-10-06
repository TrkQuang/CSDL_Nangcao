"""
FILE: sql_advanced/embedded/psycopg2_cursor.py
MỤC ĐÍCH: Minh họa SQL nhúng (Embedded SQL) trong ứng dụng thông qua Python và thư viện psycopg2.
          Sử dụng con trỏ (Cursor), tham số hóa câu truy vấn (Parameterized Queries)
          để ngăn chặn SQL Injection và quản lý Transaction an toàn.
PHỤ TRÁCH: TV3.
"""

import os
import sys

# Khung kết nối CSDL PostgreSQL mẫu
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "detai17_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASS", "postgres"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}

def demo_embedded_query(user_id: int):
    """
    [VÍ DỤ MẪU]: Truy vấn danh sách bạn bè của một người dùng thông qua Cursor
    """
    try:
        import psycopg2
    except ImportError:
        print("[LỖI]: Chưa cài đặt thư viện psycopg2. Chạy: pip install -r requirements.txt")
        return

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Dùng tham số %s an toàn thay vì format string
        query = """
            SELECT u.user_id, u.full_name, u.email
            FROM friend_edge fe
            JOIN users u ON fe.b = u.user_id
            WHERE fe.a = %s
            ORDER BY u.user_id;
        """
        cursor.execute(query, (user_id,))
        records = cursor.fetchall()

        print(f"=== Danh sách bạn bè của User ID {user_id} ===")
        for row in records:
            print(f"- ID: {row[0]}, Tên: {row[1]}, Email: {row[2]}")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"[LỖI KHI THỰC THI]: {e}")

if __name__ == "__main__":
    print("Script minh họa Embedded SQL (Python + psycopg2)")
    # demo_embedded_query(1)
