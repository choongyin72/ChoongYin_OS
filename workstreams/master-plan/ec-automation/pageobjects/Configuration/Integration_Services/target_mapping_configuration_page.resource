*** Settings ***
Documentation       T3 (screen) — Target Mapping Configuration page object.
...                 Screen: Configuration > Integration Services > Import > Target Mapping
...                 Configuration (IS.0002). DB: class IMP_TARGET_MAPPING (label "Import Target
...                 Mapping"), CLASS_TYPE=OBJECT, TIME_SCOPE_CODE=INVARIANT (no version table);
...                 verify view OV_IMP_TARGET_MAPPING.
...
...                 REDUCED SCOPE (owner-confirmed 2026-08-24, live-reconned this session): this
...                 screen does NOT support Insert/Update/Delete. Live DOM probe on this sandbox
...                 shows the Insert and Delete toolbar `<li>` both carry class
...                 `ui-submenu-state-disabled`, and there is no Update icon at all (count=0) - so
...                 this isn't merely "the owner said so", it is directly confirmed by this
...                 session's own recon, consistent with the owner's instruction. This page object
...                 therefore only exposes READ/FIND keywords - no Insert/Update/Delete keyword
...                 exists here on purpose, matching the "2 TC only" scope for this screen.
...
...                 NON-STANDARD ids (this screen only, confirmed live 2026-08-24 - do NOT copy the
...                 generic manage_object.resource navigator/GO ids for this screen):
...                   - Navigator filters (Class / Attribute / EC Key), none mandatory:
...                     StandardNavigator:form:G:0:R:1:C:0:in / C:1:in / C:2:in
...                     (NOT the usual nav:form:... ids)
...                   - GO button: buttongo:form:B (NOT button:form:B / go_button:form:B)
...                   - Grid body: imp_target_mapping_table:form:T_data (~20 real rows)
...                   - Grid columns are autocomplete-dropdown cells (`Cn_dd_input`), NOT plain
...                     <td> text, so the shared `table.resource` Get Table Rows (textContent-based)
...                     returns blank cells here - this page object reads `.value` via JS instead.
...                     Column order (0-based): 0=Class 1=Attribute 2=Ec Key 3=Class Key 1
...                     4=Class Key 2 ... (Class Key 3-10, Condition 1-3, From/To Unit, Constant
...                     String/Number/Date follow, unused by this suite).

Library             Browser
Library             ../../../libraries/DbVerify.py
Resource            ../../../resources/common.resource
Variables           ../../../resources/credentials.py


*** Variables ***
${TMC_SCREEN}       Target Mapping Configuration
${TMC_GRID_DATA}    imp_target_mapping_table:form:T_data
${TMC_NAV_CLASS}    StandardNavigator:form:G:0:R:1:C:0:in
${TMC_NAV_ATTR}     StandardNavigator:form:G:0:R:1:C:1:in
${TMC_NAV_KEY}      StandardNavigator:form:G:0:R:1:C:2:in
${TMC_GO}           buttongo:form:B


*** Keywords ***
Open Target Mapping Configuration Screen
    [Documentation]    Suite Setup: launch, login (screen-dedicated credentials), navigate.
    ...    Does NOT click GO yet - callers filter first, then call
    ...    Apply Target Mapping Configuration Navigator, matching this screen's real gesture
    ...    order (filters are optional, but GO is always required to load the grid).
    [Arguments]    ${user}=${TARGET_MAPPING_CONFIGURATION_EC_USER}    ${pass}=${TARGET_MAPPING_CONFIGURATION_EC_PASS}
    Launch EC And Open Screen    ${TMC_SCREEN}    ${user}    ${pass}

Apply Target Mapping Configuration Navigator
    [Documentation]    Click this screen's own non-standard GO (${TMC_GO}) to (re)load the grid.
    Click    css=[id="${TMC_GO}"]
    Wait For Load State    networkidle    timeout=15s
    Sleep    1s

Filter Target Mapping Configuration By Class
    [Documentation]    Type into the (optional) Class navigator filter. Does NOT click GO -
    ...    caller does that via Apply Target Mapping Configuration Navigator, so a caller can
    ...    combine multiple filters before applying.
    [Arguments]    ${class_value}
    Click    css=[id="${TMC_NAV_CLASS}"]
    Type Text    css=[id="${TMC_NAV_CLASS}"]    ${class_value}    clear=Yes

Target Mapping Configuration Row Count
    [Documentation]    Return the number of currently rendered data rows in the grid (the
    ...    tbody's own <tr> count) - used for the clean-state / baseline check in TC01, and by
    ...    the DB row-count-unchanged proof around the live run.
    ${n}=    Evaluate JavaScript    ${None}
    ...    () => { const tb = document.getElementById('${TMC_GRID_DATA}'); return tb ? tb.querySelectorAll('tr').length : 0; }
    RETURN    ${n}

Find Target Mapping Configuration Row
    [Documentation]    Read-only find: scan the currently-rendered grid rows for one whose
    ...    Class/Attribute/Ec Key/Class Key 1/Class Key 2 (columns 0-4, `Cn_dd_input.value`)
    ...    match the 5 given values. Returns the 0-based row index, or -1 if not found. Never
    ...    clicks/selects/modifies the row - pure read.
    [Arguments]    ${class_val}    ${attribute}    ${ec_key}    ${key1}    ${key2}
    ${row}=    Evaluate JavaScript    ${None}
    ...    () => { const tb = document.getElementById('${TMC_GRID_DATA}'); if (!tb) return -1;
    ...    const trs = tb.querySelectorAll('tr');
    ...    for (let i = 0; i < trs.length; i++) {
    ...    const g = (c) => { const el = trs[i].querySelector(`input[id\$=":C\${c}_dd_input"]`); return el ? el.value : null; };
    ...    if (g(0) === '${class_val}' && g(1) === '${attribute}' && g(2) === '${ec_key}' && g(3) === '${key1}' && g(4) === '${key2}') { return i; }
    ...    }
    ...    return -1; }
    RETURN    ${row}

Target Mapping Configuration Row Should Be Found
    [Documentation]    Assert the exact 5-field row is present in the currently rendered grid,
    ...    and its own fields read back match what was asked for (row-identity check, same
    ...    spirit as the standing "verify row identity" rule - even though this is read-only
    ...    with no Save at risk).
    [Arguments]    ${class_val}    ${attribute}    ${ec_key}    ${key1}    ${key2}
    ${row}=    Find Target Mapping Configuration Row
    ...    ${class_val}    ${attribute}    ${ec_key}    ${key1}    ${key2}
    Should Be True    ${row} >= 0
    ...    msg=Row not found: Class=${class_val} Attribute=${attribute} EcKey=${ec_key} Key1=${key1} Key2=${key2}

Target Mapping Configuration Row Should Exist In DB
    [Documentation]    DB ground-truth: assert this exact mapping (by its unique Ec Key) is
    ...    present in OV_IMP_TARGET_MAPPING. Read-only.
    [Arguments]    ${ec_key}
    Code Should Be Present In View    OV_IMP_TARGET_MAPPING    ${ec_key}

Target Mapping Configuration DB Row Count
    [Documentation]    DB ground-truth row count of OV_IMP_TARGET_MAPPING - used to prove the
    ...    suite mutated nothing (unchanged before/after the live run).
    ${n}=    View Row Count    OV_IMP_TARGET_MAPPING
    RETURN    ${n}
