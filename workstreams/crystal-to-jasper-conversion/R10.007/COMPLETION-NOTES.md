# R10.007 — Monthly Plant Condensate Contract Price — rebuild notes (2026-09-04)

Rebuilt against `crytsal report in pdf/R10.007 - Monthly Plant Condensate Contract Price.pdf`.
Files: `output/R10_007_Monthly_Plant_Condensate_Contract_Price.jrxml` + `.pdf`.
Backup: `*.backup_20260904_rebuild`.

## Verification
| Check | Result |
|---|---|
| pages / images | 1/1 · 1/1 |
| embedded fonts | 11 BoldItalic / 19 Plain / 17 Bold — **exact match** |
| span positions | **0 of 47** off at 1.5pt; dx=0 for 40, −1 for 6 |
| font/size mismatches | 0 |
| words | 1 difference — the Buyer overflow, see below |

## Type 1 — defects against the reference (all fixed)
Systemic set: no font jar, zero italics, purple `#444080` → `#444088`, no logo, no footer rule,
footer missing its second line, info-block values wrongly tinted, white-pen bug (39 pens).

**Report-specific:**

1. **TWO purple styles were needed.** This report's component-table label cells and its
   two-line column headers are `Arial-BoldMT` (bold, NO italic), while the info-block label
   cells are `Arial-BoldItalicMT`. A single purple style gets one group wrong — 19 elements
   moved to a new `HeaderBoldStyle`. R10.002/003 do not have this split.
2. **The whole component table sat ~7pt too low.** Its 2-line header was built as two stacked
   12pt cells starting at y=261; the reference has ONE 23.8pt cell at abs 282.1 = local 254.1.
   Every row below inherited the error. Repositioned header + 5 data rows + the Contract Price
   row, which is also **11.3pt tall, not 13**.
3. **Formula line is 10.0pt** here (R10.003's is 12.0) and `Arial-BoldMT`. Built at
   `PlainLabelStyle` 8.0. Its box was 20pt at y=196; measured 17.8pt at local 191.
4. **Comments box was 74pt too short** — built h=58, measured h=132.1.
5. **Footnote had an inline `fontSize="6.5"`**; the reference is 9.0 `Arial-BoldMT`.
6. Missing 2.8pt filler at local y=344 (abs 372.6) before the Contract Price row.
7. **Title is two lines at 18pt** (abs y=48.4 / 70.2). Boxes had to grow 20 → 22 or the text is
   silently dropped, and each line is now left-aligned at its measured x (local 180 / 232) —
   centring could not deliver the full 23.4pt shift without pushing the box past the 539pt
   column.
8. `ValueCellStyle` needed `rightPadding="3"` here, where R10.002 measured 1. The inset is
   per report, so it is read from each reference rather than assumed.

## 🔶 OPEN ITEM — Buyer name overflow (same as R10.003)
`P_BUYER` = `"INPEX Energy Trading Singapore"` does not fit its ~125pt column at 9.0pt.

| | renders |
|---|---|
| reference | `INPEX Energy Trading Singapo` — cut mid-word and **overflowing into the neighbouring purple `Status` cell** (PyMuPDF extracts the two as `SingapoStatus`) |
| ours | `INPEX Energy Trading` — breaks at the last whole word, stays inside the cell |

Owner's call: keep ours, match Crystal's overflow, or widen the column / shrink that field.
Unchanged pending direction.

## Type 2 — none applied
The 2.8pt filler is present because Crystal has it. R10.001/R10.002's sliver removal was NOT
carried here — owner ruled type-2 decisions are per report.
