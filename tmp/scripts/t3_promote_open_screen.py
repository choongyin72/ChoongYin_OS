"""Rewrite every T3 'Open <X> Screen' body from the 3-step copy-paste
(Open EC Browser / Login To EC / Navigate To Screen) to a one-line delegation
to the new T1 keyword Launch EC And Open Screen (common.resource).

Only rewrites the EXACT canonical body; anything customized is left alone and listed.
"""
import re
from pathlib import Path

PO = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/pageobjects")

# canonical body: args line, then the 3 steps (allowing the screen-name var to differ)
PATTERN = re.compile(
    r"(    \[Arguments\]    \$\{user\}=\$\{EC_USER\}    \$\{pass\}=\$\{EC_PASS\}\n)"
    r"    Open EC Browser\n"
    r"    Login To EC    \$\{user\}    \$\{pass\}\n"
    r"    Navigate To Screen    (\$\{[A-Z0-9_]+\})"
)

changed, skipped = [], []
for f in sorted(PO.rglob("*.resource")):
    text = f.read_text(encoding="utf-8")
    if "Open EC Browser" not in text:
        continue
    new, n = PATTERN.subn(
        lambda m: m.group(1) + f"    Launch EC And Open Screen    {m.group(2)}    ${{user}}    ${{pass}}",
        text)
    if n:
        f.write_text(new, encoding="utf-8")
        changed.append((str(f.relative_to(PO)), n))
    else:
        skipped.append(str(f.relative_to(PO)))

print(f"rewritten: {len(changed)} files")
for rel, n in changed:
    print(f"  {rel}  ({n} occurrence)")
print(f"\nfiles containing 'Open EC Browser' NOT matching canonical pattern: {len(skipped)}")
for rel in skipped:
    print(f"  !! {rel}")
