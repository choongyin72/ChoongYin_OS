*** Settings ***
Documentation       T3 (screen) — Regulatory Permits page object.
...                 Screen: Configuration > Assets > Basic Objects > Regulatory Permits.
...                 Custom-URL OV screen (confirmed live 2026-08-23): grid id nav:form:T_data
...                 (NOT the manage_object_nav_ prefix), WITH a GO button (button:form:B count=1,
...                 unlike Account/Cost Centre which have none) - T2's Save And Refresh List
...                 auto-detects this and uses Apply Navigator. Field labels are SCREEN-PREFIXED
...                 ("Permit Code"/"Permit Name", confirmed live via the New Object form field
...                 dump - NOT the generic "Code"/"Name" Bank/Object List use, matching State's
...                 precedent that labels are never assumed). Regulatory Agency is a MANDATORY
...                 FORM FIELD dropdown on the Insert form (MandatoryCellStyle CSS class,
...                 confirmed live) - NOT a navigator/scope dropdown, so this screen stays
...                 genuinely nav-free per the batch-2 "confirmed nav-free" premise.
...                 Rebuilt 2026-08-23 (batch-2 Bank-pattern conversion) - replaces the older
...                 hardcoded-field-id pattern with the label-driven, properties-file-driven,
...                 T2-consolidated pattern already used by Bank/State/Account/Cost Centre.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${REGULATORY_PERMITS_SCREEN}          Regulatory Permits
${REGULATORY_PERMITS_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/regulatory_permits_insert.properties
${REGULATORY_PERMITS_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/regulatory_permits_update.properties
${REGULATORY_PERMITS_FORM_VERIFY}    ${CURDIR}/../../../../testdata/regulatory_permits_form_verify.properties
${REGULATORY_PERMITS_GRID_VERIFY}    ${CURDIR}/../../../../testdata/regulatory_permits_grid_verify.properties
# Custom-URL OV grid id (NOT the manage-object constant - confirmed live 2026-08-23: grid id is
# nav:form:T_data, matching Account/Cost Centre's convention, even though this screen DOES have a
# GO button unlike those two - Save And Refresh List handles either case automatically).
${REGULATORY_PERMITS_TABLE}    nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date). Row layout matches the framework-invariant
# shape already documented on Bank/State/Account (Start Date C:1, End Date label C:2, End Date
# input C:3) - reused from the pre-existing old-pattern file's own proven value.
${REGULATORY_PERMITS_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Regulatory Permits' own form-field label set for round-trip verification. Only Permit Code/
# Permit Name are listed (confirmed present in BOTH objectForm and updateAttributes) - Start Date
# and Regulatory Agency are Insert-only fields not yet confirmed present in updateAttributes (no
# live data existed to select+inspect an existing row on this sandbox; OV_REGULATORY_PERMITS is
# 0 rows before this suite's own TC02 creates the first one) - kept OUT of this list to avoid an
# unconfirmed claim, same discipline as Bank excluding its own Start Date for the same reason.
@{REGULATORY_PERMITS_FORM_LABELS}    Permit Code    Permit Name


*** Keywords ***
Find Regulatory Permits Row By Filter
    [Documentation]    Filter the Regulatory Permits grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource) - matches Account's/
    ...    Bank's own explicit filter usage (owner, 2026-08-22: "others... should follow
    ...    Account... utilise same filter feature"), wired in from the start for this batch.
    [Arguments]    ${code}
    Find Object Row By Filter    ${REGULATORY_PERMITS_TABLE}    ${code}

Clear Regulatory Permits Row Filter
    [Documentation]    Clear the Code column filter (see Find Regulatory Permits Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${REGULATORY_PERMITS_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Regulatory Permits' OWN credentials
    ...    (${REGULATORY_PERMITS_EC_USER}/${REGULATORY_PERMITS_EC_PASS} from credentials.py) on
    ...    the current page - works whether this is the very first login or a re-login after
    ...    Logout From EC Application. Zero-argument wrapper (matching Bank/Account convention)
    ...    that supplies Regulatory Permits' own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${REGULATORY_PERMITS_EC_USER}    ${REGULATORY_PERMITS_EC_PASS}

Open Regulatory Permits Screen
    [Documentation]    Navigate to the Regulatory Permits screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${REGULATORY_PERMITS_SCREEN}

Insert Regulatory Permits Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties And
    ...    Verify Code, so regulatory_permits_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked, matching
    ...    Bank/Account. Fills every field in regulatory_permits_insert.properties, including the
    ...    mandatory Regulatory Agency dropdown - auto-detected by kind.
    [Arguments]    ${properties_path}=${REGULATORY_PERMITS_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Permit Code
    RETURN    ${code}

Verify Regulatory Permits Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification (no
    ...    DB check here, matching Bank/Account's TC02 convention): row exists in the grid, then
    ...    the form shows what was just inserted (Permit Code/Permit Name - see
    ...    @{REGULATORY_PERMITS_FORM_LABELS}'s own docs for why Start Date/Regulatory Agency are
    ...    excluded). Delegates the full sequence to the shared T2 Verify Object Insert Exists.
    ...    Filters via Find Regulatory Permits Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Regulatory Permits Row By Filter    ${code}
    Verify Object Insert Exists    ${REGULATORY_PERMITS_TABLE}    ${code}    Regulatory Permits
    ...    ${REGULATORY_PERMITS_INSERT_PROPERTIES}    @{REGULATORY_PERMITS_FORM_LABELS}
    ...    code_label=Permit Code
    Clear Regulatory Permits Row Filter

Update Regulatory Permits Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Pre-save
    ...    evidence screenshot captured before Save is clicked, matching Bank/Account. Filters via
    ...    Find Regulatory Permits Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${REGULATORY_PERMITS_UPDATE_PROPERTIES}
    Find Regulatory Permits Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${REGULATORY_PERMITS_TABLE}    ${code}
    ...    ${properties_path}    ${TEST NAME}_action    code_label=Permit Code
    Clear Regulatory Permits Row Filter
    RETURN    ${data}

Verify Regulatory Permits Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification,
    ...    matching Bank/Account's TC03 convention: the form shows the updated Permit Name (the
    ...    only field regulatory_permits_update.properties lists). Delegates the full sequence to
    ...    the shared T2 Verify Object Form Record. Filters via Find Regulatory Permits Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Regulatory Permits Row By Filter    ${code}
    Verify Object Form Record    ${REGULATORY_PERMITS_TABLE}    ${code}    Regulatory Permits
    ...    ${REGULATORY_PERMITS_UPDATE_PROPERTIES}    Permit Name    code_label=Permit Code
    Clear Regulatory Permits Row Filter

Find Regulatory Permits Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates the full
    ...    select+capture sequence. Calls Find Regulatory Permits Row By Filter first. Deliberately
    ...    does NOT clear the filter afterward - Verify Regulatory Permits Record Found (called
    ...    right after, same TC) needs the grid still filtered for its own grid-check.
    [Arguments]    ${code}=${TEST_CODE}
    Find Regulatory Permits Row By Filter    ${code}
    Find Object Record    ${REGULATORY_PERMITS_TABLE}    ${code}    Regulatory Permits
    ...    code_label=Permit Code

Verify Regulatory Permits Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the form record match the expected (post-update) data. Delegates the full sequence to
    ...    the shared T2 Verify Object Found. Caller must already have selected the row (TC04
    ...    does, via Find Regulatory Permits Record before this) AND left the Code filter active -
    ...    this keyword clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${REGULATORY_PERMITS_TABLE}    ${code}
    ...    ${REGULATORY_PERMITS_GRID_VERIFY}    ${REGULATORY_PERMITS_FORM_VERIFY}
    ...    @{REGULATORY_PERMITS_FORM_LABELS}
    Clear Regulatory Permits Row Filter

Delete Regulatory Permits Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the permit, set End Date = Start Date (true delete), Save. Captures the TC05
    ...    evidence screenshot right after the End Date is filled but BEFORE Save is clicked,
    ...    matching Bank/Account. Filters via Find Regulatory Permits Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Regulatory Permits Row By Filter    ${code}
    Delete Object Via End Date    ${REGULATORY_PERMITS_TABLE}    ${REGULATORY_PERMITS_DEL_ENDDATE}
    ...    ${code}    ${date}    ${TEST NAME}_action
    Clear Regulatory Permits Row Filter

Verify Regulatory Permits Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid (filtered by Code = ${code} via Find Regulatory Permits Row By
    ...    Filter) and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Find Regulatory Permits Row By Filter    ${code}
    Verify Object Removed    ${REGULATORY_PERMITS_TABLE}    OV_REGULATORY_PERMITS    ${code}
    Clear Regulatory Permits Row Filter
    Capture Step    ${TEST NAME}_verify

Verify Regulatory Permits Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Filters the grid to
    ...    Code = ${code} first via Find Regulatory Permits Row By Filter, then delegates the
    ...    standard check + screenshot to the shared T2 Verify Object Does Not Exist, and clears
    ...    the filter after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Regulatory Permits Row By Filter    ${code}
    Verify Object Does Not Exist    ${REGULATORY_PERMITS_TABLE}    ${code}
    Clear Regulatory Permits Row Filter
