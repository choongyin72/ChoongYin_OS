"""OV-GM bundle generator - emits the PROVEN Node/Chemical-Tank template (driver + T3 + suite + SOW +
README) for one OV-GM screen from a JSON config. Cuts per-screen work + keeps every bundle identical to
the verified exemplars. NEVER runs anything live - just writes files. verify_screen is still the gate.

Usage: py tmp/gen_ovgm.py '<json>'
  json keys: screen, bf, view (OV_*), base, folder (e.g. Configuration/Assets/Chemical_Objects),
             slug (chem_stream), abbr (cs, for evidence prefix), code_prefix (AUTOTEST_CS_),
             code_label, name_label, screen_folder (Chemical_Stream),
             extra_dropdowns (list of mandatory dropdown labels, each first-available),
             has_op_pu (bool: set Op Production Unit first-available for grid visibility)
             parent_dd (label of the form dd that must EQUAL the navigator's captured top-parent)
All fields resolved BY LABEL in RF/driver (no hardcoded rows). Op PU + extra dds = __FIRST__ (probe-safe).
"""
import json
import sys
from pathlib import Path

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
a = json.loads(sys.argv[1])
screen = a["screen"]; view = a["view"].upper(); base = a.get("base", "")
folder = a["folder"].strip("/"); slug = a["slug"]; abbr = a["abbr"]
# relative depth must be computed, not hardcoded: `%(up)s` is only right for a 3-segment folder
# (Message Group at Configuration/Messaging has 2 and every import silently failed to resolve)
_up = "../" * (len(folder.split("/")) + 1)
cpfx = a["code_prefix"]; code_l = a["code_label"]; name_l = a["name_label"]
sfolder = a["screen_folder"]; bf = a.get("bf", "")
extra_dd = a.get("extra_dropdowns", []); has_op_pu = a.get("has_op_pu", True)
# parent_dd: the objectForm dropdown that MUST equal the navigator's captured top-parent, or the new row
# lands outside the scope the grid is showing (Message Group: nav first = 'Administration' but the form's
# first = 'ALLOCATION' -> insert persisted, grid never listed it). Do NOT also list it in
# extra_dropdowns, or it gets set twice (second write wins, __FIRST__ would clobber the scope).
parent_dd = a.get("parent_dd", "")
# parent_dd VALIDATED 2026-08-01 end-to-end on Area (tmp/validate_parent_dd_area.py, 7/7 PASS, exit 0):
# navigator set to a PU -> value captured -> bound into the form's Op Production Unit -> Save -> the row
# LISTS in the grid -> OV_AREA.OP_PRODUCTIONUNIT_CODE == the code for that PU name -> End=Start removes it
# -> 0 residual. Node was the wrong test bed (its Op PU panel does not offer the navigator's PU at all).
# Two flaws in the TEST had to be fixed first, neither in this code: start date 2000-01-01 (Op PU only
# offers PUs effective at the form's start date; 'Production Unit' starts 2002-01-01) and comparing a UI
# LABEL against the DB's CODE ('Production Unit' vs 'EEAL').
assert parent_dd not in extra_dd, ("parent_dd %r must not also appear in extra_dropdowns - it would be "
                                   "overwritten with __FIRST__" % parent_dd)
popups = a.get("popups", [])   # mandatory Pick-from-EC-Object popup labels (first-available, nav-scoped)
view_lc = view.lower()
name_val = "AUTOTEST %s 001" % screen

# ---- driver insert_fields (python) ----
ins = [
    '                {"label": %r, "value": CODE,       "kind": "text"},' % code_l,
    '                {"label": %r, "value": NAME,       "kind": "text"},' % name_l,
    '                {"label": "Start Date", "value": START_DATE, "kind": "date"},',
]
for d in extra_dd:
    ins.append('                {"label": %r, "value": "__FIRST__", "kind": "dropdown"},' % d)
for pp in popups:
    ins.append('                {"label": %r, "value": "__FIRST__", "kind": "popup"},' % pp)
if has_op_pu:
    ins.append('                {"label": "Op Production Unit", "value": "__FIRST__", "kind": "dropdown"},')
if parent_dd:
    # value is the runtime variable `pu`, deliberately unquoted - insert_fields is built AFTER
    # apply_ovgm_navigator() returns, so the captured top-parent is in scope here.
    ins.append('                {"label": %r, "value": pu, "kind": "dropdown"},' % parent_dd)
ins_block = "\n".join(ins)

driver = '''"""%(screen)s - IUD driver (thin). Reuses shared engine ec_object_iud.py + DbVerify.py.

OV-GM (grid manageObject:form:T_data) = navigator-GATED (cascade + GO before the grid loads). Built on the
gated-navigator capability (apply_ovgm_navigator). Fields by label. Extra dropdowns + Op Production Unit set
first-available (probe per screen - the nav PU is not necessarily a valid Op PU option).
Run headed: EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/%(slug)s_iud.py
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

SCREEN        = %(screen)r
GRID_DATA_ID  = "manageObject:form:T_data"
VIEW          = %(view_lc)r
CODE          = os.environ.get("EC_CODE", "%(cpfx)s001")
START_DATE    = "2000-01-01"
END_DATE      = START_DATE
NAME          = %(name_val)r
NAME_UPD      = %(name_val)r + " UPDATED"

URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / %(slug)r / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / ("%(abbr)s_" + label + ".png")))
    except Exception:
        pass


def step(page, name, fn):
    try:
        fn()
        results[name] = "PASS"
    except Exception as e:
        results[name] = "FAIL: %%s" %% (repr(e)[:160])
        shot(page, name + "_FAIL")
        raise


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not HEADED, slow_mo=SLOWMO,
                                    args=["--ignore-certificate-errors", "--start-maximized"])
        ctx = browser.new_context(ignore_https_errors=True, no_viewport=HEADED,
                                  viewport=None if HEADED else {"width": 1920, "height": 1080})
        page = ctx.new_page()
        try:
            print("[MODE] headed=%%s code=%%s" %% (HEADED, CODE))
            ec.login(page, URL, USER, PW)
            print("  screen:", ec.open_object_screen(page, SCREEN))
            shot(page, "01_loaded")
            pu = ec.apply_ovgm_navigator(page)
            results["nav_pu"] = "PASS: PU=%%r" %% pu
            print("  navigator applied; top-parent PU =", repr(pu))
            assert pu, "navigator cascade returned no top-parent PU"

            insert_fields = [
%(ins_block)s
            ]
            update_fields = [{"label": %(name_l)r, "value": NAME_UPD, "kind": "text"}]

            if ec.row_exists(page, GRID_DATA_ID, CODE):
                print("  pre-existing", CODE, "-> closing (End=Start) first")
                ec.closeObjectRecord(page, GRID_DATA_ID, CODE, END_DATE)

            print("=== INSERT ===")
            step(page, "insert_ui", lambda: ec.insertObjectRecord(page, GRID_DATA_ID, insert_fields))
            shot(page, "02_inserted")
            def _v_ins():
                assert ec.wait_for_row(page, GRID_DATA_ID, CODE), "not in grid"
                assert db.code_present(VIEW, CODE), "not in ov view"
                ok, act = db.field_equals(VIEW, CODE, "NAME", NAME)
                assert ok, "DB NAME=%%r != %%r" %% (act, NAME)
            step(page, "insert_db", _v_ins)
            print("  INSERT verified (grid + DB + NAME)")

            print("=== UPDATE ===")
            step(page, "update_ui", lambda: ec.updateObjectRecord(page, GRID_DATA_ID, CODE, update_fields))
            shot(page, "03_updated")
            def _v_upd():
                ok, an = db.field_equals(VIEW, CODE, "NAME", NAME_UPD)
                assert ok, "DB NAME=%%r != %%r" %% (an, NAME_UPD)
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
            results["self_clean"] = "CLEAN (0 residual)" if residual == 0 else ("RESIDUAL=%%d" %% residual)
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
        print("  %%s %%-12s: %%s" %% (mark, k, v))
    print("Overall:", "ALL PASS" if ok else "FAILURES")
    print("Evidence:", EVID)
    sys.exit(0 if ok else 1)
''' % dict(screen=screen, slug=slug, view_lc=view_lc, cpfx=cpfx, name_val=name_val,
           abbr=abbr, ins_block=ins_block, name_l=name_l, up=_up)

# ---- T3 insert keyword lines ----
t3_ins = [
    "    Fill OV Field By Label       objectForm    %s    ${code}" % code_l,
    "    Fill OV Field By Label       objectForm    %s    ${name}" % name_l,
    "    Fill OV Date By Label        objectForm    Start Date    ${start_date}",
]
for d in extra_dd:
    t3_ins.append("    Fill OV Dropdown By Label    objectForm    %s    __FIRST__" % d)
for pp in popups:
    t3_ins.append("    Pick OV Popup By Label       objectForm    %s    __FIRST__" % pp)
if has_op_pu:
    t3_ins.append("    Fill OV Dropdown By Label    objectForm    Op Production Unit    __FIRST__")
if parent_dd:
    t3_ins.append("    Fill OV Dropdown By Label    objectForm    %s    ${GM_PU}" % parent_dd)
t3_ins_block = "\n".join(t3_ins)

t3 = '''*** Settings ***
Documentation       T3 (screen) - %(screen)s page object.
...                 Screen: %(folder_h)s > %(screen)s.
...                 OV-GM (manage-object, groupmodel): the grid loads ONLY after the navigator
...                 cascade + GO (capability Apply OV-GM Navigator First Available). Fields resolved
...                 BY LABEL (no hardcoded rows). Extra dropdowns + Op Production Unit first-available.

Library             Browser
Library             %(up)slibraries/DbVerify.py
Resource            %(up)sresources/common.resource
Resource            %(up)sresources/manage_object.resource


*** Variables ***
${SCR}              %(screen)s
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${GM_PU}            ${EMPTY}


*** Keywords ***
Open %(screen)s Screen
    [Documentation]    Suite Setup: launch, login, navigate, fill the OV-GM navigator cascade
    ...    first-available + GO, RETURN the top-parent PU (grid empty until then).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    ${pu}=    Apply OV-GM Navigator First Available
    RETURN    ${pu}

%(screen)s Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

%(screen)s Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

%(screen)s Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in %(view)s.
    [Arguments]    ${code}
    Code Should Be Present In View    %(view)s    ${code}

%(screen)s Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from %(view)s.
    [Arguments]    ${code}
    Code Should Be Absent In View    %(view)s    ${code}

%(screen)s Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert %(screen)s Record
    [Documentation]    Insert (all fields BY LABEL) + Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
%(t3_ins_block)s
    Save And Refresh List

Update %(screen)s Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    %(name_l)s    ${new_name}
    Save And Refresh List

Delete %(screen)s
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
''' % dict(screen=screen, folder_h=folder.replace("/", " > "), view=view,
           t3_ins_block=t3_ins_block, name_l=name_l, up=_up)

suite = '''*** Settings ***
Documentation       EC IUD Test - %(screen)s (%(folder_h)s).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in %(view)s). NEVER touch existing data;
...                 a unique %(cpfx)s<timestamp> code is generated per run.

Resource            %(up)spageobjects/%(folder)s/%(slug)s_page.resource

Suite Setup         Set Up %(screen)s Suite
Suite Teardown      Close EC

Test Tags           iud    %(slug)s


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2000-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    %(screen)s Row Should Not Exist    ${TEST_CODE}
    Capture Step    %(slug)s_tc01_clean

TC02 Insert New %(screen)s
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert %(screen)s Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    %(screen)s Row Should Exist    ${TEST_CODE}
    %(screen)s Should Exist In DB    ${TEST_CODE}
    Capture Step    %(slug)s_tc02_inserted

TC03 Update %(screen)s Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update %(screen)s Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    %(screen)s Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    %(slug)s_tc03_updated

TC04 Delete %(screen)s
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete %(screen)s    ${TEST_CODE}    ${END_DATE}
    %(screen)s Row Should Not Exist    ${TEST_CODE}
    %(screen)s Should Not Exist In DB    ${TEST_CODE}
    Capture Step    %(slug)s_tc04_deleted


*** Keywords ***
Set Up %(screen)s Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    %(cpfx)s    %(name_short)s
    ${pu}=    Open %(screen)s Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
''' % dict(screen=screen, folder_h=folder.replace("/", " > "), view=view, cpfx=cpfx,
           folder=folder, slug=slug, name_short=name_l.replace(" Code", "").replace(" Name", ""), up=_up)

sow = '''# SOW - %(screen)s IUD (%(folder_h)s)

- **Screen:** %(screen)s   **BF:** %(bf)s   **View:** `%(view)s`   **Base:** `%(base)s`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
- Navigator cascade first-available + GO; fields BY LABEL; extra dropdowns + Op Production Unit first-available.
- IUD: INSERT -> UPDATE(Name) -> DELETE(End=Start). Test data `%(cpfx)s<timestamp>`; self-clean = absent in %(view)s.
- Deliverables: driver `py/%(slug)s_iud.py`, T3 `pageobjects/%(folder)s/%(slug)s_page.resource`,
  suite `tests/%(folder)s/%(slug)s_iud.robot`, this SOW, `VERIFY-REPORT.md` (auto-generated).
''' % dict(screen=screen, folder_h=folder.replace("/", " > "), bf=bf, view=view, base=base,
           cpfx=cpfx, slug=slug, folder=folder, up=_up)

readme = '''# %(screen)s - EC Object IUD bundle

**Screen:** %(folder_h)s > %(screen)s (BF %(bf)s). OV-GM (grid `manageObject:form:T_data`), navigator-GATED,
date-effective. Built on the item-1 gated-navigator capability (PR #244). See `%(slug)s_sow.md` +
`VERIFY-REPORT.md`. Driver `py/%(slug)s_iud.py`; T3/suite under `%(folder)s`.
''' % dict(screen=screen, folder_h=folder.replace("/", " > "), bf=bf, slug=slug, folder=folder, up=_up)

# ---- write ----
(EC / "py" / ("%s_iud.py" % slug)).write_text(driver, encoding="utf-8")
p_t3 = EC / "pageobjects" / folder / ("%s_page.resource" % slug); p_t3.parent.mkdir(parents=True, exist_ok=True)
p_t3.write_text(t3, encoding="utf-8")
p_su = EC / "tests" / folder / ("%s_iud.robot" % slug); p_su.parent.mkdir(parents=True, exist_ok=True)
p_su.write_text(suite, encoding="utf-8")
scr = EC / "screens" / folder / sfolder; scr.mkdir(parents=True, exist_ok=True)
(scr / ("%s_sow.md" % slug)).write_text(sow, encoding="utf-8")
(scr / "README.md").write_text(readme, encoding="utf-8")
# ASCII guard
for f in [EC/"py"/("%s_iud.py"%slug)]:
    bad = [c for c in f.read_text(encoding="utf-8") if ord(c) > 127]
    if bad:
        print("WARN non-ascii in", f, bad[:5])
print("WROTE bundle for", screen)
print("  driver:", (EC/"py"/("%s_iud.py"%slug)))
print("  t3    :", p_t3)
print("  suite :", p_su)
print("  screens:", scr)
print("  verify: py scripts/verify_screen.py --name %r --t3 %s --suite %s --driver %s --out %s/VERIFY-REPORT.md"
      % (screen, p_t3, p_su, EC/"py"/("%s_iud.py"%slug), scr))
