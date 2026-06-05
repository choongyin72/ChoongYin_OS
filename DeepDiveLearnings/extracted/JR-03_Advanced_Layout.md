# CLAUDE CODE EXECUTION PROMPT — JR-03: Advanced Layout

## CONTEXT
This is a **self-directed deep-dive learning task**. The user is NOT present to monitor progress.
You must work autonomously from start to finish, then produce a written summary and backup all outputs.
Do NOT pause to ask questions. If you encounter ambiguity, make the best professional decision and document it in the summary.

**Prerequisite**: JR-01 and JR-02 must be completed. Read both summary files before starting.

---

## TASK IDENTITY
- **Task ID**: JR-03
- **Tool**: JasperReports 7.0.3+
- **Phase**: Advanced Layout
- **Backup folder**: `deep_dive/JR-03/`

---

## LEARNING OBJECTIVES

### 1. Subreports
- `<subreport>` element anatomy: `subreportExpression`, `dataSourceExpression`, `parametersMapExpression`
- Passing parameters to subreports: `<subreportParameter>` element
- Returning values from subreports: `<returnValue>` element
- Subreport connection vs data source: differences and when to use each
- Compiling subreports: dependency order (subreport must compile before master)
- Relative path vs absolute path for `subreportExpression`
- Nested subreports (subreport within subreport)
- Common subreport pitfall: `net.sf.jasperreports.engine.JRException: Subreport not found` — resolution
- Performance impact of subreports and when to prefer crosstabs instead

### 2. Crosstabs
- `<crosstab>` element structure: rowGroups, columnGroups, measures
- `<rowGroup>` and `<columnGroup>`: name, width/height, totalPosition
- `<measure>` element: name, class, calculation, `measureExpression`
- `<crosstabCell>` layout: header cells, detail cells, total cells
- `whenNoDataCell` — handling empty crosstab
- Styling crosstab cells: alternating row colours using `<conditionalStyle>`
- Crosstab grand totals: row total, column total, corner cell
- Crosstab data pre-grouping: must the data source be pre-sorted?
- Common pitfall: crosstab cell width overflow — resolution

### 3. Charts
- Chart types available in JasperReports 7.0.3: bar, line, pie, area, scatter, bubble, gantt, thermometer, meter
- `<barChart>` anatomy: `<chartDataset>`, `<categorySeries>`, `<valueExpression>`, `<labelExpression>`
- Chart customisation: title, subtitle, legend, plot orientation
- `<chartCustomizerClass>` — advanced customisation via Java class
- Chart export behaviour: vector (PDF) vs raster (HTML)
- Common pitfall: chart not rendering in PDF — resolution steps

### 4. Export Configuration — PDF & Excel
**PDF:**
- `net.sf.jasperreports.export.pdf.*` properties
- Page size, orientation, compression
- `pdfFontName` recap in export context
- Password protection: `net.sf.jasperreports.export.pdf.encrypted`
- Tagged PDF for accessibility

**Excel (XLSX):**
- `net.sf.jasperreports.export.xls.*` properties
- `isOnePagePerSheet`, `isRemoveEmptySpaceBetweenRows`, `isRemoveEmptySpaceBetweenColumns`
- `net.sf.jasperreports.export.xls.sheet.name` — per-band sheet naming
- Cell type detection: numeric cells vs string cells
- Common pitfall: merged cells breaking Excel formulas — resolution

### 5. `isTitleNewPage` & `PAGE_COUNT` Behaviour
- How `isTitleNewPage="true"` affects page numbering
- Why `PAGE_COUNT` shows inflated count when title is on its own page
- Pattern to display correct total pages: using a second pass with `isUsingCache`
- `net.sf.jasperreports.print.keep.full.content` property
- `TwoPassXlsExporter` concept
- Footer suppression on title page using `isPrintRepeatedValues="false"` + group technique

### 6. Conditional Styles
- `<style>` element: name, isDefault, `conditionalStyles`
- `<conditionalStyle>` with `<conditionExpression>`
- Style inheritance: `style` attribute on elements
- Dynamic background colour on detail rows (zebra striping)
- Highlight negative values in red

---

## DELIVERABLES

Produce ALL of the following inside `deep_dive/JR-03/`:

### 1. `advanced_layout_guide.md`
Comprehensive guide for all 6 topics with annotated snippets and EC use-case context.

### 2. `master_with_subreport.jrxml`
Master report demonstrating:
- `<subreport>` calling `subreport_detail.jrxml`
- Parameter passing to subreport
- Return value from subreport
- v7.0.3 compliant, CDATA on all expressions

### 3. `subreport_detail.jrxml`
The subreport called by the master above. Self-contained and compilable independently.

### 4. `crosstab_report.jrxml`
Report with a crosstab demonstrating:
- At least 2 row groups, 1 column group
- At least 1 measure with Sum calculation
- Row and column grand totals
- Conditional style for alternating rows
- v7.0.3 compliant

### 5. `export_config_reference.md`
Quick-reference table of the most important PDF and Excel export properties with:
- Property name
- Default value
- Recommended value for EC reports
- Notes

### 6. `SUMMARY_JR-03.md`
Task completion summary containing:
- Date/time completed
- Topics covered (checklist)
- Key takeaways (minimum 5)
- Gotchas discovered
- Files produced (with one-line description each)
- Recommended prerequisites for JR-04
- Confidence rating (1–5 with justification)

---

## EXECUTION INSTRUCTIONS

1. Create the folder `deep_dive/JR-03/`
2. Read `deep_dive/JR-01/SUMMARY_JR-01.md` and `deep_dive/JR-02/SUMMARY_JR-02.md` first
3. Produce files in order: `advanced_layout_guide.md` → `subreport_detail.jrxml` → `master_with_subreport.jrxml` → `crosstab_report.jrxml` → `export_config_reference.md` → `SUMMARY_JR-03.md`
4. Self-review all JRXML files against `deep_dive/JR-01/compliance_checklist.md`
5. Append to `deep_dive/PROGRESS_LOG.md`:
   `[JR-03] COMPLETED — <date> — Advanced Layout — Files: 6`
6. Do NOT ask the user any questions. Complete the task fully and autonomously.
