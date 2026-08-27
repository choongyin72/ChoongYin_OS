# JOURNAL — Bank Account IUD

_Screen: Configuration > Assets > Financial Objects > Bank Account (OV, date-effective, no
mandatory navigator). View `OV_BANK_ACCOUNT`. Distinct screen from Bank (CO.0001, the Bank-pattern
exemplar) — do not confuse the two bundles._

## Backfill note (2026-07-25 entry, retained)
This bundle was built in an earlier session, **before** the 19-item IUD deliverable checklist mandated a
per-bundle `JOURNAL.md` (item #3). It was missing until **2026-07-25**, when the owner flagged the gap during
a Bank Account reuse-run. Backfilled here from the verified artifacts + today's live run.

## Built (2026-06-11, original)
- RF: `bank_account_page.resource` (T3) + `bank_account_iud.robot` suite (reuses T2 `manage_object` + `DbVerify.py`).
- Playwright: standalone `playwright/ec_iud_bank_account.py` bundle (+ investigation recon + evidence).
- SOW: `bank_account_sow.md`. Knowledge map (added 2026-07-25): `ec-ui-knowledge/screens/bank_account.md`.

## Done well (2026-06-11/07-25)
- Full I-U-D, DB-verified against `OV_BANK_ACCOUNT` (`Code Should Be Present/Absent In View`), self-cleaning (`AUTOTEST_`).
- Correctly handled the richer New-Object form vs Bank: mandatory **Sort Code (R8)** + 3 mandatory ref dropdowns
  **Bank (R20) / Customer (R21) / Currency (R23)** — row indices recon'd, NOT copied from Bank.

## Done wrong / lesson (2026-07-25)
- On the "next screen = Bank Account" request I first reported "Done" after only running the tests —
  **without** producing the knowledge-base MD (`bank_account.md`) or this JOURNAL. Owner caught it. Lesson:
  "Done" = the full deliverable set (tests + KB MD + JOURNAL + evidence), not just green tests.

## Blockers -> resolution (2026-07-25)
- None (reuse run). The check-existing-first gate correctly identified Bank Account as already implemented,
  so no parallel copy was created — only the existing suites were run.

## Decisions (2026-07-25)
- Kept the existing standalone Playwright bundle (not migrated to the generic `py/ec_object_iud.py` engine) because
  the engine does not yet handle mandatory reference dropdowns; migration deferred until dropdown support is added.

## Evidence (2026-07-25)
- RF: `results/_bankacct/report.html` (4/4, 2026-07-25).
- Playwright: `evidence/bank_account_0[1-8]_*.png` (ALL PASS, 2026-07-25).

---

## Built (2026-08-23, PR #478 — Bank-pattern RF conversion, FINAL screen of the 23-screen pool)
- Rebuilt the RF suite (`bank_account_page.resource` + `bank_account_iud.robot`) from the OLD
  hardcoded-field-id pattern (`Fill New Object Form ${BANK_ACCOUNT_INS_CODE} ...`, generated-
  timestamp code, single Suite-Setup login) to Bank/Berth's label-driven, properties-file-driven,
  T2-consolidated pattern, including explicit grid-filter wiring — the same conversion applied
  across Batches 2-11 of the Bank-pattern project.
- New properties files: `testdata/bank_account_{insert,update,form_verify,grid_verify}.properties`.
- Additive credentials: `resources/credentials.py` gained `BANK_ACCOUNT_EC_USER`/
  `BANK_ACCOUNT_EC_PASS` (falls back to `EC_USER`/`EC_PASS`/`sysadmin` if unset).
- Registry row modified (`docs/ec_screen_registry.md`, from the 2026-06-11 Playwright-era entry);
  new scorecard row added (`docs/automation-scorecard.md` — no prior Bank Account entry existed
  there); own row appended to `docs/{bank-pattern-conversion-checklist,
  grid-filter-standardization-checklist}.md`.
- No shared T1/T2 file changes (`resources/manage_object.resource` / `resources/common.resource`
  untouched) — Batch 11 ground rule.

## Done well (PR #478)
- Live run: `EC_HEADLESS=true robot tests/.../bank_account_iud.robot` -> **5/5 PASS** (TC01
  clean-state, TC02 insert, TC03 update, TC04 find, TC05 delete).
- DbVerify assertions: `Code Should Be Present In View OV_BANK_ACCOUNT ${code}` (TC02),
  `Code Should Be Absent In View OV_BANK_ACCOUNT ${code}` (TC05).
- Fresh oracledb connection before AND after the run confirmed `AUTOTEST_BACC` free / 0 residual
  `AUTOTEST%` rows in `OV_BANK_ACCOUNT`.
- Grid-filter keyword confirmed fired: `Find Object Row By Filter` 15x / `Clear Object Row Filter`
  15x via output.xml grep.
- `robocop check` -> 7 issues (2 VAR02 + 5 DOC02), same baseline-noise class already accepted
  throughout this batch series — no regression.
- `robot --dryrun` on the full `tests/` tree -> 772/772 pass.

## Done wrong / lessons (PR #478)
- Live-recon'd the real objectForm/updateAttributes ECCell labels (30 fields each) before writing
  any config — Code label confirmed SCREEN-PREFIXED "Bank Account Code" (not generic "Code" like
  Bank) — a wrong assumption here would have broken every label-driven keyword.
- Trusted the screen's own already-proven Playwright driver's field set (Sort Code + Bank/
  Customer/Currency dropdowns) over a static CSS mandatory scan, since Customer showed
  `{mandatory:false}` on this pass but the proven driver + SOW confirm it's a conditional-
  mandatory business rule (Process Train Batch-9 lesson) — a static-scan-only approach would have
  silently dropped a real mandatory field.
- Dropdown fields filled with `__FIRST__` are excluded from the round-trip form-label compare (a
  resolved reference value can re-render different display text after reload — Storage Flow
  Batch-10 precedent).
- A live Vendor dropdown exists but is neither in the proven driver nor static-mandatory —
  deliberately omitted (IUD-fill-only-needed-fields), not silently included "just in case."

## Blockers -> resolution (PR #478)
- No hard blockers disclosed in the PR body; the conversion merged same-day with clean evidence.

## Decisions (PR #478)
- Zero edits to `manage_object.resource`/`common.resource` (Batch 11 ground rule) — this screen's
  quirks (screen-prefixed Code label, extra mandatory dropdowns) stay local to
  `bank_account_page.resource`, not pushed into shared T2/T1 code.

## Evidence (PR #478)
- Cited in the PR body: live 5/5, full-tree dryrun 772/772, robocop 7 issues, grid-filter 15x/15x,
  DB self-clean 0 residual — see `gh pr view 478` for the exact text.

---

## Backfill session (2026-08-28, `docs/lean-deliverable-backfill-workorder.md`, Batch 11)

_Owner decision 2026-08-27 retired the 2026-08-23/26 lean waiver (Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`) — SOW/README/JOURNAL/evidence/CHECKLIST/KB map are restored
requirements for Bank-pattern conversions. This session adds those documentation/evidence
artifacts around PR #478's already-merged, already-live-tested RF automation. No RF file
(`bank_account_page.resource`, `bank_account_iud.robot`, `testdata/bank_account_*.properties`) was
modified to produce this backfill._

## Built (this session)
- Updated `bank_account_sow.md` (Section 7 addendum), `README.md`, `JOURNAL.md` (this entry),
  `ec-ui-knowledge/screens/bank_account.md` — all pulled from PR #478's real body/commit content,
  not invented.
- Added `CHECKLIST.md` and `VERIFY-REPORT.md` (neither existed before this session).
- Captured fresh RF evidence into the pre-existing `evidence/` folder (merged alongside the
  2026-06-11 Playwright-era screenshots/results.json, not overwritten).

## Done well (this session)
- `py -m robocop check pageobjects/.../bank_account_page.resource tests/.../bank_account_iud.robot`
  -> **7 issues** (same 2 VAR02 + 5 DOC02 categories PR #478 cited — no drift).
- `robot --dryrun tests/.../bank_account_iud.robot` -> **5/5 PASS**.
- Fresh-connection DB read BEFORE the live run: `DbVerify.fetch_object("OV_BANK_ACCOUNT",
  "AUTOTEST_BACC")` -> `None` (confirmed absent, code free to use).
- `EC_HEADLESS=true robot --outputdir .../Bank_Account/evidence tests/.../bank_account_iud.robot`
  -> **5/5 PASS on the first attempt** — no flake, no retry needed.
- Fresh-connection DB read AFTER the run: `DbVerify.fetch_object("OV_BANK_ACCOUNT",
  "AUTOTEST_BACC")` -> `None` (confirmed absent again — self-clean verified).
- Grid-filter keyword re-confirmed firing: `Find Object Row By Filter` 15x / `Clear Object Row
  Filter` 15x in this session's own `output.xml` — matches PR #478's cited count exactly.
- `py scripts/check_bundle_hygiene.py` (repo root) -> `RESULT: PASS` (167 bundles + 272 recon
  scripts scanned; the one WARN reported is a pre-existing, unrelated Contract Area
  `investigation/` script, not this screen).

## Done wrong / lessons (this session)
- None — this was a straightforward evidence-capture/documentation pass around already-proven
  automation; no automation file was touched and no live-run flake occurred.

## Blockers -> resolution (this session)
- None.

## Decisions (this session)
- Bundle location kept at `screens/Configuration/Assets/Financial_Objects/Bank_Account/`
  (pre-existing path from the 2026-06-11 build), UPDATED rather than duplicated, per the
  workorder's instruction to update an existing bundle instead of creating a parallel one.
- Playwright driver + `investigation/` left untouched (Section H permanent waiver) — the
  pre-existing 2026-06-11 bundle is kept as historical reference only.

## Evidence (this session)
- `evidence/log.html`, `evidence/output.xml`, `evidence/report.html`,
  `evidence/playwright-log.txt`, per-TC screenshots (`TC0N ..._{login,open_screen,action,verify,
  logout}.png`) from this session's live 5/5 RF run, alongside the pre-existing 2026-06-11
  Playwright evidence (`bank_account_0[1-8]_*.png`, `bank_account_results.json`, unchanged).
