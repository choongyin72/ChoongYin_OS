"""Build the final grouped summary of the Assets screen scan:
- per-type counts and per-section breakdown
- OTHER bucket sub-grouped by URL family for later processing
Writes tmp/screen_scan/assets_scan_summary.md (final form) and prints a
compact report."""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

J = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/assets_scan.json")
OUT = J.parent / "assets_scan_summary.md"
data = json.loads(J.read_text(encoding="utf-8"))

def urlfam(u):
    m = re.match(r"https://[^/]+/[^/]+/([^/?]+)", u or "")
    return m.group(1) if m else "?"


def mdtable(header, rows):
    """Render a markdown table with pipe-aligned fixed-width columns."""
    srows = [[str(c) for c in r] for r in [header] + rows]
    widths = [max(len(r[i]) for r in srows) for i in range(len(header))]
    def fmt(r):
        return "| " + " | ".join(r[i].ljust(widths[i]) for i in range(len(r))) + " |"
    sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
    return [fmt(srows[0]), sep] + [fmt(r) for r in srows[1:]]

by_type = defaultdict(list)
for k, r in data.items():
    t = r.get("type", "ERROR") if r.get("status") == "ok" else "ERROR"
    by_type[t].append(r)

sec_counts = defaultdict(Counter)
for t, rows in by_type.items():
    for r in rows:
        sec_counts[r["section"]][t] += 1

lines = [
    "# Configuration > Assets — screen classification (FINAL)",
    "",
    f"App: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/ | scanned read-only | {len(data)} screens, 29 sub-sections",
    "",
    "## Headline counts",
    "",
]
lines += mdtable(
    ["Type", "Count", "Template", "Ready?"],
    [
        ["OV", len(by_type["OV"]), "Bank / Equipment (manage_object)", "yes — T2 exists"],
        ["TV", len(by_type["TV"]), "MIME / Language (table class)", "yes — T2 exists"],
        ["OV-variant", len(by_type["OV-variant"]), "navigator+grid custom URL", "likely — recon first screen"],
        ["OTHER", len(by_type["OTHER"]), "none yet", "parked for later process"],
        ["ERROR", len(by_type["ERROR"]), "search nav failed (flaky)", "re-probe manually"],
    ],
)
lines += ["", "## Per-section breakdown", ""]
sec_rows = []
for sec in sorted(sec_counts):
    c = sec_counts[sec]
    sec_rows.append([sec, c["OV"], c["TV"], c["OV-variant"], c["OTHER"], c["ERROR"], sum(c.values())])
tot_row = ["TOTAL"] + [sum(r[i] for r in sec_rows) for i in range(1, 7)]
lines += mdtable(["Section", "OV", "TV", "OV-variant", "OTHER", "ERROR", "Total"], sec_rows + [tot_row])
lines += [""]

lines += ["", "## Screens by type", ""]
for t in ("OV", "TV", "OV-variant"):
    lines.append(f"### {t} ({len(by_type[t])})")
    lines.append("")
    for r in sorted(by_type[t], key=lambda r: (r["section"], r["screen"])):
        lines.append(f"- {r['section']} :: **{r['screen']}** — {r['confidence']} ({r['why']})")
    lines.append("")

lines.append(f"### OTHER ({len(by_type['OTHER'])}) — parked, grouped by URL family")
lines.append("")
fams = defaultdict(list)
for r in by_type["OTHER"]:
    fams[urlfam(r.get("url", ""))].append(r)
for fam, rows in sorted(fams.items(), key=lambda kv: -len(kv[1])):
    lines.append(f"**{fam}** ({len(rows)})")
    for r in sorted(rows, key=lambda r: (r["section"], r["screen"])):
        lines.append(f"- {r['section']} :: {r['screen']}")
    lines.append("")

if by_type["ERROR"]:
    lines.append("### ERROR — manual re-probe needed")
    for r in by_type["ERROR"]:
        lines.append(f"- {r['section']} :: {r['screen']} ({r.get('why','')})")

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"written -> {OUT}")
print("\nPer-section (OV/TV/OVvar/OTHER):")
for sec in sorted(sec_counts):
    c = sec_counts[sec]
    print(f"  {sec:32s} {c['OV']:3d} {c['TV']:3d} {c['OV-variant']:3d} {c['OTHER']:3d}")
print("\nTop OTHER families:")
for fam, rows in sorted(fams.items(), key=lambda kv: -len(kv[1]))[:8]:
    print(f"  {len(rows):3d}  {fam}")
