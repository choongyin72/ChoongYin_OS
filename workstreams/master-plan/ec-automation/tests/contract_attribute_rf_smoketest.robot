*** Settings ***
Documentation       LIVE VALIDATION smoke test for resources/contract_attribute.resource — proves
...                 the RF port of contract_attribute_helpers.py actually works against a real EC
...                 screen (Sale Contract Attributes, local sandbox), not just in theory. Uses
...                 SS1_Contract_A row 13 (Parent Contract) — pre-existing test data already proven
...                 non-protected + safely self-cleaning during the Python-side validation
...                 (2026-08-09). Set -> verify -> Delete -> verify blank again, so the sandbox is
...                 left exactly as found. TC04/TC05 close out the checkbox and protected-attribute
...                 code paths not covered by TC01-03 (dropdown + delete).

Resource            ../resources/common.resource
Resource            ../resources/contract_attribute.resource

Suite Setup         Set Up Contract Attribute Smoke Test
Suite Teardown      Close EC

Test Tags           smoketest    contract-attribute


*** Variables ***
${ROW_PARENT_CONTRACT}          13
${ROW_ENFORCE_TAKE_OR_PAY}      8
${TEST_VALUE}                   SS1_Contract_B
${TEST_DAYTIME}                 2026-01-01


*** Test Cases ***
TC01 Row Starts Blank
    [Documentation]    Confirm row 13 (Parent Contract) is blank before we touch it.
    [Tags]    clean-state
    ${value}=    Get Contract Attribute Row Value    ${ROW_PARENT_CONTRACT}
    Should Be Empty    ${value}

TC02 Set Never Before Set Value
    [Documentation]    Set a value on the never-before-set attribute via the RF keyword (exercises
    ...    the Insert->Attribute Version + Daytime path, not just a plain edit).
    [Tags]    insert
    ${status}=    Set Contract Attribute Value    ${ROW_PARENT_CONTRACT}    ${TEST_VALUE}    ${TEST_DAYTIME}
    Should Be Equal    ${status}    OK
    ${value}=    Get Contract Attribute Row Value    ${ROW_PARENT_CONTRACT}
    Should Be Equal    ${value}    ${TEST_VALUE}

TC03 Delete Restores Blank
    [Documentation]    Delete the version, restoring blank state (self-clean).
    [Tags]    delete    cleanup
    Delete Contract Attribute Value    ${ROW_PARENT_CONTRACT}
    ${value}=    Get Contract Attribute Row Value    ${ROW_PARENT_CONTRACT}
    Should Be Empty    ${value}

TC04 Checkbox Edit Round Trip
    [Documentation]    "Enforce Take or Pay" (row 8) already has a value (Y) on every contract
    ...    template checked on this sandbox — no naturally blank checkbox exists to exercise the
    ...    combined Insert+checkbox path, so this proves the checkbox EDIT (existing-value) path
    ...    instead: toggle to N, verify, toggle back to Y (self-clean), verify restored.
    [Tags]    checkbox
    ${before}=    Get Contract Attribute Row Value    ${ROW_ENFORCE_TAKE_OR_PAY}
    Should Be Equal    ${before}    Y
    Set Contract Attribute Value    ${ROW_ENFORCE_TAKE_OR_PAY}    N
    ${after}=    Get Contract Attribute Row Value    ${ROW_ENFORCE_TAKE_OR_PAY}
    Should Be Equal    ${after}    N
    Set Contract Attribute Value    ${ROW_ENFORCE_TAKE_OR_PAY}    Y
    ${restored}=    Get Contract Attribute Row Value    ${ROW_ENFORCE_TAKE_OR_PAY}
    Should Be Equal    ${restored}    Y

TC05 Protected Attribute Detected
    [Documentation]    Switch to Transport Contract Attributes (same JSF component, different
    ...    ACCESS_COLUMN) and confirm Set Contract Attribute Value returns PROTECTED for a known
    ...    system-protected attribute, without leaving any value behind.
    [Tags]    protected
    Navigate To Screen    Transport Contract Attributes
    Set Contract Attribute Navigator    TS1 BU    TS1 CA    TS1 Contract 1
    ${status}=    Set Contract Attribute Value    0    999    2026-01-01
    Should Be Equal    ${status}    PROTECTED
    ${value}=    Get Contract Attribute Row Value    0
    Should Be Empty    ${value}


*** Keywords ***
Set Up Contract Attribute Smoke Test
    [Documentation]    Login, open Sale Contract Attributes, navigate to SS1_Contract_A.
    Open EC Browser
    Login To EC
    Navigate To Screen    Sale Contract Attributes
    Set Contract Attribute Navigator    SS1 BU    SS1 CA    SS1_Contract_A
