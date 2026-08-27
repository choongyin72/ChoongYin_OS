*** Settings ***
Documentation       T3 (screen) — Well Bore page object.
...                 Screen: Configuration > Assets > Well_and_Reservoir_Objects > Well Bore (CO.0054).
...                 OV-GM (groupmodel manage-object) screen whose navigator is PER-FIELD groups
...                 nav:form:G:1..G:4:R:1:C:0 (Production Unit / Area / Facility Class 1 / 'Well &
...                 Well Hookup') — NOT a same-row C:1..C:N cascade, so the shared T2 "Apply
...                 Navigator From Properties" (resources/manage_object.resource) does not cover
...                 this shape (see that keyword's own documented "KNOWN LIMITATION" for PER-FIELD
...                 groups — this is exactly that gap). A 5th group G:5 ('Well') is scan-flagged
...                 mandatory (CSS) but offers ZERO options under every scope tried — confirmed by
...                 the pre-existing proven driver py/well_bore_iud.py (recon 2026-07-31,
...                 re-verified live 2026-08-27) — it is deliberately left EMPTY; GO succeeds and
...                 the grid loads on 4 levels (verified: 'P1 W008 WB001' lists). Converted to the
...                 Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE (2026-08-27) via a
...                 BESPOKE screen-local T3 navigator keyword (modeled on well_page.resource's own
...                 prior "Apply Well Navigator" precedent and Equipment's "Apply Equipment
...                 Navigator" per-field-group pattern) — resources/manage_object.resource was NOT
...                 touched.
...                 Mandatory objectForm field: 'Well' POPUP whose list grid is
...                 `Objects:form:T_data` (NOT PopupList:form:T_data) — screen-local picker below;
...                 picks the nav-scope well by value (the popup's FIRST row is a graph object,
...                 deliberately not used). DELETE = End Date = Start Date (true delete in
...                 OV_WELL_BORE).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Resource            ../../../../resources/navigator.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${WELL_BORE_SCREEN}     Well Bore
${WELL_BORE_TABLE}      manageObject:form:T_data
# navigator (groupmodel): PER-FIELD groups G:1..G:4, each R:1:C:0 — MANDATORY before the grid
# loads. G:5 ('Well') is deliberately excluded (zero usable options, confirmed by the
# pre-existing driver). Values confirmed live via py/well_bore_iud.py's own proven NAV tuple —
# carried over verbatim, not invented.
${WELL_BORE_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/well_bore_navigator.properties
${WELL_BORE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/well_bore_insert.properties
${WELL_BORE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/well_bore_update.properties
${WELL_BORE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/well_bore_form_verify.properties
${WELL_BORE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/well_bore_grid_verify.properties
# 'Well' POPUP grid (screen-local; NOT the generic PopupList:form:T_data). FIELD-REUSE RULE: this
# is the SAME value as G:4's navigator fill (P1 W008 OP) — the popup must pick the nav-scope well,
# not its own first row (a graph object with no bores).
${WELL_BORE_POPUP_GRID}    Objects:form:T_data
${WELL_BORE_NAV_WELL}      P1 W008 OP
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven —
# same documented rationale as Area's/Well's/Bank's own DEL_ENDDATE constants. Value reused
# verbatim from the pre-existing Well Bore driver's own ${DEL_ENDDATE}.
${WELL_BORE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Well Bore's own form-field label set (Start Date deliberately excluded — same convention as
# Well/Area's own label sets: it lives in objectdates' fill-once trio, not the round-trip
# comparison set here).
@{WELL_BORE_FORM_LABELS}    Well Bore Code    Well Bore Name


*** Keywords ***
Find Well Bore Row By Filter
    [Documentation]    Explicitly filter the Well Bore grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource), matching every
    ...    other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${WELL_BORE_TABLE}    ${code}

Clear Well Bore Row Filter
    [Documentation]    Clear the Code column filter (see Find Well Bore Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${WELL_BORE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Well Bore's OWN credentials (${WELL_BORE_EC_USER}/
    ...    ${WELL_BORE_EC_PASS} from credentials.py) on the current page - works whether this is
    ...    the very first login (page freshly loaded on the login form via the shared T1 Open EC
    ...    Application) or a re-login after Logout From EC Application (same login form, not a
    ...    new page/tab).
    Login To EC Screen    ${WELL_BORE_EC_USER}    ${WELL_BORE_EC_PASS}

Apply Well Bore Navigator From Properties
    [Documentation]    BESPOKE screen-local T3 navigator keyword — this screen's navigator is
    ...    PER-FIELD groups (a distinct nav:form:G:<n> group per cascade level, each addressed at
    ...    its own R:1:C:0), NOT a same-row C:1..C:N cascade, so the shared T2 "Apply Navigator
    ...    From Properties" (resources/manage_object.resource) explicitly does not cover this
    ...    shape (documented there as a KNOWN LIMITATION). Modeled on well_page.resource's own
    ...    prior "Apply Well Navigator" precedent and Equipment's "Apply Equipment Navigator"
    ...    (pageobjects/.../Equipment_Objects/equipment_page.resource) per-field-group pattern:
    ...    reads ${properties_path} (one line per group, in FILE ORDER — the keys, e.g. "G:1", are
    ...    free-form documentation only, NOT resolved by DOM lookup), fills nav:form:G:<n>:R:1:C:0
    ...    for n = 1, 2, 3, 4 in that order via the shared T1 "Set Navigator Filter"
    ...    (resources/navigator.resource), then clicks GO ("Apply Navigator") exactly ONCE at the
    ...    end. Group 5 ('Well') is deliberately NEVER filled — it is scan-flagged mandatory (CSS)
    ...    but offers zero usable options under every scope tried (confirmed by the pre-existing
    ...    driver py/well_bore_iud.py); GO succeeds anyway and the grid loads on 4 levels. This
    ...    keyword lives entirely in well_bore_page.resource — resources/manage_object.resource is
    ...    NOT touched by this conversion.
    [Arguments]    ${properties_path}=${WELL_BORE_NAVIGATOR_PROPERTIES}
    ${data}=    Read Properties    ${properties_path}
    VAR    ${group}    ${1}
    FOR    ${label}    IN    @{data.keys()}
        Set Navigator Filter    G:${group}    ${data}[${label}]
        ${group}=    Evaluate    ${group} + 1
    END
    Apply Navigator

Open Well Bore Screen With Navigator Values Populated
    [Documentation]    Navigate to the Well Bore screen, THEN fill + submit the mandatory 4-level
    ...    PER-FIELD-group navigator (Production Unit -> Area -> Facility Class 1 -> Well & Well
    ...    Hookup, one dropdown per group + GO) - Well Bore's grid stays empty until this happens,
    ...    so this single keyword bundles both steps for the test case (owner's exact skeleton
    ...    calls this as ONE line per TC, not two). Assumes the caller already logged in this test
    ...    case (via Login To EC Application) - matches every other Area-pattern-converted
    ...    screen's "Open <Screen> Screen" convention, extended here with the genuine per-field-
    ...    group OV-GM navigator gesture via the BESPOKE "Apply Well Bore Navigator From
    ...    Properties" keyword above (NOT the shared T2 keyword - see that keyword's own
    ...    documentation for why).
    Open EC Screen    ${WELL_BORE_SCREEN}
    Apply Well Bore Navigator From Properties    ${WELL_BORE_NAVIGATOR_PROPERTIES}

Pick Well Popup
    [Documentation]    Screen-LOCAL picker for the mandatory 'Well' POPUP field on objectForm:
    ...    waits for the real list grid `Objects:form:T_data` (the generic T1/T2 popup helpers
    ...    wait for PopupList:form:T_data and so report a false 'empty source list' on this
    ...    screen), then clicks the row whose value equals ${want} (defaults to the nav-scope
    ...    well, ${WELL_BORE_NAV_WELL} - the popup's FIRST row is a graph object with no bores,
    ...    deliberately not used). Carried over verbatim from the pre-existing proven driver's
    ...    own screen-local picker (py/well_bore_iud.py's pick_well_popup / this file's prior
    ...    "Pick Well Popup").
    [Arguments]    ${pin_id}    ${want}=${WELL_BORE_NAV_WELL}
    Evaluate JavaScript    ${None}    () => document.getElementById('${pin_id}B').click()
    Wait For Elements State    css=[id="popupIFrame"]    visible    timeout=15s
    Wait For Elements State    css=[id="popupIFrame"] >>> css=[id="${WELL_BORE_POPUP_GRID}"]    visible    timeout=15s
    Sleep    1.5s
    ${found}=    Evaluate JavaScript
    ...    css=[id="popupIFrame"] >>> css=[id="${WELL_BORE_POPUP_GRID}"]
    ...    (tbody) => { let hit = false; tbody.querySelectorAll('tr').forEach(tr => { const inp = tr.querySelector('td input'); const v = inp ? inp.value.trim() : (tr.innerText || '').trim(); if (!hit && v.startsWith('${want}')) { hit = true; tr.querySelector('td').click(); } }); return hit; }
    Should Be True    ${found}    msg=Well popup row '${want}' not found in ${WELL_BORE_POPUP_GRID}
    Wait For Elements State    css=[id="popupIFrame"]    hidden    timeout=15s
    Sleep    1s
    ${val}=    Get Property    css=[id="${pin_id}"]    value
    Should Not Be Empty    ${val}    msg=Well popup pick did not fill the pin field

Insert Well Bore Record And Save
    [Documentation]    Friendly-narrative wrapper mirroring the shared T2 "Insert Object From
    ...    Properties And Verify Code" shape, but screen-LOCAL because this screen's insert form
    ...    has an extra mandatory step the shared T2 keyword does not know about: the 'Well' POPUP
    ...    (screen-local picker above), filled AFTER the label-driven text/date fields and BEFORE
    ...    Save. Reads ${properties_path} (Well Bore Code/Well Bore Name/Start Date) via the same
    ...    PropertiesReader mechanism T2 uses, fills each by label, picks the Well popup, saves,
    ...    and asserts the resulting Code matches ${expected_code} (integrity check, same as T2's
    ...    own "Insert Object From Properties And Verify Code").
    [Arguments]    ${properties_path}=${WELL_BORE_INSERT_PROPERTIES}    ${expected_code}=${TEST_CODE}
    ${data}=    Read Properties    ${properties_path}
    Open New Object Form
    Fill OV Field By Label    objectForm    Well Bore Code    ${data}[Well Bore Code]
    Fill OV Field By Label    objectForm    Well Bore Name    ${data}[Well Bore Name]
    Fill OV Date By Label     objectForm    Start Date    ${data}[Start Date]
    ${pin}=    Get Attribute
    ...    xpath=//span[contains(@class,'ECCell') and contains(@id,':objectForm:form:') and normalize-space(text())='Well']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input[substring(@id, string-length(@id) - 3) = ':pin']
    ...    id
    Pick Well Popup    ${pin}
    Save And Refresh List
    Should Be Equal As Strings    ${data}[Well Bore Code]    ${expected_code}
    ...    msg=Inserted Well Bore Code does not match the suite's TEST_CODE

Verify Well Bore Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Well Bore Code/Well Bore Name's LIVE SCREEN value is compared to
    ...    testdata/well_bore_insert.properties. Filters via Find Well Bore Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Well Bore Row By Filter    ${code}
    Verify Object Insert Exists    ${WELL_BORE_TABLE}    ${code}    Well Bore    ${WELL_BORE_INSERT_PROPERTIES}
    ...    @{WELL_BORE_FORM_LABELS}    code_label=Well Bore Code
    Clear Well Bore Row Filter

Update Well Bore Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Well
    ...    Bore Name is listed in testdata/well_bore_update.properties - Well Bore Code is
    ...    read-only in updateAttributes. Filters via Find Well Bore Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${WELL_BORE_UPDATE_PROPERTIES}
    Find Well Bore Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${WELL_BORE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Well Bore Code
    Clear Well Bore Row Filter
    RETURN    ${data}

Verify Well Bore Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Well Bore Name's LIVE SCREEN value to
    ...    testdata/well_bore_update.properties. Filters via Find Well Bore Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Well Bore Row By Filter    ${code}
    Verify Object Form Record    ${WELL_BORE_TABLE}    ${code}    Well Bore    ${WELL_BORE_UPDATE_PROPERTIES}
    ...    Well Bore Name    code_label=Well Bore Code
    Clear Well Bore Row Filter

Find Well Bore Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Well
    ...    Bore Row By Filter first. Deliberately does NOT clear the filter afterward - Verify
    ...    Well Bore Record Found (called right after, same TC) needs the grid still filtered to
    ...    ${code} for its own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Well Bore Row By Filter    ${code}
    Find Object Record    ${WELL_BORE_TABLE}    ${code}    Well Bore    code_label=Well Bore Code

Verify Well Bore Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Well Bore Record before this) AND left the Code filter active
    ...    - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${WELL_BORE_TABLE}    ${code}    ${WELL_BORE_GRID_VERIFY_PROPERTIES}
    ...    ${WELL_BORE_FORM_VERIFY_PROPERTIES}    @{WELL_BORE_FORM_LABELS}
    Clear Well Bore Row Filter

Delete Well Bore Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the Well Bore, set End Date = Start Date (EC true delete for OV_WELL_BORE),
    ...    Save. Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List
    ...    (inside T2) already re-applies the navigator, so the assertion reads a fresh list.
    ...    Filters via Find Well Bore Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Well Bore Row By Filter    ${code}
    Delete Object Via End Date    ${WELL_BORE_TABLE}    ${WELL_BORE_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Well Bore Row Filter

Verify Well Bore Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_WELL_BORE) - the DB check lives here, in the
    ...    shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword (same
    ...    convention Well/Area's own conversions use).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${WELL_BORE_TABLE}    OV_WELL_BORE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Well Bore Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${WELL_BORE_TABLE}    ${code}
