# JOURNAL — Price Object IUD (CO.3016, OV-GM)

_Screen: Configuration > Assets > Sales_Objects > Price Object (**CO.3016**), OV-GM (groupmodel
manage-object, date-effective). View `OV_PRICE_OBJECT`._

_This JOURNAL entry for the PR #536 conversion was backfilled 2026-08-27 under
`docs/lean-deliverable-backfill-workorder.md` (owner decision retiring the 2026-08-23/26 lean waiver —
Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`). The RF automation described below was already built
and merged in PR #536 on 2026-08-26; this JOURNAL narrates what that PR's body actually recorded — it is
not a new build and no automation file was touched to produce it. The 2026-08-03 entry below is the
original build's own JOURNAL content, kept unchanged._

## 2026-08-03 (original build)
- **Branch:** `feature/build-price-object-iud`. Previously parked as "pager-walk click timeout
  (5-page grid)" (original), then re-investigated for issue #321 (2026-08-02): that characterization
  did NOT hold up under careful re-testing — the pager itself walked all 5 pages cleanly, twice. The
  REAL root cause found that round: inserting with Business Unit deliberately left unset leaves the
  row with no `BUSINESS_UNIT_CODE`, so it is genuinely not visible under any page of a BU-scoped grid
  — the same missing/wrong-scope defect class as Message Group and Planned Well, not a pagination bug.
- **This round: built the fix.** Used `gen_ovgm.py` with `parent_dd: "Business Unit"` so the
  navigator's captured top-parent (first-available Business Unit, e.g. "EC LNG Norway") is bound into
  the insert form's own Business Unit dropdown — the exact mechanism that was missing before.
- **New generator gap found and fixed locally (same class as Service/CO.2103):** the navigator has
  only ONE mandatory dropdown (Business Unit), but 2 more OPTIONAL FILTER dropdown columns exist on
  the same nav row (unrelated to Business Unit, not cascade children). `gen_ovgm.py`'s `nav_levels`
  config key only caps the Python driver's cascade — the generator does NOT thread `nav_levels` into
  the generated RF T3, which always emits `Apply OV-GM Navigator First Available` with no cap and times
  out on column 2/3's empty options. Fixed by hand, following the exact precedent already set on
  Service's own T3: replaced the shared cascade keyword call with a direct `Select First EC Dropdown
  Option` on the screen's own single nav-dropdown variable.
- Confirmed live + DB-verified via `verify_screen.py` (OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4,
  live RF 4/4, Playwright driver 8/8). Full I-U-D. 0 residual.

## Built (2026-08-26, PR #536 — Area-pattern conversion)
- Converted Price Object's bespoke-inline-navigator RF automation to the Area full pattern: 5 TCs
  (Verify Clean State / Insert / Update / Find / Delete), per-TC login/logout, fixed test code
  `AUTOTEST_PRICE_OBJECT` (replacing the original build's generated `AUTOTEST_PO_<timestamp>` code),
  properties-file-driven insert/update/verify, the navigator filled via the shared `Apply Navigator
  From Properties` T2 keyword (`resources/manage_object.resource`), explicit grid-filter wiring
  (`Find/Clear Price Object Row By Filter`), and zero inline DB-verify calls in the `.robot` file.
- New `testdata/price_object_{navigator,insert,update,form_verify,grid_verify}.properties` files;
  additive `PRICE_OBJECT_EC_USER`/`PRICE_OBJECT_EC_PASS` in `resources/credentials.py`; the existing
  `docs/ec_screen_registry.md` Price Object row was modified in place (not a new row).
- No shared T1/T2 file (`manage_object.resource`, `common.resource`) was modified — this screen reuses
  the existing `Apply Navigator From Properties` keyword as-is (first built for Area, PR #523).

## Done well
- **Real gotcha, disclosed rather than assumed:** the navigator's real, currently-working Business Unit
  value was re-confirmed LIVE this session via a fresh read-only recon
  (`tmp/recon_price_object_nav.py`, not committed — gitignored `tmp/`), rather than reused from a
  sibling screen's documented value. It resolves to **"EC LNG Norway"**, NOT "Royalty Canada" — the
  value used by sibling screens Property/Price Index/Division Order/Royalty Contract, a DIFFERENT
  environment default. Recorded in `testdata/price_object_navigator.properties` and the registry.
- Live run: 5/5 PASS (TC01-TC05). Fresh oracledb connection after the live run:
  `SELECT CODE, NAME FROM OV_PRICE_OBJECT WHERE CODE LIKE 'AUTOTEST%'` → 0 residual rows (self-clean
  confirmed). Pre-build: confirmed `AUTOTEST_PRICE_OBJECT` free in `OV_PRICE_OBJECT` (0 rows) before
  wiring in the fixed test code. Full-tree dryrun 850/850. Grid-filter keyword confirmed firing (15
  hits in `output.xml` for `Find Object Row By Filter`). Zero inline DB-verify calls in the new
  `.resource`/`.robot` files (grepped for `Should Exist In DB`/`Field Should Equal In View`/`Code
  Should Be Present/Absent In View` — 0 hits).
- Robocop parity vs Area's own baseline: 7 DOC02-only issues both sides (missing `[Documentation]` on
  TC03-05), no new issue category introduced by the conversion.

## Done wrong / lessons
- The original build's "pager timeout" park reason was wrong TWICE before the real defect (a missing
  Business Unit scope binding) was found — this is the same lesson recorded in the original 2026-08-03
  entry above, worth restating here because the PR #536 conversion's own navigator-value re-confirmation
  step exists specifically to avoid repeating that class of mistake (assuming a value instead of
  verifying it live).
- No new "done wrong" was disclosed in PR #536's own body beyond the above — the conversion itself
  reported clean on first live run (5/5), unlike Area's own backfill evidence-capture session (which
  hit a real TC05 grid-redraw flake). This backfill's own evidence-capture run (below) also passed
  clean on first try.

## Blockers -> resolution
- No hard blockers on the original conversion (PR #536) — merged same-day with clean evidence cited in
  the PR body.
- This backfill session's evidence-capture run: no blockers. `tasklist` was checked for stray
  `chrome.exe`/`chrome-headless-shell.exe` processes before the live run per this backfill's own
  instruction (several pre-existing stray `chrome-headless-shell.exe` processes were present, unrelated
  to this run and not interfering) — the live run completed 5/5 clean on the first attempt.

## Decisions
- Price Object stays classified **OV-GM**, not reclassified as plain Bank-shaped, despite adopting the
  Area 5-TC RF STRUCTURE — the genuine mandatory Business Unit navigator + GO gesture was kept.
- The Playwright driver (`py/price_object_iud.py`) was deliberately left untouched by PR #536 — Section H
  of `docs/IUD-DELIVERABLE-CHECKLIST.md` (2026-08-27) waives items 4/5 (Playwright driver +
  `investigation/`) for Bank-/Area-pattern work permanently (Universal Screen Engine replaces that role);
  the pre-existing bundle here (`py/price_object_iud.py`, `investigation/gen_ovgm_config.json`,
  `evidence/po_0[1-5]_*.png`) is kept as historical reference, not rebuilt.
- `Apply Navigator From Properties` lives in the SHARED `resources/manage_object.resource` (T2), reused
  as-is from Area's own build (PR #523) — no shared-file change was needed for Price Object.

## Evidence
- PR #536: cited live 5/5, full-tree dryrun 850/850, DB self-clean 0/0 (fresh connection), grid-filter
  keyword fired (15 hits), zero inline DB-verify calls (0 hits), robocop parity (7 issues) — see the PR
  body (`gh pr view 536`) for the exact commands/output cited.
- This backfill session (2026-08-27):
  - `robot --dryrun tests/Configuration/Assets/Sales_Objects/price_object_iud.robot` → **5/5 PASS**.
  - `EC_HEADLESS=true robot --outputdir .../Price_Object/evidence tests/.../price_object_iud.robot` →
    **5/5 PASS** clean, first attempt (no flake).
  - DB self-clean: `libraries.DbVerify.fetch_object("OV_PRICE_OBJECT", "AUTOTEST_PRICE_OBJECT")` →
    `None` (confirmed absent), fresh oracledb connection, this session.
  - `py -m robocop check` on `price_object_page.resource` + `price_object_iud.robot` → **7 issues**
    (DOC02 missing TC docs) — matches PR #536's cited 7-issue parity with Area's own baseline, no drift.
  - `py scripts/check_bundle_hygiene.py` (repo-wide) → **PASS** — "no hardcoded creds (R16), pure
    ASCII (R20), no CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families" (167
    bundles + 271 recon scripts scanned; the one WARN reported belongs to Contract Area's
    `investigation/`, unrelated to this screen).
  - Evidence artifacts: `evidence/log.html`, `evidence/output.xml`, `evidence/report.html` (this
    session's clean 5/5 run), alongside the pre-existing 2026-08-03 Playwright evidence
    (`evidence/po_0[1-5]_*.png`).
