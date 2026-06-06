# DOC-01 — Foundations / Core Concepts
**Source:** EC 14.2.4 local `/doc/.../technical-documentation/` — product_concept + user_guide + overview (11 pages)
**Read:** 2026-06-06

---

## 1. What EC is — five business areas
EC does **accounting of hydrocarbon quantities, qualities, and ownership from wells → transport → first sale.** Five modules:

| Module | Covers |
|---|---|
| **Production** | Data acquisition (DCS/historians), validation, well tests, well-rate estimation, **allocation** (phase/sales product back to wells/completions/zones), inventory, emissions, **deferment/downtime**, forecasts, ownership allocation (royalty/PSA), KPIs, JV + regulatory reporting |
| **Chemistry** | Chemical inventory, lab integration, injection-network optimization |
| **Transport** | Cargo scheduling (crude/LNG), lifting programmes, tanker/lift accounting, demurrage, nominations (pathed/non-pathed), pipeline flow & capacity/curtailment, gas storage/balancing, title transfer |
| **Sales** | Gas sales contracts, nominations, availability vs obligations, take-or-pay (carry-forward/make-up/shortfall), multi-currency pricing |
| **Revenue** | Valuation of sales/purchases + tariffs, invoicing, accruals, prior-period adjustments, ERP/financial integration, inventory valuation, UOP depreciation, forecasting/budgeting. **SOX404** traceability. "Reservoir to revenue." |

*(Woodside Pluto = Production + Allocation + Revenue + Sales + Transport on this platform.)*

## 2. The configuration philosophy (EC's core selling point)
**Configurable without programming or downtime.** Changes take effect immediately, while in use. Configurable: Tree View menu, Navigator, Object Access, Units, Audit tracking, Check Rules, Record Status processes, Screen config, columns, calculated numbers, language, by-role/by-status.
- **Units:** Display Unit (shown) vs Storage Unit (DB). ⚠ Changing storage unit does **not** recalc stored data.
- **Object Access:** hides specific assets everywhere (screens + dropdowns), by role.
- **New objects** added via config screens are immediately available, no programming.

## 3. The EC screen anatomy (7 panes) — confirms my IUD work
Title Bar · Tool Bar · Tree View · Navigator Pane · Data Window · Status Area · browser status line.
- **Tool Bar icons:** Save, Retrieve/Refresh, **New (Insert)**, **Delete**, Maximize/Minimize, Add to Favorites, Screen settings, Available Tasks (refreshes every 5 min). Greyed = deactivated (activates as you add data) — *matches the disabled Save/Delete I saw on Bank/Equipment.*
- **Tree View:** top = config/maintenance; bottom = business functions grouped (Allocation, Terminal Op…). Has search + drag-to-Favorites — *this is the sidebar search I drive in automation.*
- **Navigator:** Standard (date + asset dropdowns + Go) vs Filter. Most screens use a **dynamic Group Model Navigator** populated from Group Model config — *exactly the cascading navigator I cracked on Equipment.*
- **🔑 Cell colour semantics (confirms my automation):** **white = editable, yellow = mandatory, gray = read-only.** (This is precisely the "Required fields are empty" + yellow Area/FacilityClass I hit on Equipment, and the gray read-only Equipment Type.)

## 4. Record status lifecycle 🔑
**Provisional (default) → Verified (auto-loaded via data capture/interfaces) → Approved (job run, highest security).** Status Area tabs: Record Status, Revision Info, Approval Status (four-eyes), Hints & Tips, Validation, Trending, Attachments.
- Audit journal auto-kept for VERIFIED+ (configurable down to PROVISIONAL+).
- *(Ties to the `RECORD_STATUS='P'` I saw in OV_BANK/OV_EQPM, and `REV_NO` revisions.)*

## 5. Classes & Objects 🔑 (the abstraction behind everything)
DB has an **abstraction view layer** separating business logic from table structure. Four class types:
| Class type | What |
|---|---|
| **Object class** | static physical thing — Facility, Tank, Separator, **Well**, **Bank**, **Equipment** (my IUD targets are Object classes) |
| **Data class** | measurements/events owned by an object (daily tank volumes, exported volumes) — *the "data grid" screens like Daily Equipment Status* |
| **Interface class** | abstraction over several object classes w/ common attributes (nodes in stream diagrams) |
| **Table class** | like data class, less validation/row-security; no object owner/timestamp PK |
Enables: virtual vs stored attributes, custom attributes, ringfencing/data-locking, four-eye/control-point as generic add-ons, table changes without touching business logic. Controlled at package / template / project levels.

## 6. Group Model 🔑
Hierarchical asset/class structure (parent→child) that **populates screen navigators dynamically.** One parent, many child relations. Two predefined: **Geographical** and **Operational**; others client-configurable. Config screen under Configuration → System. *(This is why the Equipment navigator was Production Unit → Area → Facility Class — a Group Model hierarchy.)*

## 7. Calculation Framework 🔑
Client-defined business logic as **process diagrams** (no compiler). Two parts: **Definition Framework** (create/maintain) + **Execution Framework** (reads from DB, executes).
- Building blocks: **attributes & variables** (point at DB values), **equations, sets, conditions** (arith/logic operators). Sets = the group of objects an equation applies to.
- Equations stored as **MathML** (XML for math); built in the **Equation Editor** (visual) in the **Maintain Calculation** screen; conform to **EC Calculation Syntax** (object/var on left, expression on right; optional condition).
- Changes available immediately, no compile. Used in Allocation/HC Accounting, Sales/Contract, Price, Cargo Scheduling.
- **Stream/Node concept:** Stream = flow (e.g. pipeline gas); Node = connection point (well, platform, terminal). Quantities on Streams, calculations on Nodes. Visualized in the configurable **Stream Node Diagram**.

## 8. Users, Roles, Groups, Access 🔑 (ties to Role Maintenance recon)
- **Users + role/group assignments** live in **Keycloak** (or EC business functions). Keycloak can federate from LDAP/AD/Entra ID.
- **Roles** = what activities + access level; must exist in **both EC and Keycloak** (Role Maintenance screen syncs them — *the Keycloak-sync button I saw in recon*).
- **Partitioning** = which objects (fields/facilities/contracts) a role can access.
- **Groups** = meaningful collections of EC Roles (efficient bulk assignment); users can be in many; highest access wins.
- **Access levels per screen:** No access (invisible) · Read · Change (Save only) · New (Save+New) · Delete (Save+New+Delete) · Edit-on-VERIFIED · Edit-on-APPROVED. *(This maps directly to the toolbar button enablement I observed.)*

## 9. Reporting concept
Framework for product + customer reports, internal + 3rd-party. Fixed report needs: **template** (which engine + params) + **definition** (content) + **report/runnable**. Five report systems:
| System | Note |
|---|---|
| **Yellowfin** | "EC Reporting and Analytics"; can also run JasperReports |
| **EC Jasper Report** | deprecated in EC13 but used; PDF/Excel/CSV |
| **EC Excel Report** | spreadsheet↔DB mapping; works with calc engine |
| **External System** | report made/stored externally, triggered + stored from EC |
| **EC Internal** | deprecated EC11; legacy Jasper 3.1 / gen_xml_report_db |
Ad-hoc: Yellowfin, **Export to Excel Express** (any EC-class DB view). Workflow: Configure → Generate (Report Administration / scheduled / BPM) → Search/View → Distribute (Messaging/email) → Publish → Verify/Approve → Batch (Report Sets).

---

## Cross-links to my work
- Confirms the **IUD automation observations**: cell colours (white/yellow/gray), record status P/V/A, toolbar enablement, Group Model navigator, Manage Object = Object class.
- `[[reference_ec_object_delete]]` — Bank/Equipment are **Object classes**; date-effective delete = End=Start.
- Calc Framework + Reporting overlap my prior JasperReports deep dive and root `ec_doc_calc_*.txt` / `ec_doc_p06_calc_framework.txt`.
- Next: **DOC-02 General Configuration A** (class config rules, class model, group model config, view generator).
