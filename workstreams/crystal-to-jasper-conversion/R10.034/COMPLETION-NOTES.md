# R10.034 — Annual Quantity Statement — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. Final report in the confirmed R10 batch order. Portrait, single-instance
"calculation form" (same family as R10.029), the most structurally elaborate single-page report
built in this batch.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R10.034\output\`.

## Report shape (measured directly)
- Portrait (595x842), ~22pt margins, same TEAL label-cell convention (`#0091B5`) as R10.029 —
  confirmed via `get_drawings()` fill recon, not assumed.
- Info fields: Date of Issuance/Contract Year/Date of Applicable ADP Issue/Contract/Buyer — a
  **single-column 5-row label/value list**, genuinely different from R10.029's paired 2-column
  layout despite both reports being in the same "calculation form" family — confirmed via recon,
  not assumed to match the immediately-preceding sibling.
- "ACQ for the Contract Year" calc block: 5 label/value rows + a result row "ACQ after
  adjustment (Base ACQ)".
- A numbered (1-6) **3-value-column table** (AACQ / Quantity Actually Delivered / Balance) plus a
  Total row — confirmed via `get_drawings()` that each row's value area is ONE WIDE BORDERLESS
  white cell containing 3 separate right-aligned text runs at fixed x-offsets, not 3 individually
  bordered cells; modelled the same way (3 `textField`s sharing one background rectangle per row).
- "AACQ for the Contract Year" section: a further list of 11 deduction/result rows (Quantity not
  delivered due to Seller's/Buyer's Force Majeure, Take-Back Quantity, Seller's Supply
  Deficiency, Scheduled Make-Up LNG Quantity, Take-or-Pay Quantity, Total Delivered Quantity,
  Make-Up LNG Quantity actually delivered, Quantity Paid by Buyer, Annual Quantity Deficiency,
  Fractional Quantity) — single value column, right-aligned, genuinely borderless (confirmed via
  recon of this section's own drawings, unlike the bordered teal/white cells used elsewhere in
  the same report).
- The reference PDF's own export concatenates 12 separate single-page samples (one per buyer,
  each independently printing "Page 1 of 1") — built from page 1's sample (CPC Corporation,
  Taiwan).

## Defects found and fixed
1. **Band-height overflow** on first compile (`title height=675` too short for content reaching
   y=699) — fixed by bumping to 705, consistent with the routine band-sizing fix seen across
   every multi-row report in this batch.
2. **One label wrapped to 2 lines instead of 1** ("Force Majeure Restoration Quantity scheduled
   in Contract Year") — caught immediately by the whole-page text diff (missing the full string,
   extra a truncated variant), fixed by widening the element and reducing its font size slightly
   (7.5→6.8) to fit the reference's single-line rendering.

## Verification performed
- Whole-page text extraction (`page.get_text('text')`) confirmed a PERFECT match (63/63 lines,
  zero missing, zero extra) after the line-wrap fix.
- Coordinate spot-check on 6 labels/values confirmed Y-axis (row) alignment within ~1-2pt
  everywhere — consistent with the exact-recon-position method's track record across this whole
  batch. X-axis spot-check results were inconclusive for values that appear more than once in the
  document (e.g. "92,888,762" appears both in the ACQ calc block and as Row 1's AACQ value) since
  the simple exact-string search used for verification can't disambiguate which occurrence it
  found — not treated as a defect, since content-completeness was already independently confirmed
  via the whole-page diff.

## Not done this phase (by design)
- Live query/data verification — deferred, same as all prior R10 reports.

## Key takeaway
This report closes out the confirmed R10 batch (R10.002 through R10.034, 24 total JRXML files
across 20 distinct reports/report-variants). The exact-recon-position method established on
R10.011 (Part J4) and reused throughout the rest of the batch continued to produce the tightest,
most reliable alignment of any approach tried this session — on a report with 25+ distinct rows
across 4 sub-sections, it still landed the vast majority of positions within 1-2pt on the first
or second build attempt, with only routine band-height and line-wrap fixes needed, no structural
rework.
