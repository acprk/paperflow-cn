# -*- coding: utf-8 -*-
"""由 content.py（内容）+ journal_style.py（版式）生成投稿用 Word。

用法（在本目录下）：python build_docx.py [输出文件名.docx]
依赖：python-docx、Pillow
"""
import os
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Mm, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content as C          # noqa: E402
import journal_style as S    # noqa: E402

F = S.FONT
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'build', 'manuscript.docx')
ALIGN = {'center': WD_ALIGN_PARAGRAPH.CENTER, 'left': WD_ALIGN_PARAGRAPH.LEFT}


def setfont(run, east, size, bold=False, latin=None):
    latin = latin or F['body_latin']
    run.font.name = latin
    run.font.size = Pt(size)
    run.font.bold = bold
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.insert(0, rf)
    for k in ('w:ascii', 'w:hAnsi'):
        rf.set(qn(k), latin)
    rf.set(qn('w:eastAsia'), east)


def style_font(st, east, size, bold=False):
    st.font.name = F['body_latin']
    st.font.size = Pt(size)
    st.font.bold = bold
    rpr = st.element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.insert(0, rf)
    for k in ('w:ascii', 'w:hAnsi'):
        rf.set(qn(k), F['body_latin'])
    rf.set(qn('w:eastAsia'), east)
    for k in ('w:asciiTheme', 'w:hAnsiTheme', 'w:eastAsiaTheme'):
        if rf.get(qn(k)) is not None:
            del rf.attrib[qn(k)]
    st.font.color.rgb = RGBColor(0, 0, 0)


doc = Document()
s0 = doc.sections[0]
s0.page_width, s0.page_height = Mm(S.PAGE['width_mm']), Mm(S.PAGE['height_mm'])
s0.top_margin, s0.bottom_margin = Cm(S.PAGE['top_cm']), Cm(S.PAGE['bottom_cm'])
s0.left_margin, s0.right_margin = Cm(S.PAGE['left_cm']), Cm(S.PAGE['right_cm'])

N = doc.styles['Normal']
style_font(N, F['body_east'], F['body_pt'])
N.paragraph_format.line_spacing = F['line_spacing']
N.paragraph_format.space_before = N.paragraph_format.space_after = Pt(0)
N.paragraph_format.first_line_indent = Pt(F['first_indent_pt'])
N.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
for name, east, size, align, indent in [('Heading 1', F['h1_east'], F['h1_pt'], ALIGN[F['h1_align']], 0),
                                        ('Heading 2', F['h2_east'], F['h2_pt'], WD_ALIGN_PARAGRAPH.LEFT, F['h2_indent_pt'])]:
    st = doc.styles[name]
    style_font(st, east, size, bold=True)
    pf = st.paragraph_format
    pf.alignment = align
    pf.first_line_indent = Pt(indent)
    pf.space_before, pf.space_after = Pt(8), Pt(3)
    pf.line_spacing = F['line_spacing']
    pf.keep_with_next = True


def para(text='', east=None, size=None, bold=False, align=None, indent=True, space_after=0, line=None):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    if not indent:
        p.paragraph_format.first_line_indent = Pt(0)
    if space_after:
        p.paragraph_format.space_after = Pt(space_after)
    if line:
        p.paragraph_format.line_spacing = line
    if text:
        setfont(p.add_run(text), east or F['body_east'], size or F['body_pt'], bold)
    return p


def page_field(p, size):
    for kind, val in (('begin', None), ('instr', ' PAGE '), ('separate', None), ('text', '1'), ('end', None)):
        r = p.add_run()
        setfont(r, F['body_east'], size)
        if kind == 'instr':
            e = OxmlElement('w:instrText')
            e.set(qn('xml:space'), 'preserve')
            e.text = val
            r._element.append(e)
        elif kind == 'text':
            r.text = val
        else:
            e = OxmlElement('w:fldChar')
            e.set(qn('w:fldCharType'), kind)
            r._element.append(e)


def header_footer(sec, text):
    if S.HEADER_SHOWS_TITLE:
        h = sec.header.paragraphs[0]
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        h.paragraph_format.first_line_indent = Pt(0)
        setfont(h.add_run(text), F['header_east'], F['header_pt'])
    f = sec.footer.paragraphs[0]
    f.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f.paragraph_format.first_line_indent = Pt(0)
    page_field(f, F['header_pt'])


# ---------- 前置部分 ----------
para(C.TITLE, F['title_east'], F['title_pt'], True, WD_ALIGN_PARAGRAPH.CENTER, False, 3, line=1.3)
if C.SUBTITLE:
    para(C.SUBTITLE, F['author_east'], 14, False, WD_ALIGN_PARAGRAPH.CENTER, False, 6)
para(C.AUTHOR, F['author_east'], F['author_pt'], False, WD_ALIGN_PARAGRAPH.CENTER, False)
para(C.AFFIL, F['body_east'], 10.5, False, WD_ALIGN_PARAGRAPH.CENTER, False, 8)
p = para('', indent=False, line=1.3)
setfont(p.add_run(S.LABELS['abstract']), F['abstract_label_east'], F['abstract_pt'], True)
setfont(p.add_run(C.ABSTRACT), F['abstract_east'], F['abstract_pt'])
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p = para('', indent=False, line=1.3)
setfont(p.add_run(S.LABELS['keywords']), F['abstract_label_east'], F['abstract_pt'], True)
setfont(p.add_run(C.KEYWORDS), F['abstract_east'], F['abstract_pt'])
if C.CLC:
    para(C.CLC, F['body_east'], 10.5, indent=False, space_after=6, line=1.3)
if C.EN_TITLE:
    para(C.EN_TITLE, F['body_east'], 12, True, WD_ALIGN_PARAGRAPH.CENTER, False, 3, line=1.2)
    para(C.EN_AUTHOR, F['body_east'], 10.5, False, WD_ALIGN_PARAGRAPH.CENTER, False)
    para(C.EN_AFFIL, F['body_east'], 10.5, False, WD_ALIGN_PARAGRAPH.CENTER, False, 4)
    p = para('', indent=False, line=1.2)
    setfont(p.add_run('Abstract: '), F['body_east'], 10.5, True)
    setfont(p.add_run(C.EN_ABSTRACT), F['body_east'], 10.5)
    p = para('', indent=False, space_after=10, line=1.2)
    setfont(p.add_run('Key words: '), F['body_east'], 10.5, True)
    setfont(p.add_run(C.EN_KEYWORDS), F['body_east'], 10.5)
else:
    para('', indent=False, line=1.0)
header_footer(s0, C.TITLE)

TEXT_W_CM = S.PAGE['width_mm'] / 10 - S.PAGE['left_cm'] - S.PAGE['right_cm']


def caption(text, where):
    align = WD_ALIGN_PARAGRAPH.LEFT if where.endswith('left') else WD_ALIGN_PARAGRAPH.CENTER
    c = para(text, F['caption_east'], F['caption_pt'], False, align, False, 3)
    c.paragraph_format.space_before = Pt(6)
    if where.startswith('above'):
        c.paragraph_format.keep_with_next = True
    return c


def three_line_table(key):
    cap, head, rows, w = C.TABLES[key]
    if S.CAPTION['table'].startswith('above'):
        caption(cap, S.CAPTION['table'])
    t = doc.add_table(rows=1 + len(rows), cols=len(head))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    total = Cm(TEXT_W_CM)
    for gc, x in zip(t._tbl.tblGrid.findall(qn('w:gridCol')), w):
        gc.set(qn('w:w'), str(int(total * x / 635)))
    borders = OxmlElement('w:tblBorders')
    for side, sz in (('top', '12'), ('bottom', '12')):
        e = OxmlElement('w:' + side)
        e.set(qn('w:val'), 'single')
        e.set(qn('w:sz'), sz)
        e.set(qn('w:color'), '000000')
        borders.append(e)
    for side in ('left', 'right', 'insideH', 'insideV'):
        e = OxmlElement('w:' + side)
        e.set(qn('w:val'), 'nil')
        borders.append(e)
    t._tbl.tblPr.append(borders)
    for ri, row in enumerate([head] + rows):
        for ci, txt in enumerate(row):
            cell = t.cell(ri, ci)
            cell.width = int(total * w[ci])
            cp = cell.paragraphs[0]
            cp.paragraph_format.first_line_indent = Pt(0)
            cp.paragraph_format.line_spacing = 1.2
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            setfont(cp.add_run(txt), F['caption_east'] if ri == 0 else F['body_east'], F['table_pt'], ri == 0)
            if ri == 0:
                tcPr = cell._tc.get_or_add_tcPr()
                tb = OxmlElement('w:tcBorders')
                b = OxmlElement('w:bottom')
                b.set(qn('w:val'), 'single')
                b.set(qn('w:sz'), '6')
                b.set(qn('w:color'), '000000')
                tb.append(b)
                tcPr.append(tb)
    if not S.CAPTION['table'].startswith('above'):
        caption(cap, S.CAPTION['table'])
    para('', indent=False, line=1.0)


def figure(key):
    from PIL import Image
    path, cap = C.FIGS[key]
    where = S.CAPTION['score'] if key in C.SCORE_KEYS else S.CAPTION['figure']
    if where.startswith('above'):
        caption(cap, where)
    p = para('', align=WD_ALIGN_PARAGRAPH.CENTER, indent=False, line=1.0)
    im = Image.open(path)
    wcm = min(TEXT_W_CM, im.size[0] / 300 * 2.54)
    p.add_run().add_picture(path, width=Cm(wcm))
    if not where.startswith('above'):
        caption(cap, where)


for b in C.B:
    kind = b[0]
    if kind == 'h1':
        doc.add_paragraph(b[1], style='Heading 1')
    elif kind == 'h2':
        doc.add_paragraph(b[1], style='Heading 2')
    elif kind == 'p':
        para(b[1])
    elif kind == 'fig':
        figure(b[1])
    elif kind == 'table':
        three_line_table(b[1])

doc.add_paragraph(S.LABELS['refs_heading'], style='Heading 1')
for r in C.REFS:
    p = para(r, F['body_east'], F['ref_pt'], indent=False, line=1.25)
    p.paragraph_format.left_indent = Pt(26)
    p.paragraph_format.first_line_indent = Pt(-26)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
if C.FUND:
    para(C.FUND, F['body_east'], F['ref_pt'], indent=False)
para(C.AUTHOR_BIO, F['body_east'], F['ref_pt'], indent=False)

os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
doc.save(OUT)
print('saved', OUT, '| 正文段落字符', C.BODY_CHARS, '| 注释', len(C.REFS), '| 未引用文献', C.UNUSED)
