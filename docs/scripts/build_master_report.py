"""
File điều phối chính: Biên dịch Báo cáo tổng kết hoàn chỉnh De_tai_17_Bao_cao_Tong_ket.docx
Tích hợp toàn bộ nội dung học thuật, công thức toán học, thuật toán, bảng số liệu,
nhật ký thực nghiệm, mã lệnh SQL/Cypher/ODL/OQL/JPQL và đầy đủ 15 sơ đồ/hình ảnh 300 DPI.
"""

from __future__ import annotations
import os, sys, shutil
from pathlib import Path
from docx import Document

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "docs" / "scripts"))

from report_builder.styles import setup_page_layout
from report_builder.ch0_preliminary import build_ch0
from report_builder.ch1_eer_spec import build_ch1
from report_builder.ch2_normalization import build_ch2
from report_builder.ch3_trees import build_ch3
from report_builder.ch4_sql_transactions import build_ch4
from report_builder.ch5_oo_neo4j import build_ch5
from report_builder.ch6_benchmark_pgbench import build_ch6
from report_builder.ch7_conclusion_clo7 import build_ch7
from render_diagrams import draw_eer_diagram, draw_oo_class_diagram

def main():
    print("=====================================================================")
    print(" BẮT ĐẦU BIÊN DỊCH BÁO CÁO TỔNG KẾT HOÀN CHỈNH CHO ĐỀ TÀI 17")
    print("=====================================================================")

    # 1. Kiểm tra và sinh sơ đồ hình vẽ nếu chưa có
    eer_img = ROOT / "docs" / "eer_diagram.png"
    oo_img = ROOT / "oo_model" / "class_diagram.png"
    if not eer_img.exists():
        draw_eer_diagram()
    if not oo_img.exists():
        draw_oo_class_diagram()

    # 2. Khởi tạo tài liệu Word
    doc = Document()
    setup_page_layout(doc)

    # 3. Biên dịch từng phân hệ chương mục
    print("-> Đang biên dịch Trang bìa, Lời cảm ơn, Mục lục & Lời mở đầu...")
    build_ch0(doc)

    print("-> Đang biên dịch Chương 1: Đặc tả nghiệp vụ & Thiết kế EER...")
    build_ch1(doc)

    print("-> Đang biên dịch Chương 2: Lý thuyết Phụ thuộc hàm & Chuẩn hóa 3NF/BCNF/Chase/4NF...")
    build_ch2(doc)

    print("-> Đang biên dịch Chương 3: 4 Mô hình Cây phân cấp (Adjacency, Path, Nested Set, Closure)...")
    build_ch3(doc)

    print("-> Đang biên dịch Chương 4: SQL Nâng cao, Đệ quy đồ thị R1-R4 & Giao dịch Deadlock T3...")
    build_ch4(doc)

    print("-> Đang biên dịch Chương 5: CSDL Hướng đối tượng (ODL/OQL/JPQL) & Đồ thị Neo4j/Cypher...")
    build_ch5(doc)

    print("-> Đang biên dịch Chương 6: Thiết kế vật lý, Benchmark 360 runs, pgbench & Ma trận cô lập...")
    build_ch6(doc)

    print("-> Đang biên dịch Kết luận & Phụ lục Báo cáo làm việc nhóm CLO7 (8 biên bản họp)...")
    build_ch7(doc)

    # 4. Lưu tài liệu Word
    out_docx = ROOT / "report" / "De_tai_17_Bao_cao_Tong_ket.docx"
    out_docx.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_docx))

    # 5. Thống kê và kiểm tra kết quả
    size_mb = out_docx.stat().st_size / (1024 * 1024)
    print("\n=====================================================================")
    print(f" BIÊN DỊCH THÀNH CÔNG BÁO CÁO TỔNG KẾT MASTER!")
    print(f" Đường dẫn: {out_docx}")
    print(f" Dung lượng file: {size_mb:.2f} MB ({out_docx.stat().st_size:,} bytes)")
    print(f" Tổng số đoạn văn (Paragraphs): {len(doc.paragraphs)}")
    print(f" Tổng số bảng biểu (Tables): {len(doc.tables)}")
    print("=====================================================================")

if __name__ == "__main__":
    main()
