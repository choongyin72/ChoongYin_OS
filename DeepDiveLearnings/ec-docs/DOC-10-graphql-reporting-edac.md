# DOC-10 — GraphQL + eDAC + Reporting
**Source:** EC 14.2.4 `graphql` (8) + `edac` (4) + `reporting-and-analytics` (7) = 19 pages · **Read:** 2026-06-06

## A. EC GraphQL 🔑 (a 4th IUD path)
A REST endpoint (`/rest/v1/services/graphql`, sub-endpoints `/schema`, `/query`) offering GraphQL over the EC domain model — "ask for exactly what you need." Also a Java API.
- **Type system auto-generated from EC classes**: type name = CLASS in caps; fields = attributes (caps; disabled/ignored/report-only excluded); **`REL__<relation>`** (outgoing), **`REF__<class>`** (incoming), plus `meta` (EcClassRecordMeta = createdBy/revNo/recId…). Scalars: Int/Float/String/Boolean/ID + EC's `Number`/`Void`.
- **Queries**: hierarchical; filters **`qc` (criteria, e.g. `["CODE,=,P1_AREA"]`), `qs` (sort), `qf`, `qt`** — same filter syntax as the REST domain API; aliases + variables supported.
- 🔑 **Mutations**: `insert_<CLASS>`, `update_<CLASS>`, `merge_<CLASS>`, `delete_<CLASS>` (records: `[<CLASS>_Record!]!`), processed sequentially. **This is a 4th way to do IUD** (UI / direct-DB / REST / **GraphQL**) — e.g. `insert_T_BASIS_OBJECT` + `insert_T_BASIS_ACCESS` in one request. *(A GraphQL-based EC-IUD automation would be far simpler than my Playwright UI approach.)*
- **Directives** (`@`): `@distinct @group @limit @move @put @reduce @remove @trim @void` + standard `@include`/`@skip` — reshape/format output; chainable.
- **Transformations**: server-side **JSONata** engine (`transformation` request attr) or client-side.
- **Schema extensions**: implement `GraphQLSchemaProvider` SPI (register via `META-INF/services`) to add custom types + field resolvers (from mothership modules or extensions).

## B. EC Data Access Control (eDAC) 🔑
Row-level data access, **EC-12.0+ all classes access-controlled**.
- **Mechanism**: eDAC adds a **where-clause predicate into the generated class view** (object/interface/data/table views) — so **Application layer and DB layer share one access-controlled view**. ⚠️ **Direct DB tables + hand-coded views are NOT access-controlled** — only generated class/`OV_`/`DV_` views are. *(Relevant: I query as `ECKERNEL_EC` (owner) → full access; an external/reporting user would be filtered.)*
- **ACL** (Access Control Lookup): object class is the root — direct object-id lookup vs user's explicitly assigned roles. Empty predicate = everyone sees all; non-empty = filtered by ACL + roles.
- **Three methods** (configure via class property **`ACCESS_CONTROL_IND=Y`** + object partition, owner ctx ≥1000):
  - **Direct** (object classes only) — direct ACL lookup.
  - **Relational** — data/table class inherits from owner object class (`ACCESS_CONTROL_METHOD` = TO_CLASS/FROM_CLASS/ACL_LOOKUP).
  - **Reference** — via a read-only reference class (e.g. CONTRACT ↔ TRAN/SALE/REVN_CONTRACT, dependency `ACCESS_CONTROLLED_BY`).
- Report views get the same predicate; **journal views get none**.
- **External DB users**: never connect as ECKERNEL/ENERGYX. Link an external user to an EC app user via a **logon trigger** (`dbms_session.set_context('CLIENTCONTEXT','USER'/'ROLES',...)`) + `ue_ringfencing.allowAccessToGlobalContext`. (Ringfencing/Object-Partitioning from DOC-02 row-level security.)

## C. Reporting & Analytics
- **Template-based fixed reports**: every report needs a **report template** (engine + params) + **report definition** (content) + **report/runnable** (DOC-01 reporting concept). Generated report streamed to DB as a **BLOB**.
- **Engines**: **internal** (EC does all processing, sync generation/async call) vs **external** (separate server, EC writes commands to a DB table, engine polls). Plus **Yellowfin** ("EC Reporting and Analytics", ad-hoc + dashboards), **EC Jasper Report**, EC Excel, External System.
- **Jasper**: How to create/install/configure (ties to my JasperReports deep dive — Oracle, Jasper Studio, jrxml→jasper).
- **Database Reporting Layer**: the `RV_` report views (used by Check Rules `${var}` from RV view, DOC-03).
- **EC Standard Reports** config; **XML report via PL/SQL** (`gen_xml_report_db`); **Report Access** config (by role); **Export to Excel Express** (RP.0011, ad-hoc, not template-connected).
- Automate generation via Scheduling or Process Automation (BPM).

---

## Cross-links
- 🔑 **GraphQL mutations** = a clean 4th IUD path (with qc/qs filters) — strong candidate for a future API-based EC-IUD vs UI automation. All paths fire `DomainObjectChanged` (DOC-07).
- **eDAC** predicates live in the **generated class views** (DOC-02 view generator) — why my `ECKERNEL_EC` queries see everything but app/reporting users are filtered; ringfencing (DOC-02).
- Reporting builds on DOC-01 reporting concept + RV_ report layer (DOC-03 check rules) + my JasperReports deep dive.
- Next (final): **DOC-11 IAM + DB Dev + Containers**.
