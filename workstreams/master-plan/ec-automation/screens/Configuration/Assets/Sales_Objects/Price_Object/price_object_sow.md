# SOW — Price Object IUD (Configuration > Assets > Sales_Objects)

- **Screen:** Price Object   **BF:** CO.3016   **View:** `OV_PRICE_OBJECT` (versioned)   **Base:** `PRODUCT_PRICE`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- **Navigator shape:** ONE mandatory Business Unit dropdown (`nav:form:G:0:R:1:C:1:dd`) + GO. NOT a real
  cascade — 2 sibling dropdown columns on the same nav row are unrelated optional filters (same class of
  shape as Service/CO.2103), so the shared multi-level cascade keyword is bypassed in favor of a direct
  single-dropdown fill (now delegated to the shared T2 `Apply Navigator From Properties`, driven by
  `testdata/price_object_navigator.properties`).
- **Mandatory fields:** Price Object Code, Price Object Name, Start Date, Product Name, Price Concept, UOM,
  Price Rounding Rule (insert form); Business Unit must equal the navigator's captured value or the new row
  is not visible under this navigator scope (OV-GM constraint). Update touches Price Object Name only —
  Price Object Code is read-only in `updateAttributes`. Delete = End Date = Start Date (true delete).
- **Test data:** fixed test code `AUTOTEST_PRICE_OBJECT` (confirmed absent from `OV_PRICE_OBJECT` before
  wiring in), not a generated/unique code — every run must complete TC05 (delete) so the code stays free.

## Dev story

**Original build (2026-08-03):** parked twice before this build — first as a "pager-walk click timeout
(5-page grid)" (2026-07-27), then re-investigated for issue #321 (2026-08-02), where that characterization
did not hold up under careful re-testing (the pager itself walked all 5 pages cleanly, twice). The real
root cause: inserting with Business Unit left unset leaves the row with no `BUSINESS_UNIT_CODE`, so it is
genuinely not visible under any page of a BU-scoped grid — the same missing/wrong-scope defect class as
Message Group and Planned Well, not a pagination bug. Fixed via `gen_ovgm.py`'s `parent_dd: "Business Unit"`
binding the navigator's captured value into the insert form's own Business Unit dropdown. A related
generator gap was found and hand-fixed the same round: `gen_ovgm.py`'s `nav_levels` config key only caps
the Python driver's cascade, not the generated RF T3, which always emits `Apply OV-GM Navigator First
Available` and times out on this screen's 2 unrelated optional filter columns — fixed locally by bypassing
the shared cascade keyword with a direct single-dropdown fill on the T3, matching the precedent already set
on Service (CO.2103). Delivered as `py/price_object_iud.py` (Playwright) + a first-generation RF T3/suite
(4 TCs, generated `AUTOTEST_PO_<timestamp>` code), verified via `verify_screen.py` OVERALL PASS (robocop 0,
hygiene 0, dryrun 4/4, live RF 4/4, Playwright driver 8/8), full I-U-D, 0 residual.

**Area-pattern conversion (2026-08-26, PR #536):** the original bespoke-inline-navigator RF automation was
rebuilt to the Area full pattern — 5 TCs (Verify Clean State / Insert / Update / Find / Delete), per-TC
login/logout, fixed test code `AUTOTEST_PRICE_OBJECT` (replacing the generated `AUTOTEST_PO_<timestamp>`
code), properties-file-driven insert/update/verify, the navigator filled via the shared `Apply Navigator
From Properties` T2 keyword (`resources/manage_object.resource`), explicit grid-filter wiring
(`Find/Clear Price Object Row By Filter`), and zero inline DB-verify calls in the `.robot` file. **Real
gotcha found and worth flagging:** the navigator's real, currently-working Business Unit value was
re-confirmed live this session via a fresh read-only recon (`tmp/recon_price_object_nav.py`, not
committed) — it resolves to **"EC LNG Norway"**, NOT "Royalty Canada" (the value used by sibling screens
Property/Price Index/Division Order/Royalty Contract — a different environment default). Recorded in
`testdata/price_object_navigator.properties` and the registry rather than assumed from a sibling screen.
Live 5/5, full-tree dryrun 850/850, DB self-clean confirmed (0 residual `AUTOTEST%` rows, fresh
connection), robocop parity vs Area's own baseline (7 DOC02-only issues both sides).

**Not to be confused with** "Product Price Object" (CD.0011, PR #502) — a distinct custom-URL screen with
no navigator; that screen's files are untouched by either build described above.

## Deliverables
- Driver `py/price_object_iud.py` (pre-existing Playwright reference, kept unchanged — items 4/5 waived
  for Bank-/Area-pattern work per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`)
- T3 `pageobjects/Configuration/Assets/Sales_Objects/price_object_page.resource` (Area-pattern shape)
- Suite `tests/Configuration/Assets/Sales_Objects/price_object_iud.robot` (5 TCs)
- This SOW, `README.md`, `JOURNAL.md`, `evidence/`, `CHECKLIST.md`
- KB map `ec-ui-knowledge/screens/price_object.md`

## Section 7 — backfill addendum (2026-08-27)

This SOW was refreshed under `docs/lean-deliverable-backfill-workorder.md` (owner decision 2026-08-27,
Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`, retiring the 2026-08-23/26 lean waiver). The RF
automation described above was already built and merged in PR #536 on 2026-08-26; this addendum documents
that conversion — no automation file (`price_object_page.resource`, `price_object_iud.robot`,
`testdata/price_object_*.properties`) was touched to produce it.
