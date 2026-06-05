# Browser Library (Playwright) — Quick Reference for EC

## Top-20 Most-Used Keywords

| Keyword | Arguments | Return | EC Use Case |
|---|---|---|---|
| `New Browser` | `browser=chromium`, `headless=False`, `args=[]` | browser ID | Launch browser in Suite Setup |
| `New Context` | `ignoreHTTPSErrors=True`, `viewport={}` | context ID | Create EC session |
| `New Page` | `url` | page ID | Open EC URL |
| `Go To` | `url` | — | Navigate to EC screen URL |
| `Wait For Load State` | `state=networkidle`, `timeout=30s` | — | After every PrimeFaces AJAX action |
| `Wait For Elements State` | `selector`, `state=visible`, `timeout=30s` | — | Before interacting with elements |
| `Click` | `selector` | — | Click button, link, menu item |
| `Fill Text` | `selector`, `text` | — | Fill most input fields (clears first) |
| `Type Text` | `selector`, `text`, `delay=50ms` | — | **EC search fields** — triggers AJAX keyup |
| `Clear Text` | `selector` | — | Clear input before typing |
| `Get Text` | `selector` | text | Read cell or label value |
| `Get Property` | `selector`, `property` | value | Read `value`, `class`, `data-rk` |
| `Get Element` | `selector` | element | Get element handle |
| `Get Element Count` | `selector` | count | Count matching elements |
| `Select Options By` | `selector`, `by=label`, `value` | — | PrimeFaces dropdown |
| `Take Screenshot` | `filename=name.png` | path | Test evidence screenshots |
| `Close Browser` | — | — | Suite Teardown |
| `Get Url` | — | url | Verify current URL |
| `Execute JavaScript` | `script` | result | Run JS on page |
| `Press Keys` | `selector`, `key` | — | Enter, Tab, Escape |

## Wait Strategies

| Situation | Keyword to use |
|---|---|
| After clicking Go/Save/Search | `Wait For Load State    networkidle    timeout=30s` |
| Before clicking any element | `Wait For Elements State    ${SEL}    visible    ${WAIT_TIMEOUT}` |
| After page navigation | `Wait For Load State    networkidle    timeout=60s` |
| Wait for element to disappear | `Wait For Elements State    ${SEL}    hidden    ${WAIT_TIMEOUT}` |
| Wait for spinner to clear | `Wait For Elements State    css=.ui-blockui    hidden    30s` |

## EC-Specific Locator Patterns

| Element | Locator | Note |
|---|---|---|
| Keycloak username | `id=username` | Stable |
| Keycloak submit | `id=kc-login` | Stable |
| Sidebar search | `xpath=//input[@id='menu:searchForm:searchTxt']` | PrimeFaces |
| Treeview link | `xpath=//label[contains(@class,'tv-link') and normalize-space(.)='${NAME}']` | Dynamic text |
| Last page btn | `css=span.ui-icon-seek-end` | PrimeFaces pagination |
| Data row | `tr[data-rk]` | EC table rows |
| Screen toggle | `id=screenToolbar:form:minmaxMenu` | Existing in ec_browser.robot |

## State Values for `Wait For Elements State`
`visible` `hidden` `enabled` `disabled` `editable` `readonly` `checked` `unchecked` `stable` `attached` `detached`
