# JOURNAL — DOA Credit Limit IUD (RF)

_Screen: Configuration > Assets > Financial Objects > DOA Credit Limit, OV (Manage Object,
date-effective, no navigator). View `OV_DOA_CREDIT_LIMIT`._

_This JOURNAL was backfilled 2026-08-28 under `docs/lean-deliverable-backfill-workorder.md` (owner
decision retiring the 2026-08-23/26 lean waiver — Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`). The RF automation described below was already built and
merged in PR #443 (Batch 4 of the Bank-pattern conversion project) on 2026-08-23; this JOURNAL
narrates what that PR's body actually recorded — it is not a new build and no automation file was
touched to produce it._

## Built (2026-08-23, PR #443)

- Converted DOA Credit Limit's IUD suite from the older hardcoded-field-id pattern to the
  label-driven, properties-file-driven, T2-consolidated **Bank/VAT Code pattern**: 5 TCs (Verify
  Clean State / Insert / Update / Find / Delete), fixed test code `AUTOTEST_DOA`, per-TC
  Login/Logout, explicit `Find/Clear DOA Credit Limit Row By Filter` grid-filter wiring included
  from the start.
- Files rebuilt: `pageobjects/Configuration/Assets/Financial_Objects/doa_credit_limit_page.resource`,
  `tests/Configuration/Assets/Financial_Objects/doa_credit_limit_iud.robot` (4 TCs -> 5 TCs).
- New properties files: `testdata/doa_credit_limit_{insert,update,form_verify,grid_verify}.properties`.
- Additive credentials: `DOA_CREDIT_LIMIT_EC_USER`/`_PASS` in `resources/credentials.py`.
- Registry/scorecard/checklist doc rows updated at merge time (not touched by this backfill).

## Done well

- Live recon before any config (dumped objectForm/updateAttributes labels + MandatoryCellStyle via
  throwaway RF scripts, `tmp/recon_doa*.robot`, deleted before commit).
- No `__FIRST__` on mandatory reference dropdowns — literal `Amount Based`/`ANALYTICS.REPORTADMIN`
  used instead (per the VAT Code round-trip-verify precedent), because TC02's verify compares the
  live screen back against the same insert-properties file.
- Live 5/5 pass. `DOA Credit Limit Should Exist In DB`/`Should Not Exist In DB` assert against
  `OV_DOA_CREDIT_LIMIT` via `DbVerify.code_should_be_present_in_view`/`code_should_be_absent_in_view`.
  Fresh (independent) connection re-read after the full suite: 0 residual `AUTOTEST_DOA` rows, 0
  residual `RECON_DOA_SAVE` rows (a throwaway recon row, cleaned up same session), total
  `OV_DOA_CREDIT_LIMIT` row count back to the original 3. `Find DOA Credit Limit Row By Filter`
  confirmed fired 7 times via `output.xml` grep.
- Grid-filter wiring included from day one; per-TC Login/Logout; pre-save evidence screenshots.

## Done wrong / lessons

- **Two genuine evidence-based fixes during the original build (both disclosed in PR #443's own
  body, not smoothed over):**
  1. A real EC **conditional-mandatory** business rule: `Currency`'s static CSS class is
     `{mandatory:false}`, but a live Save attempt with `DOA Type = Amount Based` and no Currency
     failed with the banner "Amount Based DOA Requires a currency" — invisible to the static
     `MandatoryCellStyle` scan alone. Fix: `Currency=USD` added to the insert properties despite
     the static scan saying optional.
  2. `Role Name` re-renders as its Description (`Report Administrator`) after any
     `updateAttributes` reload, not the raw code used to select it
     (`ANALYTICS.REPORTADMIN`) — a live-DOM round-trip check against the same insert literal would
     always fail here. Fix: `Role Name` deliberately excluded from the live-DOM round-trip
     form-label list (`@{DOA_CREDIT_LIMIT_FORM_LABELS}`); DB ground-truth (`ROLE_ID` column) still
     covers it independently — same documented re-render gotcha class as Account Mapping's Line
     Item Type (registry note).
  3. **2026-08-25 alignment fix** (separate follow-up commit, same screen): removed a leftover
     inline `DOA Credit Limit Should Exist In DB`-style direct DB-verify keyword and matching TC02
     call that had crept in and violated Bank's pure-screen-only verification convention
     (2026-08-18) — same deviation class flagged on several other Batch-4/5 screens (Royalty
     Depositor, Stream Item Category, Calculation Context, Document Template all cite "same
     deviation class as DOA Credit Limit (PR #503)" in the registry). Re-verified live 5/5 after the
     fix.
- No issues found or introduced during this backfill session itself — the live re-run below passed
  clean on the first attempt (no retry needed).

## Blockers -> resolution

- No hard blockers on the original conversion (PR #443) — the two business-rule/re-render findings
  above were root-caused via live Save banners/DOM dumps and fixed within the same session, not
  escalated.
- This backfill session (2026-08-28) hit no blockers: dryrun, live run, DB self-clean, and hygiene
  all passed on the first attempt.

## Decisions

- DOA Credit Limit stays classified plain **OV / Manage Object, no navigator** (only the universal
  Date+GO as-at-date bar) — confirmed live 2026-08-23, not assumed from a sibling screen.
- The Playwright driver (`playwright/ec_iud_doa_credit_limit.py`) and `investigation/` recon scripts
  from this screen's original 2026-06-11 build are kept as historical reference, not rebuilt or
  touched — permanently waived per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` (Universal
  Screen Engine replaces that role going forward).
- `Role Name` is excluded from the live-DOM round-trip form-label list by design (see "Done wrong"
  #2 above) — one canonical representation (DB `ROLE_ID`) picked per field when screen display and
  DB storage genuinely differ, matching Bank's own precedent.

## Evidence

- PR #443: cited live 5/5, `Find DOA Credit Limit Row By Filter` fired 7 times, DB self-clean 0/0/0
  (`AUTOTEST_DOA`, `RECON_DOA_SAVE`, total row count) via a fresh connection — see
  `gh pr view 443` for the exact text.
- This backfill session (2026-08-28):
  - `robot --dryrun tests/Configuration/Assets/Financial_Objects/doa_credit_limit_iud.robot` ->
    **5/5 PASS**.
  - `EC_HEADLESS=true robot --outputdir .../DOA_Credit_Limit/evidence
    tests/.../doa_credit_limit_iud.robot` -> **5/5 PASS clean** (first attempt, no retry needed).
  - DB self-clean: `DbVerify.fetch_object("OV_DOA_CREDIT_LIMIT", "AUTOTEST_DOA")` -> `None`
    (confirmed absent) via a fresh oracledb connection after the run.
  - `Find DOA Credit Limit Row By Filter` confirmed fired **18 times** via `output.xml` grep (this
    session's run).
  - `py -m robocop check` on `doa_credit_limit_page.resource` + `doa_credit_limit_iud.robot` ->
    **7 issues** (DOC02 missing TC documentation) — same issue category as Bank/Area's own
    baselines, not a new category.
  - `py scripts/check_bundle_hygiene.py` (repo root) -> **PASS** — "no hardcoded creds (R16), pure
    ASCII (R20), no CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families" (167
    bundles + 272 recon scripts scanned; the one WARN reported is a pre-existing, unrelated
    Contract Area finding).
  - Evidence artifacts: `evidence/log.html`, `evidence/output.xml`, `evidence/report.html`,
    `evidence/playwright-log.txt`, per-TC screenshots (`TC0N ..._{login,open_screen,action,verify,
    logout}.png`) from this clean run, alongside the pre-existing 2026-06-11 Playwright evidence
    (`doa_credit_limit_01_loaded.png` ... `doa_credit_limit_08_final_state.png`,
    `doa_credit_limit_results.json`).
