"""
Định nghĩa phong cách trình bày văn bản chuẩn học thuật cho Báo cáo Tổng kết Đồ án.
Trường Đại học Sài Gòn - Khoa Công nghệ Thông tin.
"""

from __future__ import annotations
import os, sys
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

ROOT = Path(__file__).resolve().parents[3]

# Bảng màu chuẩn học thuật đơn sắc (Đen - Trắng - Xám, không màu mè AI)
C_PRIMARY = RGBColor(0, 0, 0)        # Đen nguyên bản (Pure Black)
C_SECONDARY = RGBColor(0, 0, 0)      # Đen nguyên bản
C_MUTED = RGBColor(70, 70, 70)       # Xám ghi đậm trung tính cho Header/Footer
C_CODE = RGBColor(0, 0, 0)           # Đen nguyên bản
C_ACCENT = RGBColor(0, 0, 0)         # Đen nguyên bản
C_GREEN = RGBColor(0, 0, 0)

HEX_PRIMARY = "262626"               # Xám đen đậm / Than chì cho tiêu đề bảng
HEX_ZEBRA = "F9FAFB"                 # Xám rất nhạt xen kẽ dòng
HEX_BORDER = "CCCCCC"                # Đường kẻ viền xám trung tính
HEX_CALLOUT_BG = "F4F4F5"            # Nền hộp ghi chú xám nhạt
HEX_CALLOUT_BORDER = "71717A"        # Viền hộp ghi chú xám trung tính
HEX_CODE_BG = "F4F4F5"               # Nền khối mã xám nhạt

def setup_page_layout(doc: Document):
    """Cấu hình trang A4 và lề tiêu chuẩn đồ án tốt nghiệp đóng gáy (Top/Bottom 2.5cm, Left 3.0cm, Right 2.0cm)."""
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.0)
        
        # Header học thuật
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "ĐỒ ÁN CƠ SỞ DỮ LIỆU NÂNG CAO — ĐỀ TÀI 17: MẠNG XÃ HỘI HỌC TẬP"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.style.font.name = "Times New Roman"
        hp.style.font.size = Pt(8.5)
        hp.style.font.italic = True
        hp.style.font.color.rgb = C_MUTED
        
        # Footer học thuật có đánh số trang
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Trường Đại học Sài Gòn — Khoa CNTT  |  Trang "
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        fp.style.font.name = "Times New Roman"
        fp.style.font.size = Pt(9)
        fp.style.font.color.rgb = C_MUTED
        
        fld = OxmlElement('w:fldSimple')
        fld.set(qn('w:instr'), 'PAGE')
        fp._p.append(fld)

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

def add_heading_1(doc, text: str):
    h = doc.add_heading(level=1)
    r = h.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(15)
    r.bold = True
    r.font.color.rgb = C_PRIMARY
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    return h

def add_heading_2(doc, text: str):
    h = doc.add_heading(level=2)
    r = h.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = C_SECONDARY
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    return h

def add_heading_3(doc, text: str):
    h = doc.add_heading(level=3)
    r = h.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    r.font.italic = True
    r.font.color.rgb = C_MUTED
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(2)
    h.paragraph_format.keep_with_next = True
    return h

def add_paragraph(doc, text: str, bold_prefix: str = None, italic: bool = False, indent: float = 0):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.45
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(6)
    if indent > 0:
        p.paragraph_format.left_indent = Inches(indent)
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.bold = True
        
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.italic = italic
    return p

def add_bullet(doc, text: str, bold_prefix: str = None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.line_spacing = 1.40
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(5)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.bold = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    return p

def add_styled_table(doc, headers: list[str], data: list[list[str]], col_widths: list[float] = None):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Header Row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_shading(hdr_cells[i], HEX_PRIMARY)
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5)
            r.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

    # Data Rows
    for r_idx, row_data in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        bg_hex = HEX_ZEBRA if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            set_cell_shading(row_cells[c_idx], bg_hex)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            
            s_val = str(val).strip()
            if c_idx == 0 and len(headers) > 3 and not s_val.isdigit():
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            elif any(ch.isdigit() for ch in s_val) and len(s_val) < 15 and not ('\n' in s_val):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(10)
                r.font.color.rgb = RGBColor(0, 0, 0)

    if col_widths and len(col_widths) == len(headers):
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Inches(w)

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(2)
    p_after.paragraph_format.space_after = Pt(4)
    return table

def add_code_block(doc, code_str: str, caption: str = None):
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(6)
        p_cap.paragraph_format.space_after = Pt(2)
        r_cap = p_cap.add_run(f"Đoạn mã: {caption}")
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(10)
        r_cap.font.italic = True
        r_cap.bold = True
        r_cap.font.color.rgb = RGBColor(0, 0, 0)

    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.2)
    set_cell_shading(cell, HEX_CODE_BG)
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    
    cell.text = code_str.strip()
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(0)
    for r in p.runs:
        r.font.name = "Consolas"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_figure(doc, img_rel_path: str, caption: str, width_inches: float = 6.0):
    full_path = ROOT / img_rel_path
    if not full_path.exists():
        print(f"<!> CẢNH BÁO: Không tìm thấy ảnh {full_path}")
        return

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(3)
    p_img.paragraph_format.keep_with_next = True
    
    r_img = p_img.add_run()
    r_img.add_picture(str(full_path), width=Inches(width_inches))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(8)
    r_cap = p_cap.add_run(caption)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(10)
    r_cap.bold = True
    r_cap.font.italic = True
    r_cap.font.color.rgb = RGBColor(0, 0, 0)

def add_callout_box(doc, text: str, title: str = "ĐÁNH GIÁ & ĐÚC KẾT"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.2)
    set_cell_shading(cell, HEX_CALLOUT_BG)
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
    cell.text = ""
    p_t = cell.paragraphs[0]
    p_t.paragraph_format.space_after = Pt(2)
    r_t = p_t.add_run(f"★ {title.upper()}: ")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(10.5)
    r_t.bold = True
    r_t.font.color.rgb = RGBColor(0, 0, 0)

    r_b = p_t.add_run(text)
    r_b.font.name = "Times New Roman"
    r_b.font.size = Pt(10.5)
    r_b.font.italic = True
    r_b.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

