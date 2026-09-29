# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Confirmed by brief: flat static HTML/CSS published from this repo by GitHub Pages at https://resume.patpadgett.com (custom domain, HTTPS enforced, branch main, path /). No build framework, no CDN runtime; fonts self-hosted. The same HTML renders the web page and, through its print stylesheet, the PDF that ships beside it. Companion DOCX and TXT are generated from the same data so every format says the same thing.

## Users

Confirmed by brief: any hiring manager or headhunter (agency recruiter, in-house recruiter, engineering manager) who receives the resume by email, link, or job-portal upload. They read it on a laptop screen in a PDF viewer or browser, sometimes print it on US Letter, and skim for 6-30 seconds before deciding whether to read closely. Before any human sees it, an Applicant Tracking System parses it into fields and keyword-scores it.

Inferred (labelled): the roles they hire for are the ones the master resume targets: telecom billing mediation / revenue assurance, DevOps / infrastructure automation, senior Linux/SRE and IT operations. The document is generic on purpose: one version that lands with all of them.

## Product Purpose

A single "generic" resume for Patrick Padgett built from /data/pat/career/resume/master/MASTER_RESUME.md (the sole source of truth), delivered as a designed, printable, PDF-ready page with his headshot and clickable links, and as ATS-clean companion files. Success: a recruiter remembers him after one pass, a hiring manager finds the proof they need on page one, an ATS extracts every section and keyword in order, and the printed page looks as good as the screen.

## Positioning

The combination no neighbouring candidate can truthfully copy: 14 years as Sprint's highest-tier (Tier III) SME for wireless and wireline billing mediation (Nortel, Ericsson, Lucent AMA/CDR/EDR data) plus senior infrastructure automation at Jabil and Raymond James plus 25 years of production Linux, with hard numbers behind each: $2M saved a year, +250% mediation throughput, -50% alarm MTTR, a $50M 130-switch platform replacement, 99.999% uptime for 14 years, and corkscrew (2000-present) packaged in every major Linux distribution.

## Operating Context

- Content source of record: /data/pat/career/resume/master/MASTER_RESUME.md. Its BUILD GUIDE fixes length (2 pages, never 3), bullet counts per employer, title variants, the "always include" list ($2M / 250% / 50% MTTR trio, corkscrew with star count, LinkedIn + GitHub URLs) and the exclusions.
- Existing pipeline: /data/pat/career/resume/build_from_master.py produces role-tailored ATS PDF/DOCX/MD into tailored/; this product is the generic, designed sibling and must not contradict those files.
- Sister sites: patpadgett.com (hub), work.patpadgett.com (earlier resume site, IBM Plex Mono / VT323 terminal world), blog., music., octavitin., genx. Each build is a new world; the earlier resume worlds (Saira + Martian Mono NOC page at patpadgett.com/resume, Archivo/oxide-red linkedin-site, Space Grotesk/cobalt hallmark) are anti-reference.
- Readers arrive from email attachments, LinkedIn (linkedin.com/in/patpadgett), GitHub (github.com/patpadgett), job portals and cold outreach.

## Capabilities and Constraints

Confirmed by brief:
- Headshot on the resume (Patrick supplied it; source /data/pat/career/resume/resume-ats/final-noc/assets/avatar@2x.jpg, 640x640, colour, office background).
- Clickable links: email, phone, LinkedIn, GitHub, patpadgett.com, corkscrew repo.
- Printable and PDF-ready: US Letter, real text, embedded fonts, page breaks that never orphan a job header.
- 100% ATS-compliant: single-column reading order in the text layer, standard section headers (PROFESSIONAL SUMMARY, TECHNICAL SKILLS, PROFESSIONAL EXPERIENCE, PROJECTS, EDUCATION), no tables, text boxes, skill bars or icon fonts carrying meaning, plain hyphens and straight quotes, contact block in the body not a running header, ATS keyword line included, ligatures disabled, photo carries no text.
- Brief: two pages, the leaner end of the master's bullet counts; every metric verbatim from the master, nothing invented.
- Generic: no company or posting tailoring; the on-file headline "Telecom Billing Mediation Engineer | DevOps and Infrastructure Automation" names both halves.

Exclusions (master): Hindia / India Indonesia Travel Agency, soft-skill lists, "references available", street address, more than one summary, any number Patrick cannot defend in an interview.

Undecided: none material. (Inferred, labelled: the HTML page is a rendition of the resume itself rather than a landing page about it.)

## Brand Commitments

- Name: Patrick Padgett; handle patpadgett everywhere. Contact: pat@patpadgett.com, +1 816-601-5983, Greater Tampa Bay, FL, open to remote or hybrid.
- Voice: direct, concrete, verb-first bullets with the number in the first half of the line; dryly funny only where it costs nothing. Never salesy.
- Education is a Graphic Arts certificate (offset lithography, 2nd place Missouri VICA) - a real print-trade training that the document's craft may honour.
- No pinned palette or typeface. Negative constraint: visibly different from every earlier patpadgett resume/site build.

## Evidence on Hand

- All numbers, employers, dates, titles: MASTER_RESUME.md (confirmed by Patrick 2026-09-18 and 2026-09-28).
- Recommendations (Kathryn Walker, CNO Sprint; Renee Keffer, Director Network Operations Sprint; Jake Weaver, codesigned; Linux Magazine) - the master rules quotes off the resume except the one-line CNO commendation under the D3884 bullet.
- corkscrew: github.com/patpadgett/corkscrew, 194 stars, Debian/Ubuntu/Red Hat/CentOS/FreeBSD/Cygwin packages, Linux Magazine Issue 166 (2014), 2600, Wikipedia article.
- Headshot as above. No logos, no client names, no certifications (none held - do not invent).

## Product Principles

1. Proof before adjectives: every claim traces to the master; numbers do the persuading.
2. Two readers, one page order: the six-second skimmer lands on name, claim, numbers and contact; the close reader gets the full record in strict reverse chronology.
3. One source, every format: HTML, PDF, DOCX and TXT are generated from the same data and never drift from the master.
4. ATS is a hard gate, not a trade-off: no visual device may cost a single extracted word or scramble the reading order.
5. New world: this build is not a recolour of any earlier Padgett resume.

## Accessibility & Inclusion

Semantic single-h1 document, real text throughout, alt text on the headshot, contrast >= 4.5:1 for body text, keyboard-reachable links with visible focus, no reliance on colour alone for meaning (numbers are emphasised by weight as well as ink), prefers-reduced-motion honoured, prints legibly in black and white.
