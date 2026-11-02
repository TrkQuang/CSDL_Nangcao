"""Read-only regression check: python -I docs/scripts/check_report.py."""
from pathlib import Path
from xml.dom import minidom
import zipfile

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'report/De_tai_17_Bao_cao_Tong_ket.docx'


def check():
    with zipfile.ZipFile(REPORT) as archive:
        assert archive.testzip() is None
        doc = minidom.parseString(archive.read('word/document.xml'))
        text = ' '.join(n.firstChild.data for n in doc.getElementsByTagName('w:t') if n.firstChild)
        required = ['85.509', '13.381', '6.814', '4555.684127',
                    'SAVEPOINT', 'fn_search_posts_dynamic', 'TÀI LIỆU THAM KHẢO',
                    'gợi ý kết bạn', 'FD6: post_id', 'không hợp lệ']
        for value in required:
            assert value in text, f'Missing corrected content: {value}'
        assert 'PostgreSQL 18.6' not in text
        assert '0.039 ms' not in text
        assert 'hoàn thành 100% mục tiêu' not in text
        assert len(doc.getElementsByTagName('w:sectPr')) == 2
        assert len(doc.getElementsByTagName('w:drawing')) == 23
        assert len(doc.getElementsByTagName('w:tbl')) >= 105
        assert 'word/styles.xml' in archive.namelist()
        for name in archive.namelist():
            if name.endswith('.xml'):
                minidom.parseString(archive.read(name))
        assert 'SET lft = -lft, rgt = -rgt' not in text
        assert '2.490 ms' not in text
        contents = doc.getElementsByTagName('w:tbl')[0]
        pages = []
        for row in contents.getElementsByTagName('w:tr')[1:]:
            cell = row.getElementsByTagName('w:tc')[-1]
            pages.append(''.join(n.firstChild.data for n in cell.getElementsByTagName('w:t') if n.firstChild))
        assert len(pages) == 13 and all(page.isdecimal() for page in pages)
        assert list(map(int, pages)) == sorted(map(int, pages))
        assert 'fn_check_comment_post_closed' not in text
        assert 'fn_calculate_reputation_score' not in text
        assert 'proc_move_comment' in text
        assert 'An–Chi–Em' in text
        assert 'TỐI ƯU TUYỆT ĐỐI O(1)' not in text
        assert 'O(1) (ON DELETE CASCADE)' not in text
    print('PASS: corrected evidence, missing sections, package integrity and layout structure')


if __name__ == '__main__':
    check()
