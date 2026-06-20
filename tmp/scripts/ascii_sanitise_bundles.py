"""R20 one-off: ASCII-normalise EC Playwright bundle + recon .py files.

Scans screens/**/playwright/*.py and screens/**/investigation/*.py, replaces a KNOWN set of non-ASCII
chars with ASCII equivalents (em/en dashes, box-drawing, arrows, check/cross, smart quotes, etc.). Any
non-ASCII char NOT in the map is reported and the file is left untouched-for-that-char (no silent mangle),
so it can be handled deliberately. Run: py -X utf8 tmp/scripts/ascii_sanitise_bundles.py
"""
import os
from pathlib import Path

ROOT = Path(os.environ.get("REPO_ROOT") or Path(__file__).resolve().parents[2])
SCREENS = ROOT / "workstreams" / "master-plan" / "ec-automation" / "screens"

MAP = {
    "—": "-", "–": "-", "‒": "-", "―": "-", "−": "-",
    "─": "-", "━": "-", "│": "|", "┃": "|",
    "┌": "+", "┐": "+", "└": "+", "┘": "+",
    "├": "+", "┤": "+", "┬": "+", "┴": "+", "┼": "+",
    "→": "->", "←": "<-", "↑": "^", "↓": "v", "⇒": "=>",
    "✓": "OK", "✔": "OK", "✅": "OK", "✗": "X", "✘": "X",
    "❌": "X", "❗": "!", "⚠": "(!)", "️": "",
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "…": "...", "•": "*", "·": ".", " ": " ",
    "°": " deg", "×": "x", "÷": "/", "±": "+/-",
    "≈": "~", "≠": "!=", "≤": "<=", "≥": ">=",
    "✅": "OK", "➜": "->", "▶": ">", "▪": "-", "→": "->",
}


def main():
    if not SCREENS.exists():
        print(f"screens dir not found: {SCREENS}")
        return
    files = sorted(SCREENS.glob("**/playwright/*.py")) + sorted(SCREENS.glob("**/investigation/*.py"))
    changed, unmapped = [], []
    for f in files:
        text = f.read_text(encoding="utf-8")
        new = text
        for k, v in MAP.items():
            new = new.replace(k, v)
        # report any remaining non-ASCII (unmapped) per line
        leftover = []
        for n, line in enumerate(new.splitlines(), 1):
            for ch in line:
                if ord(ch) > 127:
                    leftover.append((n, ch, f"U+{ord(ch):04X}"))
        if leftover:
            unmapped.append((f.relative_to(ROOT), leftover))
        if new != text:
            f.write_text(new, encoding="utf-8")
            changed.append(f.relative_to(ROOT))
    print(f"scanned {len(files)} file(s); rewrote {len(changed)}")
    for c in changed:
        print(f"  fixed: {c}")
    if unmapped:
        print(f"\n(!) {len(unmapped)} file(s) still have UNMAPPED non-ASCII (left for manual review):")
        for rel, lst in unmapped:
            for n, ch, code in lst[:20]:
                print(f"   {rel}:{n}: {code} {ch!r}")
    else:
        print("\nRESULT: all bundle/recon .py are now pure ASCII")


if __name__ == "__main__":
    main()
