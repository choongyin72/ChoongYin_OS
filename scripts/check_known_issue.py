#!/usr/bin/env python3
"""STEP 0 on ANY EC blocker: have we already hit this? Run BEFORE the first live scan.

    py scripts/check_known_issue.py "Chemical Product" CHEM_USAGE_REPORT_CONF
    py scripts/check_known_issue.py "ORA-02292: integrity constraint ... child record found"

Searches every place a past diagnosis could live, prints file:line hits, and exits 2 when it finds
anything (2 = STOP AND READ THOSE FIRST), 0 when the ground is genuinely new.

Origin: 2026-07-31. Asked for Chemical Product's (CO.0072) delete gesture I ran three fresh live scans
and produced a THINNER diagnosis of something already written up in EC_KNOWN_ISSUES.md:202-219 - then
asked the owner a question the file had already answered, and mis-classified an EC PRODUCT DEFECT (the
UI silently swallows ORA-02292/ORA-20102) as a gap in my own knowledge. Owner: "next times do a scan to
check u face such error problem or not." A rule I have to remember is the thing that failed; a command
that prints hits does not depend on my memory.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# every place a past EC diagnosis / park / gotcha can live
SOURCES = [
    "ec-ui-knowledge/EC_KNOWN_ISSUES.md",
    "ec-ui-knowledge/EC_UI_SOP.md",
    "ec-ui-knowledge/EC_BUG_TRACE_SOP.md",
    "ec-ui-knowledge/screens/*.md",
    "tmp/OV_SWEEP_PARKED.md",
    "docs/lessons-learned.md",
    "docs/session-memory.md",
    "docs/automation-scorecard.md",
    "workstreams/master-plan/ec-automation/docs/ec_screen_registry.md",
    "workstreams/master-plan/ec-automation/docs/*.md",
]


def a(s):
    """The source docs contain em-dashes/arrows; this console is cp1252 and raises on them.
    Everything printed goes through here (found by running it, not by reading it)."""
    return str(s).encode("ascii", "replace").decode("ascii")


def files():
    seen, out = set(), []
    for pat in SOURCES:
        for p in (sorted(ROOT.glob(pat)) if "*" in pat else [ROOT / pat]):
            if p.is_file() and p not in seen:
                seen.add(p)
                out.append(p)
    return out


def terms_from(argv):
    """Take the raw args AND auto-extract high-signal tokens from a pasted error string:
    ORA-nnnnn codes, EC error codes, CONSTRAINT/FK names, and ALL_CAPS table names."""
    terms = [x.strip() for x in argv if x.strip()]   # not 'a' - that is the ASCII helper
    blob = " ".join(argv)
    auto = set()
    auto.update(re.findall(r"ORA-\d{4,5}", blob, re.I))
    auto.update(re.findall(r"EC[A-Z]*-\d+", blob))
    auto.update(re.findall(r"\b(?:FK|PK|UK|CK)_[A-Z0-9_]{4,}", blob))
    auto.update(t for t in re.findall(r"\b[A-Z][A-Z0-9]{2,}(?:_[A-Z0-9]+){1,}\b", blob) if len(t) > 6)
    for t in sorted(auto):
        if not any(t.lower() == x.lower() for x in terms):
            terms.append(t)
    return terms


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    terms = terms_from(sys.argv[1:])
    print("STEP 0 - already-seen check")
    print(a("  terms: %s" % ", ".join(repr(t) for t in terms)))

    hits = []
    for p in files():
        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        for n, line in enumerate(lines, 1):
            low = line.lower()
            for t in terms:
                if t.lower() in low:
                    hits.append((p.relative_to(ROOT).as_posix(), n, t, line.strip()[:150]))
                    break

    if not hits:
        print("\n  NO prior record found for these terms -> new ground, a fresh scan is justified.")
        print("  (Write what you find back into ec-ui-knowledge/ in the SAME session.)")
        return 0

    by_file = {}
    for f, n, t, txt in hits:
        by_file.setdefault(f, []).append((n, t, txt))
    print("\n  %d hit(s) in %d file(s) - STOP: READ THESE BEFORE ANY LIVE SCAN.\n" % (len(hits), len(by_file)))
    for f in sorted(by_file):
        print(a("  %s" % f))
        for n, t, txt in by_file[f][:8]:
            print(a("      :%-5d [%s] %s" % (n, t, txt)))
        if len(by_file[f]) > 8:
            print(a("      ... +%d more" % (len(by_file[f]) - 8)))
        print("")
    print("  A re-investigation does not just cost tokens - it produces a WORSE answer than the file,")
    print("  and can mis-classify an EC PRODUCT DEFECT as your own knowledge gap.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
