# SOW - Contract IUD (Configuration > Assets > Contract_Objects)

_Updated 2026-08-27 (deliverable backfill, `docs/lean-deliverable-backfill-workorder.md` Batch 3) to
reflect the 2026-08-26 Area-pattern conversion (PR #546). The section below this note is the
original 2026-08-02 SOW, kept verbatim for history; §2 documents what actually changed._

## 1. Original build (2026-08-02)
- **Screen:** Contract   **BF:** CO.2016   **View:** `OV_CONTRACT`   **Base:** `CONTRACT`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade (PROVEN explicit values, not first-available) + GO; fields BY LABEL + extra dropdowns.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `AUTOTEST_CT_<timestamp>`; self-clean = absent in OV_CONTRACT.
- Deliverables (original): driver `py/contract_iud.py`, T3 `pageobjects/Configuration/Assets/Contract_Objects/contract_page.resource`,
  suite `tests/Configuration/Assets/Contract_Objects/contract_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).

## 2. Area-pattern conversion (2026-08-26, PR #546)
- **Pattern:** rebuilt from the original inline-navigator/suite-login/4-TC build to the full Area
  pattern: 5 TCs (clean-state/insert/update/find/delete), per-TC login/logout with dedicated
  `CONTRACT_EC_USER`/`CONTRACT_EC_PASS` (`resources/credentials.py`), properties-file-driven
  insert/update/verify, explicit grid-filter wiring (`Find/Clear Contract Row By Filter` -> shared
  T2 `Find/Clear Object Row By Filter`), navigator fill delegated to the shared T2 `Apply Navigator
  From Properties` (`resources/manage_object.resource`), driven by
  `testdata/contract_navigator.properties`. Contract remains genuinely OV-GM — the Business
  Unit+GO gesture is real and required; this was a structural conversion, not a reclassification
  to plain Bank-shaped.
- **Navigator:** Business Unit = `TS5 BU` (single dropdown `nav:form:G:0:R:1:C:1:dd`, PROVEN
  explicit value reused as-is from the screen's own prior driver — the task brief that assigned
  this conversion had cited "TS3 BU"; that value was checked against the real prior driver
  (`py/contract_iud.py`) and corrected to the actual, already-proven `TS5 BU` before use).
- **Mandatory fields (Insert, `objectForm`):** Contract Code, Contract Name, Start Date, **End
  Date** (unusual — mandatory on Insert, unlike most OV-GM screens where End Date is optional and
  used only for delete), **Contract Year Start**, plus dropdowns Contract Template (`__FIRST__`)
  and Contract Area (`TS5 Contract Area`, must sit under the navigator's own Business Unit=TS5 BU
  scope or the inserted row is invisible under this navigator scope).
- **Mandatory fields (Update, `updateAttributes`):** Contract Name only — Contract Code is
  read-only post-insert.
- **Delete:** End Date = Start Date via the packed `objectdates` row
  (`tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`, hardcoded id — packed-row rationale, same
  as Bank/Area's own del-enddate constants).
- **Test data:** fixed code `AUTOTEST_CONTRACT` (confirmed absent from `OV_CONTRACT` before use,
  replacing the original per-run `AUTOTEST_CT_<timestamp>` scheme);
  `testdata/contract_{insert,update,form_verify,grid_verify,navigator}.properties`.
- **Dev story — genuine branch-name-collision incident:** Contract's conversion and Contract
  Area's conversion were independently dispatched with the SAME worktree branch name
  (`feature/contract-area-pattern-conversion`). Contract's own agent detected this itself from
  unexpected commit history in its own worktree, self-fixed by cherry-picking only its own commit
  onto a fresh branch off `origin/master` (`contract-conversion-fix`, resolving one
  `credentials.py` merge conflict by keeping only the `CONTRACT_EC_USER`/`CONTRACT_EC_PASS`
  lines), and raised PR #546 clean as a result. It could NOT fix the other side — Contract Area's
  PR #542 still had Contract's commit appended on top of its own; an attempted force-push to
  unwind that was blocked by the environment's own safety guardrail against destructive rewrites
  of an already-published PR branch, and required separate, owner-approved intervention (disclosed
  to the owner before being carried out). Full detail in `JOURNAL.md`'s "Blockers -> resolution".
- **Live run:** needed 3 attempts at conversion time due to transient UI-timing flakiness
  (`Could not find active page` during AJAX-heavy navigator/grid redraws) — DB reads after the
  flaky attempts already showed 0 residual rows both times, confirming the flakiness was UI-timing
  only, not a business-logic or delete defect.
- **Deliverables (added/changed by the conversion):** rebuilt T3
  `pageobjects/Configuration/Assets/Contract_Objects/contract_page.resource`, rebuilt suite
  `tests/Configuration/Assets/Contract_Objects/contract_iud.robot`, 5 properties files under
  `testdata/`, additive `resources/credentials.py` entries. Registry/scorecard rows updated
  in-place (not duplicated). Playwright driver `py/contract_iud.py` left unchanged (superseded by
  the Universal Screen Engine per owner decision — no new driver built).

## 3. This backfill (2026-08-27)
Adds the documentation/evidence bundle this screen was missing under the now-retired lean waiver:
`README.md` (exact run commands), refreshed `JOURNAL.md` (branch-collision incident captured
honestly), `evidence/backfill_2026-08-27/` (fresh dryrun + live 5/5 run + DB self-clean + robocop +
hygiene evidence), refreshed `CHECKLIST.md`, and KB map `ec-ui-knowledge/screens/contract.md`. The
RF automation itself, `py/contract_iud.py`, the registry row, and the scorecard row were NOT
modified by this backfill — all already existed and were already correct from PR #546.
