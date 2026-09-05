# R10.012 — Condensate Demurrage Calculation — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. Tenth R10 report. 2 STATIC pages (title=page1, summary=page2, natural
band-overflow break, same mechanism as R10.006/R10.010/R10.011).

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R10.012\output\`.

## Two reference PDF samples — one JRXML, not two
This report has two reference PDFs (FC = Field Condensate, PC = Plant Condensate). Compared both
directly before building: they share the exact same layout template (2-line title, 3-row info
grid, Laytime/Allowed Laytime/Reimbursable Laytime tables, Demurrage Rate/Amount on page 2),
differing only in field VALUES and two conditionally-present "Overwrite" rows (FC shows
"Overwrite Laytime" after Laytime-after-Adjustment; PC shows "Overwrite Laytime Exclusions"
after Adjustment: Laytime Exclusions). This is NOT the genuinely-different-layout case the
R10.030/R10.031 multi-variant rule targets, so built as ONE JRXML (based on the PC sample, which
has one more row than FC), including both optional overwrite rows as always-present (blank by
default) rather than building two separate files.

## Report shape (measured directly)
- 2-line title ("Condensate Demurrage" / "Calculation") — unlike R10.011's single-line "LPG
  Demurrage Calculation".
- Info grid: Date Of Issue/Loading Port, Product/Vessel Name, Cargo Name/**Loaded Quantity**
  (confirmed via recon: no "(MT)" unit suffix here, unlike R10.011's "Loaded Quantity (MT)").
- Same Laytime → Allowed Laytime → Reimbursable Laytime section order and 4-column bordered
  table convention as R10.011 (label / colA / colB(Time) / colC(hrs)), reused directly since
  this report's fields fit the same template shape.
- Page 2 rate methodology differs from R10.011's bunker-cost a)/b)/c) breakdown: this report uses
  a Worldscale/AFRA-based i)/ii) comparison instead ("Actual Demurrage Rate Payable Under
  SPA/CP" vs "Worldscale Demurrage Rate Corrected by AFRA", picking the lesser of the two).

## Build approach
Applied R10.011's Part J4/J5 lesson from the start this time: every row position in BOTH the
title band and the summary band was taken directly from the reference PDF's own measured
`abs_y - topMargin(28)` value, not computed from a formula — for both bands, not retrofitted
after a miss in one of them. Result: coordinate spot-check on 7 labels across both pages landed
within ~1-2pt on the FIRST build attempt, with no offset-chasing needed at all this time.

## Known, documented deviations from the PC-only reference (not treated as defects)
1. The "Delay due to Adverse Weather (non FM)" row (present in R10.011's LPG report) and the
   "Overwrite Laytime" row (present in the FC sample) are both included in this build as
   always-present blank rows, even though the PC reference used for row-position recon doesn't
   show either row's LABEL at all (Crystal Reports appears to conditionally suppress the whole
   row, not just blank its value, when not applicable) — a deliberate cross-variant union choice
   (see the "one JRXML, not two" section above), not an oversight.
2. Page 2 of the reference shows one unlabeled value ("0.000" at abs y=250.0, x=313.4, with no
   text label found anywhere near it in the word-position recon) whose purpose could not be
   determined from the visible layout alone — left out of this build rather than guessing at a
   label, and flagged here as an open item for anyone doing the live-query phase to investigate
   against the underlying Crystal Reports formula.

## Verification performed
- Whole-page text extraction (`page.get_text('text')`) against the PC reference confirmed all
  its text lines are represented, with the two deliberate extra rows (see above) accounted for
  and the "0.000" gap documented rather than silently dropped.
- Coordinate spot-check on 7 labels across both pages confirmed alignment within ~1-2pt
  everywhere, consistent with R10.011's exact-position method.

## Not done this phase (by design)
- Live query/data verification — deferred, same as all prior R10 reports.

## Key takeaway
Confirmed the exact-recon-position method (R10.011's Part J4/J5 fix) generalizes well: applied
from the start on a NEW report with its own genuinely different section shape (Worldscale/AFRA
page-2 methodology instead of bunker-cost breakdown), it again produced sub-2pt alignment on the
first attempt. Also established a working pattern for handling multiple reference-PDF samples of
the same underlying report: compare them structurally first, and only split into separate JRXMLs
(per the R10.030/R10.031 rule) when the difference is a genuinely different LAYOUT, not just
different field values or a couple of conditionally-suppressed optional rows.
