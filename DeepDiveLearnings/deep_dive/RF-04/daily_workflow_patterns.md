# Daily Workflow Patterns — Robot Framework + Claude Code

## Pattern A: Automate a New EC Screen

**Trigger:** User asks to automate a screen not yet in the project

### Steps
1. **Read ROBOT_CLAUDE.md** (mandatory — placed at project root)
2. **Understand the screen** — user provides screen name + manual test steps
3. **Scan live UI with Playwright MCP:**
   - Navigate to local EC: `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`
   - Open the screen via sidebar
   - Inspect DOM for element IDs/classes
   - Document all locators found
4. **Create variables file:** `resources/variables/{screen_name}_variables.robot` with discovered selectors
5. **Create pages file:** `resources/pages/{ScreenName}Page.resource` using ${VARIABLES}
6. **Create keywords file:** `resources/keywords/{ScreenName}Keywords.resource` calling pages
7. **Create test file:** `tests/{category}/TC_{ScreenName}.robot` using keywords only
8. **Run dry-run:** `robot --dryrun tests/{category}/TC_{ScreenName}.robot`
9. **Run linting:** `robocop tests/ resources/`
10. **Run tests:** `robot --variablefile vars/local.py tests/{category}/`
11. **Commit**

---

## Pattern B: Fix a Failing Test

**Trigger:** CI fails, or test was working before EC update

### Steps
1. **Get failure info:** test name, error message, screenshot, log excerpt
2. **Read the failing .robot file** + all imported resources
3. **Use Playwright MCP** to verify current UI state:
   - Navigate to the screen
   - Check if the element still exists with the same selector
4. **Identify root cause:**
   - Selector stale → update in variables/ file
   - Timing issue → increase WAIT_TIMEOUT or add networkidle wait
   - Screen layout changed → remap page keywords
5. **Minimum change principle** — change only what's broken, don't refactor around it
6. **Re-run** to verify fix
7. **Commit** with clear message: `fix: update {screen} locator after EC 14.2.5 update`

---

## Pattern C: Add Test Case to Existing Suite

**Trigger:** New test scenario identified for already-automated screen

### Steps
1. **Read ROBOT_CLAUDE.md** (always first)
2. **Read existing suite** — understand existing test cases and keywords
3. **Check if required keywords exist:**
   - If all keywords exist → write test case only in tests/
   - If new page interaction needed → add to pages/ + keywords/ first
4. **NEVER modify existing keywords** — extend by adding new keyword or optional argument
5. **Write new test case** — pure business steps, no locators
6. **Add idempotent setup/teardown** if test creates data
7. **Run suite** — verify new test passes AND existing tests still pass
8. **Commit**

---

## Decision Tree: Where Does New Code Go?

```
New automation need
    ↓
Is it a new screen?
    YES → Create variables/ + pages/ + keywords/ + tests/ files
    NO → Is it a new scenario on existing screen?
            YES → Does keyword exist in keywords/?
                    YES → Add test case to tests/ only
                    NO → Add to pages/ and keywords/, then tests/
            NO → Is it a new reusable utility?
                    YES → Add to libraries/ECHelpers.py
```
