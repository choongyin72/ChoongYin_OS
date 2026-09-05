# R10.006 — LPG Freight Rate Calculation — Completion Notes (2026-08-30)

**Phase:** LAYOUT ONLY. Fifth R10 report — the first genuinely **landscape, 2-page, STATIC**
(non-repeating) report in the R10 batch. Built fresh (no prior R10 report shares this shape).

**Build location:** `C:\Projects\INPEX\sources\CrystalReports\R10.006\output\`.

## Report shape (measured directly)
- Landscape page geometry (`842x595`, vs every prior R10 report's portrait `595x842`).
- **Page 1**: standard 4-row info table (Date of Issue/Contract Year, Contract Name/Month,
  Buyer/Status, Delivery Term/blank — same skeleton as R10.002/003/007 but wider columns for
  landscape), then two sections using a **new convention not seen in prior R10 reports**: the
  section label itself carries a full-width purple background bar (`SectionBarStyle`, not the
  plain-text `SectionLabelStyle` used by R10.002/003/007's "Applicable JCC Price" style headers).
  "Assumptions" section (Baltic Rate, Bunker Price IFO 380 CST/MGO, each with a unit and an
  italic note line). "Fixed Parameters" section (Cargo Intake, Distance Laden/Ballast for both
  routes, Vessel Speed, Bunker Consumption, Port Charge per port).
- **Page 2**: a large (~30-row) "Freight Calculation" table with a 2-line group header (Load
  Port/Discharge Port sub-labels under two route-group headers, "Ras Tanura"/"Darwin", each
  spanning a value column + a formula-letter column), followed by data rows for Freight Rate,
  Cargo Intake, Gross Revenue, Vessel Speed, Distance, Laden/Ballast Passage Days, Sea Margin,
  Laytime, Bunkering Days, Total Voyage Days, Bunker Price, Bunker Consumptions, Bunker Cost
  (Total IFO/Total MGO/Total Bunker), Port Charge (Load/Discharge/Total), Total Time Charter
  (T/C) Cost, and Equivalent Daily T/C Rate — each row annotated with its own formula letter
  (A through O) reflecting the real freight-rate calculation chain.

## Page-break mechanism (new for this session)
No repeating detail row exists (each page has entirely different static content), so R07.018's
group/`startNewPage` mechanic (which needs a real repeating field to group on) doesn't apply.
Used `<title>` for page 1's content and `<summary>` for page 2's content instead, relying on
**natural band-overflow pagination**: title's declared height (440) + summary's declared height
(470) together exceed the available page height (595 - 28 - 28 = 539), so JasperReports must
place the whole `summary` band (an atomic unit under `splitType="Prevent"`) on a fresh page.
An `<element kind="break" type="Page"/>` was also placed at the start of the summary band as a
belt-and-braces marker, but an isolated minimal repro (`minitest.jrxml`, both bands small enough
to fit on one page) proved this **`break` element by itself does NOT force a new page** in this
engine build — the actual 2-page split is produced entirely by the band-height-overflow
mechanism, not by the break element. Confirmed via Jackson-error discovery that `type="Page"` /
`"PAGE"` are both accepted (no error), but neither produces a page break on its own; kept the
element in place as harmless but the design does not depend on it working.

## Defects found and fixed
1. **Missing report-level attributes for a summary-page footer**: with `<summary>` +
   `<pageFooter>`, JasperReports suppresses page footer on the summary's page unless
   `summaryWithPageHeaderAndFooter="true"` is set on the root `<jasperReport>` element (verified
   the exact attribute name via a deliberate Jackson `UnrecognizedPropertyException` — confirmed
   real property list includes `summaryWithPageHeaderAndFooter`, `titleNewPage`,
   `summaryNewPage`). Added both `summaryWithPageHeaderAndFooter="true"` and
   `titleNewPage="false"`.
2. **Duplicate XML attribute silently broke the footer entirely** — a `sed` edit meant to bump
   one footer textField's `height` from 8 to 12 appended a second `height="12"` attribute
   instead of replacing the original `height="8"`, producing an element with two `height`
   attributes. This didn't throw a compile error but the footer never rendered on either page
   (confirmed via whole-page `get_text('text')` showing `Last refresh date:` completely absent).
   Fixed by replacing the malformed element cleanly (single `height="12"`) — this fixed the
   footer immediately.
3. **Page 2's table was incomplete on first build**: the Port Charge (Load/Discharge/Total),
   Total Time Charter (T/C) Cost, and Equivalent Daily T/C Rate rows were never written in the
   first pass — found via whole-page text diff against the reference (these labels/values were
   entirely missing from GEN, not just misplaced). Added all three rows plus their parameters.
4. **Several placeholder values were wrong, not just cosmetically approximate** — cross-checked
   against the reference's own text at the relevant y-positions and found real mismatches, not
   copy-paste rounding: Laden Passage Days RT should be 17.35 (had 17.34); Ballast Passage Days
   DW should be 7.89 (had 7.90); both Laytime rows (Load Port and Discharge Port) should be 2.25/
   2.25 (had wrongly copied 1.50/1.50); and — most substantively — "Total IFO Cost" and "Total
   MGO Cost" had been given the SAME value as "Total Bunker Cost" (786,010.74 RT / 391,369.40 DW)
   instead of their own distinct component values (Total IFO Cost = 783,546.72 RT / 390,020.21
   DW; Total MGO Cost = 2,464.02 RT / 1,349.20 DW — confirmed these two sum correctly to the
   existing Total Bunker Cost values, so the structure was right, only the IFO/MGO split values
   were wrong). Fixed all six parameter defaults.

## Verification performed
- Whole-page text extraction (`page.get_text('text')`) run BEFORE any coordinate comparison, per
  the mandatory rule established on R10.002/003 — caught all defects above.
- Remaining text-diff noise after fixes (value+unit or value+formula-letter appearing as one
  joined token in the reference's line-grouping vs two separate tokens in mine, e.g.
  `"17.35 days"` vs `"17.35"`+`"days"`) confirmed as a PyMuPDF line-joining/geometry-heuristic
  artifact, not a real content or position defect — every individual value and label is present
  in both; spot-checked several of these joined pairs by locating both tokens' actual (x,y) in
  each PDF and confirming they sit on the same visual line at matching positions.
- Coordinate spot-check on 8 key section/row labels across both pages (Assumptions, Fixed
  Parameters, Baltic Rate, Cargo Intake, Ras Tanura sub-header, Total Time Charter, Equivalent
  Daily T/C Rate) landed within ~2-9pt of the reference on both axes — consistent with the
  tolerance band already accepted across the rest of the R10 family.

## Not done this phase (by design)
- Live query/data verification — deferred, same as all prior R10 reports. All values remain
  parameter defaults matched to the reference's own sample instance, not live SQL.

## Key takeaway
This report needed two genuinely new mechanisms not used by any prior R10 report: a landscape
page layout, and a `<title>`+`<summary>` 2-STATIC-page split relying on natural band-height
overflow (the `<break>` element itself proved to be a no-op in isolation — verified via a
targeted minimal repro rather than assumed). It also surfaced a new failure class beyond the
already-documented "height too small silently drops text" bug: a **duplicate XML attribute from
a careless `sed` edit silently breaks an element with zero compile error** — worth checking for
whenever a `sed`-based fix is applied to attribute values rather than a proper Edit/regex
replace. Finally, several of this report's placeholder values weren't just close-enough
approximations — two rows had literally the wrong number copied from a different (sibling) row —
reinforcing that even "layout only, values are placeholders" still needs each placeholder
checked individually against the reference rather than assumed self-consistent.
