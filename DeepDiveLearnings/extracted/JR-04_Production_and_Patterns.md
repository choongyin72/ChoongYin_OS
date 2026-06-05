# CLAUDE CODE EXECUTION PROMPT — JR-04: Production & Claude Code Patterns

## CONTEXT
This is a **self-directed deep-dive learning task**. The user is NOT present to monitor progress.
You must work autonomously from start to finish, then produce a written summary and backup all outputs.
Do NOT pause to ask questions. If you encounter ambiguity, make the best professional decision and document it in the summary.

**Prerequisite**: JR-01 through JR-03 must be completed. Read all three summary files before starting.

---

## TASK IDENTITY
- **Task ID**: JR-04
- **Tool**: JasperReports 7.0.3+
- **Phase**: Production & Claude Code Patterns
- **Backup folder**: `deep_dive/JR-04/`

---

## LEARNING OBJECTIVES

### 1. JasperReports Server REST API (v7.0.3+)
- Base URL patterns: `/jasperserver/rest_v2/`
- Authentication: HTTP Basic vs token-based
- Key endpoints:
  - `GET /resources` — browse repository
  - `POST /reports/{reportURI}.pdf` — run report to PDF
  - `POST /reports/{reportURI}.xlsx` — run report to Excel
  - `GET /reports/{reportURI}/inputControls` — get report parameters
  - `PUT /resources/{uri}` — upload JRXML
- Request/response format: JSON vs XML headers
- Passing input control parameters in REST call
- Async report execution: `POST /reportExecutions`, polling for status
- Error response structure and common HTTP status codes
- How EC's JasperServices sits on top of the Jasper REST API

### 2. `compile_and_preview.bat` Patterns
- Command-line compilation: `jrc.bat` / `ant` / Maven plugin
- `JasperCompileManager` Java API (for reference)
- Batch compilation: compiling all `.jrxml` in a folder
- Validation before compile: XML schema check
- Preview via `JasperFillManager` + `JasperViewer` (headless alternative)
- The `compile_and_preview.bat` script conventions established in this project:
  - Input: `.jrxml` path argument
  - Output: `.jasper` + PDF preview in temp folder
  - Error exit codes
- Integration with VS Code tasks: `tasks.json` to trigger compile on save

### 3. Common Pitfalls & Troubleshooting Reference
Produce a definitive reference covering at least 20 pitfalls, each with:
- Symptom / error message
- Root cause
- Resolution steps
- Prevention pattern

Must include:
- `JRException: Subreport not found`
- `Font not found` / blank text in PDF
- `PAGE_COUNT` overcounting
- `isTitleNewPage` footer showing on title page
- CDATA expression syntax errors
- Crosstab cell width overflow
- Excel merged cell issues
- Null pointer in expression
- Band height too small for content
- Parameter type mismatch

### 4. World-Class Best Practices
- Report naming conventions (file names, report names, resource URIs)
- Version control strategy for `.jrxml` files (what to commit, what to `.gitignore`)
- Reusable style templates: `<style>` in master template, imported via `<reportFont>`
- Performance: minimise subreport depth, push aggregation to SQL, avoid scriptlets where possible
- Maintainability: parameterise everything that might change (colours, thresholds, labels)
- Testing strategy: unit test data sets, visual regression via PDF diff
- Documentation inside JRXML: XML comment conventions

### 5. Claude Code Integration Patterns for JasperReports
Define at least 8 repeatable prompt patterns for daily Claude Code use. For each pattern:
- **Pattern name**
- **Trigger**: when to use it
- **Template prompt**: exact text to give Claude Code (with `{placeholders}`)
- **Expected output**: what Claude Code should produce
- **Validation step**: how to verify the output is correct

Required patterns:
1. "Generate new JRXML from column list"
2. "Convert Crystal Reports field to JRXML field"
3. "Add a group with subtotals to existing JRXML"
4. "Fix v7.0.3 compliance violations in JRXML"
5. "Add conditional style (zebra stripe / highlight)"
6. "Generate crosstab from pivot specification"
7. "Generate REST API call for a named report with parameters"
8. "Debug expression: given error message, find root cause"

---

## DELIVERABLES

Produce ALL of the following inside `deep_dive/JR-04/`:

### 1. `rest_api_guide.md`
Complete REST API reference with curl examples for each endpoint listed above.
Include EC/JasperServices-specific notes where the API differs.

### 2. `compile_preview_patterns.md`
Guide to command-line compilation and `compile_and_preview.bat` conventions,
including VS Code `tasks.json` snippet.

### 3. `pitfalls_and_troubleshooting.md`
The 20+ pitfall reference table (symptom / cause / resolution / prevention).

### 4. `best_practices.md`
World-class best practices guide structured as actionable rules, not just descriptions.

### 5. `claude_code_patterns_JR.md`
The 8+ repeatable Claude Code prompt patterns with full template text.
Format each pattern as a ready-to-paste block.

### 6. `JasperReports_Cheatsheet.md`
One-page (dense) cheatsheet covering:
- JRXML skeleton
- All band names
- All variable calculation types
- All resetType options
- Key pdfFontName mappings
- Top 10 most-used properties
- Most common expression patterns
- REST API quick reference

### 7. `SUMMARY_JR-04.md`
Task completion summary containing:
- Date/time completed
- Topics covered (checklist)
- Key takeaways (minimum 5)
- Gotchas discovered
- Files produced (with one-line description each)
- Overall JasperReports mastery assessment: what the user can now do independently
- Confidence rating (1–5 with justification)

---

## EXECUTION INSTRUCTIONS

1. Create the folder `deep_dive/JR-04/`
2. Read all previous JR summaries: `JR-01/SUMMARY_JR-01.md` through `JR-03/SUMMARY_JR-03.md`
3. Produce files in order listed above
4. The cheatsheet must be genuinely dense and production-useful — not a summary of the guide
5. Append to `deep_dive/PROGRESS_LOG.md`:
   `[JR-04] COMPLETED — <date> — Production & Claude Code Patterns — Files: 7`
   `[JR COMPLETE] All 4 JasperReports tasks finished — <date>`
6. Do NOT ask the user any questions. Complete the task fully and autonomously.
