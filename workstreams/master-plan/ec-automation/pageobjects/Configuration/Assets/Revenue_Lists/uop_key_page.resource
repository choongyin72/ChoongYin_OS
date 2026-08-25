*** Settings ***
Documentation       T3 (screen) — UOP Key page object.
...                 Screen: Configuration > Assets > Revenue_Lists > UOP Key (CD.0099). Manage-Object (OV) screen.
...                 Holds UOP Key's locators + thin IUD wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Converted to full Bank-pattern shape (2026-08-25): properties-file-driven insert/update/verify,
...                 explicit Find/Clear Row By Filter grid-filter wiring, fixed AUTOTEST test code, 5-TC narrative
...                 (Clean State/Insert/Update/Find/Delete) with per-TC Login/Logout, PURE SCREEN verification only
...                 (no inline DB-verify keyword calls in uop_key_iud.robot - that deviation from the prior
...                 2026-07-26 generator-scaffolded build is what this conversion fixes, matching the fix already
...                 applied to County/DOA Credit Limit/Document Template/Document Sequence/Calculation Context/
...                 Royalty Depositor/Stream Item Category via GitHub Issue #504's sweep).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables            ../../../../resources/credentials.py


*** Variables ***
${UOP_KEY_SCREEN}          UOP Key
${UOP_KEY_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/uop_key_insert.properties
${UOP_KEY_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/uop_key_update.properties
${UOP_KEY_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/uop_key_form_verify.properties
${UOP_KEY_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/uop_key_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal string.
${UOP_KEY_TABLE}           ${OV_MANAGE_OBJECT_TABLE}
# UOP Key's own form-field label set (Start Date/End Date deliberately excluded - they live only
# in objectdates, not updateAttributes, same convention as Bank. Company/Key Type deliberately
# excluded too - both are mandatory reference dropdowns filled via __FIRST__ during Insert, whose
# resolved display text can differ after reload, same reason Bank excludes Country from its
# screen-compare label set).
@{UOP_KEY_FORM_LABELS}    Code    Name    Description    Comment    Key Number


*** Keywords ***
Find UOP Key Row By Filter
    [Documentation]    Explicitly filter the UOP Key grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource), matching Bank/Account's
    ...    own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${UOP_KEY_TABLE}    ${code}

Clear UOP Key Row Filter
    [Documentation]    Clear the Code column filter (see Find UOP Key Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${UOP_KEY_TABLE}

Login To EC Application
    [Documentation]    Authenticate as UOP Key's OWN credentials (${UOP_KEY_EC_USER}/
    ...    ${UOP_KEY_EC_PASS} from credentials.py) on the current page - works whether this is the
    ...    very first login (page freshly loaded on the login form via the shared T1 Open EC
    ...    Application) or a re-login after Logout From EC Application. Screen-specific wrapper
    ...    (matches Bank's convention: uop_key_iud.robot's test cases call this with ZERO
    ...    arguments) that supplies UOP Key's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${UOP_KEY_EC_USER}    ${UOP_KEY_EC_PASS}

Open UOP Key Screen
    [Documentation]    Navigate to the UOP Key screen. Assumes the caller already logged in this
    ...    test case (via Login To EC Application) - this keyword ONLY navigates (matches Bank's
    ...    per-TC login/logout convention, not a shared Suite Setup/Teardown login). Delegates to
    ...    the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${UOP_KEY_SCREEN}

Insert UOP Key Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, so uop_key_iud.robot's test case body reads as a plain business step with ZERO
    ...    arguments. Also owns the integrity check that the inserted Code matches the suite's
    ...    ${TEST_CODE} - fails on its own if testdata/uop_key_insert.properties' Code ever drifts
    ...    out of sync with the suite variable. The TC02 evidence screenshot is captured BEFORE
    ...    Save is clicked (matches Bank).
    [Arguments]    ${properties_path}=${UOP_KEY_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify UOP Key Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here): row exists in the grid, then every field's LIVE SCREEN value is
    ...    compared to testdata/uop_key_insert.properties via @{UOP_KEY_FORM_LABELS}. Delegates
    ...    the full sequence (row-check, select, form-compare, screenshot) to the shared T2 Verify
    ...    Object Insert Exists. Filters via Find UOP Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find UOP Key Row By Filter    ${code}
    Verify Object Insert Exists    ${UOP_KEY_TABLE}    ${code}    UOP Key    ${UOP_KEY_INSERT_PROPERTIES}
    ...    @{UOP_KEY_FORM_LABELS}
    Clear UOP Key Row Filter

Update UOP Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns the
    ...    applied {label: value} dict so the caller can DB-verify against exactly what was set.
    ...    The TC03 evidence screenshot is captured BEFORE Save is clicked. Filters via Find UOP
    ...    Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${UOP_KEY_UPDATE_PROPERTIES}
    Find UOP Key Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${UOP_KEY_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    Clear UOP Key Row Filter
    RETURN    ${data}

Verify UOP Key Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check): selects the row (loading updateAttributes), then compares Name's LIVE SCREEN
    ...    value to testdata/uop_key_update.properties - only that label, since that's the only
    ...    field the file has. Delegates the full sequence to the shared T2 Verify Object Form
    ...    Record. Filters via Find UOP Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find UOP Key Row By Filter    ${code}
    Verify Object Form Record    ${UOP_KEY_TABLE}    ${code}    UOP Key    ${UOP_KEY_UPDATE_PROPERTIES}
    ...    Name
    Clear UOP Key Row Filter

Find UOP Key Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates the full
    ...    select+capture sequence. Calls Find UOP Key Row By Filter first. Deliberately does NOT
    ...    clear the filter afterward - Verify UOP Key Record Found (called right after, same TC)
    ...    needs the grid still filtered to ${code} for its own grid-check; it clears the filter
    ...    once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find UOP Key Row By Filter    ${code}
    Find Object Record    ${UOP_KEY_TABLE}    ${code}    UOP Key

Verify UOP Key Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND the
    ...    full form record match the expected data. Delegates the full sequence to the shared T2
    ...    Verify Object Found. Caller must already have selected the row (TC04 does, via Find UOP
    ...    Key Record before this) AND left the Code filter active from that same call - clears the
    ...    filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${UOP_KEY_TABLE}    ${code}    ${UOP_KEY_GRID_VERIFY_PROPERTIES}
    ...    ${UOP_KEY_FORM_VERIFY_PROPERTIES}    @{UOP_KEY_FORM_LABELS}
    Clear UOP Key Row Filter

Delete UOP Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the uop_key, set End Date = Start Date (true delete), Save. Captures the TC05
    ...    evidence screenshot right after the End Date is filled but BEFORE Save is clicked.
    ...    UNLIKE Bank (which hardcodes its End Date field id - a documented row-packing shape
    ...    proven for OV_BANK), UOP Key's End Date id is resolved LIVE via OV Field Id By Label
    ...    (label-driven) - the same mechanism the prior 2026-07-26 build already proved for this
    ...    exact field ("Fill OV Date By Label objectdates End Date"), so this is not a fresh
    ...    guess. Filters via Find UOP Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find UOP Key Row By Filter    ${code}
    Select Object Row    ${UOP_KEY_TABLE}    ${code}
    ${enddate_id}=    OV Field Id By Label    objectdates    End Date
    Delete Object Via End Date    ${UOP_KEY_TABLE}    ${enddate_id}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear UOP Key Row Filter

Verify UOP Key Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_FIN_UOP_DEPR_KEY) - the shared DB-ground-truth
    ...    keyword, just called under one name.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${UOP_KEY_TABLE}    OV_FIN_UOP_DEPR_KEY    ${code}
    Capture Step    ${TEST NAME}_verify

Verify UOP Key Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${UOP_KEY_TABLE}    ${code}
