# R10.010 – R10.034 layout audit vs the original Crystal PDFs

Date: 2026-09-04. Owner request: *"please do a DETAIL CHECK on R10.010 til R10.034 report layout
with its respective original crystal report layout.... currenly its produced the report layout is
far from its own original crytal report layout"*.

Method: `tmp/r10_audit_layout.py`, measuring every build PDF against its own reference PDF —
page count and size, border-rule positions (absolute page coordinates, so the wider/landscape
reports are handled), purple fill bands by pixel sampling, font family/size census plus per-span
bold/italic/size mismatches, and content compared whitespace-squashed so a wrapped or
hyphen-broken caption is not miscounted as missing. Raw output: `tmp/r10_audit_layout.txt`.
Band/query structure from a separate pass over the JRXMLs.

> **SUPERSEDED IN PART — 2026-09-05.** An enlarged band-by-band re-read of R10.026–R10.034
> (`R10-026-034-DEFECTS.md`) found **two statements in this file to be wrong**, both mine:
> (1) "Not one of these has a `detail` band" — six of the eight DO; my grep used `<detail `
> with a trailing space and missed every `<detail>` written without attributes. (2) R10.034's
> purple bands are not misplaced, they are **absent**: that JRXML contains no `#444080` at all.
> Read `R10-026-034-DEFECTS.md` for the current defect list on those eight files.

---

## Headline

11 JRXML files across 8 folders. Two distinct problems, needing different work:

| Tier | Files | Problem |
|---|---|---|
| **A** | 6 | **Structurally incomplete** — the repeating body of the report was never built |
| **B** | 3 | Complete, but the layout does not follow the original |
| — | 11 | Fonts (italic / size) wrong in **every** file |

---

## Tier A — the repeating body was never built (6 files)

> **Re-measured 2026-09-05** with each JRXML paired to **its own** reference. The first pass used
> `sorted(...)[0]`, so all three R10.030 variants were compared with `(ADP, per buyer)` and both
> R10.031 variants with `(ADP)`. Three figures changed, and one report turns out not to be a
> multi-page problem at all.

| File | Pages build / ref | Words missing | Bands present |
|---|---|---|---|
| R10.026 Average_ACQ_Balance | 1 / 2 | 9 | title, columnHeader, pageFooter |
| R10.029 AACQ_Notice_to_Buyer | 1 / 10 | 78 | title, pageFooter |
| R10.030 …ADP_per_buyer | 1 / 11 | 271 | title, columnHeader, pageFooter |
| R10.030 …ADP_per_contract | 1 / **12** | **268** | title, columnHeader, pageFooter |
| R10.030 …SDS_per_buyer | 1 / **9** | **151** | title, columnHeader, pageFooter |
| R10.031 …DES_Buyers_ADP | 1 / 2 | 87 | title, columnHeader, pageFooter |
| R10.031 …DES_Buyers_SDS | **1 / 1 — page count MATCHES** | **47** | title, columnHeader, pageFooter |
| R10.034 Annual_Quantity_Statement | 1 / 12 | 105 | title, pageFooter |

So it is **seven** files that need per-buyer repetition, not eight: `R10.031 …DES_Buyers_SDS`'s
own original is a single page, and its 47 word differences are data/layout, not missing pages.

**R10.012 is no longer in this tier or in Tier B** — it was split into `_PC` and `_FC`, one JRXML
per reference PDF, both owner-verified 2026-09-05.

**Not one of these has a `detail` band, a `<query>`, or a `subDataset`.**

What the extra reference pages actually are, verified by reading the Buyer cell on every page:
**one complete statement per buyer.** R10.034's 12 pages are CPC Corporation, Dummy Buyer,
INPEX Corporation, JERA ×2, Kansai Electric, Kyushu Electric, Osaka Gas, TotalEnergies, Toho
Gas, Tokyo Gas. R10.029's 10 pages are 10 buyers. Each page's own footer reads `Page 1 of 1`
(R10.030's longer ones read `Page 1 of 2` / `Page 2 of 2`), which confirms they are independent
statements rather than one long document.

So the build is not missing a *body* — it renders **one** statement, and the reference is a batch
of N. What is missing is the ability to repeat that statement per buyer: all the content sits in
the `title` band, which prints once, so even with a 12-row dataset bound the build would still
produce one page. That needs a `detail` band or a group.

**Two corrections to earlier statements of mine, both in this area:**

1. I first reported these as *"likely `detail`-band-needs-records, may be resolved by data
   binding"*. Incomplete — there is no detail band, so data binding alone will not produce the
   extra pages.
2. I then over-corrected to *"the repeating body was never built"*. Also wrong — the statement
   layout **is** built; it is the per-buyer repetition that is absent. The word counts below
   ("271 missing") are therefore N-1 copies of largely the same statement, not 271 words of
   unbuilt content.

Additional real layout defects in this tier, independent of the missing body:

- **Part F1 — text that renders as nothing.** 22 elements have a box shorter than
  `fontSize × 1.2`, which makes JasperReports silently drop the text:
  R10.031 ADP 10, R10.031 SDS 8, R10.030 ADP_per_buyer 2, R10.030 ADP_per_contract 2.
  All are `height="9"` boxes on an 8.0pt style (needs 9.6). Affected captions include
  `Contract Year`, `Contract`, the date of issue and the version.
- **R10.031 fonts are wrong on almost every span** — 156 (ADP) and 174 (SDS) size mismatches.
- **R10.029 / R10.034 purple bands are badly out.** R10.034's original has **24** purple bands;
  the build has **8**. R10.029's original has 14 against the build's 12, at different y.
- **R10.029** also carries one white-ring rectangle (`PurpleSectionStyle`, title y=214) — the
  same defect fixed on R10.006, R10.008 and R10.009.

---

## Tier B — complete, but the layout does not follow the original (3 files)

All three are the Demurrage family, 2 pages each, page size correct.

| File | Extra rules (we draw, original does not) | Missing rules | Font mismatches (bold / italic / size) |
|---|---|---|---|
| R10.010 LNG_Demurrage_EBC | **73** | 9 | 21 / 25 / 67 (p1) + 9 / 7 / 25 (p2) |
| R10.011 LPG_Demurrage | **38** | 11 | 16 / 15 / 81 (p1) + 23 / 3 / 45 (p2) |
| R10.012 Condensate_Demurrage | **44** | 15 | 13 / 16 / 55 (p1) + 15 / 4 / 28 (p2) |

### R10.010 — the original is almost entirely borderless

Measured on the original: the **only** bordered thing on page 1 is the info block
(x 0/128/255/383/510, y 109…174). Everything below it — sections 1 NOR, 2 Used Laytime,
3 Demurrage Allowed Laytime — has **no cell borders at all**. Page 1 has 7 horizontal rules in
total; the build draws **59**.

The original's design language is:

- a thin purple rule under the title (y 99…102)
- the info block bordered, **label columns purple, value columns white**
- one **purple column-header band per numbered section** (page 1: y 201…219, 330…348,
  552…570; page 2: y 120…138) — filled, but *not* bordered
- all data rows plain text, no borders, no fills
- a footer rule at y 765…768
- page 2 carries a **Comment box** (x 0…539, y 421…478) which the build does not have at all

### R10.011 / R10.012 — page 2 is empty of layout

Page 1 is over-bordered (38 and 44 extra rules) in the same way as R10.010, though these two
originals *do* have a bordered main table (x 0/227/312/397) — but with rules only at group
boundaries: **12** rules where the build draws 48 and 51. Same lesson as R10.006: Crystal draws
grid lines at group boundaries, not per sub-row.

Page 2 is the reverse. The originals have 4 verticals, 6 horizontal rules and 2 purple bands;
**the build has none of any of them** — zero rules, zero fills.

### Value/unit columns collide (R10.010)

The build renders `174,000m3`, `89,610.00USD/Day` and `0.00 USD` as single joined spans because
the value and unit cells abut. The original keeps them apart — value right-aligned ending ~380,
unit at x ≈ 399–401.

---

## Universal across all 11 files

- **Italic is missing or misapplied everywhere** — 3 to 50 spans per file. The originals make
  heavy use of `Arial-BoldItalicMT` (titles, info-block labels, section headings, column
  headers) and `Arial-ItalicMT` (info-block *values* in the Demurrage family). Several builds
  have no italic style defined at all.
- **Font sizes run 0.5–1.5pt small** — 17 to 174 mismatched spans per file. Typical pattern:
  title 16.0 where the original is 18.0, body 8.0 where the original is 9.0, notes 6.5 where the
  original is 9.0, footer 7.0 where the original is 8.0 **bold**.

## Not layout — do not "fix" these

- **R10.012 content differences** (22 missing / 26 extra words) are **different sample data**:
  the original is `IC24-FC-020` / September-2024 / `FPSO Lion`, the build is `IC23-PC-013` /
  July-2023 / `Darwin Plant`. This resolves at SQL binding.
- **R10.030 SDS_per_buyer** (16 extra words) and **R10.031 SDS** (14) are likewise sample-data
  differences.

---

## Suggested order

1. **R10.010** — pattern-setter for "follow the original": strip the grid to the info block,
   add the per-section purple bands, fix fonts, separate the value/unit columns, add page 2's
   Comment box.
2. **R10.011 / R10.012** — same treatment, plus reduce their main table to group-boundary rules
   and build page 2's layout, which is currently empty.
3. **Tier A layout defects that stand alone** — the 22 Part F1 drops, R10.029's white ring,
   R10.031's fonts, R10.029/R10.034's purple bands.
4. **Tier A missing bodies** — needs a decision: building repeating rows for 1–11 pages of
   content per report is a different order of work from layout correction, and for R10.030
   (11 pages, ~275 words missing each) it is effectively building the report body.
