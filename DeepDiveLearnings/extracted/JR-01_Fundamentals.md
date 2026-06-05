# CLAUDE CODE EXECUTION PROMPT — JR-01: JasperReports Fundamentals

## CONTEXT
This is a **self-directed deep-dive learning task**. The user is NOT present to monitor progress.
You must work autonomously from start to finish, then produce a written summary and backup all outputs.
Do NOT pause to ask questions. If you encounter ambiguity, make the best professional decision and document it in the summary.

---

## TASK IDENTITY
- **Task ID**: JR-01
- **Tool**: JasperReports 7.0.3+
- **Phase**: Fundamentals
- **Backup folder**: `deep_dive/JR-01/`

---

## LEARNING OBJECTIVES

Cover ALL of the following topics with depth and working examples:

### 1. Core JRXML Structure & Architecture
- What JasperReports is and how the engine works (fill → compile → export pipeline)
- The role of `.jrxml` source files vs compiled `.jasper` files
- JRXML document skeleton: `<jasperReport>` root element and its mandatory attributes
- The 9 standard report bands: `title`, `pageHeader`, `columnHeader`, `detail`, `columnFooter`, `pageFooter`, `lastPageFooter`, `summary`, `noData`
- Band purpose, render order, and when each fires
- `reportElement` anatomy: x, y, width, height coordinate system (pixels, origin top-left)

### 2. v7.0.3 Syntax Compliance Rules — CRITICAL
- Namespace declaration: `xmlns="http://jasperreports.sourceforge.net/jasperreports"`
- Required `schemaLocation` for v7.0.3
- CDATA requirement: ALL expression content MUST be wrapped in `<![CDATA[ ... ]]>`
- Deprecated attributes to NEVER use: list at least 10 with their v7.0.3 replacements
- Attribute casing rules (camelCase enforcement)
- Self-closing vs explicit close tags: which elements require explicit close
- Common XML validation errors and how to read them

### 3. pdfFontName & Font Mapping
- Why `pdfFontName` exists and when it applies (PDF export path only)
- Standard Helvetica family mappings:
  - Regular → `Helvetica`
  - Bold → `Helvetica-Bold`
  - Italic → `Helvetica-Oblique`
  - Bold-Italic → `Helvetica-BoldOblique`
- How to set font on `<textElement><font>` vs `<reportElement>`
- `isPdfEmbedded` attribute: when true vs false
- `pdfEncoding` attribute: standard value
- Common font rendering pitfall: font not found at runtime → resolution steps

### 4. Band Height & Layout Geometry
- How band height is calculated and enforced
- `splitType` attribute: `Stretch`, `Prevent`, `Immediate` — behaviour differences
- `stretchType` on reportElement: `NoStretch`, `ContainerBottom`, `ContainerHeight`, `ElementGroupBottom`, `ElementGroupHeight`
- `isRemoveLineWhenBlank` and `isPrintWhenDetailOverflows`
- `<printWhenExpression>` — syntax and use cases
- Coordinate math: avoiding element overlap and out-of-bounds errors
- How `isTitleNewPage` works and its interaction with footer suppression
- `PAGE_COUNT` built-in variable: why it shows total+1 on title page and how to exclude it

### 5. Parameters, Fields, Variables
- `<parameter>` declaration: name, class, defaultValueExpression
- `<field>` declaration: name, class — mapping to data source columns
- `<variable>` declaration: name, class, resetType, calculation types
- Built-in variables: `PAGE_NUMBER`, `PAGE_COUNT`, `COLUMN_NUMBER`, `REPORT_COUNT`, `COLUMN_COUNT`
- Expression language: Java expressions inside CDATA
- Null-safety patterns: `$F{field} != null ? $F{field} : ""`

---

## DELIVERABLES

Produce ALL of the following files inside `deep_dive/JR-01/`:

### 1. `annotated_template.jrxml`
A fully working JRXML report template that:
- Is v7.0.3 compliant (validate every attribute against compliance rules above)
- Contains ALL 9 bands (some may be empty but must be present and correctly declared)
- Demonstrates at least 3 parameters, 3 fields, 2 variables
- Uses `pdfFontName` Helvetica mappings correctly
- Includes at least one `printWhenExpression`
- Includes page number (`PAGE_NUMBER`) and total pages (`PAGE_COUNT`) in the page footer
- All expressions use CDATA wrapping
- Includes inline XML comments explaining every major section

### 2. `concepts.md`
Prose explanation of all 5 topic areas above. For each topic:
- Clear explanation of the concept
- Annotated code snippet demonstrating it
- At least one real-world use case from an EC/hydrocarbon reporting context
- Common pitfall + resolution

### 3. `compliance_checklist.md`
A reusable checklist with checkboxes for verifying any JRXML is v7.0.3 compliant.
Minimum 20 checklist items.

### 4. `SUMMARY_JR-01.md`
Task completion summary containing:
- Date/time completed
- Topics covered (checklist)
- Key takeaways (minimum 5)
- Gotchas discovered during this task
- Files produced (with one-line description each)
- Recommended prerequisites for JR-02
- Confidence rating: how well the examples demonstrate production readiness (1–5 scale with justification)

---

## EXECUTION INSTRUCTIONS

1. Create the folder `deep_dive/JR-01/` before writing any files
2. Produce files in this order: `concepts.md` → `annotated_template.jrxml` → `compliance_checklist.md` → `SUMMARY_JR-01.md`
3. After producing `annotated_template.jrxml`, self-review it against the compliance checklist before finalising
4. If any v7.0.3 violation is found during self-review, fix it before saving
5. Append one line to `deep_dive/PROGRESS_LOG.md`:
   `[JR-01] COMPLETED — <date> — JasperReports Fundamentals — Files: 4`
   (Create `PROGRESS_LOG.md` if it does not exist)
6. Do NOT ask the user any questions. Complete the task fully and autonomously.
