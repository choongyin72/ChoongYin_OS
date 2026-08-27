# SOW — Deferment Group IUD

_Backfilled 2026-08-28 per `docs/lean-deliverable-backfill-workorder.md` (Batch 11, last screen).
Supersedes the 2026-07-26 pre-Bank-pattern version of this file — the screen was rebuilt to the
full Bank pattern in PR #479 (merged 2026-08-23) and this SOW now reflects that rebuild._

## Classification
- **Screen:** Configuration > Assets > Facility_Objects > Deferment Group (BF_CODE **CO.0149**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) — date-effective — **plain Bank-pattern**
  (no navigator, no mandatory dropdowns). Rebuilt to the label-driven, properties-file-driven,
  T2-consolidated, explicit-grid-filter shape shared by Bank/State/Berth/Bank Account, converted in
  Batch 8 of the Bank-pattern-conversion project.
- **DB view:** `OV_DEFERMENT_GROUP` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_DEFERMENT_GROUP` (date-effective delete)

## Nav / grid / cells
- **Open:** menu search "Deferment Group" -> `label.tv-link` (text label, not `span.tv-link` — a
  14.1.x-vs-14.2.4 selector difference already noted on Bank). No navigator section — plain OV.
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`). Explicit
  grid-column filter wired via `Find/Clear Object Row By Filter` (T2 `manage_object.resource`) —
  15 `Find Object Row By Filter` hits confirmed in the live run's `output.xml` at merge time.
- **NO hardcoded field ids** — resolved BY LABEL via T2 `Fill OV * By Label` / `OV Field Id By Label`:
  - **Insert (objectForm):** `Deferment Group Code`, `Deferment Group Name`, `Start Date` (mandatory).
    Optional dropdowns skipped (screen has none mandatory).
  - **Update (updateAttributes):** `Deferment Group Name` only (Code read-only). Start Date is
    Insert-only, deliberately excluded from `@{DEFERMENT_GROUP_FORM_LABELS}` (matches Bank/State/Berth).
  - **Delete (objectdates):** `End Date` field id `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`
    = Start Date (true delete).

## Test data
- Fixed test code `AUTOTEST_DEFERMENT_GROUP` (per PR #479's registry entry); dedicated credential
  pair `DEFERMENT_GROUP_EC_USER`/`DEFERMENT_GROUP_EC_PASS` (defaults to `sysadmin`/`sysadmin` via
  `EC_USER`/`EC_PASS` fallback in `resources/credentials.py`). Never touches real production rows.

## Dev story (pulled from PR #479's real body — merged 2026-08-23)
Deferment Group was rebuilt to the current Bank/Berth/Bank-Account label-driven, properties-file-driven,
T2-consolidated Bank-pattern shape as part of Batch 8 (2026-08-23), **but the build was BLOCKED at
that time**: `TV_T_BASIS_ACCESS` had `LEVEL_ID=0` ("No access") for all 5 roles on this screen object
(`OBJECT_ID=1087`), so the screen link was unreachable even via menu search or treeview browsing —
not a code defect, a live-sandbox role-access gate. The rebuilt work sat uncommitted in an isolated
clone (`Workplaces/deferment_group`) rather than being merged untested. The owner granted sysadmin-role
access in the sandbox after that; PR #479 re-verified live access first (login + menu search actually
found and opened the screen), then ran the full live gate — 5/5 PASS (TC01 clean-state, TC02 insert,
TC03 update, TC04 find, TC05 delete), full-tree dryrun 774/774, robocop clean on the page object,
grid-filter keyword confirmed fired (15 hits) — before raising the PR.

**Regression found during this backfill (2026-08-28) — see JOURNAL.md "Blockers -> resolution":**
re-running the suite live for evidence capture found the SAME symptom recurring (menu-search timeout
on the `Deferment Group` tv-link, both an initial attempt and one retry). A direct DB check against
`TV_T_BASIS_ACCESS` for `OBJECT_ID=1087` confirms `LEVEL_ID=0` for all 5 roles again — the access
grant that unblocked PR #479 has regressed in this sandbox. This is a live-environment/role-access
fact, not an automation defect; it is disclosed here and in JOURNAL/CHECKLIST rather than silently
worked around, per this project's standing rules on honest disclosure of live-run failures.

## Lessons / known risks
- Optional dropdowns skipped (none mandatory).
- Delete uses the shared engine's row-absence wait (async grid redraw) — no screen-specific tuning.
- **Access is a live external dependency, not a one-time fix.** `TV_T_BASIS_ACCESS.LEVEL_ID` for
  `OBJECT_ID=1087` can regress independently of any code change in this repo; any future live-run
  failure with this exact "tv-link not found" symptom should check that table FIRST (real DB query,
  not another selector-guessing script) before assuming a regression in the RF suite itself.
