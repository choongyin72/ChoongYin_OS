# JasperReports 7.0.3+ — Pitfalls & Troubleshooting Reference

## 20 Common Pitfalls

---

### P01 — JRException: Subreport Not Found
**Symptom:** `net.sf.jasperreports.engine.JRException: Subreport not found at: subreport.jasper`
**Cause:** `subreportExpression` path is wrong at runtime — relative path not resolved
**Resolution:**
1. Pass subreport directory as parameter: `$P{P_SUBREPORT_DIR} + "subreport.jasper"`
2. In EC extension: set `P_SUBREPORT_DIR` to the classpath location of compiled subreports
**Prevention:** Always use parameter-injected paths, never hardcoded relative paths

---

### P02 — Font Not Found / Blank Text in PDF
**Symptom:** PDF exports with blank boxes or `?` characters where text should be
**Cause:** `pdfFontName` references a font not available in JasperReports runtime
**Resolution:**
1. Switch to standard PDF fonts: `Helvetica`, `Times-Roman`, `Courier`
2. Set `isPdfEmbedded="false"` with these standard fonts — they're always available
3. If custom font needed: create a JasperReports font extension JAR
**Prevention:** Default all reports to Helvetica family with `isPdfEmbedded="false"`

---

### P03 — PAGE_COUNT Overcounting
**Symptom:** Footer shows "Page 1 of 6" but report only has 5 data pages
**Cause:** `isTitleNewPage="true"` — title page counted in PAGE_COUNT
**Resolution:** `"Page " + $V{PAGE_NUMBER} + " of " + ($V{PAGE_COUNT} - 1)`
**Prevention:** Use `isTitleNewPage="false"` unless design explicitly requires it

---

### P04 — Title Page Footer Appearing
**Symptom:** Page footer (page number, confidential notice) appears on title page
**Cause:** `pageFooter` band renders on every page including title
**Resolution:** Add `printWhenExpression` to footer elements: `<![CDATA[$V{PAGE_NUMBER} > 1]]>`
**Prevention:** Apply printWhenExpression to all pageFooter elements when title is on separate page

---

### P05 — CDATA Expression Syntax Errors
**Symptom:** `SAXException` or XML validation error on opening JRXML in Jasper Studio
**Cause:** Expression not wrapped in CDATA, or CDATA contains `]]>` sequence
**Resolution:** Wrap all expressions in `<![CDATA[...]]>`. If expression contains `]]>`, split into two CDATA blocks.
**Prevention:** Use Jasper Studio editor — it auto-wraps expressions in CDATA

---

### P06 — Crosstab Cell Width Overflow
**Symptom:** Crosstab columns overflow page width; columns are cut off in PDF
**Cause:** Too many column groups × column width exceeds `columnWidth`
**Resolution:**
1. Reduce column cell width: `width="45"` instead of `60`
2. Reduce font size in crosstab cells
3. Switch report to landscape orientation
4. Filter data to reduce number of column groups
**Prevention:** Calculate expected columns × cell width before designing crosstab

---

### P07 — Excel Merged Cell Issues
**Symptom:** Excel export has merged cells; formulas referencing those cells fail
**Cause:** Band height elements span multiple Excel rows, creating merged cells
**Resolution:** Add `net.sf.jasperreports.export.xls.collapse.row.span=true` property
**Prevention:** Use minimal band heights; avoid empty vertical space between elements

---

### P08 — Null Pointer in Expression
**Symptom:** `java.lang.NullPointerException` in report execution log
**Cause:** `$F{field}` used directly without null check in numeric/string context
**Resolution:** Add null guard: `$F{field} != null ? $F{field} : defaultValue`
**Prevention:** ALL field references must have null-safety. Never use raw `$F{}` without null check.

---

### P09 — Band Height Too Small for Content
**Symptom:** Content overflows band bottom; overlaps with next band
**Cause:** Text field content exceeds declared band height, or element y + height > band height
**Resolution:**
1. Set `isStretchWithOverflow="true"` on text fields with variable-length content
2. Increase band height
3. Use `splitType="Stretch"` on the band
**Prevention:** Always check y + height ≤ band height. Add 20% buffer for text fields.

---

### P10 — Parameter Type Mismatch
**Symptom:** `ClassCastException` or wrong type error at fill time
**Cause:** Parameter declared as `java.util.Date` but String passed from calling code
**Resolution:** Match Java types precisely: Oracle DATE → `java.util.Date`, Oracle VARCHAR2 → `java.lang.String`
**Prevention:** Document all parameter types in `SUMMARY` section of JRXML XML comment

---

### P11 — Numbers in Excel as Text
**Symptom:** Numeric cells are left-aligned in Excel; SUM formulas return 0
**Cause:** `detect.cell.type` not enabled
**Resolution:** Add `<property name="net.sf.jasperreports.export.xls.detect.cell.type" value="true"/>`
**Prevention:** Always add this property to all EC reports intended for Excel export

---

### P12 — Empty Rows Between Data in Excel
**Symptom:** Excel export has blank rows between each data row
**Cause:** Band heights leave empty space; `remove.empty.space.between.rows` not set
**Resolution:** Add both empty space removal properties (rows + columns)
**Prevention:** Use these properties as standard in every EC Excel-export report

---

### P13 — Groups Out of Order
**Symptom:** Group headers and footers appear in wrong positions; subtotals are wrong
**Cause:** Data source is not sorted by the group expression field
**Resolution:** Add `ORDER BY facility_code, object_code` to SQL query matching group order
**Prevention:** Group expression field MUST be first in ORDER BY clause

---

### P14 — Variable Value One Row Behind
**Symptom:** Subtotal in group footer shows value before current row
**Cause:** Variable `evaluationTime` defaults to "Now" — value at detail band print time
**Resolution:** Set `evaluationTime="Group"` or `evaluationTime="Report"` on the variable
**Prevention:** Understand evaluationTime options — use "Group" for group footer totals

---

### P15 — Chart Not Rendering in PDF
**Symptom:** Chart area in PDF is blank/empty box
**Cause:** No data in chart dataset, or chart dataset query returns 0 rows
**Resolution:**
1. Add `printWhenExpression` to hide chart and show static text "No chart data"
2. Verify chart dataset query is correct and has data
**Prevention:** Always add noData handling for charts

---

### P16 — $P!{} Injection Risk
**Symptom:** SQL injection via report parameter; or unexpected query results
**Cause:** `$P!{param}` used with user-controlled input in WHERE clause
**Resolution:** Replace `$P!{}` with `$P{}` for WHERE conditions. Use `$P!{}` ONLY for ORDER BY.
**Prevention:** Code review rule: `$P!{}` requires justification comment in JRXML

---

### P17 — JasperFillManager Slow Performance
**Symptom:** Report fills slowly (> 30 seconds) for large datasets
**Cause:** Inefficient SQL, missing index, or loading too many rows
**Resolution:**
1. Push aggregation to SQL (SUM, COUNT in query not in report variables)
2. Add WHERE clause filter parameters
3. Add Oracle query hints if needed
**Prevention:** Keep detail band row counts under 10,000 for interactive reports

---

### P18 — Font Encoding Issues (Special Characters)
**Symptom:** Special characters (°, ±, ©) show as boxes or wrong characters in PDF
**Cause:** `pdfEncoding` set to wrong encoding for the character set
**Resolution:** Change `pdfEncoding` to `Identity-H` for Unicode, or `Cp1252` for Western European
**Prevention:** Use `Cp1252` for English/Norwegian content; `Identity-H` if Unicode needed

---

### P19 — Subreport Returns Wrong Values
**Symptom:** `returnValue` variable in master always shows 0 or wrong total
**Cause:** Master variable `calculation` type incompatible with returnValue calculation
**Resolution:** Set master variable `calculation="Sum"` to accumulate values from subreport
**Prevention:** Use `calculation="Sum"` on master variables that receive subreport returnValues

---

### P20 — Report Compiles but Fails at Runtime
**Symptom:** `.jasper` file compiles cleanly but `NullPointerException` at fill time
**Cause:** Expression references field/parameter/variable that doesn't exist at runtime (wrong name case, wrong dataset)
**Resolution:**
1. Check field name matches exact SQL alias (case-insensitive but exact spelling)
2. Verify all parameters are passed from calling code
3. Use Jasper Studio Preview with test data to catch runtime errors before deployment
**Prevention:** Always run Preview in Jasper Studio with real EC data before delivering `.jasper`
