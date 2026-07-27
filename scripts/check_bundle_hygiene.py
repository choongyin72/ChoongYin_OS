"""check_bundle_hygiene.py - enforce R16 (no hardcoded creds) + R20 (ASCII-only) on EC Playwright bundles.

Two static gates over screens/**/playwright/*.py, ec-automation/py/*.py (canonical drivers +
shared engine), and screens/**/investigation/*.py:
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
EC = ROOT / "workstreams" / "master-plan" / "ec-automation"
SCREENS = EC / "screens"
PYDIR = EC / "py"   # canonical driver location (drivers + shared engine) - was NOT scanned pre-2026-07-26

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


# --- #237 item 2 guard: a hand-ticked CHECKLIST claim must never contradict the auto-generated
#     VERIFY-REPORT sitting next to it (the #235 failure: CHECKLIST "[x] robocop clean" while
#     VERIFY-REPORT said robocop exit=1 / OVERALL: FAIL). Ticks come from the tools, not the keyboard.
_VR_GATE = re.compile(r"^\s*-\s*\[( |x)\]\s*\*\*(\w+)\*\*\s*(.*?)\s*-", re.I)  # - [x] **10** robocop clean - ...
_VR_OVERALL_FAIL = re.compile(r"OVERALL:\s*FAIL", re.I)
# keywords that identify each gate in a hand-written CHECKLIST line (matched only on [x]-ticked lines).
# NOTE: gate 16 (hygiene) is deliberately EXCLUDED - hygiene's pass/fail is decided BY this very script
# (this contradiction scan is part of it), so cross-checking a "hygiene clean" claim against gate 16 would
# be self-referential/circular (a failing contradiction makes hygiene fail, which then re-flags the claim).
_GATE_KEYWORDS = {
    "10": ["robocop"], "11": ["dryrun", "--dryrun"],
    "12": ["live rf", "rf suite", "n/n live"], "13": ["db ground", "db-verified"],
    "14": ["full i-u-d", "i-u-d"], "15": ["self-clean", "self clean"],
    "pw": ["playwright"],
}


def _ticked(line):
    """True if the line carries a ticked [x] box; False if [ ]; None if no checkbox."""
    if "[x]" in line.lower():
        return True
    if "[ ]" in line:
        return False
    return None


def checklist_contradictions(bundle_dir):
    """Return list of (msg) where a CHECKLIST.md CLAIM contradicts the auto-generated VERIFY-REPORT.md.
    Only positive (ticked / asserted) CHECKLIST claims count - an honest '[ ] ... pending' line is fine."""
    chk = bundle_dir / "CHECKLIST.md"
    vr = bundle_dir / "VERIFY-REPORT.md"
    if not (chk.exists() and vr.exists()):
        return []
    vr_txt = vr.read_text(encoding="utf-8", errors="replace")
    chk_lines = chk.read_text(encoding="utf-8", errors="replace").splitlines()
    failed = [m.group(2).lower() for line in vr_txt.splitlines()
              for m in [_VR_GATE.match(line)] if m and m.group(1) != "x"]
    overall_fail = bool(_VR_OVERALL_FAIL.search(vr_txt))
    out = []
    # (a) OVERALL: FAIL report must not sit under a CHECKLIST line that POSITIVELY claims OVERALL PASS
    #     (a ticked [x] line, or an unboxed assertion). An explicit '[ ] ... OVERALL PASS - pending' is honest.
    if overall_fail:
        for line in chk_lines:
            if re.search(r"OVERALL\s*PASS", line, re.I) and _ticked(line) is not False:
                out.append("VERIFY-REPORT says OVERALL: FAIL but CHECKLIST positively claims OVERALL PASS")
                break
    # (b) per-gate: a failed VERIFY-REPORT gate must not be [x]-ticked in CHECKLIST - match by gate number
    #     OR by the gate's keyword (e.g. '[x] robocop clean' while gate 10 robocop failed).
    for gid in failed:
        if gid == "16":     # hygiene gate is self-referential (see _GATE_KEYWORDS note) - never cross-check it
            continue
        hit = False
        for line in chk_lines:
            if _ticked(line) is not True:
                continue
            low = line.lower()
            if re.search(r"\[x\]\s*\*{0,2}" + re.escape(gid) + r"\b", low) or \
               any(kw in low for kw in _GATE_KEYWORDS.get(gid, [])):
                hit = True
                break
        if hit:
            out.append(f"gate {gid} failed in VERIFY-REPORT but is [x]-ticked/claimed clean in CHECKLIST")
    return out


def main():
    if not SCREENS.exists():
        print(f"[hygiene] screens dir not found: {SCREENS}"); return 0
    # BUNDLES (R16 FAIL + R20 FAIL): legacy screens/**/playwright/ AND the canonical ec-automation/py/
    # driver + shared-engine location (added 2026-07-26 - drivers moved to py/ but the glob never followed).
    bundles = sorted(SCREENS.glob("**/playwright/*.py"))
    if PYDIR.exists():
        bundles += sorted(PYDIR.glob("*.py"))
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

    # #237 item 2 - CHECKLIST vs VERIFY-REPORT contradiction scan over every bundle dir
    contradictions = []
    for vr in sorted(SCREENS.glob("**/VERIFY-REPORT.md")):
        for msg in checklist_contradictions(vr.parent):
            contradictions.append((vr.parent.relative_to(ROOT), msg))

    print(f"[hygiene] scanned {len(bundles)} bundle(s) + {len(recon)} recon script(s)")
    if contradictions:
        print(f"\n[hygiene] FAIL - {len(contradictions)} CHECKLIST/VERIFY-REPORT contradiction(s) "
              f"(#237 item 2 - ticks must match the auto-generated report):")
        for rel, msg in contradictions:
            print(f"   {rel}: {msg}")
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
    if fails or nonascii or contradictions:
        print("\n[hygiene] RESULT: FAIL")
        return 1
    print("\n[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT contradictions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
