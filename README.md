# resume.patpadgett.com

Patrick Padgett's generic resume, drawn as an engineering drawing sheet. Live at https://resume.patpadgett.com (GitHub Pages, branch `main`, path `/`).

## What ships

| File | What it is |
|---|---|
| `index.html` | The resume as two fixed 8.5 x 11 in sheets on a drafting board. **Build output - do not hand-edit.** |
| `styles.css` | The world: two inks, D-DIN, ISO pen weights, print stylesheet. Hand-edited. |
| `Patrick_Padgett_Resume.pdf` | The same two sheets printed by Chromium from `index.html`. Real text, embedded fonts, 6 live links, headshot. |
| `Patrick_Padgett_Resume.docx` / `.txt` / `.md` | ATS twins generated from the same selection (Calibri, single column, no photo, KEYWORDS line). |
| `assets/headshot.jpg` | Patrick's headshot, grayscale for the two-ink sheet. Source: `career/resume/resume-ats/final-noc/assets/avatar@2x.jpg`. |
| `assets/fonts/` | D-DIN 400/700/Italic + D-DIN Exp 700 (woff2). SIL OFL 1.1, Datto Inc. Licence in `D-DIN-OFL.txt`. |
| `assets/og-card.jpg`, `icon.svg`, `icon-512.png`, `apple-touch-icon.png`, `favicon.ico` | Share card (composed 1200x630 from `.og.html`: name, headline, outcomes, DETAIL A) and the PP detail-circle mark. |
| `robots.txt`, `sitemap.xml`, `404.html`, `CNAME` | Pages plumbing. |
| `PRODUCT.md`, `DESIGN.md`, `.impeccable/` | Impeccable product truth, the recorded visual world, surface brief, review captures. |

## Source of truth and rebuild

The only content source is `/data/pat/career/resume/master/MASTER_RESUME.md`. `build.py` never rewrites a fact; it **selects** (which bullets, which skill terms, how many achievements) via the `PROFILE` dict at the top, and asserts that every skill term it prints exists in the master.

    cd /data/pat/2_PUBLISHED/resume.patpadgett.com
    env -u PYTHONPATH -u PYTHONHOME /data/pat/career/resume/resume-ats/.venv/bin/python build.py

The build:
1. parses the master with the resume system's own parser (`career/resume/build_from_master.py`),
2. writes assets, DOCX/TXT/MD,
3. writes a one-flow `index.html`, then `render.js` (Playwright) measures it and paginates into exactly two sheets with keep-with-next (a section header, job header or first bullet never ends a sheet),
4. rewrites `index.html` with the two sheets, checks for overflow, prints the PDF, captures `.impeccable/review/*.png` and the og card.

If the fit report says 3 pages, trim a selection in `PROFILE` (drop a bullet or a skill term). Do not shrink type below 9.4pt / 11.2pt.

Then the ATS gate (must print `compat score 100` for both files):

    env -u PYTHONPATH -u PYTHONHOME /data/pat/career/resume/resume-ats/.venv/bin/python tools/ats_bench.py

## ATS design

- Reading order in the text layer is a single column: name, headline, contact, PROFESSIONAL SUMMARY, KEY ACHIEVEMENTS, TECHNICAL SKILLS, PROFESSIONAL EXPERIENCE, PROJECTS, EDUCATION AND PROFESSIONAL DEVELOPMENT. No tables, text boxes, columns or icon fonts.
- Every drawing element (zone band, DETAIL A caption, NOTES, title block) is SVG **path outlines** generated from the font by `build.py`, so parsers never see "SHEET 1 OF 2" inside the resume.
- Section headers use `word-spacing`, not `letter-spacing`: tracked caps extract as `P R O F E S S I O N A L`, which fails header detection.
- ASCII only (plain hyphens, straight quotes); `ascii_check()` fails the build otherwise. Ligatures off.
- Contact block is body text, not a running header. Phone/email/LinkedIn/GitHub/site/corkscrew are real links in the PDF.
- Headshot is an image with alt text; no text is painted into it.

## Design notes

Direction (chosen by Patrick from the Impeccable direction round, seed 4bf155d2): the resume as an A-size engineering drawing. Two inks - drafting black `#141414`, redline red `#C8102E` for figures and links. One family, D-DIN (DIN 1451 lineage, the road-sign and drawing-standard face). Pen weights 0.5 / 1 / 2 pt map to ISO 0.18 / 0.35 / 0.7 mm. Detail view, general notes and title block follow ANSI Y14.1 sheet conventions; REV is the master's `Last updated` month, SHEET n OF 2 is computed. Full tokens in `DESIGN.md`.

Anti-reference (earlier Padgett resume builds, all different worlds): NOC page (Saira/Martian Mono), linkedin-site (Archivo/oxide red), hallmark (Space Grotesk/cobalt), work.patpadgett.com (IBM Plex Mono terminal).

## QA performed (2026-09-29)

- Two sheets, 0px overflow on both; PDF is 2 pages, ASCII text layer, D-DIN embedded, 6 URI links, 1 image, PDF title metadata set.
- ATS compat 100/100 for PDF and DOCX via `career/resume/ats_check.py`; keyword median 47% across 41 saved postings (generic version - tailored builds in `career/resume/tailored/` are for specific postings).
- Impeccable detector: 1 warning (13px toolbar wordmark tracking), classified as a label, not body text.
- Mobile 390 and 320: 0px horizontal overflow. Print emulation: 2 pages, toolbar and colophon hidden.
- Two vision inspection rounds fixed: header grouping, rule rhythm, zone band geometry from the border box, title block cell collision, notes alignment, figure splitting across lines.
- Finish review and documentation: see the commit message and `DESIGN.md`.
- Critique rounds (`.impeccable/critique/`): 23/32 -> 23/32 (round 2 widened to print, zoom, landscape, share card, keyboard, PDF pages, proofread); all five round-2 issues fixed in the following commit.

## Before this goes live (owner)

- Nothing blocking. Optional: Search Console property for resume.patpadgett.com and submit `sitemap.xml`.
