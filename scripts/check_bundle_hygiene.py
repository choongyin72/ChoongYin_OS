"""check_bundle_hygiene.py - enforce R16 (no hardcoded creds) + R20 (ASCII-only) on EC Playwright bundles.

Two static gates over screens/**/playwright/*.py and screens/**/investigation/*.py:
  * R16 - a hardcoded credential literal NOT read from the environment is a FAILURE in BUNDLES (exit 1);
    in throwaway investigation/ recon scripts it only WARNs (they should use tmp/scripts/ec_session.py).
  * R20 - ANY non-ASCII byte (em-dash, box-drawing, check/cross, smart quotes...) in EITHER glob is a
    FAILURE. A green test run never catches non-ASCII that hides in a FAIL-only branch or a docstring; it
    detonates as UnicodeEncodeError on a cp1252 (captured/redirected) stream exactly when a regression
    trips that path. So this is a static scan, not a runtime check. Author bundle/recon .py ASCII-clean.

Run in the ec-object-iud-builder verify step (Step 5) and/or CI:
    py scripts/check_bundle_hygiene.py
A line is an R16 violation when it carries a credential literal ('sysadmin'/"sysadmin") or a hardcoded
#username/#password fill, AND the line does not resolve it from env (os.environ / getenv / EC_USER / EC_PASS).
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("REPO_ROOT") or Path(__file__).resolve().parents[1])
SCREENS = ROOT / "workstreams" / "master-plan" / "ec-automation" / "screens"

CRED_LITERAL = re.compile(r"""['"]sysadmin['"]""")
FILL_HARDCODED = re.compile(r"""#(?:username|password)['"]\s*,\s*['"][^'"]+['"]""")
ENV_OK = ("os.environ", "getenv", "EC_USER", "EC_PASS", "ec_session")


def violations_in(path):
    out = []
    for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if any(tok in line for tok in ENV_OK):
            continue
        if CRED_LITERAL.search(line) or FILL_HARDCODED.search(line):
            out.append((n, line.strip()[:90]))
    return out


def non_ascii_in(path):
    out = []
    for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        for col, ch in enumerate(line, 1):
            if ord(ch) > 127:
                out.append((n, col, f"U+{ord(ch):04X} {ch!r}"))
    return out


def main():
    if not SCREENS.exists():
        print(f"[hygiene] screens dir not found: {SCREENS}"); return 0
    bundles = sorted(SCREENS.glob("**/playwright/*.py"))
    recon = sorted(SCREENS.glob("**/investigation/*.py"))
    fails, warns, nonascii = [], [], []
    for f in bundles:
        for ln, txt in violations_in(f):
            fails.append((f.relative_to(ROOT), ln, txt))
    for f in recon:
        for ln, txt in violations_in(f):
            warns.append((f.relative_to(ROOT), ln, txt))
    # R20 - non-ASCII is a FAIL in BOTH globs (bundles + recon)
    for f in bundles + recon:
        for ln, col, code in non_ascii_in(f):
            nonascii.append((f.relative_to(ROOT), ln, col, code))

    print(f"[hygiene] scanned {len(bundles)} bundle(s) + {len(recon)} recon script(s)")
    if warns:
        print(f"\n[hygiene] WARN - {len(warns)} hardcoded-credential line(s) in investigation/ recon scripts "
              f"(use tmp/scripts/ec_session.py):")
        for rel, ln, txt in warns[:40]:
            print(f"   {rel}:{ln}: {txt}")
        if len(warns) > 40:
            print(f"   ... and {len(warns) - 40} more")
    if nonascii:
        print(f"\n[hygiene] FAIL - {len(nonascii)} non-ASCII char(s) in bundle/recon .py (R20 - author ASCII):")
        for rel, ln, col, code in nonascii[:60]:
            print(f"   {rel}:{ln}:{col}: {code}")
        if len(nonascii) > 60:
            print(f"   ... and {len(nonascii) - 60} more")
    if fails:
        print(f"\n[hygiene] FAIL - {len(fails)} hardcoded-credential line(s) in BUNDLES (R16 - use env vars):")
        for rel, ln, txt in fails:
            print(f"   {rel}:{ln}: {txt}")
    if fails or nonascii:
        print("\n[hygiene] RESULT: FAIL")
        return 1
    print("\n[hygiene] RESULT: PASS - no hardcoded creds (R16) and pure ASCII (R20) in all bundles/recon")
    return 0


if __name__ == "__main__":
    sys.exit(main())
