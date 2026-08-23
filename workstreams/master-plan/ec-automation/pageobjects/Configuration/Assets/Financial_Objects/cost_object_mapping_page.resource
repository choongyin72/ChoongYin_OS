*** Settings ***
Documentation       T3 (screen) — Cost Object Mapping page object.
...                 Screen: Configuration > Assets > Financial Objects > Cost Object Mapping.
...                 Manage-Object (OV) screen. Holds Cost Object Mapping's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 4) to mirror Bank/Customer exactly - replaces the
...                 older hardcoded-field-id pattern with the label-driven, properties-file-
...                 driven, T2-consolidated pattern.
...                 Live-confirmed 2026-08-23 (tmp/recon_com.py + tmp/recon_com_insert.py +
...                 tmp/recon_com_cleanup.py - deleted before final commit): objectForm order is
...                 Code, Alternative Code, Name, Start Date, End Date, Description, Object
...                 Type, Cost Object, Line Item Type, Company, Node, Product, Distribution
...                 Object Type, Profit Centre. FOUR mandatory reference dropdowns beyond
...                 Code/Name (confirmed via the same MandatoryCellStyle-on-wrapping-<span>
...                 technique documented on VAT Code/Customer): Object Type, Cost Object,
...                 Company, Distribution Object Type. Cost Object is a CASCADE dropdown -
...                 empty ("Dependent field 'Start Date' is empty" banner) until BOTH Start
...                 Date and Object Type are already set, so testdata/
...                 cost_object_mapping_insert.properties lists Start Date and Object Type
...                 BEFORE Cost Object (PropertiesReader/Insert Object From Properties fill in
...                 file order). All 4 dropdown values use REAL literal option text, not
...                 __FIRST__ (Batch 2 VAT Code gotcha - __FIRST__ never resolves to literal
...                 text for TC02's round-trip Verify Object Insert Exists comparison): Object
...                 Type="Cost Center", Cost Object="AA" (cascade-populated), Company="Acme
...                 Chemicals", Distribution Object Type="Country". A live insert+delete
...                 round-trip with a throwaway RECON_CMAP_TEST code proved this fill order/
...                 value set actually Saves and self-cleans (DB-verified both ways). Grid shows
...                 Code, Name, Start Date (same 3 columns as Bank/Account/Country).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${COST_OBJECT_MAPPING_SCREEN}          Cost Object Mapping
${COST_OBJECT_MAPPING_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/cost_object_mapping_insert.properties
${COST_OBJECT_MAPPING_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/cost_object_mapping_update.properties
${COST_OBJECT_MAPPING_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/cost_object_mapping_form_verify.properties
${COST_OBJECT_MAPPING_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/cost_object_mapping_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
${COST_OBJECT_MAPPING_TABLE}       ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - same documented shape as Bank's/Customer's own DEL_ENDDATE (the row packs TWO
# fields, Start Date C:1 / End Date C:3, with the End Date label at C:2) - confirmed unchanged
# live 2026-08-23 (objectdates plan: single row, End Date at C:3).
${COST_OBJECT_MAPPING_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Cost Object Mapping's own form-field label set (Start Date deliberately excluded - it lives
# only in objectForm/objectdates, not updateAttributes, same convention as Bank/Customer).
# Defined ONCE here so both Verify Cost Object Mapping Record Exists (TC02, against
# cost_object_mapping_insert.properties) and Verify Cost Object Mapping Record Found (TC04,
# against cost_object_mapping_form_verify.properties) share the same list.
@{COST_OBJECT_MAPPING_FORM_LABELS}    Code    Name    Description    Object Type    Cost Object
...    Company    Distribution Object Type


*** Keywords ***
Find Cost Object Mapping Row By Filter
    [Documentation]    Explicitly filter the Cost Object Mapping grid's Code column to ${code}
    ...    via the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Bank's/Customer's own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${COST_OBJECT_MAPPING_TABLE}    ${code}

Clear Cost Object Mapping Row Filter
    [Documentation]    Clear the Code column filter set by Find Cost Object Mapping Row By
    ...    Filter, via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${COST_OBJECT_MAPPING_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Cost Object Mapping's OWN credentials
    ...    (${COST_OBJECT_MAPPING_EC_USER}/${COST_OBJECT_MAPPING_EC_PASS} from credentials.py)
    ...    on the current page - works whether this is the very first login (page freshly
    ...    loaded on the login form via the shared T1 Open EC Application) or a re-login after
    ...    Logout From EC Application. Screen-specific wrapper (matches Bank's/Customer's own
    ...    pattern) that supplies Cost Object Mapping's own credential defaults to the shared T1
    ...    Login To EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${COST_OBJECT_MAPPING_EC_USER}    ${COST_OBJECT_MAPPING_EC_PASS}

Open Cost Object Mapping Screen
    [Documentation]    Navigate to the Cost Object Mapping screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${COST_OBJECT_MAPPING_SCREEN}

Insert Cost Object Mapping Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties, so
    ...    cost_object_mapping_iud.robot's test case body reads as a plain business step with
    ...    ZERO arguments - the underlying mechanics (properties-file-driven insert) are
    ...    UNCHANGED. Also owns the integrity check that the inserted Code matches the suite's
    ...    ${TEST_CODE} - this keyword fails on its own if
    ...    testdata/cost_object_mapping_insert.properties' Code ever drifts out of sync with the
    ...    suite variable. The TC02 evidence screenshot is captured BEFORE Save is clicked,
    ...    passed through to Insert Object From Properties, which fills every field first (in
    ...    file order - Start Date/Object Type BEFORE Cost Object, required for the cascade).
    [Arguments]    ${properties_path}=${COST_OBJECT_MAPPING_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Cost Object Mapping Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check here): row exists in the grid, then every field's LIVE
    ...    SCREEN value (via Get OV Field Value By Label) is compared to
    ...    testdata/cost_object_mapping_insert.properties (the file used to insert, not the
    ...    post-update cost_object_mapping_form_verify.properties) - Code, Name, Description,
    ...    Object Type, Cost Object, Company, Distribution Object Type
    ...    (${COST_OBJECT_MAPPING_FORM_LABELS}). Start Date is NOT verified here - it only
    ...    exists as a grid column / objectdates field, not an updateAttributes field.
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Insert Exists. Filters via Find Cost Object Mapping Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Cost Object Mapping Row By Filter    ${code}
    Verify Object Insert Exists    ${COST_OBJECT_MAPPING_TABLE}    ${code}    Cost Object Mapping
    ...    ${COST_OBJECT_MAPPING_INSERT_PROPERTIES}    @{COST_OBJECT_MAPPING_FORM_LABELS}
    Clear Cost Object Mapping Row Filter

Update Cost Object Mapping Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns
    ...    the applied {label: value} dict so the caller can DB-verify against exactly what was
    ...    set. The TC03 evidence screenshot is captured BEFORE Save is clicked. Filters via
    ...    Find Cost Object Mapping Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${COST_OBJECT_MAPPING_UPDATE_PROPERTIES}
    Find Cost Object Mapping Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${COST_OBJECT_MAPPING_TABLE}    ${code}
    ...    ${properties_path}    ${TEST NAME}_action
    Clear Cost Object Mapping Row Filter
    RETURN    ${data}

Verify Cost Object Mapping Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check): selects the row (loading updateAttributes), then compares
    ...    Name/Description's LIVE SCREEN value (via Get OV Field Value By Label) to
    ...    testdata/cost_object_mapping_update.properties - only those two labels, since that's
    ...    the only fields that file has. Delegates the full sequence (select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Form Record. Filters via Find Cost Object
    ...    Mapping Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Cost Object Mapping Row By Filter    ${code}
    Verify Object Form Record    ${COST_OBJECT_MAPPING_TABLE}    ${code}    Cost Object Mapping
    ...    ${COST_OBJECT_MAPPING_UPDATE_PROPERTIES}    Name    Description
    Clear Cost Object Mapping Row Filter

Find Cost Object Mapping Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates
    ...    the full select+capture sequence. Calls Find Cost Object Mapping Row By Filter first.
    ...    Deliberately does NOT clear the filter afterward - Verify Cost Object Mapping Record
    ...    Found (called right after, same TC) needs the grid still filtered to ${code} for its
    ...    own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Cost Object Mapping Row By Filter    ${code}
    Find Object Record    ${COST_OBJECT_MAPPING_TABLE}    ${code}    Cost Object Mapping

Verify Cost Object Mapping Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid
    ...    AND the full form record match the expected data - the SAME two existing live-DOM
    ...    round-trip keywords, just called under one name. Also captures the TC04 evidence
    ...    screenshot. Delegates the full sequence (grid-compare, form-compare, screenshot) to
    ...    the shared T2 Verify Object Found. Caller must already have selected the row (TC04
    ...    does, via Find Cost Object Mapping Record before this) AND left the Code filter
    ...    active from that same call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${COST_OBJECT_MAPPING_TABLE}    ${code}
    ...    ${COST_OBJECT_MAPPING_GRID_VERIFY_PROPERTIES}    ${COST_OBJECT_MAPPING_FORM_VERIFY_PROPERTIES}
    ...    @{COST_OBJECT_MAPPING_FORM_LABELS}
    Clear Cost Object Mapping Row Filter

Delete Cost Object Mapping Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the cost object mapping, set End Date = Start Date (true delete), Save.
    ...    Captures the TC05 evidence screenshot right after the End Date is filled but BEFORE
    ...    Save is clicked. Filters via Find Cost Object Mapping Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Cost Object Mapping Row By Filter    ${code}
    Delete Object Via End Date    ${COST_OBJECT_MAPPING_TABLE}    ${COST_OBJECT_MAPPING_DEL_ENDDATE}
    ...    ${code}    ${date}    ${TEST NAME}_action
    Clear Cost Object Mapping Row Filter

Verify Cost Object Mapping Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database - the SAME two existing DB-ground-truth
    ...    keywords, just called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${COST_OBJECT_MAPPING_TABLE}    OV_FIN_COST_OBJECT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Cost Object Mapping Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the
    ...    shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${COST_OBJECT_MAPPING_TABLE}    ${code}
