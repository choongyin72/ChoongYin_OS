*** Settings ***
Documentation       T3 (screen) — Blend page object.
...                 Screen: Configuration > Assets > Hydrocarbon Objects > Blend (CO.0219).
...                 Manage-Object (OV) screen. Holds Blend's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Converted from the partial label-driven pattern to the full properties-file-
...                 driven, grid-filter-wired, T2-consolidated "Bank pattern" (Batch 7, 2026-08-23).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${BLEND_SCREEN}          Blend
${BLEND_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/blend_insert.properties
${BLEND_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/blend_update.properties
${BLEND_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/blend_form_verify.properties
${BLEND_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/blend_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
${BLEND_TABLE}          ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - same documented shape as Bank's own ${BANK_DEL_ENDDATE} / Customer's own
# ${CUSTOMER_DEL_ENDDATE} (live-confirmed 2026-08-23 on Blend itself via a fresh recon: the
# objectdates row packs TWO fields, Start Date C:1 / End Date C:3, with the End Date label at
# C:2 - identical shape to Bank/Customer).
${BLEND_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Blend's field labels are "Blend Code"/"Blend Name" (screen-prefixed, matching State's own
# "State Code"/"State Name" precedent) - NOT the generic "Code"/"Name" Bank/Customer use.
# Confirmed live 2026-08-23: objectForm carries Master System Code, Master System Name,
# Blend Code*, Blend Name*, Start Date*(mandatory), End Date, Sort Order, Description
# (MandatoryCellStyle only on Blend Code/Blend Name/Start Date's data cells - confirmed via a
# fresh per-row class dump); updateAttributes carries the same set minus the two Date fields
# (Blend Code read-only there). ${BLEND_CODE_LABEL} is threaded through every T2 call that
# needs to resolve the Code field by label (matching State's own code_label= usage).
${BLEND_CODE_LABEL}    Blend Code
# Defined ONCE here so both Verify Blend Record Exists (TC02, against blend_insert.properties)
# and Verify Blend Record Found (TC04, against blend_form_verify.properties) share the same list.
@{BLEND_FORM_LABELS}    Blend Code    Blend Name    Description


*** Keywords ***
Find Blend Row By Filter
    [Documentation]    Explicitly filter the Blend grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource) - matches Bank's/
    ...    Customer's/State's own explicit filter usage (owner, 2026-08-22: "others... should
    ...    follow Account... utilise same filter feature"), rather than relying only on Select
    ...    Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${BLEND_TABLE}    ${code}

Clear Blend Row Filter
    [Documentation]    Clear the Code column filter (see Find Blend Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${BLEND_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Blend's OWN credentials (${BLEND_EC_USER}/
    ...    ${BLEND_EC_PASS} from credentials.py) on the current page - works whether this is
    ...    the very first login (page freshly loaded on the login form via the shared T1 Open
    ...    EC Application) or a re-login after Logout From EC Application (same login form, not
    ...    a new page/tab). Screen-specific wrapper (matches Bank's/Customer's own pattern) that
    ...    supplies Blend's own credential defaults to the shared T1 Login To EC Screen
    ...    (common.resource), which owns the actual login mechanics - kept here only because a
    ...    shared file should not hardcode any screen's credentials.
    Login To EC Screen    ${BLEND_EC_USER}    ${BLEND_EC_PASS}

Open Blend Screen
    [Documentation]    Navigate to the Blend screen. Assumes the caller already logged in this
    ...    test case (via Login To EC Application) - this keyword ONLY navigates, matching the
    ...    per-TC login/logout convention (each test case gets its own explicit Login/Logout
    ...    step instead of one shared Suite Setup/Teardown login). Delegates to the shared T1
    ...    Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${BLEND_SCREEN}

Insert Blend Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And
    ...    Verify Code, so blend_iud.robot's test case body reads as a plain business step with
    ...    ZERO arguments - the underlying mechanics (properties-file-driven insert) are
    ...    UNCHANGED. Also owns the integrity check that the inserted Code matches the suite's
    ...    ${TEST_CODE} - this keyword fails on its own if testdata/blend_insert.properties'
    ...    Blend Code ever drifts out of sync with the suite variable. The TC02 evidence
    ...    screenshot is captured BEFORE Save is clicked, passed through to Insert Object From
    ...    Properties, which fills every field first. Passes code_label=${BLEND_CODE_LABEL}
    ...    since Blend's Code field is labeled "Blend Code", not the generic "Code".
    [Arguments]    ${properties_path}=${BLEND_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=${BLEND_CODE_LABEL}
    RETURN    ${code}

Verify Blend Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check here): row exists in the grid, then every field's LIVE
    ...    SCREEN value (via Get OV Field Value By Label) is compared to
    ...    testdata/blend_insert.properties (the file used to insert, not the post-update
    ...    blend_form_verify.properties) - Blend Code, Blend Name, Description
    ...    (${BLEND_FORM_LABELS}). Start Date is NOT verified here - it only exists as a grid
    ...    column / objectdates field, not an updateAttributes field. Delegates the full
    ...    sequence (row-check, select, form-compare, screenshot) to the shared T2 Verify Object
    ...    Insert Exists. Filters via Find Blend Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Blend Row By Filter    ${code}
    Verify Object Insert Exists    ${BLEND_TABLE}    ${code}    Blend    ${BLEND_INSERT_PROPERTIES}
    ...    @{BLEND_FORM_LABELS}    code_label=${BLEND_CODE_LABEL}
    Clear Blend Row Filter

Update Blend Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns
    ...    the applied {label: value} dict so the caller can DB-verify against exactly what was
    ...    set. The TC03 evidence screenshot is captured BEFORE Save is clicked. Filters via
    ...    Find Blend Row By Filter first, clears after. Passes code_label=${BLEND_CODE_LABEL}
    ...    so the row-identity check (Code read back from updateAttributes) resolves "Blend
    ...    Code", not the generic "Code" label that doesn't exist on this screen.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${BLEND_UPDATE_PROPERTIES}
    Find Blend Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${BLEND_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=${BLEND_CODE_LABEL}
    Clear Blend Row Filter
    RETURN    ${data}

Verify Blend Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check): selects the row (loading updateAttributes), then compares
    ...    Blend Name/Description's LIVE SCREEN value (via Get OV Field Value By Label) to
    ...    testdata/blend_update.properties - only those two labels, since that's the only
    ...    fields that file has. Delegates the full sequence (select, form-compare, screenshot)
    ...    to the shared T2 Verify Object Form Record. Filters via Find Blend Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Blend Row By Filter    ${code}
    Verify Object Form Record    ${BLEND_TABLE}    ${code}    Blend    ${BLEND_UPDATE_PROPERTIES}
    ...    Blend Name    Description    code_label=${BLEND_CODE_LABEL}
    Clear Blend Row Filter

Find Blend Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates
    ...    the full select+capture sequence. Calls Find Blend Row By Filter first. Deliberately
    ...    does NOT clear the filter afterward - Verify Blend Record Found (called right after,
    ...    same TC) needs the grid still filtered to ${code} for its own grid-check; it clears
    ...    the filter once both checks are done. Passes code_label=${BLEND_CODE_LABEL}, matching
    ...    State's own precedent for a screen-prefixed Code label.
    [Arguments]    ${code}=${TEST_CODE}
    Find Blend Row By Filter    ${code}
    Find Object Record    ${BLEND_TABLE}    ${code}    Blend    code_label=${BLEND_CODE_LABEL}

Verify Blend Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid
    ...    AND the full form record match the expected data - the SAME two existing live-DOM
    ...    round-trip keywords, just called under one name. Also captures the TC04 evidence
    ...    screenshot. Delegates the full sequence (grid-compare, form-compare, screenshot) to
    ...    the shared T2 Verify Object Found. Caller must already have selected the row (TC04
    ...    does, via Find Blend Record before this) AND left the Code filter active from that
    ...    same call - clears the filter itself once both checks are done. Matches State's own
    ...    usage (no code_label needed here - Verify Object Found doesn't resolve the Code field
    ...    by label the way Insert/Update/Find do).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${BLEND_TABLE}    ${code}    ${BLEND_GRID_VERIFY_PROPERTIES}
    ...    ${BLEND_FORM_VERIFY_PROPERTIES}    @{BLEND_FORM_LABELS}
    Clear Blend Row Filter

Delete Blend Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the blend, set End Date = Start Date (true delete), Save. Captures the TC05
    ...    evidence screenshot right after the End Date is filled but BEFORE Save is clicked.
    ...    Filters via Find Blend Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Blend Row By Filter    ${code}
    Delete Object Via End Date    ${BLEND_TABLE}    ${BLEND_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Blend Row Filter

Verify Blend Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database - the SAME two existing DB-ground-truth
    ...    keywords, just called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${BLEND_TABLE}    OV_BLEND    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Blend Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${BLEND_TABLE}    ${code}
