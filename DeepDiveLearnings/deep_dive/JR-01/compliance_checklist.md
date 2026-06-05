# JasperReports v7.0.3 Compliance Checklist

Use this checklist before delivering any JRXML file. Every item must be ✅ before the file is committed.

---

## Namespace & Schema

- [ ] Root `<jasperReport>` has `xmlns="http://jasperreports.sourceforge.net/jasperreports"`
- [ ] Root has `xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"`
- [ ] Root has correct `xsi:schemaLocation` pointing to jasperreport.xsd
- [ ] `name` attribute matches the filename (without `.jrxml`)
- [ ] `pageWidth`, `pageHeight`, `columnWidth`, `leftMargin`, `rightMargin`, `topMargin`, `bottomMargin` all declared

---

## Expressions & CDATA

- [ ] ALL expression values wrapped in `<![CDATA[...]]>`
- [ ] No raw expression text outside CDATA (XML validation will fail)
- [ ] No deprecated attribute `isBlankWhenNull="true"` — replaced with null-check in expression
- [ ] All expressions return the correct Java type (e.g. `String` field → String expression)

---

## Fonts & PDF

- [ ] All `<font>` declarations use `pdfFontName` attribute
- [ ] `pdfFontName` uses standard values: `Helvetica`, `Helvetica-Bold`, `Helvetica-Oblique`, `Helvetica-BoldOblique`
- [ ] `isPdfEmbedded="false"` when using standard Helvetica/Times/Courier
- [ ] `pdfEncoding="Cp1252"` set for Western European content
- [ ] No font references to non-standard fonts without a registered font extension JAR

---

## Band Structure

- [ ] All 9 standard bands declared (title, pageHeader, columnHeader, detail, columnFooter, pageFooter, lastPageFooter, summary, noData) — empty bands use `<band height="0"/>`
- [ ] `noData` band has meaningful "no results" message
- [ ] No element extends beyond its band height (y + height ≤ band height)
- [ ] No element extends beyond column width (x + width ≤ columnWidth)
- [ ] No overlapping elements (unless intentional layering)

---

## Null Safety

- [ ] Every `<textFieldExpression>` using `$F{}` has null check: `$F{field} != null ? ... : "default"`
- [ ] Every numeric field has a default of `0` or `0.0`
- [ ] Every Date field has null-safe `SimpleDateFormat` call
- [ ] No raw `$F{field}` without null guard in numeric/date contexts

---

## Parameters

- [ ] Every `<parameter>` has a `<defaultValueExpression>` or is clearly documented as required
- [ ] No hardcoded credentials, URLs, or environment-specific values in parameters
- [ ] `$P!{}` (raw injection) used only for ORDER BY clauses — NEVER in WHERE conditions with user input
- [ ] `REPORT_CONNECTION` parameter declared with `isForPrompting="false"` if using JDBC connection

---

## Variables

- [ ] All `<variable>` declarations have correct `calculation` type
- [ ] All variables have `<initialValueExpression>` where calculation is `Sum`, `Count`, etc.
- [ ] `resetType` appropriate for grouping level
- [ ] Variable classes match expected Java types

---

## Deprecated Attribute Check

- [ ] No `isBlankWhenNull` attribute on textField elements
- [ ] No `fontName`, `isBold`, `isItalic`, `fontSize`, `forecolor` directly on `<reportElement>`
- [ ] No `hAlign`, `vAlign` on `<reportElement>` — use `<textElement>` with `textAlignment`
- [ ] No `scriptletClass` attribute — use Java processor classes instead
- [ ] `whenNoDataType` uses `"NoData"` not `"NoDataSection"` (renamed in v7)
- [ ] No `mode="Transparent"` if not supported in v7 (verify in Jasper Studio)

---

## Self-Review Steps

1. Open in Jasper Studio 7.0.3 — confirm no validation errors shown in Problems panel
2. Validate against schema: Right-click → Validate
3. Run Preview with sample data — confirm all bands render
4. Export to PDF — confirm no blank text or font errors
5. Export to Excel — confirm cells are correctly typed (numbers as numbers, not strings)
