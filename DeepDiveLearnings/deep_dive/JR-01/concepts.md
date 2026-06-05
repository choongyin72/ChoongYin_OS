# JR-01: JasperReports 7.0.3+ Fundamentals — Concepts

## 1. Core JRXML Structure & Architecture

### How the Engine Works — Fill → Compile → Export Pipeline

```
.jrxml (XML design) 
    ↓ JasperCompileManager.compileReport()
.jasper (compiled binary)
    ↓ JasperFillManager.fillReport(dataSource, parameters)
JasperPrint (in-memory object)
    ↓ JasperExportManager.exportToPdf() / exportToXlsx() / exportToHtml()
Output file (PDF, Excel, HTML, CSV)
```

**Why two steps?**  
- Compile once (expensive) → fill many times (cheap)
- `.jasper` files are deployment artefacts — commit to version control
- Never recompile in production unless the design changed

**EC use case:** EC's `frmw-report` module compiles `.jrxml` at deployment time. The `.jasper` is stored in the extension WAR. At report execution time, EC calls `JasperFillManager.fillReport()` with an Oracle JDBC connection and report parameters.

---

### The 9 Standard Report Bands

| Band | Render timing | Typical use |
|---|---|---|
| `title` | Once — first page start | Report title, logo, run date |
| `pageHeader` | Top of every page | Column headers, report name |
| `columnHeader` | Before first detail row on each page | Table column labels |
| `detail` | Once per data source row | The actual data |
| `columnFooter` | After last detail row on each page | Per-page subtotals |
| `pageFooter` | Bottom of every page | Page number, confidentiality notice |
| `lastPageFooter` | Bottom of LAST page only (overrides pageFooter) | Grand totals, signatures |
| `summary` | Once — after all detail rows | Grand totals, summary statistics |
| `noData` | When data source returns 0 rows | "No data found for criteria" message |
| `background` | Every page, behind all other bands | Watermarks, background images |

**Render order per page:**
```
pageHeader → columnHeader → [detail × N rows] → columnFooter → pageFooter
```

**EC use case:** Use `noData` band for every EC report — Oracle queries on large datasets can return empty results. Without `noData`, the user sees a blank page with no explanation.

---

### `reportElement` Coordinate System

```xml
<reportElement x="30" y="5" width="200" height="20"/>
```
- Origin = **top-left** corner of the band
- All values in **pixels** (72 pixels per inch by default)
- Elements are **absolutely positioned** — they do not flow around each other
- x + width must not exceed `columnWidth` (page width minus margins)
- y + height must not exceed the band's `height` attribute

**Pitfall:** Overlapping elements render on top of each other without error. Always check that y + height of element ≤ band height.

---

## 2. v7.0.3 Syntax Compliance Rules — CRITICAL

### Namespace Declaration (MANDATORY)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jasperReport
    xmlns="http://jasperreports.sourceforge.net/jasperreports"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://jasperreports.sourceforge.net/jasperreports
        http://jasperreports.sourceforge.net/xsd/jasperreport.xsd"
    name="ReportName"
    pageWidth="595" pageHeight="842"
    columnWidth="535" leftMargin="30" rightMargin="30"
    topMargin="20" bottomMargin="20">
```

### CDATA Requirement — ALL Expressions
Every expression value MUST be wrapped in CDATA:
```xml
<!-- CORRECT -->
<textFieldExpression><![CDATA[$F{OBJECT_CODE}]]></textFieldExpression>

<!-- WRONG — will fail XML validation -->
<textFieldExpression>$F{OBJECT_CODE}</textFieldExpression>
```

### Deprecated Attributes — v7.0.3 Replacements

| Deprecated (v6) | Replacement (v7.0.3) | Notes |
|---|---|---|
| `isBlankWhenNull="true"` on textField | Use expression: `$F{f} != null ? $F{f} : ""` | Attribute removed |
| `fontName="Arial"` | Use `<font fontName="Arial"/>` in `<textElement>` | Direct on reportElement removed |
| `forecolor="#000000"` | Use `<font forecolor="#000000"/>` | |
| `isBold="true"` | `<font isBold="true"/>` inside `<textElement>` | |
| `isItalic="true"` | `<font isItalic="true"/>` | |
| `fontSize="10"` | `<font size="10"/>` | |
| `hAlign="Center"` | `<paragraph>` with `lineSpacingSize` or CSS style | |
| `vAlign="Middle"` | Use box padding adjustments | |
| `scriptletClass` | Use Java processor classes instead | Scriptlets discouraged in v7 |
| `whenNoDataType="NoDataSection"` | `whenNoDataType="NoData"` | Value renamed |

### Attribute Casing Rules
All JasperReports attributes use **camelCase**:
- `pageWidth` not `page_width`
- `leftMargin` not `left_margin`
- `isBold` not `is_bold`

### Self-Closing vs Explicit Close Tags
Elements containing sub-elements require explicit close tags:
```xml
<!-- Correct -->
<band height="20">
    <textField>...</textField>
</band>

<!-- Empty band — explicit close required -->
<title>
    <band height="0"/>
</title>
```

---

## 3. pdfFontName & Font Mapping

### Why pdfFontName Exists
PDF export embeds fonts differently from screen rendering. The `pdfFontName` maps a screen font name to its PDF equivalent. Without correct mapping, PDF export shows blank text or boxes.

### Standard Helvetica Mappings
```xml
<textElement>
    <font fontName="Helvetica" pdfFontName="Helvetica"
          isPdfEmbedded="false" pdfEncoding="Cp1252"/>
</textElement>

<!-- Bold -->
<font fontName="Helvetica" pdfFontName="Helvetica-Bold" isBold="true" isPdfEmbedded="false"/>

<!-- Italic -->
<font fontName="Helvetica" pdfFontName="Helvetica-Oblique" isItalic="true" isPdfEmbedded="false"/>

<!-- Bold + Italic -->
<font fontName="Helvetica" pdfFontName="Helvetica-BoldOblique" isBold="true" isItalic="true" isPdfEmbedded="false"/>
```

### `isPdfEmbedded` and `pdfEncoding`
- `isPdfEmbedded="false"` — use standard PDF font (Helvetica is a standard PDF font, always available)
- `isPdfEmbedded="true"` — embed the full font in PDF (larger file, needed for non-standard fonts)
- `pdfEncoding="Cp1252"` — Western European encoding (standard for English/European reports)

### Pitfall: Font Not Found at Runtime
**Symptom:** PDF has blank text or ??? characters  
**Cause:** `pdfFontName` references a font not registered in JasperReports font extensions  
**Resolution:**
1. Use standard PDF fonts (Helvetica, Times-Roman, Courier) with `isPdfEmbedded="false"`
2. Or: add font JAR to classpath (create a JasperReports font extension JAR)
3. Or: use `isPdfEmbedded="true"` with a font file present on the server

**EC use case:** EC reports should default to Helvetica family with `isPdfEmbedded="false"`. This requires no font JAR and works on any server.

---

## 4. Band Height & Layout Geometry

### `splitType` Attribute
Controls what happens when a band's content exceeds the available page space:

| Value | Behaviour |
|---|---|
| `Stretch` | Band splits across pages — some elements on one page, rest on next |
| `Prevent` | Prevents splitting — band moves entirely to next page if it doesn't fit |
| `Immediate` | Splits immediately at the page boundary |

**EC recommendation:** Use `Prevent` for detail bands with multi-row content to avoid orphaned rows.

### `stretchType` on reportElement
```xml
<reportElement stretchType="ContainerHeight" .../>
```
| Value | Behaviour |
|---|---|
| `NoStretch` | Element keeps its fixed height |
| `ContainerHeight` | Element stretches to fill the band's full height |
| `ContainerBottom` | Element bottom aligns with band bottom |
| `ElementGroupHeight` | Stretches to match tallest sibling in element group |
| `ElementGroupBottom` | Bottom aligns with lowest sibling |

### `isRemoveLineWhenBlank`
```xml
<textField isBlankWhenNull="true">
    <reportElement isRemoveLineWhenBlank="true" .../>
```
When the text field is blank AND this is true, the element takes zero height — other elements below move up. Useful for optional address lines.

### `printWhenExpression`
```xml
<reportElement>
    <printWhenExpression><![CDATA[$F{STATUS}.equals("ACTIVE")]]></printWhenExpression>
</reportElement>
```
Element only prints when expression evaluates to `Boolean.TRUE`. Use for conditional rows, status-dependent sections.

### PAGE_COUNT Overcounting with isTitleNewPage
When `isTitleNewPage="true"`, the title is on page 1 and data starts on page 2. `PAGE_COUNT` counts the title page, so a 3-page report shows PAGE_COUNT=4. **Resolution:** Use a two-pass export or subtract 1 from PAGE_COUNT in the footer expression:
```xml
<![CDATA["Page " + $V{PAGE_NUMBER} + " of " + ($V{PAGE_COUNT} - 1)]]>
```

---

## 5. Parameters, Fields, Variables

### Parameters — Runtime Input
```xml
<parameter name="P_DAYTIME" class="java.util.Date">
    <defaultValueExpression><![CDATA[new java.util.Date()]]></defaultValueExpression>
</parameter>
<parameter name="P_OBJECT_ID" class="java.lang.String">
    <defaultValueExpression><![CDATA["ALL"]]></defaultValueExpression>
</parameter>
```
- Passed from calling code: `params.put("P_DAYTIME", selectedDate)`
- Available in expressions as `$P{P_DAYTIME}`
- Use `$P!{P_PARAM}` for SQL injection into query string (DANGEROUS — validate input first)

### Fields — Data Source Columns
```xml
<field name="OBJECT_CODE" class="java.lang.String"/>
<field name="NET_OIL_VOL_SM3" class="java.lang.Double"/>
<field name="DAYTIME" class="java.util.Date"/>
```
- Must match SQL column names (case-insensitive in Oracle)
- `class` must match Java type returned by JDBC
- Available as `$F{OBJECT_CODE}` in expressions

### Variables — Calculated Values
```xml
<!-- Running total -->
<variable name="TOTAL_OIL" class="java.lang.Double" calculation="Sum" resetType="Report">
    <variableExpression><![CDATA[$F{NET_OIL_VOL_SM3}]]></variableExpression>
    <initialValueExpression><![CDATA[0.0]]></initialValueExpression>
</variable>

<!-- Row count -->
<variable name="ROW_COUNT" class="java.lang.Integer" calculation="Count" resetType="Report">
    <variableExpression><![CDATA[1]]></variableExpression>
</variable>
```

### Built-in Variables
| Variable | Type | Value |
|---|---|---|
| `PAGE_NUMBER` | Integer | Current page number |
| `PAGE_COUNT` | Integer | Total pages |
| `COLUMN_NUMBER` | Integer | Current column (multi-column reports) |
| `REPORT_COUNT` | Integer | Total records processed |
| `COLUMN_COUNT` | Integer | Total records in current column |

### Null-Safety Pattern (MANDATORY)
```xml
<!-- Never let null reach the output -->
<![CDATA[$F{NET_OIL_VOL_SM3} != null ? 
    new java.text.DecimalFormat("#,##0.000").format($F{NET_OIL_VOL_SM3}) : 
    "0.000"]]>
```

**EC use case:** Oracle queries on EC views (`RV_PWEL_DAY_STATUS`, `RV_STRM_COMP_ANALYSIS`) frequently return NULL for missing PHD data. Every numeric field MUST have null-safety.
