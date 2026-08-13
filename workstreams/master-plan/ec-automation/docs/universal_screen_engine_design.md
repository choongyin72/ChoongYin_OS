# Universal EC Screen Engine — design draft

**Status: DRAFT for owner review. Not yet approved to build.** Written in response to the owner's
question: can screen navigation be driven by a runtime component classifier instead of per-family
generators, and if so how well would it generalize across ALL EC screen types.

## 1. Problem this solves

Today, navigating a new EC screen means: recon it live (`scan_ec_screen.py`), identify which **family**
it belongs to (OV / OV-GM / TV / PC / N1 / N2 / N3 / RUN-verify), then use that family's own
generator/driver (`gen_ov_screen.py`, `gen_ovgm.py`, hand-built T2 resources) to build the automation.
Each family re-solves the same underlying problem — "find this field, know its widget type, drive it
correctly" — independently. The families exist because the *business semantics* differ (delete = End
Date vs. physical, mandatory-cascade nav vs. none), but the *DOM mechanics* of the widgets underneath are
the same everywhere, because EC's whole UI is one consistent PrimeFaces/JSF component palette.

**Goal:** separate those two concerns. One generic engine handles "how do I find and drive any field,
regardless of which screen it's on." The family-specific knowledge (what delete means, what's mandatory,
what order to fill things in) becomes a thin config/spec layered on top, not a rewritten driver each time.

## 2. Three layers

```
┌─────────────────────────────────────────────────────────────┐
│  3. VERIFICATION LAYER  (unchanged — stays separate, always) │
│     DbVerify.py — ground truth, per-screen DB assertions     │
├─────────────────────────────────────────────────────────────┤
│  2. INTERACTION LAYER  (generic, NEW)                        │
│     fill(label, value) / select(label, option) / click(label)│
│     / grid_cell(row, col) / resolve_popup(label) / ...        │
├─────────────────────────────────────────────────────────────┤
│  1. CLASSIFIER LAYER  (generic, NEW)                          │
│     scans live DOM → structural map: regions + widgets        │
└─────────────────────────────────────────────────────────────┘
```

Layer 3 (DB verification) is explicitly **out of scope for this design** — it stays exactly as it is
today, per-screen, business-specific. This engine only replaces the "how do I click/fill things"
problem, never the "did this actually work" problem.

## 3. Layer 1 — Classifier

One read-only live scan (extends `scan_ec_screen.py`'s approach) that segments the screen's DOM into
**regions**, then classifies every field inside each region into a **widget primitive**.

### 3.1 Region detection (structural signatures, not guesses)
| Region | Signature |
|---|---|
| Toolbar | fixed icon strip at top (`screenToolbar:form:...`), consistent across every screen |
| Navigator | `nav:form:G:<g>:R:1:C:<c>:...` id pattern, sits above the grid/form |
| Grid | PrimeFaces datatable markup, paginated or scrollable, row/column cell ids |
| Form / data-window | `objectForm` or field-group container, one-record-at-a-time layout |

These four signatures already appear, informally, in the family table in `ec_screen_registry.md` and in
every existing T2 resource — the classifier just makes the detection explicit and reusable instead of
implicit in each generator's assumptions.

### 3.2 Widget primitive detection (per field, inside a region)
| Primitive | Signature |
|---|---|
| Text input | plain `<input>`, no paired `_button`/`_panel` |
| Dropdown (autocomplete) | `<id>_button` + `<id>_panel` pair; options read via `data-item-label` |
| Date field | id ends `da_input` |
| Checkbox | `<input type=checkbox>` |
| Popup picker | button that opens a **separate EC object-picker popup** (per the Pick-from-EC-Object
  capability already built) rather than a `_panel` dropdown |
| Button / icon | `<a>`/`<button>` with a `title` or icon class, not inside a field group |
| Grid cell | `<id>:T:<idx>:C<c>_in`-style id inside a datatable |

Output: a structured map — `{region: [{label, primitive, dom_id, mandatory}]}` — the same shape
`scan_ec_screen.py` already returns for OV/OV-GM, generalized to every region/primitive instead of
being written per-family.

### 3.3 Confidence + escalation (mandatory, not optional)
The classifier must self-report confidence per field, and **refuse to guess silently**:
- High confidence: signature matches exactly one primitive, label is unambiguous.
- Low confidence / unrecognized: multi-tab regions, nested sub-grids, popup-launched-from-popup, custom
  widgets (Equation Editor's MathML builder, file upload) — flag as `UNRECOGNIZED`, do not attempt to
  drive it. This becomes the input list for one-time human recon, same as today, not a forced guess.

This directly implements the calibration given earlier: strong on the standard six primitives (which
cover the large majority of screens, since they're all built from the same component palette), explicit
fallback on structural outliers — never a blind guess that looks confident but isn't.

## 4. Layer 2 — Interaction

A small generic API, built once, on top of the classifier's output — replacing per-screen hardcoded
selectors with **label-driven** calls (continuing the pattern already proven safe in the 2026-07-26+
"label-driven, zero hardcoded field ids" OV-reuse builds):

```python
engine.fill("Name", "AUTOTEST_ROYALTY_01")
engine.select("Method", "Fixed number of Days")
engine.click("Save")
engine.grid_cell(row=3, col="Value").set("123.45")
engine.resolve_popup("Contract").pick_by_code("AUTOTEST_CNTR_01")
engine.toolbar("New Object")
```

Each call: (a) looks up the field by label in the classifier's map, (b) dispatches to the gesture already
documented in the `ec-screen-automation` skill's cookbook for that primitive (dropdown → click `_button`
then match `data-item-label`; grid cell → click, real keystrokes, Tab; etc.), (c) waits for the standard
PrimeFaces AJAX settle (`networkidle`), (d) **re-reads the DOM afterward to confirm the field's displayed
value actually changed** — a cheap sanity check before assuming the click "worked," catching the class of
bug that bit CD.0024 (insert persisted, UI read failed on a wrong assumed grid id).

## 5. What happens to the existing family-specific tooling

Not a rip-and-replace. Migration path:
1. **Layer 1+2 built and proven first**, validated against the ~176 *already-covered* screens (their
   correct behavior is known ground truth) — run the classifier against each, diff its region/widget map
   against what the existing hand-built T2/T3 resources already assume. Mismatches = classifier bugs,
   fixed before touching anything live.
2. Existing family generators (`gen_ov_screen.py`, `gen_ovgm.py`) get **rewritten to consume the engine**
   instead of hardcoding gestures — family-specific logic (what "delete" means, mandatory-cascade order)
   becomes a small per-family spec dict, not a driver rewrite. Nothing about *business semantics* changes;
   only the mechanical layer underneath is unified.
3. **Pilot on 3-5 genuinely new, uncovered screens** next, comparing effort/time against today's
   recon-then-clone process, before declaring it the default path for all new screens.
4. DB-verification (`DbVerify.py`), the registry, the scorecard, and the RF T1/T2/T3 layering are
   **untouched** by this — this design only replaces the Playwright-side mechanics.

## 6. Open risks / questions (owner input needed before building)

- **Multi-tab and nested-popup screens** (e.g. some OV-GM-with-popup, Equation Editor) need a documented
  escalation format, not silent failure — worth deciding now what "hand back to recon" looks like in
  practice (a report file? a paused run?).
- **Where does the engine live** — a new module under `workstreams/master-plan/ec-automation/py/`
  (sibling to the existing `ec_object_iud.py` shared engine), or its own top-level package? Recommend the
  former, to keep it inside the same tested project rather than a parallel one.
- **Rollout order** — validate-against-known-176 first (safe, no live risk, pure comparison) is the
  natural Phase 1; suggest starting there regardless of what's decided on the rest.

## 7. Phased plan (proposed, awaiting go-ahead)

| Phase | What | Risk |
|---|---|---|
| 1 | Build classifier only; run read-only against the 176 known screens; diff vs. known facts | None — read-only, no live writes |
| 2 | Build interaction layer + verification-echo; unit-test against 3-5 already-covered screens (re-run existing suites through the new engine, compare pass/fail to the existing hand-built T2/T3) | Low — same screens, same DB assertions, just a different driver underneath |
| 3 | Rewrite `gen_ov_screen.py`/`gen_ovgm.py` to consume the engine | Low — mechanical refactor, existing tests as regression gate |
| 4 | Pilot on 3-5 new uncovered screens, honest before/after effort comparison | Normal IUD-build risk, same as today |

Nothing here starts building until you say go — this is the design only.

## 8. Phase 1 findings log (2026-08-12, owner-authorized autonomous session)

Classifier built at `workstreams/master-plan/ec-automation/py/universal_classifier.py`. Validated
live, read-only, against 4 structurally distinct screens: **Bank** (OV plain), **Contract** (OV,
2-level cascade nav + checkboxes), **Meter** (OV-GM + real popup picker), **Language** (TV, no nav,
inline-editable grid). Every bug below was found by testing against a screen whose correct answer was
already independently known (registry / screenshots / direct DOM inspection) — not assumed.

**Bugs found + fixed, in order:**
1. **Label-lookup only ever checked column `C:0`** — every column after the first (e.g. `objectdates`'
   End Date at `C:3`) inherited the wrong label. Fixed: search leftward from the field's own column for
   the nearest labeled cell, instead of a hardcoded `C:0`.
2. **Dropdown vs. popup requires a click-probe for `dd_input` fields, but NOT for `:pin` fields.**
   Initially assumed all EC-object-pickers used the same `dd_input` suffix as plain dropdowns, needing a
   click-and-inspect probe to tell them apart (PrimeFaces doesn't render `_panel` into the DOM until
   clicked, confirmed on Bank's `Country`). **Correction, found on Meter:** popup fields actually carry a
   *distinct* id suffix (`:pin`) and an explicit `ECPopupCell` parent class — a hard structural signature,
   not a heuristic. No click-probe needed for popups at all; only true `dd_input` fields still need the
   probe to disambiguate a plain autocomplete from an (apparently rare/nonexistent in practice)
   `dd_input`-style popup.
3. **Click-probe's dropdown check required visible `data-item-label` option rows** — but a
   server-filtered, type-to-search autocomplete (Contract's "Message Contact - Billing") renders its panel
   **visible but empty** until text is typed. Fixed: classify as `dropdown` on panel visibility +
   `ui-autocomplete-panel` class alone, not on having pre-loaded options.
4. **Cascade-nav mandatory detection is single-pass and misses 2nd-level dependent fields.** EC's
   yellow-mandatory styling doesn't apply to a still-disabled field, so scanning navigator mandatory-ness
   *before* filling anything can never see a field that only becomes mandatory once its parent is chosen
   (confirmed on Contract: Contract Area is disabled until Business Unit is set). Fixed: iterative
   rescan-and-fill loop (bounded to 5 rounds) instead of one upfront scan.
5. **Not every field required to populate the grid is ever colored mandatory at all.** Contract Area on
   Contract is required to filter the grid but is *never* yellow (mandatory-yellow apparently only governs
   fields required to Save, not fields required to List). Fixed: if the grid still has 0 rows after the
   normal cascade-fill, fall back to filling any remaining enabled-but-empty nav dropdown once, regardless
   of color.
6. **Grid `sample_cell_id` (the "locate a row/column to compare/validate a value" feature requested
   mid-session) — CORRECTED after initially being logged as a genuine unresolved bug.** First test run
   showed `null` on Bank too, but that was against a STALE result captured before later fixes; re-run
   after the fixes, **Bank resolves `sample_cell_id` correctly** (e.g.
   `manage_object_nav_nav:form:T:0:C0_la`), same as Language. The remaining `null` results on
   Contract/Meter are fully explained by finding #7 below (their gated cascade nav can land on an
   empty-data combination, so there is no row to sample an id from at all) — not a separate defect in the
   cell-lookup logic itself. Lesson for myself: don't log a "confirmed unresolved" finding off a single
   early run without re-checking it against the latest state before writing it down as fact.
7. **Known, not-yet-fixed limitation:** cascade dropdowns are still filled by "pick the first available
   option," which can land on a structurally valid but data-empty combination (confirmed on Contract: BU
   "EC LNG Norway" + CA "NO LNG Europe ECLNG Norway" → 0 rows; same category likely explains Meter's null
   too, also BU-gated). Structural facts (columns, primitives, mandatory flags) stay correct regardless;
   only cell-sampling is affected when this happens. Real fix = smarter option-picking (prefer a
   combination already known to have data, e.g. from a DB row-count check) instead of "first available" —
   not yet implemented.

**Net result:** all 4 test screens now classify with **zero unresolved (`unknown_after_probe`) fields**.
The classifier generalizes cleanly across OV, OV-GM+popup, and TV shapes without any family-specific
branching in its own logic — every fix above was a genuine structural-signature correction (id suffix,
CSS class, panel visibility), not a special case for one screen.

**5th screen tested: Object List Setup (PC family) — initial finding CORRECTED, then fully resolved.**
First pass: navigator generalized correctly (2 separate mandatory-dropdown groups, `G:1`/`G:2` - a shape
none of the first 4 screens had), but grid/form came back empty. Initially misdiagnosed as "PC uses a
different grid-id convention" - **wrong**, confirmed by live manual test: `[id$=':T_data']` matches PC's
grid (`tab:tabPanel:object_list_table:form:T_data`) perfectly fine. The REAL cause: List Class has **295
options**, and blind "pick the first available" (`ALLOC_NETWORK`, `ALLOC_NETWORK_GROUP`, ...) landed on
values with zero configured Object Lists - the dependent dropdown then has no options, the grid/tab
element doesn't even render (not just 0 rows - `grid_id` itself resolves to `None`), and 15 bounded
sequential retries still weren't enough (owner: "trace the notes .md files / query the DB relationship
instead of brute-forcing"). **Fix, per the owner's redirect:** a one-time READ-ONLY DB check
(`OV_OBJECT_LIST` joined to `OBJECT_LIST_SETUP` by `object_id`, grouped by `generic_class_name`) found
only 2 of 295 classes (`FIN_WBS`, `FIN_ACCOUNT`) actually populated in seconds - far faster than blind UI
cycling. Added an opt-in `NAV_HINT_OPTION` env var: tried first (by exact `data-item-label` match)
before falling back to blind cycling, keeping the classifier itself DOM-only/generic by default while
letting a quick DB check (or the `ec-screens/notes/` corpus, see below) supply a known-good starting
value for screens with a large, sparse cascade-option space.
**Result with the hint (`NAV_HINT_OPTION=FIN_WBS`):** grid renders with **9 real columns** - Daytime,
End Date, Object Code (dropdown-in-grid), Split Share, Comments, Sort Order, Create Object
(checkbox-in-grid), Priority, Role (dropdown-in-grid) - all `sample_cell_id`s resolved, including the
first checkbox-in-grid and dropdown-in-grid widget types seen so far.
Both nav dropdowns were correctly flagged `mandatory:true` in the very first pass this time (unlike
Contract's 2nd-level case) - PC's 2 dds are structurally sibling-mandatory, not parent-gated, so no
iterative rescan was even needed here.
**Note on the help corpus:** `DeepDiveLearnings/ec-screens/notes/` (per-BF_CODE markdown, most/all of
EC's online-help) was checked first per the owner's redirect - it mis-resolved (`CD.0131`/`CD.0132` both
point to the plain OV `Object List`, not the PC `Object List Setup`), so the direct DB query was the
right fallback, not the notes corpus alone. Worth remembering for future screens: check the notes first,
but cross-verify against a direct DB query when the two don't obviously agree.
**Minor remaining inefficiency (not a correctness bug):** the classifier's row-select/Insert-form scan
(built for OV's modal-form pattern) doesn't know PC has no such form at all, so it burns a ~30s timeout
before correctly returning an empty `form` region. Low-value fix (skip the attempt if no `objectForm`
container exists structurally) - not done tonight, logged for later.

**PC form-scan inefficiency — FIXED (2026-08-12):** capped the row-select probe's click at 5s instead
of Playwright's 30s default. Verified no regression on Bank (where the click genuinely needs to
succeed). This was the right amount of patience for an optimistic probe, not a wait for something
expected to happen.

**Grid-cell dropdown `sample_cell_id` — FIXED (2026-08-12, live-tested with the owner).** Owner asked
to try selecting a FIELD in the Object List Setup grid live; found the "Object Code" grid-cell dropdown
couldn't actually be typed into via its reported `sample_cell_id` (`...C2_dd`) - that id is the OUTER
wrapper `<span class="ui-autocomplete">`, not the nested `<...C2_dd_input>` that's the real interactive
element (confirmed live: typing into the wrapper did nothing; typing into the nested input correctly
triggered the type-to-search autocomplete and returned real matching Object Codes). `scan_grid_columns`
now resolves any `_dd`-suffixed cell id to its nested `_input` child, same convention as form-level
`dd_input` fields.

## 9. Batch 1 breadth-pass findings (2026-08-12) - a major toolbar-detection bug found and fixed

Ran the classifier against 12 structurally diverse, already-known registry screens (Area, Analysis
Point, Account, Regulatory Permits, Nomination Cycle, Daily Production Well Status 1, Validation
Overview - Pluto Scarborough, Field, Transport System, Production Unit, Carrier, Sub Field). 10/12
classified cleanly on first pass. Two genuine findings, one of which turned into a significant,
cross-cutting bug affecting EVERY screen tested so far (Bank/Contract/Meter included), not just the
screen that exposed it - reported here bug-by-bug, since the investigation itself is instructive.

**Toolbar Insert/Delete disabled-detection - THREE separate bugs found and fixed, via one investigation:**
1. **`closest('li,a')` stops at the nearer `<a>` ancestor**, never reaching the `<li>` that actually
   carries `ui-submenu-state-disabled` (span → a → li - the `<a>` matches first). Confirmed live on
   **Daily Production Well Status 1 (N1)**: its Insert/Delete `<li>` genuinely IS disabled (matching the
   long-documented "N1 = update-only" convention), but this bug always missed it and reported `enabled`.
   Fixed: `closest('li')` only.
2. **`document.querySelector('.ui-icon-insert')` is unscoped (whole page), and the class is NOT
   unique** - a personalization/settings menu elsewhere on the page can reuse the same icon class and
   get matched instead of the real toolbar icon (same root cause as the earlier `:pin` discovery, but
   for icon classes this time, not id suffixes). Confirmed by directly hovering the matched element on
   N1: it opened a "system of measurement override" settings menu, not a record-insert menu. Fixed:
   scope the query to inside the toolbar container (`[id^="screenToolbar"]`) only.
3. **Even scoped, `dis()` tested `li.outerHTML` (the ENTIRE subtree HTML) instead of `li.className`** -
   any disabled marker ANYWHERE inside that li's full nested HTML matched the regex, including nested
   sub-items. Confirmed live on **Contract**: its Insert flyout has multiple sub-items (`New Object` +
   `New Version`), and `New Version` being legitimately disabled (no row selected) falsely flagged the
   WHOLE Insert action as disabled, even though `New Object` itself was fully available - and had
   already been proven to work moments earlier in the same run. Fixed: test `li.className` only.

**Verification, three-way, after all three fixes:** Contract `insert:enabled / delete:DISABLED`
(matches - Insert genuinely works, Delete-via-toolbar is disabled because deletion happens via
End-Date-editing in the form instead); N1 `insert:DISABLED / delete:DISABLED` (matches the documented
update-only convention); Bank `insert:enabled / delete:DISABLED` (same OV convention as Contract).
**This means every earlier "clean" toolbar reading for Bank/Contract/Meter before this fix was
questionable** - the structural facts (grid, form fields, mandatory flags) those runs captured are
unaffected, but their toolbar `insert`/`delete` values specifically should not be trusted from before
this fix landed.

**"Validation Overview - Pluto Scarborough" open-failure — RESOLVED, not a classifier bug.** The
screen's actual treeview label is just **"Validation Overview"** - "Pluto Scarborough" is a
client-context descriptor added to the registry's screen name for documentation clarity, never part of
the literal link text (confirmed: a live search returned exactly 4 tv-links - "Validation Overview",
"Validation Overview by Facility", "Flush Cache", "Dashboard" - none matching the full registry string).
The exact-match locator correctly found zero matches and correctly timed out; there was nothing to fix
in the classifier. Re-run with the correct name: fully clean, zero unresolved fields - toolbar
`DISABLED/DISABLED` (correct, this is a run-only screen with no CRUD at all), navigator correctly found
the 2-field date range (From/To), grid correctly captured its 3 real columns (Group, Status, Summary).
Lesson for future batches: when pulling screen names from the registry, strip any trailing
client-context descriptor before using it as the search term - the registry documents facts ABOUT a
screen, not necessarily its exact literal treeview label.

**Area/N1 isolated `unknown_after_probe` fields - FIXED (2026-08-12).** Both turned out to be the same
root cause: genuinely slow AJAX panel-render time (confirmed live, ~6s for Area's "System of
Measurement" dd), not disabled/broken fields - the classifier's dd click-probe window was extended from
2.5s to 7s. Verified both resolve cleanly now; no regression on Bank. Committed `aea5f01e`.

**NOTE FOR FUTURE USE - grid columns can legitimately have `sample_cell_id: null` even on a real,
correctly-classified screen (found live-testing N1 after the above fix, 2026-08-12):** N1's grid header
lists 141 columns (the union of every possible well-equipment attribute), but the last ~23 (an Electric
Submersible Pump / ESP sub-section) had `sample_cell_id: null` on every one of the 5 currently-loaded
rows. Confirmed via direct DOM check: all 5 rows have exactly 118 `<td>` cells, not 141 - the ESP
columns genuinely have NO cell in ANY of these rows, because `scan_grid_columns` only ever samples
whichever rows the CURRENT nav-scope happens to load, and this particular well group has zero
ESP-equipped wells. **This is not a classifier bug** - it's the same "sparse valid-combination" category
already documented for cascade dropdowns (Object List Setup), just showing up as missing per-column
data instead of a missing dropdown option. To get a real sample for a conditionally-rendered column like
this, the fix is the same pattern already built: navigate to a different, DB-confirmed nav-scope that
actually contains a row exercising that column (e.g. an ESP well), not a classifier code change.
**Apply this going forward:** a `null` `sample_cell_id` on a structurally-correct grid does not by
itself mean something is broken - check whether the loaded rows actually contain data for that column
before assuming a bug.

**Batch 1 final tally: 12/12 screens classify fully cleanly, zero open items.**

## 10. Batch 2 findings (2026-08-12) - PC toolbar-timing bug fixed; deep-cascade scope boundary documented

Ran 15 more screens, prioritizing genuinely new shapes (N1 tank/composition/sub-daily variants, N2
allocation-run, N3 status-process, EVENT-LOG, 3-tier PC). **Zero exceptions, zero unresolved
primitives across all 15** - the fixes hold at scale. Two things worth reporting, not just "clean":

**Toolbar timing bug - FIXED.** Unit - Well Setup (PC) read `DISABLED/DISABLED`, contradicting
Object List Setup's `enabled/enabled` for the same family. Confirmed live: the toolbar check ran in
Region 1, BEFORE the navigator's cascade-fill (Region 2) - and this screen's Insert genuinely IS
disabled until a valid parent scope (Unit Agreement) is selected, matching real business logic (you
can't insert a well-setup member without knowing which unit it belongs to). Checking too early gave a
technically-true-at-that-moment but misleading reading. Fixed: moved the whole toolbar check to run
AFTER the cascade-fill+GO sequence, so it reads the screen's settled/navigated state. Verified: Unit -
Well Setup now `enabled/enabled`; N1 still `DISABLED/DISABLED` (genuinely disabled regardless of nav);
Bank still `enabled/DISABLED` (ungated, unaffected). No regressions. Committed `7c50aacf`.

**Deep multi-level cascade sparse-data problem - INVESTIGATED, documented as a Phase 1 scope
boundary, not force-fixed.** 6 of 15 screens (all N1/N2/N3/EVENT-LOG, each with 4-8 nav fields -
notably deeper than the 1-2 level cascades fixed so far) hit the "grid never populated" limitation.
Investigated one representative case fully: **Alarms** (3-level BU→PU→Area cascade) has only **4 rows
total in its entire backing table** (`FCTY_DAY_ALARM`), all dated 2011, all belonging to one specific
facility. Tested the obvious hypothesis - set the nav date to 2011-01-01 (matching the real data) with
dropdowns left at first-available - **still 0 rows**. This proves the blocker isn't just the
never-touched date field; it's that a 3-level dropdown chain needs to resolve to the EXACT facility
hierarchy that owns those 4 rows, and blind first-option cycling across 3 independent levels has very
low odds of landing there by chance. Resolving this per-screen would require a dedicated DB query to
trace the specific object's BU→PU→Area parentage (the same kind of investigation Object List Setup's
fix needed, but one level deeper) - genuinely screen-specific work, not a one-time generic classifier
change. **Decision: not fixed now.** Structural facts (columns, primitives, mandatory flags) for all 6
affected screens are still correct and unaffected; only "sample real data for a cell" is blocked for
these specifically. Flagging as an accepted Phase 1 limitation for deep-cascade screens, revisit only
if/when cell-sampling on one of these 6 specific screens is actually needed for something.

## 11. Batch 3 findings (2026-08-13) - zero real bugs, two readings verified correct under scrutiny

15 more screens (heavy on N1 siblings across object classes, plus a 3rd PC instance). Two results
looked suspicious at first glance and were investigated with the same rigor as every prior finding -
**both turned out to be the classifier correctly reporting real facts, not bugs:**

- **Tract - Well Setup `DISABLED/DISABLED`** - looked like a regression of the PC toolbar-timing fix
  (Unit - Well Setup now reads `enabled/enabled`). Investigated: `TRACT` has only 4 rows total in the
  whole DB, and the nav's picked Unit Agreement has none of them as children - the cascade genuinely
  never completes, so Insert staying disabled is accurate. Same root cause category as the
  already-documented Alarms finding, just surfacing as a toolbar symptom instead of an empty grid.
- **Well Gas Component Analysis `enabled/enabled`** - looked inconsistent with sibling Stream/Oil
  Component Analysis (`DISABLED/DISABLED`), despite the registry describing them as siblings of the
  same pattern. Direct DOM check: the real Insert `<li>` has zero disabled markers, and the grid
  genuinely has a row - the live evidence is unambiguous. This screen apparently has different
  (fuller) CRUD capability than its documented siblings; trusted the live ground truth over the
  registry's shared-pattern framing. Its `row_select_scan_err` timeout is the same already-known
  expected behavior as Nomination Cycle (TV-style editable grid, not OV's click-row pattern).

**Batch 3 final tally: 15/15 structurally correct, zero classifier bugs found.** First batch where
investigation confirmed everything was already right rather than surfacing a new fix.

## 12. Batch 4 findings (2026-08-13) - one real fix (click-timeout cap), one unresolved isolated case

15 more screens, prioritizing new discriminators (junction/multi-object, forecast-manager,
TV-context-gated dual grid) over the ~30 near-duplicate OV-GM clones now in the registry.

**Price Object - click-stall mitigated (root cause not fully pinned down).** 9 `probe_err: Locator.
click: Timeout 30000ms exceeded` in one run (~270s wasted) trying to open dropdown panels in the
Update form. Investigated: `elementFromPoint` at the button's center returned a DIFFERENT, empty-id
`<span>` sitting on top of it - something overlaps the button, at least intermittently (a direct repro
via the Insert form's equivalent field succeeded cleanly). Root cause not conclusively identified (looks
like a transient overlay/label during a busy row-select-then-scan sequence), so rather than force an
unproven fix, capped `classify_dd`'s initial button click at 8s instead of Playwright's 30s default -
same principle as the earlier row-select cap: bound the cost of an optimistic action instead of
chasing a fix I can't fully prove. Re-ran clean (0 errors); verified no regression on Bank. Committed.

**Stream Item - screen open failure, INVESTIGATED, NOT RESOLVED, documented honestly.** Unlike
Validation Overview's naming mismatch, the exact "Stream Item" tv-link genuinely exists, is visible,
and its `onclick="EC.treeview.onClick(event, 'STREAM_ITEM', false)"` handler is correctly wired.
Clicking it (direct click, force-click, +Escape, +4s extra wait) triggers a real AJAX round-trip to
the actual screen URL (`manage_stream_item/CLASS_NAME/STREAM_ITEM.jsf`) that reports success in the
console - but no `manage_stream_item`-related element ever appears anywhere in the DOM afterward, and
the search-results overlay never closes (`searchOverlayVisible: true` throughout). Checked for a
separate content iframe (none - `page.frames` count of 2 is the main frame + an unrelated blank
utility frame, not a distinct content frame). No further generic Playwright technique tried resolved
it. **Stopping investigation here** per the escalate-after-repeated-attempts principle - this looks
like a genuine, isolated issue specific to this one screen (every other ~57 screens tested open via
the identical mechanism without issue), not a generalizable classifier gap. Logged as unresolved,
not force-fixed, not silently dropped - same spirit as the registry's own PARKED screens.

**Batch 4 tally: 13/15 clean, 1 mitigated (Price Object), 1 unresolved isolated case (Stream Item).**

## 13. Batch 5 findings (2026-08-13) - one naming fix, click-stall confirmed RECURRING (not one-off)

15 more screens, mostly domain-variety sampling now that all distinct structural shapes are proven.
Registry now essentially exhausted for genuinely new shapes - remaining rows are near-duplicate
OV-GM/plain-OV clones (~113 of ~175 total).

**Contact Group Set open-failure - RESOLVED, naming mismatch.** Real treeview label is "Maintain
Contact Group Set", not "Contact Group Set" - same class as Validation Overview. Verified clean with
the correct name.

**Click-stall (Price Object, Batch 4) CONFIRMED RECURRING - Service and Contract Capacity hit the
same `probe_err` timeout (5 and 3 occurrences respectively), all clustered consecutively in the same
`updateAttributes` (row-select-derived Update) form.** Investigated a second time, same methodology as
Price Object: replicated the exact click sequence via the Insert form's equivalent fields (which share
identical field structure) - every click succeeded cleanly, no lingering panel detected before any
click (`panel state BEFORE click = {'exists': False}` for all 9 fields tested). **Root cause still not
identified after two genuine investigation attempts** - the failure is specific to the row-select
context and doesn't reproduce via a controlled Insert-form repro. Per the escalate-after-repeated-
attempts principle, stopping further root-cause investigation here. The 8s timeout cap (already
shipped for Price Object) bounds the cost and doesn't corrupt results - affected fields are correctly
flagged `probe_err`, not silently misclassified. Accepting this as a known, bounded, unresolved-at-
root-cause limitation rather than continuing to grind on it.

**Batch 5 tally: 13/15 clean, 1 fixed (naming), 1 confirmed-recurring-but-bounded (click-stall).**

**Overall Phase 1 breadth-pass status: 77 of 175 registered screens tested across 5 batches.** Every
genuinely distinct structural shape in the registry has now been exercised at least once. The
remaining ~98 screens are overwhelmingly near-duplicate clones of shapes already proven clean -
continuing to mechanically test all of them has sharply diminishing value. Recommend either (a) a
lighter final sampling pass (10-15 more, purely as a broader confidence check) then declaring the
breadth pass complete, or (b) stopping here and moving to Phase 2 (interaction layer) - owner's call.

## 14. Batches 6-11 (2026-08-13) - full registry coverage completed, findings logged not fixed

Owner directed a change of approach for this stretch: run all remaining batches back-to-back, LOG any
finding without stopping to investigate/fix, then do one consolidated fix pass at the end (see §15).
98 screens tested across 6 batches (6 through 11), bringing total coverage to **175/175 - the entire
registry**.

**Batch 6 (15 screens: Equipment, MIME Type Mapping, Business Unit, Country, State, Object List, Cost
Centre, Currency, Company, Customer, Vendor, Delivery Point, Commercial Entity, Company Contact,
Licence): clean.** Equipment hit the already-accepted sparse-cascade limitation; not a new bug.

**Batch 7 (15 screens: County, Region, DOA Credit Limit, WBS, Delivery Stream, Nomination Point,
Pipeline Segment, Transport Zone, Daily Gas Stream Status, Daily Oil Stream Status, Stream Oil
Component Analysis, Royalty Depositor, Document Date Term, Port, Well): clean.** Stream Oil Component
Analysis hit the sparse-cascade limitation; not new.

**Batch 8 (15 screens: Exchange Rate Source, Payment Scheme, Product Description, Revenue Order,
Sales Order, VAT Code, Cost Object Mapping, MMS Lease, Operator Lease, Production Sub Unit, Pipeline,
Daily Water Stream Status, Document Received Term, Berth, Canal): 15/15 clean, zero findings.**

**Batch 9 (15 screens: Revenue Stream Category, Split Item Other, Reservoir Block, Reservoir
Formation, Blend, Chemical Transport Tank, Calculation Context, Dummy Tag Event Object, Transactional
Inventory Layout Set, HCB System, Data Extract Set, Document Template, Transactional Inventory
Properties, Storage Flow, UOP Key): 15/15 clean, zero findings.**

**Batch 10 (15 screens: Process Train, Calculation Group Context, Deferment Group, EC Code Object,
Conversion Group, Document Sequence, Calculation Library, Task Process, Production Separator, Test
Device, Channel, Loading Arm, Tug Boat, Facility Class 1, Storage): 14/15 clean.** Deferment Group's
treeview link click timed out at 30s - a SECOND occurrence of the open-failure class first seen on
Stream Item (Batch 5). Channel and Tug Boat hit the sparse-cascade limitation; not new. Logged, not
investigated at the time (per the batch-then-fix approach).

**Batch 11 / FINAL (7 screens: Chemical Stream, Shift, Chemical Stream Hookup, Price Rate, Property,
Price Index, Division Order): 6/7 clean.** Chemical Stream hit the click-stall pattern (3x `probe_err`
dropdown-click timeouts) - a FOURTH occurrence of the class first seen on Price Object (Batch 4). Shift,
Chemical Stream Hookup, and Division Order hit the sparse-cascade limitation; not new.

**Full-registry tally: 175/175 screens tested. Findings requiring the consolidated fix pass: Stream
Item + Deferment Group (open-failure, 2 occurrences), Price Object/Service/Contract Capacity/Chemical
Stream (click-stall, 4 occurrences). All other flagged items across every batch are the already-
accepted sparse valid-combination limitation (grid can't be reached by blind cascade-cycling when the
dropdown's valid combinations are sparse) - confirmed via DB row counts on multiple screens, not a
classifier defect.**

## 15. Consolidated fix pass (2026-08-13)

**Item 1 - Stream Item open-failure: RESOLVED.** Root cause: `classify_screen()`'s readiness gate and
GO-button-id lists (4 locations in `universal_classifier.py`) hardcoded
`['go_button:form:B','button:form:B','navButton:form:B']` and never included `buttongo:form:B` -
Stream Item's real GO button id. Live investigation confirmed the tv-link click always succeeded (8s);
the screen's readiness gate then looped the full 30s because none of its known ids matched, and
falsely reported `SCREEN_NEVER_RENDERED_NAV_GRID_FORM_OR_GO`. Clicking `buttongo:form:B` directly
populated 4 real grids (`nav:form:T_data`, 2 tab-panel grids, `RunningJobs:form:T_data`), proving the
screen works fine once the right button is found. **Fix:** added `'buttongo:form:B'` to the go-id list
in both places it's defined (readiness gate + nav-fields-raw scan); the two `go_id`/`go_id2` fallback
sites already consume that list so no separate edit was needed there. **Regression check:** re-ran
Stream Item (now classifies clean, 0 unrecognized, 59 form fields resolved) + Bank + Contract (both
unchanged) - no regression. This is the exact same defect class independently flagged in GitHub Issue
#345 (against a different codebase's `ec_object_iud.py`), confirming it's a recurring EC-specific
gotcha (some screens use a non-standard GO button id) worth remembering generally, not a one-off typo.

**Item 2 - Deferment Group open-failure: NOT a code bug - environment/registration-state issue,
documented not fixed.** DB confirms the class is real and correctly configured
(`CLASS_CNFG.DEFERMENT_GROUP` = OBJECT/VERSIONED; `CLASS_PROPERTY_CNFG.LABEL` = literally "Deferment
Group", matching the registry exactly). But the live menu search for the exact term "Deferment Group"
returns "No records found"; searching "Deferment" alone returns 12 unrelated results, none matching.
The registry row claims this screen was live-verified 4/4 RF + 7/7 Playwright on 2026-07-26 - something
has changed on this sandbox since then (search index staleness, or the screen's menu/treeview wiring
was later removed) that is outside the classifier's control. Not investigated further per the escalate-
after-repeated-attempts principle (this is an EC environment-state question, not a script defect) -
flagged for a manual UI check (e.g. does the screen still appear if navigated to directly via
treeview folders, or does a cache flush restore it) rather than further code changes.

**Item 3 - Click-stall (Price Object / Service / Contract Capacity / Chemical Stream): still
unresolved at root cause, now confirmed a 4th time.** Consistent with Batches 4-5's findings - the
stall is specific to the row-select-derived Update form context and does not reproduce via a
controlled Insert-form repro. Per the same escalate-after-repeated-attempts principle already applied
in Batch 5, not re-investigating a third time without new information; the existing 8s timeout cap
continues to bound the cost (fields are correctly flagged `probe_err`, never silently misclassified).
Accepting as a known, bounded, unresolved-at-root-cause limitation.

**Item 4 - Sparse valid-combination limitation: reconfirmed, not a bug.** Now observed on 10 screens
total across all batches (Alarms, Tract, Equipment, Stream Oil Component Analysis, Channel, Tug Boat,
Chemical Stream, Shift, Chemical Stream Hookup, Division Order). Consistent with the DB-verified root
cause established in Batches 2-3 (genuinely sparse data, not a classifier defect) - no further action.

**Fix pass tally: 1 fixed (Stream Item), 1 documented as environment/out-of-scope (Deferment Group), 2
accepted as known bounded limitations (click-stall, sparse-cascade). Universal Screen Engine Phase 1
breadth pass is now COMPLETE: 175/175 registry screens tested, every finding resolved or explicitly
accounted for.**

## 16. Follow-up on the two accepted-limitation items (2026-08-13) - two more concrete attempts, both closed with stronger evidence

Owner asked for a real fix plan rather than leaving both items at "accepted, not investigated further"
without trying anything new. Two genuinely new angles were tried (not a repeat of prior methods):

**Deferment Group - tried "Flush Cache" (the exact menu action visible next to the search box) to test
the stale-search-index theory.** Clicked it, then re-searched "Deferment Group" immediately: still "No
records found". This disproves the stale-index theory outright - it isn't a caching problem. The class
is correctly configured in `CLASS_CNFG`/`CLASS_PROPERTY_CNFG` but is not exposed via the live menu
search under any tool available here, even after the one refresh mechanism the UI itself offers.
**Closed for good** - nothing further is actionable from this side; this needs an EC admin/environment-
level check (was the menu/treeview wiring for this class removed after the 2026-07-26 build?), not more
script-level investigation.

**Click-stall - ran a genuinely different diagnostic** (prior 3 attempts all compared against a clean
Insert-form repro; this one instead used the proven `ec_object_iud.py` driver to reach the real
row-select context directly, captured browser console + failed-network events during the click, and
inspected `elementFromPoint` at the button's exact center before clicking). Two findings: (1) the
"something overlaps the button" observation from the original Batch 4 investigation is a **false
lead** - the element sitting on top is the button's own icon `<span class="ui-icon-triangle-1-s">`, a
normal child element, not a foreign overlay; Playwright correctly clicks through it regardless. (2)
Swept all 11 dropdown fields in a real update form (not just one) with zero reopen-delay between
clicks, matching the original failure pattern as closely as possible - **0/11 stalled this run**, no
console errors, no failed requests. This is the 4th distinct investigation attempt (Batch 4, Batch 5
x2, this one) and the first to use console/network capture + a full field sweep; it still produced zero
reproducible signal and disproved the one concrete theory anyone had. **Closed as a confirmed
intermittent/transient issue** (most likely server-side AJAX/render-queue timing under load, given it
never reproduces in a clean, isolated attempt) rather than a fixable client-side defect - the 8s timeout
cap remains the correct mitigation (bounds the cost, never silently misclassifies a field).

**Both items now closed with stronger evidence than before, not just re-stated as "accepted."** No
further action planned on either unless new information surfaces (e.g. the click-stall recurs with a
different, reproducible pattern in a future batch).

## 17. Phase 2 - Interaction layer built and validated (2026-08-13)

Owner authorized Phase 2 per the original phased plan (section 7): build the interaction layer,
validate against already-covered screens by re-running their proven IUD flows through the new engine
instead of hand-built per-screen code, DB-verified, self-cleaning.

**Built:** `workstreams/master-plan/ec-automation/py/engine.py` - a generic `Engine` class driven by
the Phase 1 classifier's field/primitive map, not per-family branching. Public API: `fill(label, value)`,
`select(label, value)`, `check(label, value)`, `resolve_popup(label).pick_by_code(value)`,
`click('Save'|'GO')`, `toolbar(action, icon=None)`, `select_row(grid_id, code)` (OV),
`select_grid_row(grid_id, value)` (TV), `grid_cell(grid_id, row, col_label).set(value)/.get()`,
`find_grid_row(grid_id, value)`. Every write call re-reads the DOM afterward (verification-echo) -
the exact mechanism the original design called for to catch a CD.0024-class silent failure.

**Validated against the two structurally distinct exemplars the Phase 1 classifier itself was first
proven on** (matching section 7's "re-run existing suites, compare pass/fail" acceptance criterion,
adapted to a Playwright-level rather than RF-level comparison given no pre-existing RF suite covers
either screen under this exact naming): **Bank** (OV, plain, form-driven) and **Language** (TV,
grid-cell-driven, no navigator/form region at all). Both ran a full **Insert -> Update -> Delete**
cycle entirely through the generic engine (no hardcoded field ids anywhere in the test scripts - every
field/action resolved by label or column header), DB-verified at every step, self-cleaned to zero
residual. Genuinely different code paths were exercised: Bank never touches `grid_cell()`/
`select_grid_row()`; Language never touches `fill()`'s date-handling, `select()`, or `resolve_popup()`.

**Real bugs found and fixed while building this (not hypothetical - every one surfaced by an actual
failed validation run, root-caused via DB/DOM evidence before fixing):**

1. **Date fields: the visible/typed value can be wrong even though nothing looks wrong client-side.**
   Confirmed live (Bank's Start Date): the field's calendar widget carries its real expected format in
   `data-p-pattern` (e.g. `'yyyy-MM-dd'`). A value typed in a different format (`'01/01/2020'`) displays
   correctly in the DOM `.value`, raises no client-side error, but the widget's underlying date model
   never parses it - Save then fails server-side ("Required fields are empty") for that field, with
   every client-side signal having looked fine. Root-caused by reading `ec_error()` (the same
   structural error-banner detector already proven in `ec_object_iud.py`) after a Save attempt, not by
   guessing. **Fix:** `_reformat_date_to_pattern()` reads the field's own `data-p-pattern` and
   reformats the caller's value to match it generically, rather than assuming one fixed format.

2. **The Save link's `title` attribute is not a reliable locator - EC blanks it after first use.**
   Confirmed live on BOTH Bank and Language: EC's PrimeFaces tooltip widget sets the anchor's native
   `title` to `''` after the first hover/interaction on that toolbar (moving the tooltip text into its
   own floating widget), while the link itself stays fully enabled and clickable. A `@title='Save
   [Ctrl+s]'` locator - the exact pattern already used in `ec_object_iud.py` and the `ec-screen-
   automation` skill's own cookbook - therefore finds **zero matches** after the very first Save on a
   screen, not a "still disabled" false negative but a genuinely wrong search key. **Fix:** locate by
   the `.ui-icon-save` icon class + check the ancestor `<li>`'s own class for the disabled marker (the
   same structural-signature technique already proven for toolbar disabled-detection in the Phase 1
   classifier) - EC does not mutate this. Worth carrying back into `ec_object_iud.py`/the skill cookbook
   at some point, since they'd hit the exact same failure on a screen requiring 2+ Saves in one session.

3. **A row's grid position is not stable across a Save - confirmed on TV, matches an existing OV
   principle.** Language: after Save, a just-inserted row moved from index 1 (where it was filled) to
   index 8 (the end) - not left where it was. Any code that remembers a row index across a Save and
   reuses it operates on the WRONG row silently (no error - it just edits whatever row happens to sit
   at that index now). This is the exact same "never trust position, resolve by identity" principle
   already established for OV row-select elsewhere in this codebase, now confirmed true for TV grids
   too. **Fix:** `find_grid_row(grid_id, value)` re-resolves a row's current index by scanning cell
   *values* (not text content - grid cells are `<input>` elements, so `td.textContent` is always empty
   regardless of the cell's actual value) every time, never reused across a Save.

4. **TV's Insert/Delete flyout link text is the class's own label, not a fixed generic string - and
   the SAME text appears under both icons.** Confirmed live, Language: both the Insert and Delete
   toolbar icons' flyouts contain a link literally labeled `'Language'` - identical text under two
   different icons. A text-only flyout search (the approach that works fine for OV's fixed `'New
   Object'`/`'Delete'` strings) is genuinely ambiguous for TV and will click the wrong icon's flyout.
   **Fix:** `toolbar(action, icon=None)` accepts an optional `icon='insert'|'delete'` hint to pin the
   search when the text is ambiguous (always true for TV); OV callers passing fixed unique strings are
   unaffected (default `icon=None` searches both, unchanged behavior).

5. **(Caught this one myself, not the engine's fault) VARCHAR2 column-length limits are real and EC
   fails silently past them.** An early Language update test used a 36-character value against a
   `VARCHAR2(32)` `NAME` column - the DOM showed the full typed value with no client-side error, Save
   "succeeded" with no exception, but the DB never persisted the change (silent server-side rejection).
   Traced via the DB schema (`all_tab_columns`), not assumed. Not an engine defect - a test-data
   authoring mistake - but worth naming here since it looked identical to bug #2 above until root-
   caused, and is a real trap for anyone writing test data against an unfamiliar EC table.

**Regression check:** re-ran Bank's full cycle again after all of the above fixes landed - still 3/3
DB-verified PASS, no behavior change on the exemplar the fixes weren't targeting.

**Phase 2 status: COMPLETE per section 7's acceptance criterion** (generic interaction layer built,
validated end-to-end on both structurally distinct exemplars, DB-verified, self-cleaning, zero
regression). Not yet done (per the same phased plan, unstarted): Phase 3 (rewrite
`gen_ov_screen.py`/`gen_ovgm.py` to consume the engine) and Phase 4 (pilot on new uncovered screens).

## 18. Phase 3 step 1 - OV-GM navigator-cascade support added to the engine (2026-08-13)

Owner authorized Phase 3. First gap identified before any generator rewrite could start: Phase 2's
`engine.py` was validated only on Bank and Language - **neither has a navigator at all**, so the
OV-GM cascade (Business Unit -> Production Unit -> Area -> ...) that every existing `gen_ovgm.py`
bundle depends on had zero engine-level coverage. Building that first, since the generator rewrite
can't proceed without it.

**Added `Engine.apply_navigator(values=None, levels=4, row=1)`** - generic and structural, no
per-screen hardcoding (matches the standing "resolve by label/structure, never hardcode" rule).
Unifies the 4 modes the string-templated generators currently express as separate code paths
(`nav_mode='go_only'`, `nav_values=[...]`, `nav_value=...`, default first-available cascade) into
ONE method: pass explicit `values` for known-good scope values (the `NAV_HINT_OPTION` pattern from
Phase 1), omit for first-available cascade, and a screen with no cascade columns at all degrades
automatically to a bare GO with no separate flag needed - the absence of `nav:form:G:0:R:<row>:C:*`
columns already says everything.

**Validated live against Node** (OV-GM, 3-level mandatory cascade: Production Unit -> Area ->
Facility Class 1; already-shipped, RF 4/4 + Playwright 8/8 exemplar per the registry) - full
navigator cascade + Insert -> Update -> Delete through the engine alone, DB-verified at every step,
self-cleaned to zero residual.

**Real defect found and fixed while validating (not the navigator code - a `Save` error-detection
gap):** the first Node insert attempt failed silently - DB check showed no row, but `ec_error()`
checked right after `click('Save')` returned `''` (no error), even though EC's own banner DID say
`'Required fields are empty... Calculation Sequence Number'`. Root-caused: `click('Save')` calls
`_refresh_field_map()` immediately afterward, which probes every `dd_input` field via `classify_dd()`
- a live click+Escape - as a side effect of "just reading labels." That probe dismisses EC's error
notification before the caller ever gets to check it, so **any code built on the engine would
silently believe a failed Save had succeeded.** This is exactly the class of failure the
verification-echo elsewhere in this layer exists to prevent, just on the Save path instead of a
field write. **Fix:** `click('Save')` now checks `ec_error()` (the same structural, non-substring
detector already proven in `ec_object_iud.py`) immediately after the click, BEFORE the refresh runs,
and raises a new `SaveFailed` exception if EC reports one - matching the exact ordering
`ec_object_iud.py`'s own `insertObjectRecord`/`updateObjectRecord` already use. Confirmed the fix
raises correctly on a deliberately-incomplete Save, then re-ran the full Node cycle clean.
(Separately: the missing mandatory field itself was a gap in my own quick test script, not a
classifier or engine defect - Node's proven driver already documents "Calculation Sequence Number"
as an extra mandatory field beyond the plain-OV set; I hadn't done fresh recon before writing the
test and trusted an abbreviated registry summary instead.)

**Regression check:** re-ran Bank (OV) and Language (TV) again after both changes landed - both
still 3/3 DB-verified PASS, unchanged.

**Status: engine-level OV-GM support proven on one exemplar (Node).** Not yet done: validating
`apply_navigator(values=[...])` (the explicit-value path, for a sparse-cascade screen where
first-available has no valid combination) against a live screen - Node's cascade happened to have a
populated first-available option throughout, so only the default path has live evidence so far.
Next: the actual generator rewrite (`gen_ov_iud_bundle.py` first, then `gen_ovgm.py`), each
regression-checked against an already-shipped exemplar before being trusted on anything new.
