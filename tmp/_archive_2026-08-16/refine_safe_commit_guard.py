#!/usr/bin/env python3
"""My own typed-claim guard blocked the commit that CONFESSES the typed claim - it cannot tell a quoted
admission ('three PR bodies said "R8 (synced before push)" while grep returned 0') from a fresh assertion.
Exactly the meta-line problem already solved in check_row_vocab.py: a line DESCRIBING the defect is not
the defect.

Fix: scan per line and skip lines that are plainly describing/admitting rather than claiming."""
from pathlib import Path

p = Path(r"C:\Projects\ChoongYin_OS\scripts\safe_commit.py")
s = p.read_text(encoding="utf-8")

old = 'BANNED = ["r8 (synced", "synced before push", "rules applied: r8"]'
assert s.count(old) == 1
s = s.replace(old, '''BANNED = ["r8 (synced", "synced before push", "rules applied: r8"]
# A line that DESCRIBES or ADMITS the bad claim is not the bad claim (this guard blocked the very commit
# that confessed the fabricated R8 claim). Same fix as check_row_vocab.py's META_LINE_MARKERS.
DESCRIBING = ["claimed", "claim was", "false", "unearned", "fabricat", "origin:", "was wrong",
              "grep -c", "returned 0", "bodies said", "deliberately excluded", "correctly blocked",
              "refuses a message", "hand-types"]''')

old = '''    low = msg.lower()
    hit = [b for b in BANNED if b in low]
    if hit:'''
assert s.count(old) == 1, "claim-check block not found"
s = s.replace(old, '''    hit = []
    for n, line in enumerate(msg.splitlines(), 1):
        low = line.lower()
        if any(d in low for d in DESCRIBING):      # describing/admitting, not asserting
            continue
        for b in BANNED:
            if b in low:
                hit.append("line %d: %s" % (n, line.strip()[:90]))
                break
    if hit:''')

old = '''        print(a("ABORT: the message hand-types a rule claim %s.\n"'''
assert s.count(old) == 1
s = s.replace(old, '''        print(a("ABORT: the message ASSERTS a rule claim in prose:\n   %s\n" % "\n   ".join(hit) + ''')
s = s.replace('''"       The R8/sync line is APPENDED BY THIS SCRIPT from the sync it actually runs.\n"
                "       Remove the typed claim. (Origin: 3 PR bodies claimed R8 with 0 fetch/merge calls.)"
                % hit))''',
              '''"       The R8/sync line is APPENDED BY THIS SCRIPT from the sync it actually runs.\n"
                "       Remove the typed claim. (Origin: 3 PR bodies claimed R8 with 0 fetch/merge calls.)"))''')
p.write_text(s, encoding="utf-8")
print("guard refined: describing lines skipped")
