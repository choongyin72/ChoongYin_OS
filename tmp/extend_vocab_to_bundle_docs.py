#!/usr/bin/env python3
"""Close the hole that let the #265/#278/#283 defect class survive: check_row_vocab.py only ever
validated the registry + scorecard ROWS, so wrong-family wording lived on undetected in each bundle's
CHECKLIST.md / JOURNAL.md and in the KB map (ec-ui-knowledge/screens/<slug>.md). That is exactly where
today's Report Group audit found it, and where the 6 already-merged screens were wrong.

This adds those three files to the same validator, so hygiene (gate 16 inside verify_screen) now covers
them for every screen in docs/screen_families.json.

Correction notes and history are NOT defects: a line that describes the old wrong wording (e.g. "this
bundle shipped with OV-GM wording ...", Trailer's #278 story, "the ... claim was WRONG") must not trip
the check, or fixing a defect would make the gate fail forever.
"""
from pathlib import Path

p = Path(r"C:\Projects\ChoongYin_OS\tmp\check_row_vocab.py")
s = p.read_text(encoding="utf-8")

old = 'NEGATIONS = ["no cascade", "without cascade", "not ov-gm", "no navigator/go", "no navigator go",\n             "unusable", "n/a cascade"]'
assert s.count(old) == 1, "NEGATIONS block not found"
s = s.replace(old, old[:-1] + ',\n'
              '             # a line that DESCRIBES the old wrong wording is a correction, not a defect\n'
              '             "was wrong", "claim was", "family text corrected", "does not describe this screen",\n'
              '             "still said", "wording that does not", "is historical", "shipped with ov-gm wording"]')

# ---- scan the bundle docs + KB map in addition to the rows -------------------------------------
anchor = "def main("
assert s.count(anchor) == 1, "main() not found"
helper = '''EC = ROOT / "workstreams" / "master-plan" / "ec-automation"


def bundle_doc_mismatches(screen, family):
    """CHECKLIST.md / JOURNAL.md / KB map - the files the row-only check never looked at."""
    out = []
    folder = screen.replace(" ", "_")
    targets = []
    for d in EC.rglob(folder):
        if d.is_dir():
            targets += [d / "CHECKLIST.md", d / "JOURNAL.md"]
    kb = ROOT / "ec-ui-knowledge" / "screens" / (folder.lower() + ".md")
    targets.append(kb)
    for f in targets:
        if not f.is_file():
            continue
        for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if not line.strip():
                continue
            scrub = _strip_negations(line)
            bad = [t for t in FORBIDDEN.get(family, []) if t.lower() in scrub]
            if bad:
                out.append(("%s:%d" % (f.name, n), bad, line.strip()[:120]))
    return out


''' + anchor
s = s.replace(anchor, helper)

# ---- report them from main() -------------------------------------------------------------------
import re as _re
m = _re.search(r"\n(\s*)return 0\n", s)
assert m, "main()'s success return not found"
ind = m.group(1)
inject = ("\n%sdocfails = bundle_doc_mismatches(screen, family)\n"
          "%sif docfails:\n"
          "%s    print('MISMATCH (bundle docs) - family %%r:' %% family)\n"
          "%s    for where, bad, line in docfails:\n"
          "%s        print('   %%-22s forbidden %%s | %%s' %% (where, bad, line))\n"
          "%s    return 1\n"
          "%sreturn 0\n") % (ind, ind, ind, ind, ind, ind, ind)
s = s[:m.start()] + inject + s[m.end():]
p.write_text(s, encoding="utf-8")
print("check_row_vocab.py now validates CHECKLIST.md / JOURNAL.md / KB map too")
