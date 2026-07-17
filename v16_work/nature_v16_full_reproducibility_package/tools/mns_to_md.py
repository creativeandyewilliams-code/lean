#!/usr/bin/env python3
"""Convert the .mns manuscript markup to Markdown (a faithful text projection).
Used to generate .md, and (via pandoc) .tex and .docx."""
import re, sys, html


def strip_tags(t):
    t = re.sub(r"</?i>", "*", t)
    t = re.sub(r"</?b>", "**", t)
    t = re.sub(r"<sub>(.*?)</sub>", r"_\1", t)
    t = re.sub(r"<super>(.*?)</super>", r"^\1", t)
    t = re.sub(r"<sup>(.*?)</sup>", r"^\1", t)
    t = t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    t = re.sub(r"&#x?[0-9a-fA-F]+;", lambda m: html.unescape(m.group(0)), t)
    return t


def convert(text, fig_prefix="../source_figures/"):
    out = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if ln.startswith("#TITLE "):
            out.append("# " + strip_tags(ln[7:].strip()))
        elif ln.startswith("#AUTHOR "):
            out.append("\n**" + strip_tags(ln[8:].strip()) + "**")
        elif ln.startswith("#META "):
            out.append("\n*" + strip_tags(ln[6:].strip()) + "*")
        elif ln.startswith("#H2 "):
            out.append("\n## " + strip_tags(ln[4:].strip()))
        elif ln.startswith("#H3 "):
            out.append("\n### " + strip_tags(ln[4:].strip()))
        elif ln.startswith("#EQ "):
            out.append("\n> " + strip_tags(ln[4:].strip()) + "\n")
        elif ln.startswith("#UL "):
            out.append("- " + strip_tags(ln[4:].strip()))
        elif ln.startswith("#OL "):
            out.append(strip_tags(ln[4:].strip()) + "  ")
        elif ln.startswith("#FIG "):
            out.append("\n*" + strip_tags(ln[5:].strip()) + "*\n")
        elif ln.startswith("#IMG "):
            spec = ln[5:].strip()
            path, _, cap = spec.partition("|")
            base = path.strip().split("/")[-1]
            out.append(f"\n![{strip_tags(cap.strip())}]({fig_prefix}{base})\n")
        elif s == "#HR":
            out.append("\n---\n")
        elif s in ("#SPACE",):
            out.append("")
        elif s == "#PAGEBREAK":
            out.append("\n")
        elif s == "#TABLE":
            i += 1
            rows = []
            while i < len(lines) and lines[i].strip() != "#ENDTABLE":
                if lines[i].startswith("#ROW "):
                    rows.append([strip_tags(c.strip()) for c in lines[i][5:].split("|")])
                i += 1
            if rows:
                ncol = max(len(r) for r in rows)
                rows = [r + [""] * (ncol - len(r)) for r in rows]
                out.append("\n| " + " | ".join(rows[0]) + " |")
                out.append("|" + "|".join(["---"] * ncol) + "|")
                for r in rows[1:]:
                    out.append("| " + " | ".join(r) + " |")
                out.append("")
        elif s == "":
            out.append("")
        else:
            out.append(strip_tags(s))
        i += 1
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    fig = sys.argv[3] if len(sys.argv) > 3 else "../source_figures/"
    open(dst, "w").write(convert(open(src, encoding="utf-8").read(), fig))
    print("wrote", dst)
