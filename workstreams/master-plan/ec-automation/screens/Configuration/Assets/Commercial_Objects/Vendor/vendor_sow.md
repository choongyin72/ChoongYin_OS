# EC Screen IUD Operation — Statement of Work (SOW)
**Project:** EC RF Automation (workstreams/master-plan/ec-automation)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Vendor
**Author:** Choong-Yin Lee / Claude (backfill pass, Batch 7, 2026-08-28)
**Original conversion:** PR #439, "Vendor - Bank-pattern conversion (Batch 4)", merged 2026-08-23
**Version:** 2.0 — supersedes the 2026-06-12 v1.0 SOW (kept below, Appendix, for history);
this section reflects the CURRENT Bank-pattern implementation that has been live since PR #439.

---

## 1. Classification
- **Pattern:** plain Bank pattern — Manage Object (OV), **no navigator section** (confirmed
  live 2026-08-23 per PR #439/registry: only the universal Date + GO as-at-date bar, no
  mandatory nav dropdown).
- **Treeview path:** Configuration > Assets > Commercial Objects > Vendor.
- **DB view (ground truth):** `OV_VENDOR`.
- **Delete semantics:** End Date = Start Date (true delete, standard EC Object convention).
- **Grid id:** reused from T2's centralized constant `${OV_MANAGE_OBJECT_TABLE}` (T3 does not
  re-hardcode the literal string — same convention as Bank/Customer).

## 2. Mandatory fields (confirmed live 2026-08-23, objectForm AND updateAttributes identical)
| Field | Type | Notes |
|---|---|---|
| Code | text | read-only after create (guard in updateAttributes) |
| Name | text | |
| Start Date | date | objectdates only, not in updateAttributes |
| ERP Vendor Code | text | |
| Official Name | text | |
| Vendor Group | reference dropdown | real first option = literal `Contract Owner Vendor` (used verbatim, not `__FIRST__` — VAT Code round-trip-verify gotcha) |
| Description | text | optional; included as TC03's second Update field, matching Bank's/Customer's own Name+Description pair |

Grid columns: Code / Name / Start Date / End Date (Bank convention).

## 3. Test data used
Fixed test code `AUTOTEST_VEND`, Start Date `2000-01-01`. Values live in:
- `testdata/vendor_insert.properties` — Code/Name/Description/Start Date/ERP Vendor
  Code/Official Name/Vendor Group.
- `testdata/vendor_update.properties` — Name/Description only (the two fields that exist in
  `updateAttributes`).
- `testdata/vendor_form_verify.properties` — post-update merged-state expectation (TC04).
- `testdata/vendor_grid_verify.properties` — grid-only column expectation (Code/Name/Start
  Date, no End Date until deleted).

## 4. Dev story (from PR #439's real body, not invented)
Converted the Vendor screen from the older hardcoded-field-id pattern to the label-driven,
properties-file-driven, T2-consolidated "Bank pattern", reusing shared
`resources/manage_object.resource` keywords and wiring in explicit grid-filter
`Find/Clear Vendor Row By Filter` from day one. Real gotchas hit and resolved during the
original build (per the PR body's "Rules applied" section):
- Live recon before config (no extrapolation from Customer) — the mandatory field set (Code,
  Name, Start Date, ERP Vendor Code, Official Name, Vendor Group dd) was confirmed live on
  BOTH `objectForm` and `updateAttributes` via throwaway RF recon scripts (deleted before
  commit, per the lean-build convention of the time).
- Vendor Group's real first dropdown option (`Contract Owner Vendor`) was read back live and
  used literally rather than `__FIRST__`, per the VAT Code round-trip-verify gotcha (Batch 2)
  — `__FIRST__` never resolves to literal text for a form-compare assertion.
- Grid columns were confirmed live from an existing row's raw cell text, not assumed.
- No `resources/manage_object.resource` or `resources/common.resource` edits were made.
- robocop after conversion: 7 issues (2 VAR02 + 5 DOC02) — fewer than the then-established
  9-issue baseline, no new issue classes.
- Full `tests/` dryrun at merge time: 740/740 pass.

## 5. Test execution (original PR #439, 2026-08-23)
| Run | Mode | Result |
|---|---|---|
| Live suite | headless | 5/5 PASS (`robot tests/.../vendor_iud.robot`) |
| DB self-clean | fresh oracledb connection | 0 residual `AUTOTEST_VEND` rows in `OV_VENDOR`, before and after |
| Filter-fired check | `grep -c 'name="Find Vendor Row By Filter"' output.xml` | 5 |

## 6. This backfill pass (2026-08-28)
This is a documentation/evidence backfill only (owner decision 2026-08-27, Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md` retiring the 2026-08-23/26 lean waiver). No automation
file was modified. See `README.md`, `JOURNAL.md`, `CHECKLIST.md`, and
`evidence/rf_backfill_2026-08-28/` for the re-run confirmation and citations.

## 7. Deliverables
RF suite + page object under `pageobjects|tests/.../Commercial_Objects/vendor_*`, this bundle,
registry row in `docs/ec_screen_registry.md`, scorecard row in `docs/automation-scorecard.md`,
KB selector map `ec-ui-knowledge/screens/vendor.md`.

---

# Appendix — original v1.0 SOW (2026-06-12, pre-Bank-pattern, kept for history)

The content below describes the screen's OLDER shape (pre-conversion Playwright reference +
older RF suite with a timestamped test code) and predates PR #439's Bank-pattern conversion.
It is retained verbatim for historical traceability; Sections 1-7 above are the current,
authoritative description.

## 1. REQUIREMENT (v1.0, superseded)
Automate IUD on the **Vendor** screen with DB-level proof. Constraints: NEVER touch
existing data; test codes `AUTOTEST_VEND_<timestamp>`; local sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_VENDOR` | PASS |
| UPDATE | Name change visible in grid row | PASS |
| DELETE | End=Start -> gone from grid AND absent in `OV_VENDOR` | PASS |

## 2. DESIGN (v1.0, superseded)
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Commercial Objects > Vendor |
| Screen type | Manage Object (OV) |
| List/grid id | `manage_object_nav_nav:form:T_data` |
| DB view | `OV_VENDOR` |
| Delete semantics | End Date = Start Date (true delete) |

### DOM reference (rows derived from recon LABELS) — v1.0, pre-conversion
```
INSERT: Code  tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
        Name  tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
        Start tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
        ERP Vendor Code:      tab:tabPanel:objectForm:form:G:0:R:6:C:1:in (MANDATORY text)
        Official Name:        tab:tabPanel:objectForm:form:G:0:R:7:C:1:in (MANDATORY text)
UPDATE: Code  tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (guard)
        Name  tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
DELETE: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

### Test data (v1.0, superseded — current suite uses fixed `AUTOTEST_VEND`, see Section 3 above)
Code `AUTOTEST_VEND_<timestamp>` | Name `Vendor <code>` (+` UPD`) | Start=End `2003-01-01`

| Extra mandatory field | Test value |
|---|---|
| ERP Vendor Code | `ERP999` |
| Official Name | `AUTOTEST Official` |
| Vendor Group (reference dd, banner-discovered) | first available option |

## 3. DEVELOPMENT (v1.0, superseded)
Generated DATA-DRIVEN from the section recon (`investigation/commercial_objects_recon.py`).
Banner-discovered mandatory dropdowns resolved in fix round 1.

## 4. TEST EXECUTION (v1.0, superseded)
| Run | Mode | Result |
|---|---|---|
| RF dryrun | headless | PASS |
| RF live | headless | TC01–TC04 4/4 PASS, DB-verified |
| Playwright reference run | headless | see `evidence/vendor_results.json` |

## 5. DELIVERABLES (v1.0, superseded)
RF suite + page object under `tests|pageobjects/.../Commercial_Objects/vendor_*`,
this bundle, registry row in `docs/ec_screen_registry.md`.
