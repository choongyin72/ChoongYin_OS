"""check_bundle_hygiene.py — enforce R16: EC Playwright BUNDLES must never hardcode credentials.

Scans the canonical bundles (screens/**/playwright/ec_iud_*.py): a hardcoded credential literal that is NOT
read from the environment is a FAILURE (exit 1). The throwaway investigation/ recon scripts are scanned too
but only WARN (they should use tmp/scripts/ec_session.py, but they don't gate a release).

Run in the ec-object-iud-builder verify step (Step 5) and/or CI:
    py scripts/check_bundle_hygiene.py
A line is a violation when it carries a credential literal ('sysadmin'/"sysadmin") or a hardcoded
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


def main():
    if not SCREENS.exists():
        print(f"[hygiene] screens dir not found: {SCREENS}"); return 0
    bundles = sorted(SCREENS.glob("**/playwright/*.py"))
    recon = sorted(SCREENS.glob("**/investigation/*.py"))
    fails, warns = [], []
    for f in bundles:
        for ln, txt in violations_in(f):
            fails.append((f.relative_to(ROOT), ln, txt))
    for f in recon:
        for ln, txt in violations_in(f):
            warns.append((f.relative_to(ROOT), ln, txt))

    print(f"[hygiene] scanned {len(bundles)} bundle(s) + {len(recon)} recon script(s)")
    if warns:
        print(f"\n[hygiene] WARN — {len(warns)} hardcoded-credential line(s) in investigation/ recon scripts "
              f"(use tmp/scripts/ec_session.py):")
        for rel, ln, txt in warns[:40]:
            print(f"   {rel}:{ln}: {txt}")
        if len(warns) > 40:
            print(f"   ... and {len(warns) - 40} more")
    if fails:
        print(f"\n[hygiene] FAIL — {len(fails)} hardcoded-credential line(s) in BUNDLES (R16 — use env vars):")
        for rel, ln, txt in fails:
            print(f"   {rel}:{ln}: {txt}")
        print("\n[hygiene] RESULT: FAIL")
        return 1
    print("\n[hygiene] RESULT: PASS - no hardcoded credentials in any bundle")
    return 0


if __name__ == "__main__":
    sys.exit(main())
