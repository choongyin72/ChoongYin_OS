# JOURNAL — Payment Scheme IUD (RF)

_Screen: Configuration > Assets > Financial Objects > Payment Scheme, OV (plain Manage Object,
date-effective, no navigator). View `OV_PAYMENT_SCHEME`._

_This JOURNAL was backfilled 2026-08-28 under `docs/lean-deliverable-backfill-workorder.md` (owner
decision 2026-08-27 retiring the 2026-08-23/26 lean waiver — Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`). The RF automation described below was already built and
merged in PR #420 on 2026-08-22; this JOURNAL narrates what that PR's body actually recorded — it
is not a new build and no automation file was touched to produce it. This screen is Batch 6 (the
first Bank-pattern wave) of the backfill work order._

## Built (2026-08-22, PR #420)
- Converted Payment Scheme's RF suite from the older hardcoded-field-id/generated-code pattern to
  the current **Bank/State pattern**: label-driven field resolution, properties-file-driven test
  data, per-TC login/logout, a fixed test code (`AUTOTEST_PAYMENT_SCHEME`, replacing
  `AUTOTEST_PSCH_<timestamp>`), delegating to shared T2 (`resources/manage_object.resource`) and
  T1 (`resources/common.resource`) keywords.
- Files rewritten: `payment_scheme_page.resource` (T3), `payment_scheme_iud.robot` (5 TCs: Clean
  State, Insert, Update, Find, Delete).
- Files added: `testdata/payment_scheme_{insert,update,form_verify,grid_verify}.properties`.
- Files touched additively: `resources/credentials.py` (`PAYMENT_SCHEME_EC_USER`/
  `PAYMENT_SCHEME_EC_PASS`), `docs/ec_screen_registry.md` (row updated in place),
  `docs/automation-scorecard.md` (new row appended after Company's).
- This was part of the same "Round 2" batch as Account and Exchange Rate Source (independent
  branch off master, not stacked on either).

## Done well
- Full 5-TC I-U-D-Find cycle, DB-verified vs `OV_PAYMENT_SCHEME` at the fixed code
  `AUTOTEST_PAYMENT_SCHEME`.
- PR #420 cited: live recon confirmed no navigator, single grid (`manage_object_nav_nav:form:T_data`,
  GO present, count=1), `objectForm` fields Code/Name/Start Date/End Date/Comments/Description with
  only Code/Name/Start Date mandatory-yellow, generic (not screen-prefixed) field labels.
- `AUTOTEST_PAYMENT_SCHEME` confirmed free in `OV_PAYMENT_SCHEME` before the build (count=0);
  `CODE` column confirmed `VARCHAR2(32)` — the 23-char code fits.
- robocop: 9 issues, identical in kind/count to the State/Cost Centre/WBS exemplars' own baseline
  (VAR02 unused `${OBJ_NAME_UPD}` + 5x DOC02 missing TC docs) — zero new issues.
- Full-tree dryrun at the time: 724/724 PASS.
- Live headless run: 5/5 PASS, first attempt, no retry needed.
- Fresh-connection DB re-read post-run: 0 residual rows (self-clean confirmed).

## Done wrong / lessons
- No defect or flake was disclosed in PR #420's own body for Payment Scheme itself — the build
  went green on the first live attempt.
- A genuine minor operational detail from the merge: landing PR #420 required resolving append
  conflicts in `resources/credentials.py` and `docs/automation-scorecard.md` against sibling PRs
  from the same batch (Cost Centre/Revenue Order/WBS/Exchange Rate Source) that were merging
  around the same time. Both conflicts were resolved by **keeping both sides** — the additive
  credential block and the additive scorecard row from each PR — not by dropping either side's
  content. This is a routine append-only-file merge mechanic (multiple PRs each appending a new
  row/block to the same file), not a design or automation issue.
- **This backfill session (2026-08-28):** the fresh dryrun + live headless re-run both passed 5/5
  clean on the first attempt — no flake to disclose, unlike some sibling backfills (e.g. Area's
  TC05 grid-redraw flake). Robocop re-run reproduced the same 9-issue baseline exactly (no drift).

## Blockers -> resolution
- No hard blockers on the original conversion (PR #420) — merged same-day with clean evidence,
  first-attempt live pass.
- No blockers in this backfill session — dryrun, live run, DB self-clean check, and hygiene check
  all passed on the first attempt; no retry was needed (process rule's one-retry allowance was not
  invoked).

## Decisions
- Payment Scheme is classified as a **plain Bank-pattern OV** screen (no navigator section),
  matching Bank/State/Object List's shape rather than Area's OV-GM shape — confirmed live in PR
  #420 (no navigator GO gesture required before the grid loads; only the toolbar GO/Refresh at
  `button:form:B`).
- Grid filtering uses the same explicit `Find/Clear Payment Scheme Row By Filter` convention as
  Account/Bank/State/Object List (owner-directed standardisation, 2026-08-22), rather than relying
  on the implicit 3s-timeout fallback in `Select Object Row`.
- The pre-existing Playwright bundle (`playwright/ec_iud_payment_scheme.py`, from the original
  2026-06-11 build) was left untouched by PR #420 and by this backfill — Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md` (2026-08-27) permanently waives a new Playwright driver for
  Bank-/Area-pattern work (the Universal Screen Engine replaces that role going forward); the
  pre-existing one is kept as historical reference, not rebuilt.

## Evidence
- PR #420: cited live 5/5, full-tree dryrun 724/724, DB self-clean 0/0 (fresh connection),
  robocop 9-issue baseline (parity with State/Cost Centre/WBS) — see `gh pr view 420` for the
  exact body text these figures are pulled from.
- This backfill session (2026-08-28):
  - `robot --dryrun tests/Configuration/Assets/Financial_Objects/payment_scheme_iud.robot` ->
    **5/5 PASS**.
  - `EC_HEADLESS=true robot --outputdir <bundle>/evidence tests/.../payment_scheme_iud.robot` ->
    **5/5 PASS**, first attempt, no retry needed.
  - DB self-clean: `DbVerify.fetch_object("OV_PAYMENT_SCHEME", "AUTOTEST_PAYMENT_SCHEME")` ->
    `None` (confirmed absent) after the run, via a fresh Python/oracledb connection.
  - `py -m robocop check` on `payment_scheme_page.resource` + `payment_scheme_iud.robot` ->
    **9 issues** (DOC02/VAR02) — matches PR #420's cited 9-issue baseline exactly, no drift.
  - `py scripts/check_bundle_hygiene.py` (repo-wide) -> **PASS** ("no hardcoded creds (R16), pure
    ASCII (R20), no CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families");
    one unrelated pre-existing WARN on a different screen's (Contract Area) recon script, not
    Payment Scheme's.
  - Evidence artifacts: `evidence/log.html`, `evidence/output.xml`, `evidence/report.html`,
    `evidence/playwright-log.txt`, per-TC screenshots (`TC0N ..._{login,open_screen,action,verify,
    logout}.png`) from this session's clean run, alongside the pre-existing 2026-06-11 Playwright
    evidence (`payment_scheme_0[1-8]_*.png`, `payment_scheme_results.json`).
