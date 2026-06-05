# JasperReports — Claude Code Prompt Patterns

## Pattern 1: Generate New JRXML from Column List

**Trigger:** You have a SQL query and want a complete JRXML report
**Template:**
```
Generate a v7.0.3 compliant JRXML report with these specs:
- Report name: {ReportName}
- Data source: Oracle JDBC — localhost:1521/ORCL (ECKERNEL_EC/energy)
- SQL: {paste your SQL here}
- Fields: {column1 (type), column2 (type), ...}
- Parameters: {P_PARAM1 (type), ...}
- Output: PDF A4 landscape + Excel
- Groups: {group by FIELD_X}
- Totals: {Sum of FIELD_Y per group and grand total}
Apply all EC best practices: null-safety, noData band, Helvetica fonts, Excel properties.
```
**Expected output:** Complete `.jrxml` file with all bands, fields, variables, styles
**Validation:** Open in Jasper Studio → no validation errors → Preview with local DB

---

## Pattern 2: Fix v7.0.3 Compliance Violations

**Trigger:** Existing JRXML has errors or was designed in v6.x
**Template:**
```
Fix all v7.0.3 compliance violations in this JRXML:
{paste JRXML content}

Check for and fix:
1. Missing CDATA wrappers on expressions
2. Deprecated isBlankWhenNull attribute → null-check expression
3. Deprecated font attributes on reportElement → move to <font> in <textElement>
4. Namespace declaration correct for v7.0.3
5. whenNoDataType="NoDataSection" → "NoData"
Return the corrected JRXML file.
```
**Validation:** Jasper Studio shows no errors in Problems panel

---

## Pattern 3: Add Group with Subtotals

**Trigger:** Existing flat report needs grouping by a field
**Template:**
```
Add a group to this JRXML that groups by {FIELD_NAME}:
{paste JRXML content}

Requirements:
- groupExpression = $F{{FIELD_NAME}}
- groupHeader: show {FIELD_NAME} value in bold, dark background
- groupFooter: show subtotal of {NUMERIC_FIELD} right-aligned, bold
- Add variable {GROUP_SUBTOTAL} with calculation=Sum, resetType=Group
- SQL must be sorted by {FIELD_NAME} — add to ORDER BY if not present
Return updated JRXML.
```
**Validation:** Group headers/footers appear at correct positions; subtotals match SQL GROUP BY result

---

## Pattern 4: Add Conditional Style

**Trigger:** Need zebra striping, negative value highlighting, or status-based colours
**Template:**
```
Add these conditional styles to this JRXML:
{paste JRXML}

Style 1 — Zebra stripe on detail band: alternate rows with backcolor #F5F5F5
Style 2 — Red text when {FIELD_NAME} < 0 (highlight negative values)
Style 3 — Bold green when {STATUS_FIELD} = 'A' (Approved)

Apply styles to the detail band elements. Use conditionalStyle blocks inside <style> definitions.
```

---

## Pattern 5: Add Subreport

**Trigger:** Master report needs per-group detail from a different query
**Template:**
```
Add a subreport to this master JRXML:
{paste master JRXML}

Subreport specs:
- Subreport name: {SubreportName}
- Called from: detail band of master, passing $F{{MASTER_KEY_FIELD}} as P_PARENT_ID
- Subreport query: {paste SQL}
- Subreport fields: {list fields}
- Return value: {SUBRPT_VARIABLE_NAME} → master variable {MASTER_VAR_NAME} calculation=Sum

Create both master_updated.jrxml and {SubreportName}.jrxml.
Both must be v7.0.3 compliant.
```

---

## Pattern 6: Generate Crosstab from Pivot Spec

**Trigger:** Need a pivot/matrix report
**Template:**
```
Generate a crosstab JRXML with:
- Rows: {row_field} from {table/view}
- Columns: {column_field} (e.g. month, year, category)
- Measure: Sum of {measure_field}
- SQL filter: WHERE {condition}
- Row grand totals: Yes
- Column grand totals: Yes
- Row alternating background: #F0F0F0 on even rows
- v7.0.3 compliant
- Use subDataset for crosstab data
```

---

## Pattern 7: Debug Expression Error

**Trigger:** Report fails with JRException or NullPointerException at fill time
**Template:**
```
Debug this JasperReports expression error:

Error: {paste full stack trace}
Expression causing error: {paste the expression}
Field/variable types: {P_PARAM1=Date, F_FIELD1=Double, ...}

Find the root cause and provide the corrected expression.
```

---

## Pattern 8: Generate REST API Call

**Trigger:** Need to run a Jasper Server report programmatically
**Template:**
```
Generate a curl command and Python requests snippet to:
- Run report: {/reports/path/ReportName}
- Output format: {pdf | xlsx}
- Parameters: {P_DAYTIME=2025-01-01, P_FACILITY=ALL}
- Server: {jasper-server-url}
- Auth: {username/password}

Include both synchronous and async execution patterns.
```
