# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — MMS Lease
**Author:** Choong-Yin Lee / Claude
**Date:** 2026-06-12 (original), updated 2026-08-28 (Bank-pattern backfill, Batch 6)
**Version:** 2.0 — RF suite rebuilt to the Bank pattern (PR #437, merged 2026-08-23);
this revision backfills SOW/JOURNAL/evidence/CHECKLIST/KB per
`docs/lean-deliverable-backfill-workorder.md`, owner decision 2026-08-27 (Section H).

---

## 1. Classification

| Property | Value |
|---|---|
| Screen | MMS Lease |
| Treeview path | Configuration > Assets > Commercial Objects > MMS Lease |
| Screen type | Manage Object (OV), plain — **no navigator/scope dropdown before the grid loads** (confirmed live 2026-08-23: `manage_object_nav` GO button count = 0) |
| Pattern | Bank pattern (`ec-bank-pattern-converter`) — label-driven, properties-file-driven, T2-consolidated, explicit grid-filter wiring |
| DB view | `OV_MMS_LEASE` (key `CODE`) |
| Grid id | `manage_object_nav_nav:form:T_data` (reused as `${OV_MANAGE_OBJECT_TABLE}` / `${MMS_LEASE_TABLE}`) |
| Delete semantics | End Date = Start Date (true delete — row leaves `OV_MMS_LEASE`) |

## 2. Fields

- **Field labels are screen-prefixed**: "MMS Lease Code" / "MMS Lease Name" (not generic
  "Code"/"Name" — confirmed live via a field-label recon dumping every `ECCell` label).
- `objectForm` (Insert), 6 labels: MMS Lease Code, MMS Lease Name, Description, Start Date,
  End Date, Operator. Mandatory (yellow, `MandatoryCellStyle`-confirmed) = 3: MMS Lease
  Code, MMS Lease Name, Start Date.
- `updateAttributes` (Update), 4 labels: MMS Lease Code, MMS Lease Name, Description,
  Operator (no Start/End Date — same as Bank/State/Country). Mandatory = 2: MMS Lease
  Code, MMS Lease Name.
- Description/Operator confirmed optional and deliberately omitted (IUD-fill-only-needed-
  fields convention).
- Grid columns: MMS Lease Code / MMS Lease Name / Start Date / End Date.
- Delete field: `objectdates` row R0, End Date input `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`.

## 3. Test data

Fixed test code `AUTOTEST_MMS_LEASE` (confirmed free in `OV_MMS_LEASE` before wiring in,
2026-08-23), Name `AUTOTEST MMS Lease` → `AUTOTEST MMS Lease UPDATED`, Start = End
`2000-01-01`. Properties files: `testdata/mms_lease_insert.properties`,
`mms_lease_update.properties`, `mms_lease_form_verify.properties`,
`mms_lease_grid_verify.properties`.

## 4. Dev story (real, from PR #437's body — Batch 3 of the Bank-pattern conversion project)

Converted MMS Lease's IUD suite from the older hardcoded-field-id, generated-code pattern
to the label-driven, properties-file-driven, T2-consolidated "Bank pattern" already used by
Bank/State/Country/Account/Cost Centre, including explicit grid-filter wiring
(`Find MMS Lease Row By Filter` / `Clear MMS Lease Row Filter`) from the start rather than
relying on the implicit 3s-timeout fallback in `Select Object Row`. Live recon (a real
insert+select+delete+DB-verify cycle on a throwaway record) confirmed the navigator has no
mandatory scope, the screen-prefixed field labels, and the mandatory-field sets in both
`objectForm` and `updateAttributes` before any config was written — no guessing. Result:
live RF run 5/5 PASS, full `tests/` dryrun 735/735 PASS, robocop 9 issues (4 VAR02 + 5
DOC02, identical in kind/count to the Bank/Country baseline — a stable characteristic of
this pattern family, not a defect), DB self-clean 0 residual `AUTOTEST_MMS_LEASE` rows via
an independent fresh connection. This was one of 5 screens (Customer, Field Group, Licence,
MMS Lease, Operator Lease) converted in parallel under isolated clones in the same Batch 3
wave; no shared T1/T2 files were touched, and the `credentials.py` change was additive-only.

## 5. Deliverables

RF T3 `pageobjects/Configuration/Assets/Commercial_Objects/mms_lease_page.resource` + suite
`tests/Configuration/Assets/Commercial_Objects/mms_lease_iud.robot` (already merged, PR
#437) — this bundle (SOW/README/JOURNAL/evidence/CHECKLIST) backfills the documentation
around that already-working automation; no RF/pageobject files were modified for this
backfill. Registry row in `docs/ec_screen_registry.md` (already present). KB selector map:
`ec-ui-knowledge/screens/mms_lease.md` (added by this backfill).

The Playwright driver (`playwright/ec_iud_mms_lease.py`) and its `investigation/` recon
scripts predate the Bank-pattern conversion and stay in place as historical reference —
per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` the Playwright bundle role is now
waived permanently in favour of the Universal Screen Engine; no new Playwright work was
done for this backfill.
