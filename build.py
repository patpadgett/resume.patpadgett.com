#!/usr/bin/env python
"""Build resume.patpadgett.com from /data/pat/career/resume/master/MASTER_RESUME.md.

    build.py            -> index.html, styles.css, assets/, PDF, DOCX, TXT, MD, og card, icons, sitemap
    build.py --no-pdf   -> HTML/CSS/assets only (skip the Playwright pagination + PDF pass)

The master is the single source of truth. This script only SELECTS and ORDERS; it never
rewrites a fact. Selection lives in PROFILE below (bullet counts, skill rows, sentence trims).
Design decisions live in DESIGN.md; the direction contract in .impeccable/surfaces/index-html.md.
"""
import datetime, importlib.util, json, os, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MASTER = Path("/data/pat/career/resume/master/MASTER_RESUME.md")
FONT_SRC = Path("/data/pat/.hermes/cache/scratch/fonts/ddin")           # D-DIN (OFL 1.1) as downloaded
HEADSHOT_SRC = Path("/data/pat/career/resume/resume-ats/final-noc/assets/avatar@2x.jpg")
SITE = "https://resume.patpadgett.com"
PDF_NAME = "Patrick_Padgett_Resume.pdf"
INK, RED, PAPER = "#141414", "#C8102E", "#FFFFFF"

# ------------------------------------------------------------------ master parser (shared with the ATS pipeline)
spec = importlib.util.spec_from_file_location("bfm", "/data/pat/career/resume/build_from_master.py")
bfm = importlib.util.module_from_spec(spec); spec.loader.exec_module(bfm)

# ------------------------------------------------------------------ generic profile: what this ONE resume shows
PROFILE = dict(
    headline="Telecom Billing Mediation Engineer | DevOps and Infrastructure Automation",
    summary="primary",
    # KEY ACHIEVEMENTS: substrings of master achievement bullets, in display order (the signature trio + the $50M program)
    achievements=["Saved $2 million", "throughput 250%", "mean-time-to-resolution 50%", "$50M replacement"],
    # TECHNICAL SKILLS: master category label -> a SUBSET of that category's master list (selection, never invention)
    skills=[
        ("Telecom billing / mediation", "billing mediation, revenue assurance, CDR/EDR/AMA usage-record pipelines, rating and charging, Nortel / Ericsson / Lucent switch data formats, BSS/OSS, mediation rules, data reconciliation, Tier III production support, root cause analysis, ETL, Oracle SQL"),
        ("Unix / Linux / OS", "RHEL, CentOS, Debian, Ubuntu, HP-UX, Solaris, FreeBSD, Red Hat Satellite, Windows Server"),
        ("IaC & configuration management", "Terraform, Ansible (playbooks, roles, YAML, Jinja2), CloudFormation, Puppet, Chef"),
        ("CI/CD & version control", "Azure DevOps, GitHub Actions, GitLab CI/CD, Jenkins, Octopus Deploy, Git, pull-request code review and branching/tagging strategy; canary / A-B / blue-green deployment"),
        ("Cloud, containers & virtualization", "AWS (EC2, S3, RDS, VPC), Microsoft Azure (VMs, Storage, Virtual Networking, Azure DevOps), Google Cloud Platform, hybrid cloud, Docker, Kubernetes, microservices, KVM, VMware ESX/vCenter/Horizon"),
        ("Monitoring & observability", "ELK Stack (Elasticsearch, Logstash, Kibana), Splunk, Dynatrace, Prometheus, Grafana, centralized logging, alerting and dashboards, SLOs/SLIs, on-call incident response, postmortems and root cause analysis (RCA), SRE practices"),
        ("Programming & scripting", "Python, Perl, PHP, Ruby, C / C++ / C#, Java, JavaScript / TypeScript, SQL, bash / ksh / zsh, PowerShell; Ruby on Rails, Django, .NET Core, REST API design; Oracle, MySQL, PostgreSQL"),
        ("Operations & ITSM", "on-call and Tier 2/3 escalation, troubleshooting, release and change management, capacity planning, backup and disaster recovery, SOPs and runbooks, vendor management, ITIL, SDLC (Agile, Scrum, Waterfall), Jira Service Management, Confluence"),
    ],
    # experience bullets: substrings of master bullets, in display order (signature metrics live in KEY ACHIEVEMENTS, not repeated)
    bullets={
        "VIMOPS": ["Founded and run", "Cut client deployment times 70%", "legacy monolith"],
        "JABIL": ["Azure DevOps and Octopus Deploy with automated", "Kubernetes across approx. 112", "Ansible playbook library"],
        "RAYMOND": ["Anchored Linux SME", "Ansible playbooks and Jenkins"],
        "CODESIGNED": ["Drove 30% growth"],
        "SPRINT": ["Anchored Tier III", "Ran the Unix/Linux mediation pipelines", "Recovered tens of millions", "Sustained 99.999% uptime"],
        "CYBERRAZOR": [],
        "VARIOUS": [],
    },
    one_liners={  # employers rendered as a single line (no bullets); facts verbatim from the master
        "CYBERRAZOR": "Built Fasttrack, a Ruby on Rails celeration-charting web app for behavior analysts at schools serving students with autism; trained 30+ educators, improving student progress tracking 20%.",
        "VARIOUS": "Ran Unix systems and networks serving 3,000 subscribers for six dial-up-era ISPs; shipped first commercial software at 13.",
    },
    sabbaticals={  # one line each (master BUILD GUIDE: "1 line each")
        "May 2019 - Feb 2020": "Sabbatical, international travel (Indonesia, Malaysia, Vietnam, Cambodia; conversational Bahasa Indonesia) | May 2019 - Feb 2020",
        "May 2017 - Mar 2018": "Sabbatical, U.S. travel and independent study of DevOps practices and Infrastructure as Code | May 2017 - Mar 2018",
    },
    corkscrew_sentences=2,
)

def select(R):
    T = {"name": R["contact"]["Name"], "headline": PROFILE["headline"], "contact": R["contact"],
         "summary": R["summaries"][PROFILE["summary"]]}
    T["achievements"] = [next(a for a in R["achievements"] if s in a) for s in PROFILE["achievements"]]
    # every listed skill must exist in the master's category lists (merged "Cloud, containers & virtualization" draws on two)
    master_terms = {t.strip().lower() for _, v in R["skills"] for t in re.split(r",|;", v)}
    master_blob = " ".join(v.lower() for _, v in R["skills"])
    for k, v in PROFILE["skills"]:
        for term in re.split(r",|;", v):
            t = term.strip().lower()
            assert t in master_terms or t in master_blob, f"skill term not in master: {term!r}"
    T["skills"] = PROFILE["skills"]
    exp = []
    for j in R["experience"]:
        key = j["org"].split()[0]
        if key == "Personal":
            continue
        picks = PROFILE["bullets"].get(key, [])
        bullets = [next(b for b in j["bullets"] if s in b) for s in picks]
        exp.append({**j, "bullets": bullets, "line": PROFILE["one_liners"].get(key)})
    T["experience"] = exp
    T["sabbaticals"] = PROFILE["sabbaticals"]
    ck = next(p for p in R["projects"] if p["name"] == "corkscrew")
    sents = re.split(r"(?<=\.) ", ck["desc"])
    desc = " ".join(sents[:PROFILE["corkscrew_sentences"]])
    T["project"] = {"head": ck["head"], "desc": desc}
    T["education"] = R["education"]
    T["profdev"] = [d if d.endswith(".") else d + "." for d in R["profdev"][:1]]
    T["ats_line"] = R["ats_line"]
    m = re.search(r"Last updated: (\d{4}-\d{2}-\d{2})", MASTER.read_text()); T["rev"] = m.group(1) if m else datetime.date.today().isoformat()
    T["date"] = datetime.date.today().isoformat()
    # REV letter: A for the first shipped master month (2026-09), then B, C... per later master month
    y, mth = int(T["rev"][:4]), int(T["rev"][5:7]); T["rev_letter"] = chr(ord("A") + max(0, (y - 2026) * 12 + (mth - 9)))
    return T

# ------------------------------------------------------------------ text helpers
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

UNITS = r"(?:client organizations|enterprise clients|clients|switches|subscribers|educators|GitHub stars|forks|servers|states|vendors|manufacturing plants|plants)"
# Tier 1 (red): outcomes - money, percentages, multipliers, recovered revenue, uptime.
OUTCOME = re.compile(r"(\$\d[\d,.]*(?:M\b|\s?(?:million|billion))?(?:\s?annually)?|\b\d[\d,.]*\s?%|\b\d+x\b|tens of millions of dollars|about \d+ minutes/year)")
# Tier 2 (black bold): scale and tenure - counts of things run or delivered, years.
SCALE = re.compile(r"(\bapprox\. \d[\d,]* " + UNITS + r"|\b\d[\d,]*\+? " + UNITS + r"|\b\d[\d,]*-(?:switch|vendor|server|state)\b|\b\d+\+? years\b)")
FIG = re.compile("(" + OUTCOME.pattern[1:-1] + "|" + SCALE.pattern[1:-1] + ")")
def redline(s, demote=()):
    """Mark figures: outcomes -> <b class=fig> (red), scale/tenure -> <b class=num> (black bold).
    `demote`: outcome strings that should render as tier 2 here (e.g. the summary's repeats of KEY ACHIEVEMENTS)."""
    out, i = [], 0
    for m in FIG.finditer(s):
        g = m.group(0)
        tier1 = bool(OUTCOME.fullmatch(g)) and not any(d in g for d in demote)
        cls = "fig" if tier1 else "num"
        if g.count(" ") > 1: cls += " wrap"
        out.append(esc(s[i:m.start()])); out.append(f'<b class="{cls}">{esc(g)}</b>'); i = m.end()
    out.append(esc(s[i:])); return "".join(out)

def ascii_check(t):
    bad = sorted({c for c in t if ord(c) > 127}); assert not bad, f"non-ASCII in output: {bad}"

# ------------------------------------------------------------------ glyphs -> SVG paths (chrome text is never text)
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
_FONTS = {}
def font(name):
    if name not in _FONTS: _FONTS[name] = TTFont(FONT_SRC / f"{name}.ttf")
    return _FONTS[name]

def text_path(s, size, fontname="D-DIN", tracking=0.0):
    """Return (svg path d, advance width) for string s at size pt, baseline at y=0, x from 0."""
    f = font(fontname); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upem = f["head"].unitsPerEm; k = size / upem
    pen = SVGPathPen(gs); x = 0.0
    for ch in s:
        g = cmap.get(ord(ch), cmap.get(ord("?")))
        tp = TransformPen(pen, (k, 0, 0, -k, x, 0)); gs[g].draw(tp)
        x += gs[g].width * k + tracking * size
    d = re.sub(r"(\d+\.\d{2})\d+", r"\1", pen.getCommands())
    return d, x

def svg_text(s, x, y, size, fontname="D-DIN", tracking=0.0, anchor="start", fill=INK, cls=""):
    d, w = text_path(s, size, fontname, tracking)
    if anchor == "end": x -= w
    elif anchor == "middle": x -= w / 2
    c = f' class="{cls}"' if cls else ""
    return f'<path{c} fill="{fill}" transform="translate({x:.2f} {y:.2f})" d="{d}"/>'

# ------------------------------------------------------------------ sheet chrome (border, zone ticks, title block, notes, detail)
PT = 72.0                     # 1in in pt
W, H = 8.5 * PT, 11 * PT      # 612 x 792
BORDER = 0.35 * PT            # border inset from the paper edge
PAD = 0.62 * PT               # content inset from the paper edge
HAIR, MED, HEAVY = 0.5, 1.0, 2.0   # pen weights in pt (ISO 0.18 / 0.35 / 0.7 mm)

TRIM = 0.16 * PT              # outer trim line; the zone band lies between TRIM and BORDER
def zone_strips():
    """Zone band between the trim line and the border, divided into 4 cells per edge, numbered/lettered from the border box."""
    cols, rows = 4, 4; size = 6.0; cap = size * 0.72
    iw, ih = W - 2 * BORDER, H - 2 * BORDER
    def glyph(ch, x, y):
        d, w = text_path(ch, size, "D-DIN-Bold")
        return f'<path fill="{INK}" transform="translate({x - w/2:.2f} {y:.2f})" d="{d}"/>'
    mid = (TRIM + BORDER) / 2
    L = [f'<rect x="{TRIM}" y="{TRIM}" width="{W - 2*TRIM}" height="{H - 2*TRIM}" fill="none" stroke="{INK}" stroke-width="{HAIR}"/>']
    for i in range(1, cols):
        x = BORDER + i * iw / cols
        L.append(f'<line x1="{x:.2f}" x2="{x:.2f}" y1="{TRIM}" y2="{BORDER}"/><line x1="{x:.2f}" x2="{x:.2f}" y1="{H - BORDER}" y2="{H - TRIM}"/>')
    for i in range(1, rows):
        y = BORDER + i * ih / rows
        L.append(f'<line y1="{y:.2f}" y2="{y:.2f}" x1="{TRIM}" x2="{BORDER}"/><line y1="{y:.2f}" y2="{y:.2f}" x1="{W - BORDER}" x2="{W - TRIM}"/>')
    for i in range(cols):
        x = BORDER + (i + .5) * iw / cols
        L.append(glyph(str(i + 1), x, mid + cap / 2)); L.append(glyph(str(i + 1), x, H - mid + cap / 2))
    for i in range(rows):
        y = BORDER + (i + .5) * ih / rows
        L.append(glyph("ABCD"[i], mid, y + cap / 2)); L.append(glyph("ABCD"[i], W - mid, y + cap / 2))
    return f'<svg class="zone" aria-hidden="true" viewBox="0 0 {W} {H}" width="{W}pt" height="{H}pt"><g stroke="{INK}" stroke-width="{HAIR}">{"".join(L)}</g></svg>'

TB_W, TB_H = 282.0, 60.0     # title block in pt; sits in the sheet's bottom-right corner against the border
def title_block(T, sheet, total):
    x0, y0 = 0.5, 0.5; w, h = TB_W - 1, TB_H - 1
    r1, r2 = 22.0, 41.0
    c1, c2, c3 = 66.0, 150.0, 222.0
    t1, t2 = 128.0, 226.0
    L = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{PAPER}" stroke="{INK}" stroke-width="{MED}"/>',
         f'<g stroke="{INK}" stroke-width="{HAIR}"><line x1="{x0}" x2="{x0+w}" y1="{r1}" y2="{r1}"/><line x1="{x0}" x2="{x0+w}" y1="{r2}" y2="{r2}"/>'
         f'<line x1="{t1}" x2="{t1}" y1="{y0}" y2="{r1}"/><line x1="{t2}" x2="{t2}" y1="{y0}" y2="{r1}"/>'
         f'<line x1="{c1}" x2="{c1}" y1="{r1}" y2="{y0+h}"/><line x1="{c2}" x2="{c2}" y1="{r1}" y2="{y0+h}"/><line x1="{c3}" x2="{c3}" y1="{r1}" y2="{y0+h}"/></g>']
    def cell(x, y, lab, val, valfont="D-DIN-Bold", vsize=7.2, track=0.0):
        return svg_text(lab, x + 4, y + 6.8, 4.8, "D-DIN", 0.08) + svg_text(val, x + 4, y + 15.8, vsize, valfont, track)
    L.append(cell(x0, y0 - 0.5, "NAME", T["name"].upper(), "D-DINExp-Bold", 8.4, 0.02))
    L.append(cell(t1, y0 - 0.5, "TITLE", "RESUME - GENERIC", "D-DIN-Bold", 7.2, 0.04))
    L.append(cell(t2, y0 - 0.5, "CAGE", "8PMQ9"))
    L.append(cell(x0, r1, "SIZE", "A"))
    L.append(cell(c1, r1, "DWG NO", "PP-RESUME-2026"))
    L.append(cell(c2, r1, "REV", T["rev_letter"]))
    L.append(cell(c3, r1, "SCALE", "NTS"))
    L.append(cell(x0, r2, "DRAWN", "P. PADGETT"))
    L.append(cell(c1, r2, "DATE", T["date"]))
    L.append(cell(c2, r2, "SOURCE", "MASTER RECORD"))
    L.append(cell(c3, r2, "SHEET", f"{sheet} OF {total}"))
    return f'<svg class="tb" aria-hidden="true" viewBox="0 0 {TB_W} {TB_H}" width="{TB_W}pt" height="{TB_H}pt">{"".join(L)}</svg>'

NOTES = ["ALL FIGURES ARE PRODUCTION RESULTS VERIFIED BY THE CANDIDATE.",
         "RED FIGURES ARE MEASURED OUTCOMES; BOLD BLACK FIGURES ARE SCALE, TENURE AND REPEATS. RED UNDERLINED TEXT IS A LIVE LINK.",
         "LATEST REVISION OF THIS SHEET: RESUME.PATPADGETT.COM"]
NB_W, NB_H = 232.0, 60.0
def notes_block():
    """NOTES: rule at y=22, level with the title block's first row line; three notes below, clear of the border."""
    L = [svg_text("NOTES", 0, 17.0, 6.0, "D-DIN-Bold", 0.10),
         f'<line x1="0" x2="{NB_W}" y1="22" y2="22" stroke="{INK}" stroke-width="{HAIR}"/>']
    y = 30.0
    for i, n in enumerate(NOTES, 1):
        L.append(svg_text(f"{i}.", 0, y, 5.4, "D-DIN"))
        words, line, lines = n.split(), "", []
        for wd in words:
            if len(line) + len(wd) + 1 > 68: lines.append(line); line = wd
            else: line = (line + " " + wd).strip()
        lines.append(line)
        for ln in lines:
            L.append(svg_text(ln, 9, y, 5.4, "D-DIN", 0.01)); y += 6.6
        y += 1.0
    return f'<svg class="nb" aria-hidden="true" viewBox="0 0 {NB_W} {NB_H}" width="{NB_W}pt" height="{NB_H}pt">{"".join(L)}</svg>'

def cont_cue(i):
    """Screen-only continuation mark in the zone-label idiom: glyph outlines, never text (stays out of the ATS layer and the print)."""
    d, w = text_path(f"SHEET {i}  -  PROFESSIONAL EXPERIENCE, CONTINUED FROM SHEET {i - 1}", 5.6, "D-DIN-Bold", 0.08)
    return (f'<svg class="cont" aria-hidden="true" viewBox="0 0 {w + 2:.1f} 8" width="{w + 2:.1f}pt" height="8pt">'
            f'<path fill="{INK}" transform="translate(1 6.2)" d="{d}"/></svg>')

DET = 78.0   # detail circle diameter in pt
def detail_view():
    """DETAIL A: the headshot as a detail view; caption centred beneath it, as on a drawing."""
    r = DET / 2; cx = r + 2; cy = r + 2; W_ = DET + 4
    cap_y = DET + 14.0
    d1, w1 = text_path("DETAIL A", 7.4, "D-DIN-Bold", 0.10)
    d2, w2 = text_path("SCALE NTS", 5.4, "D-DIN", 0.10)
    L = [f'<defs><clipPath id="detclip"><circle cx="{cx}" cy="{cy}" r="{r - 0.5}"/></clipPath></defs>',
         f'<image href="assets/headshot.jpg" x="{cx - r}" y="{cy - r}" width="{DET}" height="{DET}" clip-path="url(#detclip)" preserveAspectRatio="xMidYMid slice"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="{MED}"/>',
         f'<path fill="{INK}" transform="translate({cx - w1/2:.2f} {cap_y:.2f})" d="{d1}"/>',
         f'<line x1="{cx - w1/2:.2f}" x2="{cx + w1/2:.2f}" y1="{cap_y + 2.6:.2f}" y2="{cap_y + 2.6:.2f}" stroke="{INK}" stroke-width="{HAIR}"/>',
         f'<path fill="{INK}" transform="translate({cx - w2/2:.2f} {cap_y + 10.2:.2f})" d="{d2}"/>']
    H_ = cap_y + 11
    return (f'<figure class="detail"><svg viewBox="0 0 {W_:.1f} {H_:.1f}" width="{W_:.1f}pt" height="{H_:.1f}pt" role="img" aria-label="Patrick Padgett, headshot">'
            f'{"".join(L)}</svg></figure>')

# ------------------------------------------------------------------ resume body (the ATS text layer, in reading order)
def body_blocks(T):
    c = T["contact"]
    phone = c["Phone"]; tel = "+" + re.sub(r"\D", "", phone)
    B = []
    B.append('<header class="head"><div class="head-text">'
             f'<h1>{esc(T["name"])}</h1>'
             f'<p class="headline">{esc(T["headline"])}</p>'
             f'<p class="contact"><span><a href="tel:{tel}">{esc(phone)}</a></span><span><a href="mailto:{esc(c["Email"])}">{esc(c["Email"])}</a></span><span>{esc(c["Location"])}</span></p>'
             f'<p class="contact"><span><a href="{esc(c["LinkedIn"])}">linkedin.com/in/patpadgett</a></span><span><a href="{esc(c["GitHub"])}">github.com/patpadgett</a></span><span><a href="{esc(c["Website"])}">patpadgett.com</a></span></p>'
             f'</div>{detail_view()}</header>')
    B.append('<h2>PROFESSIONAL SUMMARY</h2>')
    B.append(f'<p class="summary">{redline(T["summary"], demote=("$2M", "250%", "50%", "$50M"))}</p>')
    B.append('<h2>KEY ACHIEVEMENTS</h2>')
    B.append('<ul>' + "".join(f'<li>{redline(a)}</li>' for a in T["achievements"]) + '</ul>')
    B.append('<h2>PROFESSIONAL EXPERIENCE</h2>')
    order = ["VIMOPS", "May 2019 - Feb 2020", "JABIL", "May 2017 - Mar 2018", "RAYMOND", "CODESIGNED", "SPRINT", "CYBERRAZOR", "VARIOUS"]
    jobs = {j["org"].split()[0]: j for j in T["experience"]}
    for key in order:
        if key in T["sabbaticals"]:
            B.append(f'<p class="sabb">{esc(T["sabbaticals"][key])}</p>'); continue
        j = jobs[key]
        org = j["org"] if key != "VARIOUS" else "Various ISPs and Consultancies"
        B.append(f'<div class="job"><h3>{esc(org)}<span class="loc"> | {esc(j["loc"])}</span></h3>'
                 f'<p class="title">{esc(j["title"])}<span class="dates"> | {esc(j["dates"])}</span></p></div>')
        if j["bullets"]:
            B.append('<ul class="exp">' + "".join(f'<li>{redline(b)}</li>' for b in j["bullets"]) + '</ul>')
        elif j.get("line"):
            B.append(f'<p class="oneline">{redline(j["line"])}</p>')
    B.append('<h2>TECHNICAL SKILLS</h2>')
    B.append('<ul class="skills">' + "".join(f'<li><b>{esc(k)}:</b> {esc(v)}</li>' for k, v in T["skills"]) + '</ul>')
    B.append('<h2>PROJECTS</h2>')
    head = T["project"]["head"]
    head_html = esc(head).replace("github.com/patpadgett/corkscrew", '<a href="https://github.com/patpadgett/corkscrew">github.com/patpadgett/corkscrew</a>')
    B.append(f'<p class="proj"><b>{head_html}</b></p>')
    B.append(f'<p>{redline(T["project"]["desc"])}</p>')
    B.append('<h2>EDUCATION AND PROFESSIONAL DEVELOPMENT</h2>')
    B.append(f'<div class="edu"><p>{esc(" | ".join(T["education"]))}</p><p class="profdev">{esc(" ".join(T["profdev"]))}</p></div>')
    return B

# ------------------------------------------------------------------ page
def page_html(T, blocks, paginated=None):
    """paginated: None -> one flow sheet (for the measuring pass); else list of html strings per sheet."""
    desc = ("Patrick Padgett's resume: 14 years as Sprint's Tier III billing mediation SME (Nortel, Ericsson, Lucent CDR/EDR), then DevOps at Jabil and Raymond James.")
    assert 150 <= len(desc) <= 160, len(desc)
    ld = {"@context": "https://schema.org", "@type": "Person", "@id": SITE + "/#person", "name": "Patrick Padgett",
          "url": SITE + "/", "image": SITE + "/assets/headshot.jpg", "email": "mailto:pat@patpadgett.com", "telephone": T["contact"]["Phone"],
          "jobTitle": "Telecom Billing Mediation Engineer | DevOps and Infrastructure Automation",
          "address": {"@type": "PostalAddress", "addressRegion": "FL", "addressLocality": "Tampa Bay", "addressCountry": "US"},
          "sameAs": ["https://www.linkedin.com/in/patpadgett", "https://github.com/patpadgett", "https://patpadgett.com",
                     "https://work.patpadgett.com", "https://blog.patpadgett.com"],
          "knowsAbout": ["Telecom billing mediation", "Revenue assurance", "CDR/EDR processing", "Linux", "Ansible", "Terraform", "Kubernetes",
                         "Docker", "CI/CD", "ELK Stack", "Python", "Perl", "C"],
          "alumniOf": {"@type": "EducationalOrganization", "name": "Lake Career & Technical Center"},
          "mainEntityOfPage": {"@type": "WebPage", "@id": SITE + "/", "name": "Patrick Padgett - Resume",
                               "hasPart": {"@type": "DigitalDocument", "name": "Patrick Padgett - Resume (PDF)", "url": f"{SITE}/{PDF_NAME}", "encodingFormat": "application/pdf"}}}
    ldjson = json.dumps(ld, separators=(",", ":"))
    tel = "+" + re.sub(r"\D", "", T["contact"]["Phone"])
    total = len(paginated) if paginated else 1
    if paginated is None:
        sheets = f'<section class="sheet" data-sheet="1">{zone_strips()}<div class="flow">{"".join(blocks)}</div>' \
                 f'<div class="foot">{notes_block()}{title_block(T, 1, 2)}</div></section>'
    else:
        sheets = "".join(f'<section class="sheet" data-sheet="{i}">{zone_strips()}{cont_cue(i) if i > 1 else ""}<div class="flow">{html}</div>'
                         f'<div class="foot">{notes_block()}{title_block(T, i, total)}</div></section>' for i, html in enumerate(paginated, 1))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Patrick Padgett - Resume | Telecom Billing Mediation and DevOps Engineer</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/">
<meta name="author" content="Patrick Padgett">
<meta name="theme-color" content="#C4CFC1">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="resume.patpadgett.com">
<meta property="og:title" content="Patrick Padgett - Resume">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/">
<meta property="og:image" content="{SITE}/assets/og-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Patrick Padgett resume share card: name, headline, four measured outcomes and portrait, drawn as an engineering drawing sheet">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Patrick Padgett - Resume">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/assets/og-card.jpg">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="alternate" type="application/pdf" href="/{PDF_NAME}" title="Patrick Padgett - Resume (PDF)">
<link rel="preload" href="assets/fonts/D-DINExp-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/D-DIN-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/D-DIN.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css">
<script type="application/ld+json">{ldjson}</script>
</head>
<body>
<a class="skip" href="#resume">Skip to the resume</a>
<nav class="bar" aria-label="Resume downloads">
  <a class="bar-name" href="{SITE}/">PATRICK PADGETT <span>RESUME</span></a>
  <div class="bar-actions">
    <a class="btn btn-ink" href="{PDF_NAME}" download aria-label="Download resume as PDF"><span class="long">Download PDF</span><span class="short">PDF</span></a>
    <a class="btn" href="Patrick_Padgett_Resume.docx" download aria-label="Download resume as Word document"><span class="long">Word (.docx)</span><span class="short">Word</span></a>
    <a class="btn" href="Patrick_Padgett_Resume.txt" download aria-label="Download resume as plain text"><span class="long">Plain text</span><span class="short">Text</span></a>
  </div>
</nav>
<main class="board" id="resume" tabindex="-1">
{sheets}
</main>
<footer class="colophon">
  <p class="colophon-cta"><a class="btn btn-ink" href="mailto:pat@patpadgett.com">Email Patrick</a> <a class="btn" href="tel:{tel}">Call {esc(T["contact"]["Phone"])}</a> <a class="btn" href="{PDF_NAME}" download>Download PDF</a></p>
  <p>Every figure is from the master record; ask about any of them. <a href="https://www.linkedin.com/in/patpadgett">LinkedIn</a> &middot; <a href="https://github.com/patpadgett">GitHub</a> &middot; <a href="https://patpadgett.com">patpadgett.com</a></p>
</footer>
</body>
</html>
"""

# ------------------------------------------------------------------ assets
def make_assets(T):
    from PIL import Image, ImageOps, ImageEnhance, ImageDraw
    A = ROOT / "assets"; F = A / "fonts"; F.mkdir(parents=True, exist_ok=True)
    for fn in ["D-DIN.woff2", "D-DIN-Bold.woff2", "D-DIN-Italic.woff2", "D-DINExp-Bold.woff2"]:
        shutil.copy(FONT_SRC / fn, F / fn)
    shutil.copy(FONT_SRC / "COPYING.txt", F / "D-DIN-OFL.txt")
    # headshot: one ink. grayscale, gentle contrast, sharpened for print
    im = Image.open(HEADSHOT_SRC).convert("L")
    im = ImageOps.autocontrast(im, cutoff=(0.3, 0.2))
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im.save(A / "headshot.jpg", quality=92, optimize=True, progressive=False,
            comment=b"Origin: Patrick Padgett's own headshot (career/resume/resume-ats/final-noc/assets/avatar@2x.jpg, supplied by the owner 2026-09), converted to grayscale with autocontrast by build.py make_assets(); no generative imagery.")
    # icons: a detail-circle mark with PP
    from PIL import ImageFont
    def mark(px):
        img = Image.new("RGB", (px, px), PAPER); d = ImageDraw.Draw(img)
        m = px * 0.09; d.ellipse([m, m, px - m, px - m], outline=INK, width=max(1, int(px * 0.055)))
        f = ImageFont.truetype(str(FONT_SRC / "D-DINExp-Bold.ttf"), int(px * 0.42))
        bb = d.textbbox((0, 0), "PP", font=f); tw, th = bb[2] - bb[0], bb[3] - bb[1]
        d.text(((px - tw) / 2 - bb[0], (px - th) / 2 - bb[1] - px * 0.01), "PP", font=f, fill=RED)
        return img
    from PIL import PngImagePlugin
    def png_meta(px):
        m = PngImagePlugin.PngInfo(); m.add_text("Comment", f"Origin: drawn by build.py mark(): D-DIN Exp Bold 'PP' in a pen-weight circle (PIL), {px}px; no generative imagery."); return m
    mark(512).save(A / "icon-512.png", optimize=True, pnginfo=png_meta(512))
    mark(180).save(A / "apple-touch-icon.png", optimize=True, pnginfo=png_meta(180))
    mark(64).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    d, w = text_path("PP", 42, "D-DINExp-Bold")
    (A / "icon.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" fill="{PAPER}"/>'
                                f'<circle cx="50" cy="50" r="41" fill="none" stroke="{INK}" stroke-width="5.5"/>'
                                f'<path fill="{RED}" transform="translate({50 - w/2:.2f} 65)" d="{d}"/></svg>\n')

def make_docx_txt(T):
    """ATS twins per the master's formatting spec: single column, Calibri, no photo, contact in the body."""
    c = T["contact"]
    order = ["VIMOPS", "May 2019 - Feb 2020", "JABIL", "May 2017 - Mar 2018", "RAYMOND", "CODESIGNED", "SPRINT", "CYBERRAZOR", "VARIOUS"]
    jobs = {j["org"].split()[0]: j for j in T["experience"]}
    L = [T["name"], T["headline"], f'{c["Phone"]} | {c["Email"]} | {c["Location"]}',
         "linkedin.com/in/patpadgett | github.com/patpadgett | patpadgett.com", "",
         "PROFESSIONAL SUMMARY", T["summary"], "", "KEY ACHIEVEMENTS"] + [f"- {a}" for a in T["achievements"]] + ["", "PROFESSIONAL EXPERIENCE"]
    for key in order:
        if key in T["sabbaticals"]: L += [T["sabbaticals"][key], ""]; continue
        j = jobs[key]; org = j["org"] if key != "VARIOUS" else "Various ISPs and Consultancies"
        L += [f"{org} | {j['loc']}", f"{j['title']} | {j['dates']}"]
        L += [f"- {b}" for b in j["bullets"]] if j["bullets"] else ([j["line"]] if j.get("line") else [])
        L.append("")
    L += ["TECHNICAL SKILLS"] + [f"{k}: {v}" for k, v in T["skills"]] + [""]
    L += ["PROJECTS", T["project"]["head"], T["project"]["desc"], "", "EDUCATION AND PROFESSIONAL DEVELOPMENT", " | ".join(T["education"])]
    L += [f"- {d}" for d in T["profdev"]] + ["", "KEYWORDS", T["ats_line"], ""]
    txt = "\n".join(L); ascii_check(txt)
    (ROOT / "Patrick_Padgett_Resume.txt").write_text(txt)
    md = "\n".join(("# " + l if i == 0 else ("## " + l if l in ("PROFESSIONAL SUMMARY", "KEY ACHIEVEMENTS", "TECHNICAL SKILLS", "PROFESSIONAL EXPERIENCE", "PROJECTS", "EDUCATION AND PROFESSIONAL DEVELOPMENT", "KEYWORDS") else l)) for i, l in enumerate(L))
    (ROOT / "Patrick_Padgett_Resume.md").write_text(md)
    from docx import Document
    from docx.shared import Pt, Inches
    from docx.oxml.ns import qn
    d = Document()
    for s in d.sections: s.left_margin = s.right_margin = Inches(0.6); s.top_margin = s.bottom_margin = Inches(0.55)
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5); st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    st.paragraph_format.space_after = Pt(3); st.paragraph_format.line_spacing = 1.05
    d.core_properties.author = T["name"]; d.core_properties.title = f"{T['name']} - Resume"; d.core_properties.keywords = T["ats_line"][:250]
    d.core_properties.subject = T["headline"]; d.core_properties.comments = ""; d.core_properties.last_modified_by = T["name"]   # python-docx stamps "generated by python-docx" otherwise
    def para(text, size=None, bold=False, after=4, before=0, italic=False):
        p = d.add_paragraph(); r = p.add_run(text); r.bold = bold; r.italic = italic
        if size: r.font.size = Pt(size)
        p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(before); return p
    def head(t): para(t, size=12, bold=True, before=10, after=3)
    def bullet(t): p = d.add_paragraph(t, style="List Bullet"); p.paragraph_format.space_after = Pt(3)
    para(T["name"], size=18, bold=True, after=0); para(T["headline"], size=11, after=1)
    para(f'{c["Phone"]} | {c["Email"]} | {c["Location"]}', after=0); para("linkedin.com/in/patpadgett | github.com/patpadgett | patpadgett.com", after=6)
    head("PROFESSIONAL SUMMARY"); para(T["summary"])
    head("KEY ACHIEVEMENTS"); [bullet(a) for a in T["achievements"]]
    head("PROFESSIONAL EXPERIENCE")
    for key in order:
        if key in T["sabbaticals"]: para(T["sabbaticals"][key], italic=True, before=4, after=2); continue
        j = jobs[key]; org = j["org"] if key != "VARIOUS" else "Various ISPs and Consultancies"
        para(f"{org} | {j['loc']}", bold=True, before=6, after=0); para(f"{j['title']} | {j['dates']}", after=2)
        if j["bullets"]: [bullet(b) for b in j["bullets"]]
        elif j.get("line"): para(j["line"])
    head("TECHNICAL SKILLS")
    for k, v in T["skills"]:
        p = d.add_paragraph(); r = p.add_run(k + ": "); r.bold = True; p.add_run(v); p.paragraph_format.space_after = Pt(2)
    head("PROJECTS"); para(T["project"]["head"], bold=True, after=1); para(T["project"]["desc"])
    head("EDUCATION AND PROFESSIONAL DEVELOPMENT"); para(" | ".join(T["education"]), after=2); [bullet(x) for x in T["profdev"]]
    head("KEYWORDS"); para(T["ats_line"], size=9)
    d.save(ROOT / "Patrick_Padgett_Resume.docx")

def make_og_page(T):
    """Identity-led share card source: name at display size, headline, one outcome, DETAIL A, border + zone band. Rendered to 1200x630 by render.js."""
    c = T["contact"]
    (ROOT / ".og.html").write_text(f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><link rel="preload" href="assets/fonts/D-DINExp-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/D-DIN-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/D-DIN.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css">
<style>
html,body{{margin:0;background:{PAPER};width:1200px;height:630px;overflow:hidden}}
.og{{position:relative;width:1200px;height:630px;background:{PAPER};font-family:"D-DIN",sans-serif;color:{INK}}}
.og .frame{{position:absolute;inset:34px;border:5px solid {INK}}}
.og .trim{{position:absolute;inset:14px;border:1px solid {INK}}}
.og .tick{{position:absolute;background:{INK}}}
.og .z{{position:absolute;font:700 13px/1 "D-DIN",sans-serif}}
.og .col{{position:absolute;left:92px;top:110px;width:700px}}
.og .name{{font:700 88px/0.95 "D-DIN Exp","D-DIN",sans-serif;text-transform:uppercase;letter-spacing:.01em}}
.og .hl{{margin-top:22px;font:700 28px/1.2 "D-DIN",sans-serif}}
.og .proof{{margin-top:16px;font:400 24px/1.38 "D-DIN",sans-serif}}
.og .proof b{{color:{RED};font-weight:700}}
.og .url{{position:absolute;left:92px;bottom:66px;font:700 24px/1 "D-DIN",sans-serif;letter-spacing:.12em;color:{RED}}}
.og .det{{position:absolute;right:92px;top:96px;width:300px;text-align:center}}
.og .det .ph{{width:300px;height:300px;border-radius:50%;border:5px solid {INK};background:url(assets/headshot.jpg) center/cover;box-sizing:border-box}}
.og .det .cap{{margin-top:18px;font:700 18px/1 "D-DIN",sans-serif;letter-spacing:.14em}}
.og .det .cap small{{display:block;margin-top:8px;font:400 14px/1 "D-DIN",sans-serif;letter-spacing:.14em}}
.og .rule{{margin-top:16px;width:660px;height:3px;background:{INK}}}
</style></head><body><div class="og">
<div class="trim"></div><div class="frame"></div>
<span class="z" style="left:50%;top:18px;transform:translateX(-50%)">2</span><span class="z" style="left:22px;top:50%;transform:translateY(-50%)">A</span><span class="z" style="right:22px;top:50%;transform:translateY(-50%)">A</span><span class="z" style="left:50%;bottom:16px;transform:translateX(-50%)">2</span>
<div class="col"><div class="name">{esc(T["name"].split()[0])}<br>{esc(T["name"].split()[-1])}</div>
<div class="rule"></div>
<div class="hl">{esc(T["headline"]).replace(" | ", "<br>")}</div>
<div class="proof">Saved <b>$2M</b> a year with an EDR routing application; raised mediation throughput <b>250%</b>; cut alarm MTTR <b>50%</b>; led a <b>$50M</b>, 130-switch platform replacement.</div></div>
<div class="url">RESUME.PATPADGETT.COM</div>
<div class="det"><div class="ph" role="img" aria-label="Patrick Padgett"></div><div class="cap">DETAIL A<small>SCALE NTS</small></div></div>
</div></body></html>""")

def make_site_files():
    today = datetime.date.today().isoformat()
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      f'  <url><loc>{SITE}/</loc><lastmod>{today}</lastmod></url>\n'
                                      f'  <url><loc>{SITE}/{PDF_NAME}</loc><lastmod>{today}</lastmod></url>\n</urlset>\n')
    (ROOT / "404.html").write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sheet not found - Patrick Padgett</title><meta name="robots" content="noindex,follow">
<link rel="icon" href="/favicon.ico" sizes="32x32"><link rel="stylesheet" href="/styles.css"></head>
<body class="p404"><main class="board"><section class="sheet sheet-404">
<h1>SHEET NOT FOUND</h1>
<p>There is no drawing at this address. The resume is two sheets and lives at the root.</p>
<p><a class="btn btn-ink" href="/">Open the resume</a> <a class="btn" href="/{PDF_NAME}">Download the PDF</a></p>
</section></main></body></html>
""")

# ------------------------------------------------------------------ main
def main():
    no_pdf = "--no-pdf" in sys.argv
    R = bfm.parse(MASTER.read_text()); T = select(R)
    make_assets(T); make_docx_txt(T); make_site_files(); make_og_page(T)
    blocks = body_blocks(T)
    flow_html = page_html(T, blocks)
    ascii_check(re.sub(r"<[^>]+>", "", flow_html).replace("&middot;", ""))
    (ROOT / "index.html").write_text(flow_html)
    json.dump({"rev": T["rev"], "date": T["date"], "site": SITE, "pdf": PDF_NAME}, open(ROOT / ".build.json", "w"))
    print("wrote flow index.html, assets, docx/txt/md")
    if no_pdf: return
    env = dict(os.environ, NODE_PATH="/data/pat/node_modules")
    r = subprocess.run(["node", str(ROOT / "render.js")], cwd=str(ROOT), env=env, capture_output=True, text=True)
    print(r.stdout[-4000:]); print(r.stderr[-2000:], file=sys.stderr)
    if r.returncode: sys.exit(r.returncode)
    # rebuild the final static page from the paginated sheets
    sheets = json.load(open(ROOT / ".paginated.json"))
    final = page_html(T, blocks, paginated=sheets)
    ascii_check(re.sub(r"<[^>]+>", "", final).replace("&middot;", ""))
    (ROOT / "index.html").write_text(final)
    r = subprocess.run(["node", str(ROOT / "render.js"), "--final"], cwd=str(ROOT), env=env, capture_output=True, text=True)
    print(r.stdout[-4000:]); print(r.stderr[-2000:], file=sys.stderr)
    if r.returncode: sys.exit(r.returncode)
    os.remove(ROOT / ".paginated.json")
    import fitz
    with fitz.open(str(ROOT / PDF_NAME)) as doc:
        doc.set_metadata({**doc.metadata, "title": f"{T['name']} - Resume | {T['headline'].replace(' | ', ' and ')}", "author": T["name"],
                          "subject": T["headline"], "keywords": T["ats_line"][:500], "creator": "resume.patpadgett.com build", "producer": "Chromium (Playwright) via render.js"})
        doc.saveIncr()
    from PIL import Image
    og = ROOT / "assets" / "og-card.png"
    im = Image.open(og).convert("RGB"); assert im.size == (1200, 630), f"og card is {im.size}, meta says 1200x630"
    im.save(ROOT / "assets" / "og-card.jpg", quality=84, optimize=True,
        comment=b"Origin: composed share card (.og.html: name, headline, outcomes, DETAIL A) rendered by render.js (Playwright/Chromium) at 1200x630, JPEG q84; no generative imagery.")
    os.remove(og); (ROOT / ".og.html").unlink(missing_ok=True)
    embed_provenance()

IMPECCABLE = Path("/data/pat/.hermes/skills/creative/impeccable/scripts/impeccable")
PROVENANCE = {
    "assets/headshot.jpg": "Origin: Patrick Padgett's own headshot (career/resume/resume-ats/final-noc/assets/avatar@2x.jpg, supplied by the owner 2026-09), converted to grayscale with autocontrast by build.py make_assets(); no generative imagery.",
    "assets/og-card.jpg": "Origin: composed share card (.og.html: name, headline, outcomes, DETAIL A portrait) rendered by render.js (Playwright/Chromium) at 1200x630, JPEG q84; no generative imagery.",
    "assets/icon-512.png": "Origin: drawn by build.py mark(): D-DIN Exp Bold 'PP' in a pen-weight circle (PIL), 512px; no generative imagery.",
    "assets/apple-touch-icon.png": "Origin: drawn by build.py mark(): D-DIN Exp Bold 'PP' in a pen-weight circle (PIL), 180px; no generative imagery.",
}
def embed_provenance():
    """Every shipping raster carries its origin in the Impeccable marker format (embed-prompt --scan must report 0 missing)."""
    if not IMPECCABLE.exists():
        print("impeccable launcher not found; provenance not embedded"); return
    pf = ROOT / ".prov.txt"
    for rel, txt in PROVENANCE.items():
        pf.write_text(txt)
        subprocess.run([str(IMPECCABLE), "embed-prompt", rel, "--prompt-file", str(pf)], cwd=str(ROOT), capture_output=True, text=True)
    pf.unlink(missing_ok=True)
    r = subprocess.run([str(IMPECCABLE), "embed-prompt", "--scan", "assets"], cwd=str(ROOT), capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1])

if __name__ == "__main__":
    main()
