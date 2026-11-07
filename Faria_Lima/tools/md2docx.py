#!/usr/bin/env python3
"""Faria Lima 대본 .md → .docx 변환기.
사용법: python3 md2docx.py <입력.md> [출력.docx]
md 규칙:
  # Faria Lima — N부 M화
  ## 포르투갈어 제목 (한국어 제목)
  > - 키: 값   (머리 정보)
  ### 등장인물  →  - NOME — 설명
  ### 장면 제목 (한국어)
  NN. NOME: frase
      이름: 번역
  ## 다음 화 예고  → 본문
"""
import re, sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

NAVY, GRAY, DARK, MID, GOLD, TXT = (RGBColor(0x1F,0x38,0x64), RGBColor(0x80,0x80,0x80),
    RGBColor(0x40,0x40,0x40), RGBColor(0x59,0x59,0x59), RGBColor(0x7F,0x60,0x00), RGBColor(0x1A,0x1A,0x1A))

def run(p, text, size, bold=None, italic=None, color=None):
    r = p.add_run(text); r.font.size = Pt(size); r.bold = bold; r.italic = italic
    if color is not None: r.font.color.rgb = color
    r.font.name = 'Calibri'; r._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')
    return r

def para(doc, center=False, after=2):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(after)
    if center: p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return p

def main(src, dst):
    lines = open(src, encoding='utf-8').read().splitlines()
    head = lines[0].lstrip('# ').strip()
    m = re.match(r'(.+?)\s*\((.+)\)\s*$', lines[2].lstrip('# ').strip())
    pt_title, ko_title = (m.group(1), m.group(2)) if m else (lines[2].lstrip('# '), '')
    meta = {}
    for l in lines:
        mm = re.match(r'>\s*-\s*([^:]+):\s*(.+)', l)
        if mm: meta[mm.group(1).strip()] = mm.group(2).strip()
    doc = Document()
    s = doc.sections[0]; s.page_width, s.page_height = Cm(21), Cm(29.7)
    for side in ('left_margin','right_margin','top_margin','bottom_margin'): setattr(s, side, Cm(2.5))
    run(para(doc, True), 'FARIA LIMA', 15, True, color=GRAY)
    run(para(doc, True), '포르투갈어 낭독 교재', 13, color=GRAY)
    run(para(doc, True), head.replace('Faria Lima — ', '').replace(' ', ' · ', 1), 12, True, color=NAVY)
    run(para(doc, True), pt_title, 20, True, True, NAVY)
    run(para(doc, True), ko_title, 12, color=DARK)
    run(para(doc, True), meta.get('난이도 · 턴 수', ''), 9, color=MID)
    run(para(doc, True, 8), '지문 없이 대사만으로 구성 · 포르투갈어 본문 + 한국어 대역', 9, color=MID)
    i, mode, last = 0, None, None
    while i < len(lines):
        l = lines[i]
        if l.startswith('### '):
            title = l[4:].strip()
            if title == '등장인물':
                mode = 'cast'; run(para(doc, True), '등장인물', 10, True, color=NAVY)
            else:
                mode = 'script'; para(doc)
                p = para(doc, after=6); run(p, title, 12, True, color=NAVY)
        elif l.startswith('## 다음 화 예고'):
            mode = 'next'; para(doc); run(para(doc, after=4), '다음 화 예고', 12, True, color=NAVY)
        elif l.startswith('## ') or l.startswith('---'):
            if mode == 'cast': mode = None
        elif mode == 'cast' and l.startswith('- '):
            name, _, desc = l[2:].partition(' — ')
            p = para(doc, True, 0); run(p, name + '  ', 10, True); run(p, desc, 9, color=MID)
        elif mode == 'script':
            mm = re.match(r'\s*(\d+)\.\s*([^:]+):\s*(.+)', l)
            if mm and not l.startswith(' '):
                p = para(doc, after=0); run(p, mm.group(2), 10, True, color=GOLD); run(p, '   ' + mm.group(3), 11, color=TXT)
                last = 'pt'
            elif l.strip() and last == 'pt':
                ko = l.strip(); ko = ko.split(':', 1)[1].strip() if ':' in ko else ko
                run(para(doc, after=5), ko, 9, italic=True, color=GRAY); last = 'ko'
        elif mode == 'next' and l.strip():
            run(para(doc), l.strip(), 10, color=DARK)
        i += 1
    doc.save(dst)

if __name__ == '__main__':
    src = sys.argv[1]; main(src, sys.argv[2] if len(sys.argv) > 2 else re.sub(r'\.md$', '.docx', src))
