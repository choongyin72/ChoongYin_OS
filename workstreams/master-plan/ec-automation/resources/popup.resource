*** Settings ***
Documentation       T1 area — EC framework object-popup picker (pin/pinB cells).
...                 Some object-form reference fields are POPUP PICKERS, not dropdowns:
...                 a readonly `…:pin` input + `…:pinB` button. pinB fires PrimeFaces AJAX
...                 then EC.popup.showPopup -> dialog `popupForm:popup` wrapping
...                 `popupIFrame` (/…/object_popup?CLASS_NAME=…) with grid
...                 `PopupList:form:T_data`. A single ROW CLICK selects the object,
...                 closes the popup and fills the pin input.
...                 GOTCHAS: (1) actionability-checked clicks on pinB time out because the
...                 dialog mask appears mid-click -> use a JS click; (2) the popup list is
...                 filtered by the screen's NAVIGATOR context (e.g. Business Unit) — set
...                 the navigator before opening the form or the list shows "No records".

Library             Browser


*** Keywords ***
Pick From EC Object Popup
    [Documentation]    Open the popup behind ${pin_prefix} (the cell id WITHOUT the B) and
    ...    select the row whose value equals ${item_label}. Verifies the pin input took
    ...    the value and the popup closed.
    [Arguments]    ${pin_prefix}    ${item_label}
    Evaluate JavaScript    ${None}    () => document.getElementById('${pin_prefix}B').click()
    Wait For Elements State    css=[id="popupIFrame"]    visible    timeout=15s
    Sleep    4s
    # locate the row by the input's live VALUE PROPERTY (the @value attribute stays empty
    # on EC's dynamically-populated grid inputs — XPath attribute matching never finds it)
    ${found}=    Evaluate JavaScript
    ...    css=[id="popupIFrame"] >>> css=[id="PopupList:form:T_data"]
    ...    (tbody) => { let hit = false; tbody.querySelectorAll('tr').forEach(tr => { const inp = tr.querySelector('td input'); const v = inp ? inp.value.trim() : ''; const t = (tr.innerText || '').trim(); if (!hit && (v === '${item_label}' || t === '${item_label}' || t.startsWith('${item_label}'))) { hit = true; tr.querySelector('td').click(); } }); return hit; }
    IF    not ${found}
        ${dump}=    Evaluate JavaScript
        ...    css=[id="popupIFrame"] >>> css=[id="PopupList:form:T_data"]
        ...    (tbody) => (tbody.innerText || '').slice(0, 200)
        Log    POPUP CONTENT :: ${dump}    console=True
    END
    Should Be True    ${found}    msg=Popup row '${item_label}' not found in PopupList
    Wait For Elements State    css=[id="popupIFrame"]    hidden    timeout=15s
    Sleep    1s
    ${val}=    Get Property    css=[id="${pin_prefix}"]    value
    Should Be Equal    ${val}    ${item_label}
    ...    msg=Popup pick did not fill the pin field (shows '${val}')
