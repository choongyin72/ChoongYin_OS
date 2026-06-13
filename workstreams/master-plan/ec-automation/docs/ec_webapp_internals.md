# EC Web App Internals — Automation Field Guide (2026-06-13)
Reverse-engineered operational knowledge of the EC web app (JSF/PrimeFaces) accumulated across
~50 automated screens + As-Built study. The "inside-out" reference that makes every new screen
faster. Pairs with ec_screen_registry.md (per-screen facts) — this is the cross-cutting framework.

## 1. Tech stack (what we're driving)
EC web = **JSF + PrimeFaces** on WildFly/JBoss, Keycloak auth, Oracle DB. Pages are
server-rendered with AJAX partial-submits (`PrimeFaces.ab({...})`). Implications for automation:
- Almost every interaction fires a server round-trip → **always `Wait For Load State networkidle`
  + a short settle Sleep** after clicks/edits; never assume synchronous DOM update.
- Element ids are **colon-delimited JSF client ids** (stable, not random) → locate by `id=`, not
  by fragile CSS/text where an id exists. Escape colons in CSS via `[id="..."]`.

## 2. The PrimeFaces id grammar (the master key)
`form:component:T:{row}:C{col}_{suffix}` — decode any cell from its id:
- `T` = datatable; `T_data` = tbody; `T_head` = header; `T:{n}` = row n (0-based).
- `C{col}` = column; suffix tells the widget type:
  - `_in` / `:in` = text input · `_da_input` = date/time input · `:dd` (+`_dd_input`,`_dd_button`,
    `_dd_panel`,`_dd_hinput`) = autocomplete dropdown · `:cb` = checkbox ·
    `:pin`/`:pinB` = **popup picker** (readonly field + button) · `_la` = label · `_cb_filter` =
    column filter.
- Object-form fields: `tab:tabPanel:objectForm:form:G:0:R:{row}:C:1:{suffix}` (insert);
  `...updateAttributes:form:...` (update); `...objectdates:form:...:C:3:da_input` (End Date = delete).
- Row labels `...:R:{r}:C:0:la` give the field NAME → recon labels first (Code/Name aren't always R0/R1).

## 3. Screen TYPES & their list-grid ids (from the registry, generalized)
- **OV manage-object**: `manage_object_nav_nav:form:T_data` (framework URL) or
  `manageObject:form:T_data` (custom/groupmodel URL). Navigator + GO (`button:form:B`). Delete =
  End Date = Start Date.
- **OV-GM (groupmodel)**: same grid id but **grid empty until navigator dd + GO**; inserted object
  must carry the Op-parent (PU/Area/BU) matching the navigator, else invisible. ⚠️ if the
  groupmodel isn't enabled, inserts persist to DB but never list (PSU/Sub Field/Pipeline).
- **TV table-class**: `table:form:T_data` (or `<grid>:form:T_data`), no navigator, PHYSICAL delete,
  cell-edit + Tab commit. Paginated; find rows across pages.
- **PC parent-child**: navigator picks parent → items in `tab:tabPanel:<x>_table:form:T_data`;
  count-delta DB oracle.
- **RUN-verify**: date/nav + GO, a Run button, output to a log/result table (verify at DB).
- **N1 daily-status grid** (Pluto transactional, not yet automated): date-navigator + GO + editable
  measured-value grid per object/day → DB *_DAY_STATUS. (Next pattern to build.)

## 4. The gestures that actually work (hard-won)
- **Dropdown (dd)**: click `{dd}_button` → wait `{dd}_panel tr[data-item-label]` → click the
  `tr[data-item-label="<exact label>"]`. Typing into dd is unreliable. Labels are DISPLAY text
  (normalize-space tolerates stored leading/double spaces). Verify `{dd}_input`.value committed.
- **Text/number cell**: fill + dispatch `change`+`blur` events (EC.bf onchange) OR type+Tab —
  plain `fill()` alone does NOT stage the value for Save.
- **Date**: fill `_da_input` + Tab (+ change/blur).
- **Popup picker (pin/pinB)**: **JS-click** the `{prefix}B` (actionability clicks race the dialog
  mask) → wait `#popupIFrame` visible → match the row inside the iframe by input VALUE PROPERTY
  **or** innerText (never XPath `@value` — EC's dynamic inputs leave the attribute empty) → click
  → popup closes + fills the `pin`. Popup list is **navigator-filtered** (set BU first).
- **Save**: toolbar `a[title="Save [Ctrl+s]"]` only when NOT `ui-state-disabled`. Save is async →
  **poll the DB to confirm persistence**, don't trust the click (the spinner lesson).
- **Hover menus** (toolbar Insert): after hovering, a body click (not Escape) dismisses cleanly;
  Insert AND Delete submenus often share the same item text → disambiguate by `contains(@onclick,"insert")`.
- **Navigator GO is mandatory** after setting nav data; some screens click GO twice; confirm the
  VISIBLE GO (`button:form:B` / `navButton:form:B`), not a hidden default-submit.
- **Expand screen**: `screenToolbar:form:minmaxMenu` toggles treeview hide (full-page); restore
  before the next treeview search.

## 5. Two config layers (why a screen looks the way it does)
- **OOTB vs custom**: a screen whose attributes are all "Product" context = out-of-the-box; **ZWP**
  context = Woodside-Pluto custom (extension). Only required attrs are configured per As-Built 02.
- **Object Start Date = version filter (universal!)**: reference dropdowns only offer objects
  effective at the form's Start Date → use the seed epoch (2003-01-01 here) on ref-dd screens.
- **Date-effective everything**: objects/calcs/configs are versioned by valid-from-date
  (ZWP_*_V0 = version 0). Delete = End Date = Start Date (zero-length window).
- **Record status P→V→A** + month-lock gate writes (status processes CO.0076 / HA.0001/0004).
- **Pluto units = SI**: °C / MPa / Sm³ / GJ/Sm³ (test data must match).

## 6. Screen URL families (recon shortcut)
Framework screens: `/com.ec.frmw.co.screens/...` (e.g. tt_validation_overview). Custom/module:
`/com.ec.<module>.co.screens/...` + popups `/com.ec.tran.co.screens/object_popup?CLASS_NAME=`.
The EC_USER_OBJECT URL + the list/grid id + key cell ids = the minimum recon to automate a screen.

## 7. Verify at DB, always
The UI can lie (optimistic state, pagination, silent reject, grain). Every pass/done claim =
DbVerify against the OV_*/base table. Dryrun proves structure; live + DB proves behaviour.
(Direct DB insert bypasses screen + CSDV validation — matches how my probes operate below the UI.)
