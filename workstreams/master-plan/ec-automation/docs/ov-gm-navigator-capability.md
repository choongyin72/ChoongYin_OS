# OV-GM gated-navigator capability (item 1)

_Built 2026-07-29. The reusable primitive that unlocks the ~41 OV-GM object screens (grid
`manageObject:form:T_data`), which are navigator-GATED: the grid is empty until a navigator cascade is set + GO._

## The pattern (proven live on Node CD.0006)
1. **Navigator cascade** = autocomplete dropdowns in ONE row across columns: `nav:form:G:0:R:1:C:1..N:dd`
   (e.g. Group B = C1 Production Unit -> C2 Area -> C3 Facility Class 1). Fill **first-available parent->child**
   (child options render only after the parent is chosen), then **GO** (`button:form:B`). The `manageObject`
   grid loads only after this.
2. **Capture the top-parent** (C1 value, e.g. `AS1 EC Exploration Norway`).
3. **Insert:** New-Object form Code/Name/Start + mandatory extras, and set the **parent-dd**
   (e.g. `Op Production Unit` / `Business Unit Name`). Set it to the captured C1 value **if that value is
   an option** in the parent-dd panel; otherwise **first-available** (`__FIRST__`). PER-SCREEN, VERIFY:
   the parent-dd panel is date-filtered and its list can DIFFER from the navigator's (real case: on **Node**
   the Op PU panel offers 5 PUs and the nav first-available `AS1...` is NOT one of them - yet the row still
   lists after GO with first-available Op PU; contrast **Area**, where nav PU == Op PU was required). Never
   assume the nav value is a valid parent-dd option - probe the panel (`tmp/node/probe_op_pu.py`).
4. **Groupmodel check (per screen):** after Save + GO, does the row LIST in the grid? YES -> groupmodel enabled,
   buildable. NO -> groupmodel OFF (insert persists but grid never lists, e.g. Production Sub Unit) -> EXCLUDE.
5. **Lazy redraw:** the GM grid redraws async after Save+GO -> poll (`wait_for_row`) / extra Apply Navigator
   before asserting.
6. **Popups** (many OV-GM screens have `pin/pinB` popup refs) now render/populate under the applied scope ->
   handled by the merged popup capability (`pick_popup` / `Pick OV Popup By Label`).

## Capability (both stacks)
- **Playwright:** `apply_ovgm_navigator(page, levels=4, row=1)` (py/ec_object_iud.py) - fills the cascade
  first-available, GO, returns the C1 top-parent value.
- **Robot Framework:** `Apply OV-GM Navigator First Available` (manage_object.resource) - twin; returns the top-parent.

## Live proof (Node CD.0006, Group B, local sandbox)
Cascade filled PU `AS1 EC Exploration Norway` -> Area `AS1_Area` -> Facility `AS1_Facility_01` -> GO -> grid
20 rows. Insert (Code/Name/Start + Calculation Sequence Number + `Op Production Unit` = nav PU) -> Save (no
error) -> GO -> **row LISTED** (groupmodel enabled). Self-cleaned (End=Start, DB-verified 0). R12: backups in
.keyword_backups/; engine compiles + ASCII-clean; Bank sibling dryrun 4/4 (no regression).

## Batch plan (next - per-screen, attended/careful, skip-and-park)
Per screen: recon the parent-dd label + mandatory set (scan_mandatory) -> generate/build with OV-GM config
(nav cascade in Open, parent-dd = nav top, grid manageObject) -> per-screen groupmodel check -> verify_screen
OVERALL PASS -> PR off master. Groups: B(20) C1/C2(10) D(3) F(1) A-OVGM(7) + Stream Item + well-hierarchy(4).
Nav shape per screen in `tmp/ov_gm_55_nav_config.json`. Exclude groupmodel-off screens (verified) like Production Sub Unit.

> RESOLVED 2026-07-31 (was logged here as an OPEN RISK - the wider fear is RETRACTED, with evidence).
> On Message Group (CO.0236) a parent-dd set to 'Administration' PERSISTED as 'Allocation'. A read-only
> probe (tmp/probe_dropdown_fidelity.py - nothing saved) set the field via `select_dropdown` both with
> `__FIRST__` and with the explicit label and READ THE INPUT BACK: it holds 'Administration' in both
> cases. **So the pick is faithful and the shared engine is NOT defective** - the divergence is introduced
> at/after SUBMIT (EC-side derivation/override of FUNCTIONAL_AREA, mechanism not yet established).
> Consequence: the other OV-GM screens' parent-dd handling is NOT implicated by this evidence. Still worth
> doing when convenient: assert the parent-dd value in the DB, not just CODE/NAME, so an EC-side override
> can never pass silently. Message Group stays parked - see tmp/OV_SWEEP_PARKED.md.

## ⚠ ENGINE GOTCHA - `select_dropdown` SILENTLY falls back to the first option (found 2026-08-01, Service CO.2103)

`py/ec_object_iud.py select_dropdown()` substitutes the FIRST available option when the requested label is
not present in the panel, with **no error and no log line**. Verbatim from the source:

```
# value None/''/'__FIRST__' => take the first available option; also used as fallback when a
# requested value isn't in the panel (cascade child: its options only appear once the parent
# dropdown - filled earlier in form order - is selected). So cascade + stale values both resolve.
...
elif opt is not None:
    opt = None  # requested value absent -> retry accepting ANY (first) option
```

The fallback is DELIBERATE and useful for cascade children. The danger is that a wrong value looks exactly
like a right one:

- **Service (CO.2103):** asked for contract `TS3 GTA Shipper A` + transport system `TS3 Transport System`;
  the row saved `TRANS_INV_BLEND` / `TS5_TS` with a green insert. Root cause was date-effectivity - those
  objects start 2011-01-01 and the form's start date was 2003-01-01, so the labels were genuinely absent
  from the panels (49 Contract options, none of them TS3).
- **Message Group (CO.0236):** asked for `Administration` (code ADM), saved `Allocation` (code ALLOCATION).

**Why nobody noticed for so long: no suite asserts dropdown values - only CODE and NAME.** A substituted
reference value therefore passes every existing gate.

**What to do on any screen where a dropdown value MATTERS (scope/parent/reference):**
1. assert the stored value in the DB, not just CODE/NAME - resolving UI LABEL -> DB CODE first
   (`'Production Unit'` is stored as `EEAL`; comparing label to code produces a false failure).
2. check date-effectivity before blaming the engine: reference dropdowns only offer objects effective at the
   form's **Start Date** (`TEST_START_DATE_REFDD` = 2003-01-01 is NOT late enough for 2011+ objects).
3. if a value must be exact, verify it is present in the panel (read-only probe) rather than trusting that
   `select_dropdown` will report a miss - it will not.

## MANDATORY pre-build step (2026-08-01): `scripts/find_populated_scope.py`

The scope trap above (Service's contract/transport system) recurred a SECOND time on Collection Point
(first-available Production Unit's cascade children came back empty) before this was built as a reusable
command instead of a doc paragraph someone has to remember to consult. Message Group's divergence is a
DIFFERENT, still-unresolved defect (see the RESOLVED note above) - it is not caused by picking an
unpopulated scope, so this tool does not explain or prevent it; see the caveat below.

**Run this before the first live attempt on any OV-GM screen with a mandatory nav cascade or a
scope-dependent form dropdown (Contract, Transport System, Production Unit, Operator Route, Functional
Area, ...):**

```
py scripts/find_populated_scope.py <OV_VIEW_NAME>
```

It queries the view's OWN existing rows (ground truth) and reports which scope-code values actually recur,
so a nav/dropdown value can be chosen from a PROVEN scope instead of "first available". Exit 1 if the view
has zero rows - that is a genuine unknown (probe the panels directly or ask), not something to skip past.

Proven on the two known scope-population failure cases, in one command each, immediately:
 - `OV_SERVICE` -> `CONTRACT_CODE` top value `TS3_FIRM2` (10 rows); `TRANSPORT_SYSTEM_CODE` -> `TS3_SYSTEM`
   (all 43 rows) - confirms `TS3_GTA_SHP_A`/`TS3_SYSTEM` were legitimate but minority values.
 - `OV_COLLECTION_POINT` -> `CP_PRODUCTIONUNIT_CODE [('P3_PU', 3), ('FRMW_PU', 1)]` - neither is the
   alphabetically-first PU the cascade would otherwise try.

CAVEAT - `OV_MESSAGE_GROUP` -> `FUNCTIONAL_AREA_CODE [('EC', 2), ('MHM13_PROD', 2)]` shows `Administration`
is not among the view's currently-populated values, but do NOT read this as explaining Message Group's
failure. The RESOLVED note above already proved `select_dropdown` faithfully sets AND reads back
`Administration` in the UI panel - it WAS a valid, selectable option, just not one that appears in existing
rows. The observed divergence (`Administration` -> `Allocation`) happens server-side, at/after Submit, by a
mechanism still not established. This tool would not have flagged or prevented that case.

Deliberately not fully automated: it reports candidates, it does not pick one or resolve CODE -> display
LABEL for you (that varies by cross-reference class - one targeted query per label, same as
`tmp/resolve_service_labels.py`'s pattern). The judgment of which scope to build against stays with
whoever is building the screen; what changes is that the judgment is now made from a proven fact, in one
command, before the first live attempt - not after a failed one.
