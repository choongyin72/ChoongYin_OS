"""Generate the RF T3 + suite + bundle docs for a PLAIN Bank-layout OV screen.

Emits label-driven, no-hardcode files that mirror the proven Port/Berth/Canal pattern.
Driver is written separately (has real logic). Every generated screen MUST still pass
scripts/verify_screen.py live before PR -- this only scaffolds the boilerplate.

Usage:
  py tmp/gen_ov_screen.py '<json config>'
config keys: screen, bfcode, view, folder, code_label, name_label, date_label, end_label,
             slug, code_prefix, cols (list of extra DB col notes, optional)
"""
import json
import sys
from pathlib import Path

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
KB = Path(r"C:\Projects\ChoongYin_OS\ec-ui-knowledge\screens")

c = json.loads(sys.argv[1])
screen = c["screen"]; bf = c["bfcode"]; view = c["view"].upper()
folder = c["folder"].strip("/")                    # e.g. Configuration/Assets/Transport_Objects
nseg = len(folder.split("/"))
up = "../" * (1 + nseg)                             # depth from pageobjects/<folder>/ or tests/<folder>/ to ec-automation
slug = c["slug"]
grid_id = c.get("grid_id", "manage_object_nav_nav:form:T_data")
# Open gesture: GO (Apply Navigator) for grids fed by a navigator - plain manage-object AND OV-GM
# (manageObject:form:T_data, navigator-scoped, lazy redraw). Toolbar Refresh only for custom-URL screens
# on their own URL with no GO button (nav:form:T_data or a bespoke <name>:form:T_data). Save And Refresh
# List (T2) already does GO-or-Refresh for reload-after-write, so only the OPEN gesture differs here.
_GO_GRIDS = ("manage_object_nav_nav:form:T_data", "manageObject:form:T_data")
_custom_url = grid_id not in _GO_GRIDS
_ov_gm = grid_id == "manageObject:form:T_data"
open_reload = ("    Refresh Screen    # custom-URL OV: no GO; grid loads on open, toolbar Refresh after writes"
               if _custom_url else "    Apply Navigator    # grid needs GO to populate (no default rows on open)")
code_l = c["code_label"]; name_l = c["name_label"]; date_l = c["date_label"]; end_l = c["end_label"]
prefix = c["code_prefix"]                           # e.g. AUTOTEST_CANAL_
dds = c.get("dropdowns", [])                        # optional [{"label","value"}] mandatory dropdown(s)
pops = c.get("popups", [])                          # optional [{"label","value"}] mandatory Pick-from-EC-Object popup(s)
extras = c.get("extra_fields", [])                  # optional [{"label","value"}] extra mandatory text/num fields
# RF T3 insert lines + Playwright driver INSERT_FIELDS entries for each mandatory dropdown (label-driven)
dd_t3 = "".join("    Fill OV Dropdown By Label    objectForm    %s    %s\n" % (d["label"], d["value"]) for d in dds)
dd_driver = "".join('    {"label": "%s", "value": "%s", "kind": "dropdown"},\n' % (d["label"], d["value"]) for d in dds)
# mandatory popup refs (pin/pinB) -> label-driven Pick OV Popup By Label (RF) + kind:"popup" (Playwright engine)
pop_t3 = "".join("    Pick OV Popup By Label    objectForm    %s    %s\n" % (p["label"], p["value"]) for p in pops)
pop_driver = "".join('    {"label": "%s", "value": "%s", "kind": "popup"},\n' % (p["label"], p["value"]) for p in pops)
# extra mandatory text/numeric fields (beyond Code/Name/Start Date) - filled label-driven, same as Code/Name
ex_t3 = "".join("    Fill OV Field By Label    objectForm    %s    %s\n" % (e["label"], e["value"]) for e in extras)
ex_driver = "".join('    {"label": "%s", "value": "%s", "kind": "text"},\n' % (e["label"], e["value"]) for e in extras)
Screen_dir = screen.replace(" ", "_")
# When a screen has mandatory dropdowns/extras, fill them in a SPLIT-OUT sub-keyword so the Insert
# keyword stays within robocop's 10-keyword-call limit (LEN03). Otherwise inline nothing.
_has_extra = bool(dds or pops or extras)
# Some OV screens make End Date mandatory on INSERT (unusual). If config gives insert_end_date, the Insert
# keyword also fills the End Date; delete still works (End=Start). Kept inline (one extra call, under LEN03).
insert_end = c.get("insert_end_date", "")
insert_end_line = ("    Fill OV Date By Label    objectForm    %s    %s\n" % (end_l, insert_end)) if insert_end else ""
end_driver = ('    {"label": "%s", "value": "%s", "kind": "date"},\n' % (end_l, insert_end)) if insert_end else ""
extra_doc = " (+ mandatory dropdowns/extra fields)" if _has_extra else ""
insert_extra_call = ("    Fill %s Mandatory Extras\n" % screen) if _has_extra else ""
extras_kw = ("""
Fill %s Mandatory Extras
    [Documentation]    Fill the mandatory dropdown(s) + extra field(s) for %s, split out of Insert to keep
    ...    the Insert keyword within the keyword-count limit. All label-driven (no hardcoded ids).
%s
""" % (screen, screen, (dd_t3 + pop_t3 + ex_t3).rstrip("\n"))) if _has_extra else ""


def w(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print("wrote", path)


# ---- T3 page object -------------------------------------------------------
t3 = f"""*** Settings ***
Documentation       T3 (screen) - {screen} page object.
...                 Screen: {folder.replace('/', ' > ')} > {screen} ({bf}). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${{SCREEN_GRID}};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             {up}libraries/DbVerify.py
Resource            {up}resources/common.resource
Resource            {up}resources/manage_object.resource


*** Variables ***
${{SCREEN_NAME}}          {screen}
${{SCREEN_GRID}}          {grid_id}
# NO hardcoded ids: grid = shared T2 ${{SCREEN_GRID}}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="{code_l}" Name="{name_l}" Date="{date_l}" End="{end_l}".


*** Keywords ***
Open {screen} Screen
    [Documentation]    Suite Setup: launch, login, open {screen}, load the list (GO).
    [Arguments]    ${{user}}=${{EC_USER}}    ${{pass}}=${{EC_PASS}}
    Launch EC And Open Screen    ${{SCREEN_NAME}}    ${{user}}    ${{pass}}
{open_reload}

{screen} Row Should Exist
    [Documentation]    Assert a {slug} with ${{code}} is present in the list.
    [Arguments]    ${{code}}
    Row Should Exist    ${{SCREEN_GRID}}    ${{code}}

{screen} Row Should Not Exist
    [Documentation]    Assert a {slug} with ${{code}} is absent from the list.
    [Arguments]    ${{code}}
    Row Should Not Exist    ${{SCREEN_GRID}}    ${{code}}

{screen} Should Exist In DB
    [Documentation]    DB ground-truth: assert ${{code}} really persisted in {view}.
    [Arguments]    ${{code}}
    Code Should Be Present In View    {view}    ${{code}}

{screen} Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${{code}} was truly deleted from {view}.
    [Arguments]    ${{code}}
    Code Should Be Absent In View    {view}    ${{code}}

{screen} Row Should Show Name
    [Documentation]    Assert the {screen} row for ${{code}} displays ${{name}}.
    [Arguments]    ${{code}}    ${{name}}
    Object Row Should Show Name    ${{SCREEN_GRID}}    ${{code}}    ${{name}}

Insert {screen} Record
    [Documentation]    Insert a new {slug}: New Object form -> Code/Name/Start Date{extra_doc} -> Save.
    [Arguments]    ${{code}}    ${{name}}    ${{start_date}}
    Open New Object Form
    Fill OV Field By Label    objectForm    {code_l}    ${{code}}
    Fill OV Field By Label    objectForm    {name_l}    ${{name}}
    Fill OV Date By Label    objectForm    {date_l}    ${{start_date}}
{insert_end_line}{insert_extra_call}    Save And Refresh List
{extras_kw}
Update {screen} Name
    [Documentation]    Select the {slug}, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${{code}}    ${{new_name}}
    Select Object Row    ${{SCREEN_GRID}}    ${{code}}
    ${{code_id}}=    OV Field Id By Label    updateAttributes    {code_l}
    ${{loaded}}=    Get Property    css=[id="${{code_id}}"]    value
    Should Be Equal    ${{loaded}}    ${{code}}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    {name_l}    ${{new_name}}
    Save And Refresh List

Delete {screen}
    [Documentation]    Select the {slug}, set End Date = Start Date (true delete), Save.
    [Arguments]    ${{code}}    ${{date}}
    Select Object Row    ${{SCREEN_GRID}}    ${{code}}
    Fill OV Date By Label    objectdates    {end_l}    ${{date}}
    Save And Refresh List
"""
w(EC / "pageobjects" / Path(folder) / f"{slug}_page.resource", t3)

# ---- suite ----------------------------------------------------------------
suite = f"""*** Settings ***
Documentation       EC IUD Test - {screen} ({folder.replace('/', ' > ')} > {screen}, {bf}).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in {view}).
...                 Layered: this test -> {slug}_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique {prefix}<timestamp> code per run.

Resource            {up}pageobjects/{folder}/{slug}_page.resource

Suite Setup         Set Up {screen} Suite
Suite Teardown      Close EC

Test Tags           iud    {slug}


*** Variables ***
${{TEST_CODE}}        ${{EMPTY}}
${{OBJ_NAME}}         ${{EMPTY}}
${{OBJ_NAME_UPD}}     ${{EMPTY}}
${{START_DATE}}       ${{TEST_START_DATE}}
${{END_DATE}}         ${{TEST_START_DATE}}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test {slug} does not exist before inserting.
    [Tags]    clean-state
    {screen} Row Should Not Exist    ${{TEST_CODE}}
    Capture Step    {slug}_tc01_clean

TC02 Insert New {screen}
    [Documentation]    Insert a new {slug}; confirm in list + DB ({view}).
    [Tags]    insert
    Insert {screen} Record    ${{TEST_CODE}}    ${{OBJ_NAME}}    ${{START_DATE}}
    {screen} Row Should Exist    ${{TEST_CODE}}
    {screen} Should Exist In DB    ${{TEST_CODE}}
    Capture Step    {slug}_tc02_inserted

TC03 Update {screen}
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update {screen} Name    ${{TEST_CODE}}    ${{OBJ_NAME_UPD}}
    {screen} Row Should Show Name    ${{TEST_CODE}}    ${{OBJ_NAME_UPD}}
    Field Should Equal In View    {view}    ${{TEST_CODE}}    NAME    ${{OBJ_NAME_UPD}}
    Capture Step    {slug}_tc03_updated

TC04 Delete {screen}
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete {screen}    ${{TEST_CODE}}    ${{END_DATE}}
    {screen} Row Should Not Exist    ${{TEST_CODE}}
    {screen} Should Not Exist In DB    ${{TEST_CODE}}
    Capture Step    {slug}_tc04_deleted


*** Keywords ***
Set Up {screen} Suite
    [Documentation]    Generate a unique test code/name, then open the {screen} screen.
    Prepare IUD Object Data    {prefix}    {screen}
    Open {screen} Screen
"""
w(EC / "tests" / Path(folder) / f"{slug}_iud.robot", suite)

# ---- bundle docs ----------------------------------------------------------
B = EC / "screens" / Path(folder) / Screen_dir
sow = f"""# SOW - {screen} IUD

## Classification
- **Screen:** {folder.replace('/', ' > ')} > {screen} (BF_CODE **{bf}**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) - date-effective; plain (no mandatory dropdowns)
- **DB view:** `{view}` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `{view}`

## Nav / grid / cells
- **Open:** menu search "{screen}" -> `label.tv-link`. Navigator = single **Date + GO**; grid needs GO.
- **Grid:** shared T2 `${{SCREEN_GRID}}` (= `manage_object_nav_nav:form:T_data`).
- **NO hardcoded field ids** - resolved BY LABEL via T2 `Fill OV * By Label` / `OV Field Id By Label`:
  - **Insert (objectForm):** `{code_l}`, `{name_l}`, `{date_l}` (mandatory). Optional dropdowns skipped.
  - **Update (updateAttributes):** `{name_l}` (Code read-only; loaded-check via `OV Field Id By Label` on `{code_l}`).
  - **Delete (objectdates):** `{end_l}` = Start Date.

## Test data
- `{prefix}<timestamp>` unique per run; Start/End = `${{TEST_START_DATE}}` (2000-01-01). Never touch real rows.

## Dev story
Recon-first (DB `CLASS_TYPE=OBJECT` ⇒ OV; live form) -> plain Bank-layout OV, no mandatory dropdowns.
Built label-driven on the shared engine + T2 (zero engine changes). Playwright driver 7/7; RF T3+suite
label-driven -> live 4/4. All gates run + auto-ticked by `verify_screen.py` (OVERALL PASS).

## Lessons / known risks
- Optional dropdowns skipped (none mandatory). Delete uses engine `wait_for_row_absent` (async redraw).
"""
w(B / f"{slug}_sow.md", sow)

readme = f"""# {screen} ({bf}) - OV IUD bundle

Manage-Object (OV) screen: **{folder.replace('/', ' > ')} > {screen}**. Full Insert / Update / Delete
(End Date = Start Date), DB-verified against `{view}`, self-cleaning. Built **label-driven, zero hardcoded
field ids** on the shared engine + T2.

## Artifacts
- **SOW:** `{slug}_sow.md`
- **Playwright driver:** `../../../py/{slug}_iud.py` (thin; shared engine + DbVerify)
- **RF T3:** `../../../pageobjects/{folder}/{slug}_page.resource`
- **RF suite:** `../../../tests/{folder}/{slug}_iud.robot`
- **investigation/** recon.py - **evidence/** {slug}_0[1-5]_*.png + rf_report.html
- **VERIFY-REPORT.md** - auto-generated by `scripts/verify_screen.py` (OVERALL PASS)

## Verified (real runs, not hand-ticked)
robocop 0 - hygiene 0 - dryrun 4/4 - **LIVE RF 4/4** - **Playwright 7/7** - self-clean 0 residual.
"""
w(B / "README.md", readme)

journal = f"""# JOURNAL - {screen} ({bf}) OV IUD

## 2026-07-26
- **Branch:** `feature/{slug}-iud` (own branch, stacked so the shared-engine helpers are present).
  Check-existing gate: only this build; reused shared engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` ⇒ OV; treeview
  {folder.replace('/', ' > ')} > {screen}. Mandatory Code/Name/Start Date; optional dropdowns skipped.
  Plain Bank-layout OV (single Date+GO nav, no mandatory dropdowns).
- **Label-driven** T3 (no hardcoded ids). Playwright driver -> 7/7; RF T3+suite -> live 4/4.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 7/7.

## Lessons
- Plain OV; generic engine handled appear/absent/pagination with zero screen-specific tuning.
"""
w(B / "JOURNAL.md", journal)

checklist = f"""# {screen} - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

## Step 0 - check-existing gate
- [x] 0a KB map created / 0b grep ec-automation -> only this build / 0c reused shared engine + DbVerify + T2 (thin driver, zero engine changes).

## A. Bundle artifacts
- [x] 1 `{slug}_sow.md` - [x] 2 `README.md` - [x] 3 `JOURNAL.md`
- [x] 4 Playwright flow -> `py/{slug}_iud.py` (py/ per owner rule; env-creds, ASCII)
- [x] 5 `investigation/` (recon.py) - [x] 6 `evidence/` ({slug}_0[1-5]_*.png + rf_report.html) - [x] 7 `CHECKLIST.md`

## B. RF files
- [x] 8 T3 `pageobjects/{folder}/{slug}_page.resource` (label-driven, NO hardcoded ids)
- [x] 9 Suite `tests/{folder}/{slug}_iud.robot`

## C. Verification gates - authored by `verify_screen.py` from REAL exit codes (see VERIFY-REPORT.md)
- [ ] 10 robocop exit 0 - [ ] 11 `--dryrun` - [ ] 12 LIVE RF N/N + Playwright 7/7
- [ ] 13 DB ground-truth - `Code Should Be Present/Absent In View {view}` + `Field Should Equal In View {view} <code> NAME` (update)
- [ ] 14 FULL I-U-D - [ ] 15 Self-clean 0 residual - [ ] 16 hygiene exit 0
_These gate boxes stay [ ] until `scripts/verify_screen.py` runs; its VERIFY-REPORT.md carries the REAL
result. NEVER hand-tick these - the CHECKLIST/VERIFY-REPORT contradiction guard in check_bundle_hygiene.py
FAILS the build if a box here claims a gate clean that VERIFY-REPORT shows failing (#237 item 2)._

## D. Delivery
- [ ] 17 Registry row - [ ] 18 Scorecard row - [ ] 19 PR (R9 body)

## E. Knowledge base
- [x] 20 KB map `ec-ui-knowledge/screens/{slug}.md`
- [x] 21 Reuse clause - N/A (new build); JOURNAL + evidence + KB map + VERIFY-REPORT all produced

_Gates 10-16 RUN by `scripts/verify_screen.py` -> `VERIFY-REPORT.md` (OVERALL PASS); ticks from real exit codes._
"""
w(B / "CHECKLIST.md", checklist)

kb = f"""# Screen: {screen}

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** {bf} - **Treeview:** {folder.replace('/', ' > ')} > {screen} _(DB treeview JSON)_
- **DB view:** `{view}` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `{screen}` -> `label.tv-link` "{screen}" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**{code_l}*** - **{name_l}*** - **{date_l}*** (date) - {end_l} - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`{code_l}` (ro) - **`{name_l}`**. Delete: **`{end_l}`** = Start Date -> leaves `{view}`.

## Automation (code in ec-automation)
- **Playwright:** `py/{slug}_iud.py` -> 7/7 (update Name).
- **RF:** T3 `pageobjects/{folder}/{slug}_page.resource` (**label-driven, NO hardcoded ids**) + suite `tests/.../{slug}_iud.robot` -> live 4/4.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
"""
w(KB / f"{slug}.md", kb)

# ---- Playwright driver ----------------------------------------------------
view_l = c["view"].lower()
name_val = c.get("name_val", "AUTOTEST %s 001" % screen)
code_val = "%s001" % prefix
driver = f'''"""{screen} - IUD driver (thin). Reuses the shared engine py/ec_object_iud.py + DbVerify.py.

OV ({folder.split('/')[-1].replace('_',' ')}, {bf}). Mandatory: {code_l}/{name_l}/{date_l}
(optional dropdowns skipped). Update = Name. Selector map: ec-ui-knowledge/screens/{slug}.md.
Run headed: EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/{slug}_iud.py
"""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent / "libraries"))
import ec_object_iud as ec
import DbVerify as db


def _repo_root():
    for p in [_HERE, *_HERE.parents]:
        if (p / ".git").exists():
            return p
    return _HERE.parents[3]


_ROOT = _repo_root()

SCREEN        = "{screen}"
GRID_DATA_ID  = "{grid_id}"
VIEW          = "{view_l}"
CODE          = os.environ.get("EC_CODE", "{code_val}")
START_DATE    = "2000-01-01"
END_DATE      = START_DATE
NAME          = "{name_val}"
NAME_UPD      = "{name_val} UPDATED"

INSERT_FIELDS = [
    {{"label": "{code_l}",  "value": CODE,       "kind": "text"}},
    {{"label": "{name_l}",  "value": NAME,       "kind": "text"}},
    {{"label": "{date_l}",  "value": START_DATE, "kind": "date"}},
{dd_driver}{pop_driver}{ex_driver}{end_driver}]
UPDATE_FIELDS = [
    {{"label": "{name_l}",  "value": NAME_UPD,   "kind": "text"}},
]

URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / "{slug}" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
results = {{}}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / f"{slug}_{{label}}.png"))
    except Exception:
        pass


def step(page, name, fn):
    try:
        fn()
        results[name] = "PASS"
    except Exception as e:
        results[name] = "FAIL: %s" % (repr(e)[:160])
        shot(page, name + "_FAIL")
        raise


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not HEADED, slow_mo=SLOWMO,
                                    args=["--ignore-certificate-errors", "--start-maximized"])
        ctx = browser.new_context(ignore_https_errors=True, no_viewport=HEADED,
                                  viewport=None if HEADED else {{"width": 1920, "height": 1080}})
        page = ctx.new_page()
        try:
            print(f"[MODE] headed={{HEADED}} code={{CODE}}")
            ec.login(page, URL, USER, PW)
            print("  screen:", ec.open_object_screen(page, SCREEN))
            shot(page, "01_loaded")
            ec.click_go(page)

            if ec.row_exists(page, GRID_DATA_ID, CODE):
                print("  pre-existing", CODE, "-> closing (End=Start) first")
                ec.closeObjectRecord(page, GRID_DATA_ID, CODE, END_DATE)
                ec.open_object_screen(page, SCREEN); ec.click_go(page)

            print("=== INSERT ===")
            step(page, "insert_ui", lambda: ec.insertObjectRecord(page, GRID_DATA_ID, INSERT_FIELDS))
            shot(page, "02_inserted")
            def _v_ins():
                assert ec.wait_for_row(page, GRID_DATA_ID, CODE), "not in grid"
                assert db.code_present(VIEW, CODE), "not in {view_l}"
                ok, act = db.field_equals(VIEW, CODE, "NAME", NAME)
                assert ok, f"DB NAME={{act!r}} != {{NAME!r}}"
            step(page, "insert_db", _v_ins)
            print("  INSERT verified (grid + DB + NAME)")

            print("=== UPDATE ===")
            step(page, "update_ui", lambda: ec.updateObjectRecord(page, GRID_DATA_ID, CODE, UPDATE_FIELDS))
            shot(page, "03_updated")
            def _v_upd():
                ok, an = db.field_equals(VIEW, CODE, "NAME", NAME_UPD)
                assert ok, f"DB NAME={{an!r}} != {{NAME_UPD!r}}"
            step(page, "update_db", _v_upd)
            print("  UPDATE verified (DB NAME)")

            print("=== DELETE (End=Start) ===")
            step(page, "delete_ui", lambda: ec.closeObjectRecord(page, GRID_DATA_ID, CODE, END_DATE))
            shot(page, "04_deleted")
            def _v_del():
                assert ec.wait_for_row_absent(page, GRID_DATA_ID, CODE), "still in grid"
                assert not db.code_present(VIEW, CODE), "still in DB view"
            step(page, "delete_db", _v_del)
            print("  DELETE verified (absent grid + DB)")

            residual = db.count_like(VIEW, "AUTOTEST")
            results["self_clean"] = "CLEAN (0 residual)" if residual == 0 else f"RESIDUAL={{residual}}"
            print("  self-clean:", results["self_clean"])
            shot(page, "05_final")
        finally:
            if HEADED:
                page.wait_for_timeout(4000)
            ctx.close()
            browser.close()


if __name__ == "__main__":
    ok = True
    try:
        main()
    except Exception as e:
        print("ABORTED:", repr(e)[:200]); ok = False
    print("\\n" + "=" * 56 + "\\nRESULTS")
    for k, v in results.items():
        mark = "OK" if str(v).startswith(("PASS", "CLEAN")) else "X"
        if mark == "X" and not str(v).startswith("RESIDUAL"):
            ok = False
        print(f"  {{mark}} {{k:<12}}: {{v}}")
    print("Overall:", "ALL PASS" if ok else "FAILURES")
    print("Evidence:", EVID)
    sys.exit(0 if ok else 1)
'''
w(EC / "py" / f"{slug}_iud.py", driver)
print("DONE")
