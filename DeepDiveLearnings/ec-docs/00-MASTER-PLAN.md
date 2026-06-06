# EC Documentation Deep Dive — Master Plan & Index
**Source:** local `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/` (**EC 14.2.4**)
**Scope:** index-then-prioritize · **KB home:** `DeepDiveLearnings/ec-docs/` · **Started:** 2026-06-06

## Tree (from index mapper)
- **technical-documentation — 230 pages** ← the deep-dive target
- release-notes — 176 pages (version histories; **skipped**, current = 14.2.4)
- installation 9 · upgrade 1 · configuration 1 · root 6

## Module breakdown (technical-documentation)
`frmw` 167 (general-config 50, bpm 24, ec-extensions 17, event 15, containers 10, ecis 10, iam 9,
graphql 8, reporting-and-analytics 7, edac 4, databasedevelopment 4, tools 3, appdev 2, rest-api/expression/blobstorage/flyway 1 each)
· `prod` 22 · `revn` 13 · `transport` 12 · `product_concept` 6 · `sale` 5 · `user_guide` 3 · top 2

## Session split (11 sessions, priority order)
Each session → one KB summary doc `DOC-NN-<name>.md` (key concepts, config, gotchas, Woodside relevance).

| # | Session | Modules | ~Pages | Priority | Status |
|---|---|---|---|---|---|
| **DOC-01** | **Foundations / Core Concepts** | product_concept + user_guide + overview | 11 | 🔴 read first | ✅ `DOC-01-foundations.md` |
| **DOC-02** | **General Configuration A** | frmw/general-config (1st half) | 25 | 🔴 core | ✅ `DOC-02-general-config-A.md` |
| **DOC-03** | **General Configuration B** | frmw/general-config (2nd half) | 25 | 🔴 core | ✅ `DOC-03-general-config-B.md` |
| **DOC-04** | **Production** | prod | 22 | 🔴 Woodside | ✅ `DOC-04-production.md` |
| **DOC-05** | **Revenue + Sales** | revn + sale | 18 | 🟠 Woodside | ✅ `DOC-05-revenue-sales.md` |
| **DOC-06** | **Transport** | transport | 12 | 🟠 Woodside | ✅ `DOC-06-transport.md` |
| **DOC-07** | **ECIS + Events** | frmw/ecis + frmw/event | 25 | 🔴 integration | ✅ `DOC-07-ecis-events.md` |
| **DOC-08** | **BPM (workflows)** | frmw/bpm | 24 | 🟠 | ✅ `DOC-08-bpm.md` |
| **DOC-09** | **EC Extensions / Dev** | ec-extensions + appdev + rest-api + expression | 21 | 🟡 | ✅ `DOC-09-extensions-dev.md` |
| **DOC-10** | **GraphQL + Reporting + eDAC** | graphql + reporting-and-analytics + edac | 19 | 🟡 | ☐ |
| **DOC-11** | **IAM + DB Dev + Containers** | iam + databasedevelopment + containers + flyway/blob/tools | 28 | 🟡 | ☐ |

**Total: 230 pages across 11 sessions.**

## Method (per session)
1. Fetch the module's pages (read-only, `ec_doc_reader.py`), extract content text.
2. Read + synthesize into `DOC-NN-<name>.md`: what it is, key config/element knowledge, gotchas, Woodside relevance, cross-links.
3. Commit. Update this index's Status. Drop a progress note.

## Cross-reference
- Prior topic-based deep dives (Sessions A–I, ectestautomation) used the **14.2.5 hub** docs — note deltas vs this local **14.2.4**.
- Existing root `ec_doc_p01..p10.txt` + `ec_doc_calc_*.txt` overlap several frmw/general-config + product_concept topics — reconcile, don't duplicate.

## Progress log
| Date | Session | Result |
|---|---|---|
| 2026-06-06 | planning | Tree mapped (230 tech pages), split into 11 sessions |
| 2026-06-06 | DOC-01 | ✅ Foundations: 5 business areas, screen anatomy, cell colours, record status P/V/A, classes (Object/Data/Interface/Table), Group Model, Calc Framework, Users/Roles/Access, Reporting |
| 2026-06-06 | DOC-02 | ✅ Class model & View Generator (explains OV_BANK/OV_EQPM = generated views + INSTEAD OF triggers); required versioned attrs (why End=Start deletes); owner-context overrides; group model config; ENFORCE_DATE_CHECK; general relations; CODE_REF popups; smart journaling |
| 2026-06-06 | DOC-03 | ✅ System config + how-tos: Oracle users (ECKERNEL/ENERGYX/REPORTING/TRANSFER), Check Rules (CTRL_CHECK_LOG, WHERE formula), DAYTIME/Production Day/time zones, calc library, business-action SQL, date macros, blocked-schedule recovery, dashboards/title-bar/column-sets/language, Messaging (MHM), navigator defaults |
| 2026-06-06 | DOC-04 | ✅ Production (Woodside core): status processes P→V→A, Deferment PD.0020, Hydrocarbon Accounting/Allocation (networks, reconciliation, PWEL/IWEL/STRM/PERF alloc tables, ghost data), Allocation BPM (work-by-exception), Stream Node Diagram, well testing PT.*, system attributes, API tank GOV, operation mode |
| 2026-06-06 | DOC-05 | ✅ Sales (GS/SD/PR/SA/TR/GP/OS, Contract Concept, Sales Allocation, Price Determination) + Revenue (doc lifecycle OPEN→BOOKED, Sales→Revenue IFAC_SALES_QTY, Stream Items/Quantity module, CSDV validation zones, Financial Item, Calendar, Visual Tracing, PDG/CDG, Inventory) |
| 2026-06-06 | DOC-06 | ✅ Transport: CA/CP/TO/LA/OD/GD/FC areas, Cargo Status T→R→C→A→D (drives record status V/A), EC Contract Concept (shared w/ Sales), Revenue interface (LOAD/UNLOAD), demurrage layout, Gantt transformers, contract end-dating (CO.2086), Berth Slot Calendar, new cargo data model (commercial vs physical) |

| 2026-06-06 | DOC-07 | Events (pub-sub Camel/ActiveMQ, DomainObjectChanged on IUD, subscriptions CO.0130/CO.1081, WebHooks/AWS-SNS/Firebase, CTRL_EVENT_TYPE/HISTORY) + ECIS (SCADA/Tag + File capture, source/target+queue, ECIS Agent, Advanced File Import, adapters OPC/Tag/Row, DEFAULT_RECORD_STATUS, Remote Endpoint secret storage) |
| 2026-06-06 | DOC-08 | BPM: jBPM engine + BPM Console, jbpmengine user, Project Management (JBPM.ADMIN, Maven), Process Template (EC alias, schedulable), Process Overview + viewer-tag node colors, Process Action handlers (chained), User Tasks->To-do List, process inbound/outbound events (DatasetUpdated) |
| 2026-06-06 | DOC-09 | Extensions/Dev: REST API (domain model IUD, OpenAPI 3.0.3, frmw-core-api SDK), EC Extensions (WAR, Extensions Manager lifecycle, Maven archetype, 4 install options), strict DB-change rules (prefix by ext-id, OWNER_CNTX>=1000, APP_SPACE_CNTX, IGNORE_IND, DB_MAPPING_TYPE=EXTENSION, Flyway), dev env + EC Hub Nexus, DomainEntityMgr, expression scripting |
