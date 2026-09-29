---
name: Patrick Padgett — Engineering Drawing Sheet
description: Two inks on bond, with a semantic resume inside outlined drawing-sheet furniture.
colors:
  ink: "#141414"
  red: "#C8102E"
  paper: "#FFFFFF"
  board: "#C4CFC1"
  board-deep: "#A9B7A6"
typography:
  display:
    fontFamily: '"D-DIN Exp", "D-DIN", sans-serif'
    fontSize: "26pt"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0"
  headline:
    fontFamily: '"D-DIN", "DIN Alternate", "Bahnschrift", "Liberation Sans", Arial, sans-serif'
    fontSize: "9.6pt"
    fontWeight: 700
    lineHeight: "12pt"
  section:
    fontFamily: '"D-DIN", "DIN Alternate", "Bahnschrift", "Liberation Sans", Arial, sans-serif'
    fontSize: "8.6pt"
    fontWeight: 700
    lineHeight: "10pt"
    letterSpacing: "0"
  body:
    fontFamily: '"D-DIN", "DIN Alternate", "Bahnschrift", "Liberation Sans", Arial, sans-serif'
    fontSize: "9.4pt"
    fontWeight: 400
    lineHeight: "11.2pt"
  contact:
    fontFamily: '"D-DIN", "DIN Alternate", "Bahnschrift", "Liberation Sans", Arial, sans-serif'
    fontSize: "9pt"
    fontWeight: 400
    lineHeight: "12.5pt"
  title:
    fontFamily: '"D-DIN", "DIN Alternate", "Bahnschrift", "Liberation Sans", Arial, sans-serif'
    fontSize: "9.2pt"
    fontWeight: 700
    lineHeight: "11.2pt"
  label:
    fontFamily: '"D-DIN", sans-serif'
    fontSize: "11.5px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.1em"
  body-mobile:
    fontFamily: '"D-DIN", "DIN Alternate", "Bahnschrift", "Liberation Sans", Arial, sans-serif'
    fontSize: "15px"
    fontWeight: 400
    lineHeight: "22px"
  display-mobile:
    fontFamily: '"D-DIN Exp", "D-DIN", sans-serif'
    fontSize: "clamp(22px, 6.8vw, 34px)"
    fontWeight: 700
    lineHeight: 1
  section-mobile:
    fontFamily: '"D-DIN", "DIN Alternate", "Bahnschrift", "Liberation Sans", Arial, sans-serif'
    fontSize: "12px"
    fontWeight: 700
    lineHeight: "16px"
  title-mobile:
    fontFamily: '"D-DIN", "DIN Alternate", "Bahnschrift", "Liberation Sans", Arial, sans-serif'
    fontSize: "14px"
    fontWeight: 700
    lineHeight: "21px"
  contact-mobile:
    fontFamily: '"D-DIN", "DIN Alternate", "Bahnschrift", "Liberation Sans", Arial, sans-serif'
    fontSize: "14px"
    fontWeight: 400
    lineHeight: "21px"
  wordmark:
    fontFamily: '"D-DIN Exp", "D-DIN", sans-serif'
    fontSize: "13px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.06em"
  colophon:
    fontFamily: '"D-DIN", "DIN Alternate", "Bahnschrift", "Liberation Sans", Arial, sans-serif'
    fontSize: "12px"
    fontWeight: 400
    lineHeight: "18px"
  colophon-mobile:
    fontFamily: '"D-DIN", "DIN Alternate", "Bahnschrift", "Liberation Sans", Arial, sans-serif'
    fontSize: "13px"
    fontWeight: 400
    lineHeight: "20px"
spacing:
  sheet-pad-x: "0.6in"
  sheet-pad-top: "0.55in"
  sheet-pad-bottom: "0.35in"
  border-inset: "0.35in"
  section-before: "12pt"
  section-after: "5.5pt"
  header-rule-gap: "5pt"
  header-to-first-section: "9pt"
  section-rule-gap: "3pt"
  paragraph-after: "2.5pt"
  job-before: "7pt"
  action-gap: "8px"
components:
  button:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    padding: "8px 12px"
  button-hover:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.red}"
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    typography: "{typography.label}"
    padding: "8px 12px"
  button-primary-hover:
    backgroundColor: "{colors.red}"
    textColor: "{colors.paper}"
  sheet:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    width: "8.5in"
    height: "11in"
    padding: "0.55in 0.6in 0.35in"
  section-heading:
    textColor: "{colors.ink}"
    typography: "{typography.section}"
  figure:
    textColor: "{colors.red}"
  title-block:
    width: "282pt"
    height: "60pt"
  notes-block:
    width: "232pt"
    height: "60pt"
---

# Design System: Patrick Padgett — Engineering Drawing Sheet

## Overview

**Creative North Star: "The Engineering Drawing Sheet"**

A white paper sheet carries dense, single-column resume text inside drafting geometry. Black establishes structure and ordinary reading; red marks figures and links. The expanded name, circular grayscale detail view, zone band and ruled title block establish the drawing-sheet identity without turning the reading column into a diagram.

The screen adds a pale drafting board and soft paper shadows. Print removes that surrounding interface while retaining the sheet itself. Resume content stays semantic text; the peripheral drawing labels are SVG glyph outlines. This separation preserves the visual identity without injecting drawing metadata into the resume text layer.

**Key Characteristics:**
- Two inks on white paper; sage board outside the printable sheet.
- One DIN family, with expanded bold reserved for the name and identity furniture.
- Three drafting pen weights and square-edged sheet geometry.
- Semantic content separated from outlined drawing furniture.
- Fixed Letter sheets on wide screens and print; fluid reading on narrow screens.

Recorded from `styles.css`, `index.html` and the drawing generators in `build.py`. This describes the built HTML/print system, not the separate Calibri DOCX companion. The surface brief remains development context, not a normative token source.

## Colors

### Primary
- **Redline red** (`red`): hard figures, resume links, button hover and keyboard focus. Figures are also bold, so emphasis survives monochrome output.

### Neutral
- **Drafting black** (`ink`): reading text, sheet furniture, rules, primary button fill and ordinary button borders.
- **Bond white** (`paper`): sheet surface, ordinary buttons and reversed primary-button text.
- **Drafting-board vinyl** (`board`): screen background only. The toolbar mixes this color at 88% with transparency.
- **Board seam** (`board-deep`): the toolbar's 1px bottom border.

**The Two Inks Rule.** Keep the printable sheet to ink and red on paper; board colors belong to the surrounding screen interface.

Selection uses a red background with white text, not red text on white. Body links are red; colophon links are black at rest and red on hover. Do not interpret the accent rule as banning the implemented red interaction states.

## Typography

D-DIN is self-hosted from `assets/fonts/`: regular 400, bold 700 and italic 400; D-DIN Exp supplies expanded bold 700. `build.py` copies the accompanying OFL license. The exact fallback stacks and primary sizes are in the frontmatter. No monospace display face or icon font participates in the sheet.

### Hierarchy
- **Display:** uppercase name, expanded bold, line-height 1, no added tracking, 5pt bottom margin.
- **Headline / employer:** bold compact headline; employer headings use the same size and line-height, uppercase, with regular-weight mixed-case location text.
- **Section:** uppercase text authored in HTML, not CSS text transformation. Word-spacing is 0.18em, letter-spacing is zero. The heading has a medium (1pt) bottom rule, the section-before/after rhythm and section-rule-gap padding from the frontmatter.
- **Body:** regular text; bold skill labels and project names, italic sabbaticals. Paragraph spacing is compact rather than a loose editorial measure.
- **Role title:** bold with regular-weight dates at the same size.
- **Contact:** compact two-line contact block with live underlined links.
- **Toolbar label:** uppercase, declared weight 600. Only 400/700 normal font files are supplied, so 600 is a CSS request rather than a separately shipped face.
- **Peripheral glyphs:** zone letters/numbers are 6pt bold; title-block labels 4.8pt with 0.08em tracking, values normally 7.2pt bold; notes heading 6pt bold, note text 5.4pt with 6.6pt baseline steps. These tiny sizes belong only to outlined drawing furniture, never essential resume copy.

Ligatures are disabled (`font-variant-ligatures: none`; `"liga" 0, "dlig" 0, "kern" 1`). Numbers use red, weight 700 and `white-space: nowrap`; avoid splitting a figure across lines.

**The Two Layers Rule.** Keep essential resume content in semantic HTML reading order; render peripheral drawing labels through the existing D-DIN glyph-outline generator rather than adding selectable SVG text.

## Layout

### Sheet and page
- Wide-screen sheet: fixed US Letter, centered, flex column, with 32px between sheets. Its size and padding are frontmatter tokens. The board uses 36px 16px 12px padding.
- Outer trim: 0.16in from the paper edge; heavy inner border at the border-inset token. Four cells per edge, numbered 1–4 top/bottom and lettered A–D left/right. The zone SVG uses a 612 × 792 coordinate space.
- Content is one column. Header is a horizontal flex row with a 20pt gap; portrait sits to the right. The header closes with the heavy (2pt) pen rule, 5pt below the contact lines; the first section heading follows 9pt later. The growing body region has hidden overflow on fixed sheets, so added content requires real pagination checks, not just a fixed height.
- Footer is non-growing, bottom-aligned, with a 12pt gap and 8pt top margin. Its negative horizontal margins reach the border. Title block meets the bottom-right border; notes align to the body left inset. These are separate SVG objects, not a content table.
- Lists use disc markers, 11pt left padding, 1pt item padding and 1.8pt bottom margins. Skills remove bullets/left padding and use 3pt row spacing. Jobs use job-before spacing, with the first child exempted.

### Responsive behavior
- **At screen widths ≤900px:** sheets become auto-width/auto-height with 40px 28px 14px padding and 20px bottom margin. Board padding becomes 20px 10px 8px. The border becomes 2px, inset 14px; zones disappear. The body overflow becomes visible. Footer SVGs stack with a 10px gap and stretch to full width with proportional height.
- **At screen widths ≤700px:** body uses the mobile token. Toolbar name disappears, actions center, toolbar padding becomes 10px 12px. Header reverses into a column with a 14px gap; the detail view is 150px wide above the name. Name size becomes `clamp(22px, 6.8vw, 34px)`. Headline is 15px/20px, contact 14px/21px, employer 15px/21px and role title 14px. List-item bottom spacing becomes 4px; contact text may break long words.
- Mobile overrides are written at `.flow` specificity so they win: section headings 12px/16px with 22px above and 8px below, jobs 12px apart, sabbaticals 12px above, list items 4px apart, skills rows 6px apart. The notes SVG is inset 14px each side so it stays inside the 14px frame; the title block runs full width beneath it.

### Print
`@page` is US Letter with zero margins. Each fixed sheet becomes one page, with no sheet shadow or animation, no board padding and no toolbar/colophon. The last sheet does not force a trailing page. Responsive rules are screen-only; red links remain red in print.

A cover letter or one-page variant can reuse the sheet, text hierarchy and furniture, but must supply its own actual content pagination and title-block metadata. Two sheets describe this resume, not a universal requirement of the visual system.

## Elevation & Depth

Depth is limited to paper on a screen-only board. Sections within the sheet remain flat; their hierarchy comes from strokes, spacing and type, not nested cards or elevation.

### Shadow Vocabulary
- **Paper at rest:** `0 1px 2px rgba(20, 20, 20, 0.18), 0 22px 44px -18px rgba(20, 20, 20, 0.45)`.
- **Paper entering:** `0 1px 2px rgba(20,20,20,0.10), 0 34px 60px -18px rgba(20,20,20,0.55)`.
- **Toolbar:** `backdrop-filter: blur(6px)` over the translucent board mixture; no toolbar shadow.

**The Paper Depth Rule.** Apply depth to the sheet on its board, not to individual resume sections; remove sheet shadows in print.

Motion is a single `settle` entrance: translateY(8px) to 0 while the entering shadow becomes the rest shadow, over 520ms with `cubic-bezier(0.16, 1, 0.3, 1)` and fill-mode `both`. Sheet 2 delays 90ms. The entrance exists only under `prefers-reduced-motion: no-preference`. Button color, border-color and background-color transition over 140ms ease-out; those color transitions are not guarded by the reduced-motion query. There is no parallax or continuous animation.

## Shapes

Square-edged sheet, buttons and rectangular title-block cells; the portrait detail is the explicit circular exception. No general rounded-container scale is defined. The focus outline alone has a 1px radius.

### Drafting pen weights
| Token | Weight | Source comment / application |
| --- | --- | --- |
| `--hair` / `HAIR` | 0.5pt | ISO 0.18mm class: outer trim, zone ticks, internal title-block rules, notes rule, detail-caption underline and link underline. |
| `--med` / `MED` | 1pt | ISO 0.35mm class: section rules, title-block frame, portrait circle, hovered link underline. |
| `--heavy` / `HEAVY` | 2pt | ISO 0.7mm class: sheet border and the header-closing rule. |

The ISO labels are the code's nominal pen classes, not exact unit conversions. The sheet border changes to 2px on fluid screens. Ordinary button borders and the board seam use 1px rather than the print pen ramp.

## Components

### Download buttons
Compact, square-edged controls. The ordinary button is black text on paper; the primary PDF control reverses to white on black. Both use 8px 12px padding, 1px borders and the label token. Ordinary hover turns text/border red; primary hover turns fill/border red and retains white text. No distinct active state is implemented. Focus-visible is a 2px red outline, offset 2px, with a 1px radius.

### Sticky download bar
A flex row fixed by sticky positioning to top 0, z-index 5, with a 16px gap and 12px 20px padding. Identity is expanded bold 13px/1 with 0.06em tracking; its regular companion label uses 0.14em tracking and an 8px left margin. Actions wrap with 8px gaps. The actual bar contains PDF, Word and plain-text downloads, not a Print button.

### Section heading and reading column
A compact bold label followed by a medium-pen rule, not a filled banner. Keep paragraph and list text in the same reading column. The section-heading snippet represents the actual `.flow h2` rule, including its specificity outcome on mobile.

### Redlined figure and link
Figures add bold red emphasis without altering the text. What turns red is decided by one regex in `build.py` (`FIG`): money, percentages, multipliers, "tens of millions of dollars", and counts of things delivered or run (clients, switches, subscribers, plants, educators, stars, forks, servers, vendors, states). Calendar numbers, ages, dates and version numbers stay black. Short figures never wrap (`nowrap`); a figure of three or more words carries `.wrap`. Links use a hairline underline offset 2.6pt with `text-decoration-skip-ink: all`; hover thickens to the medium pen. These are distinct semantics: not every red number is a link.

### Title block and notes
Title block is a paper-filled frame with medium perimeter and hairline internal rules; horizontal dividers occur at y=22 and y=41 in its 282 × 60 coordinate space. Its top-row columns differ from the lower metadata columns. Notes occupy 232 × 60, with their horizontal rule at y=22 to match the title block. Note 2 reads "RED FIGURES ARE MEASURED RESULTS AND SCALE. RED UNDERLINED TEXT IS A LIVE LINK." so the two red semantics are distinguished on paper. Both are `aria-hidden` SVGs with glyph paths; use the generator to retain this distinction when adding another sheet type.

### Detail view
The grayscale headshot is clipped to a circle of 78pt diameter with a medium outline. The complete SVG is 82pt × 103pt, with outlined `DETAIL A` and `SCALE NTS` captions below it. The first caption is 7.4pt bold with 0.10em tracking, the second 5.4pt regular with the same tracking. The built device has a caption underline, not a leader connecting to another location. The SVG carries the accessible image label; its caption paths are not resume text.

### Colophon
Screen-only context below the sheets, maximum width matching Letter paper, 12px/18px type and 4px 0 40px padding. Phone type becomes 13px/20px. Links remain black until hover; this footer is not another printable sheet component.

## Do's and Don'ts

### Do:
- **Do** reuse the paper, border and three pen weights when extending the drawing-sheet family.
- **Do** retain bold as well as red emphasis for figures and underlines for links.
- **Do** keep essential content semantic and peripheral drawing labels as glyph outlines.
- **Do** verify pagination and clipping after changing fixed-sheet content.
- **Do** preserve the reduced-motion entrance guard and remove screen furniture in print.

### Don't:
- **Don't** put the sage board color or ambient sheet shadow into the printed page.
- **Don't** apply tiny title-block and notes lettering sizes to essential resume text.
- **Don't** turn single-column reading content into title-block-style tables or decorative text paths.
- **Don't** add a fourth pen weight or a third ink; the ramp is hair / med / heavy and the palette is ink / red on paper.
- **Don't** add a Print action or a portrait leader; the built device is a captioned detail view and the PDF is the print path.
