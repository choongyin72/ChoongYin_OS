# Screen: Deferment Group

- **Type:** OV (EC Object Configuration, date-effective) — plain **Bank-pattern** (`manage_object_nav`),
  no navigator, no mandatory dropdowns. Rebuilt to the label-driven, properties-file-driven,
  T2-consolidated, explicit-grid-filter shape shared by Bank/State/Berth/Bank Account in PR #479
  (Batch 8, merged 2026-08-23) — supersedes the earlier 2026-07-26 pre-Bank-pattern build.
- **BF_CODE:** CO.0149 — **Treeview:** Configuration > Assets > Facility_Objects > Deferment Group _(DB treeview JSON)_
- **DB view:** `OV_DEFERMENT_GROUP` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 — EC 14.2.4 — local sandbox. Historical PASS: PR #479 (2026-08-23)
  cited live RF **5/5** PASS + full-tree dryrun 774/774. **Current live status: BLOCKED** — see
  Quirks below; re-confirmed 2026-08-28 during a documentation backfill pass (no automation changes).

## Selectors `[from screens/Deferment_Group/deferment_group_page.resource Variables section, 2026-08-28]`
| Purpose | Selector / constant |
|---|---|
| Open | menu search `Deferment Group` -> `label.tv-link` "Deferment Group" (label, not `span.tv-link`) |
| Grid id | `${DEFERMENT_GROUP_TABLE}` = `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`, needs GO to load) |
| Find/Clear grid filter | `Find Deferment Group Row By Filter` / `Clear Deferment Group Row Filter` -> shared T2 `Find/Clear Object Row By Filter` on `${DEFERMENT_GROUP_TABLE}` (Code column) |
| Insert | `Insert Deferment Group Record And Save` -> T2 `Insert Object From Properties And Verify Code`, properties file `testdata/deferment_group_insert.properties`, `code_label=Deferment Group Code` |
| Update | `Update Deferment Group Record And Save` -> T2 `Update Object From Properties`, `testdata/deferment_group_update.properties` |
| Delete | `Delete Deferment Group Record And Save` -> T2 `Delete Object Via End Date`, End Date field id `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` = Start Date |
| Find/verify | `Find Deferment Group Record` / `Verify Deferment Group Record Found` -> T2 `Find Object Record` / `Verify Object Found` |

### New Object form (`objectForm`) — labels (T3 resolves BY LABEL)
**Deferment Group Code*** — **Deferment Group Name*** — **Start Date*** (date) — End Date — optional dropdowns. (`*` mandatory)
`@{DEFERMENT_GROUP_FORM_LABELS}` = `Deferment Group Code`, `Deferment Group Name` (used by both
TC02's Verify Insert Exists and TC04's Verify Found — Start Date deliberately excluded, Insert-only).

### Update (`updateAttributes`) / Delete (`objectdates`)
`Deferment Group Code` (ro) — **`Deferment Group Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_DEFERMENT_GROUP`.

## Automation (code in ec-automation)
- **Playwright:** `py/deferment_group_iud.py` — pre-existing from the 2026-07-26 build (7/7 at that
  time); **not rebuilt or maintained further** — the Playwright driver + `investigation/` are
  permanently waived for Bank-/Area-pattern screens (Section H, `docs/IUD-DELIVERABLE-CHECKLIST.md`)
  since the Universal Screen Engine (`py/engine.py`) is the owner-decided replacement.
- **RF:** T3 `pageobjects/Configuration/Assets/Facility_Objects/deferment_group_page.resource`
  (**label-driven, NO hardcoded ids**, properties-file-driven, T2-consolidated) + suite
  `tests/.../deferment_group_iud.robot` (TC01-05: clean-state / insert / update / find / delete,
  per-TC Login/Logout). Dedicated credentials `DEFERMENT_GROUP_EC_USER`/`DEFERMENT_GROUP_EC_PASS`
  in `resources/credentials.py`. Historical live 5/5 (PR #479, 2026-08-23).
- **Gate:** PR #479's own body — robocop clean (page object), dryrun 774/774 (full tree), grid-filter
  keyword confirmed fired (15 `Find Object Row By Filter` hits in `output.xml`), DB self-clean 0
  residual via a fresh `oracledb` connection.

## Quirks
- Plain OV; no mandatory dropdowns. Generic/shared T2 handles appear/absent/pagination with zero
  screen-specific tuning.
- **Recurring role-access blocker — check this FIRST if the live suite times out on the menu-search
  tv-link.** `TV_T_BASIS_ACCESS` for `OBJECT_ID=1087` (`/com.ec.frmw.co.screens/manage_object_nav/
  CLASS_NAME/DEFERMENT_GROUP`) has been found at `LEVEL_ID=0` ("No access") for ALL 5 roles
  (`INST.MAN`, `OP`, `RES`, `SUP`, `SYST.ADM`) on TWO separate occasions in this sandbox: originally
  (blocking the Batch 8 build until the owner granted access 2026-08-23, enabling PR #479's merge)
  and AGAIN on 2026-08-28 (found while re-running the suite for a documentation backfill — see
  `screens/Configuration/Assets/Facility_Objects/Deferment_Group/JOURNAL.md`). Query before assuming
  a code/selector regression:
  `SELECT OBJECT_ID, ROLE_ID, LEVEL_ID FROM TV_T_BASIS_ACCESS WHERE OBJECT_ID = 1087 ORDER BY ROLE_ID;`
  A role-access grant is a live-sandbox security-config change out of automation scope — needs
  explicit owner authorization, not a script fix.
