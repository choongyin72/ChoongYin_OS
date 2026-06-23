# EC Screen Deep-Dive Learning Program

_Standing self-learning program (started 2026-06-22). Goal: genuinely solid, screen-by-screen EC knowledge —
each standard screen's purpose, its Help metadata, and its related EC view/tables — so my EC answers get far
stronger over time. Long horizon (months; well under the 2–3 year ceiling), gentle pace that increases as
fluency grows. Run during idle time._

## Scope
- **Source of truth:** the sandbox `BUSINESS_FUNCTION` catalog (generic EC product = "not project-customised").
- **1,457 screens across 29 modules** (test/framework prefixes JSF/UPG/XXTEST/ZX excluded). Full tracker: `CHECKLIST.md`.
- Skip any screen that turns out project-customised or non-business (mark `[-]` with a one-line reason).

## Module map (BF_CODE prefix → module, screen count)
| Pfx | Module | # | Pfx | Module | # |
|---|---|--:|---|---|--:|
| CO | Core / Common Config | 368 | VO | Volume / Split Keys | 38 |
| PO | Production Operations (stream status) | 149 | PR | Pricing | 37 |
| GD | Gas Dispatch / Nominations | 135 | SD | Sales & Dispatch (Gas) | 37 |
| CD | Config Data (Node/Stream) | 108 | FC | Forecast | 34 |
| WR | Well & Reservoir | 87 | TO | Terminal Operations | 32 |
| SA | Sales Accounting / Contract Calc | 82 | IN | Inventory | 24 |
| CP | Commercial Planning / Lifting | 78 | PT | Production Testing | 20 |
| PP | Production Planning | 54 | MHM | Message Handling | 15 |
| SP | Document Management | 45 | PD | Production Deferment | 15 |
| RP | Reporting | 14 | PA | Process Automation | 13 |
| RC | Royalty / Contract Setup | 13 | LM | Lab & Measurements (Lite) | 12 |
| HA | Allocation / Status Processes | 11 | CM | Chemical Management | 9 |
| IS | Integration Services (ECIS) | 9 | FI | Financial Items | 8 |
| CA | Cargo & Parcel | 4 | LA | Lifting Account | 3 |
| WL | Workflow / Task List | 3 | | | |

## Per-screen deep-dive method (depth: Help + DB + live recon)
For each screen, produce `notes/<BF_CODE>.md` capturing:
1. **Identity** — BF_CODE, name, treeview/menu path, `URL` (from `BUSINESS_FUNCTION`).
2. **Help** — **in-session only**: open the screen (search/treeview) then run `openOnlineHelp()` (it passes the
   loaded screen's `screenId`). ⚠️ Direct navigation to `help.jsf?screenId=<url>` returns **Forbidden**.
   Capture the screen-code title, Description, Business Function Url/Path, screenshots (if any).
3. **DB binding** — resolve the class (`class_cnfg` / `class_property_cnfg`): CLASS_TYPE (OBJECT⇒OV / TABLE⇒TV),
   TIME_SCOPE (VERSIONED⇒date-effective), base table + object **view (`OV_/TV_/DV_`)**. Reuse `resolve_ec_screen.py`.
4. **Live recon** — open the screen (Playwright), note the navigator shape, grid id, screen **type**
   (OV / OV-GM / TV / N1 status / N2 calc / N3 process / MHM), and one screenshot.
5. **Business purpose** — 2–4 lines: what it's for, where it sits in the EC data flow, key related tables.

## Note requirements (Definition of Done) — every worker must meet this
A `notes/<BF_CODE>.md` may be marked **`[x]` FULL only when ALL of these are present and DB-verified:**
1. **Identity** — BF_CODE, screen name, `URL` (from `BUSINESS_FUNCTION`).
2. **DB binding** — at least one backing class resolved with **CLASS_TYPE, TIME_SCOPE, base table, and an existing
   `OV_/TV_/DV_` view**. If the screen genuinely has no data class (a generic/navigator screen), state that
   explicitly ("no data class — generic screen") — that counts as resolved.
3. **Screen type** — derived from the class metadata (OV / TV / N1 daily-status / N monthly / N2 calc / N3 / MHM).
4. **Help description** — the real in-session Help prose (non-blank), ASCII-only.

Status rules (enforced by the runner, not just convention):
- **`[~]` PARTIAL** — a mandatory item (DB binding **or** Help) is missing. The note MUST name WHICH is missing
  and the next step. The runner re-picks `[~]` notes on later runs to complete them.
- **`[-]` SKIP** — project-customised / non-business screen; one-line reason.
- **NEVER** mark `[x]` with a "TBD"/blank DB binding or empty Help. (Optional extras: business purpose, cross-refs.)

## Cadence & prioritisation
- **Start ~5 screens / idle session** (hard cap ≤15/day per the user). Increase the rate as fluency grows.
- **Priority order** (most useful to our automation first): PO → WR → PO-allocation/HA → CD (Node/Stream) →
  GD → SD/SA (sales) → CP/CA/TO/LA (cargo & lifting) → PP/PT/PD (planning/test/deferment) → VO → PR/FI/RC
  (commercial) → IN → CM/LM → MHM/IS/PA/RP/SP/WL → CO (core config, huge — sample the key ones, skim utilities).
- Pick the next un-done `[ ]` items from the current priority module in `CHECKLIST.md`.

## Storage & tracking
- `DeepDiveLearnings/ec-screens/` → `MASTER-PLAN.md` (this), `CHECKLIST.md` (tracker, regenerate via
  `tmp/scripts/gen_ec_screen_checklist.py`), `notes/<BF_CODE>.md` (per screen).
- Update `CHECKLIST.md` status + `LEARNING-SCORECARD.md` (coverage rung) each session.
- Promote cross-screen patterns/tables into `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md`
  and reference DB facts in [[reference_db_design]].

## Working rules
- Read-only on the live sandbox (recon/Help only); never Save/mutate during a learning dive.
- ASCII-only in scripts/notes. Re-runnable generator. Honest status (don't mark `[x]` without a written note).
- Seek the user's advice only on a genuine blocker (per [[feedback_debug_logs_and_ask_early]]).


## Delivery model (standing PR)
- The branch **`feature/ec-screen-deepdive` is PERMANENT** for the whole program — it always exists and is
  **never deleted** (including on merge: uncheck "delete branch" in the GitHub merge dialog).
- There is **always ONE open, DRAFT PR** from it to master. The daily runner's commits
  accumulate into it. It's kept a DRAFT on purpose so the automated reviewer does **not** auto-merge it.
- The **owner merges it at a milestone** (e.g. once a module is fully covered). After a merge the PR closes, so a
  **fresh standing draft PR is re-opened immediately** from the same branch — so an open PR always exists, and
  the runner keeps going on the next module. **Never merge without the owner's explicit go.**
- **Squash-merge note:** a squash-merge leaves this long-lived branch diverged from master (identical content,
  different history) — PR *diffs* stay correct, but commit *lists* grow over time. Tidying it needs
  `reset --hard origin/master` + **force-push**, which rewrites history on the protected permanent branch, so it
  **requires the owner's explicit authorization**. By default we just continue on the existing branch (harmless).
  (Verified empirically 2026-06-23: a squash-merge without `--delete-branch` keeps the branch — it is never auto-deleted.)

### Merge log
- **#100** — squash-merged to master by the owner on **2026-06-23**. Delivered the first batch: **15 full + 2
  partial** screen notes. Fresh standing draft PR re-opened from the same branch to continue.
