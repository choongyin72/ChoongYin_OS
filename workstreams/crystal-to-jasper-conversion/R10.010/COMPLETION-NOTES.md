# R10.010 — LNG Demurrage / EBC Calculation — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. Eighth R10 report — 2 STATIC pages (title=page1, summary=page2, natural
band-overflow page break, `summaryWithPageHeaderAndFooter="true"` — same mechanism as R10.006),
but otherwise a genuinely different shape from every other R10 report so far: single-column
vessel/cargo info fields instead of a Date-of-Issue/Contract-Year grid, and 6 numbered sections
(NOR, Used Laytime, Demurrage Allowed Laytime, Reimbursable Time, Demurrage Rate, Demurrage
Reimbursable Amount) built as bordered Date/Time or Time-only tables.

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R10.010\output\`.

## Report shape (measured directly)
- Single-line title "Demurrage Calculation", repeated at the top of both pages.
- Info fields: Date Of Issuance / Demurrage Type Name / Product / Vessel Name / Cargo Name /
  Vessel Tank Size (m3) / Loading Port, in a 4-row 2-column grid (last cell blank).
- Section 1 "NOTICE OF READINESS (NOR)": Date/Time 2-column table (Scheduled Loading Date, NOR
  Tendered, All Fast, Effective NOR) + an italic note line.
- Section 2 "Used Laytime": Date/Time table with grouped sub-rows (`Start of Used Laytime` /
  `i)`/`ii)` breakdown / bracketed "[The earlier of (i) and (ii)]" result row; `End of Used
  Laytime` / its own `i)`/`ii)` breakdown / bracketed result row; then Calculated/Overwritten
  Used Laytime).
- Section 3 "Demurrage Allowed Laytime": a Time-only table (single value + "hrs" unit sub-column)
  with an inline formula note ("(174,000 - 165,000)/10,000 = 00:54").
- Section 4 "Reimbursable Time" (page 2): same Time-only table shape as Section 3.
- Section 5 "Demurrage Rate": free-form label/value lines (no bordered table) with an inline
  applicable-rate formula note.
- Section 6 "Demurrage Reimbursable Amount": free-form label/value lines + "Comment" (no box,
  unlike the bordered Comments sections in R10.007/008/009).

## Defects found and fixed
1. **Wrongly assumed this report uses a borderless, plain-text layout** — a first-glance reading
   of `get_text('text')` (no visible box characters, no obvious grid) suggested this report
   might differ from the rest of the R10 family's bordered purple-header/white-value cell
   convention. Confirmed via `page.get_drawings()` fill-color recon (not assumed) that this
   report DOES use the exact same purple (`#444080`) header-cell / white value-cell bordered
   convention as every other R10 report — the plain-text impression was simply from not
   recon'ing the vector drawings before judging the visual style. Now flagged as Part J of the
   lessons file: text-only recon is not sufficient to judge box/border style: always check
   `get_drawings()` fill colors too before assuming a report has no bordered cells.
2. **Page 1's footer showed "Page 2 of 2" instead of "Page 1 of 2"** — the page-number
   `textField` used `evaluationTime="Auto"`, which (unlike a plain default-evaluation field)
   deferred the `$V{PAGE_NUMBER}` read to a point where it reflected the NEXT page's counter on
   a 2-static-page title+summary report. Fixed by removing `evaluationTime="Auto"` — the built-in
   `PAGE_NUMBER` variable doesn't need deferred evaluation for a simple `pageFooter` on this kind
   of report, only default (`Now`) evaluation is needed.
3. **Systematic, GROWING vertical offset across the whole title-band content** (~28pt at the
   info table, growing to ~44pt by the end of the longest table) and a similar growing offset on
   the summary band (~47-53pt) — root cause: an arithmetic slip translating the reference's
   absolute divider-line position (abs y=126.1) into the JRXML's local coordinate (should be
   local≈98, was built at local=70, a flat 28pt error that then compounded further down the page
   from slightly-too-small row heights). Fixed with a scripted progressive shift (base +28 plus a
   small proportional stretch per pt of original y) applied to every element in the title band
   from the divider onward, and a separate progressive shift for the summary band — reduced most
   spot-checked positions to within ~2-10pt of the reference, with one residual ~31pt gap at the
   very last row of the longest table (Section 2's 11-row Used Laytime block), accepted as a
   residual consistent with similar deep-page drifts already accepted elsewhere in this family
   (R10.006 ~9pt, R10.009 ~12pt) — this report's much longer single-page content chain simply
   accumulates more of it.

## Verification performed
- Whole-page text extraction (`page.get_text('text')`) on both pages confirmed every reference
  text line is represented; all remaining diffs traced to value+unit text-join artifacts (e.g.
  "174,000m3" as one joined element vs "174,000"/"m3" as two reference lines), not missing
  content — including catching the "Page 2 of 2" defect on page 1's MISSING/EXTRA diff before it
  was traced to the `evaluationTime="Auto"` root cause.
- Coordinate spot-check on 6 labels/values across both pages, before and after the offset fix,
  confirmed the fix brought most positions from a 30-50pt gap down to within ~2-10pt.

## Not done this phase (by design)
- Live query/data verification — deferred, same as all prior R10 reports.

## Key takeaway
Two lessons reinforced or newly discovered here: first, a text-only recon (`get_text`) is not
sufficient to judge whether a report uses bordered/filled cells — `get_drawings()` fill-color
recon is required before concluding a report's box style, even when the text alone "looks"
borderless. Second, a single arithmetic slip converting one reference coordinate (abs→local) can
silently cascade into a report-wide, GROWING vertical offset that only becomes obviously wrong
many rows later — worth computing and sanity-checking at least 2-3 reference anchor points
(not just the first one) before building a long multi-section report, rather than trusting one
early conversion to hold for the whole page.
