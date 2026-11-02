"""
Script vẽ bổ sung 5 sơ đồ kiến trúc và biểu đồ chuyên sâu chuẩn học thuật (300 DPI):
1. Sơ đồ Lược đồ CSDL Quan hệ Vật lý (relational_schema_diagram.png)
2. Sơ đồ Cấu trúc trực quan 4 Mô hình Cây phân cấp (tree_models_comparison_diagram.png)
3. Sơ đồ Đồ thị Chờ khóa Deadlock WFG (concurrency_wfg_diagram.png)
4. Sơ đồ Kiến trúc Đa lưu trữ Polyglot Persistence (polyglot_architecture_diagram.png)
5. Biểu đồ Dung lượng Lưu trữ Vật lý tại 100k nút (benchmark_storage_chart.png)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Ellipse, Polygon
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def draw_relational_schema_diagram():
    out_path = ROOT / "docs" / "relational_schema_diagram.png"
    print(f"-> Đang vẽ Sơ đồ Lược đồ CSDL Quan hệ Vật lý tại: {out_path}")
    
    fig, ax = plt.subplots(figsize=(20, 14), dpi=300)
    ax.set_xlim(0, 2000)
    ax.set_ylim(0, 1400)
    ax.axis("off")
    fig.patch.set_facecolor('#FFFFFF')

    C_HDR = '#1E3A8A'
    C_ROW_ALT = '#F8FAFC'
    C_BORDER = '#3B82F6'
    C_PK = '#B45309'
    C_FK = '#047857'
    C_TEXT = '#0F172A'

    def draw_table_box(x, y, w, title, columns):
        row_h = 24
        header_h = 36
        total_h = header_h + len(columns) * row_h
        
        # Viền ngoài
        rect = FancyBboxPatch((x, y - total_h), w, total_h, boxstyle="square,pad=0",
                              facecolor='#FFFFFF', edgecolor=C_BORDER, linewidth=1.8, zorder=3)
        ax.add_patch(rect)
        
        # Header
        h_rect = FancyBboxPatch((x, y - header_h), w, header_h, boxstyle="square,pad=0",
                                facecolor=C_HDR, edgecolor=C_BORDER, linewidth=1.8, zorder=4)
        ax.add_patch(h_rect)
        ax.text(x + w/2, y - header_h/2, title, ha='center', va='center',
                fontsize=11, fontweight='bold', color='#FFFFFF', zorder=5)

        # Columns
        curr_y = y - header_h
        for idx, (col_name, col_type, col_key) in enumerate(columns):
            bg = C_ROW_ALT if idx % 2 == 1 else '#FFFFFF'
            r_rect = FancyBboxPatch((x, curr_y - row_h), w, row_h, boxstyle="square,pad=0",
                                    facecolor=bg, edgecolor='#E2E8F0', linewidth=0.8, zorder=3)
            ax.add_patch(r_rect)

            key_text = f"[{col_key}] " if col_key else ""
            key_color = C_PK if 'PK' in col_key else (C_FK if 'FK' in col_key else C_TEXT)
            
            ax.text(x + 10, curr_y - row_h/2, key_text + col_name, ha='left', va='center',
                    fontsize=9, fontweight=('bold' if col_key else 'normal'), color=key_color, zorder=4)
            ax.text(x + w - 10, curr_y - row_h/2, col_type, ha='right', va='center',
                    fontsize=8.5, fontstyle='italic', color='#475569', zorder=4)
            curr_y -= row_h

    # Tiêu đề
    ax.text(1000, 1360, "LƯỢC ĐỒ CƠ SỞ DỮ LIỆU QUAN HỆ VẬT LÝ (PHYSICAL RELATIONAL SCHEMA)",
            ha='center', va='center', fontsize=17, fontweight='bold', color='#1E3A8A')
    ax.text(1000, 1325, "HỆ THỐNG MẠNG XÃ HỘI HỌC TẬP — HỆ QUẢN TRỊ POSTGRESQL 18.6",
            ha='center', va='center', fontsize=11, fontstyle='italic', color='#475569')

    # Bảng USERS
    draw_table_box(60, 1260, 360, "users", [
        ("user_id", "INT GENERATED ALWAYS", "PK"),
        ("email", "VARCHAR(255) UNIQUE", "U"),
        ("full_name", "VARCHAR(150)", ""),
        ("password_hash", "VARCHAR(255)", ""),
        ("friend_count", "INT DEFAULT 0", ""),
        ("reputation", "INT DEFAULT 0", ""),
        ("created_at", "TIMESTAMPTZ DEFAULT NOW()", "")
    ])

    # Bảng STUDY_GROUP
    draw_table_box(560, 1260, 360, "study_group", [
        ("group_id", "INT GENERATED ALWAYS", "PK"),
        ("name", "VARCHAR(150) UNIQUE", "U"),
        ("topic", "VARCHAR(100)", ""),
        ("owner_id", "INT REFERENCES users", "FK"),
        ("is_private", "BOOLEAN DEFAULT FALSE", ""),
        ("created_at", "TIMESTAMPTZ DEFAULT NOW()", "")
    ])

    # Bảng GROUP_MEMBERS
    draw_table_box(1060, 1260, 380, "group_members", [
        ("group_id", "INT REFERENCES study_group", "PK, FK1"),
        ("user_id", "INT REFERENCES users", "PK, FK2"),
        ("role", "VARCHAR(20) ('owner'|'mod')", ""),
        ("joined_at", "TIMESTAMPTZ DEFAULT NOW()", "")
    ])

    # Bảng FRIENDSHIP
    draw_table_box(1560, 1260, 380, "friendship", [
        ("user_a", "INT REFERENCES users", "PK, FK1"),
        ("user_b", "INT REFERENCES users", "PK, FK2"),
        ("status", "VARCHAR(20) ('accepted')", ""),
        ("since", "TIMESTAMPTZ DEFAULT NOW()", ""),
        ("CHECK", "user_a < user_b", "CHK")
    ])

    # Bảng POST
    draw_table_box(60, 880, 380, "post", [
        ("post_id", "INT GENERATED ALWAYS", "PK"),
        ("author_id", "INT REFERENCES users", "FK1"),
        ("group_id", "INT REFERENCES study_group", "FK2"),
        ("title", "VARCHAR(255)", ""),
        ("content", "TEXT", ""),
        ("post_type", "VARCHAR(20) ('thaoluan'|'tailieu')", "CHK"),
        ("is_closed", "BOOLEAN DEFAULT FALSE", ""),
        ("file_url", "VARCHAR(500)", ""),
        ("comment_count", "INT DEFAULT 0", ""),
        ("reaction_count", "INT DEFAULT 0", ""),
        ("created_at", "TIMESTAMPTZ DEFAULT NOW()", "")
    ])

    # Bảng POST_REACTION
    draw_table_box(560, 880, 360, "post_reaction", [
        ("user_id", "INT REFERENCES users", "PK, FK1"),
        ("post_id", "INT REFERENCES post", "PK, FK2"),
        ("kind", "VARCHAR(20) ('like'|'love')", "CHK"),
        ("created_at", "TIMESTAMPTZ DEFAULT NOW()", "")
    ])

    # Bảng COMMENT_ADJACENCY
    draw_table_box(1060, 880, 400, "comment_adjacency (Mô hình 1)", [
        ("comment_id", "INT GENERATED ALWAYS", "PK"),
        ("post_id", "INT REFERENCES post", "FK1"),
        ("author_id", "INT REFERENCES users", "FK2"),
        ("parent_id", "INT REFERENCES comment_adj", "FK3"),
        ("content", "TEXT", ""),
        ("created_at", "TIMESTAMPTZ DEFAULT NOW()", "")
    ])

    # Bảng COMMENT_PATH_ENUM
    draw_table_box(1560, 880, 380, "comment_path_enum (Mô hình 2)", [
        ("comment_id", "INT GENERATED ALWAYS", "PK"),
        ("post_id", "INT REFERENCES post", "FK1"),
        ("author_id", "INT REFERENCES users", "FK2"),
        ("path", "ltree NOT NULL (Chỉ mục GiST)", "IDX"),
        ("content", "TEXT", ""),
        ("created_at", "TIMESTAMPTZ DEFAULT NOW()", "")
    ])

    # Bảng COMMENT_NESTED_SET
    draw_table_box(60, 460, 380, "comment_nested_set (Mô hình 3)", [
        ("comment_id", "INT GENERATED ALWAYS", "PK"),
        ("post_id", "INT REFERENCES post", "FK1"),
        ("author_id", "INT REFERENCES users", "FK2"),
        ("lft", "INT NOT NULL", "IDX"),
        ("rgt", "INT NOT NULL", "IDX"),
        ("content", "TEXT", ""),
        ("CHECK", "lft < rgt", "CHK")
    ])

    # Bảng COMMENT_CLOSURE
    draw_table_box(560, 460, 380, "comment_closure (Mô hình 4 - Bảng phụ)", [
        ("ancestor_id", "INT REFERENCES data(c_id)", "PK, FK1"),
        ("descendant_id", "INT REFERENCES data(c_id)", "PK, FK2"),
        ("depth", "INT NOT NULL", "")
    ])

    # Bảng FOLDER
    draw_table_box(1060, 460, 380, "folder (Thư mục tài liệu nhóm)", [
        ("folder_id", "INT GENERATED ALWAYS", "PK"),
        ("group_id", "INT REFERENCES study_group", "FK1"),
        ("parent_id", "INT REFERENCES folder", "FK2"),
        ("name", "VARCHAR(100)", ""),
        ("created_at", "TIMESTAMPTZ DEFAULT NOW()", "")
    ])

    # Bảng NOTIFICATION
    draw_table_box(1560, 460, 380, "notification (Thông báo tương tác)", [
        ("notif_id", "INT GENERATED ALWAYS", "PK"),
        ("user_id", "INT REFERENCES users", "FK1"),
        ("message", "TEXT", ""),
        ("is_read", "BOOLEAN DEFAULT FALSE", ""),
        ("created_at", "TIMESTAMPTZ DEFAULT NOW()", "")
    ])

    # Chú thích góc dưới
    ax.text(1000, 80, "Liên kết khóa ngoại: users (1) <---> (N) post | post (1) <---> (N) comment | users (1) <---> (N) study_group\nRàng buộc toàn vẹn: ON DELETE CASCADE cho bình luận, ON DELETE RESTRICT cho tài khoản đang sở hữu nhóm.",
            ha='center', va='center', fontsize=9.5, fontstyle='italic', color='#334155',
            bbox=dict(boxstyle='round,pad=6', facecolor='#F1F5F9', edgecolor='#CBD5E1'))

    plt.tight_layout()
    plt.savefig(str(out_path), bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"-> Đã vẽ xong Lược đồ CSDL Quan hệ: {out_path} ({out_path.stat().st_size} bytes)")

def draw_tree_comparison_diagram():
    out_path = ROOT / "docs" / "tree_models_comparison_diagram.png"
    print(f"-> Đang vẽ Sơ đồ So sánh 4 Mô hình Cây tại: {out_path}")
    
    fig, ax = plt.subplots(figsize=(18, 11), dpi=300)
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 1000)
    ax.axis("off")
    fig.patch.set_facecolor('#FFFFFF')

    # Tiêu đề
    ax.text(800, 960, "CƠ SỞ DỮ LIỆU PHÂN CẤP: SO SÁNH CẤU TRÚC LƯU TRỮ 4 MÔ HÌNH CÂY",
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1E3A8A')
    ax.text(800, 930, "Biểu diễn cây bình luận gồm 6 nút thảo luận (c1 đến c6) trên PostgreSQL",
            ha='center', va='center', fontsize=10.5, fontstyle='italic', color='#475569')

    # Vẽ cây mẫu ở trung tâm trên
    ax.text(800, 880, "CÂY BÌNH LUẬN MẪU (GROUND TRUTH TREE)", ha='center', va='center', fontsize=11, fontweight='bold', color='#0F172A')
    
    def draw_node(cx, cy, label, sub=""):
        c = Ellipse((cx, cy), 80, 50, facecolor='#DBEAFE', edgecolor='#1D4ED8', linewidth=1.8, zorder=4)
        ax.add_patch(c)
        ax.text(cx, cy + (4 if sub else 0), label, ha='center', va='center', fontsize=11, fontweight='bold', color='#1E3A8A', zorder=5)
        if sub:
            ax.text(cx, cy - 12, sub, ha='center', va='center', fontsize=8, color='#475569', zorder=5)

    def draw_edge(p1, p2):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#64748B', linewidth=1.5, zorder=2)

    # Vị trí các nút
    p_c1 = (800, 810)
    p_c2 = (600, 720)
    p_c3 = (1000, 720)
    p_c4 = (600, 630)
    p_c5 = (900, 630)
    p_c6 = (1100, 630)

    draw_edge(p_c1, p_c2)
    draw_edge(p_c1, p_c3)
    draw_edge(p_c2, p_c4)
    draw_edge(p_c3, p_c5)
    draw_edge(p_c3, p_c6)

    draw_node(p_c1[0], p_c1[1], "c1 (Gốc)", "depth=1")
    draw_node(p_c2[0], p_c2[1], "c2", "depth=2")
    draw_node(p_c3[0], p_c3[1], "c3", "depth=2")
    draw_node(p_c4[0], p_c4[1], "c4 (Lá)", "depth=3")
    draw_node(p_c5[0], p_c5[1], "c5 (Lá)", "depth=3")
    draw_node(p_c6[0], p_c6[1], "c6 (Lá)", "depth=3")

    # 4 Hộp đại diện 4 mô hình ở nửa dưới
    def draw_model_card(x, y, w, h, title, subtitle, rows, color):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=4,rounding_size=6",
                              facecolor='#F8FAFC', edgecolor=color, linewidth=2, zorder=3)
        ax.add_patch(rect)
        
        # Header card
        hh = 45
        h_rect = FancyBboxPatch((x, y + h - hh), w, hh, boxstyle="round,pad=4,rounding_size=6",
                                facecolor=color, edgecolor=color, linewidth=2, zorder=4)
        ax.add_patch(h_rect)
        ax.text(x + w/2, y + h - 18, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#FFFFFF', zorder=5)
        ax.text(x + w/2, y + h - 34, subtitle, ha='center', va='center', fontsize=8, fontstyle='italic', color='#E0E7FF', zorder=5)

        curr_y = y + h - hh - 20
        for r_text in rows:
            ax.text(x + 12, curr_y, r_text, ha='left', va='center', fontsize=8.5, color='#1E293B', zorder=5)
            curr_y -= 18

    # 1. Adjacency List
    draw_model_card(40, 80, 350, 480, "1. ADJACENCY LIST", "Con trỏ cha trực tiếp (parent_id)", [
        "c1: parent_id = NULL (Nút gốc)",
        "c2: parent_id = 1",
        "c3: parent_id = 1",
        "c4: parent_id = 2",
        "c5: parent_id = 3",
        "c6: parent_id = 3",
        "------------------------------------",
        "• Ưu điểm: Ghi cực nhanh O(1).",
        "• Nhược điểm: Đọc cây con phải dùng",
        "  WITH RECURSIVE lặp nhiều vòng.",
        "• Chỉ mục: B-Tree trên parent_id."
    ], '#2563EB')

    # 2. Path Enumeration
    draw_model_card(420, 80, 360, 480, "2. PATH ENUMERATION", "Đường dẫn tiền tố ltree", [
        "c1: path = '1'",
        "c2: path = '1.2'",
        "c3: path = '1.3'",
        "c4: path = '1.2.4'",
        "c5: path = '1.3.5'",
        "c6: path = '1.3.6'",
        "------------------------------------",
        "• Ưu điểm: Đọc cây con bằng <@ rất nhanh;",
        "  Ghi chèn lá chỉ O(1) ghép chuỗi.",
        "• Không bùng nổ dung lượng đĩa.",
        "• Chỉ mục: GiST trên cột path."
    ], '#059669')

    # 3. Nested Set
    draw_model_card(810, 80, 360, 480, "3. NESTED SET", "Khoảng lồng nhau (lft, rgt)", [
        "c1: [lft=1,  rgt=12]",
        "c2: [lft=2,  rgt=5]",
        "c3: [lft=6,  rgt=11]",
        "c4: [lft=3,  rgt=4] (Lá: rgt=lft+1)",
        "c5: [lft=7,  rgt=8] (Lá)",
        "c6: [lft=9,  rgt=10] (Lá)",
        "------------------------------------",
        "• Ưu điểm: Đọc cây con cực nhanh O(1)",
        "  bằng phép quét lft BETWEEN p_lft AND p_rgt.",
        "• Nhược điểm: Ghi chèn lá cực chậm O(N)",
        "  phải UPDATE dịch chuyển toàn cây!"
    ], '#D97706')

    # 4. Closure Table
    draw_model_card(1200, 80, 360, 480, "4. CLOSURE TABLE", "Bảng phụ bao đóng (ancestor, desc, depth)", [
        "c1: (1,1,0)",
        "c2: (1,2,1), (2,2,0)",
        "c3: (1,3,1), (3,3,0)",
        "c4: (1,4,2), (2,4,1), (4,4,0)",
        "c5: (1,5,2), (3,5,1), (5,5,0)",
        "c6: (1,6,2), (3,6,1), (6,6,0)",
        "------------------------------------",
        "• Ưu điểm: Đọc cây con & tổ tiên bằng JOIN.",
        "• Nhược điểm: Bùng nổ dung lượng đĩa O(N^2)",
        "  100k nút sinh ra hơn 1.06 triệu dòng!"
    ], '#7C3AED')

    plt.tight_layout()
    plt.savefig(str(out_path), bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"-> Đã vẽ xong Sơ đồ 4 Mô hình Cây: {out_path} ({out_path.stat().st_size} bytes)")

def draw_deadlock_wfg_diagram():
    out_path = ROOT / "docs" / "concurrency_wfg_diagram.png"
    print(f"-> Đang vẽ Sơ đồ Bế tắc Deadlock WFG tại: {out_path}")
    
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 900)
    ax.axis("off")
    fig.patch.set_facecolor('#FFFFFF')

    # Tiêu đề
    ax.text(800, 860, "ĐIỀU KHIỂN ĐỒNG THỜI: THỰC NGHIỆM BẾ TẮC (DEADLOCK T3)",
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1E3A8A')
    ax.text(800, 830, "Chu trình phụ thuộc khóa trong Đồ thị Chờ (Wait-For Graph - WFG) & Mã lỗi 40P01",
            ha='center', va='center', fontsize=10.5, fontstyle='italic', color='#475569')

    # Khung Session A & B
    def draw_session_box(x, y, w, h, title, subtitle, pid, color):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=5,rounding_size=6",
                              facecolor='#F8FAFC', edgecolor=color, linewidth=2, zorder=3)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 25, title, ha='center', va='center', fontsize=12, fontweight='bold', color=color, zorder=4)
        ax.text(x + w/2, y + h - 45, f"PID: {pid} — {subtitle}", ha='center', va='center', fontsize=9, fontstyle='italic', color='#475569', zorder=4)

    draw_session_box(100, 360, 420, 420, "PHIÊN 1: SESSION A", "Giao dịch 1", "16484", '#DC2626')
    draw_session_box(1080, 360, 420, 420, "PHIÊN 2: SESSION B", "Giao dịch 2", "13804", '#2563EB')

    # Tài nguyên User 1 & User 2 ở giữa
    def draw_res_box(cx, cy, label, sub):
        rect = FancyBboxPatch((cx - 130, cy - 45), 260, 90, boxstyle="round,pad=4,rounding_size=6",
                              facecolor='#FEF3C7', edgecolor='#D97706', linewidth=2, zorder=3)
        ax.add_patch(rect)
        ax.text(cx, cy + 10, label, ha='center', va='center', fontsize=11, fontweight='bold', color='#B45309', zorder=4)
        ax.text(cx, cy - 14, sub, ha='center', va='center', fontsize=8.5, color='#78350F', zorder=4)

    draw_res_box(800, 680, "TÀI NGUYÊN: DÒNG USER 1", "tuple (0, 1) in relation 'users'")
    draw_res_box(800, 460, "TÀI NGUYÊN: DÒNG USER 2", "tuple (0, 2) in relation 'users'")

    # Mũi tên Giữ khóa (Solid Arrow) và Chờ khóa (Dashed Red Arrow)
    # Session A GIỮ User 1
    ax.annotate("", xy=(660, 700), xytext=(520, 700),
                arrowprops=dict(arrowstyle="->", color="#16A34A", lw=2.5))
    ax.text(590, 720, "1. ĐANG GIỮ KHÓA\nExclusiveLock", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#16A34A')

    # Session B GIỮ User 2
    ax.annotate("", xy=(940, 480), xytext=(1080, 480),
                arrowprops=dict(arrowstyle="->", color="#16A34A", lw=2.5))
    ax.text(1010, 500, "2. ĐANG GIỮ KHÓA\nExclusiveLock", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#16A34A')

    # Session A CHỜ User 2
    ax.annotate("", xy=(660, 460), xytext=(520, 460),
                arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2.5, linestyle="--"))
    ax.text(590, 435, "3. YÊU CẦU KHÓA\n(BỊ TREO CHỜ B!)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#DC2626')

    # Session B CHỜ User 1
    ax.annotate("", xy=(940, 680), xytext=(1080, 680),
                arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2.5, linestyle="--"))
    ax.text(1010, 705, "4. YÊU CẦU KHÓA\n(BỊ TREO CHỜ A!)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#DC2626')

    # Vòng tròn chu trình bế tắc ở giữa
    c_dead = Ellipse((800, 570), 180, 70, facecolor='#FEE2E2', edgecolor='#EF4444', linewidth=2, linestyle=':')
    ax.add_patch(c_dead)
    ax.text(800, 570, "CHU TRÌNH BẾ TẮC!\n(Deadlock Detected)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#B91C1C')

    # Hộp thông báo lỗi bên dưới
    ax.text(800, 180, "CƠ CHẾ GIẢI QUYẾT BẾ TẮC CỦA POSTGRESQL (DEADLOCK DETECTOR):\n"
                      "1. Sau tham số deadlock_timeout = 1000ms, hệ thống phát hiện chu trình Session A → Session B → Session A trong Đồ thị Chờ (WFG).\n"
                      "2. PostgreSQL tự động chọn nạn nhân (Victim): Ngắt Session A với mã lỗi SQLSTATE: 40P01 (deadlock_detected) để phá vỡ chu trình.\n"
                      "3. Session B được giải phóng tài nguyên và thực hiện COMMIT giao dịch an toàn thành công 100%!",
            ha='center', va='center', fontsize=9.5, color='#0F172A',
            bbox=dict(boxstyle='round,pad=8', facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1.5))

    plt.tight_layout()
    plt.savefig(str(out_path), bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"-> Đã vẽ xong Sơ đồ Deadlock WFG: {out_path} ({out_path.stat().st_size} bytes)")

def draw_polyglot_architecture_diagram():
    out_path = ROOT / "docs" / "polyglot_architecture_diagram.png"
    print(f"-> Đang vẽ Sơ đồ Kiến trúc Đa lưu trữ Polyglot tại: {out_path}")
    
    fig, ax = plt.subplots(figsize=(18, 10), dpi=300)
    ax.set_xlim(0, 1800)
    ax.set_ylim(0, 1000)
    ax.axis("off")
    fig.patch.set_facecolor('#FFFFFF')

    # Tiêu đề
    ax.text(900, 960, "KIẾN TRÚC ĐA LƯU TRỮ (POLYGLOT PERSISTENCE ARCHITECTURE)",
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1E3A8A')
    ax.text(900, 930, "Phối hợp PostgreSQL (Single Source of Truth) và Neo4j (Graph Processing Engine)",
            ha='center', va='center', fontsize=10.5, fontstyle='italic', color='#475569')

    def draw_box(x, y, w, h, title, subtitle, color, bg='#F8FAFC'):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=5,rounding_size=6",
                              facecolor=bg, edgecolor=color, linewidth=2, zorder=3)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 22, title, ha='center', va='center', fontsize=11, fontweight='bold', color=color, zorder=4)
        ax.text(x + w/2, y + h - 42, subtitle, ha='center', va='center', fontsize=8.5, fontstyle='italic', color='#475569', zorder=4)

    # 1. Tầng Client / App
    draw_box(80, 520, 260, 240, "CLIENT APPLICATIONS", "Web UI & Mobile App", '#0369A1')
    ax.text(210, 640, "• React / Vite Client\n• REST / GraphQL API\n• Gửi tương tác học tập", ha='center', va='center', fontsize=9, color='#1E293B', zorder=4)

    # 2. Tầng Backend Services
    draw_box(460, 520, 320, 240, "API BACKEND SERVICES", "Python FastAPI / Node.js", '#4338CA')
    ax.text(620, 640, "• Xử lý nghiệp vụ chính\n• Quản trị phiên & Auth\n• Phân luồng truy vấn:\n  - Giao dịch -> RDBMS\n  - Đồ thị sâu -> Graph", ha='center', va='center', fontsize=9, color='#1E293B', zorder=4)

    # 3. PostgreSQL (Master)
    draw_box(920, 520, 380, 280, "POSTGRESQL 18.6", "Single Source of Truth (SSOT)", '#1E3A8A', '#EFF6FF')
    ax.text(1110, 650, "• Tài khoản, Nhóm, Bài viết\n• Cây bình luận (ltree)\n• ACID Transactions (3,440 TPS)\n• Khóa dòng, B-Tree, GIN, GiST", ha='center', va='center', fontsize=9, color='#1E293B', zorder=4)

    # 4. Message Broker / CDC
    draw_box(920, 180, 380, 180, "DATA SYNC BUS (CDC)", "Debezium / Apache Kafka", '#D97706', '#FEF3C7')
    ax.text(1110, 260, "• Bắt sự kiện thay đổi dữ liệu\n• Đồng bộ phi đồng bộ (Async)\n• Đảm bảo Eventual Consistency", ha='center', va='center', fontsize=9, color='#78350F', zorder=4)

    # 5. Neo4j Graph Engine
    draw_box(1420, 360, 340, 300, "NEO4J 5.x COMMUNITY", "Graph Analysis Engine", '#059669', '#ECFDF5')
    ax.text(1590, 500, "• Mạng lưới bạn bè (FoF)\n• Đường đi ngắn nhất (BFS)\n• Gợi ý môn học & nhóm bạn\n• Index-free Adjacency\n• Ngôn ngữ Cypher trực quan", ha='center', va='center', fontsize=9, color='#064E3B', zorder=4)

    # Các mũi tên liên kết
    def draw_flow_arrow(p1, p2, label):
        ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="->", color="#334155", lw=2))
        mx = (p1[0] + p2[0]) / 2
        my = (p1[1] + p2[1]) / 2 + 15
        ax.text(mx, my, label, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1E40AF',
                bbox=dict(boxstyle='square,pad=1', facecolor='#FFFFFF', edgecolor='none', alpha=0.8))

    draw_flow_arrow((340, 640), (460, 640), "HTTP / JSON")
    draw_flow_arrow((780, 680), (920, 680), "Giao dịch ACID / CRUD")
    draw_flow_arrow((780, 560), (1420, 560), "Truy vấn đồ thị Cypher")
    draw_flow_arrow((1110, 520), (1110, 360), "Ghi log WAL thay đổi")
    draw_flow_arrow((1300, 270), (1460, 360), "Nạp nút & cạnh đồ thị")

    plt.tight_layout()
    plt.savefig(str(out_path), bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"-> Đã vẽ xong Sơ đồ Polyglot: {out_path} ({out_path.stat().st_size} bytes)")

def draw_benchmark_storage_chart():
    out_path = ROOT / "docs" / "benchmark_storage_chart.png"
    print(f"-> Đang vẽ Biểu đồ So sánh Dung lượng Lưu trữ tại: {out_path}")
    
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    models = ['Adjacency List', 'Path Enum (ltree)', 'Nested Set', 'Closure Table']
    heap_sizes = [11.84, 13.48, 12.21, 58.39]
    index_sizes = [4.42, 7.23, 4.79, 34.23]

    x = range(len(models))
    width = 0.45

    b1 = ax.bar(x, heap_sizes, width, label='Dung lượng Bảng chính (Heap - MB)', color='#3B82F6', edgecolor='#1D4ED8')
    b2 = ax.bar(x, index_sizes, width, bottom=heap_sizes, label='Dung lượng Chỉ mục (Index - MB)', color='#10B981', edgecolor='#047857')

    ax.set_ylabel('Dung lượng lưu trữ trên đĩa (Megabytes - MB)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_title('SO SÁNH DUNG LƯỢNG LƯU TRỮ VẬT LÝ TRÊN ĐĨA TẠI QUY MÔ 100.000 BẢN GHI', fontsize=13, fontweight='bold', color='#1E3A8A', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=10.5, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Hiển thị tổng số MB trên đầu mỗi cột
    for i, (h, idx) in enumerate(zip(heap_sizes, index_sizes)):
        tot = h + idx
        ax.text(i, tot + 1.8, f'{tot:.2f} MB\n({(tot/16.26):.1f}x)', ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#0F172A')

    plt.tight_layout()
    plt.savefig(str(out_path), bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"-> Đã vẽ xong Biểu đồ Dung lượng: {out_path} ({out_path.stat().st_size} bytes)")

if __name__ == "__main__":
    draw_relational_schema_diagram()
    draw_tree_comparison_diagram()
    draw_deadlock_wfg_diagram()
    draw_polyglot_architecture_diagram()
    draw_benchmark_storage_chart()
