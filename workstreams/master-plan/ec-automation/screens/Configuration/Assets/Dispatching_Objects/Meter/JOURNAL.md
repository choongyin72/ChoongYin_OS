# JOURNAL — Meter (Area-pattern conversion)

_Screen: Configuration > Assets > Dispatching Objects > Meter (OV-GM, BU-gated, + generic popup).
View `OV_METER`. Converted to the full Area pattern via PR #554 (merged 2026-08-26). This JOURNAL
was backfilled 2026-08-27 (bundle predated the restored SOW/README/JOURNAL/evidence/CHECKLIST/KB
rule — Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`) — it documents what actually happened
during the PR #554 build, pulled from the PR's own body and the detailed narrative already
recorded in `docs/ec_screen_registry.md`'s starred Meter row. No RF automation was touched by this
backfill._

## Built (2026-08-26, PR #554)
- Rebuilt `pageobjects/Configuration/Assets/Dispatching_Objects/meter_page.resource` and
  `tests/Configuration/Assets/Dispatching_Objects/meter_iud.robot` from the older
  4-TC/suite-login/generated-code/inline-DB-verify pattern to the full 5-TC Area pattern
  (properties-file-driven insert/update/verify, per-TC login, explicit grid-filter wiring, zero
  inline DB-verify calls).
- New testdata files: `meter_navigator.properties`, `meter_insert.properties`,
  `meter_update.properties`, `meter_form_verify.properties`, `meter_grid_verify.properties`.
- Additive `METER_EC_USER`/`METER_EC_PASS` in `resources/credentials.py`.
- TC04 Find added (now 5 TCs, matching Area's own shape).

## Done well
- Full I-U-D DB-verified vs `OV_METER` (fixed test code `AUTOTEST_METER`, confirmed free before
  the build via a fresh oracledb connection); self-clean 0 residual both before and after the live
  run, each check via a fresh independent connection (not the test run's own session).
- No shared T1/T2 file edits — the existing `Apply Navigator From Properties`
  (`resources/manage_object.resource`) and the generic `Pick From EC Object Popup`/
  `Pick OV Popup By Label` (`resources/popup.resource`) mechanisms already covered Meter's shape
  with zero gaps; only the additive `credentials.py` entries were needed outside the screen's own
  files.
- The genuine Delivery Point popup mechanism (JS-click `pinB`, wait for `#popupIFrame`, match rows
  by value/innerText, never XPath `@value`) was carried through unchanged from the original
  2026-06-13 build — this conversion is structural only, it did not touch or re-derive the popup
  gesture itself.
- Live run 5/5 pass; full `tests/` tree dryrun 874/874 pass; robocop 7 issues on the changed
  screen files = exact parity with `area_page.resource`/`area_iud.robot`'s own 7-issue baseline
  (+3 pre-existing unrelated `credentials.py` COM04/DOC03/MISC06 findings, not a regression);
  grid-filter keyword (`Find Object Row By Filter`) confirmed fired 15 times via output.xml grep;
  zero inline DB-verify calls confirmed via grep on the final `.robot` file.

## Done wrong / lessons

**This is the single most important fact about Meter's conversion history — recorded honestly,
not softened or buried.**

Earlier in the SAME working session that eventually produced PR #554, Meter was **wrongly
classified as "does not fit the Area pattern."** That first, incorrect call happened because the
insert form's Delivery Point popup — a mandatory field on the insert form driven by the generic T1
`Pick From EC Object Popup` gesture, wired to an EC framework object-popup IFRAME, not a plain
dropdown — was conflated with the screen's actual navigator. Seeing a popup-driven mandatory field
sitting where a straightforward dropdown was expected led to the premature "doesn't fit" call
before the navigator itself had been properly, separately re-examined.

A deeper live re-investigation corrected this. Re-scanning the navigator on its own (independent
of the insert form) found it is exactly **one mandatory dropdown** — Business Unit, at
`nav:form:G:0:R:1:C:1:dd` — structurally identical to Area's own single Production Unit navigator
dropdown. A second dropdown in the same navigator row (`C:2`, labelled "Delivery Point") looks
superficially similar to the popup field by name but is a completely separate, **optional** grid
filter (GO succeeds with only C:1 filled, confirmed live) — not a duplicate of the insert-form
popup and not a blocker either way.

Once that correction was made, the two things that had been wrongly merged into one judgement were
properly separated:
- The **navigator** (Business Unit dropdown) — genuinely Area-shaped, gates the conversion.
- The **Delivery Point popup** — a separate, orthogonal, insert-form-only field, unrelated to
  navigator shape, and already fully solved by the existing generic T1 popup gesture (same
  situation as Chemical Stream's own From Connection popup, which likewise did not block that
  screen's Area-pattern conversion).

Lesson: a mandatory field that happens to use an unusual widget (a popup instead of a dropdown)
on the INSERT FORM says nothing about whether the screen's separate NAVIGATOR section matches
Area's shape. The two must be evaluated independently — do not let an unusual insert-form
mechanism bias the navigator-shape classification.

## Blockers -> resolution
- No hard blockers during the corrected build. The popup mechanism itself (JS-click race with the
  dialog mask, row match by value/innerText not XPath `@value`) had already been solved in the
  original 2026-06-13 build (`docs/meter_popup_notes.md`) and needed no rework here — only the
  surrounding TC/properties-file structure changed.

## Decisions
- No shared T1/T2 edits; only additive `resources/credentials.py` entries.
- Isolated worktree (`C:/tmp/wt-meter`), explicit-path `git add` (no `git add -A`).
- Popup mechanism preserved exactly as-is; only the surrounding structure moved to the
  properties-file-driven pattern.

## Evidence
- Live run: 5/5 pass (`EC_HEADLESS=true robot .../meter_iud.robot`) — TC01 Verify Clean State,
  TC02 Insert, TC03 Update, TC04 Find, TC05 Delete (PR #554, 2026-08-26).
- DB self-clean: `SELECT COUNT(*) FROM OV_METER WHERE CODE LIKE 'AUTOTEST_METER%'` = 0, before and
  after the live run, each via a fresh independent oracledb connection.
- This backfill (2026-08-27): re-ran the live suite once more for evidence capture — see
  `evidence/` and `CHECKLIST.md` for the fresh run's own citations.
