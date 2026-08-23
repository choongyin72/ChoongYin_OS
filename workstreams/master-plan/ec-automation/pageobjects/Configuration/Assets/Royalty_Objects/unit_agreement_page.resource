*** Settings ***
Documentation       T3 (screen) — Unit Agreement page object.
...                 Screen: Configuration > Assets > Royalty Objects > Unit Agreement.
...                 Manage-Object (OV) screen. Holds Unit Agreement's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common). Converted
...                 2026-08-23 (Batch 5) from the older hardcoded-field-id pattern to the
...                 newer label-driven, properties-file-driven, T2-consolidated Bank pattern -
...                 mirrors bank_page.resource exactly.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${UA_SCREEN}            Unit Agreement
${UA_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/unit_agreement_insert.properties
${UA_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/unit_agreement_update.properties
${UA_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/unit_agreement_form_verify.properties
${UA_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/unit_agreement_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal string.
${UA_TABLE}             ${OV_MANAGE_OBJECT_TABLE}
# Unit Agreement's own Code label is screen-prefixed ("Unit Agreement Code"), NOT the generic
# "Code" Bank/Object List use - confirmed live 2026-08-23 via objectForm/updateAttributes ECCell
# label scan (same non-universal-label gotcha State already proved 2026-08-22).
${UA_CODE_LABEL}        Unit Agreement Code
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven — same documented precedent as Bank (py/ec_object_iud.py END_DATE_ID): this row
# packs TWO fields (Start Date C:1, End Date C:3) with the End Date label at C:2, a shape the
# one-field-per-row label scan cannot safely resolve. This exact id was already proven live by
# this screen's own prior hand-written driver/suite (screens/.../Unit_Agreement/evidence/
# unit_agreement_tc04_deleted.png) before this Bank-pattern conversion.
${UA_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Unit Agreement's own form-field label set (Start Date/End Date deliberately excluded - they
# live only in objectForm, not updateAttributes; confirmed live 2026-08-23: updateAttributes
# ECCell scan returned exactly 3 labels - Unit Agreement Code, Unit Agreement Name, Comments).
# Defined ONCE here so both Verify Unit Agreement Record Exists (TC02, against
# unit_agreement_insert.properties) and Verify Unit Agreement Record Found (TC04, against
# unit_agreement_form_verify.properties) share the same list.
@{UA_FORM_LABELS}    Unit Agreement Code    Unit Agreement Name    Comments


*** Keywords ***
Find Unit Agreement Row By Filter
    [Documentation]    Explicitly filter the Unit Agreement grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank/Account/State/Country's own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${UA_TABLE}    ${code}

Clear Unit Agreement Row Filter
    [Documentation]    Clear the Code column filter set by Find Unit Agreement Row By Filter,
    ...    restoring the grid's normal unfiltered view. Via the shared T2 Clear Object Row Filter.
    Clear Object Row Filter    ${UA_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Unit Agreement's OWN credentials
    ...    (${UNIT_AGREEMENT_EC_USER}/${UNIT_AGREEMENT_EC_PASS} from credentials.py) on the
    ...    current page - works whether this is the very first login (page freshly loaded on
    ...    the login form via the shared T1 Open EC Application) or a re-login after Logout
    ...    From EC Application. Screen-specific wrapper (unit_agreement_iud.robot's test cases
    ...    call this with ZERO arguments) that supplies Unit Agreement's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${UNIT_AGREEMENT_EC_USER}    ${UNIT_AGREEMENT_EC_PASS}

Open Unit Agreement Screen
    [Documentation]    Navigate to the Unit Agreement screen. Assumes the caller already logged
    ...    in this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${UA_SCREEN}

Insert Unit Agreement Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And
    ...    Verify Code, purely so unit_agreement_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments - the underlying mechanics (properties-file-driven
    ...    insert) are UNCHANGED. Also owns the integrity check that the inserted Code matches
    ...    the suite's ${TEST_CODE}. The TC02 evidence screenshot is captured BEFORE Save is
    ...    clicked. ${code_label} is Unit Agreement's own real label, not the generic "Code".
    [Arguments]    ${properties_path}=${UA_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=${UA_CODE_LABEL}
    RETURN    ${code}

Verify Unit Agreement Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification: row
    ...    exists in the grid, then every field's LIVE SCREEN value (via Get OV Field Value By
    ...    Label) is compared to testdata/unit_agreement_insert.properties (Unit Agreement Code,
    ...    Unit Agreement Name, Comments - Start Date is NOT verified here, it only exists as a
    ...    grid column/objectForm field, not an updateAttributes field). Delegates the full
    ...    sequence (row-check, select, form-compare, screenshot) to the shared T2 Verify Object
    ...    Insert Exists. Filters via Find Unit Agreement Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Unit Agreement Row By Filter    ${code}
    Verify Object Insert Exists    ${UA_TABLE}    ${code}    Unit Agreement    ${UA_INSERT_PROPERTIES}
    ...    @{UA_FORM_LABELS}    code_label=${UA_CODE_LABEL}
    Clear Unit Agreement Row Filter

Update Unit Agreement Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns
    ...    the applied {label: value} dict so the caller can DB-verify against exactly what was
    ...    set. The TC03 evidence screenshot is captured BEFORE Save is clicked. Filters via
    ...    Find Unit Agreement Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${UA_UPDATE_PROPERTIES}
    Find Unit Agreement Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${UA_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=${UA_CODE_LABEL}
    Clear Unit Agreement Row Filter
    RETURN    ${data}

Verify Unit Agreement Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row (loading updateAttributes), then compares Unit Agreement Name/
    ...    Comments' LIVE SCREEN value to testdata/unit_agreement_update.properties. Delegates
    ...    the full sequence to the shared T2 Verify Object Form Record. Filters via Find Unit
    ...    Agreement Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Unit Agreement Row By Filter    ${code}
    Verify Object Form Record    ${UA_TABLE}    ${code}    Unit Agreement    ${UA_UPDATE_PROPERTIES}
    ...    Unit Agreement Name    Comments    code_label=${UA_CODE_LABEL}
    Clear Unit Agreement Row Filter

Find Unit Agreement Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates
    ...    the full select+capture sequence. Calls Find Unit Agreement Row By Filter first.
    ...    Deliberately does NOT clear the filter afterward - Verify Unit Agreement Record Found
    ...    (called right after, same TC) needs the grid still filtered to ${code} for its own
    ...    grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Unit Agreement Row By Filter    ${code}
    Find Object Record    ${UA_TABLE}    ${code}    Unit Agreement    code_label=${UA_CODE_LABEL}

Verify Unit Agreement Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Delegates the full sequence (grid-
    ...    compare, form-compare, screenshot) to the shared T2 Verify Object Found. Caller must
    ...    already have selected the row (TC04 does, via Find Unit Agreement Record before this)
    ...    AND left the Code filter active from that same call - clears the filter itself once
    ...    both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${UA_TABLE}    ${code}    ${UA_GRID_VERIFY_PROPERTIES}
    ...    ${UA_FORM_VERIFY_PROPERTIES}    @{UA_FORM_LABELS}
    Clear Unit Agreement Row Filter

Delete Unit Agreement Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the unit agreement, set End Date = Start Date (true delete), Save. Captures the
    ...    TC05 evidence screenshot right after the End Date is filled but BEFORE Save is
    ...    clicked. Filters via Find Unit Agreement Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Unit Agreement Row By Filter    ${code}
    Delete Object Via End Date    ${UA_TABLE}    ${UA_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Unit Agreement Row Filter

Verify Unit Agreement Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (ov_unit_agr) - the SAME two existing DB-ground-
    ...    truth keywords, just called under one name.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${UA_TABLE}    ov_unit_agr    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Unit Agreement Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the
    ...    shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${UA_TABLE}    ${code}
