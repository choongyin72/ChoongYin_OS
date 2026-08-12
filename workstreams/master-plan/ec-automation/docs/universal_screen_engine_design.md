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

**Remaining, not yet investigated (low priority):** two isolated `unknown_after_probe` fields (Area's
"System of Measurement" dd; N1's first cascade nav dd `G:1`, while `G:2`-`G:4` resolved fine).

**Batch 1 final tally: 12/12 screens now classify cleanly** (after the toolbar fix + the naming-mismatch
correction), modulo the 2 low-priority isolated field findings above.

**Recommended next steps (not yet done):** (a) investigate the two isolated `unknown_after_probe`
fields; (b) continue Batch 2+ through the remaining ~159 registry screens, stripping client-context
descriptors from screen names first; (c) only then move to Phase 2 (interaction layer).
