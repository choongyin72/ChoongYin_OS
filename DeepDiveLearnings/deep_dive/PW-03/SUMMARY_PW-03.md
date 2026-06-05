# SUMMARY — PW-03: Advanced Patterns & MCP Integration

**Date completed:** 2026-06-05
**Task ID:** PW-03

---

## Topics Covered

- [x] POM class anatomy — locators as class properties, action methods, assertion methods
- [x] Fixtures pattern (`base.extend`) — replace beforeEach with type-safe fixtures
- [x] Directory structure: pages/, fixtures/, tests/
- [x] Component objects — reusable GridComponent, NavigatorComponent
- [x] When to split vs consolidate page objects
- [x] Playwright MCP server — `@playwright/mcp`
- [x] `--ignore-https-errors` flag for EC self-signed cert in MCP
- [x] Claude Code settings.json MCP configuration
- [x] MCP workflow: navigate → screenshot → inspect DOM → generate locators → embed in RF
- [x] MCP limitations — ephemeral sessions, document immediately
- [x] Trace viewer — `on-first-retry`, `on`, `retain-on-failure`
- [x] Opening trace: `npx playwright show-trace trace.zip`
- [x] Playwright Inspector — `--debug`, `PWDEBUG=1`, `page.pause()`
- [x] VS Code debugger launch configuration
- [x] Slow motion for visual debugging
- [x] Parallel execution — workers config, fullyParallel
- [x] Test isolation checklist for EC parallel runs
- [x] `test.describe.serial()` for forced sequential tests
- [x] CI sharding: `--shard=1/4`
- [x] Python POM pattern — same structure, sync API

---

## Key Takeaways

1. **Fixtures are the correct POM instantiation pattern in Playwright** — `test.extend<Fixtures>` gives type-safety, automatic teardown, and composability. `beforeEach` is the anti-pattern.

2. **Playwright MCP + `--ignore-https-errors` is the locator discovery tool for EC** — Claude Code can open the real EC Web App, inspect DOM, and generate accurate locators without guessing. This directly feeds into Robot Framework `variables/` layer.

3. **Trace viewer is the fastest debugging tool** — instead of adding `console.log` or `page.pause()`, enable traces. After a failure, `show-trace` shows exactly what happened at each step: DOM snapshot, network, screenshot.

4. **Workers: 2 for local, 4 for CI** — EC Oracle DB connections are expensive. Too many parallel workers will create connection pool exhaustion. Limit to 4 in CI for safety.

5. **`ObjectPartitionPage.ensureRowNotExists()` is idempotency in practice** — a teardown that conditionally deletes is safer than a teardown that always deletes. Tests pass even when the previous run's teardown failed.

---

## Files Produced

| File | Description |
|---|---|
| `pom_architecture_guide.md` | POM anatomy, fixtures, directory structure, Python POM |
| `LoginPage.ts` | Production POM — EC Keycloak login, action + assertion methods |
| `ObjectPartitionPage.ts` | EC Object Partition POM — idempotent insert/delete |
| `mcp_integration_guide.md` | Playwright MCP setup, `--ignore-https-errors`, workflow |
| `trace_debug_guide.md` | Tracing modes, VS Code debugger, common debug scenarios |
| `parallel_execution_guide.md` | Workers, isolation, sharding, EC-specific limits |
| `SUMMARY_PW-03.md` | This file |

---

## Confidence Rating: 4/5
