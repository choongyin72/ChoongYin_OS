# EC Object Configuration — IUD Pattern (OV screens)

> Read this when you need to Insert/Update/Delete on an **EC object configuration** screen and
> can't remember how. Applies to ~95% of object config screens (Bank, Currency, Language-object,
> Financial/Date objects, …). Only the **Navigator columns** and **Data Window field labels**
> differ per object — the gestures below are **constant**.
> Per-screen selectors live in `screens/<name>.md`. Reusable code in `lib/`.
>
> _Distilled from the Bank task; verified live on EC 14.2.4 sandbox 2026-07-25 (I-U-D 7/7 DB-verified)._

## Step 0 — CHECK FIRST, then build (mandatory gate)
Before writing ANY new code for a screen:
1. **Read** `screens/<name>.md` if it exists — use its selectors, don't re-scan.
2. **Search for an existing implementation** — do not assume a clean slate:
   `grep -ril "<screen-slug>" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
   - Found → **reuse/extend it**; never add a parallel copy (the Bank mistake: a 3rd standalone stack).
3. **Prefer the shared engine over new code:** `py/ec_object_iud.py` (OV IUD) + `libraries/DbVerify.py`
   (DB truth). A new OV screen should be a thin driver (copy `py/bank_iud.py`, swap the config), not new plumbing.
State the search result in the plan-back ("existing impl: <path> / none").

## Screen anatomy that matters
Tree View (open) · Navigator Pane (filter fields + mandatory-yellow + **GO**) · Data Window (grid) ·
Tool Bar (**Save**, Refresh, **New** = hover-menu). Status-area tabs (Record Status / Revision /
Approval / Validation / Trending / Attachments) are read context, not part of IUD.

## Constant gestures (verified)
- **Open** — search `#menu:searchForm:searchTxt` → click `label.tv-link` (or `span.tv-link`) with exact screen name.
- **Insert** — hover `li.ui-menu-parent` containing `span.ui-icon-insert` → click submenu **"New Object"** →
  fill the **mandatory YELLOW** fields (`rgb(252,249,192)` = mandatory-and-empty) → **Save** → **GO**.
- **Update** — select the row → **"New Version"** / `updateAttributes` form → change fields (Code is read-only) → Save → GO.
- **Delete** — **End Date = Start Date** (zero-length window = true delete; row leaves the `ov_*` view).
  The toolbar **Delete is NOT used for EC Objects** (it is disabled by design).
- **Save** — `//a[@title='Save [Ctrl+s]' and not(...ui-state-disabled)]`. **GO** — `#button:form:B` (reloads the grid).

## Field id shape (object forms)
One field per row: label at `…:R:<r>:C:0` (id has a generated suffix → match by **prefix**),
input at `…:R:<r>:C:1:in` (text) / `:da_input` (date) / `:dd_input` (dropdown).
Exception: `objectdates` row R0 holds Start Date (C:1) **and End Date (C:3)** on one row.

## Non-negotiables
- **Local sandbox only.** `AUTOTEST_` prefix on all test data. **Never touch existing rows.**
- **Verify vs the DB** (`ov_<screen>`), never a green UI alone — the UI lies.
- **Self-clean**: after delete, DB re-read = 0 residual `AUTOTEST_` rows.
- **ONE scan** per new screen → write `screens/<name>.md` → reuse, never re-scan.
- **2-strike stop** on any Save/action, then report — no looping selector variations.

## Reuse (code)
> All executable code lives in **`ec-automation`** (Playwright + RF + SOW). `ec-ui-knowledge` is MD-only.
> Reusable Python helpers: **`workstreams/master-plan/ec-automation/py/`** (relative-link from any script).

- `ec-automation/py/ec_object_iud.py` — engine (fields resolved **by label**, not blind row index):
  - write: `login` · `open_object_screen` · `insertObjectRecord(grid, fields)` ·
    `updateObjectRecord(grid, code, fields)` · `closeObjectRecord(grid, code, end_date)`
  - read/locate: `row_exists` · `wait_for_row` · `select_row` · **`read_form_record(grid, code)`** →
    `{label: value}` of the whole form window (test-case inspection).
- `ec-automation/libraries/DbVerify.py` — the single DB ground-truth library (also the RF keyword lib).
  Existing: `code_should_be_present/absent_in_view`, `view_row_count`, N1/N2/N3/MHM oracles.
  Added for OV column verification: `fetch_object` · `field_equals` · **`verify_row(view, code, {COL: expected})`** ·
  `field_should_equal_in_view` (RF keyword) · `code_present` (bool) · `count_like`.
- `ec-automation/py/bank_iud.py` — thin per-screen driver (**template**): copy it, change
  `SCREEN` / `GRID_DATA_ID` / `VIEW` / the field_maps. Engine unchanged.
- **NO HARDCODED field ids** (owner rule): RF T3 resolves fields **by LABEL** via T2 `Fill OV Field By Label` /
  `Fill OV Date By Label` / `OV Field Id By Label` (`${form}` = objectForm|updateAttributes|objectdates). A field's
  label span + input are adjacent tableCells, so the label locates the input with no `R:<n>:C:<n>` id — robust to
  per-screen row shifts (Start Date R2 on Choke vs R4 on Choke Model). Playwright engine already resolves by label.
- RF layer (shared framework): `ec-automation/resources/manage_object.resource` (T2) +
  `ec-automation/libraries/DbVerify.py` + per-screen T3 `pageobjects/.../bank_page.resource` + suite `tests/.../bank_iud.robot`.

## Timing lesson (baked into the engine)
The grid redraws **asynchronously** after open/GO. Always `wait_for_row()` before `select_row()` — an instant
select on a not-yet-rendered grid returns "row not found" even though the data is there. `select_row` now
waits internally. (Every empty read in dev traced to this, never to a wrong selector.) UI reads can also lag;
for column verification prefer the DB (`verify_row`) — authoritative and immune to render timing.
