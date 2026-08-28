# EC Screen IUD — Statement of Work: **Transport Zone**
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Original build:** pre-existing RF automation (older 4-TC/suite-login/generated-code/inline-DB-verify pattern)
**Converted:** `ec-area-pattern-converter` skill — PR #557, merged 2026-08-26
**Backfilled:** `docs/lean-deliverable-backfill-workorder.md`, Batch 5 — 2026-08-28 (see §3.2, §5)
**Result:** COMPLETE — live **5/5 PASS** (Area-pattern, TC01-TC05), DB-verified, self-cleaning (0 residue)

---

## 1. REQUIREMENT / METADATA
| Property | Value | Source |
|---|---|---|
| Screen | **Transport Zone** | input |
| Treeview path | **Configuration > Assets > Dispatching Objects > Transport Zone** | `docs/ec_screen_registry.md` |
| Class type | OV-GM (Business-Unit-gated manage-object groupmodel) | registry + `transport_zone_page.resource` Documentation |
| Time scope | date-effective ⇒ **DELETE = End Date = Start Date** | registry, PR #557 body |
| Verify view | `OV_TRANSPORT_ZONE` | `libraries/DbVerify.py` usage in the suite (`Verify Object Removed ... OV_TRANSPORT_ZONE`) |
| Family | **OV-GM, single-mandatory-Business-Unit-dropdown** — same shape as Area's own Production Unit navigator / Pipeline Segment's own Business Unit navigator | registry row |

## 2. LIVE RECON (as re-confirmed live 2026-08-26, per PR #557)
**Navigator** — the grid stays empty until a Business Unit is chosen + GO. The navigator group
`nav:form:G:0` has **three columns**:
| Element | Locator | Mandatory |
|---|---|---|
| Nav Date | `nav:form:G:0` C:0 | mandatory:true but ALREADY defaulted/filled on load — no fill needed |
| **Nav Business Unit** (dd) | `nav:form:G:0` C:1 | **yes** — genuinely empty, `MandatoryCellStyle`, the ONLY field needing a fill |
| Nav 2nd dropdown (filter) | `nav:form:G:0` C:2 | no — `mandatory:false`, confirmed live; GO succeeds with C:2 left empty once C:1 is set |
| Grid | `manageObject:form:T_data` | — |

This is exactly the single-dropdown/same-row-cascade shape Area's pattern supports — FITS, no
shared-file change needed (defaults row=1/group G:0/start_col=C:1 already match).

**Insert (`objectForm`) — fields, screen-prefixed labels confirmed live:**
| Field | Mandatory |
|---|---|
| Transport Zone Code | **yes** |
| Transport Zone Name | **yes** |
| Start Date | **yes** |
| Transport System Name (dd, R:5) | **yes** — bound to the nav Business Unit scope ("TS5 Transport System" pairs with nav "TS5 BU") |
| Zone Type (R:2) | no — confirmed `mandatory:false`, deliberately excluded |
| End Date (R:4) | no — confirmed `mandatory:false`, deliberately excluded |

**Update (`updateAttributes`):** Transport Zone Name only (Transport Zone Code is read-only in `updateAttributes`).
**Delete (`objectdates`):** End Date `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` = Start Date ⇒ true delete from `OV_TRANSPORT_ZONE`.

**Test data used (unchanged, reused not reinvented):**
- Fixed test code `AUTOTEST_TRANSPORT_ZONE` (confirmed absent from `OV_TRANSPORT_ZONE` via a fresh independent oracledb connection before the PR #557 build).
- Business Unit navigator scope: `TS5 BU`.
- Insert Transport System Name dropdown value: `TS5 Transport System` (paired with the TS5 BU scope).
- Start Date `2003-01-01`.

## 3. IUD DESIGN (pre-existing, structurally converted by PR #557)
```
SETUP : Open EC Screen -> Apply Navigator From Properties (Business Unit = TS5 BU) -> GO
INSERT: New Object -> Transport Zone Code/Name/Start Date + Transport System Name = TS5 Transport System -> Save -> GO
UPDATE: select row by code -> updateAttributes Transport Zone Name -> Save -> GO
FIND  : filter grid by code -> compare grid + form record
DELETE: select row -> objectdates End Date = Start Date -> Save -> GO
```

## 3.2 AREA-PATTERN CONVERSION (PR #557, merged 2026-08-26)
Converted the RF automation from the OLD 4-TC/suite-login/generated-code/inline-DB-verify shape to
the full Area-pattern structure (real PR #557 body):
- Live recon (read-only, no Save/Insert/Delete) confirmed the navigator group `nav:form:G:0` has 3
  columns as detailed in §2 — exactly ONE genuinely mandatory+empty field (C:1 Business Unit).
  Confirmed the single-dropdown/same-row-cascade fit — no shared-file change needed to
  `resources/manage_object.resource`'s `Apply Navigator From Properties` (defaults row=1/group
  G:0/start_col=C:1 already match this screen).
- 5 TCs (added TC04 Find), per-TC Login/Logout, fixed test code `AUTOTEST_TRANSPORT_ZONE`.
- Navigator filled via the shared T2 `Apply Navigator From Properties`, driven by
  `testdata/transport_zone_navigator.properties`.
- Properties-file-driven insert/update/verify
  (`testdata/transport_zone_{insert,update,form_verify,grid_verify}.properties`).
- Dedicated credentials pair `TRANSPORT_ZONE_EC_USER`/`TRANSPORT_ZONE_EC_PASS` added to
  `resources/credentials.py` (additive only).
- Explicit `Find/Clear Transport Zone Row By Filter` wired into Update/Find/Verify-Found/Delete.
- Zero inline DB-verify calls in the `.robot` file (pure-screen verification; the one DB check —
  `Verify Object Removed ... OV_TRANSPORT_ZONE` — lives inside the shared T2 keyword).
- Field labels confirmed screen-prefixed live: "Transport Zone Code"/"Transport Zone Name" (like
  Area's "Area Code"/"Area Name"), NOT the generic "Code"/"Name" Bank/Object List use.
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows
  MODIFIED in place; new R38 sections added to `docs/bank-pattern-conversion-checklist.md` and
  `docs/grid-filter-standardization-checklist.md` (per PR #557's own "Files touched" list).
- No shared T1/T2 file changes — PR #557's body confirms `resources/manage_object.resource` was
  untouched, the existing `Apply Navigator From Properties` defaults already fit this screen.
- Isolated worktree used (`/tmp/wt-transportzone`) at build time to avoid cross-contaminating
  commits with unrelated concurrent in-progress work (Pilot/Contract Inventory/Property
  conversions found uncommitted in the shared main checkout at that time) — disclosed in PR #557's
  own "Rules applied" section.

## 4. ISSUE FOUND & FIXED
No new issue found or fixed by PR #557 itself — the conversion was structural (navigator
mandatory/optional classification was confirmed live via DOM class inspection — `MandatoryCellStyle`
vs `mandatory:false` — not assumed from the pre-existing registry note; insert/update/delete
gestures were re-confirmed to behave exactly as the pre-existing driver already documented).

This backfill (2026-08-28) hit no new issue on the fresh dryrun/live re-run — see §5 for the actual
result (retry needed, per the process rule in this task, disclosed honestly if hit).

## 5. EVIDENCE (DB ground truth)

### PR #557 conversion (2026-08-26, from its own PR body)
- Pre-build: fresh independent oracledb connection (DSN `localhost:1521/ORCL`) confirmed
  `AUTOTEST_TRANSPORT_ZONE` absent from `OV_TRANSPORT_ZONE` (count=0) and no residual `AUTOTEST%`
  rows before the build.
- Live run: `EC_HEADLESS=true robot tests/.../transport_zone_iud.robot` → **5/5 PASS** (TC01 Verify
  Clean State, TC02 Insert, TC03 Update, TC04 Find, TC05 Delete).
- Post-run: fresh independent oracledb connection confirmed 0 residual `AUTOTEST%` rows in
  `OV_TRANSPORT_ZONE`.
- Grid-filter keyword confirmed fired: `grep -c "Find Object Row By Filter" output.xml` → 15.
- Full `tests/` tree `robot --dryrun` → 875/875 pass, zero collisions.
- `py -m robocop check` on changed files → 10 issues (7 on
  `transport_zone_page.resource`/`transport_zone_iud.robot` = exact parity with
  `area_page.resource`/`area_iud.robot`'s own 7-issue baseline, confirmed by running robocop on
  Area's files directly; +3 pre-existing, unrelated `credentials.py` COM04/DOC03/MISC06 findings,
  confirmed pre-existing via `git stash`).

### This backfill (2026-08-28, `evidence/backfill_2026-08-28/`)
- Dryrun re-run of the already-proven suite alone: see `evidence/backfill_2026-08-28/dryrun/`.
- Live headless re-run: see `evidence/backfill_2026-08-28/live/` and JOURNAL.md/CHECKLIST.md for
  the exact pass count and any retry needed.
- Fresh independent oracledb connection re-read AFTER the live run, confirming self-clean.
- `py scripts/check_bundle_hygiene.py` (repo root) result.
- **No RF automation file was modified, rebuilt, or re-verified from scratch by this backfill** —
  confirmed via `git status`/`git diff --stat` against `pageobjects/`, `tests/`, `testdata/`,
  `resources/credentials.py`, `docs/ec_screen_registry.md` (no changes) before committing.

## 6. DELIVERABLES
| Deliverable | Path |
|---|---|
| T3 page object | `pageobjects/Configuration/Assets/Dispatching_Objects/transport_zone_page.resource` (Area-pattern shape, PR #557) |
| RF suite | `tests/Configuration/Assets/Dispatching_Objects/transport_zone_iud.robot` (5 TCs, PR #557) |
| Testdata | `testdata/transport_zone_{navigator,insert,update,form_verify,grid_verify}.properties` (PR #557) |
| Playwright bundle | N/A — permanently waived for Area-pattern work (Section H); none built by this backfill |
| Evidence | `screens/.../Transport_Zone/evidence/backfill_2026-08-28/` (this backfill's dryrun + live re-run) |
| JOURNAL / CHECKLIST | `JOURNAL.md`, `CHECKLIST.md` (added 2026-08-28 backfill) |
| KB selector map | `ec-ui-knowledge/screens/transport_zone.md` (added 2026-08-28 backfill) |
| Reuse | T2 `manage_object.resource` (incl. `Apply Navigator From Properties`) + T1 `common`/`table`/`navigator` (no shared-file changes by PR #557 or this backfill) |
