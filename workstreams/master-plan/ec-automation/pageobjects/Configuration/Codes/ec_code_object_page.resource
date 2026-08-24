*** Settings ***
Documentation       T3 (screen) — EC Code Object page object.
...                 Screen: Configuration > Codes > EC Code Object (CD.0135). Manage-Object (OV) screen.
...                 Converted to the full Bank-pattern shape (2026-08-24): was previously a PARTIAL
...                 label-driven build (had Fill OV Field By Label for Object Code/Name, but no
...                 properties-file-driven insert/update/verify and no explicit grid-filter wiring).
...                 Now matches bank_page.resource/berth_page.resource exactly: properties-file-driven
...                 insert/update/verify, explicit `Find/Clear EC Code Object Row By Filter` wired into
...                 Update/Find/Verify-Found/Delete, fixed test code, per-TC Login/Logout, 5 TCs, PURE
...                 SCREEN verification (no inline DB-verify in the T3/test file - the prior 4-TC suite
...                 called Field Should Equal In View directly from the test file, which the Bank
...                 convention keeps out of the test file entirely).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved
...                 by LABEL via T2 (Fill OV * By Label / Fill OV Field By Label Any Kind).

Library             Browser
Library             ../../../libraries/DbVerify.py
Library             ../../../libraries/PropertiesReader.py
Resource            ../../../resources/common.resource
Resource            ../../../resources/manage_object.resource
Variables           ../../../resources/credentials.py


*** Variables ***
${ECO_SCREEN}           EC Code Object
${ECO_INSERT_PROPERTIES}    ${CURDIR}/../../../testdata/ec_code_object_insert.properties
${ECO_UPDATE_PROPERTIES}    ${CURDIR}/../../../testdata/ec_code_object_update.properties
${ECO_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../testdata/ec_code_object_form_verify.properties
${ECO_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../testdata/ec_code_object_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal string
# (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
${ECO_TABLE}            ${OV_MANAGE_OBJECT_TABLE}
# EC Code Object's own form-field label set. Labels are GENERIC ("Object Code"/"Name"), NOT
# screen-prefixed like Disposition Type's "Disposition Code"/"Disposition Name" - confirmed live
# from this screen's own already-proven OV Field Id By Label usage (Object Code/Name/Start Date).
# Defined ONCE here so both Verify EC Code Object Record Exists (TC02) and Verify EC Code Object
# Record Found (TC04) share the same list.
@{ECO_FORM_LABELS}      Object Code    Name


*** Keywords ***
Find EC Code Object Row By Filter
    [Documentation]    Explicitly filter the EC Code Object grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches Bank's/
    ...    Disposition Type's own explicit filter usage, rather than relying only on Select Object
    ...    Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${ECO_TABLE}    ${code}

Clear EC Code Object Row Filter
    [Documentation]    Clear the Code column filter (see Find EC Code Object Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${ECO_TABLE}

Login To EC Application
    [Documentation]    Authenticate as EC Code Object's OWN credentials (${EC_CODE_OBJECT_EC_USER}/
    ...    ${EC_CODE_OBJECT_EC_PASS} from credentials.py) on the current page - works whether this is
    ...    the very first login (page freshly loaded on the login form via the shared T1 Open EC
    ...    Application) or a re-login after Logout From EC Application (same login form, not a new
    ...    page/tab). Screen-specific wrapper (matches Bank's convention: ec_code_object_iud.robot's
    ...    test cases call this with ZERO arguments) that supplies EC Code Object's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the actual
    ...    login mechanics.
    Login To EC Screen    ${EC_CODE_OBJECT_EC_USER}    ${EC_CODE_OBJECT_EC_PASS}

Open EC Code Object Screen
    [Documentation]    Navigate to the EC Code Object screen, then click GO to populate the grid
    ...    (this screen has NO default rows on open, unlike Bank). Assumes the caller already logged
    ...    in this test case (via Login To EC Application) - this keyword ONLY navigates, matching
    ...    Bank's per-TC Login/Open/action/Logout convention.
    Open EC Screen    ${ECO_SCREEN}
    Apply Navigator

Insert EC Code Object Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, purely so ec_code_object_iud.robot's test case body reads as a plain business step
    ...    with ZERO arguments - the underlying mechanics (properties-file-driven insert) are
    ...    UNCHANGED. Also owns the integrity check that the inserted Code matches the suite's
    ...    ${TEST_CODE}. The TC02 evidence screenshot is captured BEFORE Save is clicked (passed
    ...    through to Insert Object From Properties, which fills every field first).
    [Arguments]    ${properties_path}=${ECO_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Object Code
    RETURN    ${code}

Verify EC Code Object Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification: row
    ...    exists in the grid, then every field's LIVE SCREEN value (via Get OV Field Value By Label)
    ...    is compared to testdata/ec_code_object_insert.properties (the file used to insert, not the
    ...    post-update ec_code_object_form_verify.properties) - Object Code, Name (${ECO_FORM_LABELS}).
    ...    NOTE: Start Date is NOT verified here - it only exists as a grid column / objectForm-
    ...    objectdates field, not an updateAttributes field (matches Bank's own convention).
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the shared T2
    ...    Verify Object Insert Exists. Filters via Find EC Code Object Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}
    Find EC Code Object Row By Filter    ${code}
    Verify Object Insert Exists    ${ECO_TABLE}    ${code}    EC Code Object
    ...    ${ECO_INSERT_PROPERTIES}    @{ECO_FORM_LABELS}    code_label=Object Code
    Clear EC Code Object Row Filter

Update EC Code Object Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns the applied
    ...    {label: value} dict so the caller can DB-verify against exactly what was set. The TC03
    ...    evidence screenshot is captured BEFORE Save is clicked (passed through to Update Object
    ...    From Properties, which fills every field first). Filters via Find EC Code Object Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${ECO_UPDATE_PROPERTIES}
    Find EC Code Object Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${ECO_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Object Code
    Clear EC Code Object Row Filter
    RETURN    ${data}

Verify EC Code Object Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification: selects
    ...    the row (loading updateAttributes), then compares Name's LIVE SCREEN value (via Get OV
    ...    Field Value By Label) to testdata/ec_code_object_update.properties - only that label, since
    ...    that's the only field that file has. Delegates the full sequence (select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Form Record. Filters via Find EC Code Object Row
    ...    By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find EC Code Object Row By Filter    ${code}
    Verify Object Form Record    ${ECO_TABLE}    ${code}    EC Code Object
    ...    ${ECO_UPDATE_PROPERTIES}    Name    code_label=Object Code
    Clear EC Code Object Row Filter

Find EC Code Object Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates the full
    ...    select+capture sequence. Calls Find EC Code Object Row By Filter first. Deliberately does
    ...    NOT clear the filter afterward - Verify EC Code Object Record Found (called right after,
    ...    same TC) needs the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find EC Code Object Row By Filter    ${code}
    Find Object Record    ${ECO_TABLE}    ${code}    EC Code Object    code_label=Object Code

Verify EC Code Object Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND the
    ...    full form record match the expected data - the SAME two existing live-DOM round-trip
    ...    keywords, just called under one name. Also captures the TC04 evidence screenshot.
    ...    Delegates the full sequence (grid-compare, form-compare, screenshot) to the shared T2
    ...    Verify Object Found. Caller must already have selected the row (TC04 does, via Find EC
    ...    Code Object Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${ECO_TABLE}    ${code}    ${ECO_GRID_VERIFY_PROPERTIES}
    ...    ${ECO_FORM_VERIFY_PROPERTIES}    @{ECO_FORM_LABELS}
    Clear EC Code Object Row Filter

Delete EC Code Object Record And Save
    [Documentation]    Select the EC Code Object, resolve the objectdates End Date field id BY LABEL
    ...    at runtime (this screen's own already-proven convention - unlike Bank/Disposition Type,
    ...    whose objectdates row packs Start Date + End Date on the SAME row and needs a hardcoded id,
    ...    EC Code Object's objectdates only has an End Date row, so the one-field-per-row label scan
    ...    resolves it safely - confirmed live via this screen's pre-existing Delete EC Code Object
    ...    keyword, which already did exactly this), set End Date = Start Date (true delete), Save.
    ...    Called with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/
    ...    ${END_DATE}). Captures the TC05 evidence screenshot right after the End Date is filled but
    ...    BEFORE Save is clicked. Filters via Find EC Code Object Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find EC Code Object Row By Filter    ${code}
    Select Object Row    ${ECO_TABLE}    ${code}
    ${enddate_id}=    OV Field Id By Label    objectdates    End Date
    Delete Object By Zero-Length Window    ${enddate_id}    ${date}
    Capture Step    ${TEST NAME}_action
    Save And Refresh List
    Clear EC Code Object Row Filter

Verify EC Code Object Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent from
    ...    BOTH the grid and the database - the SAME two existing DB-ground-truth keywords, just
    ...    called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${ECO_TABLE}    OV_EC_CODE_OBJECT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify EC Code Object Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared T2
    ...    Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${ECO_TABLE}    ${code}
