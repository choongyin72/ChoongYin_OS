*** Settings ***
Documentation       Layer-2(a) VISUAL (hover): load each screen with the full navigator, then
...                 HOVER the frozen attribute cell so EC shows the verificationText tooltip.
...                 Water "Oil in Water" (2026-05-24); Analysis "GCV" (2025-12-13).
...                 (Temporary test; ZWP_SCREEN_VAL reverted to 'N' after.)

Library             Browser
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/navigator.resource

Suite Setup         Open EC Browser And Login
Suite Teardown      Close EC
Test Tags           frozen    visual    layer2a


*** Variables ***
${SHOTS}            ${OUTPUT DIR}


*** Keywords ***
Open EC Browser And Login
    Open EC Browser
    Login To EC    ${EC_USER}    ${EC_PASS}

Hover Frozen Cell
    [Documentation]    Find the data input aligned under the column header matching ${col_regex},
    ...    mark + hover it (real mouse move -> EC tooltip), screenshot.
    [Arguments]    ${col_regex}    ${tag}
    ${js}=    Catenate    SEPARATOR=${SPACE}
    ...    () => { const re=/${col_regex}/i;
    ...    const cands=[...document.querySelectorAll('span,td,th,div,label')].filter(e=>re.test(e.textContent||'') && (e.textContent||'').trim().length<40 && e.offsetParent);
    ...    cands.sort((a,b)=>a.textContent.length-b.textContent.length); if(!cands.length) return 'NO_HEADER';
    ...    const hdr=cands[0]; const hr=hdr.getBoundingClientRect(); const cx=hr.left+hr.width/2;
    ...    const ins=[...document.querySelectorAll('input')].filter(i=>{const r=i.getBoundingClientRect(); return i.offsetParent && r.top>hr.bottom && Math.abs((r.left+r.width/2)-cx)<60;});
    ...    const t=ins[0]||hdr; t.setAttribute('data-hov','1'); t.style.outline='3px solid red'; t.scrollIntoView({block:'center'});
    ...    return (ins[0]?'CELL ':'HEADER ')+(t.id||t.tagName)+' :: '+((t.value||t.textContent||'').trim().slice(0,30)); }
    ${found}=    Evaluate JavaScript    ${None}    ${js}
    Log    HOVER[${tag}] ${found}    console=True
    Run Keyword And Continue On Failure    Hover    css=[data-hov="1"]
    Sleep    2s
    Take Screenshot    filename=${SHOTS}/${tag}_hover_tooltip.png    fullPage=True


*** Test Cases ***
Water Oil-in-Water hover tooltip (2026-05-24)
    [Tags]    water
    Navigate To Screen    Daily Water Stream Status
    Fill Text    css=[id="nav:form:G:0:R:1:C:0:da_input"]    2026-05-24
    Keyboard Key    press    Escape
    Set Navigator Filter    G:1    Pluto Scarborough
    Set Navigator Filter    G:2    Upstream
    Set Navigator Filter    G:3    Pluto A
    Click    css=[id="button:form:B"]
    Wait For Load State    networkidle    timeout=30s
    Sleep    2s
    Hover Frozen Cell    Oil in Water    water

Analysis GCV hover tooltip (2025-12-13)
    [Tags]    analysis
    Navigate To Screen    Stream Gas Component Analysis
    Fill Text    css=[id="nav:form:G:0:R:1:C:0:da_input"]    2025-12-13
    Fill Text    css=[id="nav:form:G:1:R:1:C:0:da_input"]    2025-12-13
    Keyboard Key    press    Escape
    Set Navigator Filter    G:2    Pluto Scarborough
    Set Navigator Filter    G:3    Burrup LNG Park
    Set Navigator Filter    G:4    LNG Train 1
    Click    css=[id="go_button:form:B"]
    Wait For Load State    networkidle    timeout=30s
    Sleep    2s
    Hover Frozen Cell    GCV    analysis
