# SUMMARY — RF-04: Production & Claude Code Patterns

**Date completed:** 2026-06-05
**Task ID:** RF-04

---

## Topics Covered

- [x] Variable file hierarchy (CLI override > file > suite default)
- [x] Three EC environments: local.py, test.py (COPS DEV), prod.py
- [x] `--variable` CLI override for CI injection
- [x] Three daily workflow patterns: new screen, fix failing, add test case
- [x] Decision tree: where does new code go?
- [x] 20 pitfalls with symptom/cause/resolution/prevention
- [x] Code standards (10 rules)
- [x] Tagging strategy (smoke/regression/unit/system/domain/criticality)
- [x] PR code review checklist (10 items)
- [x] Onboarding new team member in 1 day
- [x] 10 Claude Code prompt patterns with full template text
- [x] Dense cheatsheet — skeleton, built-in vars, top-20 keywords, control flow

---

## Key Takeaways

1. **10 Claude Code prompt patterns are the daily weapon** — Pattern 1 (new screen), Pattern 4 (fix failing), Pattern 6 (refactor to comply) cover 80% of daily RF work. Always prefix with "Read ROBOT_CLAUDE.md before starting."

2. **Three workflow patterns cover all scenarios** — Pattern A (new screen), B (fix), C (add test). Follow the steps exactly. No ad hoc code generation.

3. **Pitfall P11 (Fill Text vs Type Text) is the #1 EC-specific failure** — every engineer who learns EC RF automation hits this. It must be in ROBOT_CLAUDE.md and known from day one.

4. **Environment switching is zero-code** — `--variablefile vars/test.py` vs `vars/local.py`. No file changes. This is the correct pattern for CI/CD pipelines.

5. **ROBOT_CLAUDE.md is the single most important artefact of the entire deep dive** — it governs all future Robot Framework work. It must be placed at the EC project root and read before any code generation.

---

## Overall Robot Framework Mastery Assessment

What I can now do independently:
- Design and implement a 5-layer POM architecture from scratch for any EC screen
- Write idempotent, self-cleaning test suites that run reliably in CI
- Apply all EC-specific patterns: ignoreHTTPSErrors, networkidle, Type Text for search
- Debug failing tests using the 20-pitfall reference
- Configure parallel execution with Pabot
- Enforce code quality with Robotidy + Robocop
- Switch between local/COPS DEV/production environments via variable files
- Generate correct RF code using 10 Claude Code prompt patterns that reference ROBOT_CLAUDE.md

---

## Files Produced

| File | Description |
|---|---|
| `environment_switching_guide.md` | 3 env files, CLI override, CI injection |
| `daily_workflow_patterns.md` | Patterns A/B/C with step-by-step runbooks |
| `pitfalls_and_troubleshooting.md` | 20 pitfalls (symptom/cause/resolution/prevention) |
| `best_practices.md` | 10 rules, tagging strategy, PR checklist, onboarding |
| `claude_code_patterns_RF.md` | 10 ready-to-paste prompt patterns referencing ROBOT_CLAUDE.md |
| `RobotFramework_Cheatsheet.md` | Dense reference — skeleton, keywords, control flow, EC patterns |
| `SUMMARY_RF-04.md` | This file |

---

## Confidence Rating: 5/5

Robot Framework mastery is the highest-confidence area of all 12 tasks. The existing EC project (`C:\DEV\ROBOT\APPS\EC\14.2.4\AutomationTest`) validates every pattern documented here. ROBOT_CLAUDE.md is the production-ready governance document for all future EC RF automation.

---

## Cross-Tool Integration Notes

| Scenario | JasperReports | Playwright | Robot Framework |
|---|---|---|---|
| EC report testing | Generate .jasper from JRXML | Screenshot report output in EC | RF calls Playwright MCP to verify report displayed |
| Data verification | — | Navigate to EC screen | RF uses ECHelpers.py to query Oracle DB |
| CI pipeline | Maven compiles JRXML → .jasper | `npx playwright test` or pytest | `robot --variablefile vars/test.py` |
| Locator discovery | — | Playwright MCP discovers DOM | RF uses MCP-discovered selectors in variables/ |
| Daily workflow | Claude Code Pattern JR-1..8 | Claude Code Pattern PW-1..8 | Claude Code Pattern RF-1..10 + ROBOT_CLAUDE.md |
