# CLAUDE CODE EXECUTION PROMPT — RF-03: Advanced Patterns

## CONTEXT
This is a **self-directed deep-dive learning task**. The user is NOT present to monitor progress.
You must work autonomously from start to finish, then produce a written summary and backup all outputs.
Do NOT pause to ask questions. If you encounter ambiguity, make the best professional decision and document it in the summary.

**Prerequisite**: RF-01 and RF-02 must be completed. Read both summary files and the RF-02 architecture guide before starting.

---

## TASK IDENTITY
- **Task ID**: RF-03
- **Tool**: Robot Framework
- **Phase**: Advanced Patterns
- **Backup folder**: `deep_dive/RF-03/`

---

## LEARNING OBJECTIVES

### 1. ROBOT_CLAUDE.md Governance Rules
`ROBOT_CLAUDE.md` is the governing document for how Claude Code must behave when generating `.robot` files. Study and internalise these rules — you will be authoring the definitive version in this task.

The rules Claude Code MUST follow:

**Pre-flight discipline (MANDATORY before writing any code):**
1. Read `ROBOT_CLAUDE.md` (this file) — no exceptions
2. Read ALL existing `.robot` and `.resource` files relevant to the screen being automated
3. Perform live UI scan using Playwright MCP BEFORE writing any locators
4. Map discovered locators to variables BEFORE writing page keywords
5. Check `variables/` layer — if a similar selector already exists, REUSE it, do not invent a new one

**Hard-stop conditions (Claude Code must STOP and report to user):**
- Any locator cannot be found via live scan
- The screen layout differs significantly from the description
- An existing keyword almost covers the need but not exactly
- The task requires data setup that might affect production/other tests

**Code generation rules:**
- NEVER generate a locator string inline in a page or keyword file
- NEVER duplicate an existing keyword — reuse it or extend it
- NEVER write `Sleep` or `Wait For Timeout` — use `Wait For Elements State` with `${WAIT_TIMEOUT}`
- NEVER hardcode `EC_URL`, usernames, passwords, or environment-specific values
- ALWAYS add `[Documentation]` to every keyword
- ALWAYS use `Run Keyword If Test Failed    Take Screenshot` in Test Teardown
- ALWAYS follow the 5-layer architecture — no exceptions

### 2. Idempotent Test Patterns & Cleanup
- Why idempotency matters: tests must be repeatable without manual cleanup
- The "ensure state" pattern:
  ```robot
  Ensure Role Does Not Exist For Operator
      [Arguments]    ${operator}    ${role}
      ${exists}=    Check Row In Grid    ${GRID_SELECTOR}    ${role}
      IF    ${exists}
          Delete Row From Grid    ${role}
      END
  ```
- Setup/teardown ordering: clean BEFORE insert (not just after)
- `Run Keyword And Continue On Failure` — when to use for cleanup
- Test data naming: use unique prefixes (`AUTOTEST_`) to distinguish test data from production data
- Bulk cleanup keywords: `Clean Up All Autotest Data`
- Idempotency verification: verify → conditionally act → verify again
- Handling cleanup failures: log and continue vs fail the test

### 3. Screenshot-on-Failure & Reporting
- Standard teardown pattern (MANDATORY in every test file):
  ```robot
  Test Teardown    Run Keyword If Test Failed
  ...    Take Screenshot    ${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}_failure
  ```
- Custom listener for enhanced failure reporting (Python listener class)
- `${OUTPUT_DIR}` built-in variable — always use for screenshot paths
- `${SUITE_NAME}`, `${TEST_NAME}`, `${TEST_STATUS}` — built-in metadata variables
- Robot Framework report customisation: `--reporttitle`, `--logtitle`
- Adding custom metadata to reports: `Set Suite Metadata`, `Set Test Metadata`
- Pabot report merging: `python -m pabot.pabotlib` result merge
- Log levels: `Log    message    level=INFO/DEBUG/WARN`
- `Log To Console` — use sparingly, only for CI visibility

### 4. Pabot Parallel Execution
- What Pabot is: parallel executor for Robot Framework
- Installation: `pip install robotframework-pabot`
- Basic usage: `pabot --processes 4 tests/`
- `--testlevelsplit` — run individual tests in parallel (vs suite-level)
- `pabot --pabotlib` — shared resource locking for data conflicts
- `PABOT_EXECUTION_POOL_ID` — identify parallel worker in keywords
- `Acquire Lock` / `Release Lock` — prevent test data conflicts in parallel
- `Acquire Value Set` / `Release Value Set` — parallel-safe test data pools
- When NOT to parallelise: tests that share mutable data, login-dependent sequences
- Configuring workers: `--processes` vs `--resourcefile`
- Pabot `pabot_results/` output — merging results

### 5. Robotidy & Robocop Linting
**Robotidy (formatter):**
- `robotidy <path>` — format in place
- `robotidy --check` — check without modifying (for CI)
- Key transformations applied: `AlignKeywordsTestCases`, `NormalizeSeparators`, `OrderSettings`
- `.robotidy` config file: customising transformations
- VS Code integration: format on save

**Robocop (linter):**
- `robocop <path>` — lint
- Severity levels: `E` (error), `W` (warning), `I` (info)
- Key rules to enforce: `missing-doc-keyword`, `too-long-keyword`, `not-allowed-char-in-name`, `duplicated-library-import`
- `.robocop` config file
- Rules to disable for EC project (and why): document justified exceptions
- Integration in CI: `robocop --no-dotfile-discovery tests/ resources/`
- VS Code integration: RobotCode extension runs Robocop inline

---

## DELIVERABLES

Produce ALL of the following inside `deep_dive/RF-03/`:

### 1. `ROBOT_CLAUDE.md`
The definitive governance document for Claude Code. This is the real file that will be placed at the project root.
Structure:
- Purpose and scope
- Pre-flight checklist (numbered, checkboxes)
- Hard-stop conditions (numbered list)
- Code generation rules (numbered, categorical)
- Architecture layer rules (with diagram)
- Variable naming conventions
- Keyword naming conventions
- Forbidden patterns (explicit list of things never to do)
- Required patterns (explicit list of things always to do)
- How to handle ambiguous requirements

### 2. `idempotency_patterns.robot`
A `.robot` file demonstrating:
- `Ensure Role Does Not Exist` pattern
- Setup idempotency: clean → insert → verify
- Teardown idempotency: delete → verify deleted
- `AUTOTEST_` naming convention in test data
- `Run Keyword And Continue On Failure` in cleanup

### 3. `advanced_teardown_example.robot`
Demonstrates:
- Screenshot-on-failure with `${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}_failure`
- Suite-level and test-level teardown combinations
- `Set Test Metadata` for custom report info
- Custom log messages with levels

### 4. `pabot_guide.md`
Complete Pabot reference:
- Installation
- All CLI flags with explanations
- Worker configuration recommendations for EC test suite
- `pabotlib` shared resources with code examples
- Lock/unlock patterns for EC data conflicts
- CI integration example

### 5. `linting_guide.md`
Robotidy + Robocop reference:
- Setup instructions
- `.robotidy` config for EC project
- `.robocop` config for EC project
- All enforced rules with rationale
- All disabled rules with justification
- CI pipeline integration steps

### 6. `SUMMARY_RF-03.md`
Standard task summary.

---

## EXECUTION INSTRUCTIONS

1. Create the folder `deep_dive/RF-03/`
2. Read `deep_dive/RF-01/SUMMARY_RF-01.md` and `deep_dive/RF-02/SUMMARY_RF-02.md` and `deep_dive/RF-02/architecture_guide.md`
3. `ROBOT_CLAUDE.md` is the most important deliverable — spend the most effort here; it will govern all future robot file generation
4. Produce files in order listed above
5. Self-check `idempotency_patterns.robot` and `advanced_teardown_example.robot` for syntax correctness
6. Append to `deep_dive/PROGRESS_LOG.md`:
   `[RF-03] COMPLETED — <date> — Advanced Patterns — Files: 6`
7. Do NOT ask the user any questions. Complete the task fully and autonomously.
