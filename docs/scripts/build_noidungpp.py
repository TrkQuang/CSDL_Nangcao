"""
Biên dịch tài liệu Kịch bản & Nội dung thuyết trình slide hoàn chỉnh: noidungpp.docx
Quy mô 20 slides chia đều cho 5 thành viên (Quang, Hưng, Hữu, Chương, Quỳnh).
Mỗi slide gồm: Mục tiêu, Nội dung chính trên slide, Hình ảnh minh họa nhúng trực tiếp,
và Lời thoại chi tiết cho người thuyết trình (kèm hướng dẫn trả lời phản biện).
"""

import os, sys, shutil
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

ROOT = Path(__file__).resolve().parents[2]

# Bảng màu
C_NAVY = RGBColor(30, 58, 138)
C_DARK = RGBColor(15, 23, 42)
C_MUTED = RGBColor(71, 85, 105)
C_ACCENT = RGBColor(37, 99, 235)
HEX_PRIMARY = "1E3A8A"
HEX_ZEBRA = "F8FAFC"
HEX_SCRIPT_BG = "F0FDF4"      # Xanh lục nhạt trang nhã cho lời thoại
HEX_SCRIPT_BORDER = "16A34A"  # Xanh lục viền
HEX_QA_BG = "FEF2F2"          # Đỏ nhạt cho câu hỏi phản biện
HEX_QA_BORDER = "DC2626"

def setup_page(doc):
    for sec in doc.sections:
        sec.page_width = Cm(21.0)
        sec.page_height = Cm(29.7)
        sec.top_margin = Cm(2.0)
        sec.bottom_margin = Cm(2.0)
        sec.left_margin = Cm(2.5)
        sec.right_margin = Cm(2.0)
        
        # Header
        h = sec.header.paragraphs[0]
        h.text = "KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN — ĐỀ TÀI 17: MẠNG XÃ HỘI HỌC TẬP"
        h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        h.style.font.name = "Times New Roman"
        h.style.font.size = Pt(8.5)
        h.style.font.italic = True
        h.style.font.color.rgb = C_MUTED
        
        # Footer
        f = sec.footer.paragraphs[0]
        f.text = "Trường Đại học Sài Gòn — Khoa CNTT  |  Trang "
        f.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f.style.font.name = "Times New Roman"
        f.style.font.size = Pt(9)
        f.style.font.color.rgb = C_MUTED
        fld = OxmlElement('w:fldSimple')
        fld.set(qn('w:instr'), 'PAGE')
        f._p.append(fld)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex: str):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def add_slide_header(doc, slide_no: int, title: str, presenter: str, duration: str):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_shading(cell, HEX_PRIMARY)
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(f"SLIDE {slide_no:02d}: {title.upper()}\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(13)
    r1.bold = True
    r1.font.color.rgb = RGBColor(255, 255, 255)
    
    r2 = p.add_run(f"Người trình bày: {presenter}  |  Thời lượng dự kiến: {duration}")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(10.5)
    r2.font.italic = True
    r2.font.color.rgb = RGBColor(224, 231, 255)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(4)

def add_slide_content(doc, objective: str, bullets: list[str]):
    p_obj = doc.add_paragraph()
    p_obj.paragraph_format.space_before = Pt(4)
    p_obj.paragraph_format.space_after = Pt(4)
    r_obj_lbl = p_obj.add_run("🎯 Mục tiêu cốt lõi của Slide: ")
    r_obj_lbl.font.name = "Times New Roman"
    r_obj_lbl.font.size = Pt(11)
    r_obj_lbl.bold = True
    r_obj_lbl.font.color.rgb = C_NAVY
    
    r_obj_val = p_obj.add_run(objective)
    r_obj_val.font.name = "Times New Roman"
    r_obj_val.font.size = Pt(11)
    r_obj_val.font.italic = True
    
    p_b_lbl = doc.add_paragraph()
    p_b_lbl.paragraph_format.space_before = Pt(4)
    p_b_lbl.paragraph_format.space_after = Pt(2)
    r_b_lbl = p_b_lbl.add_run("📋 Nội dung chính hiển thị trên Slide (Bullet Points):")
    r_b_lbl.font.name = "Times New Roman"
    r_b_lbl.font.size = Pt(11)
    r_b_lbl.bold = True
    r_b_lbl.font.color.rgb = C_DARK
    
    for b in bullets:
        p_b = doc.add_paragraph(style='List Bullet')
        p_b.paragraph_format.space_before = Pt(1)
        p_b.paragraph_format.space_after = Pt(3)
        p_b.paragraph_format.line_spacing = 1.25
        r_b = p_b.add_run(b)
        r_b.font.name = "Times New Roman"
        r_b.font.size = Pt(10.5)

def add_embedded_image(doc, rel_path: str, caption: str, width: float = 5.6):
    img_path = ROOT / rel_path
    if not img_path.exists():
        print(f"<!> Bỏ qua ảnh: {img_path}")
        return
    
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.keep_with_next = True
    
    r_img = p_img.add_run()
    r_img.add_picture(str(img_path), width=Inches(width))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(6)
    r_cap = p_cap.add_run(f"🖼 Minh họa trên slide: {caption}")
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(9.5)
    r_cap.bold = True
    r_cap.font.italic = True
    r_cap.font.color.rgb = C_NAVY

def add_speaker_script(doc, script_text: str, qa_text: str = None):
    # Box lời thoại
    t1 = doc.add_table(rows=1, cols=1)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1 = t1.cell(0, 0)
    c1.width = Inches(6.5)
    set_cell_shading(c1, HEX_SCRIPT_BG)
    set_cell_margins(c1, top=100, bottom=100, left=140, right=140)
    
    p1 = c1.paragraphs[0]
    p1.paragraph_format.line_spacing = 1.25
    r_t1 = p1.add_run("🎙 LỜI THOẠI CHI TIẾT CHO NGƯỜI THUYẾT TRÌNH (SPEAKER SCRIPT):\n")
    r_t1.font.name = "Times New Roman"
    r_t1.font.size = Pt(10.5)
    r_t1.bold = True
    r_t1.font.color.rgb = RGBColor(22, 101, 52)
    
    r_b1 = p1.add_run(script_text.strip())
    r_b1.font.name = "Times New Roman"
    r_b1.font.size = Pt(10)
    r_b1.font.color.rgb = RGBColor(15, 23, 42)
    
    if qa_text:
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
        t2 = doc.add_table(rows=1, cols=1)
        t2.alignment = WD_TABLE_ALIGNMENT.CENTER
        c2 = t2.cell(0, 0)
        c2.width = Inches(6.5)
        set_cell_shading(c2, HEX_QA_BG)
        set_cell_margins(c2, top=80, bottom=80, left=140, right=140)
        
        p2 = c2.paragraphs[0]
        p2.paragraph_format.line_spacing = 1.2
        r_t2 = p2.add_run("💡 DỰ ĐOÁN CÂU HỎI PHẢN BIỆN & CÂU TRẢ LỜI MẪU:\n")
        r_t2.font.name = "Times New Roman"
        r_t2.font.size = Pt(10)
        r_t2.bold = True
        r_t2.font.color.rgb = RGBColor(185, 28, 28)
        
        r_b2 = p2.add_run(qa_text.strip())
        r_b2.font.name = "Times New Roman"
        r_b2.font.size = Pt(9.5)
        r_b2.font.color.rgb = RGBColor(30, 41, 59)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    doc.add_page_break()

def build_all_slides():
    doc = Document()
    setup_page(doc)
    
    # Trang tiêu đề tài liệu kịch bản
    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_before = Pt(20)
    r_t = p_t.add_run("TÀI LIỆU KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN\nCƠ SỞ DỮ LIỆU NÂNG CAO\n\n")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(16)
    r_t.bold = True
    r_t.font.color.rgb = C_NAVY
    
    r_sub = p_t.add_run("ĐỀ TÀI 17: DỮ LIỆU PHÂN CẤP VÀ DỮ LIỆU ĐỒ THỊ TRONG CSDL QUAN HỆ\n"
                        "ỨNG DỤNG MẠNG XÃ HỘI HỌC TẬP (SOCIAL LEARNING NETWORK)\n\n"
                        "TỔNG HỢP NỘI DUNG 20 SLIDES, HÌNH ẢNH MINH HỌA & LỜI THOẠI CHI TIẾT 5 THÀNH VIÊN\n"
                        "—" * 30 + "\n")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(12)
    r_sub.bold = True
    r_sub.font.color.rgb = C_DARK
    
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.left_indent = Inches(1.0)
    p_meta.paragraph_format.line_spacing = 1.3
    p_meta.add_run("• Phân công thuyết trình:\n").bold = True
    p_meta.add_run("  - TV1: Trần Quang (Nhóm trưởng)  — Slides 01 -> 04 (Tổng quan, BR1-BR10, Chuẩn hóa 3NF/BCNF/Chase/4NF)\n")
    p_meta.add_run("  - TV2: Thanh Hưng                — Slides 05 -> 08 (4 Mô hình Cây phân cấp, Q1-Q10, CRUD, ODMG ODL/OQL)\n")
    p_meta.add_run("  - TV3: Quang Hữu                 — Slides 09 -> 12 (Lược đồ vật lý, SQL nâng cao Q1-Q8, Triggers, R1-R4, T1-T2)\n")
    p_meta.add_run("  - TV4: Chương Võ                 — Slides 13 -> 16 (CSDL Đồ thị Neo4j/Cypher, Bế tắc Deadlock T3, pgbench 3.4k TPS)\n")
    p_meta.add_run("  - TV5: Như Quỳnh                 — Slides 17 -> 20 (Benchmark 360 runs, Dung lượng đĩa, Đa lưu trữ, Tổng kết CLO7)\n")
    p_meta.add_run("• Thời lượng: 15 phút thuyết trình (3 phút/thành viên) + 5 phút Demo hệ thống + 10 phút Phản biện Q&A.\n")
    doc.add_page_break()

    # ========================================================
    # PHẦN 1: TRẦN QUANG (SLIDES 1 - 4)
    # ========================================================
    # Slide 1
    add_slide_header(doc, 1, "Giới thiệu Đề tài 17 & Đội ngũ Thực hiện", "Trần Quang (TV1 - Nhóm trưởng)", "2.5 phút")
    add_slide_content(doc, "Mở đầu buổi bảo vệ, giới thiệu tên đề tài, bối cảnh EdTech, và cơ cấu phân công nhiệm vụ của 5 thành viên.",
                      ["Đề tài 17: Dữ liệu phân cấp và Dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng Mạng xã hội học tập.",
                       "Đơn vị: Trường Đại học Sài Gòn — Khoa Công nghệ Thông tin — Bộ môn Hệ thống Thông tin.",
                       "5 thành viên: Trần Quang (Leader), Thanh Hưng (TV2), Quang Hữu (TV3), Chương Võ (TV4), Như Quỳnh (TV5).",
                       "Mục tiêu: Giải quyết trọn vẹn 3 bài toán nghiên cứu (RQ1: Cây phân cấp, RQ2: Đồ thị mạng xã hội, RQ3: Đồng thời & Vật lý).",
                       "Hệ thống công nghệ chính: PostgreSQL 18.6 và CSDL Đồ thị chuyên dụng Neo4j 5.x Community trên Docker."])
    add_speaker_script(doc,
        "Kính chào Quý Thầy Cô trong Hội đồng phản biện và toàn thể các bạn sinh viên!\n"
        "Em tên là Trần Quang, đại diện nhóm sinh viên thực hiện Đề tài số 17 với chủ đề: 'Dữ liệu phân cấp và Dữ liệu đồ thị trong CSDL quan hệ: Ứng dụng Mạng xã hội học tập'.\n"
        "Đề tài của chúng em được phát triển bởi tập thể 5 thành viên gồm em, bạn Thanh Hưng, bạn Quang Hữu, bạn Chương Võ và bạn Như Quỳnh. Trong 15 phút tới, nhóm em sẽ lần lượt trình bày toàn bộ hành trình nghiên cứu: từ thiết kế mức quan niệm EER, chứng minh toán học chuẩn hóa, hiện thực 4 mô hình cây phân cấp, đối chiếu hiệu năng với CSDL đồ thị Neo4j, đến các thực nghiệm thử tải hàng ngàn TPS và bế tắc Deadlock trên PostgreSQL 18.6.\n"
        "Em xin phép được bắt đầu phần đầu tiên: Bối cảnh nghiệp vụ và Thiết kế quan niệm.",
        "Câu hỏi: Tại sao nhóm lại chọn ứng dụng Mạng xã hội học tập thay vì một hệ thống bán hàng e-commerce thông thường?\n"
        "Trả lời: Thưa Thầy/Cô, hệ thống e-commerce chủ yếu xoay quanh các bảng phẳng 2 chiều (đơn hàng, sản phẩm). Trong khi đó, mạng xã hội học tập chứa đầy đủ hai cấu trúc dữ liệu thách thức nhất của môn học: cấu trúc cây phân cấp vô hạn cấp (chuỗi thảo luận bình luận, cây thư mục nhóm) và cấu trúc đồ thị mạng lưới kết nối phức tạp (bạn bè hai chiều, theo dõi có hướng). Đây là môi trường lý tưởng để kiểm nghiệm sâu sắc các lý thuyết nâng cao.")

    # Slide 2
    add_slide_header(doc, 2, "Bối cảnh Nghiệp vụ & Mô hình Thực thể EER Hoàn chỉnh", "Trần Quang (TV1 - Nhóm trưởng)", "3.0 phút")
    add_slide_content(doc, "Phân tích 10 quy tắc nghiệp vụ then chốt (BR1-BR10) và trực quan hóa Sơ đồ EER mở rộng.",
                      ["10 Quy tắc nghiệp vụ (BR1-BR10): Quản lý hồ sơ, Bạn bè vô hướng, Theo dõi có hướng, Nhóm học tập, Bài viết đa hình, Bình luận phân cấp...",
                       "Quy ước chuẩn tắc kết bạn vô hướng (BR2): Luôn lưu user_a < user_b để triệt tiêu 100% dư thừa dữ liệu.",
                       "Bình luận lồng nhau đa cấp (BR6): Mối kết hợp đệ quy 1:N với chính nó (parent_id), tạo nên cây N-ary vô hạn cấp.",
                       "Chuyên môn hóa rời rạc (Disjoint 'd'): Bài đăng (post) phân rã thành Bài thảo luận ('thaoluan') và Bài tài liệu ('tailieu').",
                       "Bộ đếm phi chuẩn hóa có kiểm soát (BR9): friend_count, comment_count, reaction_count bảo đảm tốc độ tải Feed O(1)."])
    add_embedded_image(doc, "docs/eer_diagram.png", "Sơ đồ Thực thể - Mối kết hợp mở rộng (EER Diagram) Hệ thống Mạng xã hội học tập", 5.6)
    add_speaker_script(doc,
        "Thưa Thầy Cô, nhìn vào Hình 1.1 trên slide là Sơ đồ EER hoàn chỉnh của hệ thống do nhóm thiết kế theo chuẩn ký hiệu Chen mở rộng.\n"
        "Hệ thống gồm 7 thực thể chính. Em xin nhấn mạnh 3 điểm kiến trúc cốt lõi:\n"
        "1. Về quan hệ Bạn bè (Friendship): Đây là quan hệ đối xứng hai chiều. Nếu A là bạn B thì B là bạn A. Nhóm áp dụng quy tắc chuẩn tắc luôn lưu user_a < user_b ở mức khóa chính. Giải pháp này giúp tiết kiệm 50% dung lượng đĩa và loại bỏ hoàn toàn nguy cơ bất nhất quán dữ liệu.\n"
        "2. Về chuỗi thảo luận (Comment): Thực thể Bình luận có liên kết đệ quy 1:N với chính nó qua trường parent_id, cho phép phản hồi lồng nhau không giới hạn độ sâu.\n"
        "3. Về tính kế thừa: Siêu lớp BÀI ĐĂNG chuyên môn hóa thành 2 lớp con là BÀI THẢO LUẬN và BÀI TÀI LIỆU theo tính chất Rời rạc hoàn toàn (Disjoint 'd'). Sau khi cân nhắc 3 phương án ánh xạ, nhóm quyết định chọn Single Table Inheritance vì tối ưu hóa tuyệt đối cho thao tác đọc Bảng tin chiếm 95% lưu lượng.",
        "Câu hỏi: Tại sao không lưu cả 2 chiều (A, B) và (B, A) trong bảng kết bạn để khi truy vấn bạn bè chỉ cần SELECT WHERE user_a = X?\n"
        "Trả lời: Thưa Thầy/Cô, việc lưu cả hai chiều sẽ làm bảng phình to gấp đôi (2 triệu dòng thay vì 1 triệu dòng). Khi người dùng hủy kết bạn, nếu ứng dụng chỉ xóa một chiều thì chiều kia vẫn tồn tại, gây lỗi dữ liệu ma. Nhóm giải quyết bằng cách lưu 1 chiều chuẩn tắc user_a < user_b và đánh 2 chỉ mục B-Tree trên user_a và user_b. PostgreSQL sẽ sử dụng BitmapOr Index Scan để quét đồng thời cả hai cột với tốc độ tương đương nhưng bảo đảm an toàn dữ liệu 100%.")

    # Slide 3
    add_slide_header(doc, 3, "Lý thuyết Phụ thuộc hàm, Bao đóng & Tìm khóa ứng viên", "Trần Quang (TV1 - Nhóm trưởng)", "3.0 phút")
    add_slide_content(doc, "Trình bày cơ sở toán học, hệ tiên đề Armstrong, thuật toán tính bao đóng CLOSURE và chứng minh khóa ứng viên duy nhất.",
                      ["Lược đồ phẳng ban đầu R(13 thuộc tính) và 4 dị thường nghiêm trọng: Dị thường thêm, Dị thường xóa, Dị thường sửa và Dư thừa dữ liệu.",
                       "Tập 15 Phụ thuộc hàm logic (F = {FD1 ... FD15}) phản ánh chặt chẽ nghiệp vụ thực tế.",
                       "Hệ tiên đề Armstrong: Luật Phản xạ, Luật Tăng trưởng, Luật Bắc cầu và các định lý dẫn xuất (Hợp, Phân rã, Giả bắc cầu).",
                       "Thuật toán CLOSURE(X, F): Phân loại thuộc tính thành L={c_id}, R={tên, tiêu đề...}, B={p_id, a_id...}, N=∅.",
                       "Chứng minh toán học: {comment_id}+ = R. Kết luận: K = {comment_id} là KHÓA ỨNG VIÊN DUY NHẤT của lược đồ phẳng."])
    add_speaker_script(doc,
        "Tiếp theo, em xin trình bày về nền tảng lý thuyết Phụ thuộc hàm và Chuẩn hóa dữ liệu.\n"
        "Nếu chúng ta lưu toàn bộ dữ liệu vào một bảng phẳng tổng hợp R gồm 13 thuộc tính như trên slide, hệ thống sẽ gặp ngay 4 dị thường nguy hiểm: không thể thêm sinh viên mới nếu chưa có bình luận (Dị thường thêm); xóa bình luận cuối cùng sẽ làm mất luôn bài viết và nhóm học tập (Dị thường xóa); sửa tên nhóm phải UPDATE hàng ngàn dòng (Dị thường sửa).\n"
        "Để chuẩn hóa, nhóm xác định tập F gồm 15 phụ thuộc hàm. Bằng cách phân loại thuộc tính, nhận thấy comment_id chỉ xuất hiện ở vế trái (Tập L). Áp dụng thuật toán CLOSURE, qua 4 bước suy dẫn bắc cầu, tập bao đóng của comment_id nở rộng ra toàn bộ 13 thuộc tính của R.\n"
        "Vì comment_id là tập đơn trị và mọi khóa đều phải chứa tập L, nhóm đã chứng minh toán học chặt chẽ rằng {comment_id} là KHÓA ỨNG VIÊN DUY NHẤT của lược đồ phẳng ban đầu.",
        "Câu hỏi: Nếu một thuộc tính không xuất hiện ở vế nào của F (Tập N) thì nó có nằm trong khóa ứng viên không?\n"
        "Trả lời: Dạ thưa Thầy/Cô, theo định lý phân loại thuộc tính, tập N (Neither) là các thuộc tính không phụ thuộc vào ai và cũng không xác định ai. Do đó, tập N BẮT BUỘC PHẢI CÓ MẶT trong mọi khóa ứng viên của lược đồ quan hệ.")

    # Slide 4
    add_slide_header(doc, 4, "Phủ tối tiểu F_min, Chuẩn hóa 3NF/BCNF, Bảng Chase & 4NF", "Trần Quang (TV1 - Nhóm trưởng)", "3.0 phút")
    add_slide_content(doc, "Quy trình tìm phủ tối tiểu F_min, thuật toán Bernstein phân rã 3NF/BCNF, chứng minh Chase Lossless Join và xử lý 4NF.",
                      ["Quy trình 3 bước tìm F_min: Phát hiện và loại bỏ thành công FD15 (author_email → author_name) bị dư thừa bắc cầu qua author_id.",
                       "Thuật toán tổng hợp Bernstein: Phân rã R thành 4 quan hệ con {R_group, R_user, R_post, R_comment}.",
                       "Kiểm tra BCNF: 100% các phụ thuộc hàm đều có vế trái là Siêu khóa ⇒ Đạt chuẩn BCNF, bảo toàn phụ thuộc hàm 100%.",
                       "Chứng minh Bảng ma trận Chase Tableau 4x13: Dòng thứ 4 chuyển thành toàn bộ ký hiệu gốc a_j ⇒ Nối không tổn thất (Lossless Join)!",
                       "Phụ thuộc đa trị (MVD): Tách User_Interests_Subjects(user_id ↠ interest | subject) thành 2 bảng đạt Dạng chuẩn 4 (4NF)."])
    add_speaker_script(doc,
        "Để phân rã lược đồ về dạng chuẩn cao, nhóm thực hiện 3 bước tìm Phủ tối tiểu F_min:\n"
        "Ở bước 3, bằng cách tính bao đóng trên tập F thiếu vắng từng FD, nhóm phát hiện phụ thuộc FD15 (author_email → author_name) hoàn toàn dư thừa vì có thể suy dẫn gián tiếp qua FD14 và FD12. Sau khi loại bỏ FD15, tập F_min còn đúng 14 phụ thuộc hàm.\n"
        "Áp dụng Thuật toán tổng hợp Bernstein, nhóm gom nhóm các FD cùng vế trái và tạo thành 4 quan hệ con: R_group, R_user, R_post, và R_comment. Vì vế trái của mọi FD đều là khóa chính hoặc khóa ứng viên, cả 4 bảng đều ĐẠT CHUẨN BCNF và BẢO TOÀN PHỤ THUỘC HÀM 100%.\n"
        "Đặc biệt, để chứng minh phép phân rã không làm mất dữ liệu, nhóm xây dựng Bảng ma trận Chase 4 dòng × 13 cột. Sau 4 bước thế giá trị bằng các FD, dòng thứ 4 đã chứa trọn vẹn 13 ký hiệu gốc a1 đến a13. Theo định lý Maier, điều này khẳng định phép nối tự nhiên 4 bảng là LOSSLESS JOIN tuyệt đối!\n"
        "Tiếp theo, em xin kính mời bạn Thanh Hưng trình bày Phần 2 về 4 Mô hình cây phân cấp và CSDL hướng đối tượng.",
        "Câu hỏi: Phân rã BCNF có luôn luôn bảo toàn phụ thuộc hàm không? Trường hợp của nhóm thì sao?\n"
        "Trả lời: Thưa Thầy/Cô, về lý thuyết tổng quát, phân rã BCNF CÓ THỂ KHÔNG bảo toàn phụ thuộc hàm (ví dụ quan hệ R(A,B,C) với AB->C và C->B). Tuy nhiên, trong đề tài của nhóm chúng em, cả 4 quan hệ con sinh ra từ thuật toán Bernstein đều ngẫu nhiên thỏa mãn điều kiện BCNF ngay lập tức mà không cần phân rã thêm. Do đó, thiết kế của nhóm vừa đạt BCNF khắt khe, vừa BẢO TOÀN ĐƯỢC 100% PHỤ THUỘC HÀM!")

    # ========================================================
    # PHẦN 2: THANH HƯNG (SLIDES 5 - 8)
    # ========================================================
    # Slide 5
    add_slide_header(doc, 5, "Dữ liệu Phân cấp: Cấu trúc & Nguyên lý 4 Mô hình Cây", "Thanh Hưng (TV2)", "3.0 phút")
    add_slide_content(doc, "Giới thiệu thách thức lưu trữ dữ liệu phân cấp trên CSDL quan hệ và cấu trúc của 4 mô hình kinh điển.",
                      ["Thách thức kỹ thuật: Trở kháng giữa cây phân cấp đệ quy và bảng dữ liệu phẳng 2 chiều của RDBMS.",
                       "1. Danh sách kề (Adjacency List): Khóa ngoại parent_id trỏ về comment_id. Rất tự nhiên, ghi O(1), nhưng đọc cây con tốn WITH RECURSIVE.",
                       "2. Liệt kê đường dẫn (Path Enumeration / ltree): Lưu chuỗi đường dẫn '1.3.5' kết hợp chỉ mục GiST. Đọc cây con cực nhanh (<@, @>).",
                       "3. Tập lồng (Nested Set - Joe Celko): Đánh số duyệt cây trước (lft, rgt). Đọc cây con bằng 1 phép quét khoảng lft BETWEEN x AND y, nhưng ghi rất đắt đỏ.",
                       "4. Bảng bao đóng (Closure Table): Bảng phụ lưu toàn bộ cặp (ancestor, descendant, depth). Đọc/ghi linh hoạt bằng JOIN, nhưng phình to dung lượng O(N^2)."])
    add_embedded_image(doc, "docs/tree_models_comparison_diagram.png", "Cấu trúc lưu trữ của 4 mô hình cây phân cấp trên cùng một cây bình luận mẫu 6 nút", 5.6)
    add_speaker_script(doc,
        "Kính chào Quý Thầy Cô! Em tên là Thanh Hưng, phụ trách nghiên cứu 4 mô hình cây phân cấp và CSDL hướng đối tượng.\n"
        "Nhìn vào Hình 3.1 trên slide, nhóm đã hiện thực hóa 4 mô hình lưu trữ kinh điển trên cùng một cây bình luận mẫu gồm 6 nút:\n"
        "• Mô hình 1 - Adjacency List: Nút 4 lưu parent_id = 2. Rất trực quan và chèn thêm nút lá cực nhanh (O(1)), nhưng khi cần lấy toàn bộ nhánh con, máy chủ phải đệ quy quét bảng nhiều lần.\n"
        "• Mô hình 2 - Path Enumeration: Khai thác extension ltree của PostgreSQL, nút 4 lưu đường dẫn nhị phân '1.2.4'. Nhờ chỉ mục GiST, việc kiểm tra nút con diễn ra với tốc độ logarit.\n"
        "• Mô hình 3 - Nested Set: Nút 1 bao bọc toàn bộ cây với lft=1, rgt=12. Nhánh của nút 2 nằm gọn trong khoảng [2, 5]. Lấy cây con chỉ cần đúng 1 câu lệnh BETWEEN.\n"
        "• Mô hình 4 - Closure Table: Tạo bảng phụ lưu 14 cặp quan hệ tổ tiên - hậu duệ, biến các phép duyệt cây phức tạp thành phép JOIN đơn giản.",
        "Câu hỏi: Trong 4 mô hình trên, mô hình nào dễ bị hỏng cấu trúc dữ liệu nhất khi có lỗi ứng dụng?\n"
        "Trả lời: Thưa Thầy/Cô, mô hình Nested Set là dễ bị hỏng cấu trúc nhất! Vì các cặp (lft, rgt) có quan hệ mật thiết trên toàn cây, chỉ cần một thao tác UPDATE dịch chuyển tọa độ bị ngắt giữa chừng do mất điện hoặc ứng dụng crash, toàn bộ cây sẽ bị sai lệch khoảng và không thể truy vấn chính xác được nữa.")

    # Slide 6
    add_slide_header(doc, 6, "Bộ 10 Truy vấn Chuẩn Q1 – Q10 trên 4 Mô hình Cây", "Thanh Hưng (TV2)", "3.0 phút")
    add_slide_content(doc, "Quy ước Chuẩn tắc Thống nhất (Ground Truth) và hiện thực 40 câu truy vấn đối chiếu giữa 4 mô hình.",
                      ["3 Quy ước Ground Truth: Cây con (Q2, Q8) BẮT BUỘC chứa chính nó; Tổ tiên (Q3, Q10) KHÔNG chứa chính nó; Gốc có depth=1, level=0.",
                       "Truy vấn Q1 (Duyệt toàn cây DFS kèm thụt lề): Adjacency cần đệ quy mảng sort_path; Path Enum chỉ cần ORDER BY path; Nested Set ORDER BY lft.",
                       "Truy vấn Q2 (Lấy toàn bộ cây con): Path Enum dùng toán tử path <@ '1.2'; Nested Set dùng lft BETWEEN 2 AND 5; Closure dùng ancestor_id = 2.",
                       "Truy vấn Q3 (Lấy đường dẫn tổ tiên): Path Enum dùng toán tử chứa cha path @> '1.2.4'; Closure Table lọc descendant_id = 4 AND depth > 0.",
                       "Truy vấn Q8 (Đếm số hậu duệ): Nested Set đạt tốc độ siêu việt O(1) nhờ công thức số học: (rgt - lft + 1) / 2 mà không cần quét bảng!"])
    add_speaker_script(doc,
        "Để so sánh công bằng giữa 4 mô hình, nhóm đã thiết lập Bộ Quy ước Chuẩn tắc Ground Truth: cây con của nút X bắt buộc phải gồm chính X, còn chuỗi tổ tiên thì không chứa chính nó.\n"
        "Nhóm đã viết đầy đủ 40 câu truy vấn SQL chuẩn cho 10 bài toán nghiệp vụ từ Q1 đến Q10:\n"
        "• Ở truy vấn Q1 - Duyệt cây hiển thị thụt đầu dòng: Trong khi Adjacency List phải viết biểu thức bảng chung WITH RECURSIVE dài 15 dòng kết hợp mảng sắp xếp đường dẫn, thì Path Enumeration chỉ cần đúng 1 dòng ORDER BY path là dữ liệu tự động sắp xếp theo thứ tự duyệt cây trước!\n"
        "• Ở truy vấn Q8 - Đếm tổng số phản hồi con: Nested Set thể hiện vẻ đẹp toán học với độ phức tạp O(1). Chỉ cần lấy (rgt - lft + 1) / 2 là ra ngay kết quả mà không cần máy chủ phải đếm từng dòng dữ liệu.\n"
        "Toàn bộ 40 truy vấn đều đã được chạy kiểm nghiệm tự động và đối soát trả về kết quả 100% đồng nhất.",
        "Câu hỏi: Tại sao truy vấn Q3 trong Closure Table lại cần điều kiện depth > 0?\n"
        "Trả lời: Thưa Thầy/Cô, vì trong Closure Table, mỗi nút luôn có một bản ghi tự tham chiếu chính nó với depth = 0 (ví dụ cặp (4, 4, depth=0)). Theo quy ước Ground Truth của đề tài, tổ tiên thực sự không bao gồm chính nút đó, do đó điều kiện depth > 0 là bắt buộc để lọc bỏ bản ghi tự thân.")

    # Slide 7
    add_slide_header(doc, 7, "Thao tác Ghi CRUD & Ma trận So sánh Độ phức tạp Big-O", "Thanh Hưng (TV2)", "3.0 phút")
    add_slide_content(doc, "Phân tích chi phí thuật toán của các thao tác ghi (Chèn nút lá, Di chuyển nhánh cây con) và bảng ma trận Big-O.",
                      ["Thao tác Chèn lá (Insert Leaf): Adjacency và Path Enum đạt O(1); Nested Set chịu án phạt O(N) do phải UPDATE lft, rgt trên nửa cây!",
                       "Thao tác Di chuyển nhánh (Move Subtree): Adjacency cực nhanh O(1) (UPDATE parent_id); Path Enum O(K) đổi chuỗi; Nested Set cực kỳ phức tạp.",
                       "Giải thuật Move Subtree trong Nested Set: Đưa nhánh sang vùng số âm, thu hẹp cây cũ, mở rộng cây mới, tính displacement đưa nhánh về.",
                       "Bảng ma trận Big-O: Đọc cây con (Adjacency: O(K) chậm nhất, 3 mô hình còn lại: O(log N + K)); Ghi chèn (Nested Set O(N) tệ nhất).",
                       "Khuyến nghị kỹ thuật: Path Enumeration (ltree) là sự dung hòa toán học hoàn hảo nhất giữa tốc độ đọc và chi phí ghi."])
    add_speaker_script(doc,
        "Thưa Thầy Cô, điểm phân hóa lớn nhất giữa các mô hình cây không nằm ở thao tác đọc mà nằm ở chi phí của các thao tác GHI (CRUD):\n"
        "1. Khi chèn một bình luận lá mới: Trong Adjacency List và Path Enum, máy chủ chỉ chèn đúng 1 dòng dữ liệu (O(1)). Nhưng trong Nested Set, hệ thống bắt buộc phải chạy 2 câu lệnh UPDATE để cộng thêm 2 đơn vị cho toàn bộ các nút nằm bên phải vị trí chèn. Với bảng 100.000 dòng, thao tác này khóa hàng chục ngàn bản ghi, làm tốc độ ghi chậm hơn 600 lần!\n"
        "2. Khi di chuyển một nhánh bình luận: Adjacency chỉ tốn 1 lệnh sửa parent_id. Còn với Nested Set, nhóm đã phải viết cả một Stored Procedure phức tạp: tạm thời đưa tọa độ nhánh sang số âm để tránh xung đột, co cụm cây cũ, nới rộng cây mới rồi dời nhánh về.\n"
        "Tổng kết ma trận Big-O trên slide cho thấy: Path Enumeration ltree là người chiến thắng toàn diện trong các mạng xã hội hiện đại: đọc nhanh như Nested Set nhưng ghi nhanh như Adjacency List.",
        "Câu hỏi: Kỹ thuật Gaps trong Nested Set có giải quyết triệt để được vấn đề chậm khi chèn nút mới không?\n"
        "Trả lời: Thưa Thầy/Cô, kỹ thuật Gaps (để dành khoảng trống cách nhau 1.000 đơn vị) chỉ giải quyết được tạm thời trong giai đoạn đầu. Khi khoảng trống bị lấp đầy sau nhiều lần chèn, hệ thống bắt buộc phải chạy một giao dịch bảo trì lớn để đánh số lại toàn bộ cây. Quá trình này sẽ khóa chặt toàn bộ bảng dữ liệu, do đó nó không phù hợp cho các mạng xã hội có tần suất bình luận liên tục.")

    # Slide 8
    add_slide_header(doc, 8, "CSDL Hướng đối tượng ODMG 3.0: ODL, OQL & Ánh xạ JPQL", "Thanh Hưng (TV2)", "3.0 phút")
    add_slide_content(doc, "Mô hình hóa hướng đối tượng chuẩn ODMG 3.0 với 6 lớp đối tượng, 8 truy vấn OQL và giải quyết Lệch pha trở kháng.",
                      ["Sơ đồ 6 Lớp đối tượng (UML Class Diagram): NguoiDung, NhomHocTap, BaiDang (Siêu lớp), BaiThaoLuan, BaiTaiLieu, BinhLuan.",
                       "Lược đồ ODL: Khai báo đầy đủ phạm vi thể hiện (extent), khóa định danh (key), thuộc tính đa trị set<string>, và quan hệ đối ứng inverse.",
                       "Bộ 8 truy vấn OQL chuẩn: Điều hướng qua dấu chấm (.) không cần JOIN, toán tử đa hình IS_OF_CLASS, và hàm gộp đối tượng.",
                       "Ánh xạ ORM / JPA / JPQL: Ánh xạ thực thể Hibernate, giải quyết triệt để vấn đề kinh điển N+1 Selects Problem bằng @EntityGraph.",
                       "5 Khía cạnh Lệch pha trở kháng (Impedance Mismatch): Định danh, Đóng gói, Kế thừa, Kiểu dữ liệu và Điều hướng quan hệ."])
    add_embedded_image(doc, "oo_model/class_diagram.png", "Sơ đồ 6 Lớp đối tượng ODMG 3.0 (UML Class Diagram) Hệ thống Mạng xã hội học tập", 5.6)
    add_speaker_script(doc,
        "Tiếp theo, em xin trình bày về phân hệ CSDL Hướng đối tượng tuân thủ chuẩn quốc tế ODMG 3.0.\n"
        "Nhìn vào Hình 5.1 trên slide, nhóm đã thiết kế Sơ đồ lớp gồm 6 thực thể. Điểm đặc sắc của ngôn ngữ định nghĩa ODL là hỗ trợ từ khóa inverse: khi thiết lập quan hệ tác giả cho một bài viết, danh sách bài viết của người dùng đó sẽ tự động được cập nhật hai chiều mà không cần viết trigger.\n"
        "Về ngôn ngữ truy vấn đối tượng OQL, lập trình viên có thể điều hướng tự nhiên qua các liên kết: ví dụ p.tac_gia.email thay vì phải JOIN hai bảng như trong SQL.\n"
        "Nhóm cũng đã nghiên cứu sâu 5 khía cạnh 'Lệch pha trở kháng' giữa OOP và RDBMS. Đặc biệt, nhóm đã xử lý thành công vấn nạn N+1 Selects Problem trong Hibernate bằng cách áp dụng @EntityGraph và JPQL JOIN FETCH, gom 21 câu truy vấn lẻ thành đúng 1 câu lệnh JOIN duy nhất.\n"
        "Tiếp theo, em xin kính mời bạn Quang Hữu trình bày Phần 3 về Lược đồ vật lý, SQL nâng cao và Quản trị giao dịch.",
        "Câu hỏi: OQL khác gì so với SQL truyền thống trong việc xử lý kế thừa đa hình?\n"
        "Trả lời: Thưa Thầy/Cô, trong SQL truyền thống, nếu muốn lọc bài viết tài liệu từ bảng kế thừa, ta phải so sánh chuỗi WHERE post_type = 'tailieu'. Trong khi đó, OQL hỗ trợ toán tử hướng đối tượng nguyên bản: WHERE p IS_OF_CLASS(BaiTaiLieu), cho phép công cụ CSDL tự động kiểm tra kiểu đối tượng trong bộ nhớ một cách an toàn kiểu (Type-safe).")

    # ========================================================
    # PHẦN 3: QUANG HỮU (SLIDES 9 - 12)
    # ========================================================
    # Slide 9
    add_slide_header(doc, 9, "Thiết kế Lược đồ CSDL Quan hệ Vật lý (PostgreSQL 18.6)", "Quang Hữu (TV3)", "3.0 phút")
    add_slide_content(doc, "Hiện thực hóa lược đồ vật lý 13 bảng trên PostgreSQL 18.6 cùng hệ thống khóa chính, khóa ngoại và chỉ mục chuyên biệt.",
                      ["Kiến trúc 13 bảng vật lý: Phân hệ tài khoản (users, friendship, user_follow), Phân hệ nhóm (study_group, group_members), Phân hệ bài viết (post, post_reaction)...",
                       "Hệ thống khóa chính tự tăng: Sử dụng chuẩn SQL hiện đại INT GENERATED ALWAYS AS IDENTITY thay cho kiểu SERIAL cũ.",
                       "Cưỡng chế toàn vẹn tham chiếu: ON DELETE CASCADE cho bình luận, cảm xúc; ON DELETE RESTRICT cho chủ sở hữu nhóm học tập.",
                       "Hiện thực hóa Single Table Inheritance: Bảng post chứa cột phân loại post_type kèm CHECK constraints có điều kiện.",
                       "Chiến lược đánh chỉ mục: B-Tree trên toàn bộ khóa ngoại; GiST trên path ltree; GIN trên vector tìm kiếm toàn văn Full-Text Search."])
    add_embedded_image(doc, "docs/relational_schema_diagram.png", "Sơ đồ Lược đồ CSDL Quan hệ Vật lý (Physical Relational Schema) trên PostgreSQL 18.6", 5.6)
    add_speaker_script(doc,
        "Kính chào Quý Thầy Cô! Em tên là Quang Hữu, phụ trách thiết kế lược đồ vật lý, lập trình SQL nâng cao và quản trị giao dịch.\n"
        "Hình 1.2 trên slide là toàn bộ kiến trúc Lược đồ CSDL Quan hệ Vật lý của đề tài chạy trực tiếp trên PostgreSQL 18.6.\n"
        "Lược đồ gồm 13 bảng vật lý được chuẩn hóa tối ưu. Em xin làm rõ 3 giải pháp kỹ thuật nổi bật:\n"
        "1. Toàn bộ các bảng đều sử dụng chuẩn SQL hiện đại GENERATED ALWAYS AS IDENTITY để quản lý khóa chính tự tăng, ngăn chặn hoàn toàn việc chèn đè ID thủ công làm sai lệch chuỗi tuần tự.\n"
        "2. Về ràng buộc toàn vẹn: Nhóm áp dụng ON DELETE RESTRICT trên trường owner_id của nhóm học tập, ngăn không cho xóa tài khoản người dùng nếu họ vẫn đang là chủ nhóm chưa bàn giao.\n"
        "3. Ở bảng post, nhóm áp dụng kỹ thuật Single Table Inheritance với ràng buộc CHECK (post_type <> 'tailieu' OR file_url IS NOT NULL) để bảo đảm tính chặt chẽ về dữ liệu mà vẫn giữ trọn vẹn ưu thế quét đĩa O(1).",
        "Câu hỏi: Tại sao nhóm không dùng kiểu UUID làm khóa chính mà lại dùng số nguyên INT tự tăng IDENTITY?\n"
        "Trả lời: Thưa Thầy/Cô, việc chọn INT (4 bytes) hoặc BIGINT (8 bytes) thay vì UUID (16 bytes) là một quyết định tối ưu hóa bộ nhớ có chủ đích: Khóa chính số nguyên nhỏ hơn 4 lần so với UUID, giúp cây chỉ mục B-Tree gọn nhẹ hơn rất nhiều, chứa được nhiều con trỏ hơn trên mỗi trang đĩa 8KB và giữ được tỷ lệ cache hit cao trong RAM. Hơn nữa, số nguyên tuần tự giúp loại bỏ hiện tượng phân mảnh trang đĩa (Page Splitting) khi chèn dữ liệu mới.")

    # Slide 10
    add_slide_header(doc, 10, "Bộ 8 Truy vấn SQL Nâng cao (Q1 – Q8)", "Quang Hữu (TV3)", "3.0 phút")
    add_slide_content(doc, "Khai thác các tính năng hiện đại nhất của PostgreSQL: Window Functions, CUBE/ROLLUP, Full-Text Search và JSONB.",
                      ["Q1 (Window Functions): Sử dụng DENSE_RANK() OVER (PARTITION BY group_id) để xếp hạng thành viên tích cực nhất từng nhóm.",
                       "Q2 (Time-series Analysis): Sử dụng hàm LAG() lấy bài viết tháng trước, tính tỷ lệ phần trăm tăng trưởng (% growth) của cộng đồng.",
                       "Q3 (Báo cáo đa chiều): Sử dụng GROUP BY CUBE (topic, post_type) tự động sinh các dòng tổng phụ và đại tổng.",
                       "Q4 (Tìm kiếm toàn văn Full-Text Search): Sử dụng to_tsvector, to_tsquery và hàm xếp hạng ts_rank() kết hợp chỉ mục GIN.",
                       "Q5 (Phép chia quan hệ Relational Division): Tìm sinh viên tham gia TẤT CẢ các nhóm công khai chuyên đề KHMT bằng NOT EXISTS/EXCEPT.",
                       "Q6 (Dữ liệu bán cấu trúc JSONB): Sử dụng toán tử containment @> truy vấn các tài liệu học tập có chứng chỉ hoàn thành."])
    add_speaker_script(doc,
        "Trên slide là bộ 8 truy vấn SQL phân tích nâng cao từ Q1 đến Q8 do nhóm xây dựng:\n"
        "• Ở truy vấn Q1 và Q2: Nhóm khai thác tối đa sức mạnh của các Hàm cửa sổ Window Functions. Thay vì phải viết các câu lệnh SELECT lồng nhau tốn kém, DENSE_RANK() phân vùng theo group_id xếp hạng học viên cực nhanh; còn hàm LAG() cho phép nhìn ngược về tháng trước để tính phần trăm tăng trưởng bài viết.\n"
        "• Ở truy vấn Q3: Mệnh đề GROUP BY CUBE tự động tạo ra một khối dữ liệu phân tích đa chiều giữa chuyên đề học tập và thể loại bài đăng, sinh ra các dòng tổng phụ cho ban quản hiệu nhà trường.\n"
        "• Ở truy vấn Q4: Hệ thống tích hợp công cụ tìm kiếm toàn văn Full-Text Search. Nhờ chỉ mục GIN, truy vấn tìm từ khóa trong hàng trăm ngàn bài viết diễn ra tức thì với độ trễ dưới 1 mili-giây.\n"
        "• Ở truy vấn Q5: Nhóm hiện thực hóa phép chia quan hệ kinh điển để tìm ra các bạn sinh viên xuất sắc nhất tham gia toàn bộ các nhóm học tập.",
        "Câu hỏi: Phép chia quan hệ trong truy vấn Q5 được thực thi như thế nào nếu bảng nhóm có thêm một nhóm mới?\n"
        "Trả lời: Thưa Thầy/Cô, câu truy vấn Q5 sử dụng biểu thức lồng NOT EXISTS kết hợp phép trừ tập hợp EXCEPT. Mỗi khi có nhóm công khai mới được tạo, tập hợp tất cả các nhóm sẽ tự động tăng lên. Do đó, câu truy vấn sẽ lập tức đòi hỏi sinh viên phải tham gia cả nhóm mới đó thì mới xuất hiện trong kết quả, bảo đảm tính linh hoạt và chính xác tuyệt đối theo thời gian thực.")

    # Slide 11
    add_slide_header(doc, 11, "Lập trình Tầng Máy chủ: Triggers, Stored Procedures & Python", "Quang Hữu (TV3)", "3.0 phút")
    add_slide_content(doc, "Đóng gói logic nghiệp vụ tầng CSDL: Triggers kiểm soát đóng bài, Thủ tục kết bạn an toàn, UDF danh tiếng và Ứng dụng nhúng Python.",
                      ["Q9 (Database Trigger): trg_check_comment_post_closed chặn ngay lập tức thao tác chèn bình luận vào bài thảo luận đã đóng (is_closed=TRUE).",
                       "Q10 (Stored Procedure proc_add_friend): Tự động sắp xếp chuẩn tắc LEAST/GREATEST, cập nhật bộ đếm friend_count và sinh notification trong 1 giao dịch.",
                       "Q11 (User-Defined Function): fn_calculate_reputation_score tính điểm danh tiếng dựa trên công thức trọng số: 5*bài + 2*bình luận + 1*like.",
                       "Q12 (Dynamic View v_social_feed): View động tính điểm thịnh hành thời gian thực kết hợp thuật toán suy giảm theo thời gian (Time-decay).",
                       "Ứng dụng nhúng Python (psycopg2): Quản trị bể kết nối ThreadedConnectionPool, con trỏ tham số hóa (Parameterized Queries) loại trừ 100% SQL Injection."])
    add_speaker_script(doc,
        "Để bảo đảm toàn vẹn dữ liệu và giảm thiểu tải cho tầng ứng dụng, nhóm đã chuyển các logic nghiệp vụ quan trọng vào tầng máy chủ CSDL (Server-Side Programming):\n"
        "• Ở Q9: Nhóm viết Trigger Before Insert chặn đứng hành vi bình luận vào các bài đã đóng, ném ra mã lỗi check_violation rõ ràng.\n"
        "• Ở Q10: Toàn bộ quy trình kết bạn được đóng gói trong Stored Procedure proc_add_friend. Thủ tục tự động tính LEAST và GREATEST giữa 2 ID để bảo đảm thứ tự chuẩn tắc, tăng bộ đếm bạn bè và phát sinh thông báo trong một giao dịch ACID nguyên tử.\n"
        "• Ở Q12: View v_social_feed tính điểm 'Hot Score' của bài viết dựa trên công thức tương tác chia cho lũy thừa thời gian, giúp các bài viết mới và bổ ích luôn nổi lên đầu Bảng tin.\n"
        "Đồng thời, nhóm xây dựng module Python hoàn chỉnh với thư viện psycopg2, thiết lập ThreadedConnectionPool và sử dụng con trỏ tham số hóa, phòng chống tuyệt đối lỗ hổng SQL Injection nguy hiểm.",
        "Câu hỏi: Việc đưa nhiều logic nghiệp vụ vào Stored Procedures và Triggers có gây quá tải CPU cho máy chủ CSDL không?\n"
        "Trả lời: Thưa Thầy/Cô, đây là sự đánh đổi giữa băng thông mạng và năng lực CPU: Việc chạy Stored Procedure loại bỏ hoàn toàn các round-trips mạng qua lại giữa Web Server và DB Server, giúp giao dịch hoàn thành nhanh hơn gấp nhiều lần và giảm thời gian giữ khóa dòng (Lock Hold Time). Hơn nữa, việc cưỡng chế bằng Trigger đảm bảo an toàn dữ liệu 100% ngay cả khi có nhiều ứng dụng khác nhau (Web, Mobile App) cùng truy cập trực tiếp vào CSDL.")

    # Slide 12
    add_slide_header(doc, 12, "SQL Đệ quy trên Đồ thị bạn bè (R1 – R4) & Giao dịch T1 – T2", "Quang Hữu (TV3)", "3.0 phút")
    add_slide_content(doc, "Giải quyết 4 bài toán đồ thị bằng WITH RECURSIVE của SQL:1999 và quản trị giao dịch an toàn.",
                      ["Bài toán R1 (Friends of Friends): Tìm bạn của bạn và đếm số bạn chung (mutual friends) bằng 2 tầng CTE đệ quy.",
                       "Bài toán R2 (k-Hop Reachability): Khảo sát mạng lưới kết nối lan tỏa trong phạm vi k=3 chặng kèm mảng visited.",
                       "Bài toán R3 (Shortest Path BFS): Thuật toán tìm kiếm theo chiều rộng trong SQL đệ quy, tìm đường đi ngắn nhất giữa 2 học viên.",
                       "Bài toán R4 (Cycle Detection): Phát hiện các vòng lặp quan hệ theo dõi bằng điều kiện followed_id = ANY(path).",
                       "Giao dịch T1 (Chuyển điểm danh tiếng): Áp dụng khóa bi quan SELECT FOR UPDATE theo thứ tự ID tăng dần, triệt tiêu nguy cơ bế tắc."])
    add_speaker_script(doc,
        "Phần cuối của chương 4 là các bài toán đồ thị xã hội được giải quyết bằng chuẩn SQL đệ quy WITH RECURSIVE:\n"
        "• Bài toán R1: Hệ thống tìm kiếm các bạn của bạn chưa kết bạn với An, đồng thời đếm số bạn chung và liệt kê danh sách bạn chung để đưa ra tính năng 'Những người bạn có thể biết'.\n"
        "• Bài toán R3: Nhóm hiện thực hóa thuật toán Breadth-First Search (BFS) ngay trong lòng câu lệnh SQL. Bằng cách lưu mảng đường dẫn visited và dừng đệ quy khi gặp đích, truy vấn trả về chính xác đường đi ngắn nhất giữa bạn An và bạn Giang với độ dài 2 chặng.\n"
        "• Về quản trị giao dịch: Trong giao dịch T1 chuyển nhượng điểm danh tiếng giữa 2 tài khoản, nhóm tuân thủ nghiêm ngặt quy tắc Khóa theo thứ tự xác định (Ordered Locking): luôn khóa ID nhỏ trước, ID lớn sau. Quy tắc này triệt tiêu hoàn toàn khả năng hình thành chu trình chờ khóa.\n"
        "Tiếp theo, em xin kính mời bạn Chương Võ trình bày Phần 4 về CSDL Đồ thị Neo4j và thực nghiệm bế tắc Deadlock.",
        "Câu hỏi: Thuật toán BFS trong SQL đệ quy có nguy cơ bị lặp vô tận (Infinite Loop) nếu đồ thị có chu trình không?\n"
        "Trả lời: Thưa Thầy/Cô, hoàn toàn không bị lặp vô tận vì nhóm đã cài đặt mảng lịch sử visited_array. Tại mỗi bước mở rộng đệ quy, điều kiện WHERE NOT (next_id = ANY(path_nodes)) sẽ lập tức loại bỏ các nút đã từng đi qua, đảm bảo thuật toán luôn dừng chính xác.")

    # ========================================================
    # PHẦN 4: CHƯƠNG VÕ (SLIDES 13 - 16)
    # ========================================================
    # Slide 13
    add_slide_header(doc, 13, "CSDL Đồ thị Chuyên dụng Neo4j & Đối chiếu Cypher", "Chương Võ (TV4)", "3.0 phút")
    add_slide_content(doc, "Triển khai máy chủ đồ thị Neo4j 5.x Community trên Docker và mô hình hóa Đồ thị thuộc tính (LPG).",
                      ["Kiến trúc Docker: Triển khai Neo4j 5.x Community độc lập (Port 7474 HTTP Browser, Port 7687 Bolt nhị phân).",
                       "Mô hình Labeled Property Graph (LPG): Các nút mang nhãn :User, :Group; các cạnh có hướng và thuộc tính :FRIEND_WITH, :MEMBER_OF.",
                       "Bản chất vượt trội của Neo4j: Cơ chế Duyệt kề không dùng chỉ mục (Index-free Adjacency) với con trỏ bộ nhớ vật lý O(1).",
                       "So sánh cú pháp Cypher vs SQL: Cypher sử dụng mô hình khớp mẫu hình học MATCH (u)-[:FRIEND_WITH]->(f) cực kỳ trực quan.",
                       "Ràng buộc Schema Constraints trên Neo4j: Cưỡng chế tính duy nhất UNIQUE trên user_id và post_id."])
    add_embedded_image(doc, "neo4j/screenshots/01_neo4j_full_graph.png", "Toàn cảnh Đồ thị Mạng xã hội học tập hiển thị trên Neo4j Browser (Graph View)", 5.6)
    add_speaker_script(doc,
        "Kính chào Quý Thầy Cô! Em tên là Chương Võ, phụ trách triển khai CSDL đồ thị Neo4j, thực nghiệm bế tắc Deadlock và thử tải đồng thời pgbench.\n"
        "Nhìn vào Hình 5.2 trên slide là giao diện Neo4j Browser trực quan hóa mạng xã hội học tập của nhóm chạy trên nền tảng Docker.\n"
        "Trong khi PostgreSQL lưu dữ liệu thành các bảng phẳng và liên kết qua khóa ngoại, Neo4j tổ chức dữ liệu dưới dạng Đồ thị thuộc tính (Labeled Property Graph). Điểm tạo nên sự vượt trội của Neo4j là cơ chế Index-free Adjacency: mỗi nút lưu trữ trực tiếp các con trỏ bộ nhớ RAM trỏ tới các nút lân cận. Do đó, việc bước qua một cạnh quan hệ có độ phức tạp O(1) bất biến, hoàn toàn không phụ thuộc vào việc đồ thị có 1.000 nút hay 10 triệu nút.\n"
        "Ngôn ngữ Cypher với cú pháp mũi tên vẽ lại chính xác cấu trúc đồ thị, giúp câu truy vấn ngắn gọn và dễ bảo trì hơn SQL đệ quy rất nhiều.",
        "Câu hỏi: Neo4j có hỗ trợ giao dịch ACID đầy đủ như PostgreSQL không?\n"
        "Trả lời: Thưa Thầy/Cô, Neo4j là một hệ quản trị CSDL đồ thị thương mại tuân thủ ACID 100%. Mọi thao tác ghi Cypher đều được bao bọc trong transaction, ghi nhật ký Write-Ahead Log và hỗ trợ các mức cô lập giao dịch an toàn.")

    # Slide 14
    add_slide_header(doc, 14, "4 Bài toán Đồ thị trên Cypher & Phân tích Độ sâu k", "Chương Võ (TV4)", "3.0 phút")
    add_slide_content(doc, "Hiện thực 4 bài toán đồ thị R1-R4 trên Cypher và bảng đối soát hiệu năng theo độ sâu đồ thị k.",
                      ["Bài toán R1 (Friends of Friends): MATCH (an)-[:FRIEND_WITH]-(f)-[:FRIEND_WITH]-(fof) lọc ra chính xác Cúc (2 bạn chung) và Giang (1 bạn chung).",
                       "Bài toán R2 (Đường đi ngắn nhất): Hàm tích hợp shortestPath((an)-[:FRIEND_WITH*]-(giang)) trả về đường An -> Bình -> Giang (len=2).",
                       "Bài toán R3 (Phát hiện chu trình): MATCH p = (a)-[:FRIEND_WITH*3..6]-(a) phát hiện 3 chu trình tam giác trong mạng lưới.",
                       "Bảng đo lường theo độ sâu k: Tại k=1..2, PostgreSQL ngang ngửa Neo4j (~0.05ms); Nhưng tại k=4, PostgreSQL tốn 12.4ms trong khi Neo4j chỉ tốn 0.18ms (Nhanh hơn 70 lần!); Tại k=5, Neo4j nhanh hơn 400 lần!",
                       "Nguyên nhân: PostgreSQL phải Hash Join bùng nổ theo hàm mũ O(B^k), còn Neo4j chỉ tốn chi phí tuyến tính O(k)."])
    add_embedded_image(doc, "neo4j/screenshots/03_neo4j_shortest_path.png", "Đường đi ngắn nhất giữa hai học viên An và Giang trên Neo4j Browser", 5.6)
    add_speaker_script(doc,
        "Trên slide là kết quả thực thi 4 bài toán đồ thị trên Neo4j bằng ngôn ngữ Cypher:\n"
        "Hình 5.4 thể hiện thuật toán shortestPath tìm đường đi học tập ngắn nhất giữa bạn An và cô Giang. Cypher tìm ra đường đi An -> Bình -> Giang chỉ trong nháy mắt.\n"
        "Đặc biệt, bảng số liệu thực nghiệm ở Chương 5 đã vạch rõ ranh giới kỹ thuật giữa hai nền tảng:\n"
        "• Khi độ sâu đồ thị k <= 2 chặng (bạn trực tiếp hoặc bạn của bạn), PostgreSQL xử lý cực nhanh (~0.05ms), hoàn toàn tương đương Neo4j nhờ chỉ mục B-Tree.\n"
        "• Nhưng khi độ sâu tăng lên k = 4 và k = 5 chặng, chi phí JOIN của PostgreSQL bùng nổ dữ dội lên 180 ms và có nguy cơ tràn bộ nhớ work_mem. Trong khi đó, Neo4j vẫn duy trì tốc độ ấn tượng dưới 0.5 mili-giây, nhanh hơn PostgreSQL tới 400 lần!\n"
        "Điều này khẳng định: với các mạng lưới kết nối sâu, CSDL đồ thị chuyên dụng là giải pháp không thể thay thế.",
        "Câu hỏi: Nếu Neo4j nhanh như vậy, tại sao chúng ta không thay thế hoàn toàn PostgreSQL bằng Neo4j?\n"
        "Trả lời: Thưa Thầy/Cô, Neo4j tối ưu vượt trội cho các phép duyệt đồ thị, nhưng với các tác vụ quét bảng hàng loạt (Table Scans), tính toán tổng hợp tài chính số lượng lớn (Aggregation SUM, COUNT trên hàng triệu dòng) hoặc xử lý cây phân cấp bảng tin thì PostgreSQL lại tối ưu và tiết kiệm tài nguyên hơn nhiều. Do đó, mô hình lai ghép Đa lưu trữ (Polyglot) là sự kết hợp hoàn hảo nhất.")

    # Slide 15
    add_slide_header(doc, 15, "Thực nghiệm Bế tắc Giao dịch (Deadlock T3) & Phòng chống", "Chương Võ (TV4)", "3.0 phút")
    add_slide_content(doc, "Tái hiện thành công hiện tượng bế tắc Deadlock T3 trên 2 session PostgreSQL, phân tích đồ thị WFG và giải pháp.",
                      ["Khái niệm: Bế tắc xảy ra khi 2 phiên cùng giữ tài nguyên này và chờ tài nguyên kia, tạo thành chu trình trên Đồ thị Chờ khóa (WFG).",
                       "Kịch bản thực nghiệm: Session A khóa user_id=1 chờ user_id=2; Session B khóa user_id=2 chờ user_id=1. Xuất hiện chu trình A -> B -> A.",
                       "Cơ chế phát hiện của PostgreSQL: Sau deadlock_timeout = 1000ms, Deadlock Detector ngắt Session A với mã lỗi SQLSTATE 40P01.",
                       "Trích xuất Log thực tế: 'ERROR: deadlock detected... Process 16484 waits for ExclusiveLock... blocked by process 13804'.",
                       "3 Nguyên tắc vàng phòng chống bế tắc: (1) Ordered Locking (LEAST/GREATEST); (2) SELECT FOR UPDATE NOWAIT; (3) SKIP LOCKED."])
    add_embedded_image(doc, "docs/concurrency_wfg_diagram.png", "Đồ thị Chờ khóa (Wait-For Graph - WFG) gây ra Bế tắc (Deadlock T3) giữa 2 Session", 5.6)
    add_speaker_script(doc,
        "Một trong những điểm nhấn thực nghiệm quan trọng của đề tài là việc tái hiện và kiểm soát thành công hiện tượng Bế tắc giao dịch (Deadlock T3).\n"
        "Nhìn vào Sơ đồ Đồ thị Chờ khóa WFG trên Hình 4.1: Session A giữ khóa bản ghi số 1 và đòi khóa bản ghi số 2; đồng thời Session B giữ khóa bản ghi số 2 và đòi khóa bản ghi số 1. Hai phiên tạo thành một chu trình phụ thuộc vòng tròn A -> B -> A.\n"
        "Đúng sau 1 giây (deadlock_timeout), bộ giám sát bế tắc của PostgreSQL đã phát hiện chu trình, chủ động hủy bỏ (ABORT) Session A và ném ra mã lỗi chuẩn SQLSTATE 40P01 như trong nhật ký log nguyên bản trên slide, giải phóng cho Session B hoàn thành commit an toàn.\n"
        "Từ thực nghiệm này, nhóm đúc kết 3 nguyên tắc vàng cho môi trường sản xuất: luôn khóa tài nguyên theo thứ tự tăng dần LEAST/GREATEST, sử dụng NOWAIT để lập trình cơ chế thử lại (Retry Loop), và áp dụng SKIP LOCKED cho hàng đợi thông báo.",
        "Câu hỏi: Làm thế nào PostgreSQL chọn session nào để hủy (victim transaction) khi xảy ra Deadlock?\n"
        "Trả lời: Thưa Thầy/Cô, PostgreSQL thường ưu tiên chọn hủy phiên giao dịch vừa phát sinh câu lệnh làm khép kín chu trình bế tắc (the transaction that triggered the deadlock cycle), hoặc phiên có thời gian chạy ngắn hơn nhằm giảm thiểu chi phí hoàn tác dữ liệu (Rollback cost).")

    # Slide 16
    add_slide_header(doc, 16, "Thử tải Đồng thời bằng pgbench & Ma trận Cô lập", "Chương Võ (TV4)", "3.0 phút")
    add_slide_content(doc, "Thử tải Stored Procedure bằng pgbench trên 3 mức tải và kiểm nghiệm thực tế ma trận cô lập giao dịch ANSI SQL.",
                      ["Thử tải pgbench trên proc_add_friend: Khảo sát tại 5, 10, và 20 Clients đồng thời qua kịch bản tự động hóa run_pgbench.ps1.",
                       "Kết quả ấn tượng: Đạt thông lượng ổn định ~3,440 TPS, tỷ lệ lỗi 0.000% (0 lỗi Deadlock) nhờ cơ chế khóa chuẩn tắc LEAST/GREATEST.",
                       "Chứng minh Định luật Little (Little's Law: N = X * R): Khi TPS bão hòa phần cứng, số clients tăng gấp đôi thì độ trễ tăng tuyến tính gấp đôi (1.45ms -> 2.90ms -> 5.81ms).",
                       "Ma trận cô lập giao dịch: Kiểm chứng 4 dị thường (Dirty Read, Non-Repeatable Read, Phantom Read, Write Skew).",
                       "PostgreSQL SSI (Serializable Snapshot Isolation): Phát hiện dị thường Write Skew và chủ động ABORT với mã lỗi SQLSTATE 40001!"])
    add_speaker_script(doc,
        "Để đánh giá năng lực chịu tải thực tế, nhóm đã sử dụng công cụ tiêu chuẩn công nghiệp pgbench để thử tải Stored Procedure kết bạn trên 3 mức đồng thời: 5, 10 và 20 Clients.\n"
        "Kết quả đo lường thực tế rất ấn tượng: Hệ thống đạt thông lượng tối đa xấp xỉ 3.445 TPS với 100% giao dịch thành công và 0% tỷ lệ lỗi bế tắc. Kết quả này hoàn toàn tuân theo Định luật Little: khi thông lượng chạm ngưỡng bão hòa năng lực phần cứng, số kết nối tăng gấp đôi thì độ trễ phản hồi tăng tuyến tính từ 1.45ms lên 5.81ms mà không làm sụp đổ hệ thống.\n"
        "Về mức cô lập: Nhóm đã thực nghiệm tái hiện dị thường Write Skew giữa 2 session đồng thời. Cơ chế Serializable Snapshot Isolation (SSI) của PostgreSQL đã phát hiện xung đột phụ thuộc đọc-ghi và ngắt phiên thứ hai với mã lỗi SQLSTATE 40001, bảo vệ toàn vẹn quỹ điểm thưởng của nhóm.\n"
        "Tiếp theo, em xin kính mời bạn Như Quỳnh trình bày Phần 5 về Đo lường dung lượng đĩa, Kết quả Benchmark 360 runs và Tổng kết đề tài.",
        "Câu hỏi: Định luật Little có ý nghĩa gì trong việc cấu hình Connection Pool của ứng dụng Web?\n"
        "Trả lời: Thưa Thầy/Cô, Định luật Little N = X * R chỉ ra rằng nếu thông lượng tối đa của máy chủ là 3,440 TPS và thời gian xử lý trung bình là 2.9ms, thì số lượng kết nối tối ưu chỉ cần khoảng 10 kết nối hoạt động đồng thời. Cấu hình Connection Pool quá lớn (hàng trăm kết nối) không làm tăng tốc độ mà chỉ gây lãng phí RAM và tăng chi phí chuyển đổi ngữ cảnh CPU (Context Switching).")

    # ========================================================
    # PHẦN 5: NHƯ QUỲNH (SLIDES 17 - 20)
    # ========================================================
    # Slide 17
    add_slide_header(doc, 17, "Thiết kế Vật lý & Đo lường Dung lượng Đĩa Lưu trữ", "Như Quỳnh (TV5)", "3.0 phút")
    add_slide_content(doc, "Phân tích cấu trúc vi mô trang đĩa 8KB, đo lường dung lượng lưu trữ thực tế (Heap + Index) tại quy mô 100.000 bản ghi.",
                      ["Vi cấu trúc trang đĩa 8KB (Page Layout): PageHeader (24B), Mảng con trỏ dòng ItemId (4B/dòng), và TupleHeader (23B) chứa Null Bitmap.",
                       "Cơ chế tối ưu hóa HOT (Heap-Only Tuples): Cập nhật không đổi cột chỉ mục thì không cần sửa cây B-Tree.",
                       "Số liệu dung lượng đĩa tại 100k nút: Adjacency (16.2 MB), Nested Set (17.0 MB), Path Enumeration (20.7 MB).",
                       "Hiện tượng bùng nổ không gian của Closure Table: Chiếm tới 92.62 MB đĩa cứng (Gấp gần 6 lần Adjacency List!).",
                       "Bản chất: Số lượng cặp quan hệ tổ tiên - hậu duệ trong bảng bao đóng bùng nổ lên tới 1,067,146 dòng dữ liệu!"])
    add_embedded_image(doc, "docs/benchmark_storage_chart.png", "Biểu đồ So sánh Dung lượng Lưu trữ Vật lý trên Đĩa (MB) giữa 4 Mô hình Cây tại 100.000 bản ghi", 5.6)
    add_speaker_script(doc,
        "Kính chào Quý Thầy Cô! Em tên là Như Quỳnh, phụ trách sinh dữ liệu lớn, đo lường dung lượng đĩa và tự động hóa bộ đo Benchmark Suite 360 runs.\n"
        "Nhìn vào Biểu đồ Hình 6.1 trên slide là kết quả đo lường dung lượng đĩa thực tế của 4 mô hình cây tại quy mô 100.000 bình luận:\n"
        "Trong khi 3 mô hình Adjacency List, Nested Set và Path Enumeration chỉ tiêu tốn từ 16 đến 20 MB bộ nhớ (gồm cả bảng heap và các chỉ mục), thì mô hình CLOSURE TABLE bùng nổ lên tới 92.62 MB, gấp gần 6 lần các mô hình còn lại!\n"
        "Bằng cách truy vấn bảng hệ thống pg_class, em phát hiện nguyên nhân bản chất: để quản lý 100.000 bình luận phân cấp, bảng phụ comment_closure đã phải lưu tới 1.067.146 dòng cặp quan hệ!\n"
        "Đây là một minh chứng thực nghiệm sống động cho cái giá phải trả về không gian lưu trữ khi chúng ta đánh đổi bộ nhớ để lấy tốc độ đọc của Closure Table.",
        "Câu hỏi: Tại sao dung lượng của Path Enumeration (20.7 MB) lại lớn hơn Adjacency List (16.2 MB)?\n"
        "Trả lời: Thưa Thầy/Cô, vì bảng Path Enumeration phải lưu chuỗi nhãn ltree có kích thước biến đổi (ví dụ '1.3.15.42') lớn hơn số nguyên INT 4 bytes của parent_id. Đồng thời, chỉ mục GiST trên cột path (5.02 MB) cũng có kích thước lớn hơn chỉ mục B-Tree thông thường (2.21 MB). Tuy nhiên, đổi lại mức chênh lệch 4 MB đĩa đó là tốc độ đọc cây con nhanh hơn tới 18 lần!")

    # Slide 18
    add_slide_header(doc, 18, "Benchmark Suite: Đọc Cây con Q2 & Ghi Chèn Lá mới", "Như Quỳnh (TV5)", "3.0 phút")
    add_slide_content(doc, "Kết quả 360 phép đo Benchmark tự động tại 3 quy mô (1k, 10k, 100k nút) trên 2 thao tác trọng yếu.",
                      ["Phương pháp luận Benchmark: 360 phép đo, warm-up cache 10 lần, trích xuất JSON Buffers bằng EXPLAIN (ANALYZE, BUFFERS).",
                       "Thao tác Đọc cây con Q2 (100k nút): Closure Table (0.039ms) và Nested Set (0.048ms) nhanh nhất; Path Enum đạt mức tuyệt vời 0.140ms; Adjacency chậm nhất (2.490ms, chậm hơn 63 lần!).",
                       "Phân tích Buffer Cache Q2: Adjacency tốn 38 khối Shared Buffers do đệ quy lặp; Path Enum chỉ tốn đúng 8 khối nhờ chỉ mục GiST.",
                       "Thao tác Ghi chèn nút lá mới (100k nút): Adjacency (0.070ms) và Path Enum (0.125ms) duy trì O(1) xuất sắc.",
                       "Sự sụp đổ hiệu năng ghi của Nested Set: Tăng từ 0.52ms (1k) lên 43.8ms (100k nút), chậm gấp hơn 600 lần Adjacency List!"])
    add_embedded_image(doc, "benchmark/results/charts/q2_subtree_100000.png", "Biểu đồ Thời gian truy vấn đọc cây con (Q2) tại quy mô 100.000 nút (ms)", 5.6)
    add_speaker_script(doc,
        "Tiếp theo, em xin công bố kết quả của Bộ thử nghiệm Benchmark 360 runs đo đạc trên máy chủ thực tế:\n"
        "1. Về thao tác ĐỌC cây con (Truy vấn Q2) trên biểu đồ Hình 6.4:\n"
        "Tại quy mô 100.000 bản ghi, mô hình Danh sách kề truyền thống mất tới 2.49 mili-giây và ngốn 38 khối Shared Buffers do phải chạy đệ quy nhiều thế hệ. Trong khi đó, Closure Table và Nested Set đọc siêu tốc dưới 0.05ms. Đáng chú ý nhất là Path Enumeration ltree: chỉ mất đúng 0.14 mili-giây và 8 khối cache RAM nhờ cấu trúc lọc tiền tố thông minh của chỉ mục GiST.\n"
        "2. Về thao tác GHI chèn nút lá mới (Insert Leaf):\n"
        "Adjacency List và Path Enum chứng minh ưu thế tuyệt đối khi duy trì chi phí O(1) ổn định từ 0.07ms đến 0.12ms. Ngược lại, Nested Set sụp đổ hiệu năng hoàn toàn: thời gian chèn nhảy vọt từ 0.52ms ở 1k nút lên tới 43.8 mili-giây ở 100k nút, chậm hơn 600 lần!\n"
        "Kết quả này khẳng định Nested Set hoàn toàn không thể dùng cho các hệ thống mạng xã hội có người dùng bình luận đồng thời.",
        "Câu hỏi: Tại sao nhóm phải chạy warm-up cache 10 lần trước khi lấy số liệu benchmark?\n"
        "Trả lời: Thưa Thầy/Cô, việc warm-up cache 10 lần là quy chuẩn thực nghiệm khoa học bắt buộc để loại trừ yếu tố ngẫu nhiên của việc đọc đĩa cơ học lần đầu (Cold Cache / Disk I/O). Việc warm-up đảm bảo dữ liệu và chỉ mục đã được nạp trọn vẹn vào Shared Buffer Pool của PostgreSQL, giúp phép đo phản ánh chính xác hiệu năng thuật toán và chi phí xử lý CPU của từng mô hình.")

    # Slide 19
    add_slide_header(doc, 19, "Benchmark Di chuyển Nhánh & Kiến trúc Đa Lưu trữ", "Như Quỳnh (TV5)", "3.0 phút")
    add_slide_content(doc, "Đánh giá thao tác di chuyển nhánh cây con (Move Subtree) và Đề xuất Kiến trúc Đa lưu trữ (Polyglot Persistence).",
                      ["Thao tác Move Subtree (100k nút): Adjacency chỉ mất 0.062ms (O(1)); Path Enum mất 0.56ms (đổi chuỗi tiền tố); Nested Set mất tới 138.5ms (cực chậm!).",
                       "Đúc kết lựa chọn mô hình cây: Path Enumeration (ltree) là giải pháp tối ưu toàn diện nhất cho chuỗi bình luận trên PostgreSQL.",
                       "Đề xuất Kiến trúc Đa lưu trữ (Polyglot Persistence): Dung hòa sức mạnh giữa RDBMS quan hệ và CSDL đồ thị.",
                       "PostgreSQL: Đóng vai trò Single Source of Truth (SSOT), quản lý tài khoản, bài viết, cây bình luận ltree và giao dịch ACID (~3,440 TPS).",
                       "Neo4j: Đóng vai trò Động cơ Phân tích Đồ thị (Graph Analytics Engine), nhận sự kiện đồng bộ qua Debezium/Kafka để phân tích mạng xã hội."])
    add_embedded_image(doc, "docs/polyglot_architecture_diagram.png", "Sơ đồ Kiến trúc Đa lưu trữ (Polyglot Persistence Architecture) kết hợp PostgreSQL và Neo4j", 5.6)
    add_speaker_script(doc,
        "Ở thao tác phức tạp nhất là Di chuyển nhánh cây con (Move Subtree):\n"
        "Số liệu đo đạc khẳng định Adjacency List vô địch với 0.06ms; Path Enum hoàn thành nhanh chóng trong 0.56ms; còn Nested Set phải mất tới hơn 138 mili-giây để tính toán lại tọa độ của toàn bộ cây.\n"
        "Từ toàn bộ các kết quả thực nghiệm trên, nhóm đề xuất Sơ đồ Kiến trúc Đa lưu trữ (Polyglot Persistence) trên Hình 5.6:\n"
        "Thay vì cố gắng gượng ép một CSDL duy nhất giải quyết mọi bài toán, hệ thống chia tách nhiệm vụ rõ ràng:\n"
        "• PostgreSQL làm Nguồn dữ liệu tin cậy duy nhất (Single Source of Truth), đảm nhận lưu trữ an toàn người dùng, bài đăng, cây bình luận bằng Path Enumeration ltree, và xử lý các giao dịch ACID với thông lượng 3.440 TPS.\n"
        "• Hàng đợi sự kiện CDC (Debezium và Kafka) sẽ bắt các thay đổi kết bạn và đồng bộ sang CSDL đồ thị Neo4j.\n"
        "• Neo4j chuyên biệt thực thi các thuật toán gợi ý bạn học, tìm đường đi ngắn nhất và phân tích cộng đồng.",
        "Câu hỏi: Làm thế nào đảm bảo dữ liệu giữa PostgreSQL và Neo4j không bị lệch pha khi có sự cố mạng ở tầng Kafka CDC?\n"
        "Trả lời: Thưa Thầy/Cô, Debezium đọc trực tiếp từ Write-Ahead Log (WAL) của PostgreSQL theo cơ chế ít nhất một lần (At-least-once delivery). Khi mạng phục hồi, Debezium sẽ tự động phát lại các sự kiện từ vị trí offset đã lưu. Phía Neo4j sử dụng các câu lệnh Cypher MERGE có tính chất lũy thừa (Idempotent), do đó việc nhận lại sự kiện trùng lặp không làm sai lệch dữ liệu đồ thị.")

    # Slide 20
    add_slide_header(doc, 20, "Tổng kết Đề tài, Phụ lục CLO7 & Hỏi đáp (Q&A)", "Như Quỳnh & Trần Quang", "2.5 phút")
    add_slide_content(doc, "Tổng kết các thành quả nghiên cứu chính, báo cáo làm việc nhóm chuẩn đầu ra CLO7 và mở phiên Hỏi đáp (Q&A).",
                      ["Hoàn thành 100% mục tiêu đề ra và giải quyết trọn vẹn 3 câu hỏi nghiên cứu (RQ1: Cây phân cấp, RQ2: Đồ thị mạng xã hội, RQ3: Đồng thời & Vật lý).",
                       "Sản phẩm hoàn chỉnh: Báo cáo tổng kết master De_tai_17_Bao_cao_Tong_ket.docx quy mô 110 trang, 20 sơ đồ 300 DPI, 105 bảng biểu đối sánh.",
                       "Báo cáo làm việc nhóm CLO7: Đầy đủ 8 biên bản họp nhóm tuần, bảng bản đồ Git commits, 100% thành viên được xếp loại A+ xuất sắc.",
                       "Kho lưu trữ GitHub công khai: https://github.com/TrkQuang/CSDL_Nangcao.git với mã nguồn sạch, chạy kiểm thử tự động.",
                       "Tập thể nhóm Đề tài 17 trân trọng cảm ơn Quý Thầy Cô và sẵn sàng lắng nghe các câu hỏi phản biện!"])
    add_speaker_script(doc,
        "Kính thưa Quý Thầy Cô trong Hội đồng phản biện!\n"
        "Qua quá trình làm việc nhóm nghiêm túc, khoa học và đoàn kết, Đề tài 17 đã hoàn thành 100% khối lượng công việc được giao:\n"
        "1. Đã giải quyết triệt để 3 câu hỏi nghiên cứu lớn về Cây phân cấp, Đồ thị xã hội và Điều khiển đồng thời.\n"
        "2. Đã biên soạn Báo cáo tổng kết hoàn chỉnh quy mô 110 trang A4, tích hợp 20 hình ảnh sơ đồ chất lượng cao và 105 bảng biểu số liệu chi tiết.\n"
        "3. Đã ghi nhận đầy đủ 8 biên bản họp nhóm định kỳ và bản đồ Git Commits, minh chứng cho năng lực làm việc nhóm đạt chuẩn đầu ra CLO7 của nhà trường.\n"
        "Thay mặt toàn thể 5 thành viên nhóm Đề tài 17, chúng em xin trân trọng cảm ơn Quý Thầy Cô đã chú ý lắng nghe bài thuyết trình!\n"
        "Nhóm chúng em rất mong nhận được những nhận xét, góp ý quý báu của Thầy Cô và sẵn sàng bước vào phần trả lời câu hỏi phản biện!",
        "Lời kết chuẩn bị: Nhóm đã sẵn sàng mở môi trường pgAdmin 4, Docker Neo4j Browser và terminal PowerShell để Demo trực tiếp bất kỳ câu truy vấn hoặc kịch bản nào mà Thầy Cô yêu cầu.")

    # Lưu file
    out_path = ROOT / "slides" / "noidungpp.docx"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))
    
    # Copy sang report/noidungpp.docx
    shutil.copy2(str(out_path), str(ROOT / "report" / "noidungpp.docx"))
    
    size_mb = out_path.stat().st_size / (1024 * 1024)
    print("\n=====================================================================")
    print(f" BIÊN DỊCH THÀNH CÔNG TÀI LIỆU KỊCH BẢN THUYẾT TRÌNH (20 SLIDES)!")
    print(f" Đường dẫn: {out_path}")
    print(f" Đã sao chép sang: {ROOT / 'report' / 'noidungpp.docx'}")
    print(f" Dung lượng file: {size_mb:.2f} MB ({out_path.stat().st_size:,} bytes)")
    print(f" Tổng số đoạn văn (Paragraphs): {len(doc.paragraphs)}")
    print(f" Tổng số bảng biểu (Tables): {len(doc.tables)}")
    print("=====================================================================")

if __name__ == "__main__":
    build_all_slides()
