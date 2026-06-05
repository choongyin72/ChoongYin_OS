# SUMMARY — JR-02: Data Sources & Expressions

**Date completed:** 2026-06-05
**Task ID:** JR-02

---

## Topics Covered

- [x] JDBC data source — Oracle setup, query execution, field mapping
- [x] `$P{}` safe parameterised binding vs `$P!{}` raw injection
- [x] `$X{IN, column, param}` multi-value IN clause
- [x] JREmptyDataSource — when to use, pattern
- [x] JRBeanCollectionDataSource — bean getter mapping
- [x] JRCsvDataSource — column name mapping, fieldDescription
- [x] JRJsonDataSource — JSON path expressions
- [x] JRXmlDataSource — XPath expressions
- [x] `whenNoDataType` options — NoData recommended for EC
- [x] Java expression syntax inside CDATA
- [x] All expression locations (textFieldExpression, printWhenExpression, etc.)
- [x] 17 practical expression examples
- [x] Null-safety reference table (String, Number, Date, Division)
- [x] All 11 variable calculation types
- [x] resetType and incrementType options
- [x] Group declaration with groupHeader/groupFooter
- [x] Group subtotal variables with resetGroup
- [x] Data must be SQL-sorted for groups

---

## Key Takeaways

1. **`$X{IN, column, param}` is critical for EC multi-stream reports** — when filtering by a list of stream/well codes, use this syntax with `java.util.Collection`. Attempting to build an IN clause manually leads to SQL injection risk or runtime errors.

2. **CSV fields are always String** — JRCsvDataSource maps all values as String. Numeric parsing must happen in the expression: `Double.parseDouble($F{value}.trim())`. Always guard against empty strings.

3. **Groups MUST be SQL-sorted** — JasperReports detects group breaks by comparing consecutive `groupExpression` values. If the data is not sorted by the group column, the group will appear to start and stop randomly.

4. **`System` calculation type gives full manual control** — when `Sum`, `Count`, etc. don't fit, use `System` with `calculation="System"` and write the entire logic in `variableExpression`. Evaluated every row.

5. **`$P!{}` is SQL injection — use only for ORDER BY** — raw parameter injection bypasses JDBC prepared statement protection. Only safe when the value is developer-controlled (e.g. a column name from a fixed list), NEVER with user input.

---

## Gotchas

1. Oracle `DATE` type maps to `java.util.Date` in JDBC — not `java.sql.Date`. Use `java.text.SimpleDateFormat` for formatting.
2. Oracle `NUMBER` with no scale maps to `java.math.BigDecimal` by default in some JDBC drivers — declare field as `java.lang.Double` and JDBC will auto-convert, but add null check.
3. Group expression value change is evaluated after the row is processed — groupFooter shows the PREVIOUS group's totals, not the current row's. This is correct and expected.
4. `$X{IN, ...}` syntax requires the parameter class to be `java.util.Collection` — using `java.util.List` or array will fail.

---

## Files Produced

| File | Description |
|---|---|
| `data_sources_guide.md` | All 6 data source types with config, EC use cases, common errors |
| `expressions_guide.md` | 17 practical expressions, null-safety table, variable types, group declaration |
| `working_report_sql.jrxml` | v7.0.3 SQL report — 2 params, 5 fields, 3 variables, groups, conditional print |
| `working_report_csv.jrxml` | v7.0.3 CSV report — column mapping, string-to-numeric parsing |
| `SUMMARY_JR-02.md` | This file |

---

## Confidence Rating: 4/5

Strong command of all data source types and expression patterns. Working JRXML files cover the full range of real-world patterns. Runtime validation needed to confirm Oracle JDBC type mapping and group sorting behaviour on live EC data.
