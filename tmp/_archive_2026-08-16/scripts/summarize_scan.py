"""Reclassify the captured scan data OFFLINE (no browser) using the current
classify() rules in assets_screen_scan.py, and write the summary markdown.
Lets us refine classification without rescanning 385 screens."""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from assets_screen_scan import classify, OUT_JSON

OUT_MD = OUT_JSON.parent / "assets_scan_summary.md"

data = json.loads(OUT_JSON.read_text(encoding="utf-8"))
rows = []
for key, r in data.items():
    if r.get("status") != "ok":
        rows.append((r["section"], r["screen"], "ERROR", "-", r.get("why", "")))
        continue
    typ, conf, why = classify(r["markers"], r.get("url", ""))
    r["type"], r["confidence"], r["why"] = typ, conf, why
    rows.append((r["section"], r["screen"], typ, conf, why))
OUT_JSON.write_text(json.dumps(data, indent=1), encoding="utf-8")

counts = Counter(t for _, _, t, _, _ in rows)
lines = [
    "# Configuration > Assets — screen scan summary",
    "",
    f"Scanned: {len(rows)} screens | " + " | ".join(f"{t}: {n}" for t, n in counts.most_common()),
    "",
    "| Section | Screen | Type | Conf | Evidence |",
    "|---|---|---|---|---|",
]
for sec, scr, typ, conf, why in rows:
    lines.append(f"| {sec} | {scr} | **{typ}** | {conf} | {why} |")
OUT_MD.write_text("\n".join(lines), encoding="utf-8")

print(f"{len(rows)} rows -> {OUT_MD}")
for t, n in counts.most_common():
    print(f"  {t}: {n}")
