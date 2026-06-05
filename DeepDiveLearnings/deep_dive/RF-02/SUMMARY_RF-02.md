# SUMMARY — RF-02: Layered POM Architecture

**Date completed:** 2026-06-05
**Task ID:** RF-02

---

## Topics Covered

- [x] 5-layer architecture: tests/keywords/pages/variables/libraries
- [x] Layer rules — what belongs in each layer
- [x] Test layer: pure business steps, no selectors
- [x] Keywords layer: business operations, idempotency helpers
- [x] Pages layer: screen-specific Browser Library calls with variable selectors
- [x] Variables layer: ALL locators, centralised
- [x] Libraries layer: Python utilities (DB, generators, parsers)
- [x] Environment variable files: local.py, test.py (COPS DEV), prod.py
- [x] Suite setup/teardown patterns
- [x] Idempotent test design: Test Setup + Test Teardown cleanup
- [x] AUTOTEST_ prefix convention for test data
- [x] Custom Python library: ECHelpers with DB query and grid parsing

---

## Key Takeaways

1. **The 5-layer architecture is the EC project standard** — the existing `C:\DEV\ROBOT\APPS\EC\14.2.4\AutomationTest` project follows exactly this pattern. All new tests must fit this structure.

2. **Never put selectors in tests or keywords** — selectors change when EC updates. With all selectors in variables/, fixing a selector change is 1 file edit, not hunting through 20 test files.

3. **Idempotency = Test Setup AND Test Teardown both clean** — `Ensure Role Does Not Exist` in BOTH setup (clean before test) and teardown (clean after test). This means tests can be re-run without manual cleanup.

4. **ECHelpers Python library bridges RF and Oracle DB** — `ROBOT_LIBRARY_SCOPE = 'SUITE'` creates one DB connection per suite. DB queries return Robot-compatible types (string, bool, list).

5. **Three variable files = three environments** — `local.py` (localhost), `test.py` (COPS DEV), `prod.py` (production). Switch with `--variablefile vars/test.py`. No code changes needed.

---

## Files Produced (17)

| File | Layer | Description |
|---|---|---|
| `tests/login/TC_Login.robot` | 1 | Login test suite — 3 test cases |
| `tests/object_partition/TC_ObjectPartition.robot` | 1 | Object Partition — 3 idempotent tests |
| `resources/keywords/LoginKeywords.resource` | 2 | Login business operations |
| `resources/keywords/ObjectPartitionKeywords.resource` | 2 | Object Partition business operations + idempotency |
| `resources/pages/LoginPage.resource` | 3 | Keycloak form interactions |
| `resources/pages/ObjectPartitionPage.resource` | 3 | Grid/dropdown/insert interactions |
| `resources/variables/common_variables.robot` | 4 | Shared EC variables |
| `resources/variables/login_variables.robot` | 4 | Login screen selectors |
| `resources/variables/object_partition_variables.robot` | 4 | Object Partition selectors |
| `resources/libraries/ECHelpers.py` | 5 | Python DB + utilities library |
| `data/object_partition_data.py` | data | Test data (operators, roles) |
| `vars/local.py` | env | Local EC environment |
| `vars/test.py` | env | COPS DEV environment |
| `vars/prod.py` | env | Production (read-only) |
| `architecture_guide.md` | doc | Layer rules, anti-patterns |
| `SUMMARY_RF-02.md` | doc | This file |

---

## Confidence Rating: 5/5

The 5-layer architecture is already in production use in the EC automation project. This scaffold is a clean reference implementation of those patterns, extended with explicit documentation and idempotency examples.
