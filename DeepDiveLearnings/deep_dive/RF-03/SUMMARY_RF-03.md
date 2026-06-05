# SUMMARY — RF-03: Advanced Patterns

**Date completed:** 2026-06-05
**Task ID:** RF-03

---

## Topics Covered

- [x] ROBOT_CLAUDE.md — definitive governance document (pre-flight, hard-stops, rules)
- [x] 10 forbidden patterns (Sleep, inline locators, Fill Text for search, etc.)
- [x] 8 required patterns (documentation, teardown screenshot, networkidle, etc.)
- [x] Variable and keyword naming conventions
- [x] EC-specific mandatory patterns
- [x] How to handle ambiguous requirements
- [x] Idempotent test patterns — ensure-state before AND after
- [x] `Run Keyword And Continue On Failure` for cleanup
- [x] AUTOTEST_ prefix convention
- [x] Screenshot-on-failure with `${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}` path
- [x] `Set Test Metadata` for custom report info
- [x] Log levels: INFO/WARN/DEBUG with semicolon format for Excel
- [x] Pabot parallel execution — workers, pabotlib, lock/unlock
- [x] Robotidy formatter — .robotidy config for EC
- [x] Robocop linter — enforced and disabled rules for EC

---

## Key Takeaways

1. **`ROBOT_CLAUDE.md` is the weapon** — this single file governs all future RF code generation. Place at project root. Claude Code reads it before writing any .robot file. All 10 forbidden + 8 required patterns encoded.

2. **Idempotency requires BOTH setup and teardown cleanup** — cleaning only in teardown means the first run after a partial failure leaves dirty state. Clean in BOTH places.

3. **`Run Keyword And Continue On Failure` in teardown** — ensures ALL cleanup steps run even if one fails. Without this, a failed delete step leaves subsequent cleanup skipped.

4. **Screenshot path `${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}`** — uses RF built-in variables for cross-platform path separation. Always use this exact pattern.

5. **Workers ≤ 4 for EC Oracle** — Oracle connection pool has limits. More than 4 parallel workers risks connection exhaustion. Test with 2, scale to 4 in CI.

---

## Files Produced

| File | Description |
|---|---|
| `ROBOT_CLAUDE.md` | ★ Governance document — copy to project root |
| `idempotency_patterns.robot` | Ensure-state pattern, AUTOTEST_ prefix, cleanup in setup+teardown |
| `advanced_teardown_example.robot` | Screenshot-on-failure, Set Test Metadata, log levels |
| `pabot_guide.md` | Installation, CLI flags, worker config, lock patterns, result merging |
| `linting_guide.md` | Robotidy + Robocop config, enforced rules, justified exceptions |
| `SUMMARY_RF-03.md` | This file |

---

## Confidence Rating: 5/5

`ROBOT_CLAUDE.md` is the most important artefact across all 12 tasks. It encodes everything learned across RF-01, RF-02, and RF-03 into a single governance document. When placed at the EC project root, it ensures consistent, correct Robot Framework code generation for all future EC automation work.
