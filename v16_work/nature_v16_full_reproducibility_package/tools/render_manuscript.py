#!/usr/bin/env python3
"""Render a line-oriented manuscript markup file to PDF.

This is a self-contained builder used to regenerate the Nature Communications
v15 Article and Supplement PDFs from an editable text source. It exists because
the original manuscripts were only available as LibreOffice-produced PDFs with
no recoverable source; the v15 revision required editing their text, so the
content was transcribed into the `.mns` markup files rendered here.

Markup (line oriented):
  #TITLE text          document title
  #AUTHOR text         centred author line
  #META text           small centred metadata line
  #H2 text             section heading
  #H3 text             subsection heading (bold italic)
  #EQ markup           centred display equation
  #UL markup           bullet list item
  #OL markup           numbered / lettered list item (marker written in text)
  #FIG markup          figure caption block (small italic, boxed rule)
  #IMG path|caption    embedded image with caption
  #TABLE ... #ENDTABLE table; #ROW a|b|c rows (first #ROW is the header)
  #HR                  thin horizontal rule
  #SPACE               vertical gap
  #PAGEBREAK           page break
  (blank line)         paragraph break
  other text           body paragraph (consecutive lines are joined)

Inline markup inside text/equations uses reportlab mini-HTML: <i> <b> <sub>
<super> <font>. Math symbols are written as Unicode. Literal '&' is auto
escaped; '<'/'>' are reserved for tags, so comparisons use Unicode ≤ ≥ ≠.
"""
import re
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image, KeepTogether, PageBreak, CondPageBreak,
)
from reportlab.lib.styles import ParagraphStyle

FONT_DIR = "/usr/share/fonts/truetype/freefont/"
pdfmetrics.registerFont(TTFont("Serif", FONT_DIR + "FreeSerif.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", FONT_DIR + "FreeSerifBold.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Italic", FONT_DIR + "FreeSerifItalic.ttf"))
pdfmetrics.registerFont(TTFont("Serif-BoldItalic", FONT_DIR + "FreeSerifBoldItalic.ttf"))
pdfmetrics.registerFontFamily(
    "Serif", normal="Serif", bold="Serif-Bold",
    italic="Serif-Italic", boldItalic="Serif-BoldItalic",
)

STY = {}
STY["body"] = ParagraphStyle("body", fontName="Serif", fontSize=10, leading=14,
                             alignment=TA_JUSTIFY, spaceAfter=6)
STY["title"] = ParagraphStyle("title", fontName="Serif-Bold", fontSize=17,
                               leading=21, alignment=TA_LEFT, spaceAfter=8)
STY["author"] = ParagraphStyle("author", fontName="Serif", fontSize=11.5,
                                leading=15, alignment=TA_LEFT, spaceAfter=4)
STY["meta"] = ParagraphStyle("meta", fontName="Serif", fontSize=9,
                             leading=12, alignment=TA_LEFT, spaceAfter=3,
                             textColor=colors.HexColor("#333333"))
STY["h2"] = ParagraphStyle("h2", fontName="Serif-Bold", fontSize=13,
                           leading=16, spaceBefore=12, spaceAfter=5,
                           textColor=colors.HexColor("#111111"))
STY["h3"] = ParagraphStyle("h3", fontName="Serif-BoldItalic", fontSize=11,
                           leading=14, spaceBefore=8, spaceAfter=3)
STY["eq"] = ParagraphStyle("eq", fontName="Serif-Italic", fontSize=10.5,
                           leading=15, alignment=TA_CENTER,
                           spaceBefore=4, spaceAfter=6)
STY["ul"] = ParagraphStyle("ul", parent=STY["body"], leftIndent=16,
                           bulletIndent=4, spaceAfter=3)
STY["ol"] = ParagraphStyle("ol", parent=STY["body"], leftIndent=16,
                           spaceAfter=3)
STY["fig"] = ParagraphStyle("fig", fontName="Serif-Italic", fontSize=9,
                            leading=12, alignment=TA_LEFT, spaceAfter=4,
                            textColor=colors.HexColor("#222222"))
STY["cap"] = ParagraphStyle("cap", fontName="Serif", fontSize=8.5,
                            leading=11, alignment=TA_CENTER, spaceAfter=6,
                            textColor=colors.HexColor("#222222"))
STY["tbl"] = ParagraphStyle("tbl", fontName="Serif", fontSize=8.5, leading=11)
STY["tblh"] = ParagraphStyle("tblh", fontName="Serif-Bold", fontSize=8.5,
                             leading=11)

ENTITY = re.compile(r"&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)")


def esc(text):
    return ENTITY.sub("&amp;", text)


def make_para(text, style):
    return Paragraph(esc(text), style)


class Manuscript:
    def __init__(self, running_header):
        self.running_header = running_header
        self.story = []

    # -- header/footer -----------------------------------------------------
    def _decorate(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Serif", 8)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawString(2.0 * cm, A4[1] - 1.15 * cm, self.running_header)
        canvas.drawRightString(A4[0] - 2.0 * cm, 1.1 * cm, str(doc.page))
        canvas.setStrokeColor(colors.HexColor("#cccccc"))
        canvas.setLineWidth(0.4)
        canvas.line(2.0 * cm, A4[1] - 1.3 * cm, A4[0] - 2.0 * cm, A4[1] - 1.3 * cm)
        canvas.restoreState()

    def build(self, blocks, out_path):
        frame = Frame(2.0 * cm, 1.6 * cm, A4[0] - 4.0 * cm, A4[1] - 3.4 * cm,
                      id="main", leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0)
        doc = BaseDocTemplate(out_path, pagesize=A4,
                              title=self.title, author="Andy E. Williams")
        doc.addPageTemplates([PageTemplate(id="main", frames=[frame],
                                           onPage=self._decorate)])
        doc.build(self.parse(blocks))

    # -- parsing -----------------------------------------------------------
    title = ""

    def parse(self, text):
        story = []
        lines = text.split("\n")
        i = 0
        para_buf = []

        def flush():
            if para_buf:
                joined = " ".join(para_buf).strip()
                if joined:
                    story.append(make_para(joined, STY["body"]))
                para_buf.clear()

        while i < len(lines):
            raw = lines[i]
            line = raw.rstrip("\n")
            stripped = line.strip()
            if stripped == "":
                flush()
                i += 1
                continue
            if line.startswith("#TITLE "):
                flush(); self.title = line[7:].strip()
                story.append(make_para(line[7:].strip(), STY["title"]))
            elif line.startswith("#AUTHOR "):
                flush(); story.append(make_para(line[8:].strip(), STY["author"]))
            elif line.startswith("#META "):
                flush(); story.append(make_para(line[6:].strip(), STY["meta"]))
            elif line.startswith("#H2 "):
                flush(); story.append(CondPageBreak(2.4 * cm))
                story.append(make_para(line[4:].strip(), STY["h2"]))
            elif line.startswith("#H3 "):
                flush(); story.append(CondPageBreak(1.8 * cm))
                story.append(make_para(line[4:].strip(), STY["h3"]))
            elif line.startswith("#EQ "):
                flush(); story.append(make_para(line[4:].strip(), STY["eq"]))
            elif line.startswith("#UL "):
                flush()
                story.append(Paragraph(esc(line[4:].strip()), STY["ul"],
                                       bulletText="•"))
            elif line.startswith("#OL "):
                flush()
                story.append(make_para(line[4:].strip(), STY["ol"]))
            elif line.startswith("#FIG "):
                flush(); story.append(self._figbox(line[5:].strip()))
            elif line.startswith("#IMG "):
                flush(); story.append(self._img(line[5:].strip()))
            elif line.strip() == "#HR":
                flush()
                story.append(HRFlowable(width="100%", thickness=0.5,
                                        color=colors.HexColor("#bbbbbb"),
                                        spaceBefore=4, spaceAfter=6))
            elif line.strip() == "#SPACE":
                flush(); story.append(Spacer(1, 6))
            elif line.strip() == "#PAGEBREAK":
                flush(); story.append(PageBreak())
            elif line.strip() == "#TABLE":
                flush()
                j, tbl = self._table(lines, i)
                story.append(Spacer(1, 2)); story.append(tbl)
                story.append(Spacer(1, 6)); i = j; continue
            else:
                para_buf.append(stripped)
            i += 1
        flush()
        return story

    def _figbox(self, caption):
        para = make_para(caption, STY["fig"])
        t = Table([[para]], colWidths=[A4[0] - 4.0 * cm])
        t.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#bbbbbb")),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f6f6f6")),
        ]))
        return KeepTogether([Spacer(1, 2), t, Spacer(1, 4)])

    def _img(self, spec):
        path, _, caption = spec.partition("|")
        img = Image(path.strip())
        maxw = A4[0] - 4.0 * cm
        if img.imageWidth > maxw:
            ratio = maxw / img.imageWidth
            img.drawWidth = maxw
            img.drawHeight = img.imageHeight * ratio
        flow = [Spacer(1, 4), img]
        if caption.strip():
            flow.append(make_para(caption.strip(), STY["cap"]))
        flow.append(Spacer(1, 4))
        return KeepTogether(flow)

    def _table(self, lines, i):
        i += 1
        rows = []
        while i < len(lines) and lines[i].strip() != "#ENDTABLE":
            ln = lines[i]
            if ln.startswith("#ROW "):
                cells = ln[5:].split("|")
                rows.append(cells)
            i += 1
        i += 1  # skip #ENDTABLE
        ncol = max(len(r) for r in rows)
        data = []
        for ri, r in enumerate(rows):
            r = r + [""] * (ncol - len(r))
            style = STY["tblh"] if ri == 0 else STY["tbl"]
            data.append([Paragraph(esc(c.strip()), style) for c in r])
        avail = A4[0] - 4.0 * cm
        colw = [avail / ncol] * ncol
        t = Table(data, colWidths=colw, repeatRows=1)
        t.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "Serif"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LINEBELOW", (0, 0), (-1, 0), 0.7, colors.HexColor("#444444")),
            ("LINEABOVE", (0, 0), (-1, 0), 0.7, colors.HexColor("#444444")),
            ("LINEBELOW", (0, -1), (-1, -1), 0.7, colors.HexColor("#444444")),
            ("LINEBELOW", (0, 1), (-1, -2), 0.25, colors.HexColor("#dddddd")),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        return i, t


def main():
    src, out, header = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(src, encoding="utf-8") as fh:
        text = fh.read()
    m = Manuscript(header)
    m.build(text, out)
    print("wrote", out)


if __name__ == "__main__":
    main()
