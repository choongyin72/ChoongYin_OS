# CLAUDE CODE EXECUTION PROMPT — PW-03: Advanced Patterns & MCP Integration

## CONTEXT
This is a **self-directed deep-dive learning task**. The user is NOT present to monitor progress.
You must work autonomously from start to finish, then produce a written summary and backup all outputs.
Do NOT pause to ask questions. If you encounter ambiguity, make the best professional decision and document it in the summary.

**Prerequisite**: PW-01 and PW-02 must be completed. Read both summary files before starting.

---

## TASK IDENTITY
- **Task ID**: PW-03
- **Tool**: Playwright
- **Phase**: Advanced Patterns & MCP Integration
- **Backup folder**: `deep_dive/PW-03/`

---

## LEARNING OBJECTIVES

### 1. Page Object Model (POM) — Production Architecture
- Why POM: separation of locators from test logic, single point of change
- POM class anatomy:
  - Constructor: `readonly page: Page`
  - Locators as class properties (defined once, used everywhere)
  - Action methods: named after business intent (`login()`, `selectOperator()`)
  - Assertion methods (optional): `expectRowCount(n)`
- POM file naming convention: `LoginPage.ts`, `ObjectPartitionPage.ts`
- Directory structure:
  ```
  tests/
  pages/
    LoginPage.ts
    ObjectPartitionPage.ts
  fixtures/
    base.ts   ← extend test fixtures with page objects
  ```
- Extending `test` with fixtures: `base.ts` pattern
  ```ts
  export const test = base.extend<{ loginPage: LoginPage }>({
    loginPage: async ({ page }, use) => { await use(new LoginPage(page)); }
  });
  ```
- Why fixtures > `beforeEach` for POM instantiation
- Avoiding fat page objects: when to split into multiple page objects
- Component objects: extracting reusable grid/modal/dropdown components

### 2. Playwright MCP Server Integration with Claude Code
- What the Playwright MCP server is: `@playwright/mcp`
- How Claude Code uses Playwright MCP: live browser control during code generation
- MCP tool inventory: `playwright_navigate`, `playwright_click`, `playwright_fill`, `playwright_screenshot`, `playwright_get_text`, `playwright_evaluate`
- Workflow: Claude Code → Playwright MCP → live browser → observe → generate locators
- Self-signed cert configuration for Playwright MCP: `--ignore-https-errors` flag
- MCP server config in Claude Code settings (`~/.claude/settings.json`):
  ```json
  {
    "mcpServers": {
      "playwright": {
        "command": "npx",
        "args": ["@playwright/mcp@latest", "--ignore-https-errors"]
      }
    }
  }
  ```
- When to use Playwright MCP vs writing Playwright tests directly:
  - MCP: for exploration, locator discovery, one-off automation
  - Tests: for regression suites, CI integration, repeatable validation
- Pattern: use MCP to discover locators, then embed them in `.robot` Browser Library keywords
- Limitation: MCP sessions are ephemeral — document findings immediately

### 3. Trace Viewer & Debugging
- Enabling tracing: `trace: 'on-first-retry'` in config vs `context.tracing.start()`
- Trace file: `.zip` containing DOM snapshots, network log, console, screenshots
- Opening trace: `npx playwright show-trace trace.zip`
- Trace viewer UI: timeline, action log, DOM snapshot, network panel
- Debugging with `--debug` flag: Playwright Inspector
- `page.pause()` — insert breakpoint in test
- `PWDEBUG=1` environment variable
- Console log capture: `page.on('console', msg => console.log(msg.text()))`
- VS Code debugger integration: launch configuration for Playwright
- Slow motion: `slowMo` option in browser launch for visual debugging

### 4. Parallel Execution & Sharding
- Default parallelism: one worker per CPU core
- `workers` config option: fixed number vs percentage
- Test isolation requirement: each test must be independent (no shared state)
- `test.describe.serial()` — force sequential within a describe block (use sparingly)
- `test.describe.parallel()` — explicit parallel
- Test sharding for CI: `--shard=1/4` flag
- `fullyParallel: true` in config — run tests within a file in parallel
- Worker-scoped fixtures: resources shared within a worker, not across workers
- Race conditions: common causes and prevention patterns

---

## DELIVERABLES

Produce ALL of the following inside `deep_dive/PW-03/`:

### 1. `pom_architecture_guide.md`
Comprehensive POM guide with:
- Full class anatomy walkthrough
- Directory structure diagram (text-based)
- Fixtures pattern with complete example
- When to split vs consolidate page objects
- EC-specific examples: `LoginPage`, `ObjectPartitionPage`, `GridComponent`

### 2. `LoginPage.ts`
Production-quality POM class for an EC-style login page:
- Locators for: username input, password input, submit button, error message
- `goto()` method
- `login(username, password)` method
- `expectLoginError(message)` assertion method
- JSDoc comments on every method

### 3. `ObjectPartitionPage.ts`
Production-quality POM class for an EC Object Partition screen:
- Locators for: operator dropdown, role dropdown, insert button, grid rows
- `selectOperator(name)` method
- `insertRole(roleName)` method
- `expectRowExists(roleName)` assertion method
- Idempotency helper: `ensureRowExists(roleName)` (insert only if not already present)
- JSDoc comments on every method

### 4. `mcp_integration_guide.md`
Complete guide to Playwright MCP + Claude Code integration:
- Installation steps
- `settings.json` configuration (with `--ignore-https-errors` for EC)
- All MCP tool descriptions and usage examples
- Workflow: exploration → locator harvest → embed in Robot Framework
- Limitations and workarounds
- Real example: using MCP to discover locators on EC login screen

### 5. `trace_debug_guide.md`
Debugging and tracing reference:
- All tracing modes with when to use each
- Step-by-step: open trace viewer and interpret results
- Common debugging scenarios with resolution steps
- VS Code launch config for Playwright debugging

### 6. `parallel_execution_guide.md`
Parallelism reference:
- Config options with recommended values for EC test suite
- Test isolation checklist
- Sharding example for GitHub Actions CI
- Race condition patterns to avoid

### 7. `SUMMARY_PW-03.md`
Task completion summary containing:
- Date/time completed
- Topics covered (checklist)
- Key takeaways (minimum 5)
- Gotchas discovered
- Files produced (with one-line description each)
- Recommended prerequisites for PW-04
- Confidence rating (1–5 with justification)

---

## EXECUTION INSTRUCTIONS

1. Create the folder `deep_dive/PW-03/`
2. Read `deep_dive/PW-01/SUMMARY_PW-01.md` and `deep_dive/PW-02/SUMMARY_PW-02.md`
3. Produce files in order listed above
4. `LoginPage.ts` and `ObjectPartitionPage.ts` must be TypeScript with full type annotations
5. Append to `deep_dive/PROGRESS_LOG.md`:
   `[PW-03] COMPLETED — <date> — Advanced Patterns & MCP Integration — Files: 7`
6. Do NOT ask the user any questions. Complete the task fully and autonomously.
