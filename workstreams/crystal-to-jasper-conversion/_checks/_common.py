"""Shared path resolution for the Crystal->Jasper layout checks.

Usage from any check script:

    from _common import open_pair
    gen, ref = open_pair()          # report number from argv[1], e.g.  py compare_ink.py R07.004

Layout assumed (same for every report in this project):
    C:\\Projects\\INPEX\\sources\\CrystalReports\\<report>\\output\\*.pdf          <- generated
    C:\\Projects\\INPEX\\sources\\CrystalReports\\<report>\\crytsal report in pdf\\*.pdf  <- reference
      (the folder really is spelled "crytsal" in the source tree)
"""
import glob
import os
import sys

import fitz

BASE = r"C:\Projects\INPEX\sources\CrystalReports"


def resolve(report):
    root = os.path.join(BASE, report)
    gen = [p for p in glob.glob(os.path.join(root, "output", "*.pdf"))
           if not os.path.basename(p).startswith("_")]
    ref = glob.glob(os.path.join(root, "crytsal report in pdf", "*.pdf"))
    if not gen:
        raise SystemExit(f"no generated PDF under {root}\\output")
    if not ref:
        raise SystemExit(f"no reference PDF under {root}\\crytsal report in pdf")
    if len(gen) > 1:
        print(f"NOTE: {len(gen)} generated PDFs found, using {os.path.basename(gen[0])}")
    if len(ref) > 1:
        print(f"NOTE: {len(ref)} reference PDFs found, using {os.path.basename(ref[0])}")
    return gen[0], ref[0]


def open_pair(report=None):
    if report is None:
        if len(sys.argv) < 2:
            raise SystemExit(f"usage: py {os.path.basename(sys.argv[0])} <report>   "
                             f"e.g. R07.004")
        report = sys.argv[1]
    g, r = resolve(report)
    # GENPDF overrides the generated file - used to point a check at a temp build (the real
    # PDF is often locked open in a viewer) or at an older build to validate a check.
    if os.environ.get("GENPDF"):
        g = os.path.join(BASE, report, os.environ["GENPDF"].lstrip("\\/"))
    print(f"report   : {report}")
    print(f"generated: {g}")
    print(f"reference: {r}\n")
    return fitz.open(g), fitz.open(r)
