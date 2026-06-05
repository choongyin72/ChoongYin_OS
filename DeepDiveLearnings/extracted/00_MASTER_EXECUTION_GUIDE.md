# DEEP DIVE LEARNING — MASTER EXECUTION GUIDE

## Overview

This folder contains 12 Claude Code execution prompts for a self-directed deep-dive learning session covering:
- JasperReports 7.0.3+ (4 tasks)
- Playwright (4 tasks)
- Robot Framework (4 tasks)

Each task runs **fully autonomously** — Claude Code works without supervision, produces output files, and writes a summary + progress log entry on completion.

---

## How To Run

### Step 1 — Prepare your workspace
In Claude Code, navigate to the root folder where you want all learning output to land.
All output will be created inside a `deep_dive/` subfolder with one subfolder per task.

### Step 2 — Run one task at a time
Copy the full contents of one prompt file and paste it into Claude Code.
Claude Code will:
1. Execute the learning task autonomously
2. Produce all required files in `deep_dive/<TASK_ID>/`
3. Write a summary to `deep_dive/<TASK_ID>/SUMMARY_<TASK_ID>.md`
4. Append a line to `deep_dive/PROGRESS_LOG.md`

### Step 3 — Check the progress log
After each task, verify `deep_dive/PROGRESS_LOG.md` has a new entry.
Review the summary file to confirm quality before proceeding.

### Step 4 — Run the next task
Each task reads the previous task's summaries as context before starting.
Always run in the order listed below.

### Step 5 — Final check
After RF-04 completes, check `deep_dive/MASTER_SUMMARY.md` for the overall learning assessment.

---

## Task Execution Order

| # | File | Task | Tool | Expected Files |
|---|------|------|------|---------------|
| 1 | `JR-01_Fundamentals.md` | Core JRXML structure, band anatomy, v7.0.3 syntax, font mapping | JasperReports | 4 |
| 2 | `JR-02_Data_and_Expressions.md` | Data sources, expression language, variables, groups | JasperReports | 5 |
| 3 | `JR-03_Advanced_Layout.md` | Subreports, crosstabs, charts, export config | JasperReports | 6 |
| 4 | `JR-04_Production_and_Patterns.md` | REST API, pitfalls, best practices, Claude Code patterns | JasperReports | 7 |
| 5 | `PW-01_Fundamentals.md` | Architecture, installation, locators, actions, assertions | Playwright | 5 |
| 6 | `PW-02_Auth_and_Network.md` | Auth sessions, SSL certs, network interception, screenshots | Playwright | 6 |
| 7 | `PW-03_Advanced_and_MCP.md` | POM, MCP integration, trace viewer, parallel execution | Playwright | 7 |
| 8 | `PW-04_Production_and_Patterns.md` | EC patterns, pitfalls, CI workflow, Claude Code patterns | Playwright | 7 |
| 9 | `RF-01_Fundamentals.md` | Architecture, .robot file anatomy, Browser Library, EC conventions | Robot Framework | 5 |
| 10 | `RF-02_Layered_POM_Architecture.md` | 5-layer POM scaffold, keyword design, variable layer | Robot Framework | 17 |
| 11 | `RF-03_Advanced_Patterns.md` | ROBOT_CLAUDE.md, idempotency, Pabot, Robotidy, Robocop | Robot Framework | 6 |
| 12 | `RF-04_Production_and_Patterns.md` | Environment switching, daily workflows, Claude Code patterns | Robot Framework | 7 |

**Total expected files produced: ~82 files across 12 task folders**

---

## Output Structure (after all tasks complete)

```
deep_dive/
├── PROGRESS_LOG.md              ← One line per completed task
├── MASTER_SUMMARY.md            ← Overall learning assessment (created by RF-04)
│
├── JR-01/                       ← JasperReports Fundamentals
│   ├── annotated_template.jrxml
│   ├── concepts.md
│   ├── compliance_checklist.md
│   └── SUMMARY_JR-01.md
│
├── JR-02/                       ← Data Sources & Expressions
│   ├── data_sources_guide.md
│   ├── expressions_guide.md
│   ├── working_report_sql.jrxml
│   ├── working_report_csv.jrxml
│   └── SUMMARY_JR-02.md
│
├── JR-03/                       ← Advanced Layout
│   ├── advanced_layout_guide.md
│   ├── master_with_subreport.jrxml
│   ├── subreport_detail.jrxml
│   ├── crosstab_report.jrxml
│   ├── export_config_reference.md
│   └── SUMMARY_JR-03.md
│
├── JR-04/                       ← Production & Claude Code Patterns
│   ├── rest_api_guide.md
│   ├── compile_preview_patterns.md
│   ├── pitfalls_and_troubleshooting.md
│   ├── best_practices.md
│   ├── claude_code_patterns_JR.md
│   ├── JasperReports_Cheatsheet.md
│   └── SUMMARY_JR-04.md
│
├── PW-01/                       ← Playwright Fundamentals
│   ├── concepts.md
│   ├── starter_test.spec.ts
│   ├── playwright.config.ts
│   ├── locator_reference.md
│   └── SUMMARY_PW-01.md
│
├── PW-02/                       ← Auth Sessions & Network
│   ├── auth_guide.md
│   ├── network_guide.md
│   ├── globalSetup.ts
│   ├── auth_test.spec.ts
│   ├── network_test.spec.ts
│   └── SUMMARY_PW-02.md
│
├── PW-03/                       ← Advanced Patterns & MCP Integration
│   ├── pom_architecture_guide.md
│   ├── LoginPage.ts
│   ├── ObjectPartitionPage.ts
│   ├── mcp_integration_guide.md
│   ├── trace_debug_guide.md
│   ├── parallel_execution_guide.md
│   └── SUMMARY_PW-03.md
│
├── PW-04/                       ← Playwright Production
│   ├── ec_patterns_guide.md
│   ├── pitfalls_and_troubleshooting.md
│   ├── ci_workflow.yml
│   ├── best_practices.md
│   ├── claude_code_patterns_PW.md
│   ├── Playwright_Cheatsheet.md
│   └── SUMMARY_PW-04.md
│
├── RF-01/                       ← Robot Framework Fundamentals
│   ├── concepts.md
│   ├── starter_test.robot
│   ├── ec_variables.py
│   ├── browser_library_reference.md
│   └── SUMMARY_RF-01.md
│
├── RF-02/                       ← Layered POM Architecture
│   ├── architecture_guide.md
│   ├── ec_project_scaffold/     ← Full 17-file project scaffold
│   └── SUMMARY_RF-02.md
│
├── RF-03/                       ← Advanced Patterns
│   ├── ROBOT_CLAUDE.md          ← ★ KEY FILE — copy to project root when ready
│   ├── idempotency_patterns.robot
│   ├── advanced_teardown_example.robot
│   ├── pabot_guide.md
│   ├── linting_guide.md
│   └── SUMMARY_RF-03.md
│
└── RF-04/                       ← Robot Framework Production
    ├── environment_switching_guide.md
    ├── daily_workflow_patterns.md
    ├── pitfalls_and_troubleshooting.md
    ├── best_practices.md
    ├── claude_code_patterns_RF.md
    ├── RobotFramework_Cheatsheet.md
    └── SUMMARY_RF-04.md
```

---

## Key Output Files (Most Valuable)

After completion, these are the files you will use most in daily work:

| File | Purpose | Location |
|------|---------|----------|
| `ROBOT_CLAUDE.md` | Governs ALL Robot Framework Claude Code generation | `RF-03/` → copy to project root |
| `claude_code_patterns_RF.md` | Paste-ready prompts for daily Robot Framework work | `RF-04/` |
| `claude_code_patterns_PW.md` | Paste-ready prompts for daily Playwright work | `PW-04/` |
| `claude_code_patterns_JR.md` | Paste-ready prompts for daily JasperReports work | `JR-04/` |
| `JasperReports_Cheatsheet.md` | Dense JRXML reference | `JR-04/` |
| `Playwright_Cheatsheet.md` | Dense Playwright API reference | `PW-04/` |
| `RobotFramework_Cheatsheet.md` | Dense Robot Framework reference | `RF-04/` |
| `compliance_checklist.md` | Validate any JRXML for v7.0.3 compliance | `JR-01/` |
| `ec_project_scaffold/` | Ready-to-use layered POM project structure | `RF-02/` |
| `MASTER_SUMMARY.md` | Overall learning assessment + next steps | `deep_dive/` root |

---

## Notes

- **Do not skip tasks** — each task reads the previous task's output as context
- **Do not run tasks in parallel** — sequential dependency is intentional
- **Time estimate**: each task may take 5–20 minutes of Claude Code execution time
- **If a task fails mid-way**: re-run the same prompt — Claude Code will overwrite partial output
- **PROGRESS_LOG.md** is your audit trail — if it's missing an entry, that task may not have completed cleanly
