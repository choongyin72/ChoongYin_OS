# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — County
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-11 (v1.0), updated 2026-08-23/24 (v2.0 — Bank-pattern conversion), backfilled 2026-08-28
**Version:** 2.0 — CURRENT: RF suite = Bank pattern (label-driven, properties-file-driven, T2-consolidated,
pure screen-verify). Sections below marked v1.0 describe the ORIGINAL 2026-06-11 build, superseded by
the conversion — kept for history, not the live shape.

---

## 0. CLASSIFICATION (current, v2.0 — read this first)
| Property | Value |
|---|---|
| Pattern | **Bank pattern**, plain OV (manage-object), **no navigator section** — same shape as Bank/State |
| Screen type | Manage Object (OV), date-effective |
| Navigator | None (Date filter + GO only, confirmed live — no mandatory dropdown) |
| Grid id | `manage_object_nav_nav:form:T_data` |
| DB view (ground truth) | `OV_COUNTY` |
| Field labels | **Screen-prefixed**: "County Code" / "County Name" (NOT generic "Code"/"Name" — same as State/Region) |
| Mandatory fields (Insert) | County Code, County Name, Start Date (confirmed live via `MandatoryCellStyle`) |
| Non-mandatory fields present | Master System Code/Name (read-only display), Description, API Code, State dropdown — left unset per IUD-fill-only-needed-fields convention |
| Delete semantics | End Date = Start Date (true delete from `OV_COUNTY`) |
| Fixed test code | `AUTOTEST_COUNTY` (matches Account/Bank convention) |
| Grid-filter wiring | Explicit, included from the conversion (`Find/Clear County Row By Filter`) |
| DB-verify style | **Pure screen-verify** (matches Bank's owner-requested 2026-08-18 convention) — no inline DB-read keyword in the .robot suite itself; DB ground-truth is asserted via the shared T2 layer + a fresh-connection post-run check, not an in-suite `DbVerify` call |

## Dev story (real, from PR history — not invented)
- **2026-06-11** — original build (v1.0 below): old hardcoded-field-id Playwright + RF pair, Basic Objects section (12 screens).
- **2026-08-23, PR #429** ("County IUD suite - Bank-pattern conversion (batch-2)") — converted `county_page.resource`
  (T3) and `county_iud.robot` from the hardcoded-field-id pattern to the label-driven, properties-file-driven,
  T2-consolidated Bank pattern, alongside Country/Regulatory Permits/Currency/VAT Code in parallel isolated
  worker clones (`tmp/batch2_shared_findings.md`). Real gotcha hit during this build: County Code/County Name
  are screen-prefixed labels (not generic "Code"/"Name"), same as State — threaded `code_label=County Code`
  through every T2 call. Also confirmed the `objectdates` Delete field id
  (`tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`) via a live insert+delete probe round-trip before
  hardcoding it. Live run: 5/5 pass; DB self-clean confirmed 0 residual `AUTOTEST%` rows in `OV_COUNTY` via a
  fresh oracledb connection; grid-filter wiring confirmed fired 5x in output.xml.
- **2026-08-24, PR #489** ("align County suite to Bank's exact pure-screen-verify pattern") — a smaller,
  targeted fix, not a rebuild. Owner asked why `county_iud.robot` differed from `bank_iud.robot`; direct
  file comparison found County still had two extra inline DB-verify keywords (`County Should Exist In DB`,
  `County Should Be Updated In DB`) that `bank_iud.robot` deliberately does not carry (owner decision
  2026-08-18: "PURE SCREEN verification... no DB check at all here"). Removed both — the T2-delegated
  `Verify County Record Exists`/`Verify County Record Updated` already provide full screen-level
  verification, so removing the duplicate DB reads did not reduce real coverage. Re-verified: dryrun
  792/792 pass (full tree), live 5/5 pass, DB self-clean via fresh oracledb connection = 0 `AUTOTEST%` rows.

---

## v1.0 (original, 2026-06-11) — SUPERSEDED, kept for history

## 1. REQUIREMENT
Automate Insert / Update / Delete on the **County** screen and prove, at DB level,
that EC creates, modifies and truly deletes the record. Constraints: NEVER touch
existing data; all test data prefixed `AUTOTEST_CNTY_`; environment = local EC
sandbox (`ap-f0a7g341jn6d`), user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_COUNTY` | PASS |
| UPDATE | Name change visible in grid row | PASS |
| DELETE | End Date = Start Date -> gone from grid AND absent in `OV_COUNTY` | PASS |
| CLEANUP | zero leftover test data | PASS |

## 2. DESIGN

### 2.1 Screen classification
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Basic Objects > County |
| Screen type | Manage Object (OV) |
| List/grid id | `manage_object_nav_nav:form:T_data` |
| DB view (ground truth) | `OV_COUNTY` |
| Delete semantics | End Date = Start Date (true delete) |

### 2.2 Screen-specific notes
ROW-SHIFT screen like State: County Code/Name at R2/R3; dates R5/R6; State dropdown (R8) optional.

### 2.3 DOM reference (from recon)
```
INSERT objectForm : Code  tab:tabPanel:objectForm:form:G:0:R:2:C:1:in
                    Name  tab:tabPanel:objectForm:form:G:0:R:3:C:1:in
                    Start tab:tabPanel:objectForm:form:G:0:R:5:C:1:da_input
UPDATE            : Code  tab:tabPanel:updateAttributes:form:G:0:R:2:C:1:in (guard)
                    Name  tab:tabPanel:updateAttributes:form:G:0:R:3:C:1:in
DELETE objectdates: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

### 2.4 Test data
| Field | Value |
|---|---|
| Code | `AUTOTEST_CNTY_<timestamp>` (fresh per run — deleted codes linger in the base table) |
| Name / Name (update) | `County <code>` / `County <code> UPD` |
| Start = End (delete) | `2000-01-01` |

## 3. DEVELOPMENT — what it took (2026-06-11 session)
The screen was recon'd with the scripts preserved in `investigation/` (full-section
recon + label/mandatory mapping; per-screen probes where the first live run failed).
Key phase findings that shaped this screen's automation:
- Same as State: ids derived from insert order, proven live.

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF dryrun (structure) | headless | PASS |
| RF live batch | headless | TC01–TC04 4/4 PASS, DB-verified |
| RF demo | HEADED (watched) | 4/4 PASS |
| Playwright reference run | headless | see `evidence/county_results.json` |

Evidence screenshots in `evidence/` (loaded / clean / insert / update / delete steps).

## 5. DELIVERABLES
| Deliverable | Where |
|---|---|
| RF suite (maintained test) | `tests/Configuration/Assets/Basic_Objects/county_iud.robot` |
| RF page object | `pageobjects/Configuration/Assets/Basic_Objects/county_page.resource` |
| Playwright reference | `playwright/ec_iud_county.py` (+ `_shared/iud_engine.py`) |
| Recon trail | `investigation/` |
| Registry row | `docs/ec_screen_registry.md` |

## 6. LESSONS LEARNED (section-wide, applied here)
1. **Silent reject = mandatory field**: a Save that produces no row + the banner
   "Required fields are empty: <field>" — fill the named dropdown.
2. **Code/Name rows are NOT always R0/R1** — recon the `:C:0:la` labels first
   (State/County have Master System rows above them).
3. **Form dropdowns are effective-date-filtered** — only objects valid at the form's
   Start Date are offered.
4. **Dropdown labels may carry leading/double spaces** in seed data — match with
   normalize-space.
5. **The UI can lie**: groupmodel grids redraw lazily; ALWAYS verify at the DB.
