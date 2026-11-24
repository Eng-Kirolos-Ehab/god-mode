---
name: "lecture-summary-pdf"
description: "Turn a lecture PDF or slides into one designed A4 study-summary PDF: mind maps, diagrams, exam traps and a question bank (MCQ + True/False) with an answer key. Use when the user uploads a lecture and asks for a summary, تلخيص, or exam questions."
---

# Lecture Summary PDF

Use when the user uploads a lecture (PDF/slides) and asks for a summary / تلخيص, especially with mind maps and questions. Output is ONE downloadable PDF built from HTML + Chromium (Playwright). Reply in the user's language. The summary content stays in the lecture's language unless the user asks otherwise.

## Ask first (one message, use the defaults if the user says "just do it")
- **Question bank size:** default 40 MCQ + 30 True/False. Fewer for short lectures?
- **Extra language box:** a short recap in the user's own language on the Exam Traps page? (default: yes if the user writes in a different language from the lecture)
- **Cover page:** default none, so the PDF starts with the master mind map.
- **Anything to skip:** for example the university's vision/mission pages (skipped by default).

## Content rules
- Read every page of the lecture (Read with `pages`, max 20 per call). Skip boilerplate pages such as the institution's vision and mission, unless the user wants them.
- Course aims / ILOs (if present) → two short boxes on page 1 under the master map.
- Cover EVERYTHING else in the lecture; summarize, don't drop topics. Solve any in-slide practice questions.
- Fix obvious slide mistakes in a red "Heads-up" box (e.g. wrong compound name, rounded angle), never silently.
- Questions: the agreed count (default 40 MCQ with 4 options A–D and one best answer, plus 30 True/False), all answerable from the lecture, mix of easy/tricky, no ambiguous options. Answer key: one-line reason per MCQ; every False statement gets its correction.

## Defaults that keep it clean (change only if the user asks)
- No cover page. The PDF starts with the master mind map page.
- No filler subtitle under the page-1 heading.
- No jokes or slang labels. Keep the tone of a study document.
- No "How to use the question bank" box.
- The optional recap box (if agreed) goes on the Exam Traps page, unlabeled, in the user's language, in the correct direction (RTL for Arabic) and an appropriate font.

## Document structure
1. `00 The whole lecture on one page` — radial SVG master mind map (dark center circle, 6 coloured branch pills, 3–4 leaf pills each, bezier connectors) + aims/ILOs boxes.
2. One part per major topic (`01`, `02`, …), each starting on a new page with a big magenta number + title + one-line subtitle, then a CSS org-chart mind map (root pill → 4 coloured branch cards), then content.
3. Content uses: comparison tables (dark header), definition boxes (violet), tip (teal), memory trick (amber), heads-up (red), inline SVG diagrams (shapes, energy diagrams, bar charts, skeletal structures, step flows), colour-coded chips for sequences.
4. `★ Exam Traps & Quick Revision` — table of ~12 traps (trap → correct idea) + unlabeled Arabic recap box.
5. `Q1 Multiple Choice — 40 Questions` (2-column cards, magenta number badge).
6. `Q2 True or False — 30 Statements` (teal badge, TRUE/FALSE pills).
7. `✓ Answer Key` — score boxes (__/40, __/30, __/70), then 2-column keys.

## Design system
- A4, `@page{size:A4;margin:14mm 13mm 16mm 13mm}`, footer via Playwright footerTemplate: course · lecture left, `pageNumber / totalPages` right, 7.5pt grey.
- Colours: ink #16182E, mute #6B6F88, line #E3E1EA, soft #F6F4FA, magenta #D6246E, teal #0E8A8C, amber #E08A00, violet #5B4BDB, red #C8323C.
- Fonts: Inter (system) body 10.4pt; headings Space Grotesk; formulas JetBrains Mono; Arabic Cairo. Install with `npm i @fontsource/cairo @fontsource/jetbrains-mono @fontsource/space-grotesk` and load via `@font-face` with `file://` woff2 URLs.
- `h3` has a small coloured square before it and `break-after:avoid`; tables, boxes, question cards `break-inside:avoid`. Only parts force a page break.
- Chemistry/subscripts via `<sub>`/`<sup>` in HTML.

### CSS mind map (org style)
```css
.mm .root{margin:0 auto;width:max-content;background:var(--ink);color:#fff;font-family:Grotesk;font-weight:700;padding:2.5mm 7mm;border-radius:99px;position:relative}
.mm .root::after{content:"";position:absolute;left:50%;bottom:-5mm;height:5mm;border-left:2px solid var(--ink)}
.mm .br{display:grid;gap:3mm;margin-top:5mm;position:relative;padding-top:5mm}
.mm .br::before{content:"";position:absolute;top:0;left:var(--l);right:var(--l);border-top:2px solid var(--ink)}
.mm .node{position:relative;display:flex;flex-direction:column}
.mm .node::before{content:"";position:absolute;left:50%;top:-5mm;height:5mm;border-left:2px solid var(--ink)}
.mm .node h5{color:#fff;padding:2mm 2.5mm;border-radius:2mm 2mm 0 0;text-align:center}
.mm .node ul{list-style:none;border:1.5px solid;border-top:none;border-radius:0 0 2mm 2mm;padding:2mm 2.5mm;font-size:8.6pt;background:#fff;flex:1}
```
Grid columns = number of branches; `--l: calc(100%/n/2 - 1mm)`. Never use `min-height:100%` on the lists (it overflows into the next heading).

### Render
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(f"file://{html_path}"); pg.wait_for_timeout(600)
    pg.pdf(path=out_pdf, format="A4", print_background=True, prefer_css_page_size=True,
           display_header_footer=True, header_template="<div></div>", footer_template=footer)
    b.close()
```

## Workflow
1. Read the whole lecture. 2. Write one Python generator (CSS + helpers `mindmap()`, `box()`, `table()`, SVG functions + content + question lists) that writes HTML and renders the PDF. 3. Rasterize with `pdftoppm -r 55` and view contact sheets; fix orphan headings, overflowing mind maps, near-empty pages (shrink SVG widths before adding page breaks). 4. Send the PDF with SendUserFile (display: attach). 5. Reply briefly in Egyptian Arabic: what's inside + any slide errors found. Keep the generator so follow-up edits are a quick re-render.