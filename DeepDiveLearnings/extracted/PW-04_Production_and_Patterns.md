# CLAUDE CODE EXECUTION PROMPT — PW-04: Production & Claude Code Patterns

## CONTEXT
This is a **self-directed deep-dive learning task**. The user is NOT present to monitor progress.
You must work autonomously from start to finish, then produce a written summary and backup all outputs.
Do NOT pause to ask questions. If you encounter ambiguity, make the best professional decision and document it in the summary.

**Prerequisite**: PW-01 through PW-03 must be completed. Read all three summary files before starting.

---

## TASK IDENTITY
- **Task ID**: PW-04
- **Tool**: Playwright
- **Phase**: Production & Claude Code Patterns
- **Backup folder**: `deep_dive/PW-04/`

---

## LEARNING OBJECTIVES

### 1. EC Web UI-Specific Patterns
Document patterns specific to testing Energy Components (EC) Web UI:
- Login flow with `${EC_URL}`, `${EC_USERNAME}`, `${EC_PASSWORD}`
- Handling EC's Oracle-backed grid controls (slow query loads)
- Dropdown / lookup field patterns common in EC screens
- Multi-step insert flows (operator → role → confirm): sequencing and wait strategies
- Idempotency verification: check grid before inserting to prevent duplicate data
- EC session timeout: detection and recovery
- EC's URL structure: screen navigation patterns
- Expected EC-specific wait conditions: spinner disappear, grid refresh, modal close

### 2. Common Pitfalls Reference
Produce a definitive reference covering at least 20 Playwright pitfalls, each with:
- Symptom
- Root cause
- Resolution
- Prevention pattern

Must include:
- `Timeout exceeded` on locator — strict mode violation (multiple matches)
- `Element is not visible` — covered by overlay/modal
- `Element is detached from DOM` — stale reference after navigation
- Auth state not loaded — `storageState` path wrong
- `ignoreHTTPSErrors` not working — set at context level, not page level
- Flaky parallel tests — shared state between workers
- Screenshot baseline mismatch — font rendering diff across OS
- Route handler not called — pattern doesn't match actual URL
- `page.waitForTimeout` causing flakiness — replace with assertion-based wait
- Download not triggered — missing `waitForEvent('download')` before click

### 3. CI/CD Integration
- GitHub Actions workflow for Playwright tests:
  - `npx playwright install --with-deps`
  - Run tests: `npx playwright test`
  - Upload HTML report as artifact
  - Upload trace on failure
- Environment variable injection in CI
- Sharding across CI matrix: `strategy.matrix` + `--shard`
- Caching browser binaries to speed up CI
- `reporters`: `['html', 'github']` — GitHub annotations
- Retry strategy in CI vs local

### 4. World-Class Best Practices
- Test naming: `should <action> when <condition>` pattern
- Test independence: every test must set up and tear down its own state
- No `page.waitForTimeout` — always use assertions or `waitForResponse`
- Prefer `getByRole` and `getByLabel` over CSS selectors
- Keep page objects thin: no assertions inside action methods (assertion methods are separate)
- Avoid `test.only` / `test.skip` in committed code
- `.env` for secrets, never hardcode
- `test.step()` — group actions for cleaner trace output
- Code review checklist for Playwright PRs

### 5. Claude Code Integration Patterns for Playwright
Define at least 8 repeatable prompt patterns for daily Claude Code use. For each pattern:
- **Pattern name**
- **Trigger**: when to use it
- **Template prompt**: exact text to give Claude Code (with `{placeholders}`)
- **Expected output**
- **Validation step**

Required patterns:
1. "Generate Page Object from screen description"
2. "Discover locators for {screen} using Playwright MCP"
3. "Convert manual test steps to Playwright spec"
4. "Add auth state setup to existing test suite"
5. "Mock API endpoint {url} to return {fixture}"
6. "Debug failing test: given error message and spec, find root cause"
7. "Add visual regression baseline for {screen}"
8. "Generate CI workflow for Playwright test suite"

---

## DELIVERABLES

Produce ALL of the following inside `deep_dive/PW-04/`:

### 1. `ec_patterns_guide.md`
EC Web UI-specific Playwright patterns guide.
Every pattern must include a working TypeScript snippet.

### 2. `pitfalls_and_troubleshooting.md`
The 20+ pitfall reference (symptom / cause / resolution / prevention).

### 3. `ci_workflow.yml`
A production-quality GitHub Actions workflow file for running Playwright tests:
- Trigger on push/PR to main
- Install Node, install dependencies, install browsers
- Inject environment variables from secrets
- Run tests with sharding (2 shards example)
- Upload HTML report artifact
- Upload trace artifact on failure

### 4. `best_practices.md`
World-class best practices as actionable rules.
Include a PR code review checklist at the end.

### 5. `claude_code_patterns_PW.md`
The 8+ repeatable Claude Code prompt patterns with full template text.

### 6. `Playwright_Cheatsheet.md`
One-page dense cheatsheet covering:
- Locator API quick reference
- Action methods quick reference
- Assertion quick reference
- Config options quick reference
- CLI flags quick reference
- Auth state pattern (3 lines)
- Route intercept pattern (3 lines)
- POM class skeleton (10 lines)

### 7. `SUMMARY_PW-04.md`
Task completion summary containing:
- Date/time completed
- Topics covered (checklist)
- Key takeaways (minimum 5)
- Gotchas discovered
- Files produced (with one-line description each)
- Overall Playwright mastery assessment
- Confidence rating (1–5 with justification)

---

## EXECUTION INSTRUCTIONS

1. Create the folder `deep_dive/PW-04/`
2. Read all previous PW summaries before starting
3. Produce files in order listed above
4. Append to `deep_dive/PROGRESS_LOG.md`:
   `[PW-04] COMPLETED — <date> — Production & Claude Code Patterns — Files: 7`
   `[PW COMPLETE] All 4 Playwright tasks finished — <date>`
5. Do NOT ask the user any questions. Complete the task fully and autonomously.
