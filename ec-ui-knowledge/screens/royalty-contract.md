# Royalty Contract (BF RC.0059) - selector map

**Nav path:** EC_Revenue > Royalty > Royalty_Canada > Royalty Contract
**DB view:** `OV_ROYALTY_CONTRACT`   **Base:** `ROYALTY_CONTRACT`
**Type:** OV-GM (manage-object, groupmodel), navigator-GATED, date-effective.
**Last verified:** 2026-08-15, local sandbox `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`.

## Grid / navigator
- Grid tbody id: `manageObject:form:T_data`.
- Navigator dropdown: `nav:form:G:1:R:1:C:0:dd_input` (note: **group `G:1`, not `G:0`** - same
  G:0/G:1 split gap seen on Property). PROVEN explicit value: **"Royalty Canada"** (Business Unit) -
  first-available is NOT safe on this screen (a prior blind attempt landed on a sparse combination).
- GO button: `button:form:B`.

## Insert (New Object form, `objectForm`)
Mandatory fields, by label:
- `Royalty Contract Code` (text)
- `Royalty Contract Name` (text)
- `Start Date` (date) - **must be >= the referenced Contract Area's own effective date** (see
  Quirks below).
- `End Date` (date) - **unusually mandatory on INSERT** (same as Contract CO.2016), not yellow-flagged
  but Save fails without it. Use a far-future placeholder (e.g. `2099-12-31`) - unrelated to the
  Delete gesture's End=Start value.
- `Contract Template` (dropdown) - PROVEN value used: "Royalty Fixed Percentage Canada" (see Quirks
  - this specific template triggers the Delete-blocking side effect).
- `Contract Area` (dropdown) - PROVEN value used: "Alberta".

## Update
Row-select (`updateAttributes` region) -> edit `Royalty Contract Name` by label -> Save.

## Delete - PERMANENTLY BLOCKED (do not attempt)
`Royalty Contract Row` has no working Delete path on this screen for contracts using the "Royalty
Fixed Percentage Canada" template. Attempting End Date = Start Date fails with EC's own error:
`"Child record found... all child records must be deleted first."` Root cause: this template
auto-provisions 10 `CNTR_PG_SETUP` rows as a genuine EC business-logic side effect, and the screen's
UI exposes no way to view/delete them. **This is a genuine EC product limitation, not an automation
defect** - confirmed via full DB investigation (all FK-linked tables to `CONTRACT` checked for the
test object's `OBJECT_ID`). Owner-accepted permanent exception (closes Issue #336, same precedent as
Production Day Table CO.1033) - do not re-attempt Delete on a future retry without a new reason to
believe EC's own behavior has changed.

## Quirks
- **Date-effective reference dropdown trap** (shared with Property/Price Index/Message Group): a
  Start Date that predates a referenced parent object's (Business Unit/Contract Area/Functional
  Area) own effective date causes EC's reference dropdown to silently exclude that option and fall
  back to a different one - looks like a dropdown-persistence bug but is really a date mismatch.
  Always use a Start Date >= every referenced parent's own effective date.
- Test data: `AUTOTEST_RC_<timestamp>` (RF suite, `Prepare IUD Object Data`) or `AUTOTEST_RC_00N`
  (Playwright driver, `EC_CODE` env override). Residual rows accumulate permanently - see the
  bundle's `investigation/ROOT_CAUSE_delete_blocked.md` for the disclosed running count.

## See also
- `workstreams/master-plan/ec-automation/screens/EC_Revenue/Royalty/Royalty_Canada/Royalty_Contract/`
  (SOW, JOURNAL, investigation, evidence, VERIFY-REPORT).
- `docs/ov-non-bank-targets.md` (RC.0059 park record history, PR #331).
