# JOURNAL — Bank Account IUD

_Screen: Configuration > Assets > Financial Objects > Bank Account (OV, date-effective). View `OV_BANK_ACCOUNT`._

## Backfill note
This bundle was built in an earlier session, **before** the 19-item IUD deliverable checklist mandated a
per-bundle `JOURNAL.md` (item #3). It was missing until **2026-07-25**, when the owner flagged the gap during
a Bank Account reuse-run. Backfilled here from the verified artifacts + today's live run.

## Built
- RF: `bank_account_page.resource` (T3) + `bank_account_iud.robot` suite (reuses T2 `manage_object` + `DbVerify.py`).
- Playwright: standalone `playwright/ec_iud_bank_account.py` bundle (+ investigation recon + evidence).
- SOW: `bank_account_sow.md`. Knowledge map (added 2026-07-25): `ec-ui-knowledge/screens/bank_account.md`.

## Done well
- Full I-U-D, DB-verified against `OV_BANK_ACCOUNT` (`Code Should Be Present/Absent In View`), self-cleaning (`AUTOTEST_`).
- Correctly handled the richer New-Object form vs Bank: mandatory **Sort Code (R8)** + 3 mandatory ref dropdowns
  **Bank (R20) / Customer (R21) / Currency (R23)** — row indices recon'd, NOT copied from Bank.

## Done wrong / lesson
- (2026-07-25) On the "next screen = Bank Account" request I first reported "Done" after only running the tests —
  **without** producing the knowledge-base MD (`bank_account.md`) or this JOURNAL. Owner caught it. Lesson:
  "Done" = the full deliverable set (tests + KB MD + JOURNAL + evidence), not just green tests.

## Blockers -> resolution
- None today (reuse run). The check-existing-first gate correctly identified Bank Account as already implemented,
  so no parallel copy was created — only the existing suites were run.

## Decisions
- Kept the existing standalone Playwright bundle (not migrated to the generic `py/ec_object_iud.py` engine) because
  the engine does not yet handle mandatory reference dropdowns; migration deferred until dropdown support is added.

## Evidence
- RF: `results/_bankacct/report.html` (4/4, 2026-07-25).
- Playwright: `evidence/bank_account_0[1-8]_*.png` (ALL PASS, 2026-07-25).
