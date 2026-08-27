# EC Screen IUD — Statement of Work: **Contract Area**
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Built by:** ec-object-iud-builder skill (autonomous run) — 2026-06-18
**Converted:** ec-area-pattern-converter skill — PR #542, merged 2026-08-26 (see §3.2)
**Backfilled:** `docs/lean-deliverable-backfill-workorder.md`, Batch 2 — 2026-08-27 (see §3.2, §5)
**Result:** ✅ COMPLETE — live **5/5 PASS** (Area-pattern, TC01-TC05), DB-verified, self-cleaning (0 residue)

---

## 1. REQUIREMENT / METADATA (auto-derived from screen name)
| Property | Value | Source |
|---|---|---|
| Screen | **Contract Area** | input |
| Treeview path | **Configuration > Assets > Contract Objects > Contract Area** | tv-link `title=` (recon) |
| Class | `CONTRACT_AREA` | `class_property_cnfg.LABEL` |
| Class type | `OBJECT` ⇒ **OV (Manage-Object)** | `class_cnfg.CLASS_TYPE` |
| Time scope | `VERSIONED` ⇒ date-effective ⇒ **DELETE = End Date = Start Date** | `class_cnfg.TIME_SCOPE_CODE` |
| Base / version table | `CONTRACT_AREA` / `CONTRACT_AREA_VERSION` | `class_cnfg` |
| Verify view | `OV_CONTRACT_AREA` (29 seed rows) | resolver |
| App space | `EC_TRAN` | `class_cnfg` |
| Family | **OV-GM (Business-Unit-gated)** — sibling of Transport System / Nomination Point / Transport Zone | registry |

## 2. LIVE RECON (read-only scans)
**Navigator** — the grid stays empty until a Business Unit is chosen + GO:
| Element | Locator | Mandatory |
|---|---|---|
| Nav date | `nav:form:G:0:R:1:C:0:da_input` | optional |
| **Nav Business Unit** (dd) | `nav:form:G:0:R:1:C:1:dd` | **yes** |
| GO | `button:form:B` | — |
| Grid | `manageObject:form:T_data` (first column = Contract Area Code) | — |

**Insert — `objectForm` (New Object):**
| Field | Locator | Mandatory |
|---|---|---|
| Contract Area Code | `tab:tabPanel:objectForm:form:G:0:R:0:C:1:in` | **yes** |
| Contract Area Name | `tab:tabPanel:objectForm:form:G:0:R:1:C:1:in` | **yes** |
| Start Date | `tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input` | **yes** |
| End Date | `…R:3:C:1:da_input` | optional |
| Comments | `…R:4:C:1:in` | optional |
| **Business Unit Name** (dd) | `tab:tabPanel:objectForm:form:G:0:R:5:C:1:dd` | **yes** — must equal the nav BU or the row never appears in the filtered grid |
| Use as Property | `…R:6:C:1:cb` | optional |

**Update — `updateAttributes`:** Code `…R:0:C:1:in` (read-only), **Name `…R:1:C:1:in`** (edited).
**Delete — `objectdates`:** **End Date `…G:0:R:0:C:3:da_input`** ← set = Start Date ⇒ true delete from `OV_CONTRACT_AREA`.

**Scope chosen:** Business Unit **ECP Norway** (`ECP_NO`, 5 existing areas — most populated). Date `2003-01-01` (ref-dd screen, must post-date seed Business Units).

## 3. IUD DESIGN (clone of Transport System OV-GM pattern)
```
SETUP : open screen → Select EC Dropdown Option nav BU = ECP Norway → Apply Navigator (GO)
INSERT: New Object → Code/Name/Start Date + Business Unit Name = ECP Norway → Save → GO
UPDATE: select row by code → updateAttributes Name → Save → GO
DELETE: select row → objectdates End Date = Start Date → Save → GO (+1 extra GO; GM grid redraws lazily)
```
Test data: unique `AUTOTEST_CA_<YYYYMMDDHHMMSS>` per run (OV codes linger after delete — never reused). The referenced Business Unit is **read-only seed**; existing rows are never touched.

## 3.2 AREA-PATTERN CONVERSION (PR #542, merged 2026-08-26)
Converted the RF automation from the original 2026-06-18 bespoke-navigator/suite-login/4-TC
build to the full Area pattern, mirroring `area_page.resource`/`area_iud.robot` exactly (real PR
#542 body):
- 5 TCs (added TC04 Find) with **per-TC login/logout** (dedicated `CONTRACT_AREA_EC_USER`/
  `CONTRACT_AREA_EC_PASS` in `resources/credentials.py`), replacing suite-level login.
- Navigator fill delegated to the shared T2 **`Apply Navigator From Properties`**
  (`resources/manage_object.resource`, added 2026-08-26) driven by
  `testdata/contract_area_navigator.properties` — the genuine Business Unit + GO gesture was
  **kept**, not removed; this is a structural conversion, not a reclassification as plain
  Bank-shaped.
- Properties-file-driven insert/update/verify (`testdata/contract_area_{insert,update,
  form_verify,grid_verify}.properties`), replacing inline field fills.
- Explicit grid-filter wiring: `Find Contract Area Row By Filter`/`Clear Contract Area Row
  Filter` → shared T2 `Find/Clear Object Row Filter` (15 `Find Object Row By Filter` hits
  confirmed live via `output.xml` grep).
- Fixed test code `AUTOTEST_CONTRACT_AREA` (confirmed 0 rows in `OV_CONTRACT_AREA` before use),
  replacing the old per-run timestamped code.
- Zero inline DB-verify calls left in the `.robot`/`.resource` files — the screen-local
  `Contract Area Should Exist/Not Exist In DB` wrappers were removed; DB proof now comes solely
  from the shared T2 `Verify Object Removed` + the mandatory live-run self-clean check.
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows
  **modified in place**, not duplicated.

**Real incident disclosed at merge (branch-name collision):** PR #542 was raised from
`feature/contract-area-pattern-conversion`. A separate, parallel task converting the sibling
**Contract** screen (PR #546) was independently assigned the SAME branch name; that agent's
worktree was created from a point that already contained Contract Area's commit, and pushing
there silently appended the Contract commit on top of Contract Area's own commit on this
branch/PR. PR #546's own body disclosed this and stated its attempted force-push cleanup was
blocked by the environment's safety guardrail (no destructive rewrite of an already-published PR
branch without explicit authorization) — leaving a human/owner decision needed. The reviewer's
merge comment on PR #542 confirms the resolution: *"Before merging, I verified the
branch-collision cleanup #546 disclosed: this branch is back at its clean single Contract Area
commit (`1b0c874`), own 10 files only — the accidental Contract-commit append was fully undone on
the remote before review."* Contract Area's own conversion content was never at issue — only the
branch/PR was transiently affected, and it was clean again before merge.

## 4. ISSUE FOUND & FIXED (2026-06-18 original build)
**OV-GM grid redraws lazily after Save+GO.** First live run: insert *persisted* (update + delete + DB confirmed it) but `Row Should Exist` (T1, an *instant* DOM read) ran before the row rendered → false FAIL on TC02. TC03's `Click` auto-waited, so it found the row — masking the timing.
**Fix:** T3 `Contract Area Row Should Exist` now `Wait For Elements State … visible 20s` on the row span *before* the instant first-cell assertion. Screen-specific knowledge kept in T3; no shared-file change. Re-run → **4/4 PASS**.

## 5. EVIDENCE (DB ground truth)

### Original 2026-06-18 build
- **RF live (headed):** `tests/Configuration/Assets/Contract_Objects/contract_area_iud.robot` — **4/4 PASS** (`results/ca_live2/`).
  - TC02 in-suite assert: `Code Should Be Present In View    ov_contract_area    ${code}` → PASS
  - TC04 in-suite assert: `Code Should Be Absent In View     ov_contract_area    ${code}` → PASS
- **Playwright bundle:** `playwright/ec_iud_contract_area.py` — ALL PASS (`evidence/` 9 screenshots + result JSON).
- **Independent DB re-read:** `OV_CONTRACT_AREA` AUTOTEST residue = **0** (self-clean confirmed, twice).

### PR #542 Area-pattern conversion (2026-08-26)
- Live run (`EC_HEADLESS=true`): **5/5 PASS** (TC01-TC05).
- Pre-run fresh `oracledb` check: `SELECT COUNT(*) FROM OV_CONTRACT_AREA WHERE CODE =
  'AUTOTEST_CONTRACT_AREA'` → 0.
- Post-run independent fresh-connection re-check: `SELECT COUNT(*) FROM OV_CONTRACT_AREA WHERE
  CODE LIKE 'AUTOTEST%'` → **0 residual rows**.
- `robocop check` on the 2 changed files: 7 issues (2x VAR02 + 5x DOC02) — same count/kind as
  Area's own reference baseline.
- `robot --dryrun` on the full `tests/` tree: **851/851 PASS**.

### This backfill (2026-08-27, `screens/.../evidence/backfill_2026-08-27/`)
- Fresh dryrun re-run of the already-proven suite alone: **5/5 PASS**
  (`evidence/backfill_2026-08-27/dryrun/`).
- Fresh live headless re-run: **5/5 PASS** (`evidence/backfill_2026-08-27/live/`).
- Independent fresh `oracledb` connection, pre- and post-run: `OV_CONTRACT_AREA` `CODE =
  'AUTOTEST_CONTRACT_AREA'` → 0 both times; `CODE LIKE 'AUTOTEST%'` → no rows both times.
- `grep -c "Find Object Row By Filter" evidence/backfill_2026-08-27/live/output.xml` → 15
  (matches PR #542's cited count).
- `robocop check` on the 2 files re-run: 7 issues, same kind, cross-checked against
  `area_page.resource`/`area_iud.robot` (also 7) — parity confirmed independently.
- `py scripts/check_bundle_hygiene.py` (repo root) → `RESULT: PASS` (one unrelated WARN on an
  `investigation/` selector-string false positive, not a real credential).
- **No RF automation file was modified, rebuilt, or re-verified from scratch by this backfill** —
  confirmed via `git diff --stat` against `pageobjects/`, `tests/`, `testdata/`,
  `resources/credentials.py`, `docs/ec_screen_registry.md` (empty diff) before committing.

## 6. DELIVERABLES
| Deliverable | Path |
|---|---|
| T3 page object | `pageobjects/Configuration/Assets/Contract_Objects/contract_area_page.resource` (Area-pattern shape, PR #542) |
| RF suite | `tests/Configuration/Assets/Contract_Objects/contract_area_iud.robot` (5 TCs, PR #542) |
| Testdata | `testdata/contract_area_{navigator,insert,update,form_verify,grid_verify}.properties` (PR #542) |
| Playwright bundle | `screens/Configuration/Assets/Contract_Objects/Contract_Area/playwright/ec_iud_contract_area.py` (original 2026-06-18 build, permanently waived from re-verification — Section H) |
| Recon scripts | `…/Contract_Area/investigation/` (db / live / bu_distribution / treeview_path / grid_columns — original build, waived) |
| Evidence | `…/Contract_Area/evidence/` (original) + `evidence/backfill_2026-08-27/` (this backfill's dryrun + live re-run) |
| JOURNAL / CHECKLIST | `JOURNAL.md`, `CHECKLIST.md` (added 2026-08-27 backfill) |
| KB selector map | `ec-ui-knowledge/screens/contract_area.md` (added 2026-08-27 backfill) |
| Reuse | T2 `manage_object.resource` (incl. `Apply Navigator From Properties`, added 2026-08-26) + T1 `common`/`table`/`navigator` (no shared-file changes by PR #542 or this backfill) |
