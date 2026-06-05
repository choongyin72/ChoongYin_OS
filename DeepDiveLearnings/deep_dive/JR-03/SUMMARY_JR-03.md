# SUMMARY — JR-03: Advanced Layout

**Date completed:** 2026-06-05
**Task ID:** JR-03

---

## Topics Covered

- [x] Subreport anatomy — subreportExpression, subreportParameter, returnValue
- [x] Passing parameters TO subreport
- [x] Receiving values FROM subreport via returnValue
- [x] Connection vs data source for subreports
- [x] Compilation order (subreport before master)
- [x] `JRException: Subreport not found` — root cause and resolution
- [x] P_SUBREPORT_DIR parameter pattern for runtime path
- [x] Crosstab structure — rowGroup, columnGroup, measure, crosstabCell
- [x] Row and column grand totals (rowTotalGroup, columnTotalGroup)
- [x] SubDataset for crosstab (separate query)
- [x] Crosstab conditional style for alternating rows
- [x] Bar chart anatomy (chartDataset, categorySeries, barPlot)
- [x] All chart types in v7.0.3
- [x] PDF export properties — compressed, tagged, PDFA
- [x] Excel export properties — detect.cell.type, remove.empty.space, freeze.row, collapse.row.span
- [x] Conditional styles with conditionExpression
- [x] isTitleNewPage + PAGE_COUNT resolution

---

## Key Takeaways

1. **Subreports require absolute path or parameter-injected path at runtime** — the `subreportExpression` path is evaluated at fill time, not compile time. Use `$P{P_SUBREPORT_DIR} + "filename.jasper"` to keep it configurable per environment.

2. **Crosstabs need a separate subDataset** — the crosstab gets its own query (separate from the main report query). This is powerful: the master report can show summary data while the crosstab shows the full pivot independently.

3. **`detect.cell.type=true` is mandatory for Excel reports with numbers** — without this, ALL values export as text strings, making Excel calculations impossible.

4. **`remove.empty.space.between.rows=true` is essential for clean Excel** — without it, each report page break adds blank rows in Excel, making the output unusable for data analysis.

5. **Compilation order matters for subreports** — subreport must compile first. In EC extensions, subreport `.jasper` files must be packaged in the correct build order in `pom.xml`.

---

## Gotchas

1. Crosstab `bucketExpression` must return a Comparable and Serializable type. `java.util.Date` for months works, but verify Oracle `TRUNC(date, 'MM')` returns `java.sql.Timestamp` — may need casting.
2. `returnValue` from subreport only works when the variable in the master has `calculation="Sum"` or compatible type. Using `calculation="System"` on master variable means it never updates from returnValue.
3. Crosstab cells that overflow their declared width cause layout issues — always leave 10% buffer on column group width.
4. Charts with no data render an empty frame (no error, no message) — add a `printWhenExpression` to hide the chart and show a "no data" staticText instead.

---

## Files Produced

| File | Description |
|---|---|
| `advanced_layout_guide.md` | Complete guide: subreports, crosstabs, charts, export config, conditional styles |
| `subreport_detail.jrxml` | Compilable subreport — well detail per facility, exports SUBTOTAL_OIL |
| `master_with_subreport.jrxml` | Master report — facility loop, calls subreport, receives oil total back |
| `crosstab_report.jrxml` | Crosstab — streams × months, oil sum, row/column totals, alternating rows |
| `export_config_reference.md` | PDF and Excel property reference table |
| `SUMMARY_JR-03.md` | This file |

---

## Confidence Rating: 4/5

Full command of subreport pattern, crosstab structure, and export configuration. All JRXML files are v7.0.3 compliant. Rating 4/5 because subreport path resolution and crosstab column width calculations need runtime validation in Jasper Studio against live EC data.
