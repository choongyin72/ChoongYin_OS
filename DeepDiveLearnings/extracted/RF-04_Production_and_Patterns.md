# CLAUDE CODE EXECUTION PROMPT — RF-04: Production & Claude Code Patterns

## CONTEXT
This is a **self-directed deep-dive learning task**. The user is NOT present to monitor progress.
You must work autonomously from start to finish, then produce a written summary and backup all outputs.
Do NOT pause to ask questions. If you encounter ambiguity, make the best professional decision and document it in the summary.

**Prerequisite**: RF-01 through RF-03 must be completed. Read all three summary files and `ROBOT_CLAUDE.md` before starting.

---

## TASK IDENTITY
- **Task ID**: RF-04
- **Tool**: Robot Framework
- **Phase**: Production & Claude Code Patterns
- **Backup folder**: `deep_dive/RF-04/`

---

## LEARNING OBJECTIVES

### 1. Variable Files & Environment Switching
- Python variable files (`.py`): defining variables as module-level names
- YAML variable files: alternative syntax
- Selecting environment at runtime: `robot --variablefile vars/dev.py tests/`
- CI environment injection: `robot --variable EC_URL:$EC_URL tests/`
- Variable file hierarchy: command-line overrides file overrides suite defaults
- Secret management: environment variables > variable files > hardcoded (never)
- `OperatingSystem.Get Environment Variable` keyword for runtime env var access
- `.env` file + loading pattern (not native to Robot Framework — use Python library or pre-process)
- Switching browsers: `${BROWSER}` variable — `chromium`, `firefox`, `webkit`
- Headless mode: `${HEADLESS}` variable — `True`/`False`

### 2. EC Web UI Daily Workflow Patterns
Document the complete daily workflow for using Claude Code + Robot Framework on EC project work:

**Pattern A — New screen automation:**
1. Get screen name and manual test steps from user
2. Claude Code reads `ROBOT_CLAUDE.md` (mandatory)
3. Claude Code reads all existing related `.robot`/`.resource` files
4. Claude Code uses Playwright MCP to scan live UI
5. Claude Code proposes variable names for new selectors
6. User approves or adjusts variable names
7. Claude Code writes `variables/` file additions
8. Claude Code writes `pages/` resource additions
9. Claude Code writes `keywords/` additions
10. Claude Code writes `tests/` test case
11. User runs `robotidy` + `robocop` to validate
12. User runs test dry-run to verify

**Pattern B — Fix failing test:**
1. User provides: test name, error message, log excerpt
2. Claude Code reads the failing `.robot` file + related resources
3. Claude Code uses Playwright MCP to verify current UI state
4. Claude Code identifies root cause: selector stale / timing / logic error
5. Claude Code proposes targeted fix (minimum change principle)
6. User approves and applies

**Pattern C — Add test case to existing suite:**
1. User describes new scenario
2. Claude Code reads existing suite files
3. Claude Code checks if all required keywords already exist
4. If yes: write new test case only
5. If no: extend keywords layer + write test case
6. Never modify existing keywords — extend or add new ones

### 3. Common Pitfalls Reference
Produce a definitive reference covering at least 20 Robot Framework pitfalls, each with:
- Symptom
- Root cause
- Resolution
- Prevention

Must include:
- `No keyword with name` — import path wrong or typo
- `Variable not found` — wrong scope or not imported
- `ElementNotFound` after navigation — missing wait
- Selector working in MCP but not in test — context/timing difference
- `Sleep` causing flakiness — replace with Wait For Elements State
- Parallel test data conflict — missing Pabot lock
- Screenshot path with special chars — Windows path separator issue
- Variable file not loaded — wrong `--variablefile` path
- CDATA-like issue: embedded `${` in selector string — escaping with `\${`
- Test passes locally, fails in CI — headless rendering difference

### 4. World-Class Best Practices
- Robot Framework coding standards (keyword naming, variable naming, file naming)
- Test design: one assertion focus per test case
- Tag strategy: `smoke` (< 2 min), `regression` (full suite), screen-name tags
- CI pipeline design for EC test suite: nightly regression + PR smoke
- Maintenance strategy: when to update selectors vs rewrite keywords
- Versioning `.robot` files: commit messages, PR discipline
- Documentation standards: `*** Documentation ***` section in every suite
- Test data lifecycle: setup → use → teardown, AUTOTEST_ prefix
- Onboarding new team member to the framework in 1 day

### 5. Claude Code Integration Patterns for Robot Framework
Define at least 10 repeatable prompt patterns. For each:
- **Pattern name**
- **Trigger**: when to use it
- **Template prompt**: exact text (with `{placeholders}`)
- **Expected output**
- **Validation step**
- **ROBOT_CLAUDE.md rules invoked**

Required patterns:
1. "Automate new EC screen: {screen_name}"
2. "Convert manual test steps to Robot Framework test case"
3. "Add keyword for {action} on {screen}"
4. "Fix failing test: {test_name} — error: {error_message}"
5. "Add idempotency to existing test: {test_name}"
6. "Refactor .robot file to comply with ROBOT_CLAUDE.md"
7. "Add Pabot parallel support to test suite"
8. "Generate variable file entries for {screen} discovered selectors"
9. "Review .robot file for Robocop violations and fix them"
10. "Generate complete test suite from test specification document"

---

## DELIVERABLES

Produce ALL of the following inside `deep_dive/RF-04/`:

### 1. `environment_switching_guide.md`
Complete guide to variable files, environment switching, and secret management in EC context.
Include: example `vars/dev.py`, `vars/test.py`, `vars/prod.py` showing real variable shapes.

### 2. `daily_workflow_patterns.md`
The 3 workflow patterns (A, B, C) documented as step-by-step runbooks with decision trees.
Each step must be actionable — not abstract guidance.

### 3. `pitfalls_and_troubleshooting.md`
20+ pitfall reference (symptom / cause / resolution / prevention).

### 4. `best_practices.md`
World-class best practices as actionable rules.
Include: PR code review checklist, onboarding checklist, maintenance checklist.

### 5. `claude_code_patterns_RF.md`
10+ repeatable Claude Code prompt patterns with full template text.
Format as ready-to-paste blocks with placeholder syntax.

### 6. `RobotFramework_Cheatsheet.md`
Dense one-pager covering:
- `.robot` file skeleton (all 4 sections)
- All built-in variables: `${OUTPUT_DIR}`, `${SUITE_NAME}`, `${TEST_NAME}`, `${TEST_STATUS}`, etc.
- Browser Library top-20 keywords (name + signature)
- Variable types: `${}`, `@{}`, `&{}`
- Argument patterns: positional, named, defaults, `*varargs`, `**kwargs`
- Tag syntax
- FOR loop syntax (RF5)
- IF/ELSE IF/ELSE syntax (RF5)
- TRY/EXCEPT syntax (RF5)
- `Run Keyword If` vs `IF` block — when to use each
- Teardown pattern (3 lines)
- Screenshot on failure pattern (2 lines)

### 7. `SUMMARY_RF-04.md`
Task completion summary + **Master Learning Assessment**:
- Date/time completed
- Topics covered across all RF tasks (checklist)
- Key takeaways (minimum 5)
- Gotchas discovered
- Files produced
- Overall Robot Framework mastery assessment: what the user can now do independently
- Confidence rating (1–5 with justification)
- **Cross-tool integration notes**: how JasperReports + Playwright + Robot Framework work together in EC daily workflow

---

## EXECUTION INSTRUCTIONS

1. Create the folder `deep_dive/RF-04/`
2. Read ALL previous RF summaries and `deep_dive/RF-03/ROBOT_CLAUDE.md`
3. Produce files in order listed above
4. `claude_code_patterns_RF.md` patterns must reference `ROBOT_CLAUDE.md` rules explicitly
5. Append to `deep_dive/PROGRESS_LOG.md`:
   `[RF-04] COMPLETED — <date> — Production & Claude Code Patterns — Files: 7`
   `[RF COMPLETE] All 4 Robot Framework tasks finished — <date>`
   `[ALL COMPLETE] Full deep-dive learning session finished — <date>`
6. After the final log entry, produce a `deep_dive/MASTER_SUMMARY.md` file that:
   - Lists all 12 tasks with status, date, file count
   - Summarises the 3 tools and their integration
   - Lists the top 5 most important things learned across all tasks
   - States what the user is now capable of doing independently
   - Suggests next learning topics to deepen expertise further
7. Do NOT ask the user any questions. Complete the task fully and autonomously.
