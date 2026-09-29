"""ATS compatibility + keyword bench for the generic resume (uses the resume system's own checkers)."""
import sys, re, glob
sys.path.insert(0, "/data/pat/career/resume")
import ats_check
R = "/data/pat/2_PUBLISHED/resume.patpadgett.com/"
for f in ["Patrick_Padgett_Resume.pdf", "Patrick_Padgett_Resume.docx"]:
    sc, iss, txt = ats_check.compat(R + f)
    print(f, "compat score", sc, "issues", iss or "none")
# keyword match against every saved JD (median is what matters for a generic version)
jds = sorted(glob.glob("/data/pat/career/resume/jd/*.txt")) + sorted(glob.glob("/data/pat/career/resume/jd/devops_bench/*.txt"))
sc, iss, txt = ats_check.compat(R + "Patrick_Padgett_Resume.pdf")
scores = []
for jd in jds:
    try:
        kws = ats_check.jd_keywords(open(jd).read())
    except Exception as e:
        continue
    if not kws: continue
    tl = txt.lower()
    hit = [k for k in kws if k.lower() in tl]
    scores.append((round(100 * len(hit) / len(kws)), jd.split("/")[-1]))
scores.sort()
if scores:
    import statistics
    print("keyword match vs", len(scores), "saved postings: median", statistics.median([s for s, _ in scores]), "min", scores[0], "max", scores[-1])
