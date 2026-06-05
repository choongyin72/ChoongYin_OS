# CLAUDE CODE EXECUTION PROMPT — RF-02: Layered POM Architecture

## CONTEXT
This is a **self-directed deep-dive learning task**. The user is NOT present to monitor progress.
You must work autonomously from start to finish, then produce a written summary and backup all outputs.
Do NOT pause to ask questions. If you encounter ambiguity, make the best professional decision and document it in the summary.

**Prerequisite**: RF-01 must be completed. Read `deep_dive/RF-01/concepts.md` before starting.

---

## TASK IDENTITY
- **Task ID**: RF-02
- **Tool**: Robot Framework
- **Phase**: Layered POM Architecture
- **Backup folder**: `deep_dive/RF-02/`

---

## LEARNING OBJECTIVES

### 1. The Layered POM Architecture — Design Principles
The EC project uses a strict 5-layer architecture. Learn and internalise every rule:

```
project_root/
├── tests/                        ← Layer 1: Test cases ONLY (no locators, no implementation)
│   ├── login/
│   │   └── TC_Login.robot
│   └── object_partition/
│       └── TC_ObjectPartition.robot
│
├── resources/
│   ├── keywords/                 ← Layer 2: Business-level keywords (what to do)
│   │   ├── LoginKeywords.resource
│   │   └── ObjectPartitionKeywords.resource
│   │
│   ├── pages/                    ← Layer 3: Page-level keywords (how to do it on this screen)
│   │   ├── LoginPage.resource
│   │   └── ObjectPartitionPage.resource
│   │
│   ├── variables/                ← Layer 4: All variables and selectors
│   │   ├── common_variables.robot
│   │   ├── login_variables.robot
│   │   └── object_partition_variables.robot
│   │
│   └── libraries/                ← Layer 5: Custom Python libraries
│       └── ECHelpers.py
│
├── data/                         ← Test data (separate from keywords)
│   └── object_partition_data.py
│
└── vars/                         ← Environment variable files
    ├── dev.py
    ├── test.py
    └── prod.py
```

**Layer rules (MANDATORY — never violate):**
- `tests/` files: contain ONLY test cases. Import from `keywords/`. No locators, no `Click`, no `Fill Text`.
- `keywords/` files: business-level keywords only. Call page-level keywords. No direct locator strings.
- `pages/` files: screen-specific implementation keywords. Use locators from `variables/`. Call Browser Library directly.
- `variables/` files: ALL locator strings, ALL configurable values. Never hardcode in pages or keywords.
- `libraries/` files: Python utilities that cannot be expressed in Robot syntax.

### 2. Test Layer (tests/)
- Test case naming: `TC_<ScreenName>_<Scenario>.robot` or descriptive name
- Test cases must read like business requirements: `Insert New Role For Operator`
- `[Tags]` usage: `smoke`, `regression`, `object_partition`, `login`
- Suite `Documentation` explaining what the suite covers
- Import pattern:
  ```robot
  *** Settings ***
  Resource    ../../resources/keywords/ObjectPartitionKeywords.resource
  Variables   ../../resources/variables/object_partition_variables.robot
  Variables   ../../vars/${ENV}.py
  ```
- No more than 10–15 steps per test case (if longer, extract to keyword)

### 3. Keywords Layer (resources/keywords/)
- Business-readable keyword names: verb-first, plain English
- Keywords call page-layer keywords: `ObjectPartitionPage.Select Operator`
- Arguments passed through: `Insert Role For Operator    ${OPERATOR}    ${ROLE}`
- Teardown keywords: `Clean Up Inserted Role    ${ROLE}`
- Each keyword: `[Documentation]`, `[Arguments]`, clear steps
- Idempotency helpers live here: `Ensure Role Does Not Exist    ${ROLE}`

### 4. Pages Layer (resources/pages/)
- Page keywords map 1:1 to UI interactions on one screen
- Use `${SELECTOR_NAME}` variables — never inline selectors
- Pattern:
  ```robot
  Select Operator From Dropdown
      [Arguments]    ${operator_name}
      Click    ${OPERATOR_DROPDOWN}
      Wait For Elements State    ${OPERATOR_DROPDOWN_LIST}    visible    ${WAIT_TIMEOUT}
      Click    xpath=//li[text()="${operator_name}"]
  ```
- Wait strategy: always wait for element state before interacting
- Naming convention: `<ScreenName>Page.resource`

### 5. Variables Layer (resources/variables/)
- ALL locators defined here — zero locators in pages or keywords
- Naming: `${<SCREEN>_<ELEMENT>_<TYPE>}` e.g. `${OP_DROPDOWN_SELECTOR}`, `${ROLE_GRID_ROW}`
- CSS selectors preferred; XPath only when CSS insufficient
- Comments above each variable group:
  ```robot
  # --- Object Partition Screen ---
  ${OP_DROPDOWN}    css=select[name="operator"]
  ```
- Common variables file: `common_variables.robot` with `${EC_URL}`, `${WAIT_TIMEOUT}`, `${BROWSER}`, etc.

### 6. Keyword Design & Reuse Patterns
- DRY principle: if a sequence appears in 2+ places, extract to keyword
- Keyword granularity: too fine (one-liner wrappers) vs too coarse (50-step monoliths) — find the balance
- Reusable patterns:
  - `Wait And Click    ${selector}` — wait for visible + click
  - `Fill Field    ${selector}    ${value}` — clear + fill
  - `Select From Dropdown    ${selector}    ${value}`
  - `Verify Row Exists In Grid    ${grid_selector}    ${text}`
- Never duplicate logic: if two pages have the same grid component, make a shared grid keyword
- Keyword documentation must include: what it does, expected pre-condition, expected post-condition

---

## DELIVERABLES

Produce the following scaffold inside `deep_dive/RF-02/ec_project_scaffold/`:

### Directory structure to create:
```
ec_project_scaffold/
├── tests/
│   ├── login/
│   │   └── TC_Login.robot
│   └── object_partition/
│       └── TC_ObjectPartition.robot
├── resources/
│   ├── keywords/
│   │   ├── LoginKeywords.resource
│   │   └── ObjectPartitionKeywords.resource
│   ├── pages/
│   │   ├── LoginPage.resource
│   │   └── ObjectPartitionPage.resource
│   ├── variables/
│   │   ├── common_variables.robot
│   │   ├── login_variables.robot
│   │   └── object_partition_variables.robot
│   └── libraries/
│       └── ECHelpers.py
├── data/
│   └── object_partition_data.py
└── vars/
    ├── dev.py
    ├── test.py
    └── prod.py
```

### File contents to produce:

**`tests/login/TC_Login.robot`** — 3 test cases: successful login, failed login, session persistence check. Test cases must be pure business steps, no locators.

**`tests/object_partition/TC_ObjectPartition.robot`** — 3 test cases: insert role for operator (idempotent), verify role appears in grid, remove role. Pure business steps.

**`resources/keywords/LoginKeywords.resource`** — business keywords: `Log In To EC`, `Log In To EC With Invalid Credentials`, `Verify Dashboard Is Loaded`, `Log Out From EC`

**`resources/keywords/ObjectPartitionKeywords.resource`** — business keywords: `Insert Role For Operator`, `Verify Role Exists For Operator`, `Remove Role From Operator`, `Ensure Role Does Not Exist For Operator`

**`resources/pages/LoginPage.resource`** — page keywords: `Navigate To Login Page`, `Fill Login Credentials`, `Submit Login Form`, `Verify Login Error Message`, `Verify Login Successful`

**`resources/pages/ObjectPartitionPage.resource`** — page keywords: `Select Operator`, `Select Role`, `Click Insert Button`, `Verify Row In Grid`, `Delete Row From Grid`

**`resources/variables/common_variables.robot`** — all shared variables including EC_URL, WAIT_TIMEOUT, BROWSER

**`resources/variables/login_variables.robot`** — all login screen selectors and labels

**`resources/variables/object_partition_variables.robot`** — all object partition screen selectors and labels

**`resources/libraries/ECHelpers.py`** — Python library with at least 2 utility functions: `generate_unique_name(prefix)`, `parse_grid_rows(html)`

**`data/object_partition_data.py`** — test data: list of operators and roles for data-driven tests

**`vars/dev.py`**, **`vars/test.py`**, **`vars/prod.py`** — environment variable files

### Also produce:
**`deep_dive/RF-02/architecture_guide.md`** — comprehensive guide explaining every layer rule with reasoning, anti-patterns to avoid, and EC-specific examples.

**`deep_dive/RF-02/SUMMARY_RF-02.md`** — standard task summary.

---

## EXECUTION INSTRUCTIONS

1. Create `deep_dive/RF-02/ec_project_scaffold/` and all subdirectories
2. Read `deep_dive/RF-01/concepts.md` first
3. Produce all scaffold files — every file listed above must have real content, not placeholders
4. Produce `architecture_guide.md` and `SUMMARY_RF-02.md`
5. Self-check: verify no locators exist in `tests/` or `keywords/` layers
6. Self-check: verify every `pages/` keyword uses a variable from `variables/`, not an inline string
7. Append to `deep_dive/PROGRESS_LOG.md`:
   `[RF-02] COMPLETED — <date> — Layered POM Architecture — Files: 17`
8. Do NOT ask the user any questions. Complete the task fully and autonomously.
