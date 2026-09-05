# R07.001 — Defect Round 01 — owner-reported list

**Stage 1 (collecting).** Owner is listing; nothing verified, nothing changed.
Protocol: LIST → GO (I verify + present) → PROCEED (I fix).

Reported 2026-09-01 with an annotated screenshot of **page 1, Health, Safety & Environment**
(red circles marking each location).

| # | Location | Reported defect |
|---|---|---|
| 1 | 1st CPF table ↔ 1st FPSO table (circle at "Security events" / FPSO header boundary) | The two grid tables sit too close — they look connected to each other. **Add a narrow space gap between the two grid tables.** |
| 2 | 1st FPSO table, Comments column (circle at the far-right edge, header row) | The Comments **column header's right borderline is not aligned** with the right borderline of its data rows below. |
| 3 | 2nd CPF table and 2nd FPSO table (circles at "Main facility" in both) | The **column header row is not connected to its data row** — in both the 2nd CPF and the 2nd FPSO grid tables. |

Note on numbering: the owner's first message numbered its items 1, 2, 2 — renumbered 1–3 here,
no items merged or dropped.

## Page 2

Reported 2026-09-01, annotated screenshot (circle spanning the "Name" header / "MMA Brewster"
data-row boundary).

| # | Location | Reported defect |
|---|---|---|
| 4 | Page 2, **Support Vessels** section | The **column header row is not connected to its data row**. (Same class as #3.) |

## Page 3

Reported 2026-09-01, annotated screenshot with a circle at **every** column boundary on the
header/data junction (Area|Tag, Tag|Work Order, Work Order|Plan, Plan|Priority,
Priority|Risk, Risk|Description).

| # | Location | Reported defect |
|---|---|---|
| 5 | Page 3, **Production Risks for CPF** grid table | The column header row and data row **borderlines are not jointed perfectly** — the vertical column lines do not meet across the header/data boundary. Circled at every column boundary, so it is the whole header row, not one column. |

## Page 5

Reported 2026-09-01, annotated screenshot, circles again at every column boundary on the
header/data junction. Owner: "similar issues as in Page 3".

| # | Location | Reported defect |
|---|---|---|
| 6 | Page 5, **Production Risks for FPSO** grid table | Same as #5 — column header row and data row **borderlines not jointed perfectly** across the whole header row. Owner explicitly ties this to #5, so expect a shared root cause. |

## Pages 6 and 7

Reported 2026-09-01, two annotated screenshots — page 6 (Marcus Wicks) and page 7
(John Spencer) — circles at the table's right edge.

| # | Location | Reported defect |
|---|---|---|
| 8 | Pages **6 and 7**, Comments tables (both the purple section band and the Comment/Author header row) | The **last (right-most) borderline of the column header rows is not aligned with the data rows' right borderline.** Two screenshots supplied: page 6 (Marcus Wicks) and page 7 (John Spencer), circles at the table's right edge showing the purple header bands and the data-row right border ending at different x. Owner says the same issue on both pages. <br>**Same class as #2** (page 1 FPSO Comments header right border) — expect a shared root cause. |

## Cross-page (pages 2–5)

Reported 2026-09-01, annotated screenshot of page 2 Major Equipment Status for CPF (circle
around the "Utilities" values in the first column, against the table's left border).

| # | Location | Reported defect |
|---|---|---|
| 7 | **First column data values sit too near the left borderline**, in SIX sections: <br>• page 2 — Major Equipment Status for CPF <br>• page 3 — Production Risks for CPF <br>• page 4 — Major Equipment Status for FPSO <br>• page 5 — Production Risks for FPSO <br>• page 5 — Consumables for CPF <br>• page 5 — Consumables for FPSO | The first-column data value is too close to the table's left border — needs left padding / indent to match the reference. One defect, six locations; owner listed the sections explicitly. |

---

## How these 8 items group

Owner's read: "its not so many defects" — agreed. The 8 reported items collapse into **4
symptom groups**, which is what makes the list short even though it spans 7 pages:

| Group | Items | Symptom |
|---|---|---|
| A | 3, 4, 5, 6 | Column header row not joined to its data row (vertical lines don't meet across the header/data boundary) |
| B | 2, 8 | Header row's right-most borderline not aligned with the data rows' right borderline |
| C | 7 | First-column data value too close to the table's left border (6 sections) |
| D | 1 | Two adjacent tables touching — need a narrow gap between them |

Whether each group is really ONE root cause is a claim to be tested at GO, not assumed —
grouping by symptom is not the same as grouping by cause, and on R07.006 a single
"thickness" symptom turned out to have two separate causes.

---

# STAGE 2 — VERIFICATION RESULTS (owner said GO, 2026-09-01)

**All 8 items measured. All 8 are CONFIRMED REAL DEFECTS. None was a check artifact.**
Every item was measured in the generated PDF *and* in the reference the same way. Nothing has
been changed — awaiting **PROCEED**.

## Confirmed measurements

### Group A — header row not joined to its data row (items 3, 4, 5, 6)

| Item | Location | REF vertical gap | GEN vertical gap | GEN vertical's x vs header boundary |
|---|---|---|---|---|
| 3 | p1 2nd CPF | 346.50→347.00 = **0.50pt** | 346.00→347.00 = **1.00pt** | +0.50pt |
| 3 | p1 2nd FPSO | 391.35→391.85 = **0.50pt** | 391.00→392.00 = **1.00pt** | +0.50pt |
| 4 | p2 Support Vessels | 716.70→730.50 = **0.65pt** | 717.00→730.00 = **0.00pt** | −0.50pt |
| 5 | p3 Production Risks CPF | 174.25→174.75 = **0.50pt** | 174.00→175.00 = **1.00pt** | +0.50pt |
| 6 | p5 Production Risks FPSO | 174.25→174.75 = **0.50pt** | 174.00→175.00 = **1.00pt** | +0.50pt |

### Group B — header's right borderline not aligned with data rows (items 2, 8)

| Item | Location | header rect right edge | data-row vertical x | offset |
|---|---|---|---|---|
| 2 | p1 1st FPSO Comments | REF 805.05 / GEN 805.00 | REF 805.00 / GEN 805.50 | REF 0.05 → **GEN 0.50pt** |
| 8 | p6 Comments | REF 810.25 / GEN 810.00 | REF 810.60 / GEN 811.50 | REF 0.35 → **GEN 1.50pt** |
| 8 | p7 Comments | REF 812.75 / GEN 812.00 | REF 812.65 / GEN 813.50 | REF 0.10 → **GEN 1.50pt** |

Item 8 has a **second component**: my purple fill overhangs its own border rect on the right
(p7 fill 813.00 vs rect 812.00; p6 fill 811.00 vs rect 810.00 — 1pt of purple past the border
line), where the reference insets the fill 0.5pt *inside* the rect. That is the notch visible
in the owner's screenshots.

### Group D — adjacent tables touching (item 1)

| | CPF table bottom | separator rule | FPSO header top | rule→table | rule→header |
|---|---|---|---|---|---|
| REF | 238.05 | 238.55 | 241.40 | **0.50pt** | **2.85pt** |
| GEN | 238.00 | 239.50 | 241.00 | 1.50pt | 1.50pt |

In Crystal the rule sits tight against the CPF table and clear of the FPSO header, so it reads
as *closing* the CPF table. Mine is centred between the two, so it reads as belonging to the
FPSO header — that is the "looks connected" symptom.

### Group C — first-column value too near the left border (item 7)

| Section | REF inset | GEN inset | delta |
|---|---|---|---|
| p2 Major Equipment Status for CPF | 1.20pt | **−0.76pt** | −1.96 |
| p3 Production Risks for CPF | 2.20pt | 0.54pt | −1.66 |
| p4 Major Equipment Status for FPSO | 1.20pt | **−0.76pt** | −1.96 |
| p5 Production Risks for FPSO | 2.20pt | 0.54pt | −1.66 |
| p5 Consumables for CPF | 1.55pt | 0.54pt | −1.01 |
| p5 Consumables for FPSO | 1.55pt | 0.54pt | −1.01 |

Negative inset = the text starts **left of the border line**, i.e. touching/overlapping it.

---

## ROOT CAUSES — 8 items, only 2 causes

Both were confirmed in the source, not inferred from the symptom.

### Cause 1 — a `kind="line"` element renders its stroke CENTRED, a rectangle border does not
Explains items **1, 2, 3, 4, 5, 6, 8** — seven of the eight.

`<element kind="line" x="-1" width="1">` occupies local −1..0 (abs 23..24) and JasperReports
draws the 1pt stroke across that whole box, so it renders **centred at abs 23.50**. A
`rectangle`'s border at the same nominal x renders **on the edge, at 23.00**. Verified on
pages 1, 3, 5, 6 and 7 — every traced vertical renders at nominal + 0.5.

**The report has 402 vertical line elements and 516 line elements in total**, so this is
systemic, not local to the reported tables. The same +0.5 applies *downward* to horizontal
rules, which is what pushes item 1's separator rule low.

Compounded by integer rounding: coordinates are traced with `round()`, adding up to ±0.5pt.
Item 1 is the clearest case — reference rule at 238.55 → rounds to 239 (+0.45) → renders at
239.50 (+0.5) = 0.95pt low. Items 4 and 8 likewise combine a 1pt rounding difference with the
0.5pt centring, which is why their offsets are 0.5 and 1.5 rather than uniformly 0.5.

Note for the fix: Part Z9 records that JasperReports 7.0.3 **rejects decimal element
coordinates**, so `x="22.5"` is not available. The fix has to be either a nominal shift or
drawing these edges as rectangle borders instead of lines.

### Cause 2 — the generator subtracts 1 from every text x
Explains item **7**.

`gen_001.py` emits text at `x = int(round(x0 - LEFT)) - 1`. That `-1` was added as slack so
JasperReports could not clip glyphs (Part F1), paired with `width + 6`. But it shifts **every
one of the 1242 text elements 1pt left**.

Verified on two independent texts:
- ref `Utilities` x 24.30 → local 0.30 → round 0 → −1 → abs **23.00** = measured gen 23.00
- ref `Health, Safety & Environment` x 22.65 → local −1.35 → round −1 → −2 → abs **22.00**
  = measured gen 22.00

Scope: all 1242 texts are 1pt left, but it is only *visible* where text sits against a left
border — which is exactly the six sections the owner listed. Removing the `-1` moves all text
1pt right, so the value-position check must be re-run over the whole report afterwards.

---

## Nothing found beyond the owner's list

I looked for additional defects while measuring and have **none to add**. Two things I checked
and rejected rather than report as padding:
- p7's two purple header rects touch (142.00) where the reference has a 1pt gap (142.30→143.30)
  — but the *fills* are 2.0pt apart in both, so there is no rendered difference.
- The 17 ink mismatches and 2 text differences from the build round remain verified
  non-defects (see FACT-FINDING-SUMMARY.md §4).

**Awaiting PROCEED before changing any file.**
