*** Settings ***
Documentation       T3 (screen) — DOA Credit Limit page object.
...                 Screen: Configuration > Assets > Financial Objects > DOA Credit Limit.
...                 Manage-Object (OV) screen (navigator = manage-object, standard GO button,
...                 grid manage_object_nav_nav:form:T_data - live-confirmed 2026-08-23 via
...                 tmp/recon_doa.robot). Rebuilt 2026-08-23 (Batch 4) to mirror Bank/VAT Code
...                 exactly - replaces the older hardcoded-field-id pattern with the label-driven,
...                 properties-file-driven, T2-consolidated pattern.
...                 Live-confirmed 2026-08-23 (tmp/recon_doa.robot + tmp/recon_doa2.robot -
...                 deleted before final commit): this screen's own Code/Name fields are
...                 SCREEN-PREFIXED ("DOA Credit Limit Code"/"DOA Credit Limit Name"), not the
...                 generic "Code"/"Name" a plain manage-object screen usually has - never assumed
...                 from Bank's convention. Mandatory extras confirmed via a raw outerHTML dump
...                 ({mandatory:true} MandatoryCellStyle on each): "DOA Type" (reference dropdown,
...                 literal "Amount Based" - confirmed live to be the first of 2 real options:
...                 Amount Based/Quantity Based), "Credit Limit" (numeric text, ECNumberCell), and
...                 "Role Name" (reference dropdown, literal "ANALYTICS.REPORTADMIN" - confirmed
...                 live to be the first of 33 real catalogued options). Both dropdowns use their
...                 literal first-option text (NOT __FIRST__) deliberately - TC02's Verify DOA
...                 Credit Limit Record Exists compares the LIVE SCREEN back against the SAME
...                 insert properties file (T2's Verify Object Insert Exists), so a __FIRST__
...                 placeholder would never match the resolved option text (VAT Code/Account
...                 precedent). Currency is ALSO included despite its static CSS class being
...                 {mandatory:false} (UOM alone stays out) - a first live Save attempt without
...                 it failed with a real EC business-rule validation banner ("Amount Based DOA
...                 Requires a currency", confirmed 2026-08-23 via tmp/recon_doa3_save.robot,
...                 deleted before final commit): a genuine CONDITIONAL-mandatory rule tied to
...                 DOA Type=Amount Based, invisible to the static MandatoryCellStyle scan alone.
...                 Currency=USD (a real catalogued option, matching this screen's own
...                 pre-existing production rows). Grid shows exactly 4 columns (Code/Name/Start
...                 Date/End Date - confirmed live). Find/Clear DOA Credit Limit Row By Filter
...                 wired in from the start per the batch-4 shared findings doc, matching Bank/
...                 VAT Code's own filter-wiring convention.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${DOA_CREDIT_LIMIT_SCREEN}          DOA Credit Limit
${DOA_CREDIT_LIMIT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/doa_credit_limit_insert.properties
${DOA_CREDIT_LIMIT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/doa_credit_limit_update.properties
${DOA_CREDIT_LIMIT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/doa_credit_limit_form_verify.properties
${DOA_CREDIT_LIMIT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/doa_credit_limit_grid_verify.properties
# Grid id: reuse T2's centralized constant (plain manage-object OV, live-confirmed 2026-08-23).
${DOA_CREDIT_LIMIT_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Framework-invariant shape already
# documented/proven on Bank/Account/VAT Code (Start Date C:1, End Date label C:2, End Date input
# C:3) - not re-verified this session per the batch shared findings doc (recon budget spent on
# the field-level facts instead); confirmed to work at live TC05 run time below.
${DOA_CREDIT_LIMIT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# DOA Credit Limit's own form-field label set (Start Date excluded - confirmed live absent from
# updateAttributes, objectForm/Insert-only). Defined ONCE here so both Verify DOA Credit Limit
# Record Exists (TC02, against doa_credit_limit_insert.properties) and Verify DOA Credit Limit
# Record Found (TC04, against doa_credit_limit_form_verify.properties) share the same list.
# "Role Name" is DELIBERATELY excluded here - live-confirmed 2026-08-23 that once
# updateAttributes is (re)loaded after Save, this dropdown re-renders showing the option's
# DESCRIPTION text ("Report Administrator"), not the raw code used to select it
# ("ANALYTICS.REPORTADMIN") - a live-DOM round-trip check against the same insert-value literal
# would always fail here (confirmed live: "Field 'Role Name' shows 'Report Administrator' in
# updateAttributes, expected 'ANALYTICS.REPORTADMIN'"). ROLE_ID is still independently verified
# via DB ground-truth (DOA Credit Limit Should Exist In DB, OV_DOA_CREDIT_LIMIT.ROLE_ID stores the
# raw code) - matching Bank's own precedent of picking ONE canonical representation per field
# when the DB/screen display genuinely differ, and documenting the choice.
@{DOA_CREDIT_LIMIT_FORM_LABELS}    DOA Credit Limit Code    DOA Credit Limit Name    DOA Type
...    Credit Limit    Currency


*** Keywords ***
Find DOA Credit Limit Row By Filter
    [Documentation]    Filter the DOA Credit Limit grid's Code column to ${code}, matching Bank/
    ...    VAT Code's own explicit filter usage (batch shared findings doc: wire the filter in
    ...    from the start). Thin wrapper around the shared T2 Find Object Row By Filter
    ...    (resources/manage_object.resource).
    [Arguments]    ${code}
    Find Object Row By Filter    ${DOA_CREDIT_LIMIT_TABLE}    ${code}

Clear DOA Credit Limit Row Filter
    [Documentation]    Clear the Code column filter (see Find DOA Credit Limit Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${DOA_CREDIT_LIMIT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as DOA Credit Limit's OWN credentials
    ...    (${DOA_CREDIT_LIMIT_EC_USER}/${DOA_CREDIT_LIMIT_EC_PASS} from credentials.py) on the
    ...    current page. Zero-argument wrapper so doa_credit_limit_iud.robot's test cases read as
    ...    a plain business step; supplies DOA Credit Limit's own credential defaults to the
    ...    shared T1 Login To EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${DOA_CREDIT_LIMIT_EC_USER}    ${DOA_CREDIT_LIMIT_EC_PASS}

Open DOA Credit Limit Screen
    [Documentation]    Navigate to the DOA Credit Limit screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${DOA_CREDIT_LIMIT_SCREEN}

Insert DOA Credit Limit Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties And
    ...    Verify Code, so doa_credit_limit_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked. Passes
    ...    code_label=DOA Credit Limit Code since this screen's own Code field label is
    ...    screen-prefixed, not the generic "Code".
    [Arguments]    ${properties_path}=${DOA_CREDIT_LIMIT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=DOA Credit Limit Code
    RETURN    ${code}

Verify DOA Credit Limit Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification (no
    ...    DB check here, matching Bank/VAT Code's TC02 convention): row exists in the grid, then
    ...    the form shows what was just inserted (${DOA_CREDIT_LIMIT_FORM_LABELS}). Delegates the
    ...    full sequence (row-check, select, form-compare, screenshot) to the shared T2 Verify
    ...    Object Insert Exists. Calls Find DOA Credit Limit Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find DOA Credit Limit Row By Filter    ${code}
    Verify Object Insert Exists    ${DOA_CREDIT_LIMIT_TABLE}    ${code}    DOA Credit Limit
    ...    ${DOA_CREDIT_LIMIT_INSERT_PROPERTIES}    @{DOA_CREDIT_LIMIT_FORM_LABELS}
    ...    code_label=DOA Credit Limit Code
    Clear DOA Credit Limit Row Filter

Update DOA Credit Limit Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Pre-save
    ...    evidence screenshot captured before Save is clicked. Calls Find DOA Credit Limit Row
    ...    By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${DOA_CREDIT_LIMIT_UPDATE_PROPERTIES}
    Find DOA Credit Limit Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${DOA_CREDIT_LIMIT_TABLE}    ${code}
    ...    ${properties_path}    ${TEST NAME}_action    code_label=DOA Credit Limit Code
    Clear DOA Credit Limit Row Filter
    RETURN    ${data}

Verify DOA Credit Limit Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification,
    ...    matching Bank/VAT Code's TC03 convention: the form shows the updated Name (the only
    ...    field doa_credit_limit_update.properties lists). Delegates the full sequence (select,
    ...    form-compare, screenshot) to the shared T2 Verify Object Form Record. Calls Find DOA
    ...    Credit Limit Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find DOA Credit Limit Row By Filter    ${code}
    Verify Object Form Record    ${DOA_CREDIT_LIMIT_TABLE}    ${code}    DOA Credit Limit
    ...    ${DOA_CREDIT_LIMIT_UPDATE_PROPERTIES}    DOA Credit Limit Name
    ...    code_label=DOA Credit Limit Code
    Clear DOA Credit Limit Row Filter

Find DOA Credit Limit Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates the full
    ...    select+capture sequence. Calls Find DOA Credit Limit Row By Filter first. Deliberately
    ...    does NOT clear the filter afterward - Verify DOA Credit Limit Record Found (called
    ...    right after, same TC) needs the grid still filtered to ${code} for its own grid-check,
    ...    since it doesn't re-select the row itself; it clears the filter once both checks are
    ...    done.
    [Arguments]    ${code}=${TEST_CODE}
    Find DOA Credit Limit Row By Filter    ${code}
    Find Object Record    ${DOA_CREDIT_LIMIT_TABLE}    ${code}    DOA Credit Limit
    ...    code_label=DOA Credit Limit Code

Verify DOA Credit Limit Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the form record match the expected (post-update) data. Delegates the full sequence
    ...    (grid-compare, form-compare, screenshot) to the shared T2 Verify Object Found. Caller
    ...    must already have selected the row (TC04 does, via Find DOA Credit Limit Record before
    ...    this) AND left the Code filter active from that same call - this keyword clears the
    ...    filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${DOA_CREDIT_LIMIT_TABLE}    ${code}
    ...    ${DOA_CREDIT_LIMIT_GRID_VERIFY_PROPERTIES}    ${DOA_CREDIT_LIMIT_FORM_VERIFY_PROPERTIES}
    ...    @{DOA_CREDIT_LIMIT_FORM_LABELS}
    Clear DOA Credit Limit Row Filter

Delete DOA Credit Limit Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the doa credit limit, set End Date = Start Date (true delete), Save. Captures
    ...    the TC05 evidence screenshot right after the End Date is filled but BEFORE Save is
    ...    clicked. Calls Find DOA Credit Limit Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find DOA Credit Limit Row By Filter    ${code}
    Delete Object Via End Date    ${DOA_CREDIT_LIMIT_TABLE}    ${DOA_CREDIT_LIMIT_DEL_ENDDATE}
    ...    ${code}    ${date}    ${TEST NAME}_action
    Clear DOA Credit Limit Row Filter

Verify DOA Credit Limit Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid (filtered by Code = ${code} via Find DOA Credit Limit Row By
    ...    Filter) and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Find DOA Credit Limit Row By Filter    ${code}
    Verify Object Removed    ${DOA_CREDIT_LIMIT_TABLE}    OV_DOA_CREDIT_LIMIT    ${code}
    Clear DOA Credit Limit Row Filter
    Capture Step    ${TEST NAME}_verify

Verify DOA Credit Limit Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Filters the grid to
    ...    Code = ${code} first via Find DOA Credit Limit Row By Filter, then delegates the
    ...    standard check + screenshot to the shared T2 Verify Object Does Not Exist, and clears
    ...    the filter after.
    [Arguments]    ${code}=${TEST_CODE}
    Find DOA Credit Limit Row By Filter    ${code}
    Verify Object Does Not Exist    ${DOA_CREDIT_LIMIT_TABLE}    ${code}
    Clear DOA Credit Limit Row Filter
