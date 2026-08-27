# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Field Group
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-12
**Version:** 1.0 — COMPLETE (RF suite + Playwright reference, live + DB-verified)

---

## 1. REQUIREMENT
Automate IUD on the **Field Group** screen with DB-level proof. Constraints: NEVER touch
existing data; test codes `AUTOTEST_FG_<timestamp>`; local sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_FIELD_GROUP` | PASS |
| UPDATE | Name change visible in grid row | PASS |
| DELETE | End=Start -> gone from grid AND absent in `OV_FIELD_GROUP` | PASS |

## 2. DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Commercial Objects > Field Group |
| Screen type | Manage Object (OV) |
| List/grid id | `manage_object_nav_nav:form:T_data` |
| DB view | `OV_FIELD_GROUP` |
| Delete semantics | End Date = Start Date (true delete) |

### DOM reference (rows derived from recon LABELS)
```
INSERT: Code  tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
        Name  tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
        Start tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
UPDATE: Code  tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (guard)
        Name  tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
DELETE: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

### Test data
Code `AUTOTEST_FG_<timestamp>` | Name `Field Group <code>` (+` UPD`) | Start=End `2003-01-01`
(section-wide 2003-01-01: reference dropdowns are effective-date-filtered — the object
Start Date acts as a version; seed objects start 2003-01-01)

## 3. DEVELOPMENT
Generated DATA-DRIVEN from the section recon (`investigation/commercial_objects_recon.py`).
Banner-discovered mandatory dropdowns resolved in fix round 1; Field links into its groupmodel via the Geo Area dropdown (= navigator Area).

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF dryrun | headless | PASS |
| RF live | headless | TC01–TC04 4/4 PASS, DB-verified |
| Playwright reference run | headless | see `evidence/field_group_results.json` |

## 5. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Commercial_Objects/field_group_*`,
this bundle, registry row in `docs/ec_screen_registry.md`.

---

## 6. ADDENDUM — Bank-pattern conversion (PR #434, merged 2026-08-23) + backfill (2026-08-28)

**Classification (current, live-confirmed):** plain Bank-pattern OV screen (manage-object,
**no navigator** — confirmed live 2026-08-23). Grid id `manage_object_nav_nav:form:T_data`
(re-used from T2's `${OV_MANAGE_OBJECT_TABLE}` constant, not re-hardcoded). DB view
`OV_FIELD_GROUP`. Delete = End Date = Start Date (true delete).

**What changed in PR #434:** converted the Field Group IUD suite from the older
hardcoded-field-id/generated-code pattern (this SOW's original Sections 1-5, dated 2026-06-12,
used `AUTOTEST_FG_<timestamp>`) to the label-driven, properties-file-driven, T2-consolidated
Bank pattern (mirroring Bank/Country), with explicit grid Find/Clear Row By Filter wiring
included from the start. Files rewritten: `field_group_page.resource` (+148/-58),
`field_group_iud.robot` (+52/-44); new: `testdata/field_group_{insert,update,form_verify,
grid_verify}.properties`; additive: `resources/credentials.py`
(`FIELD_GROUP_EC_USER`/`FIELD_GROUP_EC_PASS`). Part of Batch 3 of the Bank-pattern conversion
project (5 screens: Customer, Field Group, Licence, MMS Lease, Operator Lease).

**Real gotcha from PR #434 (not invented):** the throwaway RF recon script used to
live-confirm field labels found Code/Name/Start Date mandatory in objectForm; End Date/
Description/Comments/Field Group Type (dropdown)/Reporting Field Group Indicator (checkbox)
confirmed optional and omitted from the round-trip form-label list — except Description,
kept in for business-realistic test data matching Bank's own convention. The plain
manage-object navigator (no mandatory nav scope) was reconfirmed live, matching the registry.
The `objectdates` End Date field id was reconfirmed live to match the pre-conversion file's
own value exactly (no drift).

**Current test data (fixed code, superseding Sections 1-4's generated-code description):**
`AUTOTEST_FIELD_GROUP` / `Automation Test Field Group` (+` UPDATED`) / Start=End `2003-01-01`
— see `testdata/field_group_insert.properties` / `field_group_update.properties`.

**This backfill (2026-08-28, `docs/lean-deliverable-backfill-workorder.md` Batch 6):** the
2026-08-23 conversion (PR #434) was built under the 2026-08-23/26 lean waiver, which skipped
SOW/README/JOURNAL/evidence/CHECKLIST/KB-map. This addendum, `JOURNAL.md`, `CHECKLIST.md`, a
fresh `evidence/backfill_2026-08-28/` live run, and `ec-ui-knowledge/screens/field_group.md`
backfill those artifacts. No RF/Playwright automation file was modified to produce this
addendum — see `JOURNAL.md` for the full account.
