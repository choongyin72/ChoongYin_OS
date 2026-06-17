# EC OBJECT — IUD Technical Specification TEMPLATE (Playwright + Robot Framework)

> **Purpose.** Fill this template in (via recon) for any new EC master-data/config screen that behaves
> like **Bank** (OV / Manage-Object) or **Language** (TV / Table-class). Once every `[BRACKET]` is
> resolved, you have everything needed to build the **exact same** IUD automation (Playwright bundle +
> RF suite + DB-verified, self-cleaning) and drop the files into the treeview-mirrored folder.
> **Recon-first, DB-ground-truth, self-clean** are mandatory — see [[feedback_finder_first_scope_resolution]],
> [[feedback_probe_write_self_clean]], the `ec-screen-automation` skill, and `docs/ec_screen_registry.md`.

---

## 0. How to use (the procedure this template drives)
1. **INPUT = the screen name.** Run `SCREEN="<name>" py tmp/scripts/resolve_ec_screen.py` (or the §1
   queries) to **auto-derive** class_name, screen type (`OBJECT`→OV / `TABLE`→TV), date-effective +
   delete method (`VERSIONED`→End=Start / else physical), and base/version/view — from EC config tables.
   No hand-entry of metadata.
2. **Live recon = ONE read-only scan.** Run `SCREEN="<name>" py tmp/scripts/scan_ec_screen.py` — it opens
   the screen (never Saves) and prints, keyed by the name: navigator shape + **which nav fields are
   mandatory (yellow)** + GO id, **toolbar New/Delete state** (default = enabled — it only flags the rare
   DISABLED; R10 — disabled Delete ⇒ OV End=Start), the grid id, and the form/field ids with mandatory
   flags + labels (OV: `updateAttributes` + `objectdates` End-Date C:3 + `objectForm`; TV: the grid cells).
   This fills §2 **and** §3 in one pass. Only reference-dd *sources* need an eye if the scan can't infer them.
3. Fill §1–§6 below. Then build §7 deliverables, run §8 acceptance, raise the PR.

---

## 1. Screen identity — INPUT = the screen name ONLY; everything else is DERIVED
**The single manual input is the EC screen name (the on-screen LABEL).** Run
`SCREEN="<screen name>" py tmp/scripts/resolve_ec_screen.py` (or the two SQL queries below) to auto-derive
the rest from EC's config tables — do NOT hand-enter them.

| Field | How it's derived |
|---|---|
| **Screen name** (LABEL) | **← your only input** (e.g. `Contract Area`) |
| class_name | `class_property_cnfg.LABEL` (query 1). If several rows return, pick the real class — skip `_ROWSORT` / `_TEST` / `AUTOSAVE` variants |
| **Screen type** | `class_cnfg.CLASS_TYPE` → **`OBJECT` ⇒ OV (Manage-Object)** · **`TABLE` ⇒ TV (Table-class)** |
| **Date-effective? + DELETE method** | `class_cnfg.TIME_SCOPE_CODE` → **`VERSIONED` ⇒ date-effective ⇒ DELETE = End Date = Start Date**; `EVENT`/`NONE` ⇒ **physical** row delete |
| Base table / version table | `class_cnfg.DB_OBJECT_NAME` / `DB_OBJECT_ATTRIBUTE` |
| DB view (for verify) | `OV_<class_name>` for OV (convention; resolver confirms via `all_views`) · the base table for TV |
| Treeview path (folder placement only) | from the **Maintain Treeview** screen / tv-link tooltip — the only non-DB lookup |

**The two derivation queries** (exactly what `resolve_ec_screen.py` runs):
```sql
-- (1) screen LABEL -> class_name
SELECT t.class_name FROM class_property_cnfg t
 WHERE t.property_code = 'LABEL' AND lower(t.property_value) = '<screen name>';
-- (2) class -> CLASS_TYPE (OV/TV) / TIME_SCOPE_CODE (date-effective) / base + version table
SELECT t.* FROM class_cnfg t WHERE t.class_name IN (
  SELECT class_name FROM class_property_cnfg
   WHERE property_code = 'LABEL' AND lower(property_value) = '<screen name>');
```
_(No "Screen URL fragment" — the screen is opened by name via the search box, never by URL, so it's dropped.)_

## 2. Recon checklist (record the answers)
- [x] **Auto-derived from the screen name** (§1 resolver): class_name · type (OV/TV) · date-effective + delete method · base/version table · verify view. **No hand-entry.**
- [ ] **row count** of the verify view = `[n]` (resolver / DbVerify).
- [ ] **Toolbar New enabled?** `[yes/no]`  · **Toolbar Delete enabled?** `[yes/no]` (disabled ⇒ OV End=Start).
- [ ] Navigator: `[none | date filter | cascade PU→Area→… | Business Unit + GO]`. GO id = `[button:form:B | go_button:form:B | navButton:form:B | n/a]`.
- [ ] **Mandatory (yellow) fields** on the insert form/row: `[list]` (yellow `rgb(252,249,192)`).
- [ ] Reference dropdowns (mandatory dds) + their source: `[e.g. Business Unit → OV_BUSINESS_UNIT]`.
- [ ] Object-start-date / version filter? reference dds only show objects effective at the form date.

## 3. DOM reference (fill from live recon)
**Common**
- Grid/list id: `[manage_object_nav_nav:form:T_data | <grid>:form:T_data | table:form:T_data]`
- Row resolve: row text is in `<span>` (OV/TV text) OR a cell **input value** (some grids) → match accordingly.
- Toolbar: Save `xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]`; Refresh `//a[@title='Refresh [Ctrl+r]']`; Insert/Delete = submenu `li.ui-menu-parent`.

**OV (Manage-Object) form ids** (`tab:tabPanel:<form>:form:G:0:R:{r}:C:1:{in|da_input}`)
- INSERT `objectForm` mandatory: `[R:0=Code, R:1=Name, R:2=Start Date (da_input), …]`
- UPDATE `updateAttributes`: editable `[R:1=Name]` (Code read-only)
- DELETE `objectdates`: Start `…:R:0:C:1:da_input`, **End `…:R:0:C:3:da_input`**

**TV (Table-class) cells** (`<grid>:form:T:{row}:C{n}_in`)
- `[C0_in=Id (mandatory/yellow), C1_in=Code (natural key), C2_in=Name]`

## 4. IUD design (use the block for your type)
**OV / Manage-Object**
```
INSERT: Insert toolbar → hover → "New Object" submenu → objectForm → fill mandatory (Code/Name/Start Date
        + any mandatory ref dd) → Save → GO → verify row in grid + DB view.
UPDATE: click row span (by Code) → updateAttributes → edit Name → Save → GO → verify.
DELETE: Toolbar Delete DISABLED (master data) → set End Date = Start Date in objectdates (zero-length
        window) → Save → GO → object removed from the OV view = TRUE delete (DB-verified).
        (End = Start+1 only soft-expires — row persists. ALWAYS verify at DB.)
```
**OV-GM** = OV + a mandatory **Business Unit / PU cascade + GO** before the grid loads; insert sets the group parent.
**TV / Table-class**
```
INSERT: Insert toolbar → "<Screen label>" → blank grid row → fill mandatory (YELLOW) cells incl. the PK
        (real keystrokes + Tab) → Save → Refresh → verify in grid + base table.
UPDATE: edit the Name cell (real keys + Tab) → Save → Refresh.
DELETE: select row → Delete toolbar → "<Screen label>" → Save → PHYSICAL removal from the base table.
```

## 5. Test data design
| | OV (date-effective) | TV (physical) |
|---|---|---|
| Code | `AUTOTEST_[XXX]_NNN` — **unique per run** (deleted codes linger in base table) | fixed `[ZZ / 999]` — **repeatable** (physical delete self-cleans) |
| Mandatory extras | Start Date `[2000-01-01]` + `[ref dd value]` | the PK + any yellow cell |
| Never | touch existing rows; use `AUTOTEST_` prefix | same |

## 6. DB ground-truth oracle
- Present after INSERT: `code_should_be_present_in_view([view], [code])` (DbVerify) or `view_count_where`.
- After DELETE: OV ⇒ `code_should_be_absent_in_view([view], [code])` (End=Start → 0 rows); TV ⇒ physically absent in base table.
- Self-clean check: re-read the view/table; confirm 0 residual `AUTOTEST_` / test rows.

## 7. Deliverables + folder layout (treeview-mirrored)
**Playwright bundle** under `screens/<menu path>/<Screen>/` (e.g. `screens/Configuration/System/Language/`):
- `<screen>_sow.md` (this filled spec) · `README.md` · `playwright/ec_iud_<slug>.py` · `investigation/` (recon scripts) · `evidence/` (screenshots per IUD step).
**Robot Framework:**
- T3 `pageobjects/<menu path>/<screen>_page.resource` (locators in Variables + thin wrappers; docstring matches Variables — R7).
- Suite `tests/<menu path>/<screen>_iud.robot` (TC: clean → insert → update → delete → cleanup; in-suite DB asserts).
- Reuse T2: **`manage_object.resource`** (OV) or **`table_class.resource`** (TV) + T1 `common.resource` + `DbVerify.py`. Shared-file edit ⇒ R12 (backup + canary + random sibling).
**Registry + scorecard:** append a row to `docs/ec_screen_registry.md` + `docs/automation-scorecard.md`.

## 8. Acceptance criteria
| Op | Pass condition |
|---|---|
| INSERT | new `AUTOTEST_` record in grid **and** DB view/table |
| UPDATE | Name changed + persisted (grid + DB) |
| DELETE | removed from OV view (End=Start) / physically gone (TV) — **DB-verified** |
| CLEANUP | environment exactly as found (0 residual) — DB-verified |
| RF | robocop clean · dryrun green · **live headed N/N PASS** · self-cleaning |

---

## 9. WORKED EXAMPLE — Contract Area (recon 2026-06-17; remaining live-DOM fields marked ⏳)
| Field | Value |
|---|---|
| Screen name | **Contract Area** |
| Treeview path | `Configuration > Assets > Commercial Objects > Contract Area` ⏳(confirm exact path via tv-link) |
| Screen type | **OV (Manage-Object)** — date-effective ✅ |
| DB view | `OV_CONTRACT_AREA` (29 rows) |
| Base table(s) | `CONTRACT_AREA` / `CONTRACT_AREA_VERSION` |
| Date-effective | **yes** ⇒ DELETE = **End Date = Start Date** |
| Mandatory fields | Code, Name, Object Start Date, **Business Unit** (`BUSINESS_UNIT_CODE/ID` → `OV_BUSINESS_UNIT`) ⏳(confirm yellow set live) |
| Navigator | manage-object (date filter + GO) ⏳(confirm; may be BU-gated like other Commercial/Dispatching OV) |
| Grid id | ⏳ `manage_object_nav_nav:form:T_data` (expected) |
| Form ids | ⏳ `tab:tabPanel:objectForm:form:G:0:R:{0=Code,1=Name,2=StartDate,…}` ; updateAttributes Name; objectdates End `…R:0:C:3:da_input` |
| Test data | `AUTOTEST_CA_001` (unique per run) / `AUTOTEST Contract Area 001` / Start `2000-01-01` / BU = `[an existing BU, e.g. SS1_BU]` |
| Verify | `code_should_be_present_in_view('OV_CONTRACT_AREA','AUTOTEST_CA_001')` then absent after End=Start |
| Bundle path | `screens/Configuration/Assets/Commercial_Objects/Contract_Area/` |
| RF | `pageobjects/Configuration/Assets/Commercial_Objects/contract_area_page.resource` + `tests/.../contract_area_iud.robot`, reuse `manage_object.resource` |

**Sample existing rows (for nav/BU values):** `SS1_CA` (SS1 CA, BU `SS1_BU`, start 2002-09-01), `SS2_CA` (BU `SS2_BU`). Contract Area = Bank pattern + a mandatory **Business Unit** reference dd (like the Sales Order / Dispatching OV screens).

---

## 10. Scaling to project config-testing + NIGHTLY CI config-integrity guard (the end goal)
The end goal is to run these similar tasks **automatically at scale** — for project automation/system-config
testing, and in a **nightly CI build** that catches **system config accidentally missing or deleted**.
Two distinct modes (do NOT conflate them):

**A. Authoring mode (write) — the `ec-object-iud-builder` skill.** Build per-screen IUD coverage (full
insert/update/delete, DB-verified, self-cleaning). Run on demand / when adding a screen. Destructive-but-
self-cleaning → only against the local/non-prod sandbox, never an env you can't safely write to.

**B. Nightly CI config-integrity mode (READ-ONLY) — the safe regression guard.** Do **NOT** run destructive
IUD every night on a shared env. Instead assert that **expected config still exists**:
- **Baseline:** a checked-in `config_baseline.json` per env = the expected objects/codes (+ min row counts)
  per registered screen/view (e.g. `OV_BANK` must contain the 6 standard banks; `T_BASIS_LANGUAGE` ≥ 8).
- **Nightly check** (`config_integrity_check.py`): loop the registry's screens → for each, **read-only**
  DbVerify assertions — `code_should_be_present_in_view(view, code)` for each baseline code +
  `view_row_count(view) >= baseline_min`. **Zero writes.** Any missing/deleted config ⇒ **fail the build +
  alert** (which config object vanished, in which view).
- **Optional gated write-smoke:** a tiny IUD canary (insert→verify→delete-revert→verify-clean) on a couple
  of screens, **only** in a disposable/non-prod env, behind a `--variable WRITE_OK:yes` flag.

**Delivery:** drive it from the existing CI hook (the daily-review scheduled task / a GitHub Actions
nightly). The per-screen specs (this template) + the registry are the source of truth for *what* to check;
the baseline is *what good looks like*; the nightly read-only check is the *guard*. This turns the one-off
IUD builds into a standing **"config didn't silently disappear"** safety net. (Aligns with
[[project_ec_config_integrity_goal]] and [[feedback_independent_proof_mindset]].)

---
_This template is the input to the `ec-object-iud-builder` skill (authoring mode, §0→§8) and the basis for
the nightly read-only config-integrity guard (§10)._
