*** Settings ***
Documentation       ONE-OFF diagnostic - reproduce EC's Unsaved-Changes dialog and dump the real
...                 DOM so the correct button locator can be read as fact, not guessed. Deletes
...                 nothing; discards the dirty New Object fill via whatever button turns out real.

Library             Browser
Resource            ../../workstreams/master-plan/ec-automation/resources/common.resource
Resource            ../../workstreams/master-plan/ec-automation/resources/manage_object.resource
Resource            ../../workstreams/master-plan/ec-automation/resources/screen.resource

Suite Teardown      Close Browser


*** Test Cases ***
Probe Dialog DOM
    Launch EC And Open Screen    Reservoir Formation
    Open New Object Form
    Fill OV Field By Label    objectForm    Reservoir Formation Code    AUTOTEST_PROBE_001
    Fill OV Field By Label    objectForm    Reservoir Formation Name    AUTOTEST Probe 001
    # Deliberately navigate away WITHOUT saving to force the Unsaved-Changes dialog.
    # Don't let a nav-assert failure stop us before we've captured the DOM evidence.
    Run Keyword And Ignore Error    Navigate To Screen    Reservoir Block
    ${present}=    Get Element Count    css=[id="confirmationForm:confirmation_modal"]:visible
    Log    modal present count = ${present}    console=True
    Take Screenshot
    ${btns}=    Evaluate JavaScript    ${None}
    ...    () => Array.from(document.querySelectorAll('[id^="confirmationForm"] button, [id^="confirmationForm"] a, [id^="confirmationForm"] span, [id^="confirmationForm"] div[role="button"]')).map(e=>({tag:e.tagName,id:e.id,text:e.textContent.trim()}))
    Log    ${btns}    console=True
    # REAL TEST: the dialog is now sitting open (unanswered). Prove the guard, wired into
    # Navigate To Screen, actually dismisses an ALREADY-open dialog on the next nav attempt.
    Navigate To Screen    Reservoir Block Formation
    ${still_present}=    Get Element Count    css=[id="confirmationForm:confirmation_modal"]:visible
    Log    modal present AFTER guarded nav = ${still_present}    console=True
    Should Be Equal As Integers    ${still_present}    0    msg=Guard failed to dismiss the dialog
