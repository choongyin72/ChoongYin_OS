#!/usr/bin/env python3
"""Repair my own sloppy edit: I injected `"not one\\n"[:0] or "no op"` into NEGATIONS, which strips the
bare substring "no op" and therefore swallowed legitimate signal (Cargo Planning Forecast started
failing). Replace the whole block with a clean, explicit list."""
import re
from pathlib import Path

p = Path(r"C:\Projects\ChoongYin_OS\tmp\check_row_vocab.py")
s = p.read_text(encoding="utf-8")

m = re.search(r"NEGATIONS = \[.*?\]\n", s, re.S)
assert m, "NEGATIONS block not found"

clean = '''NEGATIONS = [
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
'''
s = s[:m.start()] + clean + s[m.end():]
p.write_text(s, encoding="utf-8")
print("NEGATIONS rewritten cleanly (%d entries)" % clean.count('",'))
