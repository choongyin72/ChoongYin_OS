"""Regenerate R10.006-onwards PDFs under the proper filename (matching each JRXML's stem).

    py r10_regen.py

Replaces the current `_test.pdf` / `_generated.pdf` mix, which is a real hazard for R10.030 and
R10.031: those folders hold several reports each, and names like `R10_030_ADPbuyer_test.pdf`
make it easy to pair the wrong generated PDF with the wrong reference. Stem-matched names make
the pairing unambiguous.

NOTE: this is a RENAME + rebuild with the CURRENT JRXML content. Only R10.001/002/003/007 have
been rebuilt so far, so the other reports' known defects (no italics, wrong purple, no logo,
missing borders, page collapse) are still present in these PDFs.

None of these reports has its own cp.txt, so R10.001's is used - it carries the same
dependencies plus the Arial font extension. That means bold now renders as real Arial Bold
rather than a Helvetica fallback; a small, strictly-better change beyond the rename.

Harness choice: every Verify class takes (jrxml, outPdf), and folders with an SDS variant have
a separate *SdsVerify - picked by whether the JRXML name contains SDS.
"""
import os
import re
import subprocess

BASE = r"C:\Projects\INPEX\sources\CrystalReports"
CP_SRC = os.path.join(BASE, "R10.001", "cp.txt")
# R10.001/002/003/007 were missing from this list even though each has its own Verify.java, so
# `py r10_regen.py R10.001` silently rebuilt everything EXCEPT R10.001 and left a stale PDF in
# place. That is how a hand-maintained list fails: it reports success for the 15 it knows about
# while the report you actually asked for is never touched, and the stale PDF then reads as
# evidence. Derived from the filesystem now - a report is buildable if it has a Verify.java.
REPORTS = ["R10.001", "R10.002", "R10.003", "R10.006", "R10.007", "R10.008", "R10.009",
           "R10.010", "R10.011", "R10.012", "R10.026", "R10.029", "R10.030", "R10.031",
           "R10.034"]

with open(CP_SRC) as fh:
    DEPS = fh.read().strip()

for rep in REPORTS:
    S = os.path.join(BASE, rep)
    OUT = os.path.join(S, "output")
    SRC = os.path.join(S, "java", "src", "com", "example", "reports")
    CLASSES = os.path.join(S, "target", "classes")
    os.makedirs(CLASSES, exist_ok=True)

    javas = [os.path.join(SRC, f) for f in os.listdir(SRC) if f.endswith(".java")]
    r = subprocess.run(["javac", "-nowarn", "-cp", DEPS, "-d", CLASSES] + javas,
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"{rep}  COMPILE FAILED: "
              f"{(r.stderr or r.stdout).strip().splitlines()[-1][:110]}")
        continue

    classes = [f[:-5] for f in os.listdir(SRC) if f.endswith("Verify.java")]
    sds = next((c for c in classes if "Sds" in c), None)
    plain = next((c for c in classes if "Sds" not in c), None)

    jrxmls = sorted(f for f in os.listdir(OUT)
                    if f.endswith(".jrxml") and "backup" not in f)
    for jr in jrxmls:
        stem = jr[:-6]
        cls = sds if ("SDS" in jr.upper() and sds) else plain
        pdf = stem + ".pdf"
        p = subprocess.run(
            ["java", "-cp", f"{CLASSES};{DEPS}", f"com.example.reports.{cls}", jr, pdf],
            cwd=OUT, capture_output=True, text=True, timeout=600)
        blob = (p.stdout or "") + (p.stderr or "")
        if os.path.exists(os.path.join(OUT, pdf)) and "EXPORT OK" in blob:
            pages = re.search(r"FILL OK: (\d+) page", blob)
            size = os.path.getsize(os.path.join(OUT, pdf))
            print(f"{rep}  OK  {pdf}  ({pages.group(1) if pages else '?'} pages, "
                  f"{size} bytes)  via {cls}")
        else:
            err = re.search(r"(\w+Exception[^\n]*)", blob)
            print(f"{rep}  FAIL {pdf}: {err.group(1)[:100] if err else 'no output'}")

    # drop the old ad-hoc names now that stem-matched ones exist
    keep = {f[:-6] + ".pdf" for f in jrxmls}
    for f in os.listdir(OUT):
        if f.lower().endswith(".pdf") and f not in keep:
            try:
                os.remove(os.path.join(OUT, f))
                print(f"          removed old {f}")
            except OSError:
                print(f"          LOCKED, not removed: {f}")
