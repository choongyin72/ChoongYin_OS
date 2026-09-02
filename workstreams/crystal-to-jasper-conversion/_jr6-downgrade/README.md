# JasperReports 7 → 6.x downgrade

Converts this project's JasperReports **7.0.3 compact** JRXML into **6.x classic** JRXML, so a
report can be compiled for and deployed to EC's **legacy** report engine.

**Status: 8 reports converted, 2026-09-02. 7 of 8 render-identical to their 7.0.3 originals;
the 8th is untestable locally for a data reason, not a conversion one.**

| Report | Elements | 6.17.0 compile | Render vs 7.0.3 |
|---|---|---|---|
| R07.001 | 2,694 | ✓ | **IDENTICAL** — 7 pages, 1,263 spans, 1,448 rects |
| R07.002 | 767 | ✓ | **IDENTICAL** — 2 pages, 625 spans, 2,352 rects |
| R07.003 | 571 | ✓ | **IDENTICAL** — 5 pages, 568 spans, 1,573 rects |
| R07.004 | 380 | ✓ | **IDENTICAL** — 2 pages, 301 spans, 646 rects |
| R07.005 | 691 | ✓ | **IDENTICAL** — 2 pages, 637 spans, 2,397 rects |
| R07.006 | 520 | ✓ | **IDENTICAL** — 1 page, 250 spans, 294 rects |
| R07.012 | 78 | ✓ | **IDENTICAL** — 1 page, 385 spans, 1,438 rects |
| R07.014 | 109 | ✓ | **IDENTICAL** — 1 page, 462 spans, 1,658 rects (two-level spanning headers) |
| R07.011 | 181 | ✓ | **not testable here** — `TV_FC_PRODUCTION_REPORT` does not exist in this database (`ORA-00942`, confirmed absent from `all_objects`) |

5,991 elements in total across 9 reports. R07.014 needed no converter changes at all — the
first report to pass on the first attempt after the batch hardening, which is the signal the
mapping is now complete for this corpus rather than being patched per report. "IDENTICAL" means every text span (page, x, y, size, font, string) and
every drawing rect matches exactly, plus the same embedded font families.

**R07.012 is additionally verified through EC itself**: the 6.17.0 `.jasper` deployed to the
ZREP extension, ran on the legacy `ECJasperReportJob` engine (`Report number 22 is generated
successfully`), and its EC-rendered PDF is identical to the EC-rendered 7.x PDF — 385 spans and
1,438 rects, compared with `verify_jr6.py --pdf`.

---

## Why a downgrade is even possible

JasperReports 7 replaced the Commons Digester parser with Jackson XML and introduced the compact
`<element kind="...">` form, so 6.x cannot read a 7.x JRXML at all. But an XML inventory
(`inventory.py`) shows these reports use only:

```
element kinds : staticText, rectangle, line, textField, image
tags          : band, box, pen/topPen/bottomPen/leftPen/rightPen, style, conditionalStyle,
                parameter, defaultValueExpression, query, field, variable, text, expression,
                title, pageHeader, columnHeader, detail, summary, pageFooter
```

**Every one of those exists in 6.x.** No JR7-only feature is used. So this is a *syntax*
transformation with a 1:1 mapping, not a feature downgrade — which is why nothing is lost.
Jaspersoft Studio's "you risk to lose part of the report content" warning applies to reports
using JR7 features; these don't.

---

## Usage

### Local — convert and prove equivalence

```bash
# 0. one-off: fetch JasperReports 6.17.0 + deps into jr6170-lib/
mvn -q dependency:copy-dependencies -DoutputDirectory=jr6170-lib

# 1. convert 7.x -> 6.x  (writes into <report>/output/jr6/)
py jr7_to_jr6.py \
   "C:/Projects/INPEX/sources/CrystalReports/R07.012/output/R07_012_FC_Lifting_Report.jrxml" \
   "C:/Projects/INPEX/sources/CrystalReports/R07.012/output/jr6/R07_012_FC_Lifting_Report_jr6.jrxml"

# 2. gate: does real 6.17.0 accept it?
sh jr6build.sh R07.012 compile

# 3. render it from the local Oracle
sh jr6build.sh R07.012 fill

# 4. prove it matches the 7.x render (fonts + every span + every rect, then LOOK)
py verify_jr6.py R07.012          # exit 0 = identical

# 5. produce the deployable artifact
sh jr6build.sh R07.012 jasper
```

Step 2 is the real validity gate — the 6.17.0 compiler validates against the 6.x XSD, so any
leftover JR7 construct surfaces as a concrete `SAXParseException` naming the attribute. Step 4 is
the *fidelity* gate, and it is separate on purpose: a report can compile and fill perfectly while
rendering with every border missing (see the `<box>` trap below).

### On EC — deploy and generate

```bash
# 1. copy the artifact + logo into the ZREP extension's reports/ folder
#    (alongside the existing .jasper), then redeploy the extension
```
Then on the report definition:

| Setting | Value for a **6.x** artifact |
|---|---|
| `REPORT_ITEM.JOB_INSTANCE_CLASS` | `com.ec.frmw.report.screens.model.ejb.ECJasperReportJob` (legacy) |
| `Jasper Definition Url` (`report_item_param`, `REPORT_SYSTEM_PARAM`) | `/extension/ZREP/reports/<name>_jr6.jasper` |
| `P_BASE_URL` default in the JRXML | `/extension/ZREP/reports/` |

Then **GENERATE** from the Report Administration screen and check the log:

- `RESOURCE:` should show the **full extension path**, not a bare `logo.png`
- no `Error loading object from InputStream` — that means engine/artifact version mismatch
- status `GENERATED`, and the archived PDF opens

A 6.x `.jasper` on the **V7** engine fails, and a 7.x `.jasper` on the **legacy** engine fails —
see the matrix below. Getting that pairing wrong produces exactly the same error message in
both directions, so always confirm which engine the definition names.

---

## Compatibility matrix — measured, not assumed

| `.jasper` compiled with | EC legacy 6.21.4 | EC V7 7.0.1 |
|---|---|---|
| 7.0.3 | ✗ `Error loading object from InputStream` | ✓ loads |
| 6.17.0 | ✓ loads | ✗ `Error loading object from InputStream` |

**Incompatibility is bidirectional.** One `.jasper` cannot serve both engines; the artifact must
be paired with the engine named in `REPORT_ITEM.JOB_INSTANCE_CLASS`:

```
com.ec.frmw.report.screens.model.ejb.ECJasperReportJob          -> legacy, needs a 6.x .jasper
com.ec.frmw.report.screens.model.ejb.jasper7.ECJasperReportJob  -> V7,     needs a 7.x .jasper
```

---

## The three transformations that matter

1. **Band wrapping.** JR7 puts elements directly in `<title height=..>`; 6.x needs
   `<title><band height=..>…</band></title>`. `<detail>` already carries its own `<band>`.
2. **XSD child order.** 6.x validates order strictly and it is *not* the order JR7 files use —
   `<summary>` must come **after** `<pageFooter>`. Emitting source order fails validation.
3. **Boolean `is` prefix.** JR7 dropped it:
   `bold`/`italic`/`forPrompting`/`blankWhenNull`/`removeLineWhenBlank`/`titleNewPage` →
   `isBold`/`isItalic`/`isForPrompting`/`isBlankWhenNull`/`isRemoveLineWhenBlank`/`isTitleNewPage`.

Plus the tag renames: `<query>`→`<queryString>`, variable `<expression>`→`<variableExpression>`,
textField `<expression>`→`<textFieldExpression>`, image `<expression>`→`<imageExpression>`;
`pattern`/`isBlankWhenNull`/`evaluationTime` move onto the `<textField>` tag; `<pen>` moves
inside `<graphicElement>` for rectangle/line; positional attributes move onto `<reportElement>`;
and `conditionalStyle` expands from attributes to the nested `<conditionExpression>` + `<style>`
form.

---

## Two traps that cost a round here

### The `<box>` on a `<style>` carries the whole grid
First version of `emit_style` only walked `conditionalStyle` children and silently dropped 11 of
the 14 `<box>` elements — the ones attached to styles. Result: **165 drawings instead of 1,438**,
i.e. every cell border gone, while the report still compiled and filled without complaint.
6.x XSD order inside `<style>` is `<box>` before `<conditionalStyle>`.

### The Arial font EXTENSION must be on the classpath
Without `inpex-arial-fonts.jar`, 6.x resolves `fontName="Arial"` to nothing, iText falls back to
**Helvetica**, and `isBold`/`isItalic` are **silently ignored** — the whole report renders upright
and non-bold while the XML is perfectly correct:

```
without extension:  Helvetica x382
with extension:     ArialMT x351, Arial-BoldItalicMT x20, Arial-BoldMT x10, Arial-ItalicMT x4
                    (identical to the 7.0.3 render)
```

Diagnose with `fonts_used.py` — the embedded font family names tell you immediately, whereas
the JRXML looks fine either way.

---

## Scope note

R07.012 is 78 elements. **R07.001 is 2,694.** For R07.001 the cheaper route is to add a 6.x
output dialect to its generator (`R07.001/build/gen_001.py`) rather than convert after the fact,
since that JRXML is produced programmatically.

Also unverified by design: this proves equivalence to the **7.0.3 render**, which was itself
verified against the Crystal reference. It does not re-verify against Crystal — if the 7.x
version has a layout defect, the 6.x version faithfully reproduces it.
