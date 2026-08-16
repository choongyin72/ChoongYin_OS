from pathlib import Path
p = Path(r"C:\Projects\ChoongYin_OS\tmp\check_row_vocab.py")
s = p.read_text(encoding="utf-8")

# 1. correction/history phrasings are not defects
old = '''NEGATIONS = ["no cascade", "without cascade", "not ov-gm", "no navigator/go", "no navigator go",
             "unusable", "n/a cascade"]'''
assert s.count(old) == 1, "NEGATIONS not found"
s = s.replace(old, '''NEGATIONS = ["no cascade", "without cascade", "not ov-gm", "no navigator/go", "no navigator go",
             "unusable", "n/a cascade",
             # a line that DESCRIBES the old wrong wording is a CORRECTION or history, not a defect -
             # otherwise fixing a defect would make the gate fail forever
             "was wrong", "claim was", "family text corrected", "does not describe this screen",
             "still said", "wording that does not", "is historical", "shipped with ov-gm wording"]''')

# 2. the helper itself
anchor = "def main():"
assert s.count(anchor) == 1
helper = '''EC = ROOT / "workstreams" / "master-plan" / "ec-automation"


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
            scrub = _strip_negations(line)
            hits = [t for t in FORBIDDEN.get(family, []) if t.lower() in scrub]
            if hits:
                out.append(("%s:%d" % (f.name, n), hits, line.strip()[:110]))
    return out


''' + anchor
s = s.replace(anchor, helper)
p.write_text(s, encoding="utf-8")
print("helper + negations added")
