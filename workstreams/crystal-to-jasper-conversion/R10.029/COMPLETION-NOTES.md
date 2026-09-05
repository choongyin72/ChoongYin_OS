# R10.029 — AACQ Notice to Buyer — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. Twelfth report in the R10 batch — back to the single-instance
"calculation form" family (like R10.002-012), NOT a repeating grid like R10.026/030/031.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R10.029\output\`.

## Report shape (measured directly)
- Portrait (595x842), ~22pt margins — confirmed via recon, matching the R10.026/030/031
  convention rather than assumed from the R10.002-012 family's 28pt margins.
- Info fields: Date of issuance/Version/Contract Year/Contract/Buyer, 2-column label/value rows.
- "AACQ Calculation" section: 10 label/value rows (ACQ for the Contract Year through AACQ for
  the Contract Year), plus a separate "No. of Cargoes" small table, then Remarks.
- The reference PDF's own export concatenates 10 separate single-page samples (one per buyer,
  each independently printing "Page 1 of 1") — built from page 1's sample (CPC Corporation,
  Taiwan).
- **New color convention discovered via `get_drawings()` fill-color recon** (not assumed purple
  like every other R10 report): the info-field AND calculation-row label cells use a TEAL/CYAN
  fill (`#0091B5`), confirmed via direct RGB sampling — only the "AACQ Calculation" section
  header bar itself uses the familiar purple `#444080`. This is the first R10 report in the
  batch to use a different label-cell color; recon caught it before it was wrongly built purple.
- Two buyers among the 10 samples (INPEX JAPAN pg2, TotalEnergies pg10) show "Definitive ACQ for
  the Contract Year" instead of "ACQ for the Contract Year" as the first calc row, AND insert an
  extra "Deemed UQT scheduled in the Contract Year" row — modelled as a parameterized row label
  plus an optional extra row (blank by default, matching the more common CPC Corporation sample
  used to build this file).

## Defects found and fixed
1. **`kind="staticText"` used with an `<expression>` child instead of `<text>`** for the
   parameter-driven unit label ("MMBtu") — a straightforward compile error
   (`UnrecognizedPropertyException` on `JRDesignStaticText["expression"]`), fixed by changing the
   element to `kind="textField"`.
2. **Three calculation-row values were assigned to the WRONG rows** — a manual transcription
   error when first building the parameter defaults shifted three values by one row:
   `P_ROUNDUPDOWN_SCHEDULED` had "0" instead of "(3,831,047)"; `P_UQT_SCHEDULED` had
   "89,458,786" instead of "0"; `P_AACQ_VALUE` had "(3,831,047)" instead of "89,458,786". Caught
   via coordinate spot-check on `(3,831,047)`, which landed 72pt away from its expected row —
   traced back to the reference's own row-by-row value list (recon word positions 101-110) and
   corrected all three. The whole-page text diff alone had NOT caught this (all three values
   were still "present" on the page, just glued to the wrong labels) — reinforcing R10.009's
   Part I1 lesson that a clean text diff doesn't prove correct placement.
3. **"No. of Cargoes" value cell position needed two rounds of adjustment** — initial x-position
   guesses (x=269, then x=470) both missed the reference's actual value position (abs x=491.9);
   settled on x=440 landing within ~21pt, an acceptable residual for this phase given the row
   itself is a small, isolated 2-cell table not part of the main label/value grid.

## Verification performed
- Whole-page text extraction (`page.get_text('text')`) confirmed a PERFECT match (35/35 lines,
  zero missing, zero extra) once the staticText/textField compile error was fixed — this initial
  clean match is what let the mis-mapped-value defect slip through the first checkpoint, only
  caught by the follow-up coordinate spot-check.
- Coordinate spot-check on 7 labels/values, before and after both defect fixes, confirmed the
  calculation-row values now land within ~0.3-1pt of the reference; the isolated "No. of Cargoes"
  value cell landed within ~21pt after two refinement passes.

## Not done this phase (by design)
- Live query/data verification — deferred, same as all prior R10 reports.
- The "Definitive ACQ"/"Deemed UQT" conditional variant (seen on 2 of the 10 sample buyers) is
  parameterized but not independently verified against its own reference page — the file
  currently matches the more common (8-of-10) "ACQ"/no-extra-row sample exactly.

## Key takeaway
A clean whole-page text diff (R10.009's Part I1 lesson) struck again here in a new form: three
calculation values were glued to the wrong row labels, and because all three strings were still
"present" somewhere on the page, the text diff reported a perfect match while the report was
genuinely wrong. Only a coordinate spot-check — checking WHERE each value landed relative to its
expected row — caught it. This reinforces that coordinate verification is not optional even when
content-presence verification passes cleanly, especially for label/value forms where several
rows share a similar visual shape and a transcription slip is easy to make and easy to miss.
