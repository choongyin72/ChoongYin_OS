# JasperReports 7.0.3 — Consolidated Rules Reference

**Purpose:** single consolidated reference for converting Crystal Reports → JasperReports 7.0.3,
testing in this repo's local sandbox. Gathered 2026-08-29 per owner request.

**Source ranking (highest to lowest authority — never let a lower tier override a higher one):**
1. **`C:\DEV\INPEX Reports\Claude.md`** (v2.0, updated for the R07.024 LPG CDP conversion) — a
   real, hands-on, battle-tested mandatory ruleset from an actual conversion project. **This is
   the primary source.** Read the original in full before any real conversion work — this file
   is a summary/index of it, not a replacement.
2. `DeepDiveLearnings/extracted/JR-01` through `JR-04` — this repo's own unexecuted self-learning
   task prompts (topic outlines only; the actual deep-dive was never run, so treat these as
   **background/context**, not verified fact, except where cross-checked below).
3. Web-verified general JasperReports/Crystal-Reports facts (searched 2026-08-29, cited inline) —
   used only to fill gaps neither source above covers, and flagged where they *correct* an
   assumption in JR-01/02/03/04.

**If tier 1 and tier 2/3 ever conflict, tier 1 wins** — it's the only tier verified against a real
JasperReports 7.0.3 project. Two concrete conflicts found and resolved this way below (marked ⚠).

---

## PART A — Mandatory rules, from `Claude.md` (primary source, condensed)

### Prime directive
Converting production reports for a real organisation. An incorrect fix is worse than no fix.
Never trade one working thing for another; never delete content to fix geometry; never rewrite a
whole section to fix a syntax error; never assume Crystal behaviour maps 1:1 to JasperReports.

### Session start checklist
Read `Claude.md` in full → read the report-specific `context.md` → read the target JRXML in
full → audit all band heights/element positions → verify geometry → make the change → re-verify
geometry → run the full 14-scan pre-save checklist → only respond at 100% ✅ → **open the saved
file in Jaspersoft Studio 7.0.3 as the mandatory final verification step** (Problems panel = zero
errors, Preview renders correctly — there is no standalone CLI compile check for 7.0.3; Studio
open **is** the compile verification).

### Crystal Reports → JasperReports 7.0.3 concept mapping

| Crystal Reports | JasperReports 7.0.3 |
|---|---|
| Report Header | `<title>` band |
| Report Footer | `<summary>` band |
| Page Header / Footer | `<pageHeader>` / `<pageFooter>` band |
| Group Header / Footer | `<groupHeader>` / `<groupFooter>` inside `<group>` |
| Details Section | `<detail>` band |
| Subreport | subDataset + `componentElement` (**never** `<subreport>` element, per this project's convention) |
| Formula Field | `staticText` or `<variable>` with expression |
| Parameter Field | `<parameter>` |
| Database Field | `<field>` |
| Running Total Field | `<variable>` with `incrementType` |
| Special Field — PageN / PageCount / RecordNum | `$V{PAGE_NUMBER}` / `$V{PAGE_COUNT}` / `$V{REPORT_COUNT}` |
| Suppress (No Drill-Down) | `printWhenExpression` |
| Can Grow | `stretchType="RelativeToBandHeight"` |
| Can Shrink | no direct equivalent — use `isBlankWhenNull` |
| Keep Together | `splitType="Prevent"` on band |
| New Page Before/After | `isStartNewPage="true"` on `<group>` |
| Reset Page Number | `isResetPageNumber="true"` on `<group>` |
| Shared Variable | `<variable>` at report level |
| Cross-tab | flat CSV subDataset + fixed table (avoid live `<crosstab>` for static reports) |
| OLE Object / Chart | not directly supported — use image |

### Rule 0A — Two JRXML formats: only ONE is acceptable

Jaspersoft Studio can save JRXML in two different formats, and they use **different attribute
names for the same thing**. Detect by checking line 1 for an `xmlns=` declaration.

- **Studio compact format (FORBIDDEN)** — no `xmlns`, Jackson parser, all visual properties as
  inline attributes directly on tags (`fontName=`, `fontSize=`, `vTextAlign=`, `textAlignment=`,
  `x=`/`y=`/`width=`/`height=` directly on `<staticText>`/`<textField>`), and root attributes use
  **no** `is` prefix (`titleNewPage`, `summaryNewPage`, `summaryWithPageHeaderAndFooter`).
- **Standard JRXML format (REQUIRED)** — has `xmlns=`, all visual properties live inside child
  elements (`<reportElement>`, `<textElement><font>`), and root attributes **require** the `is`
  prefix (`isTitleNewPage`, `isSummaryNewPage`, `isSummaryWithPageHeaderAndFooter`).
- `ignorePagination` has no `is` prefix in **either** format.
- Never mix the two formats in one file. Re-check format any time Studio opens and re-saves a
  file — Studio may silently convert standard → compact on save.

### Rule 1 — XML namespace (exact, mandatory)
```
xmlns="http://jasperreports.sourceforge.net/jasperreports"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://jasperreports.sourceforge.net/jasperreports http://jasperreports.sourceforge.net/xsd/jasperreport.xsd"
```
Never add `xmlns:jr` at the root, never reference `components.xsd` at the root (only inside a
`jr:table`'s own tag, per Rule 15), never add any other namespace.

> ⚠ **Cross-check note:** a 2026-08-29 web search found a Jaspersoft Community thread stating
> JasperReports 7.0.0+ no longer does strict XSD schema validation on JRXML at the engine level
> (the schema URL may even 404). That's an *engine* fact; it does not contradict `Claude.md`'s
> Rule 1 — Studio's own parser and this project's validation scans still require the exact
> namespace block above, and it's what makes the file open correctly in Jaspersoft Studio 7.0.3
> (the mandatory verification step). Follow Rule 1 exactly regardless of engine leniency.

### Rule 2 — Mandatory band order (XSD-enforced) and declaration order
Bands, in order: `background → title → pageHeader → columnHeader → detail → columnFooter →
pageFooter → lastPageFooter → summary → noData`.
Top-level declaration order: report attributes → `<property>` → `<template>` → `<import>` →
`<parameter>` → `<queryString>` → `<field>` → `<sortField>` → `<variable>` → `<subDataset>`
(**must** be after all `<variable>`, before `<group>` and `<background>`) → `<group>` →
`<background>` → remaining bands.

### Rule 3 — Band vs. group attributes
`<band>` accepts **only** `height` and `splitType` (`Stretch|Prevent|Immediate`) — nothing else.
`isStartNewPage`, `isReprintHeaderOnEachPage`, `isResetPageNumber`, `keepTogether`,
`footerPosition`, `minHeightToStartNewPage` all belong on `<group>`, never on `<band>`.

### Rule 4 — Page geometry (must verify per report, every time)
Standard sizes @72dpi: A4 Portrait 595×842, A4 Landscape 842×595, Letter Portrait 612×792,
Letter Landscape 792×612.
- **Geometry 1 (page fill):** `topMargin + bottomMargin + title + pageHeader + columnHeader +
  detail + columnFooter + pageFooter = pageHeight`, exactly, not approximately.
- **Geometry 2 (summary fits one page):** `topMargin + pageHeader(if shown) + summary +
  pageFooter(if shown) + bottomMargin ≤ pageHeight`. Leave **≥5px breathing room** — content
  exactly at band-height boundary can still get pushed to a second page because the engine
  reserves space before rendering. If content fills the band exactly, grow the band 5px and
  shrink title 5px to keep the page-height total exact.
- **Geometry 3 (group footer + isStartNewPage worst case):** `groupFooterHeight + title +
  pageHeader + columnHeader + columnFooter + pageFooter + topMargin + bottomMargin ≤ pageHeight`.
- **Geometry 4 (element boundaries, every element, no sampling):** `element_y + element_height ≤
  band_height`; `element_x + element_width ≤ pageWidth - leftMargin - rightMargin`; `x,y ≥ 0`.

### Rule 5 — Legacy v6 compact → 7.0.3 conversion (run all 3 steps together, never separately)
1. **Attribute renames:** `default=`→`isDefault=`, `bold=`→`isBold=`, `italic=`→`isItalic=`,
   `underline=`→`isUnderline=`, `strikeThrough=`→`isStrikeThrough=`, `pdfEmbedded=`→`isPdfEmbedded=`
   (then removed entirely, see Rule 10), `blankWhenNull=`→`isBlankWhenNull=`,
   `hTextAlign=`→`textAlignment=`, `vTextAlign=`→`verticalTextAlignment=` (then banned in
   `<textElement>` in 7.0.3 — remove), `forPrompting=`→`isForPrompting=`, `fontSize="N.0"`→`"N"`
   (no decimal), move `fontName=`/`fontSize=`/`textAlignment=`/`x=y=w=h=` off the element tag into
   the correct child (`<reportElement>`, `<textElement><font>`).
2. **Element renames:** `<dataset>`→`<subDataset>`, `<query>`→`<queryString>`.
3. **Element-kind expansion:** `<element kind="X">` → `<X>` for textField/staticText/image/line/
   rectangle/ellipse/frame/subreport/crosstab/break/elementGroup/component (→`<componentElement>`)
   /genericElement; all `</element>` closing tags become the matching real tag name.

### Rule 6 — CDATA (mandatory, most common single conversion error)
Always CDATA-wrap: `<text>`, `<textFieldExpression>`, `<defaultValueExpression>`,
`<initialValueExpression>`, `<variableExpression>`, `<imageExpression>`, `<groupExpression>`,
`<printWhenExpression>`, `<queryString>`. Missing CDATA → text is silently invisible in PDF.
Inside CDATA: use the **literal character**, not the HTML entity — `\n` not `&#10;`, `³` not
`&#179;`, `°` not `&#176;`, literal `&` not `&amp;` (CDATA doesn't need entity escaping).

### Rule 7 — Banned elements & attributes (7.0.3, this project's convention)
Banned elements: `<jr:table>` family outside the one sanctioned skeleton (Rule 15), bare
`<dataset>` (must be `<subDataset>`), `<reportFont>` (use `<style>`).
Banned attributes: `isStretchWithOverflow` (→ `stretchType="RelativeToBandHeight"`),
`pdfFontName`/`isPdfEmbedded`/`pdfEncoding` (remove entirely — see Rule 10),
`verticalTextAlignment` inside `<textElement>` (invalid in 7.0.3), `font.fontSize` (→
`font.size`), `isStartNewPage` on `<band>` (belongs on `<group>`), any `jr:`-prefixed attribute
outside the sanctioned list, `forecolor`/`backcolor` on `<font>` (belong on `<reportElement>`
only). `isTitleNewPage`/`isSummaryNewPage` are only wrong in **compact** format — correct and
required in **standard** format (see Rule 0A).

> ⚠ **Cross-check note:** this directly overrides an assumption baked into `JR-01`'s learning
> objectives (which listed `pdfFontName` Helvetica mappings as a thing to learn "for the PDF
> export path"). Per this project's real, hands-on rule: **remove `pdfFontName`/`isPdfEmbedded`/
> `pdfEncoding` entirely** in 7.0.3 — do not set them at all, regardless of what older
> JasperReports docs/tutorials say. Font selection for PDF now goes through `fontName` on
> `<font>` plus (if needed) a registered font-extension JAR — see Rule 10.

### Rule 8 — Element nesting order (mandatory)
Section elements (`title`, `summary`, `pageHeader`, `detail`, etc.) contain **only** `<band>` —
never a visual element directly. `<band>`/`<frame>` direct children: `staticText`, `textField`,
`image`, `line`, `rectangle`, `ellipse`, `frame`, `break`, `elementGroup`, `componentElement`,
`crosstab`, `genericElement`. Child order inside `<staticText>`: `reportElement → box(opt) →
textElement(opt) → text`. Inside `<textField>`: `reportElement → box(opt) → textElement(opt) →
textFieldExpression`. Inside `<image>`: `reportElement → box(opt) → imageExpression`.

### Rule 9 — Data adapters and subdatasets (CSV-backed subreports)
Crystal subreports with their own data source → JasperReports subDataset + CSV data adapter.
Every subDataset needs all five: `<subDataset name="...">` declared after `<variable>`s and
before `<background>`; `<field>` declarations inside it; a `<datasetRun subDataset="Name"/>`
(self-closing — see the CSV-vs-JDBC distinction below) inside the `componentElement` that uses
it; a `.jrdax` adapter file **co-located with the JRXML**; a `.csv` data file **co-located with
the JRXML**. CSV rules: first row = column headers exactly matching field names (case-sensitive);
multi-line values must be quoted.

**Path rule (mandatory):** every `.jrdax`'s internal `<location>` element (not `<fileName>` —
verify the real element name by opening the file) must be a **bare filename**, no folder prefix,
no absolute path — `MyData.csv`, never `data\MyData.csv` or `C:\...\MyData.csv`. JasperReports
resolves relative paths from the JRXML's own folder at runtime. **Studio Preview resolves
`.jrdax` paths relative to the project root, not the JRXML folder** — a path can work in Studio
Preview and still fail at runtime. Bare filenames are the only setting that's correct both ways.

**CSV vs. JDBC datasetRun — the single most damaging silent failure:** when the adapter is
declared via the `net.sf.jasperreports.data.adapter` property on the `componentElement`'s
`reportElement`, the `datasetRun` must be **self-closing**, `<datasetRun subDataset="Name"/>`,
with **no** `connectionExpression` and **no** `$P{REPORT_CONNECTION}`. A CSV file adapter is not
a database connection — passing a connection expression to it renders the **entire report
blank, with no error anywhere.** (A JDBC-backed subDataset does use `connectionExpression` — see
Rule 15's skeleton, which is JDBC-flavoured on purpose; know which of the two your subreport is.)

`whenNoDataType` options: `NoPages` (default, blank output), `BlankPage`, `AllSectionsNoDetail`
(all bands render except detail — use with an "Empty Records" 0-row adapter for a static report
with no detail band), `NoDataSection` (renders `<noData>` band only).

**Parameters need a `defaultValueExpression`,** on every one, including LOGO/date/label fields —
without it, Jaspersoft Studio Preview shows blank for all parameter-driven content even when the
JRXML itself is correct. For an image parameter (e.g. LOGO) default it to the bare filename that
will sit co-located in the output folder at runtime.

### Rule 10 — Fonts (PDF rendering is the trap, not screen rendering)
Crystal uses Windows GDI fonts; JasperReports uses Java AWT for screen + iText for PDF — they
render differently, and PDF is the one that silently fails.

**Bold-italic on Arial/Helvetica silently drops the italic in PDF** (no error; bold renders,
italic doesn't) — neither has a bold-italic variant in the base-14 PDF spec. Never use
Arial/Helvetica for bold-italic text. **Use `DejaVu Sans`** instead — it ships bundled with
JasperReports 7.0.3 (no extension JAR needed) and renders bold-italic correctly in both Studio
Preview and PDF export.

Safe PDF built-ins with regular/bold/italic **separately** (not combined): `Helvetica`,
`Times-Roman`, `Courier`. If Arial is specifically mandated: register a
`jasperreports-fonts` extension JAR + `jasperreports_extension.properties`, only then do
`isBold`/`isItalic` behave correctly on it in PDF.

**Remove `pdfFontName`/`isPdfEmbedded`/`pdfEncoding` from every `<font>` element** — see Rule 7.

### Rule 11 — Page number / page count
`Page N of M` requires `evaluationTime="Report"` on the textField — without it, `$V{PAGE_COUNT}`
always renders 0.
```
<![CDATA["Page " + $V{PAGE_NUMBER} + " of " + $V{PAGE_COUNT}]]>
```
**Critical exception:** with `whenNoDataType="AllSectionsNoDetail"` and no detail band (a static
single-page report), `$V{PAGE_COUNT}` returns 0 **even with `evaluationTime="Report"`.** Fix: use
`$V{PAGE_NUMBER}` for **both** halves — `"Page " + $V{PAGE_NUMBER} + " of " + $V{PAGE_NUMBER}` —
which correctly renders "Page 1 of 1" under `ignorePagination="true"`.

### Rule 12 — Multi-page patterns
- **Pattern A** — detail-driven, standard tabular report; header/footer repeat every page.
- **Pattern B** — static single-page (no detail rows): needs **all four**, together:
  `ignorePagination="true"` (bypasses the engine's pre-allocation check that otherwise pushes
  summary to page 2 when bands exactly sum to page height), `titleNewPage="false"`,
  `summaryNewPage="false"`, `summaryWithPageHeaderAndFooter="true"` (renders the page footer on
  the summary page). Data adapter: "Empty Records" (0 rows). `whenNoDataType="AllSectionsNoDetail"`.
- **Pattern B-2** — static 2-page: title on page 1 (`titleNewPage="false"`), summary forced to
  page 2 (`summaryNewPage="true"`, `summaryWithPageHeaderAndFooter="true"` if it needs its own
  header/footer).
- **Pattern C** — group-driven: `isStartNewPage="true"` per group, with `isResetPageNumber="true"`
  if the counter should restart per group.
- **Pattern D** — mixed; always verify geometry for the worst-case page (every co-present band).

### Rule 13 — 20 real conversion errors (symptom → cause → fix)
| # | Symptom | Cause | Fix |
|---|---|---|---|
| 1 | Invisible text | Missing CDATA | Wrap in `<![CDATA[...]]>` |
| 2 | "Page X of 0" | Missing `evaluationTime="Report"` | Add it to the PAGE_COUNT textField |
| 3 | Blank output, no pages | Wrong/missing `whenNoDataType` or adapter | `AllSectionsNoDetail` + "Empty Records" adapter |
| 4 | JRException on open | Banned `jr:` element present | Remove all `jr:`-prefixed elements/namespace |
| 5 | XSD band-order failure | Bands out of sequence | Reorder per Rule 2 |
| 6 | Element overflows band | `y+height > band height` | Reduce element or grow band |
| 7 | Bold/italic missing in PDF | Font not registered as extension JAR | Register font, or switch to a PDF built-in |
| 8 | Table has no data | `.jrdax`/CSV not co-located with JRXML | Copy both next to the JRXML |
| 9 | `&#10;` shows as literal text | HTML entity inside CDATA | Use the real newline character |
| 10 | Header missing on summary page | `isSummaryWithPageHeaderAndFooter` not set | Set it `true` |
| 11 | `forecolor` has no effect | Placed on `<font>` instead of `<reportElement>` | Move it |
| 12 | Wrong `datasetRun` syntax inside `jr:table` | `datasetName=` used, or wrong child element | `subDataset=` + `<connectionExpression>` (JDBC case) |
| 13 | Whole report blank | `connectionExpression` used with a CSV adapter | Self-closing `<datasetRun subDataset="Name"/>`, no connection expr |
| 14 | Studio preview blank for parameters | No `defaultValueExpression` | Add one to every parameter |
| 15 | Background colour invisible | `backcolor` set without `mode="Opaque"` | Add `mode="Opaque"` to the same `reportElement` |
| 16 | Title/logo appear mid-page | `isTitleNewPage` wrong, or title content overlapping pageHeader zone | Set `isTitleNewPage="false"`, re-check y-positions |
| 17 | CSV silently loads zero rows | `<element kind="component">` never converted; or `.jrdax` path has a folder prefix; or CSV not co-located at runtime | Convert to `<componentElement>`; bare filename in `.jrdax`; copy CSV to output folder — **verify with the exported PDF, not just Studio Preview** |
| 18 | `JacksonRuntimeException: Unrecognized field isTitleNewPage` | Added `is` prefix inside **compact**-format file | Remove the prefix in compact format (see Rule 0A) |
| 19 | Bold-italic missing in PDF (specific case) | Arial/Helvetica + isBold + isItalic, no extension JAR | Switch to `DejaVu Sans` |
| 20 | Content looks rotated 90° | Studio Preview display artefact on some landscape builds | Not a real defect — verify via File → Export → PDF instead |

### Rule 14 — Mandatory 14-scan pre-save checklist
Every JRXML save (new file, fix, or update) requires all 14 scans to return **zero violations**
before saving — never save with a known violation. Use `findstr /i /n "term" file.jrxml` if a
Python-based validator isn't available; never install new tooling as a workaround.

1. **Namespace** — 0× `xmlns:jr` or `components.xsd` at root; 0× unlisted `jr:` prefix.
2. **Font attributes** — 0× `forecolor`/`backcolor` inside `<font>`; 0× `pdfFontName`/
   `isPdfEmbedded`/`pdfEncoding`; 0× `backcolor` without a sibling `mode="Opaque"`.
3. **Banned attributes anywhere** — 0× `isStretchWithOverflow`, `verticalTextAlignment` inside
   `<textElement>`, `font.fontSize`, `isTitleNewPage`/`isSummaryNewPage` (if compact format),
   `fontName=`/`fontSize=`/`x=` directly on `<staticText>`/`<textField>`, `vTextAlign=` anywhere.
4. **Banned elements** — 0× undeclared `jr:table`, `<dataset>`, `<reportFont>`, `<subreport>`,
   `<element kind="component">`, `</element>` (generic closing tag).
5. **Banned text values** — 0× `&#10;`, `&#179;`, `&#176;`.
6. **Missing CDATA** — 0× any of Rule 6's elements without `<![CDATA[...]]>`.
7. **Declaration order** — `<subDataset>` after all `<variable>`s and before `<group>`/
   `<background>`; `<parameter>` before `<subDataset>`.
8. **Geometry** — 0× element overflow (y+h, x+w); band-height+margin sum = pageHeight exactly.
9. **Root element attributes** — correct set present (format-dependent names, see Rule 0A):
   title/summary-new-page flags, `summaryWithPageHeaderAndFooter`, `ignorePagination`,
   `whenNoDataType` — and confirm the *opposite* format's naming is absent (0 occurrences).
10. **PAGE_COUNT** — every occurrence has `evaluationTime="Report"`.
11. **Band attributes** — every `<band>` has only `height`/`splitType`, nothing else.
12. **datasetRun correctness** — 0× `datasetName=`, 0× `<datasetParameter>`/
    `<datasetParameterExpression>`, 0× stray `connectionExpression` on a CSV-backed run;
    `subDataset=` present on every `<datasetRun>`.
13. **componentElement completeness** — every `jr:table` has a `<datasetRun subDataset="...">`, at
    least one `jr:column`, and `x="0" y="0"` on every element inside `jr:columnHeader`/
    `jr:detailCell` (no `<band>` wrapper inside a cell).
14. **`.jrdax` file integrity** — every co-located `.jrdax`'s `<location>` is a bare filename
    matching a CSV actually present in the output folder — no folder prefix, no absolute path.

Report format (paste before the final confirmation statement on every save):
```
FULL-FILE XSD SCAN RESULTS
SCAN 1  Namespace              : ✅ 0 violations
SCAN 2  Font attributes        : ✅ 0 violations
... (all 14) ...
ALL 14 SCANS PASSED — FILE IS CLEAN
```

### Rule 15 — Component table structure (exact skeleton, JDBC-flavoured)
`jr:` prefix is required **only** on: `jr:table`, `jr:column`, `jr:columnHeader`, `jr:detailCell`,
`jr:tableHeader`, `jr:columnFooter`, `jr:groupHeader`, `jr:groupFooter`. Everything else
(`componentElement`, `datasetRun`, `connectionExpression`, `reportElement`, `staticText`,
`textField`, `textElement`, `font`, `box`, `image`, `line`, `text`, `textFieldExpression`,
`imageExpression`, `printWhenExpression`) takes **no** prefix.

Three facts about `datasetRun` inside a `jr:table` (JDBC case) — never wrong: no `jr:` prefix;
attribute is `subDataset=` not `datasetName=`; child is `<connectionExpression>`, never
`<datasetParameter>`/`<datasetParameterExpression>`. (For the CSV-adapter case, see Rule 9 — the
`datasetRun` there is self-closing instead, with no `connectionExpression` at all — know which
kind of subreport you're editing.)

Coordinates inside `jr:columnHeader`/`jr:detailCell` are their **own** coordinate space — every
child `reportElement` uses `x="0" y="0"`, never `y > 0`, and never wraps cell content in a
`<band>`.

```xml
<componentElement>
  <reportElement x="[x]" y="[y]" width="[totalTableWidth]" height="[totalTableHeight]">
    <property name="net.sf.jasperreports.data.adapter" value="[AdapterName].jrdax"/>
  </reportElement>
  <jr:table
    xmlns:jr="http://jasperreports.sourceforge.net/jasperreports/components"
    xsi:schemaLocation="http://jasperreports.sourceforge.net/jasperreports/components http://jasperreports.sourceforge.net/xsd/components.xsd">
    <datasetRun subDataset="[SubDatasetName]">
      <connectionExpression><![CDATA[$P{REPORT_CONNECTION}]]></connectionExpression>
    </datasetRun>
    <jr:column width="[colWidth]">
      <jr:columnHeader height="[h]" rowSpan="1">
        <staticText>
          <reportElement x="0" y="0" width="[colWidth]" height="[h]"/>
          <box><pen lineWidth="0.5" lineColor="#000000"/></box>
          <textElement textAlignment="Center" verticalAlignment="Middle">
            <font fontName="Helvetica" size="8" isBold="true"/>
          </textElement>
          <text><![CDATA[Column Header]]></text>
        </staticText>
      </jr:columnHeader>
      <jr:detailCell height="[h]" rowSpan="1">
        <textField isBlankWhenNull="true">
          <reportElement x="0" y="0" width="[colWidth]" height="[h]"/>
          <box><pen lineWidth="0.5" lineColor="#000000"/></box>
          <textElement textAlignment="Right" verticalAlignment="Middle">
            <font fontName="Helvetica" size="8"/>
          </textElement>
          <textFieldExpression><![CDATA[$F{FIELD_NAME}]]></textFieldExpression>
        </textField>
      </jr:detailCell>
    </jr:column>
  </jr:table>
</componentElement>
```

### 6 stop conditions — never proceed past these without explicit instruction
1. **Data loss risk** — about to delete/replace a `subDataset`, `datasetRun`, `field`, `$F{}`
   expression, adapter property reference, or any data-bound `componentElement`.
2. **Content deletion risk** — about to delete a visual element/band content to fix geometry.
3. **Architecture change risk** — page size/orientation change, moving content between bands
   without instruction, parameter-vs-field data source change, changing the page pattern
   (A/B/C/D), changing element syntax style without instruction.
4. **Geometry cannot be satisfied** — content mathematically doesn't fit even at minimum font.
5. **Repeated failure** — same validation error survives 2 separate fix attempts — stop
   completely, do not attempt a third fix blind.
6. **Structure not understood** — a dataset run / component table / subreport section isn't
   fully understood before editing — never guess or simplify to make it easier.

Each triggers a **Stop Report** (Condition / Triggered by / Risk / Current state / What works /
What is broken / Options / Recommendation / Awaiting) and a full stop — no further edits until
the owner responds. Safe operations that do **not** need a stop report: band-height tweaks,
y/height fixes for overflow, adding a missing root `xmlns`, reordering elements for XSD sequence,
adding a brand-new parameter, adding CDATA to existing text, removing banned PDF-font attributes,
fixing v6→v7 attribute/element renames.

### Final pre-save checklist (condensed)
Namespace/syntax clean (Rule 1/6/7) → structure correct (band order, declaration order, band
attrs, `evaluationTime`, `whenNoDataType`) → geometry calculated for **this specific report**
(Rules 1-4 all satisfied, not approximated) → content completeness (every Crystal section/
formula/parameter/field/special-field/subreport has its JasperReports equivalent, every adapter/
CSV co-located) → file integrity (full 14-scan report pasted, well-formed XML, opens in Jaspersoft
Studio 7.0.3 with **zero** errors and **zero** warnings, Preview renders every page correctly).

---

## PART B — Supplementary background (from this repo's unexecuted JR-01→04 task prompts)

These four files (`DeepDiveLearnings/extracted/JR-01` through `JR-04`) define a self-learning
curriculum that was **never actually executed** — no `deep_dive/JR-*` output exists, and
`PROGRESS_LOG.md` has no JR entries. Their content below is the general JasperReports domain
knowledge implied by their learning objectives — genuinely useful background, but **not
independently verified** the way Part A is. Where Part A already covers a point more precisely
(fonts, banned attributes, page count), Part A's version is the one to follow.

**JR-01 — Fundamentals:** JRXML fill→compile→export pipeline; `.jrxml` (source) vs `.jasper`
(compiled); 9 standard bands and their render order (see Rule 2 above for the authoritative
order); `reportElement` coordinate system (pixels, origin top-left); `stretchType` options
(`NoStretch`, `ContainerBottom`, `ContainerHeight`, `ElementGroupBottom`, `ElementGroupHeight`);
`splitType` behaviour differences (`Stretch`/`Prevent`/`Immediate`); built-in variables
(`PAGE_NUMBER`, `PAGE_COUNT`, `COLUMN_NUMBER`, `REPORT_COUNT`, `COLUMN_COUNT`); null-safety
pattern `$F{field} != null ? $F{field} : ""`.

**JR-02 — Data sources & expressions:** the 6 data-source types (`JREmptyDataSource`,
`JRBeanCollectionDataSource`, JDBC, `JRCsvDataSource`, `JRJsonDataSource`, `JRXmlDataSource`) and
when to use each; `<queryString language="sql|hql|xpath|jsonql">`; `$P{param}` (safe) vs
`$P!{param}` (direct injection — SQL-injection risk, avoid) vs `$X{IN, field, param}` (multi-value
IN clause); variable `calculation` types (`Nothing`, `Count`, `DistinctCount`, `Sum`, `Average`,
`Lowest`, `Highest`, `StandardDeviation`, `Variance`, `First`, `System`) and `resetType`
(`Report`, `Page`, `Column`, `Group`, `None`) with matching `incrementType`; groups need
`resetType="Group"`/`resetGroup=` to tie a variable to a specific group; **sorting must happen in
the SQL query, not in JasperReports** — group breaks assume pre-sorted data.

**JR-03 — Advanced layout:** `<subreport>` anatomy (`subreportExpression`,
`dataSourceExpression`, `<subreportParameter>`, `<returnValue>`) — **note this conflicts with
Part A's project convention of using subDataset+componentElement instead of `<subreport>`; Part A
wins for this project.** Subreports must compile before the master (dependency order). Crosstabs:
`<rowGroup>`/`<columnGroup>`/`<measure>`, `whenNoDataCell`, alternating-row styling via
`<conditionalStyle>`. Charts: bar/line/pie/area/scatter/bubble/gantt/thermometer/meter types,
`<chartCustomizerClass>` for advanced customisation.

> ⚠ **Verified correction (web search, 2026-08-29):** JasperReports 7's underlying JFreeChart
> was upgraded to 1.5.4, which **dropped 3D chart support**. Pie 3D / Bar 3D / Stacked Bar 3D
> charts still load and run but render as flat 2D — their 3D effect is silently ignored. If a
> Crystal Report source uses a 3D chart, expect (and disclose) a visual downgrade to 2D, not a
> broken report — this is expected JasperReports 7 behaviour, not a conversion defect to "fix."

Export config: PDF via `net.sf.jasperreports.export.pdf.*` properties (page size, orientation,
compression, encryption via `net.sf.jasperreports.export.pdf.encrypted`); Excel via
`net.sf.jasperreports.export.xls.*` (`isOnePagePerSheet`, `isRemoveEmptySpaceBetweenRows/Columns`,
per-band sheet naming) — merged cells can break Excel formulas downstream, a known pitfall.

**JR-04 — Production & Claude Code patterns:** JasperReports Server REST API
(`/jasperserver/rest_v2/`) — `GET /resources` (browse repo), `POST /reports/{uri}.pdf|.xlsx` (run
report), `GET /reports/{uri}/inputControls` (get parameters), `PUT /resources/{uri}` (upload
JRXML), async execution via `POST /reportExecutions` + polling. Relevant if/when INPEX's actual
JasperReports Server needs a report deployed via API rather than manual upload — not needed for
the local-sandbox JRXML authoring/testing phase this task is currently scoped to.

---

## PART C — Verified-from-web supplementary facts (2026-08-29 search, gap-fill only)

These fill gaps neither Part A nor Part B covers; none contradict Part A.

- **JasperReports 7.0+ cannot load pre-v7 `.jrxml`/`.jrtx` files directly** — the v7 refactor
  (done for the Jakarta migration) replaced the old Apache-Commons-Digester-based parser with
  Jackson XML serialization, and deliberately broke backward compatibility for both compiled
  `.jasper` files and source `.jrxml`/`.jrtx` files. **If any existing Jasper report referenced
  for this INPEX conversion work was authored under JasperReports 6 or older, it cannot be opened
  directly in 7.0.3 — it must first be converted using Jaspersoft Studio 7+ itself** (open old
  file in Studio 7, re-save). This is a genuinely new fact worth checking before assuming any
  existing `.jrxml` in scope is usable as-is.
  [Jaspersoft/jasperreports README](https://github.com/Jaspersoft/jasperreports/blob/master/README.md)
- **General Crystal formula ↔ Java expression conceptual mapping** (beyond Part A's element-level
  table): Crystal's `IIF(cond, trueVal, falseVal)` ≈ Java's ternary `cond ? trueVal : falseVal`
  (both trueVal/falseVal must be constants/variables/functions in Crystal, same practical
  constraint applies to a JasperReports expression that must return one type). Crystal's
  `ToText(value, decimals, separator)` ≈ `new java.text.DecimalFormat(...).format(value)` or
  `String.valueOf(value)`. Crystal's typed shared/running variables (`NumberVar`, `StringVar`,
  `CurrencyVar`, evaluated `WhilePrintingRecords`) ≈ JasperReports `<variable>` with `resetType`
  — the placement rule carries over conceptually: a Crystal formula placed in the Details section
  for per-record evaluation vs. a Group Footer for an accumulated total maps directly to a
  JasperReports variable's `resetType="None"`(per-record read) vs `resetType="Group"` design.
  [Confluence: Useful Crystal Reports functions](https://ehgdev.atlassian.net/wiki/spaces/SYNMAIN/pages/2294718098/Useful+Crystal+Reports+functions),
  [i-net Clear Reports: Basic vs Crystal syntax](https://docs.inetsoftware.de/reporting/help/SyntaxComparison/p/basic-syntax-crystal-syntax)

---

## PART D — Hands-on lessons from the R07.012 FC Lifting Report conversion (2026-08-29)

This is the first real, completed conversion done under this doc (Crystal → JasperReports 7.0.3,
INPEX Ichthys "FC Lifting Report"). Everything below is **verified against a real compile→fill
(live Oracle sandbox)→PDF-export pipeline** via a standalone Java class calling
`JasperCompileManager.compileReport()` directly — **no Jaspersoft Studio was used or available in
this environment.** That absence is the source of the biggest correction to Part A below.

### D0 — ⚠ MAJOR correction to Rule 0A: compact format is not just tolerated, it's REQUIRED here
Rule 0A calls Studio's compact format ("`<element kind="X">`", no `xmlns`) **FORBIDDEN** and the
standard `xmlns` format **REQUIRED**. In this project's actual runtime — Maven-resolved
`net.sf.jasperreports:jasperreports:7.0.3`, loaded via `JasperCompileManager.compileReport(String
path)`, no Studio anywhere in the pipeline — **the standard xmlns-declared format failed to load
even a trivial file**, while the compact `kind="X"` format compiled, filled, and exported
correctly every time. Rule 0A is Studio-specific guidance from a different (tier-1) project that
assumed Jaspersoft Studio as the authoring/verification tool. **When there is no Studio in the
pipeline — just a raw Java/Maven JasperReports engine — compact format is the one that works, and
the whole file must stay consistently compact.** Before starting a new conversion, check whether
Studio is actually part of *this* pipeline; if not, use compact format from line 1, not the
standard skeleton in Rule 15/1.

### D1 — The single most damaging bug this session: opaque cells silently lose their own border
**Symptom:** any `<staticText>`/`<textField>` with `mode="Opaque"` + `backcolor` (i.e. any filled
header/label cell) that also declares a `<box>` border via its style renders the fill correctly
but the border **never appears** — not faint, not partial, completely absent — even though the
border is present and well-formed in the compiled JRXML and even in the raw PDF content stream.

**Root cause (confirmed via raw content-stream byte inspection, not assumption):** for this
element type, the engine emits the border **stroke commands before the fill command**, in the
same element's paint sequence. The fill is opaque, so it paints directly over the border that was
just drawn a few operators earlier. This is true regardless of `topPen`/`bottomPen`/`rightPen`
vs a single `<pen>`, regardless of color, regardless of pen width — **it is not fixable by
changing the box definition on an opaque text element.**

**The fix — the ONLY reliable one found:** stop drawing fill+border on the text element at all.
Use the pattern below (also independently confirmed as the real-world convention in a completely
different, already-working JRXML the owner supplied from another Ichthys report):
```xml
<!-- fill + border, self-contained, drawn first -->
<element kind="rectangle" x="X" y="Y" width="W" height="H" mode="Opaque"
         backcolor="#454087" forecolor="#D6D6D6"><pen lineWidth="1.0"/></element>
<!-- text, transparent, same coordinates, drawn on top -->
<element kind="staticText" x="X" y="Y" width="W" height="H" style="SomeTransparentStyle"
         hTextAlign="Center" vTextAlign="Middle">
    <text><![CDATA[Label]]></text>
</element>
```
For `kind="rectangle"` in the compact dialect, `backcolor` is the fill color and `forecolor` is
the border/pen color (confirmed via the Jackson `UnrecognizedPropertyException` trick below) — this
is the opposite of what you might guess from `<font>` semantics. Give the transparent overlay
style `mode="Transparent"` and no `backcolor`/`box` at all; it exists purely to hold the font/color
for the text. **Every opaque header/label cell in a converted report should use this two-element
pattern from the start** — do not attempt a single opaque text element with a border and hope it
renders; it will not, on this engine.

### D2 — Freestanding `<line>` elements are NOT a safe substitute for box borders
Needing a divider where D1's bug applies, the instinct is to add a separate `<element
kind="line">` at the boundary. **Avoid this if any box-pen border exists anywhere near it.**
A `kind="line"` element with `width="1" height="H"` compiles to a *diagonal* path from `(x,y)` to
`(x+1,y+H)` with a centered stroke — its visual center lands at approximately `x+0.5`, not `x`.
A box-pen border on a real content element, by contrast, renders its stroke exactly at the
element's declared edge (`x`, no offset). Mixing the two for what's meant to be one continuous
vertical grid line (e.g. a line divider in a header band, meeting a real cell's own border in the
band below it) produces a persistent ~0.5pt sub-pixel misalignment that reads as a "doubled" or
"thickened" line at the seam — confirmed by direct visual comparison, not a rendering-tool
artifact. **This cannot be fixed by nudging the line's integer `x` value** (the achievable
positions are `x` or `x+1`, never the exact `x+0.5` needed to match a box-pen edge). The fix is
D1's rectangle+overlay pattern, which needs no freestanding line at all — the rectangle's own
border IS the divider, drawn at the exact declared edge, matching every other box-pen border in
the document with zero cross-element coordination required.

### D3 — Adjacent-column 1pt x/width overlaps double every shared border
A common artifact carried over from Crystal column-width recon: declaring column N+1's `x` 1pt
*before* column N's own right edge (e.g. Date `x=0 width=49`, next column `x=48` not `x=49`).
Each column's own box independently draws all 4 sides, so every shared boundary gets drawn
**twice, 1pt apart** — invisible in isolation but renders as vertical grid lines roughly twice as
thick as horizontal ones once printed/zoomed. **Fix:** on the shared cell style's `<box>`, declare
only `<topPen>`/`<bottomPen>`/`<rightPen>` — omit `<leftPen>` entirely. Each cell then relies on
its left neighbor's `rightPen` for the shared line; only the very first column in a row (nothing
to its left) needs its own explicit 4-sided box (matching how Crystal's own "Date" column
rendered as a standalone override in this report). This is a report-wide style change (one line
per style), not a per-element fix — apply it up front to every column-style class before building
detail rows, not after noticing double lines.

### D4 — Verification pitfalls: don't trust one tool/one pattern, confirm with real bytes
Three separate false conclusions this session, each caused by an unverified assumption in the
*checking* method, not the JRXML itself:
1. **PyMuPDF `page.get_drawings()` can miss real strokes** depending on how you filter/interpret
   its output (e.g. assuming a specific text-pattern search catches every draw call). When a
   check says "this element isn't rendering," **also dump the raw content stream**
   (`page.read_contents()`, decode `latin-1`) and search for the actual operator sequence before
   concluding anything is missing — do not trust a single negative from one extraction method.
2. **`<rectangle>` fills compile to bezier-curve paths** (`m ... l ... c ... f`), **not** the `re`
   (rectangle) operator — a raw-byte search assuming `re\nf` will silently find nothing even when
   the fill is present and correct. Search for the fill-color-set command (`R G B rg`) followed by
   a closed `m/l/c` path and `f`, not `re`.
3. **A page can have `rotation=90` with a *portrait* mediabox** even though it displays as
   landscape — raw coordinates from `get_drawings()`/`get_text()` are in the page's own unrotated
   space. Always transform through `page.rotation_matrix` before comparing/reasoning about
   coordinates, or genuinely-present content will look absent or wildly mispositioned.
   **Critical detail found on a later report (R07.014): transform ALL FOUR corners of a bbox
   through the matrix and take min/max — not just the raw `(x0,y0)` corner.** Under a 90°
   rotation, the corner that was originally "top-left" is not necessarily the displayed top-left
   anymore, so transforming only that one point gives a systematically wrong x for elements of
   varying width/height (each one wrong by a *different* amount) — this looks exactly like a real
   misalignment bug (several footer fields appearing shifted by inconsistent amounts) but is
   purely a measurement-script artifact. If a rotated-page comparison shows inconsistent,
   varying-magnitude offsets across otherwise-unrelated elements, suspect the measurement method
   before the JRXML.

**When genuinely unsure whether a compact-format property/element is valid, don't guess against
standard-format docs** — add an obviously-wrong attribute name to the element and read the
resulting `com.fasterxml.jackson.databind.exc.UnrecognizedPropertyException` message; it lists
every real, accepted property name for that Java class (e.g. confirmed this way for
`JRDesignLine` and `JRDesignRectangle` mid-session). This is faster and more reliable than
inferring from standard-format documentation, which uses different attribute names entirely
(Rule 0A).

### D5 — Practical workflow notes
- **Live output file gets locked by the PDF viewer** (Acrobat) the moment it's opened — every
  rebuild after that fails with `FileNotFoundException` until the viewer closes the file. Keep a
  disposable alt-filename ready for "let me verify this change" builds so you're not blocked
  waiting on the canonical output path.
- **Backup the JRXML to a timestamped copy in the same folder before every edit round**, not a
  separate temp directory — makes rollback trivial and keeps the backup discoverable next to the
  file it protects. Delete superseded backups once a round is confirmed good; don't let them
  accumulate past the current working state.
- A rasterized visual render (`page.get_pixmap()` at 2-4x zoom, cropped to the area in question)
  caught every real defect this session accurately, once the verification method itself (D4) was
  sound — it is the most trustworthy single check available without Jaspersoft Studio installed.

---

## What's still missing / next steps

- The actual **Crystal Reports source file** (`.rpt`) for the one report we're converting hasn't
  been identified yet in this session — need its name/location before recon can start.
- **Local sandbox test plan** not yet defined: need to confirm Jaspersoft Studio 7.0.3 is
  installed locally, and where the converted `.jrxml`/output folder should live relative to this
  repo (a `screens/`-style bundle under a new workstream folder would match this repo's existing
  convention, e.g. `workstreams/crystal-to-jasper-conversion/<report-name>/`).
- `DeepDiveLearnings/Playwright_RobotFramework_JasperReports_files.zip` exists in this repo and
  hasn't been opened yet — may contain additional prior-session material relevant to this task;
  worth checking before starting the actual conversion.
- The INPEX live datasource (`C:\Projects\INPEX\datasource.md`) is explicitly **not** in scope for
  this phase — testing is local-sandbox only, per the owner's instruction. Do not connect to it
  without a separate, explicit go-ahead (see the standing "no AI access to customer ECaaS without
  approval" rule — INPEX isn't yet covered either way, so treat it as requiring the same
  confirmation Woodside requires until told otherwise).

## PART E — Page-per-group ("Pattern C") mechanics, from the R07.018 Provisional Lifting
Program conversion (2026-08-30) — the first multi-page report in the batch (one page per
forecast month)

**E1. Compact-format `<group>` property names (Jackson-error-discovered, same technique as
Part D's element `kind`s):**
- Page-break-per-group: `startNewPage="true"` on `<group>` — **not** `isStartNewPage` (the name
  used in JasperReports' full XSD-based XML; the compact/Jackson deserializer here uses the
  shorter Java-bean property name instead).
- Group expression: `<expression>...</expression>` nested directly inside `<group>` — **not**
  `<groupExpression>`. The Jackson `UnrecognizedPropertyException` lists the real accepted
  property set every time (`"minHeightToStartNewPage", "footerPosition", "resetPageNumber",
  "name", "groupHeader", "startNewPage", ..., "expression", "groupFooter", ...`) — read it
  rather than guessing from general JasperReports docs, which describe the different XSD schema.
- `groupHeader`/`groupFooter` bands must be **nested inside `<group>...</group>`**, not top-level
  siblings of `<detail>`. A top-level `<groupFooter name="G_MONTH">` element parses without
  error in this engine but is structurally wrong (silently creates a second, unconnected
  element) — re-check the Jackson known-properties list if unsure whether something is a
  top-level report element or a nested group property.
- Variables that reset per group need `resetType="Group" resetGroup="<name>"` on the
  `<variable>` element (matches the group's own `name` attribute).

**E2. `<title>` only ever prints on page 1 — even across group-driven page breaks.** This is a
JasperReports design constant, not a bug: the title band renders once at the very start of the
report regardless of how many `startNewPage` group breaks follow. If the reference PDF shows a
full title/subtitle block (with page-varying content, e.g. a per-page month name) on EVERY
page, the `<title>` band cannot be used for it — merge the title's elements into the
**`pageHeader`** band instead (which genuinely repeats every page), shifting the rest of the
pageHeader's own content down by the title block's height. Apply this proactively on every
report in this multi-page family — don't wait to rediscover it after a blank-title second page.

**E3. Verifying group/page-break behavior needs real multi-group data — `JREmptyDataSource`
can't do it.** A group `<expression>` that parses a data field (e.g.
`new SimpleDateFormat("yyyy-MM").format($F{DAYTIME})`) throws on `JREmptyDataSource`'s all-null
fields. Use a small in-memory `JRMapCollectionDataSource` (2+ rows spanning 2+ distinct group
values) to prove the page-break and title-repeat behavior actually works, before considering a
multi-page report's layout verified. A single-row or all-null data source will silently produce
only 1 page and hide title/group-header repeat bugs entirely.

**E4. A per-group "Opening Inventory" row (group header) works the same way as the
per-report Opening Inventory row seen in R07.012/014/016** — just declare it inside
`<groupHeader><band>...</band></groupHeader>` instead of a standalone `<columnHeader>`, and
reference the current record's own field directly (e.g. `$F{OPENING_INVENTORY}`) — JasperReports
evaluates a groupHeader band using the first record of that group, so no special "first value of
group" variable machinery is needed for this specific case.

## PART F — A silently-dropped-text bug from the R10.002/R10.003 "calculation form" builds
(2026-08-30)

**F1. A `staticText` element whose declared `height` is too small for its font size can be
SILENTLY OMITTED FROM THE RENDER ENTIRELY — not clipped, not truncated, just absent, with zero
compile warning/error.** Found on R10.002 (undetected until R10.003 hit the same pattern and
got compared more carefully) and R10.003: three section-label elements (9pt bold Arial) declared
with `height="10"` never appeared anywhere in the exported PDF's text layer (confirmed via
`page.get_text('text')`, not just a targeted dict scan — the string was absent from the whole
page). Increasing `height` to `14` made the same elements render immediately, with no other
change. **Rule: give any bold/larger-than-8pt static or dynamic text element a height with real
margin above the nominal font size (roughly font-size + 4-5pt minimum) — a "looks close enough"
height is not safe, it can drop the element outright.** This is exactly the class of defect the
project's "never assume — verify" rule exists for: a compile that reports zero warnings is not
proof the visible output is correct; the ONLY proof is reading the exported PDF's actual text
content, which is why `page.get_text('text')` (whole-page plain text, not just a targeted
y-range dict scan) should be part of the standard post-build check for every report, not only
the coordinate-comparison scan used for data columns.

**F2. Once the missing-text bug above is fixed, the same elements can render several points
lower than their declared `y` — without any further XML change.** Observed on both "Price
Formula" and "Price Formula Components (per MT)" labels: declared at y=214/y=280, rendered at
y≈241/y≈307 (an unexplained +26-27pt offset, consistent across both elements, using the same
style/height/vTextAlign combination). The offset happened to land almost exactly on the
reference PDF's real position in this instance — but this should be treated as coincidental,
not relied upon. **Always re-measure the ACTUAL rendered position after any height/style change
to a previously-broken element — do not trust the declared XML `y` once an element has needed
this kind of fix.**

## Part G — static (non-repeating) 2-page reports, `<title>`+`<summary>`, and a duplicate-attribute trap (from R10.006)

**G1. `<title>` and `<summary>` bands can carry two entirely DIFFERENT static pages of content**
(no repeating detail row needed) — useful when a report is genuinely two fixed pages rather than
a repeating grid. Put page 1's content in `<title>`, page 2's in `<summary>`. The 2-page split
does NOT need a repeating field to group on (unlike Part E's page-per-month mechanism, which
does need one).

**G2. The page break between `<title>` and `<summary>` in this scenario is produced by NATURAL
BAND-HEIGHT OVERFLOW, not by an explicit `<element kind="break" type="Page"/>`.** Verified via an
isolated minimal repro (`minitest.jrxml`, both bands deliberately small enough to fit on one
page): the `break` element compiled without error (`type="Page"` and `type="PAGE"` both accepted
per Jackson's known-property list) but produced ZERO page break — both bands rendered on the same
single page regardless. The real, working mechanism: give `<title>` a declared height close to
the full page height, and `<summary>` (with `splitType="Prevent"`, making it an atomic
non-splittable unit) a height that cannot fit in the remaining space on page 1 — JasperReports is
then forced to place the whole `summary` band on a fresh page. **Do not rely on the `break`
element alone to force a page split in this engine build — verify with a minimal repro before
trusting it, and prefer sizing title/summary bands so natural overflow does the work.**

**G3. A `<summary>` band suppresses `<pageHeader>`/`<pageFooter>` on its own page by default** —
set `summaryWithPageHeaderAndFooter="true"` on the root `<jasperReport>` element to make the
footer print on the summary's page too. Also set `titleNewPage="false"` (default already, but
worth being explicit) so the title page keeps its own footer. Both attribute names confirmed
real via a deliberate Jackson `UnrecognizedPropertyException` (the report-root's 51 known
properties list includes `summaryWithPageHeaderAndFooter`, `titleNewPage`, `summaryNewPage`).

**G4. A DUPLICATE XML ATTRIBUTE ON AN ELEMENT SILENTLY BREAKS IT WITH ZERO COMPILE ERROR** — a
careless `sed` substitution meant to change one attribute's value (bumping `height="8"` to
`height="12"` on a footer `textField`) instead APPENDED a second `height="12"` attribute next to
the original `height="8"`, leaving the element with two `height` attributes. `mvn exec:java`
compiled and filled without any warning or exception, but that entire footer text never rendered
on either page (confirmed only via whole-page `get_text('text')` showing the expected footer
string completely absent). **When changing an attribute's VALUE via `sed`, always grep the
result afterward to confirm no attribute name appears twice on the same element** — this class of
bug produces no error at any pipeline stage, only a silently missing element, same as the F1
height-too-small bug but with a different root cause.

**G5. "Layout only, values are placeholders" still requires each placeholder value to be
individually checked against the reference, not just structurally self-consistent** — on
R10.006, two rows ("Total IFO Cost", "Total MGO Cost") had been given a copy-pasted value
identical to a THIRD row ("Total Bunker Cost") instead of their own real component values. This
wasn't caught by whole-page text diff alone (both wrong values were plausible-looking numbers,
not empty/missing) — it required cross-referencing the reference PDF's own text at each row's
specific y-position to catch. A row that sums correctly (IFO + MGO = Bunker) can still have its
own two addends wrong in a way that isn't visible without checking each one.

## Part H — integer-only coordinates, and re-verifying section-header conventions per report (from R10.008)

**H1. `x`, `y`, `width`, `height` on every element MUST be plain integers in this engine's
compact-format loader — decimals are rejected with a compile error, not silently truncated.** A
code-generation script that computed 31 calendar-table row positions using a 12.5pt row height
(`y="222.0"`, `y="234.5"`, ...) failed compilation entirely with `com.fasterxml.jackson.databind
.exc.InvalidFormatException: Cannot deserialize value of type 'int' from String "222.0"`. This is
DIFFERENT from `fontSize`/`lineWidth`/`pen` widths, which DO accept decimals (`fontSize="7.5"`
compiles fine). **When generating element positions programmatically (via a Python loop, not
hand-typed), always round `x`/`y`/`width`/`height` to the nearest integer before writing the XML
— non-integer row-height arithmetic is a common source of this, since dividing an available
span evenly across N rows rarely produces whole numbers.**

**H2. A section-header's visual convention (plain text vs. full-width colored bar, as first seen
in R10.006's Part G) must be re-verified per report even within the same reporting family — do
not assume a convention discovered on the immediately-preceding sibling carries forward.**
R10.008 shares R10.007's exact info-table/title skeleton, but its "MONTH AVERAGE OF INDEX
FACTORS" section header uses the OLDER plain-text `SectionLabelStyle` (R10.002/003/007's
convention), not R10.006's newer purple-bar `SectionBarStyle` — confirmed by direct recon
(absence of any `fill` drawing behind the header text at that y-position), not assumed either
way.

**H3. A single "9pt-too-high" offset across an entire multi-row table block is a strong signal
that the table's start position, not each row's individual height, is wrong** — on R10.008, a
coordinate spot-check showed the column-header row AND every subsequent data row landing ~9pt
higher than the reference, with the offset staying essentially constant (not accumulating) across
30+ rows. This pointed to a single miscalculated starting y (the grid was placed right after the
caption text without accounting for the caption's own full height) rather than a per-row spacing
error — fixed with one uniform shift applied to the whole block, not a per-row adjustment.

## Part I — a clean text diff can hide a structural defect, and column widths must be re-measured per report even for a "familiar" table shape (from R10.009)

**I1. A whole-page text diff showing zero missing/extra lines does NOT prove the layout is
correct — it only proves every string is present SOMEWHERE on the page.** On R10.009, a table
header was built with BOTH of its two caption lines duplicated into BOTH of its two value
sub-columns (each sub-column showed the period label AND "% of Worldscale", when only one
caption belongs in each). The whole-page text diff passed clean at this stage, because both
wrong copies of each string were still literally present as text on the page — the defect was
purely about WHICH cell each string sat in, something a text-presence diff cannot see. **A clean
text diff is a necessary but not sufficient verification step — always follow it with a
coordinate/structure check, especially for any table with repeated or near-duplicate captions
across columns**, where a copy-paste defect can hide in plain sight.

**I2. Reusing a sibling report's PROVEN table STRUCTURE (row layout, style names, box
convention) is safe and encouraged, but its exact COLUMN WIDTHS must still be re-measured per
report — even when the table looks like "the same kind of table" as an already-built sibling.**
R10.009's "Freight Rate Calculation" table looks identical in shape to R10.007's
"Price Formula Components" table (label column + two half-period value columns, same style
names), so its column widths were copied wholesale (label 269pt + two 135pt value columns,
spanning the full 539pt page width). Direct recon showed R10.009's actual table is much
narrower — label ~140pt, each value column ~110-120pt, total ~380pt — confirmed by the real
reference value positions being nowhere near where the copied-width layout would place them.
Structure and styling transfer across a family; specific pixel widths do not, and must be
measured fresh every time, matching the standing rule already established for spacing offsets
in Part F/G.

## Part J — text-only recon can miss a bordered-cell style, and one bad coordinate conversion cascades into a growing page-wide offset (from R10.010)

**J1. `get_text('text')` alone is not sufficient to judge whether a report uses bordered/filled
table cells — always cross-check `page.get_drawings()` fill colors before concluding a report's
box style.** R10.010's plain-text recon showed no visible box characters, suggesting a
borderless plain-label layout unlike the rest of the R10 family's bordered purple-header/white-
value convention. `get_drawings()` fill-color recon proved this wrong: the report uses the exact
same `#444080` purple header-cell / white value-cell bordered convention as every prior R10
report — the "plain-text" impression was purely an artifact of not checking vector drawings
before judging visual style. Treat text-only recon as informative for CONTENT, never as proof of
absence of borders/fills — a dedicated `get_drawings()` pass is required before concluding a
report has (or lacks) a bordered-cell convention.

**J2. `evaluationTime="Auto"` on a page-number `textField` can show the WRONG page's counter on
a `<title>`+`<summary>` 2-static-page report — plain (default/"Now") evaluation is what's
needed for a simple `pageFooter`.** R10.010's page 1 footer showed "Page 2 of 2" instead of
"Page 1 of 2" with `evaluationTime="Auto"` set on the `$V{PAGE_NUMBER}` field; removing
`evaluationTime="Auto"` (falling back to default evaluation) fixed it immediately. `Auto`
evaluation is for fields that must resolve at a delayed point (e.g. a group footer whose value
depends on content evaluated after the band itself renders) — a plain page-number field in a
page footer doesn't need it and can get the wrong page's value if it's applied anyway.

**J3. A single arithmetic slip converting one reference coordinate from absolute-PDF-space to
JRXML-local-space (typically forgetting to subtract `topMargin`) can silently cascade into a
report-wide, GROWING vertical offset that isn't obvious until many rows later.** On R10.010, the
divider line was placed at local y=70 instead of the correct local y=98 (a flat 28pt
abs-to-local conversion error), and this single early mistake propagated through the entire rest
of the page — a coordinate spot-check near the top of the page showed only a ~28-32pt gap, but
the same check near the bottom of an 11-row table showed the gap had grown to over 40pt (row
heights were also slightly too small, compounding the original offset). **Before building a long
multi-section report, sanity-check the abs-to-local conversion at 2-3 points spread across the
page (not just the first element) — a single early anchor check can look fine while still
hiding a mistake that only becomes obvious much further down.** The eventual fix required a
scripted progressive shift (a flat base correction plus a small proportional stretch) rather than
a single uniform shift, since the error compounded rather than staying constant.

**J4. THE FIX for J3's growing-offset class of defect: use each row's own exact recon-measured
`abs_y - topMargin` value directly as the JRXML `y`, never a computed uniform-row-height
formula.** Applied on R10.011 (a report with an even longer, denser page-1 content chain than
R10.010): every element's y was taken straight from the reference PDF's own measured position
during recon, rather than derived from "row N × row-height + section-start". Result: a
coordinate spot-check on 4 widely-separated labels landed within ~1-2pt on the FIRST build
attempt, with zero growing drift — a marked improvement over every prior multi-row R10 report's
iterative offset-chasing. **This exact-position approach should be the DEFAULT method for any
table/section with more than a handful of rows going forward, not a fallback used only after a
formula-based build turns out wrong** — it costs slightly more recon effort per row upfront but
eliminates an entire class of rework.

**J5. A lesson fixed in one band of a report does not automatically apply to a different band
of the SAME report — each band needs the lesson re-applied explicitly.** On R10.011, the title
band (page 1) was built using J4's exact-position method and came out nearly perfect, but the
summary band (page 2) was built the OLD way (proportional/estimated spacing relative to section
headers) and reproduced the same growing-offset defect J3/J4 had just fixed on page 1 — one
label landed ~43pt off. Fixed by re-applying J4's exact-recon-position method to the summary
band specifically. **When a report has multiple bands (title + summary, or multiple pages),
treat each band as needing its own explicit application of any positioning lesson — "I already
fixed this class of bug earlier in the same file" is not evidence it's fixed everywhere in the
file.**

## Part K — the R07 family: programmatic row-generation, CDATA-escaping, row-pairing
variability, and a "classification table" drifting out of sync with its own "placement
table" (from R07.006, R07.002, R07.004, R07.005)

**K1. For any table with more than a handful of rows, generate the JRXML rows
programmatically from the reference PDF's own extracted words (via PyMuPDF `fitz`),
classifying each word into a row (by rounded y) and a column (by x-range), rather than
transcribing values by hand.** Introduced on R07.006 (a 25-row x 7-column table) and reused
on R07.002 (two different tables), R07.004, and R07.005 (a 29-row x 15-column well-grid plus
a separate 17-row main table). This eliminates the manual-transcription mis-mapping risk that
caused R10.029's 3-value-transposition bug on a much smaller table. The general pattern:
```python
rows = defaultdict(list)
for w in words:
    if Y_MIN < w[1] < Y_MAX:
        rows[round(w[1], 0)].append(w)
# then classify each row's words into named columns by x-range, and emit
# <element> strings directly to a fragment file for later splicing into the JRXML.
```

**K2. Row-pairing conventions (label vs. value on the same line, or on separate adjacent
lines) differ per report and must be detected from that report's own recon, never assumed
from a structurally-similar sibling.** Some tables have label+value on the SAME line
(R07.002's main table, R07.004's main table, R07.005's main table); others have a
label-only row immediately followed by a SEPARATE value-only row ~1pt below (R07.002's and
R07.005's well-grids). A generator script written for one convention will silently produce
wrong or empty rows if pointed at a table using the other convention without adapting the
pairing logic first.

**K3. CDATA content must NOT be XML-entity-escaped.** A generator's `esc()` helper that
escapes `&` to `&amp;` before writing into a `<![CDATA[...]]>` block causes the literal string
"&amp;" to render in the PDF instead of "&" — CDATA sections are already literal text and
don't need (or want) standard XML entity escaping. Discovered on R07.004 ("Cold flare & Warm
flare"); every prior report's generator happened not to hit any `&`/`<`/`>` in its label set,
so the bug was latent until this one label triggered it. If a generator must guard against
anything inside CDATA, it should only ever guard against the literal sequence `]]>` (which
would prematurely terminate the CDATA block), never the standard entity set.

**K4. `<detail>`+datasource repeating grids are for genuinely repeating per-instance data; a
report family sharing a "column shape" doesn't always share a REASON for that shape — verify
which axis (onshore/offshore vs. daily/monthly) actually drives a table's column count before
assuming a sibling's shape transfers.** Confirmed twice, in both directions: R07.004 (daily
onshore) and R07.006 (monthly onshore) share the same 7-column dual-unit (Volume+Mass) main
table shape despite different cadences — the shape tracks onshore vs. offshore, not
daily vs. monthly. Symmetrically, R07.002 (daily offshore) and R07.005 (monthly offshore)
share the same 5-column single-unit (Volume only) shape despite different cadences — same
conclusion from the opposite pair. Never assume a "same cadence" sibling's column shape
applies without checking which axis is actually load-bearing.

**K5. A "classification table" (used to bucket extracted words into named columns) and a
"placement table" (used to decide where to RENDER those same named columns) are two
independent pieces of data — if the placement table isn't literally DERIVED from the
classification table's own measured ranges, it can drift out of sync with zero visible
symptom until a coordinate check catches it.** On R07.005's well-grid generator, `COLS` (the
classification ranges, correctly measured from real recon: e.g. `MP_GAS: (268, 315)`) and
`COL_WIDTHS` (the placement x/width pairs used when emitting `<element>`s) were two
separately-authored dictionaries — `COL_WIDTHS` held independently-invented numbers (e.g.
`MP_GAS: (207, 44)`) that did not correspond to `COLS`' own range for the same column. Values
were still correctly CLASSIFIED into the right named column (so the printed diagnostic dump
looked completely correct), but then RENDERED up to 25pt away from their true position — a
defect invisible to both a code read and a whole-page text diff (every value was still present,
just glued to the wrong x). Only caught by a `search_for()` coordinate spot-check comparing
generated vs. reference PDF. **Fix and going-forward rule: never maintain two separate tables
for the same set of named columns — derive the placement table directly from the
classification table** (`COL_WIDTHS = {name: (L(x0), x1 - x0) for name, x0, x1 in COLS}`),
so there is only one measured source of truth per column.

**K6. A positioning lesson fixed in an earlier report does NOT automatically protect a NEW
generator script written for a later report — the same class of bug can be silently
reintroduced and must be re-checked per script, not assumed fixed project-wide.** R07.005's
first-pass well-grid generator computed each row's y from `start_ly + i * 13` (a fixed
row-height formula) instead of using each row's own measured position — the exact bug class
that R10.010/R10.011 (Part J3/J4) established the "exact-position method" specifically to
eliminate. It was caught before compiling by checking that the real recon's row-to-row y
deltas were uniform (208, 222, 236, ... — a consistent 14pt, not the script's assumed 13pt),
which would have produced a 29pt cumulative drift by the last of 29 rows if left unfixed.
**When writing ANY new generator script, explicitly verify it uses each row's own measured y
(not a formula), even though this exact lesson has already been "learned" and applied in
prior reports in the same project — the lesson lives in the discipline of checking, not in
having once fixed a specific file.**

## Part L — forced-page-break `<detail>` bands for content spanning MORE than
one extra page (from R07.003, a 5-page report)

**L1. The established "oversized `<summary>` relying on natural band-overflow"
trick (Part G, used by every 2-page R07/R10 report) does NOT generalize to
content spanning more than one extra physical page — JasperReports validates
`<title>`/`<summary>` band height against a SINGLE page's usable space and
REJECTS anything declared far beyond it.** A first attempt at a 5-page report
(page1 title + pages 2-5 all inside one `<summary height="3660">`) failed to
compile: `"The summary section and the margins do not fit the page height."`
The small ~13pt overflow every 2-page report relies on (declared height just
over the ~1117pt-per-page budget, forcing exactly one extra page) is tolerated;
declaring a band several times taller than one page is not — this is a hard
validation limit, not a soft pagination quirk.

**L2. THE FIX: use a repeating `<detail>` band with `splitType="Prevent"` and a
declared height close to one full page, filled via `JREmptyDataSource(N)` (N =
however many extra pages are needed), with each record's content gated by
`printWhenExpression` on the built-in `$V{REPORT_COUNT}` variable.** A `<detail>`
band has no single-page height ceiling (unlike `<title>`/`<summary>`) because it
is designed to repeat. Giving it height≈1100 (vs ~1117 usable) means a record
is placed atomically and the next record never has room left on the same page,
so it naturally rolls onto a fresh page — confirmed via an isolated minimal
repro (4 unconditional records → clean N-page result) before touching the real
production JRXML.

**L3. A `<detail>` record whose EVERY element is hidden by `printWhenExpression`
collapses to effectively ZERO height, silently losing the forced page break -
the band's declared height is not a hard per-record reservation once nothing
in it is actually visible.** Confirmed via an isolated repro: 4 conditional-only
elements (one printing per `$V{REPORT_COUNT}` value) produced only 2 pages
total instead of 4, because records 2-4's entirely-hidden content collapsed
away instead of still reserving their declared band height. **Fix: add one
UNCONDITIONAL (never printWhenExpression-gated) full-height spacer element
(e.g. a 1x1090 rectangle) to every record** - this guarantees the band always
reserves its declared space regardless of which OTHER content happens to be
visible that iteration.

**L4. A `printWhenExpression`-injection helper (or any programmatic XML
post-processing) MUST convert self-closing `<element .../>` tags to an
explicit open/close pair before inserting a child - inserting content directly
after a self-closing tag's `/>` leaves it as a DANGLING SIBLING of that
element, not a child, and the compact-format loader may silently accept the
malformed placement rather than rejecting it.** On R07.003, a regex that
correctly matched `<element kind="staticText" ...>...</element>` (inserting
`printWhenExpression` as the first child) also matched self-closing
`<element kind="rectangle" .../>` tags (the plain section-header divider bars)
and inserted `printWhenExpression` immediately AFTER the `/>` — landing it as a
direct child of `<band>` instead of the rectangle. The compact-format loader
did not raise any error; empirically it treated a `printWhenExpression` found
directly inside `<band>` as the BAND's OWN printWhenExpression, with the LAST
one encountered silently overwriting all previous ones. Since this report had
5 such stray rectangles, all still evaluating `$V{REPORT_COUNT} == 1`, the
entire detail band ended up gated on that single condition — every record
after the first silently vanished, with NO compile error and NO warning to
signal the mistake. **Fix: always convert `<element attrs/>` to
`<element attrs><child/></element>` explicitly before inserting anything, never
assume a plain string-append after a matched tag lands as a child.** This was
only found by testing the injection helper's regex against an isolated minimal
JRXML small enough to inspect the exact resulting element/band nesting by eye,
not by staring at the ~400-element production file.

**L5. When debugging a novel report-structure MECHANISM (not just a value or
position), build and test an ISOLATED minimal repro file FIRST, before
suspecting the full production JRXML.** Every one of L1-L4's root causes was
found in minutes once isolated in a ~10-element `mini.jrxml`/`mini2.jrxml`/
`mini3.jrxml` test file; the same bugs would have taken far longer to spot
buried inside ~400 real elements with real business content, where a
mis-rendered page is hard to distinguish from "just another data-position
mistake" without first ruling out the underlying page-break mechanism itself.

**L6. A sibling report's title/header text is a VALUE like any other measured
fact — copying its exact wording (not just its layout pattern) without
checking THIS report's own reference is the same "no-hardcode-copy-adapt-
verify" mistake this project already bans for positions and column shapes,
just applied to text content instead.** Every other R07 report's title starts
with "Ichthys: " - R07.003's own reference PDF has no such prefix anywhere on
any of its 5 pages (confirmed via direct recon of its own title line). The
"Ichthys: " prefix was carried over by habit from the sibling reports' pattern
rather than re-verified against this specific report's own text, and only
caught by the whole-page text diff showing "Onshore Daily Operations Report"
(ref, no prefix) as missing and "Ichthys: Onshore Daily Operations Report"
(gen, with prefix) as extra on every single page.

## Part M — border/alignment review checklist for a recap/summary block, and the
meta-lesson on reactive vs. comprehensive verification (from R07.011's Participant
recap block, a multi-round owner-guided review pass)

This part is written as a CHECKLIST to run on any future report's grid/recap block
BEFORE reporting it "matches the reference", because every item below was found only
after the owner pointed at a screenshot, one round at a time — each one was a real,
confirmable defect, and each one should have been caught by a single up-front pass
rather than discovered piecemeal.

**M1. When comparing a generated PDF's drawn coordinates against a reference PDF via
`get_drawings()`/`search_for()`, check BOTH PDFs' `page.rotation` first.** JasperReports
can export an `orientation="Landscape"` report as a PORTRAIT mediabox with a `/Rotate 90`
entry (visually identical when rendered, e.g. via `get_pixmap()`, which applies rotation
automatically) — while a hand-exported Crystal Reports reference PDF may use a genuinely
landscape mediabox with `rotation=0`. Raw coordinates from `get_drawings()`/`search_for()`
do NOT account for `/Rotate` — comparing them directly across two PDFs with different
rotation gives nonsense (e.g. a label appearing to be at x=328,y=1074 when it's actually
"at" a completely different visual position). **Always apply `page.rotation_matrix` to
one side's rects before comparing** (`rect * page.rotation_matrix`), or you will
mis-diagnose real defects as measurement noise, or vice versa.

**M2. A missing `leftPen` (or any one side) in a shared cell style is often invisible
in mid-grid columns and only shows up at cells with an actual GAP to their left, or as
column extremes.** Adjacent same-style cells hide the omission because the neighbor's
`rightPen` covers the same visual boundary. Check this by looking for the FIRST column
after ANY structural gap (a merged header spanning multiple sub-columns, a column-group
boundary), not just "does the leftmost column of the whole table look right."

**M3. A bare `<pen lineWidth="1.0"/>` (no `lineColor`) silently defaults to BLACK,
while every other border in the same block may use a lighter shared color (`#D6D6D6`
in this project's convention).** This reads as "inconsistently bold" or "looks bolder
than everything else" rather than "wrong color" at a glance — always grep for bare
`<pen .../>` (no `lineColor=`) when a border looks visually heavier than its neighbors,
and compare it against the reference's OWN measured border color (from `get_drawings()`
color, not by eye).

**M4. Column boundaries between adjacent zones must be EXACTLY flush — both a GAP and
an OVERLAP of even 1-2pt produce a visible artifact, and "close" is not sufficient.**
Closing a gap by widening one side without checking the exact target figure can
overshoot into an overlap (this happened twice in the same session — first a gap, then
the "fix" for it produced a 2pt overlap). The right procedure: compute the exact meeting
x from BOTH neighbors' true boundaries (e.g. `suffix_start = prefix_start + prefix_width`
must exactly equal the value used as `suffix_x`), not iteratively nudge widths until it
"looks right" on the next screenshot.

**M5. A true multi-row MERGED cell needs one single element spanning the FULL merged
height, positioned at the FIRST sub-row's y — not a single-row-height label element
sitting only in the LAST sub-row with nothing in the sub-row(s) above it.** The
"row above has nothing" gap is invisible in a rendered screenshot at normal zoom (looks
like the label is merely off-center) but is a real missing-border defect, confirmed by
comparing each cell's rectangle height directly against the reference (2x normal row
height = a true merge; two separate normal-height boxes = not a merge).

**M6. `hTextAlign` for label cells must be verified against the reference's actual
rendered look, not assumed from a plausible-looking default.** This project's
recap-style label cells (row/column captions in a summary block) are CENTER-aligned in
the reference, not LEFT — an assumption carried over from how ordinary body-text labels
are aligned elsewhere in the same report. Different cell ROLES (data-table body text vs.
summary-block captions) can use different alignment conventions within the SAME report;
don't extrapolate one convention onto a visually-different block without checking.

**M7. A header/mini-header box's x-position must be checked against the SAME reference
point as the rows below it, not set independently during an earlier, separate edit.**
A header box set to x=62 and its data rows set to x=64 (a flat, constant 2pt offset) each
look internally consistent in isolation, but the WHOLE column reads as "can't align" when
viewed as one continuous edge from header through all data rows. When editing a header
box and its data rows in separate passes, always diff their x-values against each other
before considering either "done".

**M8. THE MOST IMPORTANT FINDING — a shared cell style that defines BOTH `topPen` AND
`bottomPen` causes every INTERIOR row boundary to be drawn TWICE (once by the row
above's bottomPen, once by the row below's topPen), while boundaries adjacent to a
DIFFERENTLY-styled element (e.g. a header band using its own separate pen mechanism)
get drawn ONCE.** Two near-identical thin lines 0.5-1pt apart can render visually
thicker/darker than a single line at the same width — producing an inconsistent-looking
grid where some horizontal boundaries look bolder than others, with NO actual difference
in `lineWidth` anywhere in the XML. This was confirmed by directly measuring the PDF's
own drawing operations (found two separate 1.0-width lines 1pt apart at a double-drawn
boundary, vs. exactly one line at a boundary adjacent to the header). **Fix: remove ONE
side's pen (e.g. `topPen`) from the shared style** so each interior boundary is drawn
by exactly one neighbor; the outermost edge (first row's top) is still covered by the
preceding header/band's own border, since that header sits at the same y. This is a
STYLE-LEVEL fix (touches every element using that style, e.g. ~97 elements in R07.011,
likely the same shared style used by the main detail grid too) — check for regressions
on BOTH the block you were reviewing AND any other section using the same style before
calling it done.

**M9. THE META-LESSON — fix reactively one flagged item at a time, and you will
re-introduce or leave adjacent defects that only surface in the NEXT screenshot round.**
Across this single recap block, the same class of mistake repeated: closing a gap
between two columns without re-verifying the OTHER boundary of the same column; adding
a `leftPen` to fix a border without checking whether the header row's rectangles used
the same convention; center-vs-left alignment discovered only because it was pointed
out, not because it was checked against the reference up front. **Before reporting any
grid/table region "matches the reference", run a SINGLE comprehensive pass measuring
EVERY cell boundary (x, y, width, height, pen color, pen sides) against the reference's
own `get_drawings()` output — do not rely on a full-page screenshot glance, and do not
consider a fix complete until its own edit's side-effects on NEIGHBORING elements have
also been re-verified in the same pass.** This checklist (M1-M8) is exactly the set of
things that comprehensive pass should cover for any future report's grid/recap block.

## Part N — style-level fixes leak sideways, JasperReports silently drops text that
doesn't fit its box, and "variable content" needs real measurement across ALL known
instances, not one sample (from the R07.016/017/018 owner-review passes, 2026-08-30)

**N1. A style-level fix (e.g. adding `leftPen` to a shared style) must be re-checked
against EVERY element that reuses that style with its own per-element `<box>`
override — not just the elements the fix was originally aimed at.** On R07.018, adding
`leftPen` to `DetailTextStyle` (to fix a real border gap elsewhere) caused the "Remarks:"
label — which reuses `DetailTextStyle` but only explicitly zeroed `topPen`/`bottomPen`/
`rightPen` in its own override — to pick up an unwanted left border it never had before.
**Rule: after any shared-style edit, grep for every element using that style with a box
override, and check whether the new pen side needs to be explicitly zeroed there too.**

**N2. JasperReports silently drops text entirely (renders nothing, no error, no
warning) if the element's box is too short for the font size — it does not throw, warn,
or auto-shrink the font.** On R07.018, changing "Field Condensate" to bold 18pt (to
match the title) inside its original `height="16"` box made the text disappear
completely from the rendered PDF; `search_for()` and even raw `get_text()` found zero
occurrences of the string. **Rule: whenever a font size or weight is increased on an
existing element, verify the box height still comfortably exceeds the new font's line
height (roughly `fontSize * 1.2` minimum), and always re-verify the text is actually
present in the rendered output (not just that compile succeeded) — a clean compile does
NOT mean the text will render.**

**N3. When a report's own design comment says content is "variable per month/report"
(e.g. a free-text Remarks section), don't guess a fixed box height — measure the REAL
length across every available instance first.** The single reference PDF for R07.018
had 4 pages (one per month); measuring the actual Remarks paragraph height on all 4
(41.1pt / 41.1pt / 51.5pt / 30.8pt) revealed real, substantial variation and gave a
concrete worst-case (51.5pt) to size against — sizing the box to fit the worst OBSERVED
case, not an arbitrary round number, avoided both clipping the longest month and wildly
over-sizing for the shortest. **When multiple real instances exist in one file (or across
sibling reports), measure all of them before picking a fixed dimension.**

**N4. A row/column's rendered height can be internally "N lines tall" even without an
explicit multi-row merge — compare the ELEMENT height against the reference's own
measured row height and the font's line-height capacity, not just "does it look okay."**
R07.018's Date-row header used `height="28"` at `fontSize="7.0"` (line-height ~8.4pt),
giving ~3.3 lines of vertical room, while the reference's actual Date-row height measured
~20.4pt (~2.4 lines) via `get_drawings()`. The owner's framing — "check if it's a 2-row
or 3-row merge" — maps directly onto this: **compute `height / (fontSize * ~1.2)` and
compare that line-count against the reference's own measured height / line-height ratio,
not against a guessed "looks about the same" impression.**

**N5. Owner-approved workflow that worked cleanly this round: recon → present findings
as findings (not verdicts) → wait for explicit per-item go-ahead → fix → re-verify by
measurement → finalize.** When an early attempt applied multiple fixes without asking
first (R07.016), the owner had it fully reverted, then had each fix re-applied ONE AT A
TIME only after asking specifically for it. This is slower per-item but was accepted
cleanly with zero further pushback — treat "recon first, list what's confirmed vs.
still-to-check, ask before touching the file" as the default opening move on any
already-"done" report, not an optional courtesy.

## Part O — a "matches the reference's raw color" build can still be visually wrong, band-height overshoot creates a silent extra gap, and shared-attribute shifts need a scope-check every time (from the R07.023 CDP owner-review pass, 2026-08-31)

**O1. Matching a reference's raw measured color value is not the same as matching its
visual result — always sanity-check contrast, not just the hex code.** On R07.023's Total
row, `get_drawings()` on the reference genuinely showed the top border above the teal
Month/Total cell as gray `#D6D6D6` (confirmed via two independent measurements: a broad
column scan and a precise Dec/Total word-position bracket) — technically correct to
reproduce. But gray-on-`#0091B5`-teal is essentially invisible, so the built report showed
no visible Dec/Total separation on that column while the adjacent numeric cells (which get
a real purple `#454087` top border) clearly did. The owner asked for a deliberate deviation
(purple on the teal cell too) once shown the side-by-side screenshot proof. **Rule: after
measuring a real color, also render it and look at actual contrast against its own
background fill — a "correct" hex value against a similarly-toned fill is a visual no-op,
and is worth flagging to the owner as a possible deliberate-deviation candidate rather than
silently shipping the "technically accurate" version.**

**O2. When a `<title>` (or other fixed-height) band's declared height exceeds its actual
content's lowest element by more than a few points, the excess renders as a real, visible
blank gap before the next band starts — JasperReports does not auto-trim it.** Growing
R07.023's title band 300→330 to fix an overlap (Standard Cargo Size box was overlapping the
main table header by ~6pt) overshot the real requirement (313, i.e. the lowest element's own
bottom edge) by 17pt, which then showed up as a visible blank strip between the table header
and the first detail row (`Jan`) — a second owner-screenshot catch. **Rule: when resizing a
band to fix a collision, set the height to EXACTLY the tallest/lowest element's edge (measure
it, don't round up "for safety") — a band that's too short breaks compilation immediately
(loud, easy to catch) but one that's too tall creates a silent visual gap (quiet, easy to
miss) that only shows up on the rendered PDF, not the compile step.**

**O3. Before batch-shifting every element that shares an x/y coordinate value (e.g. "all
`y="252"` elements move to `y="272"`"), `grep -c` (or list) that exact attribute value across
the WHOLE file first, not just the section you intend to edit.** Used successfully multiple
times this pass (shifting the main table's header rows, closing the Dec/Total gap, moving
footer text below its new divider line) — each time, confirming the count/location of a
shared literal value before a blind find-and-replace prevented an unrelated element
elsewhere in the file from being silently caught by the same edit.

**O4. A "missing element" defect (e.g. a divider line the current build never had) needs
its OWN position verified against the reference — don't just insert it above/below an
existing element and assume the ordering is right.** Adding R07.023's missing footer divider
line got the line's own position right on the first try (measured directly: `y=790`,
`#454087`, width 1.5) but left the existing footer text at its old `y="0"`, which put the
text ABOVE the newly-added line instead of below it — inverting the reference's real order
(reference: line at `y=790`, text starting at `y=792`). Caught only by re-measuring the
REGENERATED pdf's own word positions after the first render, not by assuming the fix was
complete because the line itself matched. **Rule: adding a new element near existing ones
means re-verifying the existing elements' relative position too, not just the new element in
isolation.**

**O5. Journal discipline (owner-repeated instruction, 2026-08-31): after any real
review/fix cycle — not just at "session end" — append the genuinely new, reusable lessons
here (this file), not only into the per-report `COMPLETION-NOTES.md` or the project-level
memory summary.** Those two are report-specific and session-summary-specific respectively;
this file is the one place future sessions actually consult before touching ANY report's
layout (see [[reference_jasperreport_lessons_file]]). A lesson that only lives in one
report's own completion notes will not be found again when the same failure mode shows up
on a different report.

## Part P — a `rectangle` element's border comes from its OWN `pen`, not the style's `<box>`, and a text-extraction/coordinate check alone can miss a totally wrong color scheme (from R07.002's owner-directed full rebuild, 2026-08-31)

**P1. A `<style>`'s `<box>` only controls TEXT elements' borders — a `rectangle` element's own
border comes from its `pen` property, which the style does NOT supply automatically.** On
R07.002, 14 full-width purple section-title `rectangle` elements referenced a style
(`PurpleSectionStyle`) that HAD a `<box><pen .../></box>` definition — but since a bare
`<element kind="rectangle" .../>` with no own `<pen>` tag doesn't inherit the style's box for
its OWN border, all 14 rendered with an undefined/white border instead of the intended gray.
**Rule: every `rectangle` element needs its own explicit `<pen>` tag (even when referencing a
style that already defines colors) — a style's `<box>` never substitutes for it.**

**P2. A whole-page text-extraction match (or even a 10-label coordinate spot-check) proves
almost NOTHING about whether the visual structure/color scheme matches the reference — it
only proves the WORDS are present in roughly the right place.** R07.002 passed a "150/150
lines perfect match" text check yet had an ENTIRELY invented color palette (a light-blue
`#F8FBFC` cell fill instead of white, black/uncolored borders instead of the reference's real
gray `#D6D6D6` grid, and roughly a third of its purple section headers missing their fill
treatment entirely) that was never checked. **The real check is a `get_drawings()` color-
palette histogram comparison** — group every drawing by `(color, fill, width)` and compare
counts between reference and generated PDF; a report that's structurally wrong will show up
immediately as missing/extra color categories, even when the text content is perfect.

**P3. Every section's own title in a Crystal-derived report tends to have ONE consistent
"anatomy": [purple-filled title bar] → [dark-gray `#636363` divider line, width 1.5] →
[purple-filled column/group header row(s), gray `#D6D6D6` bordered] → [gray-bordered data
rows].** Confirmed across ALL 11 sections in R07.002 (7 on page 1, 4 on page 2) — the same
divider-line color/width/position-relative-to-title pattern repeated with zero exceptions,
meaning once one section's anatomy is confirmed via `get_drawings()`, the REMAINING sections
can be checked quickly (just verify the same 4-layer pattern applies) rather than needing
fully independent re-discovery each time — but still verify each one's specific column
boundaries/row heights, since column COUNT and WIDTH varies per section (2 columns for HSE's
label/#/comments vs 6 for Gas Export Pipeline vs 5 for the Production table).

**P4. A word-frequency diff (Counter subtraction, not sequence diff) is the right tool to
separate "genuinely missing content" from "PDF text-extraction reordering noise."** A raw
`difflib` sequence diff between reference and generated `get_text('text')` output produced
dozens of false "differences" that were purely reordering artifacts (PDF text extraction
follows drawing/z-order, not visual reading order) — switching to `collections.Counter(words)
- Counter(other_words)` isolated the handful of GENUINELY missing/extra words (e.g. a
completely absent 3rd header line "Volume" on one column) from the noise in one step.

## Part Q — a color-palette histogram is necessary but NOT sufficient; render to PNG and actually look (from R07.002's second owner pushback round, 2026-08-31)

**Q1. Coordinate/color-count checks can pass while the report still looks visibly wrong to a
human — some defect classes only show up in an actual rendered image.** After a full
`get_drawings()` color-histogram fix pass on R07.002 (Part P), the owner still rejected it as
"far from acceptable" and was right to: rendering both PDFs to PNG (`page.get_pixmap(dpi=100
or so).save(...)`) and reading them side by side immediately surfaced THREE defect classes
the histogram never could: (a) a completely missing logo image (zero `<element kind="image">`
in the whole file — a histogram only tracks vector `get_drawings()`, not raster images, so
this was invisible to that method entirely); (b) roughly half the section titles were
WRONGLY purple-filled bars when the reference shows them as plain text — the histogram
correctly counted "N purple fills" as present, but couldn't tell WHICH specific titles should
or shouldn't have them, since a wrong distribution can still sum to a similar total; (c) a
stray visually-blank bordered cell from an unfilled coordinate gap between two adjacent
elements — invisible to both a word-count diff (no missing text) and a color histogram (the
gray border color was correct, just in the wrong place). **Rule: after any histogram-level
color/border fix, ALSO render to an image and visually compare against the reference before
calling it done — the two methods catch genuinely different defect classes, neither
subsumes the other.**

**Q2. When visually comparing rendered pages, verify each suspected "looks different" spot
against `get_drawings()`/`get_text('words')` at ITS SPECIFIC location before changing
anything — a screenshot's compressed visual impression can still be wrong.** Initially
misread a JPEG-compressed reference screenshot as showing "Production"/"Internal
Consumption"/"Losses" sub-headers with a purple tint (they don't — confirmed via
`get_drawings()` at their exact y-position: zero fill). The habit of re-verifying against the
raw vector data before editing (rather than trusting the visual impression alone) caught this
before an incorrect "fix" was applied — the two are complementary: visual comparison finds
CANDIDATE defects, `get_drawings()`/`get_text()` at that specific location CONFIRMS them.

**Q3. Adding a border to a shared style (e.g. giving `PlainValueStyle` a `<box>` pen) can
create a NEW visible defect anywhere two adjacent elements using that style don't tile
edge-to-edge — a coordinate gap that was invisible when borderless becomes a visible blank
bordered box once bordered.** This is a variant of Part N1's "style-level fix leaks
sideways" lesson, but the NEW failure mode here is spatial rather than stylistic: the gap
itself was pre-existing (unnoticed because there was no border to reveal it), and only became
a defect as a SIDE EFFECT of an otherwise-correct border fix. **Rule: after adding a border to
a shared style, check for coordinate gaps between elements that use it, not just the pen
color/width itself.**

**Q4. When shifting a group of elements to a new y-position, check ALL neighboring elements'
positions too, not just whether the shifted group itself is now internally consistent.**
Rebuilding the well-grid's header with a real fill introduced a self-caused overlap with the
"Subsea Production" title and its own divider line — the header rectangle's initial `y`
value was chosen to match a REMEMBERED value from before the divider was added, not
re-checked against the divider's actual position. Caught via the SAME render-and-look method
from Q1, not assumed correct after one clean compile.

## Part R — fixing a table's HEADER is not the same as fixing the TABLE; every downstream row/cell referencing the old column geometry must be independently re-checked (from R07.002's owner pushback round 4, 2026-08-31)

**R1. When a table's column x/width boundaries are corrected, EVERY element that
positionally depends on those boundaries must be re-checked — not just the header row that
prompted the fix.** This happened TWICE in the same session on R07.002: (a) the Production
table's header was rebuilt with the correct 2-tier group/leaf structure, but the 14 data rows
underneath still referenced the OLD, unrelated column x-positions from before the fix,
producing visible gaps between cells ("bolderlines... STUCK"); (b) the well-grid's ROW2 leaf
columns and 30 data rows were bulk-corrected to their real measured widths, but ROW1's group
cells ("Flow Rate"/"MEG Injection") were left referencing the OLD boundaries, so the group
headers no longer aligned with the columns they were supposed to span. **Rule: after fixing
a column's x/width anywhere in a table (header OR data), grep for every OTHER row/band that
uses the SAME old x/width values and confirm each one either also needs the fix or is
genuinely unrelated — never assume a header fix "flows down" to the data rows automatically,
or that a data-row fix means the header is already consistent.**

**R2. A genuinely blank/empty data column (no value to show) still needs its own bordered
cell element — omitting the element entirely (rather than rendering it blank) causes the
column to visually disappear along with its border.** R07.002's Consumables CPF/FPSO tables
had "Filled/Bunkered Volume" and "Comments" columns with headers but ZERO data-row elements
for either column — not blank text, no element at all. This reads visually as "the column is
missing" (matching the owner's literal complaint "missing Comments columns section"), not as
"the column is empty." **Rule: every column that appears in a table's header needs a
corresponding (possibly empty-text) bordered element in every data row — never skip an
element just because it has no value to display.**

**R3. Free-text "paragraph" sections (multiple lines of prose under one label) may use a
SINGLE shared bordered box for all lines, not one border per line — check which pattern the
reference actually uses before assuming per-line borders are correct.** R07.002's
CPF/FPSO Comments blocks had each free-text line individually boxed (a "Production:" line,
then 3 separate "- ..." lines, each with its own 4-sided border) when the reference shows
ONE continuous bordered box containing all 4 lines together, sized to the real total content
height. The fix: draw one `mode="Transparent"` bordered `rectangle` sized to the full text
block's height, then place the individual text lines inside it with their OWN box pens
zeroed out (`<box><pen lineWidth="0.0"/></box>`) so they don't double-border.

**R4. A style-level border fix (e.g. adding a box to a shared label style) can wrongly box
an element that should have NO border at all** (a disclaimer, a free-standing caption) —
check every usage of that style for whether a border was ever intended, not just whether the
color/width is now technically correct. R07.002's Disclaimer text picked up an unwanted box
border purely from reusing `PlainLabelStyle` after that style gained a border in an earlier
fix pass — it needed the border explicitly zeroed back out for this one specific use.

## Part S — row HEIGHT vs row SPACING is a distinct defect class from column x/width, and it repeats across every table shape (from R07.002's owner pushback rounds 5-6, 2026-08-31)

**S1. A "STUCK"/gap border between rows is caused by row HEIGHT being shorter than the
Y-DELTA between consecutive rows — not by column width or border color.** This is a
completely separate defect class from Part R (which is about column x/width), and it hit
FOUR different tables in the same report before being generalized: the Production table (14
rows at `height=12` but spaced 14pt apart → 2pt gap), Gas Export Pipeline/Inventory
(header-to-data-row gap from the same height-vs-position mismatch), the well-grid's subtotal
rows (`height=13` spaced 16pt apart → 3pt gap), and the Consumables tables (row spacing
alternating 12/13 instead of a uniform value, creating inconsistent border thickness
row-to-row that reads as "the borderline size is not the same"). **Detection: measure the
reference's ACTUAL row height AND the Y-delta between consecutive rows via `get_drawings()`
— if height ≈ delta (gap near zero), rows tile edge-to-edge; if height noticeably < delta, the
reference itself will show a gap and so will a correct build. Never assume a round number
(12, 13) is "close enough" to the spacing — measure both independently and compare.**

**S2. A band's declared height fitting its own content is necessary but NOT sufficient —
the band also has to fit within `pageHeight − topMargin − bottomMargin` ALONGSIDE every
other same-page band (pageHeader/pageFooter).** Widening a band to create breathing room
between two rows (e.g. "Total" row → "Consumables for CPF" title) can silently push the
combined page budget over the limit even though the band's own content still fits inside its
own declared height — this produced a genuine, uncaught-until-recompile 3rd page (`summary`
1117→1130 pushed `summary+pageFooter` from 1147, an EXACT fit, to 1160, 13pt over). **Rule:
after ANY band-height change, recompile and check the reported page count before doing
anything else — it's a free, zero-effort correctness signal that catches this class of
mistake immediately, before it ever reaches a visual re-render.** If a band was already at a
deliberately tight fit (zero slack), absorb any new spacing need by trimming SOME OTHER
element's slack in the same band (e.g. an oversized static-text box with unused padding),
not by growing the band's declared height.

## Part T — a convention borrowed from a SIBLING table (row-rect width, a style's inherited fill/border) can be silently wrong for THIS table; always re-derive from the table's own real columns (from R07.002's owner pushback round 7, 2026-08-31)

**T1. A full-row background/border rectangle's width should be the SUM of that specific
table's own real column widths — never reused from a different table's row-width constant.**
R07.002's Production/Internal-Consumption/Losses section-label rows borrowed `width=789`
from the well-grid's row-background convention, but this table's own 6 columns only sum to
`width=784` — the 5pt overshoot created a small rectangular notch poking out past the last
column's real right edge, invisible unless the right edge is checked pixel-for-pixel against
the columns below it. **Rule: when adding a full-width row rect to a NEW table, compute its
width as the literal sum of that table's own column widths — do not copy a width value from
a sibling table just because both look like "the same convention."**

**T2. An `Opaque`-mode text element's own BACKGROUND FILL is a separate rendering hazard
from its BORDER pen — fixing one does not fix the other.** R07.002's "CPF"/"FPSO" purple bar
labels had TWO separate defects across two rounds, both caused by the same underlying x/width
offset (text at `x=4 width=789` vs the rect behind it at `x=0 width=789`): round 6 fixed the
visible double-BORDER line by zeroing the text's box pen; round 7 found the text's own opaque
FILL was still rendering as a second purple rectangle, 4pt narrower on the left but 4pt wider
on the right than the rect behind it, creating a visible "step" at the top-right corner where
the bar meets the box below. **Rule: any style-inherited element with `mode="Opaque"` that
sits exactly on top of (or flush beside) another filled/bordered rect needs BOTH its pen AND
its fill checked for x/width-offset overhang — checking only the border (because that's what
was visually obvious first) can leave the fill-based twin defect completely unnoticed until a
later, more careful pass.** The simplest fix when a rect already supplies the correct
background is to set the overlaid text to `mode="Transparent"` entirely — it never needed its
own fill.

**T3. Section-title-to-divider-line spacing should be consistent across every section title in
the same report — a leftover mismatched gap from an earlier build pass reads as a visible
inconsistency even with no other defect nearby.** R07.002's "Subsea Production" title had a
14pt gap to its own divider line, while every other section title ("Consumables for CPF/FPSO",
etc.) used a 6-7pt gap — nothing else was wrong with either element individually, but the
inconsistency stood out precisely because the pattern was already established elsewhere in
the same document. **Rule: when checking any section title's spacing, compare it against the
OTHER section titles' spacing in the same report, not just against the reference in
isolation — a self-consistency check catches this class of defect that a reference-only check
can miss if the reference itself doesn't have an exact structural analog for that section.**

## Post-mortem — checklist to re-run on R07.003 through R07.006 before considering them "done" (2026-08-31)

R07.002 went through 8 owner-pushback rounds before being accepted — the original build (like
R07.003-R07.006, built earlier in the same style) was verified with only a text-match +
10-label spot-check, which caught NONE of the following defect classes. Before trusting
R07.003-R07.006's existing "done" status, re-run this checklist against each:

1. **Color/fill scheme** — `get_drawings()` histogram: does every section title/header cell
   that should be plain text vs. purple-filled actually match the reference at that exact
   coordinate? (Part P/Q — a "matches on values" build can still have entirely wrong
   fill choices.)
2. **Logo, dividers, title/date positions** — is the page-header logo image present at all
   (not just referenced in a style), and do the divider lines/title/date sit at the reference's
   real measured y-positions, not just "look roughly right"? (Part Q.)
3. **Font extension jar wired into `pom.xml`** — does `bold`/`italic` actually render as
   `Arial-BoldMT`/`ArialItalic` (check via `get_text('dict')` span fonts), or does it silently
   fall back to plain Helvetica with zero compile error? (Part P.)
4. **Header structure fixed ⇒ data rows independently re-checked** — for every table whose
   header was ever corrected, re-verify the data rows below still reference the SAME corrected
   column x/width values, not leftover old ones. (Part R.)
5. **Row height vs. row spacing** — for every table, measure the reference's actual row
   height and the Y-delta between rows; do NOT assume a round number is "close enough" if the
   two differ — this produces "STUCK"/inconsistent border defects invisible until zoomed
   in. (Part S1.)
6. **Blank/empty columns still have their own bordered element** — never omit an element just
   because a column has no value to show for a given row. (Part R2.)
7. **Free-text blocks use ONE shared box, not one border per line** — check the reference's
   actual bordering pattern before assuming per-line borders. (Part R3.)
8. **Bold/italic/alignment verified per-element against the reference's REAL font/alignment**
   — do not assume a whole sentence or whole table is uniformly bold/centered just because one
   part of it visually looks emphasized; check via `get_text('dict')` span-level font names,
   the same way "Production:"/"PRODUCTION:" was found wrongly bold in R07.002 despite no
   visible reason to suspect it. (Round 7.)
9. **Row-rect widths and any other full-width convention re-derived per table** — never copy a
   width constant from a sibling table's row-background rect; sum THIS table's own columns.
   (Part T1.)
10. **Opaque-fill elements overlaid on another rect checked for BOTH border and fill offset**
    — not just the border, which is usually the more visually obvious half of the defect.
    (Part T2.)
11. **Section-title-to-divider spacing self-consistent across the whole report** — compare
    every section title's gap-to-its-own-line against every OTHER section title's gap in the
    same document, not just against the reference in isolation. (Part T3.)
12. **Any band-height change re-verified via page count** — after touching ANY band's declared
    height, recompile and confirm the page count is still the reference's real page count
    before doing anything else. (Part S2.)

**The meta-lesson underneath all 8 rounds: a "does it look right at a glance" pass is not the
same as "does every element's exact coordinate, height, font, and fill match the reference" —
the owner's repeated, escalating pushback was specifically about the gap between those two
standards. Apply this same rigor UP FRONT on R07.003-R07.006 rather than waiting for the same
pattern of pushback rounds to repeat there.**

## Part U — the 12-item checklist re-run on R07.005 found the SAME wholesale defect class as
R07.002, plus two genuinely new sub-classes: a raw-image-extraction distortion, and a
silently-dropped TITLE (from the R07.005 full re-audit, 2026-08-31)

**U1. Confirms the meta-lesson above generalizes beyond R07.002 specifically** — R07.005 had
been marked "done" off the same shallow text-match + 10-label spot-check, and the 12-item
checklist re-run found it had the identical wholesale problem: zero real gray gridlines, zero
real purple header fills (only 2 wrongly-purpled section titles using the wrong shade), zero
section dividers, and the font-extension jar (`inpex-arial-fonts.jar`) not even wired into
`pom.xml` — despite every other R07/R10 report in the project having it. **Do not assume a report
that "passed" its original build session actually got this rigor applied — check `pom.xml` for
the font jar and run the histogram before trusting a prior "done" status, even on a report that
was never specifically called out by the owner.**

**U2. A raster logo image extracted directly from a PDF's image XObject (`Pixmap(doc, xref)`,
`page.extract_image()`, or a fully manual `zlib.decompress()` of the raw stream) can decode to a
VISIBLY DISTORTED image even when the byte count matches `width*height*3` exactly (ruling out a
predictor/stride mismatch) — while `page.get_pixmap(clip=<real bbox>)`, i.e. asking the renderer
to actually draw that region of the live page, produces the correct image every time.** Confirmed
on R07.005's INPEX logo (plain `FlateDecode`/`DeviceRGB`, no unusual filters) via three
independent raw-extraction attempts, all producing the same sheared/merged-looking distortion,
against one working method. Root cause not fully identified (something in the image's real
PDF-level color/transform handling isn't captured by a naive raw-byte read). **Rule: always
extract an embedded raster logo via a high-DPI `get_pixmap(clip=<bbox>)` crop of the actual page,
never via `Pixmap(doc, xref)`/`extract_image()` on the image object directly** — the latter two
are for verification/measurement, not for producing a usable asset file.

**U3. A `staticText` element can be SILENTLY DROPPED FROM THE RENDER ENTIRELY in a way that a
full-page screenshot glance will not catch, even for the report's own MAIN TITLE.** R07.005's
title "Ichthys: Offshore Production Report" (21pt bold-italic, `height="24"`, under Part F1's
`fontSize*1.2`+margin rule needing ~29-30pt) was completely absent from both pages' extracted
text - but every rendered PNG I looked at before running `page.get_text('text')` "looked fine":
the missing title just reads as a bit of extra blank space under the logo, not as an obviously
broken layout, unless you are specifically looking for that exact string. **This is the strongest
argument yet for making a whole-page `page.get_text('text')` word-frequency diff (Part P4)
against the reference a MANDATORY step on every single report, every session, no exceptions -
not a nice-to-have added after a visual pass looks suspicious.** The same build also separately
dropped one word ("Quantity" out of "YTD Quantity") from a header element whose width was set to
the reference's own MEASURED text width (63pt) - this engine's real Arial-BoldItalicMT metrics
needed more room than the reference's measured width, so copying the reference's measured width
verbatim is not a safe substitute for giving the element genuine slack (fixed by widening to
90pt). Both defects were found only by the word-diff, neither by a coordinate spot-check or a
visual glance.

**U4. Adding a border to a shared cell style can expose a pre-existing, previously-invisible
COORDINATE GAP between two adjacent DATA cells, not just between a header and its data rows.**
R07.005's well-grid had a real ~25pt gap between the "Status at month end" and "Online (hrs)"
data columns from the original (unbordered) build - invisible with no border, but rendered as a
distinct blank bordered "phantom column" the moment `PlainValueStyle` gained a `<box>` pen this
session. This is the same root cause as Part Q3 (style-level border fix exposing a gap) but
confirms it applies data-cell-to-data-cell, not only style-to-neighboring-element - check EVERY
adjacent-column boundary in a repeating grid after adding borders, not just the ones adjacent to
a header that was independently rebuilt.

## Part V — proactively applying the 12-item checklist to R07.006 confirmed the SAME defect
class recurs project-wide, plus 3 new mechanical findings (from the R07.006 full-rebuild pass,
2026-08-31, run same-day and independently of the R07.005 session above — this and Part U were
written concurrently by two parallel agents that didn't know about each other, hence the
renumbering here to keep the sequence unique; no content was lost or overwritten)

**V1. The 12-item checklist is not specific to R07.002 — applying it UP FRONT (rather than
waiting for owner pushback) to a DIFFERENT report (R07.006, already marked "done" the day
before on a text-match + 9-point spot-check) found the SAME core defect classes: absent logo,
absent divider lines, and — the most consequential — a completely INVERTED purple-vs-plain
title convention. R07.006 had TWO section-label types that each needed the OPPOSITE treatment
from what was built: sub-section labels inside the main table ("Production"/"Internal
Consumption"/"Losses"/"Delivered") were wrongly purple-filled (reference: plain bold, no
italic, no fill), while the 5 section titles below the main table ("Inventory"/"Liftings"/
"CCPP"/"Environmental"/"Comments") were wrongly BUILT AS the purple bar itself, merged with
their own column-header row (reference: plain bold-ITALIC title on its own row with its own
divider line, then a SEPARATE purple-filled column-header row below it). Two different label
roles, two different WRONG directions, in the same single report — reinforces M6's lesson
("different cell ROLES can use different conventions in the SAME report") one level up, at the
level of whole section/title roles rather than just column alignment.

**V2. `fontName="Arial"` with `bold="true"`/`italic="true"` compiles with ZERO error and
renders in the exported PDF as PLAIN, NON-BOLD, NON-ITALIC HELVETICA — silently, on this
project's actual runtime (`net.sf.jasperreports:jasperreports-fonts:7.0.3` on the classpath via
Maven, no Jaspersoft Studio).** Confirmed via an isolated 3-line mini-repro
(`mini_test.jrxml`→`mini_test5.jrxml`) BEFORE touching the production file: `get_text('dict')`
on the mini-test's own OUTPUT PDF showed `font=Helvetica flags=0` regardless of the bold/italic
attributes set on the source XML. Root cause, found by extracting and inspecting
`jasperreports-fonts-7.0.3.jar` directly: its bundled `jasperreports_extension.properties` only
registers the **DejaVu** family (Sans/Serif/Sans Mono, each with real Bold/Oblique/BoldOblique
TTF variants) — "Arial" is never a registered font family in this environment, so both AWT (at
fill/measure time) and iText (at PDF-export time) silently substitute a plain default with no
error at either stage. This is Rule 10's documented gap made concrete and confirmed for this
specific project's actual dependency set.

**CORRECTION to V2 (2026-08-31, later same day, owner-directed):** the original write-up above
concluded "switch to `fontName=\"DejaVu Sans\"` everywhere" and shipped that as the fix. That
was WRONG against the owner's standing "layouts must MATCH IDENTICALLY, with no exceptions"
directive — the reference PDF's own real fonts (confirmed via `get_text('dict')` on
`R07.006 - Onshore Production Report.pdf`) are `Arial`/`ArialBold`/`ArialBoldItalic`/
`ArialItalic`, not DejaVu Sans. Making bold/italic visually distinguishable is NOT the same
bar as matching the reference's actual typeface family — different letter shapes/spacing/
character width are a real, visible mismatch even when bold vs. italic now render distinctly.
**The correct fix is to register a real Arial font extension jar** (`com.inpex:inpex-arial-fonts`,
`system`-scope, `systemPath` pointing at a co-located `output/fonts/inpex-arial-fonts.jar`) —
this was already proven working on sibling reports R07.002 and R07.004 in this same project
BEFORE this U2 finding was written, so "the fix is not register an extension jar" was simply
incorrect: that exact fix already existed and should have been replicated instead of introducing
a different font family. R07.006 now uses this same jar; verified post-fix via `get_text('dict')`
showing `ArialMT`/`Arial-BoldMT`/`Arial-ItalicMT`/`Arial-BoldItalicMT` in the exported PDF. **Rule:
when a font silently fails to register, check whether a sibling report in the same project has
ALREADY solved this exact problem with a real extension jar before reaching for a different font
family as a workaround — a workaround that merely looks visually distinct is not the same as
matching the reference's real typeface.**

This defect (and the original DejaVu-Sans mis-fix) was invisible on a full-page 150dpi screenshot
glance (text looked present, roughly correct size, and even looked vaguely "upright" at that
resolution) — it was caught only by the dedicated `get_text('dict')` span-font check that
checklist item #3 and #8 already mandate, cross-checked against the REFERENCE's own real font
names, not just "is bold/italic now visually different from regular." Since virtually every
prior R07/R10 report in this project used `fontName="Arial"` with bold/italic styling, **this
defect should be assumed present and re-checked on EVERY already-"done" report in this
project**, not just R07.006 — and any fix found should wire the real Arial jar (per R07.002/
R07.004), never substitute a different font family.

**V3. A `kind="line"` element with a declared `height="0"` is still validated by the compiler as
occupying 1pt of vertical space at a band's boundary.** Placing a horizontal divider line at the
exact measured bottom-of-band y (e.g. `y="1117"` on a `title height="1117"` band, from a
real reference measurement) fails compilation with `"Element bottom reaches outside band area:
y=1117 height=1"` — note the reported height is 1, not the declared 0. **When a divider/rule
line's measured position lands exactly at a band's declared height, clamp its y to
`declared_height - 1`, not `declared_height`, even though the element's own `height` attribute
is 0.** This is a narrower, more specific case of Rule/Geometry-4's "element_y + element_height
<= band_height" that isn't obvious from the XML alone, since the XML says height=0.

**V4. A header cell containing MULTIPLE STACKED TEXT LINES (e.g. "Short Term" / "Forecast" /
"(tonnes)" as 3 separate spans at 3 different y-positions within one visually-tall purple
column header) must position EACH line at its own measured y — using the CELL's full height
with `vTextAlign="Middle"` for every line centers all of them on top of each other into
unreadable overlapping text.** This is a variant of Part P's "measure per-element, don't reuse a
container's box for independent content" pattern, but specific to text lines that are visually
part of "one heading" yet are actually separate spans in the reference's own PDF structure —
treat every text span as needing its OWN vertical position, and only borrow the containing
cell's x-range (for horizontal centering across the full column width), never its y-range too.

**V5. A generator that classifies a reference PDF's raw `get_drawings()` output into named
groups (here: "fill+border header cells" vs. "border-only plain cells" vs. "divider lines", by
bounding-box proximity matching between a fill rect and its paired stroke rect) can rebuild an
ENTIRE report's layout in one pass with a level of positional accuracy a manual/iterative
pushback-round process cannot match** — verified afterward via an EXACT-COORDINATE set-diff
(not just a color histogram) between reference and generated PDF: of 258 real bordered cells in
the reference, all 258 were reproduced at the exact same rounded integer coordinates, with only
3 extra (harmless, sub-visible, individually investigated and disclosed rather than silently
carried) cells traced to the reference's OWN inconsistent border-stroke omission on 3 of its 4
CCPP header cells. **When a report needs the SAME rigor as an 8-round pushback session but no
owner is available to catch issues interactively, building the fix as a measurement-driven
generator (not hand-editing individual elements) both moves faster AND is independently
verifiable via an exact-coordinate diff in a way that manual edits are not.**

## Part W — a correction to Part V2 (a real Arial extension jar DOES exist project-wide), plus 3
new findings from the R07.003 full-rigor re-audit (2026-08-31)

**W1. ⚠ CORRECTION to Part V2 — "use DejaVu Sans instead of Arial" is NOT this project's actual
fix; a real custom `com.inpex:inpex-arial-fonts` extension jar already exists and is wired into
17 other reports' `pom.xml` files (R07.001, R07.002, R07.011-025, R10.002) via a
`scope="system"`/`systemPath="${project.basedir}/output/fonts/inpex-arial-fonts.jar"`
dependency.** U2 concluded "Arial is never a registered font family in this environment" from a
mini-repro that happened not to have this jar on its classpath — true for THAT repro, but not
true for the project as a whole. R07.003 was missing this exact dependency (its `pom.xml` had
`jasperreports-fonts` — the DejaVu-only bundled jar U2 correctly describes — but not the
project's own custom Arial jar), which is why its own font check reproduced U2's exact symptom
(`Helvetica`, no bold flag). Confirmed the fix by copying `inpex-arial-fonts.jar` from a working
sibling report's `output/fonts/` folder and adding the same dependency block: a `mini_fonttest.jrxml`
isolated repro went from `{'Helvetica'}` to `{'Arial-BoldMT', 'ArialMT'}` with zero other change.
**Rule: before concluding "this project has no way to render Arial correctly" on any report,
`find` the whole `C:\Projects\INPEX` tree for `inpex-arial-fonts.jar` first — if ANY sibling
report has it (as of 2026-08-31, 17 do), the fix is copying that jar + its 5-line pom.xml
dependency block into the broken report's own `output/fonts/`, not switching fonts.** A per-report `pom.xml` is
not self-evidently complete just because it compiles cleanly with zero error — compare it
against a working sibling's dependency list before trusting an "it must not be possible"
conclusion drawn from one isolated repro's classpath.

**W2. A bare `<element kind="rectangle">` with NO `mode`/`pen` at all — not just one with a
bare `<pen>` (M3's case) — still defaults to a visible BLACK width-1.0 border, and this can slip
through completely unnoticed when the rectangle exists purely as a band-height spacer (Part
L3's "unconditional spacer" pattern for forced-page-break `<detail>` bands).** A `1x1090`
spacer rectangle added specifically to stop a detail band collapsing to zero height rendered as
a solid black vertical line down the entire left edge of every page it appeared on (4 of 5
pages) — invisible to a text-only diff (a line has no text) and easy to miss on a full-page
screenshot glance if you're not specifically looking at the page edges. **Any element added
purely for band-geometry/height-reservation purposes (not for its visual content) needs
`mode="Transparent"` and an explicit `<pen lineWidth="0.0"/>` from the moment it's written, not
discovered later** — this is now the 3rd documented case of a "structural, not decorative"
element (M3's bare pens, D2's freestanding lines, and now spacer rectangles) defaulting to a
visible black artifact when nobody thought to make it explicitly invisible.

**W3. A table's column header row and its data rows can independently drift out of sync with
EACH OTHER (not just against the reference) when only one of the two is ever revisited across
multiple edit passes — and the DATA rows, not the header, can be the ones that are actually
correct.** R07.003's Production Quality table had a header row with two columns overlapping by
37pt (`N2`/`C6+` both claiming roughly `x=553-598`) and two other columns mislabeled — but the
DATA rows underneath were entirely correct (confirmed via one specific row's own real value at
its real x matching the reference exactly). The header had simply never been updated when the
data-row generator was corrected in an earlier pass. **Rule 4/R1's "re-check every row that
depends on a fixed column boundary" already covers this, but the specific new wrinkle here is:
don't assume the HEADER is the source of truth to fix the data rows against — check BOTH
independently against the reference, because either one might be the one that's actually still
wrong.**

**W4. A free-text/narrative table with a Type/Body/Author (or similar N-column) structure per
entry needs each entry's raw extracted text explicitly split into its N columns BEFORE layout —
never render the whole raw block (with the column-marker lines still embedded in the body text)
as one wide text element and hope it visually reads as a table.** R07.003's "Comments" section
(6 entries across 3 pages) had each entry's Author name and Comment Type extracted correctly as
the first two lines of a text-splitting script, but never separated OUT of the body text into
their own positioned elements in their own columns — the whole "Isabella Boyd\n<Type>\n<body>"
string was placed as one 710pt-wide block, UNDER a genuinely separate 3-column purple header row
("Comment Type"/"Comments"/"Author") that had been built correctly. Compounding this, the first
entry's block was positioned at a y that predated the section's own title/divider/header (a
leftover from before those were added), so the header rendered visibly ON TOP OF the body text's
"Degraded/Impaired SCE" line — a severe, immediately-visible overlap that a text-only diff
cannot catch (every word is still present, just glued into the wrong column and the wrong paint
order). **Rule: for any N-column free-text table, verify column-splitting and vertical
positioning together, via a rendered-PNG visual check specifically of that section — a
generator that gets the EXTRACTION right (correct entries, correct line counts) can still get
the LAYOUT completely wrong, and neither half implies the other is also correct.**

## Part X — a battery of targeted automated checks is NOT a substitute for reading the whole
page; all 4 of R07.003-R07.006 were rejected by the owner despite "passing" every check the
prior audits ran (2026-08-31)

**X1. Histogram/word-diff/zoomed-crop checks can all individually "pass" while the report is
still visibly wrong — the missing check is a plain full-page render read next to the full
reference page, at legible scale, start to finish.** Four parallel background-agent audits
(R07.003-R07.006) each ran `get_drawings()` color histograms, `get_text('dict')` font checks,
whole-page word-frequency diffs, and zoomed crops of specific regions they suspected might be
wrong — and each reported the report "genuinely matching." The owner's own comparison rejected
ALL FOUR. What those audits were missing wasn't rigor in general, it was **looking at the
ordinary, unzoomed, full page** — the specific defects that surfaced immediately on doing that
(a garbled logo, fragmented internal table borders, wrong indentation, a value in the wrong
column) were each individually detectable by eye at normal reading scale, but none of the
targeted checks happened to be pointed at that exact spot. **Rule: the FIRST verification step
on any report — before histograms, before word-diffs, before zoomed crops — should be rendering
every page in full and actually reading it end to end against the corresponding reference page.
Targeted checks are for confirming/diagnosing what a full read already flagged, or for catching
things too small to see (exact color hex values, font names) — they are not a substitute for
the read itself.**

**X2. A full-page visual impression is still not proof — verify it against real coordinate/font
data before acting, the same rule as always, just applied to what the full-page read surfaces.**
In the same session, a full-page read of R07.003 produced TWO leads that turned out to be FALSE
on measurement: "every data row is missing italic" (checked via `get_text('dict')`: both the
reference AND the generated PDF use plain `Arial` for data rows — no defect existed) and "the
Major Equipment Status header has a dashed border" (checked via `get_drawings()`: zero dashed
strokes in either PDF — a rendering/anti-aliasing artifact at low DPI, not a real pen style).
Both were dropped without action. Every defect that WAS fixed this round was first confirmed
with `search_for()`/`get_drawings()`/`get_text('dict')` coordinates before any edit was made.
**The two-step discipline is: full-page read to generate candidate defects, then real
measurement to confirm or reject each one — skipping either half produces either false
confidence (skip the read) or false positives acted on as if true (skip the measurement).**

**X3. A full-width label element sized wider than its real column, paired with per-row value
elements each individually sized to that row's specific number's string length, produces
FRAGMENTED, position-varying internal borders — a distinct visual defect from Part T1's
"wrong-width row-rect," but the same underlying cause (column width not derived from the
table's real, measured, CONSISTENT boundary).** Found identically on R07.003 and R07.004's CCPP
tables: `get_drawings()` showed the reference draws each cell as ONE clean rect per column,
constant across every row, while the generated version drew 8-9 line segments per row at
DIFFERENT x-positions row to row (label width=390 overreaching almost to the next column,
value width/x varying with `"148"` vs `"23"` vs `"7,030"`'s different string lengths). Fixed by
resizing every label/value element in the table to ONE consistent set of column
x/width values, derived from the header row's own real rects — not from the label's or value's
own text-content-driven sizing.

**X4. A row with TWO label+value column pairs (e.g. "Off-specification tank closing volume" |
value1 | "STG bypass valve" | value2) can have its one real data value placed under the WRONG
label — a genuine data-position defect, not a cosmetic one, and NOT caught by a word-frequency
diff (the value "2" is present in both PDFs, just in a different cell).** Found identically on
R07.003 and R07.004: measured the reference's real glyph x-position for the value and confirmed
which of the two value columns it actually falls under, rather than assuming symmetry or trusting
the existing element's position. **Rule: for any row pairing two label+value blocks side by side,
verify EACH value's real x-position against the reference independently — do not assume a value
is under "the label it's currently next to" in the build just because nothing else about the row
looks obviously wrong.**

**X5. A corrupted/distorted logo image is trivially visible on an ordinary full-page render at
normal reading scale, yet was missed by two full audit rounds that never happened to zoom in on
the logo specifically.** R07.006's logo rendered as a visibly garbled "INbEX" (malformed
letterforms) — the exact same raw-XObject-extraction distortion already documented as Part U2
from R07.005's own logo, and the fix was identical: measure the real bbox via
`get_image_info()`, re-extract via `get_pixmap(dpi=300, clip=bbox)` on the LIVE reference page,
overwrite the asset. **Any report using a raster logo should have that logo specifically zoomed
and visually confirmed legible — "the image element renders without a compile error" and "the
image element renders the CORRECT, undistorted picture" are two different claims, and only a
direct look (not a histogram, not a word-diff) can confirm the second one.**

## Part Y — border DOUBLING is a distinct, systemic defect class; a per-attribute diff can score ZERO on a visibly-broken section; and detail-record bands reuse the same local y as the title band (from R07.003's owner-verified round, 2026-09-01)

R07.003 was signed off by the owner on 2026-09-01 after a full screenshot-driven round. Seven
defect classes came out of it. R07.004-006 were built the same way and should be assumed to
share them until measured otherwise.

### Y1 — Doubled gridlines: every cell drawing its own 4 sides, with cells not touching
The single biggest defect, and the one the owner described as "uneven thickness ... more
noticeable in tables with more columns and rows".

Measured: Crystal's interior gridlines render **0.96pt**; mine rendered **1.92pt**, alternating
1.92 / 2.04 down the table — that alternation is what reads as "uneven".

Cause: rows sat on a 14pt pitch but each cell was only 13pt tall, leaving a 1pt gap, and every
cell drew a full four-sided border. So each row boundary got **two separate 1pt strokes 1pt
apart**, merging into a ~2pt band. Same on the vertical axis wherever a cell's right edge was
1pt short of the next cell's left edge — which is why it worsens with column count (more shared
edges, more doubling). Crystal's own edges sit ~0.5pt apart and overlap into one ~1pt line.

Fix: make neighbouring cells **share the same edge coordinate** so the two strokes are
coincident. Concretely: cell height = row pitch, and cell right edge = next cell's left edge.
~262 elements on R07.003.

Four traps while doing this, each of which cost a rebuild:
- **Gaps of 2pt exist too** (Inventory used height 12 on a 14pt pitch). A pass that only closes
  1pt gaps leaves those doubled.
- **The mirror case**: a cell 1pt TALLER than its pitch OVERLAPS the next row and doubles
  identically. R07.003's full-width sub-heading rows ("Production", "Losses") were `y=372 h=13`
  with the next row at 384 — bottom edge at 385, 1pt PAST the next row's top.
- **Only ever GROW.** A tiling pass that also shrinks cells whose height exceeds the pitch will
  push some under the minimum render height and silently drop their text (Part F1). This
  happened — two page-2 labels vanished, caught only by the text diff.
- **Header cells with nothing beneath them don't get grown**, so a pass that grows by pairing
  leaves a step in the header's bottom border. On R07.003's Major Equipment Status, five header
  cells became 27pt and two stayed 26pt, producing a visible step at the "Planned" column.

Objective test — do not eyeball it: render a 600 dpi strip across the gridline, probing only at
x positions where the strip above and below is clean white (so glyphs can't inflate the reading),
and compare the dark-run width against the reference's. `tmp/compare_ink.py` does this matched
gridline-by-gridline across both axes and all pages.

### Y2 — In a multi-line row, EVERY cell must take the row height
On Comments-style tables (R07.003 pages 3/4/5), the label and author cells were 12pt tall while
the Comments cell spanned the whole row (297pt, 900pt, 415pt). Result: the left and right column
borders existed only as ~13pt stubs below the header and the rest of the row had no side border
at all — the owner's "missing borderline for data columns". Fix: every cell in the row gets the
row's full height. Check the text fits FIRST (measure the last span's bottom y) before shrinking
any cell to the reference's row height.

### Y3 — Check each detail record separately; a whole page can be missing its rules
R07.003's page 2 (`REPORT_COUNT == 1`) had **no `<line>` elements at all** — no page-header rule
and no rule under any of its five section titles. The other records had theirs. A per-page
missing/extra horizontal-rule diff against the reference (`tmp/diag_all_lines.py`) finds this
immediately; nothing else did.

### Y4 — Continuation pages have no TOP rule
Where a table continues onto the next page (R07.003 pages 4 and 5), Crystal draws only the
verticals plus a bottom rule — no rule at the top of the page. Reproduce with
`<box ...><pen lineWidth="1.0" .../><topPen lineWidth="0.0"/></box>` on the element, repeating
the style's own pen/padding in the element box so nothing else resets.

### Y5 — Header columns must be derived from the DATA-row boundaries
Consumables, CCPP and Environmental all had headers whose columns were derived independently of
their data rows, producing steps at the table corners (header ending at 790 vs data at 792) and,
on Environmental, data rows on completely different boundaries from their own header. Always set
the header to the data rows' boundaries, not to its own arithmetic. (Extends Part W3.)

### Y6 — A row with fewer values than columns still needs the empty cells
Crystal draws an empty bordered cell; omitting it makes that column visually disappear for that
row. Found on R07.003's page-1 Production table and again in CCPP's last two rows.

### Y7 — Footer rule vs footer text
Both the rule and the footer texts sat at `y="0"` in `pageFooter`, so only the rule's own
thickness separated them (0.5pt gap vs Crystal's 2.1pt). Fix: band height +1 and text to `y="2"`.
One change, all pages — but verify it on every page rather than assuming the shared band applies.

### Y8 — THE METHODOLOGY LESSON: a clean numeric diff does not mean the section is correct
After fixing the Production Quality label column, the per-span diff reported **0 issues** on that
section. It was visibly wrong: Crystal paints the header purple continuously across the
label/C1 gap, mine had a white gap at x=172. Pixel sample: ref (68,63,135), gen (255,255,255).

The diff was blind to it because it compares text spans, and no text lives in that gap. Every
per-attribute check has a blind spot exactly where its attribute is absent.

**Order of operations: render the section as a cropped PNG and LOOK first; use measurement to pin
down what the eye already found.** Not the reverse. Two of this round's defects (the purple gap,
and a regression where a narrowed cell clipped "CPF rich gas export to GEP (mol %)" to "(mol")
were found only by looking. The owner's standing expectation is now: show paired gen/ref crops as
evidence before claiming anything is done.

### Y9 — `<title>` and `<detail>` bands reuse the same local y values
Page 1 is the `<title>` band; pages 2-5 are `<detail>` records separated only by
`printWhenExpression`. **A positional edit selected by y alone silently hits all five pages.**
A first fix script rewrote 37 elements when only 6 were intended and corrupted pages 2-5. Always
range-guard by band (line range) or by the record's `REPORT_COUNT` value, and print the count of
elements changed so an unexpected number is caught before the rebuild.

### Y10 — When the reference overflows a cell, split the element
Crystal lets one Production Quality caption overflow its cell border (text ends at 169.2, past
the 167 boundary). A JasperReports `staticText` clips at its own width, so it cannot reproduce
that directly — use a bordered blank cell at the true column width plus a borderless overlay
wide enough for the caption. (On R07.003 this was later made unnecessary by restoring the correct
column width, but the technique is the general answer to "the reference's text is wider than its
own cell".)

## Part Z — a defect counts even when the ORIGINAL has it; fix fonts before geometry; and every reference-comparison check is blind to internal inconsistency (from R07.004's owner-driven round, 2026-09-01)

### Z1 — THE STANDING RULE: two standards, not one
On R07.004 the owner found that a table's header divider rendered **2.04pt** while every
data-row divider below it rendered **1.02pt**. Measured at 1200 dpi, solid `#D6D6D6`, no
antialiasing ambiguity:

```
header row : 282.48 .. 284.46 = 2.04pt
data row   : 282.48 .. 283.44 = 1.02pt
```

**The Crystal reference has the same 2pt header divider.** So a reference comparison called it
correct, and matching Crystal would have preserved the flaw. Owner: *"its defect but not a
defect from original crystal report"*.

> Match the reference, **and** be internally consistent. Where they conflict, the owner decides.

Cause of that particular instance: the header cells sat at local `1..261` and `262..522`,
leaving a 1pt gap, so TWO 1pt strokes landed side by side (abs 283 and 284). The body cells
share their edge, so one stroke. Making the header cells share their edges on the body's own
boundaries gives a single 1pt line.

### Z2 — every check built so far was reference-only, so this class was invisible
`compare_ink.py`, `diag_all_lines.py`, `check_value_positions.py`, `check_vertical.py` all
compare generated vs reference. **None compared the output against itself.**
`workstreams/crystal-to-jasper-conversion/_checks/check_internal_consistency.py` now does:
per table, are all column-line thicknesses equal (including the one inside the header band),
are row-line thicknesses equal, are row heights uniform.

Validate any such check against a build that HAS the defect before trusting it — this one
reports the defect on the pre-fix build and 0 on the fixed build. A check that has never fired
is not a passing check.

### Z3 — fix font sizes BEFORE any geometry
R07.004 rendered all body text at 6.5pt where the reference uses 9.0 (headers 10.0, footer
6.0). Row height follows font size — the reference's HSE rows are 17pt to hold 9pt text, mine
were 12pt holding 6.5pt. Measuring borders first would have meant redoing every table.

Confirm a size mismatch by RENDERED WIDTH, not the reported size: `"Injury events"` measured
51.1pt in the reference and 36.8pt in mine, a ratio of 1.39 = exactly 9.0/6.5.

**Then immediately re-run a text-presence check:** raising the captions to 10pt in 10pt-tall
boxes silently dropped **58** of them (Part F1). Any font-size change needs its boxes grown in
the same pass.

### Z4 — data cells built from their text width instead of the table's columns
The single biggest cause on this report, behind seven separately-reported defects. Headers were
right; data rows were sized around each value:

```
GEP header : 25 | 129 | 236 | 344 | 451 | 538 | 624
GEP data   : 37 | 117 | 222 | 322 | 422 | 512 | 617      (every boundary different)
Offtakes   : header ends 813, data row ends 822          (overshoots the table)
```

Snap every data cell onto its OWN table's header boundaries, and add an empty bordered cell
wherever a column has none — the reference draws one.

**Assign cells to columns BY ORDER, never by nearest left edge.** Nearest-edge assignment moved
all four Environmental values one column right and stacked two in the same cell. Borders were
perfect and every word was present; only the CONTENT was in the wrong box.

### Z5 — scope a tiling pass per TABLE, not per band
A band can hold many tables (R07.004's title band holds seven). Grouping rows by band means a
table's last row measures its step against a neighbouring table's row, the step comes out
smaller than the height, and the grow condition never fires. Half the gaps survived.

### Z6 — a style-scoped regex misses rows built from another style
Production's three sub-heading rows use `SubSectionTitleStyle`, not `Plain*Style`. A cell
pattern matching only `Plain*` left exactly the three gaps the owner had circled, through two
further passes. Enumerate the styles a table actually uses before writing the selector.

### Z7 — centring a left-aligned caption pushes x negative
`"POB"` sits in a 100pt box for 22pt of text. Setting `x = ref_centre - width/2` gave x=-37 and
the text clipped at the page edge, rendering as `"B"`; `"Description"` became `"cription"`.
For a left-aligned caption the element's LEFT edge is what must land on the reference's text
left, not its centre. Check the sign of every computed coordinate.

### Z8 — derive the left edge PER TABLE
R07.004's reference uses two left edges: 23.1 for most tables, **25.1 for Production and Gas
Export Pipeline**. One global pass moved 18 Production elements the wrong way. (Same family as
Part T1.)

### Z9 — JasperReports 7.0.3 rejects decimal element coordinates
`x="1.5"` / `y="779.5"` fails to load (`JsonMappingException`). Pen widths accept decimals;
element x/y/width/height do not. Where the reference sits on a half-point, pick the nearer
integer and say which sub-point error you accepted.

### Z10 — do not act on a magnified crop without measuring what you are about to change
I read a 450x crop of the Inventory header, concluded "the grey outline is missing", and
rebuilt all three cells as border + inset fill. The outline was never missing — the band was
1pt short. The rebuild **introduced 1.98pt of white into dividers that were already correct at
2.04pt**, i.e. it made a non-defect worse. Caught only by measuring the PRE-FIX state
afterwards.

Looking is how you FIND a defect (Part X, Part Y8). Measuring is how you confirm what it is.
Measure the current value of the thing you are about to change, before changing it.

### Z11 — the stale-output trap
The output PDF was open in the owner's viewer for much of this round, so `JRPdfExporter` writes
failed and the owner reviewed a file up to FOUR builds behind — three of the defects raised had
already been fixed. If a write fails on a file lock, either stop and ask for it to be closed
before continuing, or build to a distinct filename and say clearly which file the evidence
refers to. Never let a review run against an output you know is stale.

## Part AA — a report can use TWO base font sizes; `rectangle` header elements are invisible to text-element patterns; a MISSING cell breaks the row LINE, not just its box; and tolerances hide defects (from R07.005's owner-verified round, 2026-09-01)

### AA1 — derive font size PER ELEMENT when a report uses more than one base size
R07.005's reference renders **471 spans at 8.0pt** (its 30-well grid) and **101 at 9.0pt**
(every other table). Mine had everything at 8.0. A style-level change would have wrongly
enlarged the well grid.

Two-stage derivation, because text matching cannot place repeated values (`'0'`, `'4'`,
`'41,253'` appear dozens of times):
1. match element text + approximate position -> placed 47
2. for the rest, pair each REFERENCE span with the generated span at the same rendered
   position and read its size -> placed the remaining 49

Result: font histogram identical to the reference. **And read the style block for the current
size — do not assume it.** My first dry run assumed `HeaderTextOverlayStyle` was 8.0pt when it
is 10.0, and proposed changing 37 captions that were already correct.

### AA2 — header cells are `rectangle`; a pattern matching staticText/textField will miss them
This cost a round on R07.004 (Inventory header divider 2.04pt vs a 1.02pt body) and TWICE on
R07.005 (well-grid header on the wrong columns after the body was fixed; then 11 header
boundaries left doubled after the body de-double).

Any pass over table geometry must include:
`kind="rectangle"` with `style="HeaderCellBoxStyle"` (or whatever the report's header style is),
not only the text cells. Enumerate the styles a table actually uses before writing the selector
— R07.005's sub-heading rows also use `SubSectionTitleStyle`, and R07.004's used the same trick.

### AA3 — a MISSING cell breaks the row's horizontal LINE, because topPen is 0
With `topPen lineWidth="0.0"` on the data styles (the correct de-doubling setup), a row's TOP
line is drawn by the row ABOVE's BOTTOM border. So a column with no cell has:
- no border of its own, and
- nothing drawing the line above the row below it

which renders as a horizontal line broken into **stubs** either side of the gap — the owner's
words were "a short horizontal line stub". Fixing it is not cosmetic infill: the empty bordered
cell is what makes the row line continuous. The reference draws one in every column of every
row.

### AA4 — tiling passes must close OVERLAPS as well as GAPS
R07.005's sub-heading rows overlapped the row below by 2pt:
```
'Production' local 717 + height 14 -> bottom 731,  next row starts 729
```
Two horizontal lines 2pt apart with white between - read by the owner as a "narrow space gap".
'Internal Consumption' happened to be 813+13=826 and looked right, which is why three of four
sub-headings were wrong and one was fine. A pass that only grows cells to close gaps will never
find this. (Y-axis twin of Part Y1's overlap case.)

### AA5 — a tall cell spanning two header rows stops the line crossing that column
The label column's header was one cell `y=679 height=38` covering both header rows, so the
inter-header horizontal line did not cross it and appeared to start partway across the table.
The reference draws that line the full width. Split the tall cell at the row boundary.

### AA6 — TOLERANCES HIDE DEFECTS: 12pt was too loose
`check_value_positions.py` ran at `TOL = 12.0`. R07.005's data-row labels were **11.8pt** out —
they were not indented under their sub-headings at all — and the check passed them. The owner
found it by eye. Every border check also passed, because the boxes were correct and only the
text position inside them was wrong.

Threshold now **4.0pt**. Re-running the three finished reports at 4.0 immediately surfaced
real items: R07.003 135, R07.004 8, R07.005 3.

**Reading a large cluster:** 93 of R07.003's 135 sit at exactly -4.2/-4.3pt. That is ONE
systematic difference (my `rightPadding="4"` against the reference's ~1pt), not 93 defects.
Group by shift value before concluding anything about count.

### AA7 — element `<box><pen>` resets ALL four pens
Adding `<box leftPadding="16"><pen lineWidth="1.0"/></box>` to indent a label also switches the
TOP pen back on, which can re-introduce the double line a de-double pass just removed. Set the
pens you want explicitly (`<topPen lineWidth="0.0"/>`) whenever you add an element box to a
cell whose style relies on a zeroed pen.

### AA8 — order the passes: snap columns BEFORE de-doubling
I ran the de-double pass first, then the well-grid and page-2 column snapping — which
introduced fresh 1pt gaps and needed the de-double run again. Correct order:
fonts -> columns/geometry -> tiling/de-double -> alignment -> internal consistency.

### AA9 — tooling traps that cost real time this session
- **`sed` with backslash Windows paths silently does nothing.** It failed twice and I read a
  stale PDF both times before noticing. Use the Edit tool, or a `GENPDF` env var on the check.
- **`py -` waits on stdin and hangs until timeout.** Twice. Always write the script to a file.
- **The stale-output trap (Part Z11) recurred through the whole session.** The owner reviewed
  builds up to four generations behind because the PDF was open and writes silently failed.
  After ANY failed write, either stop and ask for the file to be closed, or build to a distinct
  name and say plainly which file the evidence refers to.

## Part AB — a report may define NO styles; OVERLAPPING border rectangles put a neighbour's border INSIDE a column; and Crystal draws two lines per boundary where tiling gives one (from R07.006's owner-verified round, 2026-09-01)

R07.006 completed the R07.003-006 set. It was the fastest of the four because the playbook
transferred almost unchanged — but it differed structurally in two ways worth knowing.

### AB1 — a report may define NO styles at all
R07.006 has no `<style>` block: every element carries inline attributes (`fontName`, `bold`,
`fontSize`, `hTextAlign`), and **borders are separate `rectangle` elements** with text in
separate `staticText` elements.

Consequences:
- **Every style-based selector returns nothing.** Passes written against
  `style="Plain(Label|Value)Style"` silently matched zero elements. Re-key on `kind` +
  coordinates. Always confirm a selector's match count before concluding "no defects here".
- **Tiling borders becomes risk-free.** The rectangles hold no text, so shrinking cannot trigger
  the Part F1 drop — one pass tiled all 149 of them, growing and shrinking freely. Contrast with
  R07.004/005 where cells carry their own text and shrinking dropped labels.

### AB2 — OVERLAPPING rectangles render a neighbour's border INSIDE the visible column
The most instructive defect of the set. On a main-table row:
```
4..187 | 185..273 | 268..359 | 355..446 | 446..532 | 530..618 | 616..704 | 699..784
        ^ovl 2      ^ovl 5      ^ovl 4     ^0        ^2         ^2         ^5
```
Column 2 spans 185..273 while column 3 starts at 268 — so column 3's LEFT border draws five
points **inside** column 2. The owner reported it as "extra borderline shown in Volume, Mass,
YTD Volume, YTD Mass, Annual Budget Forecast", and because the overlap varied (2/5/4/0/2/2/5)
the thickness looked uneven across the table.

This is distinct from the doubling in Part Y1 (cells 1pt APART, two strokes at the boundary).
Here the cells cross over, so the spurious line lands in the middle of a column and does not
look like a boundary at all. Tiling fixed both: 15 rendered column lines became 9.

**Check for it by comparing consecutive rect spans in a row, not just the boundary set** — an
overlap and a tile produce the same boundary VALUES, so a set comparison cannot tell them apart.

### AB3 — Crystal draws TWO lines per boundary; tiling gives one
R07.006's reference renders pairs at every main-table boundary, 0.6-4.6pt apart, because Crystal
leaves a gap between adjacent cells rather than tiling them:
```
207.3/208.8  290.5/294.9  377.5/381.4  467.6/468.2  552.2/553.7  637.8/639.7  721.2/725.8
```
Reproducing that means deliberately double-drawing every border — the exact thing Parts Y1/Z1
exist to eliminate, and it fails `check_internal_consistency.py`. The choice taken across all
four reports, offered explicitly to the owner and accepted: **one clean line per boundary,
positioned inside the reference's pair.** Present this as a decision, not a silent deviation.

### AB4 — the 4.0pt value tolerance earns its keep immediately
Tightening `check_value_positions.py` from 12.0 to 4.0 (Part AA6) caught, on R07.006 alone:
- 22 labels missing a 12.2pt indent under their sub-headings
- 22 values right-aligned where the reference centres them (up to 110pt out)
- **a DUPLICATED value element** — two elements at the same x with the same text, where one
  belonged in the neighbouring column

The duplicate would never have surfaced from a border or text-presence check: the text was
present and every border was correct.

### AB5 — compounding 1pt offsets
The Liftings section rule looked "too near the table" because TWO independent 1pt errors
stacked: the rule 0.85pt low and the header 1pt high, giving a 2.50pt gap against the
reference's 4.35pt. Fixing only one would have left it visibly wrong. When a gap is roughly half
what it should be, measure BOTH sides before changing either.

### AB6 — set status, R07.003-R07.006
All four owner-verified OK on 2026-09-01. Order of passes that worked, unchanged from Part AA:
`fonts -> columns/geometry -> tiling/de-double -> alignment -> internal consistency`,
re-running the text check immediately after any font change.

---

## Part AC — TRACING the reference PDF eliminates whole defect classes; an `Opaque` fill's own `<pen>` is a second stroke on the boundary; tiling must NOT close gaps Crystal leaves deliberately; and `get_drawings()`/`get_text()` never return IMAGES (from R07.001's build, 2026-09-01 — self-verified, owner review pending)

R07.001 is 7 pages and ~2,700 elements. R07.003-006 were hand-built and each cost several owner
review rounds, all on the same recurring defects. R07.001 was instead **generated by tracing the
reference PDF**, and the difference in first-build quality is the headline lesson of this part.

### AC1 — trace the reference instead of hand-placing geometry
Read the reference's own `get_drawings()` and `get_text('dict')` and emit one JRXML element per
drawing/span at the position Crystal itself uses. `local = absolute - margin`.

First traced build, before any fix round:

| | R07.003 (hand-built) | R07.006 (hand-built) | R07.001 (traced) |
|---|---|---|---|
| font histogram | needed passes | needed passes | **exact, first attempt** |
| values out of position | 135 | 47 | **1** |
| rule differences | 14 | 0 | **0** |

This removes by construction the three defect classes that dominated every hand-built report:
invented columns, cells that overlap or leave 1pt gaps, and values in the wrong box. Prefer
tracing for any remaining report of comparable size.

Two things a trace still does NOT give you — both cost a round here:

### AC2 — `get_drawings()` and `get_text()` do NOT return images
A pure trace omits every logo. This is the **third** report in this project with a missing logo
(R07.002 and R07.003 both shipped with it absent, then were fixed). Add the image element
explicitly, and check every page — R07.001 has it on all 7 at identical coordinates.

Then two traps on the asset itself:
- **The `logo.*` already sitting in `output/` may be the WRONG mark.** R07.001's was aspect 1.903
  against the reference's 5.791, and JasperReports' default `RetainShape` silently aspect-fitted
  it into a fraction of the box. **Compare the asset's aspect to the reference's drawn bbox
  aspect** — one division that catches this instantly.
- **Extracting the embedded XObject can produce a MALFORMED wordmark.** `fitz.Pixmap(doc, xref)`
  on R07.001's logo gave "INbEX" — the image is a stencil whose SMask carries the letter shapes,
  and pulling the XObject alone drops the mask.

  **Do this instead:** render the logo *region of the page* — `page.get_pixmap(dpi=600,
  clip=fitz.Rect(page.get_image_info()[0]["bbox"]))` — which reproduces exactly what the
  reference displays, mask included. Pair it with `scaleImage="FillFrame"`.

### AC3 — an `Opaque` rectangle's own `<pen>` is a SECOND stroke on the boundary
The single highest-value finding here, and the root cause of the "borderline thickness is not the
same" defect the owner reported on R07.004, R07.005 **and** R07.006.

Emitting a traced purple band as
`mode="Opaque" backcolor="#454087"` with `<pen lineWidth="1.0" lineColor="#D6D6D6"/>`
puts a grey outline ~1pt from the border rectangle on the same boundary, so two strokes render
where the reference has one:

```
page 7, band y 122-158              gen      ref
  x=23  table left frame (fill edge) 1.98pt   1.02pt
  x=653 column boundary (fill edge)  1.98pt   1.38pt
  x=812 no fill edge                 1.02pt   1.02pt
```

`<pen lineWidth="0.0"/>` on every fill took internal-consistency findings **14 -> 0** across all
7 pages. **A fill is only a fill in Crystal. Never give a traced fill a pen.**

### AC4 — TWO wrong theories died to measurement, not reasoning
Worth recording because the *method* is the lesson:
1. *"cells don't tile, so boundaries double"* — built a full tiling pass, moved **313
   rectangles**, and the internal-consistency count **did not change at all**.
2. *"the full-width frame rect isn't snapped to the tiled columns"* — snapped those too, and
   page 7 got **slightly worse**.

Only listing the actual JRXML elements with an edge near the offending abs x showed the `Opaque`
rect with `pen=1.0` sitting beside the `Transparent` one. Extends Part Y/AB: **when a fix moves
hundreds of elements and the measurement doesn't budge, the theory is wrong — stop refining it
and go read the elements at that coordinate.**

### AC5 — tiling must NOT close a gap Crystal leaves deliberately
Tiling corrects real overlaps, but applied unconditionally it destroys layout:

```
page 2, row y=632   reference: 23.15..77.45 | (gap) | 252.15..300.75 | ...
                    mine:      23..252 (one 229pt cell)  <- gap swallowed
```

Gate it on gap size. **And use a DIFFERENT threshold per axis:** Crystal's *horizontal* cell gaps
run to ~4.6pt (Part AB4), so 6pt is right there — but 6pt *vertically* swallowed a genuine 5.85pt
blank band on page 2 (row ends abs 626.2, next table starts 632.05) and deleted that rule.
Horizontal 6pt / vertical 3pt.

### AC6 — verify a "remaining difference" before calling it benign OR real
All three residual items on R07.001 were confirmed non-defects from raw data:
- **nbsp**: the reference uses `\xa0`; my JRXML *also* contains `\xa0` — the difference is
  introduced by PDF text *extraction* (Arial maps nbsp to the space glyph). Check the JRXML.
- **a value "11.9pt out"**: the reference span is `'SIMOPS          '` (len 16, ten trailing
  spaces). Trailing whitespace widens the bbox and moves the CENTRE while the text has not moved.
  Both start at x≈181. **A centre-based position check is unreliable on spans with trailing
  whitespace — compare left edges for left-aligned text.**
- **"gridline ink mismatch" of 3-4pt**: a gridline is never that thick. At those x positions the
  reference and mine had *identical* thin rects, or (at x=621.8) **neither had any line** — the
  probe was measuring glyphs. `compare_ink` reporting **0 unmatched** is the signal that all
  reference lines are present.

### AC7 — regenerate derived images after EVERY rebuild
Read a page-pair PNG showing the pre-fix logo and nearly reported it as unfixed. The stale-output
trap on this project has now bitten at PDF level (files locked open, `sed` silently failing) and
at PNG level. **Regenerate, then look.**

### AC8 — mechanical repeats of already-recorded mistakes
- `py -` **hangs on stdin to the 120s timeout — fourth occurrence.** Always write the script to a
  file. (Already a standing rule; still repeated.)
- `$(cat cp.txt)` inside `cd X && java -cp "...$(cat cp.txt)"` is expanded **before** the `cd`
  runs, so it read the wrong directory and failed twice. Read it in a separate statement after
  the `cd`. Also: R07.001's `cp.txt`/`target/` live at the report ROOT, and the build must run in
  `output/` for the relative `logo_ref.png` to resolve.

### AC9 — set status
R07.001: 7/7 pages, fonts exact, 0 rule differences, 0 internal-consistency findings, all
residual items verified non-defects, all 7 pages visually compared. **Self-verified; owner layout
review pending.** Full detail in
`workstreams/crystal-to-jasper-conversion/R07.001/FACT-FINDING-SUMMARY.md`; generator and tooling
in that folder's `build/`.

---

## Part AD — EC 14.2.4 ships TWO Jasper engines (6.21.4 legacy + 7.0.1 V7); check the JOB CLASS before concluding anything about version compatibility (2026-09-01)

A scheduler log showed `Error occured when generating jasper report. Error loading object from
InputStream.` I inspected `ec-worker`'s `com.ec.frmw-frmw-report-jasper-14.2.4.war`, found
`jasperreports-*-6.21.4.jar`, compiled four of this project's reports against those jars, watched
all four fail on JR7-only attributes (`bold`, `titleNewPage`, `forPrompting`), and concluded that
**every report needed rewriting in 6.21.4 syntax**. That conclusion was WRONG and would have been
a large piece of wasted work.

### AD1 — EC 14.2.4 has two report engines, selected per report definition
| Engine | JasperReports | Job class |
|---|---|---|
| legacy | 6.21.4, in `frmw-report-jasper-14.2.4.war/WEB-INF/lib` | `com.ec.frmw.report.screens.model.ejb.ECJasperReportJob` |
| V7 | **7.0.1**, in `ec-app.ear/lib/net.sf.jasperreports-jasperreports-7.0.1.jar` | `com.ec.frmw.report.screens.model.ejb.jasper7.ECJasperReportJob` |

Same JRXML, same report, two report definitions: `report_no 4` used the legacy class and failed
at load; `report_no 5` used the `jasper7` class and logged `Jasper report is filled.` The
`.jasper` was never the problem — the engine was.

**The tell is in the log's `JobInstance class name:` line and the `About to execute Jasper V7
Report Job...` message.** Read those BEFORE drawing any version conclusion.

### AD2 — 7.0.3-authored JRXML compiles under EC's 7.0.1
Verified by copying EC's own `jasperreports-7.0.1.jar` out of the container, putting it first on
the classpath to shadow 7.0.3, and compiling: R07.012 and R07.001 both `COMPILE OK`. So the local
7.0.3 toolchain is safe for EC's V7 path. (Not the same as guaranteeing identical rendering —
that still needs a real EC run compared against the reference.)

### AD3 — the method failure, which is the real lesson
Finding 6.21.4 in one WAR was a *fact*; "therefore EC cannot run JR7" was an *inference* I
presented as a conclusion after four confirming compile failures. Four confirmations of a
mis-scoped hypothesis felt like strong evidence and were worth nothing, because I never asked
"which engine did the failing job actually use?" — a question the log answered in a line I had
already been given. **Repeats Part AC4 in a new form: when a hypothesis implies a large amount of
rework, spend one more step disconfirming it before reporting it.** Cheapest disconfirming check
here was `grep 'JobInstance class name' <log>`.

### AD4 — EC fills from the .jasper, not the .jrxml
`Generate jasper report based on database source and jasper-file given by
/extension/ZREP/reports/<name>.jasper`, loaded via `ExtensionMgr` from extension `ZREP`. Editing
the JRXML changes nothing on EC until it is recompiled to `.jasper` and redeployed to that
extension path.

### AD5 — two live config defects seen in the same logs
- **Doubled JRXML path** in `report_item_param`:
  `/extension/ZREP/reports/extension/ZREP/reports/R07_012_FC_Lifting_Report.jrxml`. The sibling
  `Jasper Definition Url` is correct, which is why the V7 run still worked.
- **Parameter name mismatch**: EC posts `REPORT_DATE`; the JRXML declares `P_REPORT_DATE`.
  Undeclared parameters are silently ignored, so `P_REPORT_DATE` falls back to its hardcoded
  default and the report renders that month regardless of what EC passes. EC was passing
  **2026**-07-01 against a default of 2025-07-01.

---

## Part AE — images in an EC EXTENSION-hosted report must use the `/extension/<ID>/...` path, and EC's own injected `BASE_URL` provably CANNOT resolve there (2026-09-02, owner-confirmed working)

R07.012's logo failed on EC with `JRException: Byte data not found at: <value>logo.png` for three
successive values. Resolved only by reading EC source at `C:\DEV\GIT\ec-application-2`.

### AE1 — the working answer
```xml
<parameter name="P_BASE_URL" class="java.lang.String" forPrompting="false">
    <defaultValueExpression><![CDATA["/extension/ZREP/reports/"]]></defaultValueExpression>
</parameter>
...
<expression><![CDATA[$P{P_BASE_URL} + "logo.png"]]></expression>
```
Owner-confirmed GENERATED on EC. The image must sit beside the `.jasper` in the extension
(`reports/logo.png`), which it already did — placement was never the problem.

### AE2 — why that exact prefix, and nothing else
`ResourceServiceEC.getResourceAsStream(uri)` tries three things in order:
1. `getVirtualFile(uri)` — resolved against the **ear root**, so only ear-relative paths work
2. `ExtensionMgr.getResourceFromExtensions(uri)` — the extension path
3. `ResourceServiceBasic` — `file:/` URLs only, else `getClass().getResourceAsStream(uri)`
   (**classpath**, not filesystem)

Step 2 is gated by `ExtensionPaths.getExtensionIdFromPath`, which **requires** the prefix:
```java
path = stripStart(path, "/");            // extension/ZREP/reports/logo.png
path = stripStart(path, "extension/");   // ZREP/reports/logo.png
extensionId = path.substring(0, slashPos);  // "ZREP"; blank -> return null -> NOT FOUND
```
So `logo.png`, `./logo.png` and any absolute filesystem path all miss every step. Only
`/extension/<ID>/<path>` hits step 2. Confirmed by the `.jasper` itself loading that way:
`Extension resource [/reports/...jasper] loaded from extension ZREP`.

### AE3 — the trap: do NOT rename the parameter to `BASE_URL`
`JasperReportGenerator.generateJasperReportBasedOnUrl` line 171 injects, unconditionally:
```java
reportParams.put(PARAM_NAME_BASE_URL, getMainReportLocation(locateResource(reportUrl)));
```
`locateResource` returns `File.getAbsolutePath()` and `getMainReportLocation` strips the
filename, so **`BASE_URL` = an absolute filesystem path** like
`/opt/jboss/.../tmp/ecextension/<hash>/reports/`. Per AE2 that resolves at **none** of the three
steps. EC's own reports get away with `$P{BASE_URL}` because they live inside `ec-web.war`
(ear-relative, step 1), not in an extension.

**Therefore, for an extension-hosted report, a custom parameter name is REQUIRED.** Declaring
`BASE_URL` lets EC overwrite the correct literal with an unusable absolute path. The `P_` prefix
is protective, not a bug — passed parameters override `defaultValueExpression`, and EC cannot
clobber a parameter the report does not declare. This is an EC product limitation, not fixable
from the JRXML.

### AE4 — my method failures in this thread, all the same shape
Four wrong calls, each stated with more confidence than the evidence supported:
1. "EC bundles 6.21.4, so every report needs rewriting" — inspected one WAR (the *legacy*
   engine) and never checked which engine the failing job used. See Part AD.
2. "The logo works" — proved only that a local JVM working directory resolved `./logo.png`.
   Local `JREmptyDataSource`/CWD resolution and EC's repository chain are **different
   mechanisms**; the local check could not detect this defect class at all.
3. "The `P_` prefix is the whole bug, rename to `BASE_URL`" — recommended twice, exactly
   backwards, because I read the injection site (line 171) but not the resolver it feeds.
4. "Lines 174-190 restoring the classloader is the bug" — announced before reading
   `locateResource`. It is a real quirk (extension *classes* are off the context classloader
   during `fillReport`) but irrelevant to image loading.

**The owner twice told me the correct shape** (`<imageExpression>`, `$P{...BASE_URL} + "logo.png"`)
and both times I overrode it with local-toolchain reasoning. **Rule: when the owner states a
convention for a target environment I have not read the source of, treat it as ground truth and
go read that source BEFORE contradicting it.** Also: verifying in environment A says nothing about
environment B when the resolution mechanism differs — name the mechanism, not just the result.

### AE5 — local vs EC
`/extension/ZREP/reports/` cannot resolve locally. That is correct and expected: EC is the
target. Local/Studio runs need `P_BASE_URL` overridden to `""` at fill time (a harness concern,
not a report change). Any JRXML edit also needs recompiling to `.jasper` and redeploying to the
extension before it takes effect on EC.

---

## Part AF — a JR7→JR6 downgrade IS possible and can be byte-for-byte lossless; .jasper compatibility is BIDIRECTIONALLY broken; and two silent traps (style `<box>`, font extension) (2026-09-02, proven on R07.012)

Owner asked whether a 7.0.3 JRXML can be compiled by an older JasperReports. Short answer: not
directly — 6.x validates against its own XSD and rejects JR7 constructs at parse time. But the
**source can be converted**, and for these reports the conversion is lossless. Built and proven:
`workstreams/crystal-to-jasper-conversion/_jr6-downgrade/`.

### AF1 — it is a SYNTAX transformation, not a feature downgrade
An XML inventory of both reports shows only five element kinds (`staticText`, `rectangle`,
`line`, `textField`, `image`) plus styles/conditionalStyles, parameters, query, fields, variables
and standard bands. **Every one exists in 6.x.** No JR7-only feature is used, so a 1:1 mapping
exists. Jaspersoft Studio's *"you risk to lose part of the report content"* warning is about
reports using JR7 features — inventory the file before believing it applies.

**Do the inventory with an XML parser, not grep.** Line-based grep truncates multi-line
`<element ...>` tags and gave an incomplete attribute list twice in a row here.

### AF2 — result on R07.012
Compiled first try under real 6.17.0, then vs the 7.0.3 render:
```
text spans : 385 = 385     IDENTICAL (position, size, font, string)
drawings   : 1438 = 1438   IDENTICAL (every rect)
fonts      : ArialMT x351, Arial-BoldItalicMT x20, Arial-BoldMT x10, Arial-ItalicMT x4  (both)
```
Byte-for-byte equivalent rendered content, confirmed visually too.

### AF3 — `.jasper` incompatibility is BIDIRECTIONAL
| compiled with | EC legacy 6.21.4 | EC V7 7.0.1 |
|---|---|---|
| 7.0.3 | ✗ `Error loading object from InputStream` | ✓ |
| 6.17.0 | ✓ | ✗ same error |

**One `.jasper` cannot serve both engines.** The artifact must be paired with the engine in
`REPORT_ITEM.JOB_INSTANCE_CLASS`. Corollary: that error message says *nothing* about which
direction the mismatch is — always test the file against both.

### AF4 — trap: a `<style>` can own a `<box>`, and that is where the grid lives
First `emit_style` only walked `conditionalStyle` children and silently dropped 11 of 14 `<box>`
elements. The report **still compiled and filled cleanly** — and rendered **165 drawings instead
of 1438**, i.e. every cell border gone. 6.x XSD order inside `<style>`: `<box>` then
`<conditionalStyle>`. **A clean compile proves validity, never fidelity.**

### AF5 — trap: no font extension ⇒ `isBold`/`isItalic` are SILENTLY ignored
Without `inpex-arial-fonts.jar` on the classpath, 6.x resolves `fontName="Arial"` to nothing,
iText falls back to Helvetica, and the bold/italic flags are dropped without warning:
```
without: Helvetica x382                     (everything upright, non-bold)
with   : ArialMT x351 + 3 Arial variants    (matches 7.0.3 exactly)
```
The JRXML is identical and correct in both cases. **Diagnose by reading the embedded font
family names out of the PDF (`fonts_used.py`), not by inspecting the XML.** 7.x resolves Arial
without the extension, so this asymmetry only appears on the 6.x path.

### AF6 — XSD child order differs from JR7 source order
6.x validates `jasperReport` children strictly and `<summary>` must come **after**
`<pageFooter>`; JR7 files put summary earlier. Emitting source order fails validation. Same
class of issue inside elements (`reportElement`, `box`, `textElement`, `text`).

### AF7 — method note
Two false leads came from position-matching spans by `(page, text, row)`, which is ambiguous
when a row holds several identical values (`'0'`) — it reported fabricated 443pt offsets, the
same artifact recorded in Part AC6. Replaced with **exact sorted-tuple-list comparison**, which
has no matching step and therefore cannot manufacture that artifact. Prefer whole-list equality
over pairwise matching whenever duplicates are possible.

### AF8 — scope
R07.012 = 78 elements. **R07.001 = 2,694.** For R07.001 add a 6.x output dialect to
`R07.001/build/gen_001.py` rather than converting after the fact. Also: this proves equivalence
to the *7.0.3 render*, not to Crystal — a defect in the 7.x version is faithfully reproduced.

---

## Part AG — the JR6 downgrade generalises across 8 reports; a guard that checks only ATTRIBUTES silently dropped 4,336 child-form conditions (2026-09-02)

Ran the Part AF converter over the whole R07 set. **7 of 8 render byte-identical to their 7.0.3
originals; the 8th fails only because its source view is absent from this database.**

| Report | Elements | Render vs 7.0.3 |
|---|---|---|
| R07.001 | 2,694 | IDENTICAL (7 pages, 1,263 spans, 1,448 rects) |
| R07.002 | 767 | IDENTICAL |
| R07.003 | 571 | IDENTICAL |
| R07.004 | 380 | IDENTICAL |
| R07.005 | 691 | IDENTICAL |
| R07.006 | 520 | IDENTICAL |
| R07.012 | 78 | IDENTICAL, **and verified through EC on the legacy engine** |
| R07.011 | 181 | compiles; `TV_FC_PRODUCTION_REPORT` missing here (`ORA-00942`) |

So the downgrade is a general capability, not a one-report trick. Either EC engine can now be
targeted from the same 7.0.3 source.

### AG1 — THE lesson: a guard covering one shape of a construct is not a guard
After the dropped-`<box>` incident (Part AF4) I added an allowlist that fails loudly on any
element **attribute** the converter doesn't place. It then let R07.001 lose **all 4,336**
`printWhenExpression` conditions without a word, because:

- hand-built reports (R07.012) write it as an **attribute**: `printWhenExpression="..."`
- generated reports (R07.001) write it as a **child element**: `<printWhenExpression>...`

The attribute-only guard saw nothing wrong. Every gate passed — compile OK, fill OK, 7 pages,
correct page count — and the PDF rendered **all 6 detail records on every page**: 6,383 spans
against the correct 1,263, a 5× content blow-up. Detectable only by comparing against the 7.x
render.

**Rule: when a construct can appear in more than one shape (attribute vs child, inline vs
styled, compact vs classic), the guard must enumerate every shape.** Extended `check_attrs` to
validate child tags against `KIND_CHILDREN` as well.

Corollary worth keeping: **a page count matching is nearly worthless as a fidelity signal.** All
7 pages were present and correct in the broken build. Span and rect counts caught it instantly.

### AG2 — three more mechanical gaps the batch surfaced
Each found by real compiler errors, each a one-line fix:
- `summaryWithPageHeaderAndFooter` → `isSummaryWithPageHeaderAndFooter` (R07.004)
- **`<box>` pen ORDER is fixed by the 6.x XSD**: `pen, topPen, leftPen, bottomPen, rightPen`.
  JR7 files list them in author order; R07.004 failed with *"found leftPen, expected rightPen"*
  purely from that. Same class as the band-order issue (Part AF6) — **6.x validates sequence
  everywhere, so never pass children through in source order.**
- `markup` (e.g. `markup="styled"`, how R07.003's bold `Disclaimer:` is produced) belongs on
  `<textElement>` in 6.x. Losing it would quietly change rendered text weight, not error.

### AG3 — batching is what found all four
R07.012 alone passed every gate and taught none of these. Four distinct defects appeared only
once the converter met seven more reports with different construct mixes. **For any converter or
generator, run the whole corpus before believing it works** — a single passing case measures the
case, not the tool.

## Part AH — conditional styles, paint order, and three regex traps that all failed SILENTLY

Found while taking R10.026–R10.034 from ~52% to ~76% pixel agreement against their Crystal
originals. Every item below compiled, filled and rendered without a single warning, which is
what makes them worth writing down.

### AH1 — `<conditionalStyle>`: JR7 wants ONE self-closing element with ATTRIBUTES

The 6.x nested form is accepted by JasperReports 7.0.3's loader and then **ignored**:

```xml
<!-- WRONG in JR7 - loads, never fires, no warning -->
<conditionalStyle><conditionExpression><![CDATA[$F{X} != null && ...]]></conditionExpression>
                  <style forecolor="#FF0000"/></conditionalStyle>

<!-- RIGHT - verified against R07.012-R07.016, which already use it -->
<conditionalStyle conditionExpression="$F{X} != null &amp;&amp; ..." forecolor="#FF0000"/>
```

The expression lives in an **attribute**, so `&` becomes `&amp;` and any quotes inside it -
`startsWith("(")` - become `&quot;`. Symptom: negative values that should print red print black,
and nothing anywhere complains. Cost: two rounds, because "the style is present and names the
right field" was true and still not enough. **When a styling feature silently does nothing, look
for a working example already in the corpus before re-reading the docs** - four R07 reports had
the correct form all along.

### AH2 — a `kind="rectangle"` ALWAYS strokes its outline

With no `forecolor` and no `<pen>`, JasperReports strokes it in its **default black**. So
"remove the forecolor so the rectangle stops stroking over its own fill" produces the opposite
of the intent: every band fill gains a black edge. Measured in the build afterwards:
`stroke x 23..285 #000000` sitting exactly where the original strokes `#D6D6D6`.

- a rule or a solid band → `forecolor` **equal to** `backcolor`
- a cell background that must show the original's border → an explicit
  `<pen lineWidth="0.5" lineColor="#D6D6D6"/>` on the element

### AH3 — paint order is document order, and backgrounds are usually written last

268 text elements across eight reports were being painted over by rectangles that appeared later
in their band - captions losing their last line, a `MMBtu` header vanishing entirely - while
every one of them measurably rendered at the right position and size. Moving all rectangles
ahead of all text in each band fixed them in one pass. **A text element that measures correctly
but is not visible is an ordering problem, not a geometry one.**

### AH4 — three regexes that returned the wrong thing without failing

1. **`<style name="X"[^>]*(?:/>|>.*?</style>)`** returns a **multi-style REGION** for any
   self-closing style: greedy `[^>]*` eats the `/`, the `/>` branch cannot match, and
   `>.*?</style>` runs on to a later style's closing tag. Callers that clone a style then
   duplicate that whole region, and JR refuses the report with
   `JsonMappingException: Duplicate declaration`. Fix: try `[^>]*?/>` FIRST, then the
   children form. This one pattern was copied into eight tools.
2. **`<detail ` with a trailing space** misses `<detail>`. And matching `<detail>` without
   requiring `<band>` immediately after it will match a **comment** that mentions `<detail>`
   and run to the real `</detail>`, sweeping in another band's elements. Use
   `<detail>\s*<band height="(\d+)"`.
3. **Stripping an attribute across a whole style block** also strips it from the nested
   `<style>` inside a `<conditionalStyle>`. Split at the first `>` and strip only the opening
   tag.

### AH5 — Crystal indents with LEADING SPACES inside the text

R10.026/R10.034's sub-rows read `|..........- Quantity not delivered ...|`. The span's bbox
starts where the spaces start, so measuring `bbox.x0` says the caption sits 2pt LEFT of its
parent row while the picture plainly shows it 20pt right. Both observations were correct about
different things. Every comparison in a conversion toolkit squashes whitespace before matching -
deliberately, so a hyphen-broken caption is not counted as missing - which makes this class of
difference **structurally invisible**. Copy the original's exact string, whitespace included;
no geometry change is needed.

### AH6 — measure absolutely, not by residual, once the geometry is close

A residual-shifting refiner cannot fix a row-ORDER error, because preserving order is what makes
it safe. R10.029 had its navy `AACQ Calculation` band and its teal `MMBtu` row the wrong way
round; asked to reorder, the residuals put two rows on top of each other. Computing each row's y
as `original row top − page y of the band's start` fixed it and gained 9 points on that report,
and 7 on R10.034. It also exposed the next layer: the **title band's height** decides where the
`columnHeader` starts, so the whole merged header block lands wherever that height puts it -
setting it from the original's own header-block top gained another 2-3 points on five reports.
Afterwards the residual refiners actively made things WORSE (83% → 76%) by nudging rows off the
absolute positions. **Residuals to get close, absolute placement to finish, and then stop.**
