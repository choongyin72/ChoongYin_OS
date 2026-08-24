# Screen: Document Template

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** CD.0013 - **Treeview:** Configuration > Assets > Revenue_Document_Objects > Document Template _(DB treeview JSON)_
- **DB view:** `OV_DOC_TEMPLATE` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-24 - EC 14.2.4 - local sandbox - Bank-pattern conversion: RF 5/5 live, Playwright 7/7 (unchanged, 2026-07-26)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Document Template` -> `label.tv-link` "Document Template" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Code*** - **Name*** - **Start Date*** (date) - End Date - optional dropdowns. (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Code` (ro) - **`Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_DOC_TEMPLATE`.

## Automation (code in ec-automation)
- **Playwright:** `py/document_template_iud.py` -> 7/7 (update Name). Unchanged by the 2026-08-24 conversion.
- **RF:** T3 `pageobjects/Configuration/Assets/Revenue_Document_Objects/document_template_page.resource` upgraded to the Bank pattern (2026-08-24) — properties-file-driven `Insert/Update Object From Properties`, explicit `Find/Clear Document Template Row By Filter` wired into Update/Find/Verify-Found/Delete, dedicated `DOCUMENT_TEMPLATE_EC_USER/PASS`, fixed test code `AUTOTEST_DOCUMENT_TEMPLATE`. Suite `tests/.../document_template_iud.robot` -> 5 TCs (added TC04 Find), live 5/5.

## Quirks
- Plain OV per the static scan (no CSS-flagged mandatory dropdowns), but **Document Title is
  de-facto mandatory** — Save silently fails to persist without it, per the already-proven
  `py/document_template_iud.py` INSERT_FIELDS (trusted over the static note per the standing
  gotcha: a proven driver's field set beats a static scan).
- Delete's objectdates End Date field id is resolved BY LABEL at runtime
  (`OV Field Id By Label`), not hardcoded — no live objectdates row-shape scan was run to
  safely hardcode an id the way Bank's own documented precedent does.
- Generic engine handles appear/absent/pagination.
