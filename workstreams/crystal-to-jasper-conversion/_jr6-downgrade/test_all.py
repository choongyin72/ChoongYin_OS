"""TEST ONLY - can each 7.0.3 report be downgraded to 6.17.0 and render identically?

Owner instruction: "no fix code... only test its able to downgrade and have same report for
both version". This script therefore NEVER edits a report's JRXML. It writes only into
<report>/output/jr6/.

Method, per report:
  1. jr7_to_jr6.py                    7.0.3 compact JRXML -> 6.x classic JRXML
  2. run the report's OWN harness     twice: once on 7.0.3 jars against the original JRXML,
                                      once on 6.17.0 jars against the downgraded JRXML
  3. verify_jr6.py --pdf              exact span + rect + font comparison of the two PDFs
  4. Jr6Build jasper + LoadJasper     can EC's LEGACY 6.21.4 engine load the 6.17.0 .jasper?

Running each report's own harness - rather than a generic fill - is deliberate. R07.017-022
fill from a hand-built JRMapCollectionDataSource of 2 synthetic months with a per-report
rowAt() helper; reimplementing that would mean guessing field names, and a fill that differs
from the 7.x baseline produces span differences that have nothing to do with the downgrade.
The harnesses use one 7.x-only class (net.sf.jasperreports.pdf.JRPdfExporter, which lived in
engine.export before 7.0); that single import is rewritten for the 6.x build and nothing else.

Both PDFs are generated FRESH in this run, so there is no question of which stale artifact in
output/ is the right baseline.
"""
import os
import re
import shutil
import subprocess
import sys

D = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:\Projects\INPEX\sources\CrystalReports"
SCRATCH = (r"C:\Users\CHOONG~1.LEE\AppData\Local\Temp\claude"
           r"\c--Projects-ChoongYin-OS\1df64597-646b-4513-971d-739ca8fa442e\scratchpad")
EC621 = os.path.join(SCRATCH, "ec621", "lib", "*")
ECLOAD = os.path.join(SCRATCH, "jt", "c621")
FONTS = os.path.join(BASE, "R07.001", "output", "fonts", "inpex-arial-fonts.jar")
WORK = os.path.join(D, "_testwork")

# Fill mode is NOT chosen here - each report's own harness decides it. This list is only the
# set under test, in the owner's stated order.
REPORTS = ["R07.001", "R07.002", "R07.003", "R07.004", "R07.005", "R07.006"] + \
          [f"R07.{n:03d}" for n in range(11, 26)]

# Every report declares P_BASE_URL defaulting to the EC extension path
# "/extension/ZREP/reports/" - correct for EC, but on a local disk that resolves to the drive
# root, where no logo is present, so neither PDF could be produced. Overriding it for the local
# run keeps every JRXML untouched, and is applied to the 7.x and 6.x side alike so it cannot
# influence whether they match.
#
# Points at the real extension folder rather than "./": since the logo names were normalised to
# logo.png (R07.001-006) and ichthys-logo.png (R07.011-025), a report's OWN output/ folder no
# longer holds the asset name it asks for, and the extension folder is the only place that has
# both. Using "./" fails with "Byte data not found at: ./ichthys-logo.png".
ASSET_DIR = (r"C:\Projects\INPEX\DEV\ecaas_inpex_ichthys\extensions\zrep\zrep"
             r"\src\main\webapp\reports")
PARAM_OVERRIDE = {r: {"P_BASE_URL": ASSET_DIR.replace("\\", "/") + "/"} for r in REPORTS}


def run(cmd, cwd=None, timeout=300):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       timeout=timeout, shell=False)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def cp7(report):
    """The 7.0.3 classpath. Per-report cp.txt if it has one, else R07.001's.

    The Arial font extension is appended unconditionally. Not every report's cp.txt carries it
    (R07.012's and R07.014's do not), and without it the 7.x BASELINE silently falls back to
    Helvetica and drops bold/italic - so the baseline, not the downgrade, is what is broken,
    and the comparison reports a font difference in the wrong direction. Same jar the 6.x side
    gets, so both engines are on equal footing.
    """
    for r in (report, "R07.001"):
        f = os.path.join(BASE, r, "cp.txt")
        if os.path.exists(f):
            with open(f) as fh:
                cp = fh.read().strip()
            return cp if "inpex-arial-fonts" in cp else cp + ";" + FONTS
    return None


def harness(report, jrxml=None):
    """The report's harness sources, and the main class that fills THIS jrxml.

    Some R10 folders hold more than one report file and more than one *Verify.java - R10.030
    has three jrxml against R10030SdsVerify/R10030Verify, R10.031 two, R10.012 two. Taking
    main[0] picks whichever the directory listing happened to put first, which is not a
    choice at all. The pairing rule is the one tmp/r10_regen.py already uses and renders with:
    a file whose name contains SDS fills through the Sds harness, everything else through the
    plain one.
    """
    d = os.path.join(BASE, report, "java", "src", "com", "example", "reports")
    if not os.path.isdir(d):
        return None, None
    srcs = [os.path.join(d, f) for f in os.listdir(d)
            if f.endswith(".java") and "backup" not in f]
    main = [os.path.basename(f)[:-5] for f in srcs if f.endswith("Verify.java")]
    if not main:
        return None, None
    sds = next((c for c in main if "Sds" in c), None)
    plain = next((c for c in main if "Sds" not in c), None)
    cls = sds if (jrxml and "SDS" in jrxml.upper() and sds) else (plain or main[0])
    return srcs, "com.example.reports." + cls


def brief(text, n=110):
    """Pull the most diagnostic line(s) out of a java failure.

    JRValidationException puts 'Report design not valid :' on one line and the numbered
    reasons on the lines AFTER it, so that one needs its follow-on lines or the message is
    useless. Full text is always kept in _testwork/<report>/fail.log.
    """
    m = re.search(r"Report design not valid[^\n]*\n((?:\s+\d+\..*\n){1,40})", text)
    if m:
        reasons = [l.strip() for l in m.group(1).splitlines() if l.strip()]
        return f"{len(reasons)} invalid: " + " ;; ".join(reasons)[:400]
    for pat in (r"SAXParseException[^\n]*", r"ORA-\d+[^\n]*", r"cvc-[^\n]*",
                r"net\.sf\.jasperreports[^\n]*Exception[^\n]*", r"\w+Exception[^\n]*"):
        mm = re.search(pat, text)
        if mm:
            return mm.group(0)[:n]
    return text.strip().splitlines()[-1][:n] if text.strip() else "?"


def candidates(report):
    out = os.path.join(BASE, report, "output")
    if not os.path.isdir(out):
        return []
    return sorted(f for f in os.listdir(out)
                  if f.endswith(".jrxml") and "backup" not in f
                  and "variant" not in f.lower())


def test(report, pick=None):
    out = os.path.join(BASE, report, "output")
    jr6 = os.path.join(out, "jr6")
    srcs = glob = None
    cand = candidates(report)
    if pick:
        cand = [f for f in cand if f == pick]
    if len(cand) != 1:
        return report, "NO-JRXML", f"{len(cand)} candidates", ""
    src = os.path.join(out, cand[0])
    stem = cand[0][:-6]
    os.makedirs(jr6, exist_ok=True)

    # ---- 1. downgrade
    conv6 = os.path.join(jr6, stem + "_jr6.jrxml")
    rc, log = run(["py", os.path.join(D, "jr7_to_jr6.py"), src, conv6])
    if rc != 0 or "elements:" not in log:
        return report, "CONVERT-FAIL", brief(log), ""

    # ---- 2. the report's own harness, built twice
    srcs, mainclass = harness(report, cand[0])
    if not srcs:
        return report, "NO-HARNESS", "no *Verify.java", ""
    c7 = cp7(report)
    if not c7:
        return report, "NO-CP", "no cp.txt", ""

    w7 = os.path.join(WORK, report, "c7")
    w6 = os.path.join(WORK, report, "c6")
    s7 = os.path.join(WORK, report, "s7")
    s6 = os.path.join(WORK, report, "s6")
    for p in (w7, w6, s7, s6):
        os.makedirs(p, exist_ok=True)

    def stage_src(dest, for_six):
        """Copy the harness, rewriting only what a LOCAL run needs. Both engines get the
        same treatment, so nothing here can bias the comparison."""
        made = []
        for f in srcs:
            with open(f, encoding="utf-8") as fh:
                t = fh.read()
            if for_six:
                # the one 7.x-only class: the pdf exporter moved out of engine.export in 7.0
                t = t.replace("net.sf.jasperreports.pdf.JRPdfExporter",
                              "net.sf.jasperreports.engine.export.JRPdfExporter")
            for k, v in PARAM_OVERRIDE.get(report, {}).items():
                t = t.replace(
                    "Map<String, Object> params = new HashMap<>();",
                    "Map<String, Object> params = new HashMap<>();\n"
                    f'        params.put("{k}", "{v}");', 1)
            g = os.path.join(dest, os.path.basename(f))
            with open(g, "w", encoding="utf-8") as fh:
                fh.write(t)
            made.append(g)
        return made

    src7, src6 = stage_src(s7, False), stage_src(s6, True)

    rc, log = run(["javac", "-nowarn", "-cp", c7, "-d", w7] + src7)
    if rc != 0:
        return report, "HARNESS-7-FAIL", brief(log), ""
    cp6lib = os.path.join(D, "jr6170-lib", "*") + ";" + FONTS
    rc, log = run(["javac", "-nowarn", "-cp", cp6lib, "-d", w6] + src6)
    if rc != 0:
        return report, "HARNESS-6-FAIL", brief(log), ""

    # ---- 3. two fresh PDFs, same harness, same data, different engine
    pdf7 = os.path.join(jr6, stem + "_ref7.pdf")
    pdf6 = os.path.join(jr6, stem + "_jr6.pdf")
    for p in (pdf7, pdf6):
        if os.path.exists(p):
            os.remove(p)

    rc, log = run(["java", "-cp", c7 + ";" + w7, mainclass, src, pdf7], cwd=out)
    if rc != 0 or not os.path.exists(pdf7):
        return report, "BASELINE-7-FAIL", brief(log), ""
    rc, log = run(["java", "-cp", cp6lib + ";" + w6, mainclass, conv6, pdf6], cwd=out)
    if not os.path.exists(pdf6):
        stage = "COMPILE-FAIL" if "COMPILE OK" not in log else "FILL-FAIL"
        with open(os.path.join(WORK, report, "fail.log"), "w", encoding="utf-8") as fh:
            fh.write(log)
        return report, stage, brief(log), ""

    # ---- 4. exact comparison
    rc, log = run(["py", os.path.join(D, "verify_jr6.py"), "--pdf", pdf6, pdf7, "--no-image"])
    status = "IDENTICAL" if "RESULT: IDENTICAL" in log else "DIFFERS"
    detail = ""
    if status == "DIFFERS":
        detail = " | ".join(l.strip() for l in log.splitlines()
                            if "DIFFER" in l or l.strip().startswith("pages"))[:150]
    else:
        m = re.search(r"text spans\s*: 6\.x=(\d+)", log)
        r2 = re.search(r"drawing rects\s*: 6\.x=(\d+)", log)
        detail = f"{m.group(1) if m else '?'} spans, {r2.group(1) if r2 else '?'} rects"

    # ---- 5. EC legacy 6.21.4 load check on the 6.17.0-compiled .jasper
    ecl = "-"
    rc, log = run(["sh", os.path.join(D, "jr6build.sh"), report, "jasper"])
    jas = os.path.join(jr6, stem + "_jr6.jasper")
    if os.path.exists(jas):
        rc, log = run(["java", "-cp", EC621 + ";" + ECLOAD, "LoadJasper", jas])
        ecl = "EC-LOAD-OK" if "LOADS OK" in log else "EC-LOAD-FAIL"
    else:
        ecl = "NO-JASPER"
    return report, status, detail, ecl


def main():
    todo = sys.argv[1:] or REPORTS
    # A folder holding several report files is expanded into one run per file, rather than
    # reported as NO-JRXML and skipped. That skip is why R10.012/030/031 - seven files, all
    # already layout-verified - had no 6.17 copy at all.
    jobs = []
    for r in todo:
        cand = candidates(r)
        jobs.extend([(r, c) for c in cand] if len(cand) > 1 else [(r, None)])
    rows = []
    for r, pick in jobs:
        label = r if pick is None else f"{r} {pick[:-6][-28:]}"
        try:
            row = test(r, pick)
        except subprocess.TimeoutExpired:
            row = (r, "TIMEOUT", "", "")
        except Exception as e:                                  # noqa: BLE001
            row = (r, "ERROR", f"{type(e).__name__}: {e}"[:110], "")
        row = (label,) + tuple(row[1:])
        rows.append(row)
        print(f"{row[0]:<38} {row[1]:<16} {row[3]:<13} {row[2]}", flush=True)

    print("\n=== SUMMARY")
    for st in ("IDENTICAL", "DIFFERS", "COMPILE-FAIL", "FILL-FAIL", "CONVERT-FAIL"):
        hit = [r[0] for r in rows if r[1] == st]
        if hit:
            print(f"{st:<14} {len(hit):>2}  {' '.join(hit)}")
    other = [r for r in rows if r[1] not in
             ("IDENTICAL", "DIFFERS", "COMPILE-FAIL", "FILL-FAIL", "CONVERT-FAIL")]
    for r in other:
        print(f"{r[1]:<14}  1  {r[0]}  {r[2]}")


if __name__ == "__main__":
    main()
