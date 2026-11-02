"""
Script vẽ sơ đồ EER và sơ đồ Lớp Hướng Đối Tượng (UML Class Diagram)
chuẩn học thuật, độ phân giải cao (300 DPI) để chèn vào Báo cáo Word.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Ellipse, Polygon
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def draw_eer_diagram():
    out_path = ROOT / "docs" / "eer_diagram.png"
    print(f"-> Đang vẽ sơ đồ EER tại: {out_path}")
    
    fig, ax = plt.subplots(figsize=(20, 14), dpi=300)
    ax.set_xlim(0, 2000)
    ax.set_ylim(0, 1400)
    ax.axis("off")
    fig.patch.set_facecolor('#FFFFFF')

    # Bảng màu chuyên nghiệp
    C_ENT_BG = '#E0F2FE'       # Xanh dương nhạt cho thực thể
    C_ENT_BORDER = '#0369A1'   # Viền thực thể
    C_REL_BG = '#DCFCE7'       # Xanh lục nhạt cho mối kết hợp
    C_REL_BORDER = '#15803D'   # Viền mối kết hợp
    C_ATTR_BG = '#F8FAFC'      # Trắng xám nhạt cho thuộc tính
    C_ATTR_BORDER = '#64748B'  # Viền thuộc tính
    C_PK_BG = '#FEF08A'        # Vàng nhạt cho khóa chính
    C_PK_BORDER = '#B45309'
    C_LINE = '#334155'         # Màu đường nối
    C_TEXT = '#0F172A'

    # Helper: vẽ hộp thực thể
    def draw_entity(x, y, w, h, text, is_weak=False):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=5,rounding_size=6",
                              facecolor=C_ENT_BG, edgecolor=C_ENT_BORDER, linewidth=2, zorder=3)
        ax.add_patch(rect)
        if is_weak:
            rect2 = FancyBboxPatch((x+4, y+4), w-8, h-8, boxstyle="round,pad=3,rounding_size=4",
                                   facecolor="none", edgecolor=C_ENT_BORDER, linewidth=1.2, zorder=3)
            ax.add_patch(rect2)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=10.5,
                fontweight='bold', color=C_TEXT, zorder=4)

    # Helper: vẽ mối kết hợp hình thoi
    def draw_rel(cx, cy, w, h, text):
        half_w = w / 2
        half_h = h / 2
        pts = [[cx, cy + half_h], [cx + half_w, cy], [cx, cy - half_h], [cx - half_w, cy]]
        poly = Polygon(pts, closed=True, facecolor=C_REL_BG, edgecolor=C_REL_BORDER, linewidth=2, zorder=3)
        ax.add_patch(poly)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=9,
                fontweight='bold', color='#14532D', zorder=4)

    # Helper: vẽ thuộc tính hình oval
    def draw_attr(cx, cy, rx, ry, text, is_pk=False, is_multi=False, is_derived=False):
        fc = C_PK_BG if is_pk else C_ATTR_BG
        ec = C_PK_BORDER if is_pk else C_ATTR_BORDER
        ls = '--' if is_derived else '-'
        el = Ellipse((cx, cy), rx*2, ry*2, facecolor=fc, edgecolor=ec,
                     linewidth=1.8, linestyle=ls, zorder=3)
        ax.add_patch(el)
        if is_multi:
            el2 = Ellipse((cx, cy), (rx-5)*2, (ry-4)*2, facecolor="none", edgecolor=ec,
                          linewidth=1.2, zorder=3)
            ax.add_patch(el2)
        fw = 'bold' if is_pk else 'normal'
        ax.text(cx, cy, text, ha='center', va='center', fontsize=8.5,
                fontweight=fw, color=C_TEXT, zorder=4)

    # Helper: vẽ đường nối
    def draw_line(p1, p2, label=None, label_pos=0.5, label_offset=(0, 0)):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=C_LINE, linewidth=1.4, zorder=2)
        if label:
            lx = p1[0] + (p2[0] - p1[0]) * label_pos + label_offset[0]
            ly = p1[1] + (p2[1] - p1[1]) * label_pos + label_offset[1]
            ax.text(lx, ly, label, fontsize=8.5, fontweight='bold', color='#475569',
                    bbox=dict(boxstyle='square,pad=1', facecolor='#FFFFFF', edgecolor='none', alpha=0.8),
                    ha='center', va='center', zorder=5)

    # 1. Tiêu đề sơ đồ
    ax.text(1000, 1360, "SƠ ĐỒ THỰC THỂ - MỐI KẾT HỢP MỞ RỘNG (EER DIAGRAM)",
            ha='center', va='center', fontsize=17, fontweight='bold', color='#1E3A8A')
    ax.text(1000, 1325, "HỆ THỐNG MẠNG XÃ HỘI HỌC TẬP — ĐỀ TÀI 17 (POSTGRESQL 18.6 & NEO4J)",
            ha='center', va='center', fontsize=11, fontstyle='italic', color='#475569')

    # 2. VẼ CÁC THỰC THỂ CHÍNH
    # NGUOI_DUNG
    draw_entity(460, 1060, 180, 80, "NGƯỜI DÙNG\n(users)")
    # NHOM_HOC_TAP
    draw_entity(1150, 1060, 190, 80, "NHÓM HỌC TẬP\n(study_group)")
    # THU_MUC
    draw_entity(1680, 1060, 180, 80, "THƯ MỤC\n(folder)")
    # BAI_DANG (Siêu lớp)
    draw_entity(780, 720, 200, 80, "BÀI ĐĂNG\n(post)")
    # Phân lớp con: BAI_THAO_LUAN & BAI_TAI_LIEU
    draw_entity(620, 430, 200, 70, "BÀI THẢO LUẬN\n('thaoluan')")
    draw_entity(960, 430, 200, 70, "BÀI TÀI LIỆU\n('tailieu')")
    # BINH_LUAN
    draw_entity(790, 140, 190, 80, "BÌNH LUẬN\n(comment)")

    # 3. CHUYÊN MÔN HÓA / KHÁI QUÁT HÓA (Disjoint Specialization 'd')
    c_d = Ellipse((880, 580), 50, 50, facecolor='#FEF3C7', edgecolor='#D97706', linewidth=2, zorder=3)
    ax.add_patch(c_d)
    ax.text(880, 580, "d", ha='center', va='center', fontsize=13, fontweight='bold', color='#B45309', zorder=4)
    # Đường nối từ BAI_DANG xuống d
    draw_line((880, 720), (880, 605))
    # Đường nối từ d xuống 2 lớp con
    draw_line((880, 555), (720, 500))
    draw_line((880, 555), (1060, 500))

    # 4. CÁC MỐI KẾT HỢP
    # KET_BAN (Đệ quy M:N)
    draw_rel(200, 1140, 140, 70, "KẾT BẠN\n(M:N, Đệ quy)")
    draw_line((460, 1110), (270, 1140), "N", 0.3, (0, 10))
    draw_line((460, 1090), (270, 1120), "M", 0.3, (0, -10))
    draw_attr(80, 1140, 45, 25, "since")
    draw_line((80, 1140), (130, 1140))

    # THEO_DOI (Đệ quy có hướng M:N)
    draw_rel(200, 1000, 140, 70, "THEO DÕI\n(M:N, Có hướng)")
    draw_line((460, 1070), (270, 1010), "follower", 0.4, (0, 12))
    draw_line((460, 1060), (270, 990), "followee", 0.4, (0, -12))

    # THAM_GIA (M:N Người dùng - Nhóm)
    draw_rel(890, 1160, 140, 70, "THAM GIA\n(M:N)")
    draw_line((640, 1110), (820, 1160), "M", 0.4, (0, 12))
    draw_line((1150, 1110), (960, 1160), "N", 0.4, (0, 12))
    draw_attr(830, 1260, 55, 25, "role\n('owner'/'mod')")
    draw_line((830, 1235), (870, 1180))
    draw_attr(950, 1260, 50, 25, "joined_at")
    draw_line((950, 1235), (910, 1180))

    # SỞ HỮU (1:N Người dùng - Nhóm)
    draw_rel(890, 1050, 140, 70, "SỞ HỮU\n(1:N)")
    draw_line((640, 1080), (820, 1050), "1 (owner)", 0.4, (0, 12))
    draw_line((1150, 1080), (960, 1050), "N", 0.4, (0, 12))

    # ĐĂNG BÀI (1:N Người dùng - Bài đăng)
    draw_rel(560, 890, 130, 65, "ĐĂNG BÀI\n(1:N)")
    draw_line((530, 1060), (560, 922), "1", 0.4, (-12, 0))
    draw_line((560, 858), (780, 780), "N", 0.5, (-10, -10))

    # THUỘC NHÓM (1:N Nhóm - Bài đăng)
    draw_rel(1180, 890, 140, 65, "THUỘC NHÓM\n(1:N)")
    draw_line((1220, 1060), (1180, 922), "1", 0.4, (12, 0))
    draw_line((1180, 858), (980, 780), "N", 0.5, (10, -10))

    # CẢM XÚC (M:N Người dùng - Bài đăng)
    draw_rel(380, 740, 130, 65, "CẢM XÚC\n(M:N)")
    draw_line((490, 1060), (390, 772), "M", 0.5, (-12, 0))
    draw_line((445, 740), (780, 740), "N", 0.5, (0, 12))
    draw_attr(230, 740, 60, 26, "kind\n('like'/'love'...)")
    draw_line((290, 740), (315, 740))

    # CÓ BÌNH LUẬN (1:N Bài đăng - Bình luận)
    draw_rel(880, 310, 140, 65, "CÓ BÌNH LUẬN\n(1:N)")
    draw_line((880, 720), (880, 342), "1", 0.4, (12, 0))
    draw_line((880, 278), (880, 220), "N", 0.5, (12, 0))

    # VIẾT BÌNH LUẬN (1:N Người dùng - Bình luận)
    draw_rel(480, 340, 140, 65, "VIẾT BL\n(1:N)")
    draw_line((470, 1060), (480, 372), "1", 0.5, (-12, 0))
    draw_line((530, 310), (790, 180), "N", 0.5, (0, -12))

    # TRẢ LỜI (Đệ quy 1:N Bình luận - Bình luận con)
    draw_rel(1120, 180, 140, 70, "TRẢ LỜI\n(1:N, Đệ quy)")
    draw_line((980, 190), (1050, 190), "1 (cha)", 0.4, (0, 12))
    draw_line((980, 160), (1050, 160), "N (con)", 0.4, (0, -12))

    # CÓ THƯ MỤC (1:N Nhóm - Thư mục)
    draw_rel(1510, 1100, 130, 65, "CÓ THƯ MỤC\n(1:N)")
    draw_line((1340, 1100), (1445, 1100), "1", 0.4, (0, 12))
    draw_line((1575, 1100), (1680, 1100), "N", 0.4, (0, 12))

    # THƯ MỤC CON (Đệ quy 1:N Thư mục - Thư mục con)
    draw_rel(1770, 1250, 140, 70, "THƯ MỤC CON\n(1:N, Đệ quy)")
    draw_line((1730, 1140), (1740, 1215), "1 (cha)", 0.5, (-15, 0))
    draw_line((1810, 1140), (1800, 1215), "N (con)", 0.5, (15, 0))

    # 5. CÁC THUỘC TÍNH
    # Thuộc tính NGUOI_DUNG
    draw_attr(390, 1240, 50, 24, "user_id", is_pk=True)
    draw_line((390, 1216), (480, 1140))
    draw_attr(500, 1240, 50, 24, "email (U)")
    draw_line((500, 1216), (530, 1140))
    draw_attr(620, 1240, 50, 24, "ho_ten")
    draw_line((620, 1216), (580, 1140))
    # Composite ho_ten
    draw_attr(620, 1320, 35, 18, "ho")
    draw_line((620, 1264), (620, 1302))
    draw_attr(695, 1315, 38, 18, "ten_dem")
    draw_line((645, 1258), (680, 1300))
    draw_attr(750, 1270, 35, 18, "ten")
    draw_line((665, 1248), (715, 1265))
    # Derived friend_count
    draw_attr(320, 1190, 55, 24, "/friend_count", is_derived=True)
    draw_line((365, 1175), (465, 1130))
    # Multi-valued
    draw_attr(310, 1070, 55, 24, "so_thich\n{interests}", is_multi=True)
    draw_line((365, 1070), (460, 1080))
    draw_attr(310, 930, 55, 24, "mon_hoc\n{subjects}", is_multi=True)
    draw_line((365, 940), (470, 1060))

    # Thuộc tính NHOM_HOC_TAP
    draw_attr(1140, 1240, 48, 24, "group_id", is_pk=True)
    draw_line((1140, 1216), (1190, 1140))
    draw_attr(1250, 1240, 45, 24, "name")
    draw_line((1250, 1216), (1240, 1140))
    draw_attr(1360, 1230, 45, 24, "topic")
    draw_line((1350, 1208), (1280, 1140))
    draw_attr(1380, 1160, 45, 24, "is_private")
    draw_line((1340, 1150), (1340, 1120))

    # Thuộc tính THU_MUC
    draw_attr(1720, 970, 48, 24, "folder_id", is_pk=True)
    draw_line((1720, 994), (1730, 1060))
    draw_attr(1830, 970, 45, 24, "name")
    draw_line((1820, 994), (1800, 1060))

    # Thuộc tính BAI_DANG
    draw_attr(660, 770, 45, 24, "post_id", is_pk=True)
    draw_line((705, 770), (780, 770))
    draw_attr(660, 700, 45, 24, "title")
    draw_line((705, 710), (780, 730))
    draw_attr(1080, 770, 45, 24, "content")
    draw_line((1035, 770), (980, 770))
    draw_attr(1080, 700, 48, 24, "created_at")
    draw_line((1035, 710), (980, 730))

    # Thuộc tính BAI_THAO_LUAN
    draw_attr(500, 430, 52, 24, "is_closed\n(khoa_bl)")
    draw_line((552, 430), (620, 440))

    # Thuộc tính BAI_TAI_LIEU
    draw_attr(1210, 455, 48, 24, "file_url")
    draw_line((1162, 455), (1160, 455))
    draw_attr(1210, 400, 50, 24, "tap_nhan\n{tags}", is_multi=True)
    draw_line((1160, 410), (1160, 435))

    # Thuộc tính BINH_LUAN
    draw_attr(640, 200, 52, 24, "comment_id", is_pk=True)
    draw_line((692, 190), (790, 180))
    draw_attr(640, 140, 48, 24, "content")
    draw_line((688, 145), (790, 160))
    draw_attr(640, 80, 50, 24, "created_at")
    draw_line((688, 95), (810, 140))

    # Chú thích góc dưới
    leg_box = FancyBboxPatch((80, 60), 380, 180, boxstyle="round,pad=5,rounding_size=6",
                             facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.5, zorder=2)
    ax.add_patch(leg_box)
    ax.text(270, 215, "CHÚ THÍCH KÝ HIỆU EER", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1E293B')
    
    # Legend items
    draw_entity(100, 165, 80, 30, "Thực thể")
    draw_rel(240, 180, 70, 30, "Liên kết")
    draw_attr(340, 180, 35, 15, "Khóa chính", is_pk=True)
    
    draw_attr(140, 115, 35, 14, "Đa trị", is_multi=True)
    draw_attr(240, 115, 35, 14, "Dẫn xuất", is_derived=True)
    c_leg_d = Ellipse((340, 115), 26, 26, facecolor='#FEF3C7', edgecolor='#D97706', linewidth=1.5)
    ax.add_patch(c_leg_d)
    ax.text(340, 115, "d", ha='center', va='center', fontsize=10, fontweight='bold', color='#B45309')
    ax.text(360, 115, " Chuyên môn hóa rời rạc", ha='left', va='center', fontsize=8, color='#475569')

    plt.tight_layout()
    plt.savefig(str(out_path), bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"-> Đã vẽ xong Sơ đồ EER: {out_path} ({out_path.stat().st_size} bytes)")

def draw_oo_class_diagram():
    out_path = ROOT / "oo_model" / "class_diagram.png"
    print(f"-> Đang vẽ sơ đồ Lớp ODMG 3.0 tại: {out_path}")
    
    fig, ax = plt.subplots(figsize=(18, 12), dpi=300)
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 1100)
    ax.axis("off")
    fig.patch.set_facecolor('#FFFFFF')

    C_BOX_BG = '#F8FAFC'
    C_HEADER_BG = '#DBEAFE'
    C_BORDER = '#2563EB'
    C_HEADER_TEXT = '#1E3A8A'
    C_TEXT = '#1E293B'
    C_ARROW = '#334155'

    # Helper: vẽ hộp Class 3 ngăn
    def draw_class(x, y, w, h, title, subtitle, attrs, methods):
        # Nền chính
        rect = FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                              facecolor=C_BOX_BG, edgecolor=C_BORDER, linewidth=1.8, zorder=3)
        ax.add_patch(rect)
        
        # Ngăn Header
        hh = 50
        h_rect = FancyBboxPatch((x, y + h - hh), w, hh, boxstyle="square,pad=0",
                                facecolor=C_HEADER_BG, edgecolor=C_BORDER, linewidth=1.8, zorder=3)
        ax.add_patch(h_rect)
        ax.text(x + w/2, y + h - 20, title, ha='center', va='center', fontsize=11, fontweight='bold', color=C_HEADER_TEXT, zorder=4)
        ax.text(x + w/2, y + h - 38, subtitle, ha='center', va='center', fontsize=8, fontstyle='italic', color='#475569', zorder=4)

        # Đường kẻ phân cách thuộc tính và phương thức
        attr_box_h = len(attrs) * 16 + 14
        ax.plot([x, x + w], [y + h - hh - attr_box_h, y + h - hh - attr_box_h], color=C_BORDER, linewidth=1.2, zorder=4)

        # Text Thuộc tính
        curr_y = y + h - hh - 16
        for a in attrs:
            ax.text(x + 10, curr_y, a, ha='left', va='center', fontsize=8.5, color=C_TEXT, zorder=4)
            curr_y -= 16

        # Text Phương thức
        curr_y = y + h - hh - attr_box_h - 16
        for m in methods:
            ax.text(x + 10, curr_y, m, ha='left', va='center', fontsize=8.5, color='#047857', zorder=4)
            curr_y -= 16

    # 1. Tiêu đề
    ax.text(800, 1060, "SƠ ĐỒ 6 LỚP ĐỐI TƯỢNG (ODMG 3.0 CLASS DIAGRAM)",
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1E3A8A')
    ax.text(800, 1030, "MÔ HÌNH HƯỚNG ĐỐI TƯỢNG CHO MẠNG XÃ HỘI HỌC TẬP (ODL / OQL / JPQL)",
            ha='center', va='center', fontsize=10.5, fontstyle='italic', color='#475569')

    # 2. VẼ 6 LỚP
    # NguoiDung
    draw_class(60, 700, 360, 270, "NguoiDung", "(extent dsNguoiDung, key user_id)",
               ["- user_id: integer", "- email: string", "- ho_ten: string", "- ngay_tao: date",
                "- so_thich: set<string>", "- mon_hoc: set<string>",
                "// Quan hệ (Relationships):",
                "+ cac_bai_dang: set<BaiDang> (inverse tac_gia)",
                "+ cac_binh_luan: set<BinhLuan> (inverse tac_gia)",
                "+ ds_ban_be: set<NguoiDung> (inverse ds_ban_be)"],
               ["+ themBanBe(u: NguoiDung): void", "+ thamGiaNhom(g: NhomHocTap): void"])

    # NhomHocTap
    draw_class(600, 740, 360, 230, "NhomHocTap", "(extent dsNhomHocTap, key group_id)",
               ["- group_id: integer", "- ten_nhom: string", "- chu_de: string", "- la_rieng_tu: boolean",
                "// Quan hệ:",
                "+ chu_nhom: NguoiDung",
                "+ cac_thanh_vien: set<NguoiDung>",
                "+ cac_bai_dang: set<BaiDang> (inverse nhom)"],
               ["+ themThanhVien(u: NguoiDung): void", "+ xoaThanhVien(u: NguoiDung): void"])

    # BinhLuan
    draw_class(1140, 700, 380, 270, "BinhLuan", "(extent dsBinhLuan, key comment_id)",
               ["- comment_id: integer", "- noi_dung: string", "- ngay_tao: timestamp",
                "// Quan hệ phân cấp cây:",
                "+ tac_gia: NguoiDung (inverse cac_binh_luan)",
                "+ bai_dang: BaiDang (inverse cac_binh_luan)",
                "+ binh_luan_cha: BinhLuan (inverse cac_binh_luan_con)",
                "+ cac_binh_luan_con: set<BinhLuan> (inverse binh_luan_cha)"],
               ["+ themTraLoi(bl: BinhLuan): void", "+ layCayCon(): set<BinhLuan>"])

    # BaiDang <<abstract>>
    draw_class(600, 360, 360, 260, "BaiDang <<abstract>>", "(extent dsBaiDang, key post_id)",
               ["- post_id: integer", "- tieu_de: string", "- noi_dung: string",
                "- ngay_tao: timestamp", "- so_luot_thich: integer",
                "// Quan hệ:",
                "+ tac_gia: NguoiDung (inverse cac_bai_dang)",
                "+ nhom: NhomHocTap (inverse cac_bai_dang)",
                "+ cac_binh_luan: set<BinhLuan> (inverse bai_dang)"],
               ["+ themBinhLuan(bl: BinhLuan): void", "+ tangLuotThich(): void"])

    # BaiThaoLuan (Kế thừa BaiDang)
    draw_class(320, 80, 340, 180, "BaiThaoLuan", "(extent dsBaiThaoLuan, extends BaiDang)",
               ["- da_khoa: boolean", "- luot_xem: integer",
                "// Kế thừa toàn bộ thuộc tính &",
                "// quan hệ từ BaiDang"],
               ["+ dongThaoLuan(): void", "+ moThaoLuan(): void"])

    # BaiTaiLieu (Kế thừa BaiDang)
    draw_class(900, 80, 360, 180, "BaiTaiLieu", "(extent dsBaiTaiLieu, extends BaiDang)",
               ["- duong_dan_tep: string", "- dinh_dang: string", "- dung_luong_kb: integer",
                "- cac_the: set<string>",
                "// Kế thừa toàn bộ thuộc tính &",
                "// quan hệ từ BaiDang"],
               ["+ taiTepLen(url: string): void", "+ capNhatThe(tags: set): void"])

    # 3. VẼ ĐƯỜNG NỐI VÀ MŨI TÊN KẾ THỪA (Inheritance)
    # Từ BaiThaoLuan lên BaiDang
    ax.plot([490, 490, 720, 720], [260, 300, 300, 360], color=C_ARROW, linewidth=1.5, zorder=2)
    poly1 = Polygon([[720, 360], [710, 345], [730, 345]], closed=True,
                    facecolor='#FFFFFF', edgecolor=C_ARROW, linewidth=1.5, zorder=5)
    ax.add_patch(poly1)

    # Từ BaiTaiLieu lên BaiDang
    ax.plot([1080, 1080, 840, 840], [260, 300, 300, 360], color=C_ARROW, linewidth=1.5, zorder=2)
    poly2 = Polygon([[840, 360], [830, 345], [850, 345]], closed=True,
                    facecolor='#FFFFFF', edgecolor=C_ARROW, linewidth=1.5, zorder=5)
    ax.add_patch(poly2)

    # 4. VẼ LIÊN KẾT GIỮA CÁC LỚP
    # NguoiDung - BaiDang (1..* Đăng bài)
    ax.plot([420, 600], [750, 500], color=C_ARROW, linewidth=1.2, linestyle=':', zorder=2)
    ax.text(450, 700, "1 (tác giả)", fontsize=8, fontweight='bold', color='#475569')
    ax.text(560, 540, "0..* (bài đăng)", fontsize=8, fontweight='bold', color='#475569')

    # NhomHocTap - BaiDang (1..* Đăng trong nhóm)
    ax.plot([780, 780], [740, 620], color=C_ARROW, linewidth=1.2, linestyle=':', zorder=2)
    ax.text(790, 680, "1\nnhóm", fontsize=8, fontweight='bold', color='#475569')
    ax.text(790, 630, "0..*\nbài", fontsize=8, fontweight='bold', color='#475569')

    # BaiDang - BinhLuan (1..* Chứa bình luận)
    ax.plot([960, 1140], [500, 750], color=C_ARROW, linewidth=1.2, linestyle=':', zorder=2)
    ax.text(1000, 560, "1 (bài)", fontsize=8, fontweight='bold', color='#475569')
    ax.text(1090, 700, "0..* (bình luận)", fontsize=8, fontweight='bold', color='#475569')

    # BinhLuan - BinhLuan (Quan hệ đệ quy cây bình luận)
    ax.plot([1520, 1560, 1560, 1480], [880, 880, 960, 960], color=C_ARROW, linewidth=1.2, linestyle='-', zorder=2)
    ax.text(1565, 920, "1:N đệ quy\n(cây bình luận)", fontsize=8, fontweight='bold', color='#B91C1C')

    plt.tight_layout()
    plt.savefig(str(out_path), bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"-> Đã vẽ xong Sơ đồ Lớp ODMG: {out_path} ({out_path.stat().st_size} bytes)")

if __name__ == "__main__":
    draw_eer_diagram()
    draw_oo_class_diagram()
