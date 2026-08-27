# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Licence
**Author:** Choong-Yin Lee / Claude Fable 5 (original) — updated by Claude (backfill, 2026-08-28)
**Date:** 2026-06-12 (original) — updated 2026-08-27/28 (Bank-pattern conversion backfill, PR #438 + this bundle)
**Version:** 2.0 — Bank-pattern conversion (label-driven, properties-file-driven, T2-consolidated), documentation backfilled per `docs/lean-deliverable-backfill-workorder.md` Batch 6

---

## 1. REQUIREMENT
Automate IUD on the **Licence** screen with DB-level proof. Constraints: NEVER touch
existing data; fixed test code `AUTOTEST_LICENCE` (confirmed free in `OV_LICENCE` before
being wired in on the 2026-08-23 conversion); local sandbox, user `sysadmin` (screen also
carries its own dedicated `LICENCE_EC_USER`/`LICENCE_EC_PASS` credential pair per the
2026-08-22 standing decision that every EC screen gets its own credential pair).

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | `AUTOTEST_LICENCE` row in grid AND present in `OV_LICENCE` | PASS |
| UPDATE | Licence Name change visible in grid row + form | PASS |
| FIND | Grid + form both match expected post-update state | PASS |
| DELETE | End Date = Start Date -> gone from grid AND absent in `OV_LICENCE` | PASS |

## 2. CLASSIFICATION / DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Commercial Objects > Licence |
| Pattern | Bank pattern (plain manage-object OV, no navigator) |
| Screen type | Manage Object (OV) — confirmed live 2026-08-23: GO-button count = 0 of 94 elements present, nav-free |
| Grid id | `manage_object_nav_nav:form:T_data` (reused from T2's shared `${OV_MANAGE_OBJECT_TABLE}` constant, not re-hardcoded) |
| DB view | `OV_LICENCE` |
| Field labels | Screen-prefixed: "Licence Code" / "Licence Name" (NOT the generic "Code"/"Name" Bank/Object List use) |
| Mandatory fields | Licence Code, Licence Name, Start Date (Insert-only; Start Date not present in `updateAttributes`) |
| Grid columns | Licence Code / Licence Name / Start Date / End Date (Bank convention, 4 columns) |
| Delete semantics | End Date = Start Date (true delete — row leaves `OV_LICENCE`) |

### DOM reference (current, Bank-pattern shape — label-resolved, not hardcoded)
```
INSERT (objectForm):        Licence Code / Licence Name / Start Date (MandatoryCellStyle)
UPDATE (updateAttributes):  Licence Code (read-only) / Licence Name
DELETE (objectdates):       End Date  tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```
(The original 2026-06-12 build used hardcoded per-row field ids, shown below for history;
PR #438, 2026-08-23, rebuilt the T3 page object to resolve fields by label via the shared
T2 `manage_object` keywords, matching Bank/State/Country. The ids above are what T2
resolves to today, not literals baked into `licence_page.resource` anymore.)

Original 2026-06-12 hardcoded ids (superseded):
```
INSERT: Code  tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
        Name  tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
        Start tab:tabPanel:objectForm:form:G:0:R:6:C:1:da_input
UPDATE: Code  tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (guard)
        Name  tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
DELETE: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

### Test data
Fixed code `AUTOTEST_LICENCE` | Name `AUTOTEST Licence` (+` UPDATED`) | Start=End `2000-01-01`
(current, RF suite). `testdata/licence_{insert,update,form_verify,grid_verify}.properties`
carry only the fields actually needed (IUD-fill-only-needed-fields convention) — Sort
Order/Description/Master System Code/Master System Name are optional and left blank.
(Original 2026-06-12 Playwright reference used a timestamped code `AUTOTEST_LIC_<ts>` and
`2003-01-01` dates — see `evidence/licence_results.json` for that run's own record.)

## 3. DEVELOPMENT — dev story
Built originally 2026-06-12 as a data-driven Playwright + RF pair generated from section
recon (`investigation/commercial_objects_recon.py`), using the older hardcoded-field-id
pattern (bespoke per-screen Insert/Update/Delete keywords, no properties-file-driven
insert). Converted to the full Bank pattern on 2026-08-23 (PR #438, one of 5 parallel
Batch 3 conversions alongside Customer/Field Group/MMS Lease/Operator Lease — see
`tmp/batch3_shared_findings.md`): rebuilt `licence_page.resource` and `licence_iud.robot`
to the label-driven, properties-file-driven, T2-consolidated shape used by
`bank_page.resource`/`country_page.resource`, including explicit Find/Clear Licence Row
By Filter grid-filter wiring from the start (not deferred). Live recon during that
conversion confirmed the manage-object OV shape (nav-free), the screen-prefixed field
labels, and the exact mandatory-field set (Licence Code/Licence Name/Start Date only) —
no gotcha or rework round is recorded for Licence itself in the PR body. The PR body
records robocop parity as 12 issues total (4 VAR02 + 5 DOC02 on the new suite + 3
pre-existing `credentials.py` findings) — identical in kind/count to the established
Bank/Country baseline, no new issue classes introduced.

This SOW/README/JOURNAL/evidence/CHECKLIST.md/KB-map bundle was backfilled 2026-08-27/28
per the owner's 2026-08-27 retirement of the Section G lean waiver
(`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) — the RF automation itself was NOT
touched or re-verified from scratch; this bundle only adds the documentation/evidence
artifacts the waiver had skipped.

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF dryrun | headless | 5/5 PASS (2026-08-23 original + 2026-08-28 backfill re-confirm) |
| RF live | `EC_HEADLESS=true` | TC01-TC05 5/5 PASS, DB-verified (2026-08-28 backfill re-run) |
| Filter keyword fired | `output.xml` grep | `Find Licence Row By Filter` = 5 hits (2026-08-28 re-confirm) |
| DB self-clean | fresh `oracledb` connection | `OV_LICENCE` `AUTOTEST_LICENCE` count = 0 (2026-08-28 re-confirm) |
| robocop (T3 + suite) | `py -m robocop check` | 9 issues (4 VAR02 + 5 DOC02), same shape as the original PR's cited 12 (12 minus the 3 pre-existing `credentials.py` findings, not re-scanned here) |
| Playwright reference run | headless (original 2026-06-12 build) | see `evidence/licence_results.json` |

## 5. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Commercial_Objects/licence_*`,
this bundle (SOW/README/JOURNAL/evidence/CHECKLIST.md), registry row in
`docs/ec_screen_registry.md`, KB selector map `ec-ui-knowledge/screens/licence.md`.
