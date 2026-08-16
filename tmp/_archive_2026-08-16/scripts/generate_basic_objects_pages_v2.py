"""Regenerate the 9 Basic Objects PAGE OBJECTS in thin best-practice form:
locator variables + one-line delegations to the T2 manage_object generics
(Fill New Object Form / Save And Refresh List / Update Object Name /
Delete Object Via End Date / Object Row Should Show Name).
Test suites are NOT touched (object_list/regulatory_permits suites carry
user-approved variable edits)."""
from pathlib import Path

PO_DIR = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/pageobjects/Configuration/Assets/Basic_Objects")

# slug, label, table, insR(code,name,date), updR(code,name), view, dropdown(label, R, arg) or None
SCREENS = [
    ("production_unit", "Production Unit", "manage_object_nav_nav:form:T_data", (0, 1, 4), (0, 1), "OV_PRODUCTIONUNIT", None),
    ("business_unit", "Business Unit", "manage_object_nav_nav:form:T_data", (0, 1, 2), (0, 1), "OV_BUSINESS_UNIT", None),
    ("country", "Country", "manage_object_nav_nav:form:T_data", (0, 1, 5), (0, 1), "OV_COUNTRY", None),
    ("state", "State", "manage_object_nav_nav:form:T_data", (2, 3, 4), (2, 3), "OV_STATE", None),
    ("county", "County", "manage_object_nav_nav:form:T_data", (2, 3, 5), (2, 3), "OV_COUNTY", None),
    ("region", "Region", "manage_object_nav_nav:form:T_data", (0, 1, 4), (0, 1), "OV_REGION", None),
    ("object_list", "Object List", "manage_object_nav_nav:form:T_data", (0, 1, 2), (0, 1), "OV_OBJECT_LIST",
     ("Class Name", 5, "class_name")),
    ("functional_area", "Functional Area", "manage_object_nav_nav:form:T_data", (0, 1, 2), (0, 1), "OV_FUNCTIONAL_AREA", None),
    ("regulatory_permits", "Regulatory Permits", "nav:form:T_data", (0, 1, 2), (0, 1), "OV_REGULATORY_PERMITS",
     ("Regulatory Agency", 4, "agency")),
    # production_sub_unit EXCLUDED 2026-06-11: operational groupmodel not enabled
    # in this environment - the grid can never list data (see registry).
]

TMPL = '''*** Settings ***
Documentation       T3 (screen) — {label} page object.
...                 Screen: Configuration > Assets > Basic Objects > {label}.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${{{UP}_SCREEN}}{p0}{label}
${{{UP}_TABLE}}{p1}{table}
# objectForm field IDs (Insert — new object)
${{{UP}_INS_CODE}}{p2}tab:tabPanel:objectForm:form:G:0:R:{ic}:C:1:in
${{{UP}_INS_NAME}}{p3}tab:tabPanel:objectForm:form:G:0:R:{iname}:C:1:in
${{{UP}_INS_DATE}}{p4}tab:tabPanel:objectForm:form:G:0:R:{idate}:C:1:da_input
{dd_var}# updateAttributes field IDs (Update — existing object)
${{{UP}_UPD_CODE}}{p5}tab:tabPanel:updateAttributes:form:G:0:R:{uc}:C:1:in
${{{UP}_UPD_NAME}}{p6}tab:tabPanel:updateAttributes:form:G:0:R:{uname}:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${{{UP}_DEL_ENDDATE}}{p7}tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open {label} Screen
    [Documentation]    Suite Setup: launch, login as ${{user}} (defaults to the env
    ...    user), navigate to the {label} screen. Pass a different user for role tests.
    [Arguments]    ${{user}}=${{EC_USER}}    ${{pass}}=${{EC_PASS}}
    Open EC Browser
    Login To EC    ${{user}}    ${{pass}}
    Navigate To Screen    ${{{UP}_SCREEN}}

{label} Row Should Exist
    [Documentation]    Assert a {lower} with ${{code}} is present in the list.
    [Arguments]    ${{code}}
    Row Should Exist    ${{{UP}_TABLE}}    ${{code}}

{label} Row Should Not Exist
    [Documentation]    Assert a {lower} with ${{code}} is absent from the list.
    [Arguments]    ${{code}}
    Row Should Not Exist    ${{{UP}_TABLE}}    ${{code}}

{label} Should Exist In DB
    [Documentation]    DB ground-truth: assert ${{code}} really persisted in {view}.
    [Arguments]    ${{code}}
    Code Should Be Present In View    {view}    ${{code}}

{label} Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${{code}} was truly deleted from {view}.
    [Arguments]    ${{code}}
    Code Should Be Absent In View    {view}    ${{code}}

{label} Row Should Show Name
    [Documentation]    Assert the {label} row for ${{code}} displays ${{name}}.
    [Arguments]    ${{code}}    ${{name}}
    Object Row Should Show Name    ${{{UP}_TABLE}}    ${{code}}    ${{name}}

Insert {label} Record
    [Documentation]    Insert a new {lower}: Code/Name/Start Date{dd_doc} -> Save.
    [Arguments]    ${{code}}    ${{name}}    ${{start_date}}{dd_arg}
    Fill New Object Form    ${{{UP}_INS_CODE}}    ${{{UP}_INS_NAME}}    ${{{UP}_INS_DATE}}
    ...    ${{code}}    ${{name}}    ${{start_date}}
{dd_step}    Save And Refresh List

Update {label} Name
    [Documentation]    Select the {lower}, edit Name, save + reload.
    [Arguments]    ${{code}}    ${{new_name}}
    Update Object Name    ${{{UP}_TABLE}}    ${{{UP}_UPD_CODE}}    ${{{UP}_UPD_NAME}}    ${{code}}    ${{new_name}}

Delete {label}
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${{code}}    ${{date}}
    Delete Object Via End Date    ${{{UP}_TABLE}}    ${{{UP}_DEL_ENDDATE}}    ${{code}}    ${{date}}
'''


def pad(varname, target=28):
    return " " * max(4, target - len(varname))


for slug, label, table, (ic, iname, idate), (uc, uname), view, dd in SCREENS:
    up = slug.upper()
    if dd:
        dd_label, dd_r, dd_argname = dd
        dd_var = (f"# {dd_label} is MANDATORY on this screen (EC: \"Required fields are empty\")\n"
                  f"${{{up}_INS_DD}}{pad(f'${{{up}_INS_DD}}')}tab:tabPanel:objectForm:form:G:0:R:{dd_r}:C:1:dd\n")
        dd_doc = f" + mandatory {dd_label}"
        dd_arg = f"    ${{{dd_argname}}}"
        dd_step = f"    Select EC Dropdown Option    ${{{up}_INS_DD}}    ${{{dd_argname}}}\n"
    else:
        dd_var, dd_doc, dd_arg, dd_step = "", "", "", ""
    out = TMPL.format(
        UP=up, label=label, lower=label.lower(), table=table, view=view,
        ic=ic, iname=iname, idate=idate, uc=uc, uname=uname,
        dd_var=dd_var, dd_doc=dd_doc, dd_arg=dd_arg, dd_step=dd_step,
        p0=pad(f"${{{up}_SCREEN}}"), p1=pad(f"${{{up}_TABLE}}"),
        p2=pad(f"${{{up}_INS_CODE}}"), p3=pad(f"${{{up}_INS_NAME}}"),
        p4=pad(f"${{{up}_INS_DATE}}"), p5=pad(f"${{{up}_UPD_CODE}}"),
        p6=pad(f"${{{up}_UPD_NAME}}"), p7=pad(f"${{{up}_DEL_ENDDATE}}"),
    )
    (PO_DIR / f"{slug}_page.resource").write_text(out, encoding="utf-8")
    print(f"regenerated (thin) {slug}_page.resource{' [+dd]' if dd else ''}")
print("done - tests untouched")
