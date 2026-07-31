#!/usr/bin/env python3
"""Family-vocabulary validator for registry + scorecard rows (issue #278).

WHY: a count-asserted string replace only proves the text I *intended* LANDED - it cannot prove the
text is CORRECT. Twice now an OV-GM template phrase ("cascade + GO", "groupmodel", "Op PU",
manageObject grid) shipped on a screen that is NOT OV-GM, past both a sibling column-diff and a
count-assert. This check greps the row for family-INAPPROPRIATE vocabulary, which catches
"present but wrong".

Usage:  py tmp/check_row_vocab.py "<Screen Name>" <family>
        family = ovgm | plain | custom | tv
Exit 0 = clean, 1 = mismatch found (prints each offending token + the row).
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(r"C:\Projects\ChoongYin_OS")
REG = ROOT / "workstreams" / "master-plan" / "ec-automation" / "docs" / "ec_screen_registry.md"
SC = ROOT / "docs" / "automation-scorecard.md"

# tokens that must NOT appear for a given family
FORBIDDEN = {
    "plain":  ["cascade", "groupmodel", "OV-GM", "Op PU", "Op Production Unit",
               "manageObject:form:T_data", "navigator-GATED", "gated-navigator"],
    "custom": ["cascade", "groupmodel", "OV-GM", "Op PU", "Op Production Unit",
               "manageObject:form:T_data", "navigator-GATED", "gated-navigator"],
    "tv":     ["cascade", "groupmodel", "OV-GM", "Op PU", "navigator-GATED", "gated-navigator"],
    "ovgm":   ["date-only navigator", "no navigator", "custom-URL"],
    # gated screens whose navigator uses PER-FIELD groups (G:1..G:N) rather than a single-row cascade,
    # usually with a custom grid id - e.g. Cargo Planning Forecast, Well Bore, Perforation Interval
    "gatedpf": ["date-only navigator", "no navigator", "custom-URL", "groupmodel"],
}
# tokens that SHOULD appear (at least one) for a given family - a weak positive signal
EXPECTED_ANY = {
    "plain":  ["PLAIN OV", "plain OV", "Bank family", "date-only navigator"],
    "custom": ["custom-URL", "Custom-URL", "no navigator"],
    "tv":     ["TV-style", "TV ", "table-class"],
    "ovgm":   ["OV-GM", "groupmodel", "cascade"],
    "gatedpf": ["PER-FIELD", "per-field", "nav groups"],
}

# negated phrasings are legitimate ("date-only navigator + GO (no cascade)") - strip before scanning
NEGATIONS = [
    # NEGATED phrasings are legitimate: "date-only navigator + GO (no cascade)" must not trip 'cascade'
    "no cascade", "without cascade", "not ov-gm", "no navigator/go", "no navigator go",
    "unusable", "n/a cascade",
    "no op pu gating", "no op pu to satisfy", "no op pu.", "no op pu,", "and no op pu",
    "no op production unit",
    # a line that DESCRIBES the old wrong wording is a CORRECTION or history, not a defect - without
    # these, fixing a defect would make the gate fail forever
    "was wrong", "claim was", "family text corrected", "does not describe this screen",
    "still said", "wording that does not", "is historical", "shipped with ov-gm wording",
]


# A line that is ABOUT the old wrong wording (a correction note, or history describing a past defect)
# must be SKIPPED WHOLE - substring-scrubbing cannot help when e.g. the branch NAME itself contains
# 'ov-gm'. Without this, fixing a defect would keep the gate red forever.
META_LINE_MARKERS = [
    "family text corrected", "claim was wrong", "branch name is historical", "still said",
    "does not describe this screen", "was WRONG", "shipped with ov-gm wording",
]


def is_meta_line(line):
    low = line.lower()
    return any(m.lower() in low for m in META_LINE_MARKERS)


def _strip_negations(row):
    low = row.lower()
    for n in NEGATIONS:
        low = low.replace(n, "")
    return low


def rows_for(screen):
    out = []
    for label, path in (("registry", REG), ("scorecard", SC)):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            s = line.strip()
            # EXACT first-cell match: a prefix test lets 'Pilot' pick up 'Pilot Boat' rows and
            # could report another screen's family as a mismatch.
            if not s.startswith("|"):
                continue
            cells = [x.strip() for x in s.split("|")[1:]]
            if not cells:
                continue
            first = cells[0]
            base = first.split("(")[0].strip()          # 'Truck (plain OV, CO.0264)' -> 'Truck'
            if base == screen:
                out.append((label, s))
    return out

EC = ROOT / "workstreams" / "master-plan" / "ec-automation"


def bundle_doc_mismatches(screen, family):
    """CHECKLIST.md / JOURNAL.md / KB map - the files the row-only check never looked at, and exactly
    where #265/#278/#283's wrong-family wording survived undetected on 6 merged screens."""
    out = []
    folder = screen.replace(" ", "_")
    targets = []
    for d in EC.rglob(folder):
        if d.is_dir():
            targets += [d / "CHECKLIST.md", d / "JOURNAL.md"]
    targets.append(ROOT / "ec-ui-knowledge" / "screens" / (folder.lower() + ".md"))
    for f in targets:
        if not f.is_file():
            continue
        for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if not line.strip():
                continue
            if is_meta_line(line):
                continue
            scrub = _strip_negations(line)
            hits = [t for t in FORBIDDEN.get(family, []) if t.lower() in scrub]
            if hits:
                out.append(("%s:%d" % (f.name, n), hits, line.strip()[:110]))
    return out


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    screen, family = sys.argv[1], sys.argv[2].lower()
    if family not in FORBIDDEN:
        print("unknown family %r (use: %s)" % (family, "|".join(FORBIDDEN)))
        return 2
    found = rows_for(screen)
    if not found:
        print("FAIL: no registry/scorecard row found for %r" % screen)
        return 1
    bad = False
    for label, row in found:
        scan = _strip_negations(row)
        hits = [t for t in FORBIDDEN[family] if t.lower() in scan]
        if hits:
            bad = True
            print("MISMATCH (%s) - forbidden for family %r: %s" % (label, family, hits))
            print("   row: %s" % row[:220])
        if not any(t.lower() in row.lower() for t in EXPECTED_ANY[family]):
            bad = True
            print("MISSING (%s) - no %r vocabulary present (expected one of %s)"
                  % (label, family, EXPECTED_ANY[family]))
            print("   row: %s" % row[:220])
    # the files the ROW-only check never looked at - where the defect class actually survived
    docfails = bundle_doc_mismatches(screen, family)
    if docfails:
        bad = True
        print("MISMATCH (bundle docs) - forbidden for family %r:" % family)
        for where, hits, line in docfails:
            print("   %-22s %s | %s" % (where, hits, line))
    if not bad:
        print("OK: %d row(s) + bundle docs for %r use %r vocabulary consistently"
              % (len(found), screen, family))
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
