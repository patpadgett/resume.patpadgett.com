---
version: 1
slug: "index-html"
primary_target: "index.html"
related_targets: ["Patrick_Padgett_Resume.pdf"]
---

# Surface brief: index.html (resume.patpadgett.com) and its PDF twin

Scope: the whole two-sheet resume, rendered as one HTML page (web), as the printed PDF, and mirrored as DOCX/TXT. Visitor mode: Persuade (a hiring manager or headhunter decides to call). Audience: recruiters and engineering managers reading on a laptop PDF viewer, in a browser, or on paper. Job: judge fit in six seconds, verify in two minutes, remember the candidate a day later. Action: call, email, or open LinkedIn/GitHub. Proof: the master's numbers ($2M, 250%, 50% MTTR, $50M/130 switches, 99.999% for 14 years, 194-star corkscrew). Constraints: 2 pages, master-only facts, headshot, clickable links, ATS text layer that contains nothing but the resume.

## Direction contract

THESIS: The resume is an engineering drawing of the candidate: a bond-white Letter sheet with a border, zone ticks, a title block and redlined figures. It refuses the category default (a name band, two weights, one accent colour, a sidebar of skill pills) and the designer default (Polaroid-style photo card with icons). Everything decorative is geometry; everything the ATS reads is resume text.

OWN-WORLD: Two inks on white bond: drafting black (#141414) and redline red (#C8102E), no third colour. Type is one family from the drawing standard itself, D-DIN (DIN 1451 lineage): D-DIN Exp Bold for the name, D-DIN caps tracked for labels and section titles, D-DIN regular for body, D-DIN Italic for sabbatical lines. Rules follow the ISO pen-weight ramp (0.18 / 0.35 / 0.7 mm): hairline leaders and zone ticks, section rules, heavy border and header rule. The headshot is a grayscale DETAIL A view in a pen-weight circle with a leader and label. Title block bottom-right with TITLE / SIZE A / REV / SHEET n OF 2 / DRAWN / DATE / SCALE NTS and a numbered NOTES block to its left. Chrome text (zone letters, DETAIL A, title block, notes) is drawn as glyph outlines in SVG, never as text. On screen the sheets rest on a pale sage drafting-board vinyl (Borco) with a soft offset shadow. With all content removed the page is still recognisably a drawing sheet.

STORY: The visitor sees a drawing sheet, reads a name lettered like a part title and a headline that names both halves of the career; the eye is pulled to the red figures ($2M, 250%, 50%, $50M) inside the first two sections, understands "senior telecom mediation engineer who also builds modern infrastructure, with numbers", and finds phone, email, LinkedIn and GitHub as red links at the top. The close reader turns to sheet 2 for the full chronology and the corkscrew proof. They remember "the one that looked like a blueprint" and the dollar figure.

FIRST VIEWPORT (sheet 1, top 45%): trim line, zone band and heavy border framing the sheet; top-left the name at 26pt D-DIN Exp Bold over the headline in bold, then two contact lines of red hairline-underlined links separated by CSS hairline bars; top-right the DETAIL A view (78pt circle, medium pen) with its caption centred beneath; a 2pt rule closes the header. Below: PROFESSIONAL SUMMARY (four lines; outcomes demoted to ink-bold so the achievements own the red) then KEY ACHIEVEMENTS (four bullets, outcomes red) then PROFESSIONAL EXPERIENCE opening with the current role. The primary action on the web is the sticky toolbar: Download PDF (ink-black) with Word (.docx) and Plain text beside it; the page closes with Email / Call / Download PDF. On paper the primary actions are the red links. Phones: one-row 44px toolbar (PDF / Word / Text), name beside a 96px portrait, headline and contact rows full width.

FORM: Engineering drawing sheet, candidate 5 of 7 on the grounded list (ordered: 1 offset press proof, 2 field notebook, 3 switch-room wiring schedule, 4 Unix man page, 5 engineering drawing sheet, 6 CDR billing statement, 7 punch card deck). Seed key 4bf155d2, assigned index 5, mode persuade. Challenger verdicts: star atlas declined (kept: dot-diameter hierarchy -> figure weight ramp); Rietveld declined (kept: primary colour rationed to what moves -> red only on figures and links); one-bit desktop declined (kept: whole-pixel crispness -> pen weights at exact device pixels); darkroom declined (kept: nothing); sleeping city declined (kept: nothing); ikebana competitive on audience calm (kept: charged empty margin around the detail view and between sections). Impeccable's pick, offset press proof, offered and not chosen. Canon offered and not chosen.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance.
