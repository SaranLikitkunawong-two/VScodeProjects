"""
Generate Verification Module Policies PDF
SC Partnering Pty Ltd (trading as Future Forward Planning)
Policies: PM-POL-002, PM-POL-003, PM-POL-004, PM-POL-005
"""

import re
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)

PAGE_WIDTH, PAGE_HEIGHT = A4

# --- Colour palette ---
NAVY       = colors.HexColor('#1B2A4A')
BLUE       = colors.HexColor('#2E6DA4')
LIGHT_GRAY = colors.HexColor('#F0F4FA')
ALT_ROW    = colors.HexColor('#EEF2F8')
MID_GRAY   = colors.HexColor('#CCCCCC')
DARK_GRAY  = colors.HexColor('#333333')
NOTE_BG    = colors.HexColor('#EEF4FB')
WHITE      = colors.white

CONTENT_W = PAGE_WIDTH - 3 * cm   # 1.5 cm margin each side


# ── Styles ────────────────────────────────────────────────────────────────────

def make_styles():
    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        'cover_title': S('cover_title', fontName='Helvetica-Bold', fontSize=26,
                         textColor=NAVY, alignment=TA_CENTER, leading=32, spaceAfter=10),
        'cover_sub':   S('cover_sub',   fontName='Helvetica', fontSize=13,
                         textColor=DARK_GRAY, alignment=TA_CENTER, leading=18, spaceAfter=6),
        'meta':        S('meta',        fontName='Helvetica', fontSize=10,
                         textColor=DARK_GRAY, leading=15, spaceBefore=2, spaceAfter=2),
        'policy_h1':   S('policy_h1',   fontName='Helvetica-Bold', fontSize=18,
                         textColor=NAVY, leading=24, spaceAfter=8),
        'h2':          S('h2',          fontName='Helvetica-Bold', fontSize=12,
                         textColor=NAVY, leading=17, spaceBefore=12, spaceAfter=5),
        'h3':          S('h3',          fontName='Helvetica-Bold', fontSize=10.5,
                         textColor=BLUE, leading=15, spaceBefore=8, spaceAfter=4),
        'body':        S('body',        fontName='Helvetica', fontSize=10,
                         textColor=DARK_GRAY, leading=14, spaceBefore=3, spaceAfter=3),
        'bullet':      S('bullet',      fontName='Helvetica', fontSize=10,
                         textColor=DARK_GRAY, leading=14, leftIndent=14,
                         spaceBefore=2, spaceAfter=2),
        'note':        S('note',        fontName='Helvetica-Oblique', fontSize=9.5,
                         textColor=colors.HexColor('#2c4a6e'), leading=14,
                         leftIndent=10, rightIndent=10, spaceBefore=6, spaceAfter=6,
                         borderWidth=1, borderColor=BLUE, borderPad=6, backColor=NOTE_BG),
        'th':          S('th',          fontName='Helvetica-Bold', fontSize=9,
                         textColor=WHITE, leading=12),
        'td':          S('td',          fontName='Helvetica', fontSize=9,
                         textColor=DARK_GRAY, leading=12),
        'td_bold':     S('td_bold',     fontName='Helvetica-Bold', fontSize=9,
                         textColor=DARK_GRAY, leading=12),
        'cover_label': S('cover_label', fontName='Helvetica-Bold', fontSize=10,
                         textColor=DARK_GRAY, leading=14),
        'cover_value': S('cover_value', fontName='Helvetica', fontSize=10,
                         textColor=DARK_GRAY, leading=14),
    }


# ── Header / footer callback ───────────────────────────────────────────────────

def page_decoration(canvas, doc):
    canvas.saveState()
    if doc.page == 1:
        canvas.restoreState()
        return

    # Header bar
    canvas.setFillColor(NAVY)
    canvas.rect(1.5*cm, PAGE_HEIGHT - 1.8*cm, CONTENT_W, 0.38*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(1.5*cm + 5, PAGE_HEIGHT - 1.63*cm,
                      'SC Partnering Pty Ltd  |  Future Forward Planning')
    canvas.setFont('Helvetica', 8)
    canvas.drawRightString(1.5*cm + CONTENT_W - 5, PAGE_HEIGHT - 1.63*cm,
                           'Verification Module Policies  |  v1.0  |  May 2026')

    # Footer
    canvas.setFillColor(MID_GRAY)
    canvas.rect(1.5*cm, 1.6*cm, CONTENT_W, 0.04*cm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.setFont('Helvetica', 8)
    canvas.drawString(1.5*cm, 1.15*cm, 'ABN 24 697 821 408')
    canvas.drawCentredString(PAGE_WIDTH / 2, 1.15*cm, f'Page {doc.page}')
    canvas.drawRightString(1.5*cm + CONTENT_W, 1.15*cm,
                           'CONFIDENTIAL — NDIS Submission Document')
    canvas.restoreState()


# ── Cover page ─────────────────────────────────────────────────────────────────

def cover_page(styles):
    el = []
    el.append(Spacer(1, 3.5*cm))

    # Top rule
    el.append(Table([['']], colWidths=[CONTENT_W], rowHeights=[0.55*cm],
                    style=TableStyle([('BACKGROUND', (0,0), (-1,-1), NAVY)])))
    el.append(Spacer(1, 0.6*cm))
    el.append(Paragraph('Verification Module Policies', styles['cover_title']))
    el.append(Spacer(1, 0.2*cm))
    el.append(Paragraph(
        'SC Partnering Pty Ltd<br/><b>trading as Future Forward Planning</b>',
        styles['cover_sub']))
    el.append(Spacer(1, 0.5*cm))
    el.append(Table([['']], colWidths=[CONTENT_W], rowHeights=[0.55*cm],
                    style=TableStyle([('BACKGROUND', (0,0), (-1,-1), NAVY)])))
    el.append(Spacer(1, 1.2*cm))

    # Policy index table
    rows = [
        ['Policy', 'Title', 'Practice Standard'],
        ['PM-POL-002', 'Incident Management Policy', '1.9'],
        ['PM-POL-003', 'Complaints and Feedback Management Policy', '1.10'],
        ['PM-POL-004', 'Risk Management Policy', '1.7'],
        ['PM-POL-005', 'Human Resources and Worker Screening Policy', '1.8'],
    ]
    tbl_data = []
    for r_idx, row in enumerate(rows):
        s = styles['th'] if r_idx == 0 else styles['td']
        tbl_data.append([Paragraph(c, s) for c in row])

    tbl = Table(tbl_data, colWidths=[3.2*cm, 10*cm, 3.3*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, ALT_ROW]),
        ('GRID', (0,0), (-1,-1), 0.5, MID_GRAY),
        ('LINEBELOW', (0,0), (-1,0), 1.5, NAVY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    el.append(tbl)
    el.append(Spacer(1, 1.5*cm))

    # Document details
    details = [
        ('Business:', 'SC Partnering Pty Ltd (trading as Future Forward Planning)'),
        ('ABN:', '24 697 821 408'),
        ('Version:', '1.0 — Initial Release'),
        ('Effective Date:', '15 May 2026'),
        ('Review Date:', '15 May 2027'),
        ('Approved By:', 'Saran Likitkunawong — Director'),
        ('Classification:', 'Confidential — NDIS Submission Document'),
    ]
    det_data = [[Paragraph(k, styles['cover_label']),
                 Paragraph(v, styles['cover_value'])] for k, v in details]
    det_tbl = Table(det_data, colWidths=[3.5*cm, 13*cm])
    det_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,-1), (-1,-1), 0.5, MID_GRAY),
    ]))
    el.append(det_tbl)
    el.append(PageBreak())
    return el


# ── Inline markdown → ReportLab XML ───────────────────────────────────────────

def inline(text):
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*([^*]+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.+?)`', r'<font name="Courier">\1</font>', text)
    return text


# ── Markdown table → ReportLab Table ──────────────────────────────────────────

def md_table(lines, styles):
    rows = []
    for line in lines:
        stripped = line.strip()
        if re.match(r'^\|[-:| ]+\|$', stripped):
            continue
        cells = [c.strip() for c in stripped.strip('|').split('|')]
        rows.append(cells)

    if not rows:
        return None

    col_count = max(len(r) for r in rows)
    col_w = CONTENT_W / col_count

    tbl_data = []
    for r_idx, row in enumerate(rows):
        s = styles['th'] if r_idx == 0 else styles['td']
        cells = [Paragraph(inline(c), s) for c in row]
        while len(cells) < col_count:
            cells.append(Paragraph('', s))
        tbl_data.append(cells)

    tbl = Table(tbl_data, colWidths=[col_w] * col_count, repeatRows=1)
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ('GRID', (0,0), (-1,-1), 0.5, MID_GRAY),
        ('LINEBELOW', (0,0), (-1,0), 1.2, NAVY),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    return tbl


# ── Markdown section → flowables ──────────────────────────────────────────────

META_PREFIXES = (
    '**Policy Number:**', '**Effective Date:**', '**Review Date:**',
    '**Owner:**', '**Version Control:**',
)

def parse_section(md_text, styles):
    el = []
    lines = md_text.split('\n')
    i = 0
    pending_bullets = []
    in_table = False
    table_buf = []

    def flush_bullets():
        for b in pending_bullets:
            el.append(Paragraph(f'• {b}', styles['bullet']))
        pending_bullets.clear()

    def flush_table():
        nonlocal in_table
        if table_buf:
            tbl = md_table(table_buf, styles)
            if tbl:
                el.append(Spacer(1, 4))
                el.append(tbl)
                el.append(Spacer(1, 6))
        table_buf.clear()
        in_table = False

    while i < len(lines):
        raw  = lines[i]
        s    = raw.strip()
        i   += 1

        # Table detection
        if s.startswith('|'):
            flush_bullets()
            in_table = True
            table_buf.append(s)
            continue
        if in_table:
            flush_table()

        # Skip blank / nbsp / separator lines
        if not s or s == '&nbsp;' or s == '---':
            flush_bullets()
            if el and not isinstance(el[-1], Spacer):
                el.append(Spacer(1, 4))
            continue

        # H1 policy title
        if s.startswith('# POLICY'):
            flush_bullets()
            el.append(Paragraph(inline(s.lstrip('# ')), styles['policy_h1']))
            el.append(HRFlowable(width='100%', thickness=2, color=NAVY, spaceAfter=8))
            continue

        # H2
        if s.startswith('## '):
            flush_bullets()
            el.append(Paragraph(inline(s[3:]), styles['h2']))
            continue

        # H3
        if s.startswith('### '):
            flush_bullets()
            el.append(Paragraph(inline(s[4:]), styles['h3']))
            continue

        # H4
        if s.startswith('#### '):
            flush_bullets()
            el.append(Paragraph(f'<b>{inline(s[5:])}</b>', styles['body']))
            continue

        # Metadata header lines
        if any(s.startswith(p) for p in META_PREFIXES):
            flush_bullets()
            el.append(Paragraph(inline(s), styles['meta']))
            continue

        # Blockquote / Note
        if s.startswith('> '):
            flush_bullets()
            el.append(Paragraph(inline(s[2:]), styles['note']))
            continue

        # Bullet
        if re.match(r'^[-*]\s', s):
            pending_bullets.append(inline(s[2:]))
            continue

        # Checkbox bullet
        if re.match(r'^- \[.?\]', s):
            checked = bool(re.match(r'^- \[[xX]\]', s))
            text = re.sub(r'^- \[.?\]\s*', '', s)
            mark = '☑' if checked else '☐'
            pending_bullets.append(f'{mark} {inline(text)}')
            continue

        # Numbered list
        if re.match(r'^\d+\.\s', s):
            flush_bullets()
            text = re.sub(r'^\d+\.\s+', '', s)
            el.append(Paragraph(f'    {inline(text)}', styles['bullet']))
            continue

        # Regular paragraph
        flush_bullets()
        el.append(Paragraph(inline(s), styles['body']))

    flush_bullets()
    if in_table:
        flush_table()

    return el


# ── Extract policies 2–5 from file ────────────────────────────────────────────

def extract_policies(filepath):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    policies = {}
    for n in [2, 3, 4, 5]:
        start = content.find(f'# POLICY {n}:')
        end   = content.find(f'# POLICY {n + 1}:')
        if start == -1:
            continue
        chunk = content[start: end if end != -1 else len(content)]
        chunk = re.sub(r'\n---\n---.*$', '', chunk.rstrip(), flags=re.DOTALL)
        policies[n] = chunk

    return policies


# ── Main ──────────────────────────────────────────────────────────────────────

def generate(output_path, suite_path):
    styles = make_styles()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
        topMargin=2.4*cm,  bottomMargin=2.2*cm,
        title='Verification Module Policies',
        author='SC Partnering Pty Ltd',
        subject='NDIS Verification Module — PM-POL-002, 003, 004, 005',
    )

    story = cover_page(styles)

    policies = extract_policies(suite_path)
    for n in [2, 3, 4, 5]:
        if n not in policies:
            print(f'WARNING: Policy {n} not found')
            continue
        story.extend(parse_section(policies[n], styles))
        if n < 5:
            story.append(PageBreak())

    doc.build(story, onFirstPage=page_decoration, onLaterPages=page_decoration)
    print(f'Done: {output_path}')


if __name__ == '__main__':
    base = r'C:\Users\Saran Likitkunawong\VScode\NDIS'
    generate(
        output_path=os.path.join(base, 'Verification Module Policies.pdf'),
        suite_path=os.path.join(base, 'Policy Suite - Draft Templates.md'),
    )
