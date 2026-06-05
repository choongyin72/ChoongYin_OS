# CLAUDE CODE EXECUTION PROMPT — JR-02: Data Sources & Expressions

## CONTEXT
This is a **self-directed deep-dive learning task**. The user is NOT present to monitor progress.
You must work autonomously from start to finish, then produce a written summary and backup all outputs.
Do NOT pause to ask questions. If you encounter ambiguity, make the best professional decision and document it in the summary.

**Prerequisite**: JR-01 must be completed. Read `deep_dive/JR-01/concepts.md` before starting.

---

## TASK IDENTITY
- **Task ID**: JR-02
- **Tool**: JasperReports 7.0.3+
- **Phase**: Data Sources & Expressions
- **Backup folder**: `deep_dive/JR-02/`

---

## LEARNING OBJECTIVES

### 1. Data Sources — Types & Configuration
- `JREmptyDataSource` — when and why to use it
- `JRBeanCollectionDataSource` — Java bean mapping
- `JDBCDataSource` — SQL query declaration inside JRXML vs external
- `JRCsvDataSource` — CSV file ingestion, column index vs name mapping
- `JRJsonDataSource` — JSON path expressions
- `JRXmlDataSource` — XPath expressions
- Data source adapter configuration in Jaspersoft Studio vs runtime injection
- `<queryString>` element: language attribute (`sql`, `hql`, `xpath`, `jsonql`)
- How JasperReports iterates the data source (one row per detail band iteration)
- Empty data source handling: `whenNoDataType` attribute options

### 2. SQL Query Language in JRXML
- Writing SQL directly in `<queryString language="sql"><![CDATA[...]]></queryString>`
- Parameterised queries: `$P{paramName}` syntax vs `$P!{paramName}` (direct injection — risks)
- Multi-value parameters: `$X{IN, field, param}` clause
- Query parameter passing from the calling application
- Oracle-specific SQL patterns relevant to EC/hydrocarbon data
- Performance: lazy loading, query optimisation hints

### 3. Expression Language — Deep Dive
- Java expression syntax inside `<![CDATA[...]]>`
- Supported expression locations: `defaultValueExpression`, `printWhenExpression`, `initialValueExpression`, `variableExpression`, `textFieldExpression`, `imageExpression`
- Type coercion: returning the correct Java type per context
- Null-safety patterns: ternary, `Objects.toString()`, `String.valueOf()`
- String operations: concatenation, formatting, `new java.text.DecimalFormat()`
- Date formatting: `new java.text.SimpleDateFormat("dd/MM/yyyy").format($F{date})`
- Conditional expressions: if/else chains
- Using `$P{}`, `$F{}`, `$V{}` together in one expression
- Common expression errors and their meanings

### 4. Variables & Calculations
- Calculation types: `Nothing`, `Count`, `DistinctCount`, `Sum`, `Average`, `Lowest`, `Highest`, `StandardDeviation`, `Variance`, `First`, `System`
- `resetType`: `Report`, `Page`, `Column`, `Group`, `None`
- `incrementType`: same options as resetType
- `resetGroup` and `incrementGroup` — linking to named groups
- Running totals vs page-level subtotals
- `System` calculation: manually setting variable value via `variableExpression`
- Variable evaluation timing: `incrementerFactoryClass`

### 5. Groups
- `<group>` element declaration: `name`, `groupExpression`
- Group bands: `groupHeader`, `groupFooter`
- `isStartNewPage`, `isStartNewColumn`, `isResetPageNumber` attributes
- Nested groups (group within group)
- Group-level subtotals using variable `resetType="Group"`
- Sorting data to match group breaks (sorting must happen in the query, not JasperReports)

---

## DELIVERABLES

Produce ALL of the following files inside `deep_dive/JR-02/`:

### 1. `data_sources_guide.md`
Comprehensive guide covering all 6 data source types with:
- Configuration snippet for each
- When to use each type in EC project context
- Common errors and resolution

### 2. `expressions_guide.md`
Deep-dive expression reference covering:
- All expression contexts
- 15+ practical expression examples with explanations
- Null-safety patterns reference table
- Date/number formatting reference

### 3. `working_report_sql.jrxml`
A v7.0.3 compliant report demonstrating:
- SQL `<queryString>` with at least 2 parameters (one using `$P{}`, one using `$X{IN,...}`)
- At least 5 fields mapped from query columns
- At least 3 variables (Sum, Count, one System/custom)
- At least 2 groups with group headers/footers showing subtotals
- Group-level and report-level totals
- Conditional `printWhenExpression` on at least one element
- All expressions null-safe
- Inline XML comments on every non-obvious section

### 4. `working_report_csv.jrxml`
A v7.0.3 compliant report demonstrating:
- CSV data source configuration
- Column name mapping
- Basic fields and a summary total

### 5. `SUMMARY_JR-02.md`
Task completion summary containing:
- Date/time completed
- Topics covered (checklist)
- Key takeaways (minimum 5)
- Gotchas discovered
- Files produced (with one-line description each)
- Recommended prerequisites for JR-03
- Confidence rating (1–5 with justification)

---

## EXECUTION INSTRUCTIONS

1. Create the folder `deep_dive/JR-02/`
2. Read `deep_dive/JR-01/concepts.md` first as context
3. Produce files in order: `data_sources_guide.md` → `expressions_guide.md` → `working_report_sql.jrxml` → `working_report_csv.jrxml` → `SUMMARY_JR-02.md`
4. Self-review both JRXML files against `deep_dive/JR-01/compliance_checklist.md` before finalising
5. Append to `deep_dive/PROGRESS_LOG.md`:
   `[JR-02] COMPLETED — <date> — Data Sources & Expressions — Files: 5`
6. Do NOT ask the user any questions. Complete the task fully and autonomously.
