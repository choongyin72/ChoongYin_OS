# EC Documentation Knowledge Base — Index & Close-out
**EC 14.2.4** (local `/doc/Energy-Components/current/`) · **11 sessions / 230 technical pages** · completed 2026-06-06
Plan + per-session progress log: [00-MASTER-PLAN.md](00-MASTER-PLAN.md)

## The 11 sessions
| Doc | Topic |
|---|---|
| [DOC-01](DOC-01-foundations.md) | **Foundations** — 5 business areas, screen/cell-colours/record-status, class types, Group Model, Calc Framework, Users/Roles, Reporting |
| [DOC-02](DOC-02-general-config-A.md) | **General Config A** — Class model & **View Generator**, owner-context overrides, group model, general relations, CODE_REF, journaling |
| [DOC-03](DOC-03-general-config-B.md) | **General Config B** — Oracle users, Check Rules, DAYTIME/time-zones, calc library, scheduling, dashboards, Messaging (MHM), navigator defaults |
| [DOC-04](DOC-04-production.md) | **Production** — status processes, Deferment PD.0020, Hydrocarbon Accounting/Allocation, Allocation BPM, well testing, Stream Node Diagram |
| [DOC-05](DOC-05-revenue-sales.md) | **Revenue + Sales** — Contract Concept, Sales Allocation, Price Determination, doc lifecycle, Stream Items, CSDV, Financial Item, Calendar |
| [DOC-06](DOC-06-transport.md) | **Transport** — cargo status, contract concept, demurrage, Gantt, contract end-dating, Berth Slot Calendar, new cargo model |
| [DOC-07](DOC-07-ecis-events.md) | **ECIS + Events** — pub-sub (Camel/ActiveMQ), DomainObjectChanged, WebHooks/SNS/Firebase, ECIS capture, Agent, adapters |
| [DOC-08](DOC-08-bpm.md) | **BPM** — jBPM engine, Project Mgmt, Process Templates/Actions, User Tasks, process events |
| [DOC-09](DOC-09-extensions-dev.md) | **Extensions / Dev** — REST API, EC Extensions (WAR/Maven/Flyway), data-model rules, dev env, DomainEntityMgr |
| [DOC-10](DOC-10-graphql-reporting-edac.md) | **GraphQL + eDAC + Reporting** — GraphQL queries/mutations, data access control, report engines |
| [DOC-11](DOC-11-iam-dbdev-containers.md) | **IAM + DB Dev + Containers** — Keycloak, service accounts, Flyway, container topology, PKI, Blob Storage |

## Cross-cutting threads (the "aha"s that tie it together)
1. **The View Generator is the spine.** Object classes → generated `OV_`/`DV_`/`RV_` views + `INSTEAD OF` IUD triggers (DOC-02). This single fact explains: how my Bank/Equipment IUD worked, why `OV_BANK`/`OV_EQPM` exist, where eDAC predicates live (DOC-10), and the RV_ reporting layer (DOC-10).
2. **Versioned objects → date-effective delete.** Mandated `OBJECT_START_DATE`/`OBJECT_END_DATE` (DOC-02) is *why* **End Date = Start Date is a true delete** — the docs confirm what I proved empirically.
3. **Record status P→V→A** runs through everything: status processes (DOC-04), cargo status (DOC-06), document lifecycle (DOC-05), ECIS DEFAULT_RECORD_STATUS (DOC-07).
4. **Four ways to do IUD on EC data:** UI (my Playwright work) · direct DB · **REST domain API** (DOC-09) · **GraphQL mutations** (DOC-10) — all fire `DomainObjectChanged` events (DOC-07). *For future automation, a REST/GraphQL approach + Keycloak service account (DOC-11) would beat UI automation.*
5. **Configuration over code** — owner-context overrides (DOC-02), extensions (DOC-09), BPM "work by exception" (DOC-08), generic check rules/calc framework (DOC-03/01).

## Version note
Local = **EC 14.2.4**; my earlier topic deep dives used the 14.2.5 hub docs — minor delta, no contradictions found.

## Recon scripts (read-only)
`tmp/scripts/ec_doc_index_mapper.py`, `ec_doc_reader.py` (generic: `py ec_doc_reader.py LABEL "module1,module2" start count cap`), `ec_doc_analyze_*.py`. Raw page text kept in `_raw/`.
