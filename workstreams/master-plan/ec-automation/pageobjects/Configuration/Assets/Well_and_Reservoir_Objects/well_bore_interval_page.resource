*** Settings ***
Documentation       T3 (screen) — Well Bore Interval page object.
...                 Screen: Configuration > Assets > Well_and_Reservoir_Objects > Well Bore
...                 Interval (CO.0057). OV-GM, PER-FIELD nav groups nav:form:G:1..G:6:R:1:C:0 (NOT
...                 a same-row/increasing-column cascade) — live-confirmed 2026-08-27
...                 (Workplaces/well-bore-interval-area-pattern/recon_wbi_nav_live.py, read-only,
...                 no save): G:1 Production Unit / G:2 Area / G:3 Facility Class 1 / G:4
...                 'Well & Well Hookup' = P1 W008 OP (a REAL well) / G:6 = the WELL BORE
...                 P1 W008 WB001. G:5 ('Well') exists in the DOM and shows mandatory-yellow
...                 styling when empty, but offers ZERO usable options under this scope — the
...                 already-proven py/well_bore_interval_iud.py driver skips it and GO still
...                 succeeds, confirmed again live this session. Because the shared T2
...                 "Apply Navigator From Properties" (resources/manage_object.resource) only
...                 covers the single-row/increasing-column cascade shape, this screen's
...                 navigator-fill is a BESPOKE, screen-local T3 keyword ("Apply Well Bore
...                 Interval Navigator" below), modeled on well_page.resource's pre-2026-08-26
...                 "Apply Well Navigator" keyword (the project's precedent for a per-field-groups
...                 screen) — resources/manage_object.resource is NOT touched for this screen.
...                 Mandatory form field: 'Well Bore' POPUP whose list grid is
...                 `Objects:form:T_data` (NOT the generic `PopupList:form:T_data` the shared
...                 "Fill OV Field By Label Any Kind" auto-detector expects) — screen-local
...                 picker below, reusing the SAME value as the navigator's G:6 fill
...                 (FIELD-REUSE RULE). DELETE = End Date = Start Date.
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (2026-08-27) on top of the 2026-07-31 base build (verify_screen PASS, RF 4/4 +
...                 Playwright 8/8) — this conversion is structural only; the genuine per-field
...                 navigator + mandatory popup gestures are kept, not removed.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Resource            ../../../../resources/navigator.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${WBI_SCREEN}       Well Bore Interval
${WBI_TABLE}        manageObject:form:T_data
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven
# — same documented rationale as Area's/Well's own del-enddate variables. Value reused verbatim
# from the pre-existing well_bore_interval_page.resource's ${DEL_ENDDATE}.
${WBI_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${WBI_NAVIGATOR_PROPERTIES}      ${CURDIR}/../../../../testdata/well_bore_interval_navigator.properties
${WBI_INSERT_PROPERTIES}         ${CURDIR}/../../../../testdata/well_bore_interval_insert.properties
${WBI_UPDATE_PROPERTIES}         ${CURDIR}/../../../../testdata/well_bore_interval_update.properties
${WBI_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/well_bore_interval_form_verify.properties
${WBI_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/well_bore_interval_grid_verify.properties
# Well Bore popup grid — screen-LOCAL (not the generic PopupList:form:T_data). Same value as the
# navigator's G:6 fill (FIELD-REUSE RULE), read straight out of the navigator properties file at
# insert time (see "Insert Well Bore Interval Record And Save" below) so it is never duplicated.
${WBI_POPUP_GRID}    Objects:form:T_data
# Well Bore Interval's own form-field label set (Start Date deliberately excluded — it lives only
# in objectForm's own fill-once trio at insert time, not in updateAttributes; the mandatory 'Well
# Bore' popup is deliberately excluded from round-trip label comparison — same documented caveat
# as every other converted screen's popup/dropdown fields, which can re-render different display
# text after reload).
@{WBI_FORM_LABELS}    Well Bore Interval Code    Well Bore Interval Name


*** Keywords ***
Login To EC Application
    [Documentation]    Authenticate as Well Bore Interval's OWN credentials
    ...    (${WELL_BORE_INTERVAL_EC_USER}/${WELL_BORE_INTERVAL_EC_PASS} from credentials.py) on
    ...    the current page — works whether this is the very first login (page freshly loaded on
    ...    the login form via the shared T1 Open EC Application) or a re-login after Logout From
    ...    EC Application (same login form, not a new page/tab).
    Login To EC Screen    ${WELL_BORE_INTERVAL_EC_USER}    ${WELL_BORE_INTERVAL_EC_PASS}

Open Well Bore Interval Screen With Navigator Values Populated
    [Documentation]    Navigate to the Well Bore Interval screen, THEN fill + submit the
    ...    mandatory per-field navigator groups (G:1/G:2/G:3/G:4/G:6, GO once) — the grid stays
    ...    empty until this happens, so this single keyword bundles both steps for the test case
    ...    (one line per TC, matching every other Area-pattern-converted screen's convention).
    ...    Assumes the caller already logged in this test case (via Login To EC Application).
    Open EC Screen    ${WBI_SCREEN}
    Apply Well Bore Interval Navigator

Apply Well Bore Interval Navigator
    [Documentation]    BESPOKE T3 navigator-fill (per-field groups, NOT the shared T2 "Apply
    ...    Navigator From Properties" — that keyword only supports the single-row/
    ...    increasing-column cascade shape, confirmed not applicable here). Reads
    ...    testdata/well_bore_interval_navigator.properties (column=value, key = the group's
    ...    business label, value = the group's option), maps each key to its known group id
    ...    (G:1 Production Unit / G:2 Area / G:3 Facility Class 1 / G:4 'Well & Well Hookup' /
    ...    G:6 'Well Bore'), fills each group in file order, then clicks GO ONCE — modeled on
    ...    well_page.resource's pre-2026-08-26 "Apply Well Navigator" keyword (the project's
    ...    precedent for a genuinely per-field-groups navigator). G:5 ('Well') is deliberately
    ...    OMITTED from the properties file and this fill loop — live-confirmed present in the
    ...    DOM but offering ZERO usable options under this scope (Workplaces/
    ...    well-bore-interval-area-pattern/recon_wbi_nav_live.py, 2026-08-27); the already-proven
    ...    py/well_bore_interval_iud.py driver skips it the same way and GO still succeeds.
    ${data}=    Read Properties    ${WBI_NAVIGATOR_PROPERTIES}
    Select Nav Group Value    1    ${data}[Production Unit]
    Select Nav Group Value    2    ${data}[Area]
    Select Nav Group Value    3    ${data}[Facility Class 1]
    Select Nav Group Value    4    ${data}[Well & Well Hookup]
    Select Nav Group Value    6    ${data}[Well Bore]
    Apply Navigator

Select Nav Group Value
    [Documentation]    Set one per-field navigator group (nav:form:G:<group>:R:1:C:0:dd) to
    ...    ${value}. Screen-local helper used only by Apply Well Bore Interval Navigator above —
    ...    this per-field-groups shape has no shared T2 equivalent (the shared keyword assumes a
    ...    single row, increasing column).
    [Arguments]    ${group}    ${value}
    Select EC Dropdown Option    nav:form:G:${group}:R:1:C:0:dd    ${value}
    Sleep    0.8s

Pick Well Bore Popup
    [Documentation]    Screen-LOCAL picker for the mandatory 'Well Bore' popup behind
    ...    ${pin_prefix}: waits for the real list grid `Objects:form:T_data` (the generic T2
    ...    "Pick OV Popup By Label"/"Pick From EC Object Popup" wait for `PopupList:form:T_data`
    ...    and would report a false 'empty source' here), then clicks the row whose value starts
    ...    with ${want} (the navigator's own G:6 well-bore value — FIELD-REUSE RULE). Ported
    ...    verbatim from the pre-existing well_bore_interval_page.resource's own picker.
    [Arguments]    ${pin_prefix}    ${want}
    Evaluate JavaScript    ${None}    () => document.getElementById('${pin_prefix}B').click()
    Wait For Elements State    css=[id="popupIFrame"]    visible    timeout=15s
    Wait For Elements State    css=[id="popupIFrame"] >>> css=[id="${WBI_POPUP_GRID}"]    visible    timeout=15s
    Sleep    1.5s
    ${found}=    Evaluate JavaScript
    ...    css=[id="popupIFrame"] >>> css=[id="${WBI_POPUP_GRID}"]
    ...    (tbody) => { let hit = false; tbody.querySelectorAll('tr').forEach(tr => { const inp = tr.querySelector('td input'); const v = inp ? inp.value.trim() : (tr.innerText || '').trim(); if (!hit && v.startsWith('${want}')) { hit = true; tr.querySelector('td').click(); } }); return hit; }
    Should Be True    ${found}    msg=Well Bore popup row '${want}' not found in ${WBI_POPUP_GRID}
    Wait For Elements State    css=[id="popupIFrame"]    hidden    timeout=15s
    Sleep    1s
    ${val}=    Get Property    css=[id="${pin_prefix}"]    value
    Should Not Be Empty    ${val}    msg=Well Bore popup pick did not fill the pin field

Find Well Bore Interval Row By Filter
    [Documentation]    Explicitly filter the Well Bore Interval grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    every other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${WBI_TABLE}    ${code}

Clear Well Bore Interval Row Filter
    [Documentation]    Clear the Code column filter (see Find Well Bore Interval Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${WBI_TABLE}

Insert Well Bore Interval Record And Save
    [Documentation]    Open the New Object form, fill every field in
    ...    testdata/well_bore_interval_insert.properties (Code/Name/Start Date, by label), THEN
    ...    pick the mandatory 'Well Bore' popup (screen-local — reuses the navigator's own G:6
    ...    value, FIELD-REUSE RULE, read straight from the navigator properties file so the value
    ...    is never duplicated), THEN Save + reload. Also asserts the inserted code matches the
    ...    suite's ${TEST_CODE} — same integrity check every other converted screen's insert
    ...    wrapper performs. Called with ZERO arguments so well_bore_interval_iud.robot's test
    ...    case body reads as a plain business step.
    [Arguments]    ${properties_path}=${WBI_INSERT_PROPERTIES}
    ${data}=    Read Properties    ${properties_path}
    ${nav}=    Read Properties    ${WBI_NAVIGATOR_PROPERTIES}
    Open New Object Form
    FOR    ${label}    IN    @{data.keys()}
        Fill OV Field By Label Any Kind    objectForm    ${label}    ${data}[${label}]
    END
    ${pin}=    Get Attribute
    ...    xpath=//span[contains(@class,'ECCell') and contains(@id,':objectForm:form:') and normalize-space(text())='Well Bore']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input[substring(@id, string-length(@id) - 3) = ':pin']
    ...    id
    Pick Well Bore Popup    ${pin}    ${nav}[Well Bore]
    Save And Refresh List
    Should Be Equal    ${data}[Well Bore Interval Code]    ${TEST_CODE}
    ...    msg=${properties_path} Code does not match the expected ${TEST_CODE}

Verify Well Bore Interval Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here — that is TC02's own separate DbVerify assertion): row exists in the
    ...    grid, then Well Bore Interval Code/Name's LIVE SCREEN value is compared to
    ...    testdata/well_bore_interval_insert.properties. Filters via Find Well Bore Interval Row
    ...    By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Well Bore Interval Row By Filter    ${code}
    Verify Object Insert Exists    ${WBI_TABLE}    ${code}    Well Bore Interval    ${WBI_INSERT_PROPERTIES}
    ...    @{WBI_FORM_LABELS}    code_label=Well Bore Interval Code
    Clear Well Bore Interval Row Filter

Update Well Bore Interval Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Well
    ...    Bore Interval Name is listed in testdata/well_bore_interval_update.properties — Code is
    ...    read-only in updateAttributes. Filters via Find Well Bore Interval Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${WBI_UPDATE_PROPERTIES}
    Find Well Bore Interval Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${WBI_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Well Bore Interval Code
    Clear Well Bore Interval Row Filter
    RETURN    ${data}

Verify Well Bore Interval Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Well Bore Interval Name's LIVE SCREEN value to
    ...    testdata/well_bore_interval_update.properties. Filters via Find Well Bore Interval Row
    ...    By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Well Bore Interval Row By Filter    ${code}
    Verify Object Form Record    ${WBI_TABLE}    ${code}    Well Bore Interval    ${WBI_UPDATE_PROPERTIES}
    ...    Well Bore Interval Name    code_label=Well Bore Interval Code
    Clear Well Bore Interval Row Filter

Find Well Bore Interval Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Well
    ...    Bore Interval Row By Filter first. Deliberately does NOT clear the filter afterward —
    ...    Verify Well Bore Interval Record Found (called right after, same TC) needs the grid
    ...    still filtered to ${code} for its own grid-check; it clears the filter once both
    ...    checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Well Bore Interval Row By Filter    ${code}
    Find Object Record    ${WBI_TABLE}    ${code}    Well Bore Interval    code_label=Well Bore Interval Code

Verify Well Bore Interval Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Well Bore Interval Record before this) AND left the Code
    ...    filter active — clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${WBI_TABLE}    ${code}    ${WBI_GRID_VERIFY_PROPERTIES}
    ...    ${WBI_FORM_VERIFY_PROPERTIES}    @{WBI_FORM_LABELS}
    Clear Well Bore Interval Row Filter

Delete Well Bore Interval Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the row, set End Date = Start Date (EC true delete for OV_WELL_BORE_INTERVAL),
    ...    Save. Filters via Find Well Bore Interval Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Well Bore Interval Row By Filter    ${code}
    Delete Object Via End Date    ${WBI_TABLE}    ${WBI_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Well Bore Interval Row Filter

Verify Well Bore Interval Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_WELL_BORE_INTERVAL) — the DB check lives here,
    ...    in the shared T2 Verify Object Removed, NOT as a separate screen-local DB wrapper
    ...    keyword (removed by this conversion).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${WBI_TABLE}    OV_WELL_BORE_INTERVAL    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Well Bore Interval Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) — delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${WBI_TABLE}    ${code}
