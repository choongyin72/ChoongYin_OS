# Database Design Summary — ECKERNEL_EC (Pluto Dev)

**Generated:** 2026-06-02  
**Connection:** `db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev`  
**Schema User:** `ECKERNEL_EC`

---

## Platform Identity

This is a **Tieto/Quorum Energy Components (EC)** instance — an enterprise oil & gas production and commercial management platform. The `ECBP_` package naming convention, `DV_` view prefix, and overall schema structure are unmistakeable EC fingerprints.

---

## Scale

| Metric | Value |
|--------|-------|
| Tables | 3,606 |
| Views | 9,786 |
| Triggers | 10,725 |
| Packages | 2,571 |
| Indexes | 7,859 |
| Total objects | ~37,400 |
| Total columns | 578,661 |
| Schema size (est.) | ~3.4 GB |
| FK constraints | 2,564 |
| PK constraints | 1,864 |

---

## Business Domain Map

| Domain | Prefix | Tables | Purpose |
|--------|--------|--------|---------|
| Forecasting | `FCST` | 235 | Production & commercial forecasting |
| Streams | `STRM` | 170 | Fluid stream allocation & measurement |
| Contracts | `CNTR` / `CONTRACT` / `CONT` | ~237 | Commercial contracts, transactions, documents |
| Emission Ext Model | `XEM` | 102 | External emissions modelling |
| Calculations | `CALC` | 89 | Equation engine, calc contexts |
| Zone/Well Props | `ZWP` / `ZWT` | 160 | Zone well production data |
| Chemicals | `CHEM` | 86 | Chemical injection management |
| Storage | `STOR` / `STORAGE` | 97 | Tank & storage management |
| Control/Workflow | `CTRL` / `BPM` / `JBPM` | 181 | Process control, jBPM workflow engine |
| Well Management | `WELL` / `WEBO` / `PWEL` / `IWEL` | ~147 | Wells, wellbores, producers, injectors |
| Reporting | `REPORT` | 64 | Report definitions & output |
| Products | `PRODUCT` | 57 | Hydrocarbon products |
| Nominations | `NOMPNT` | 46 | Nomination points |
| Cargo / Shipping | `CARGO` / `VOY` | 65 | LNG cargo transport, voyages |
| Finance / Revenue | `FIN` / `REVN` | 69 | Financials, revenue accounting |
| Facilities | `FCTY` | 33 | Production facility data |
| Well Stimulation | `STIM` | 32 | Well stimulation operations |
| Pipeline | `PIPE` | 22 | Pipeline infrastructure |
| Pricing | `PRICE` | 22 | Product pricing |
| Lab | `LAB` | 22 | Laboratory fluid analysis |
| Metering | `METER` | 17 | Meter configuration & readings |
| Calendar | `CALENDAR` | 17 | Scheduling & business calendars |

---

## Core Entity Model

These are the central parent tables — everything else hangs off them:

| Rank | Table | Inbound FKs | Role |
|------|-------|-------------|------|
| 1 | `GEOGRAPHICAL_AREA` | 134 | Top of the location hierarchy |
| 2 | `STREAM` | 124 | Central fluid stream entity |
| 3 | `CONTRACT` | 122 | Commercial agreements |
| 4 | `FORECAST` | 116 | Forecast scenarios |
| 5 | `COMPANY` | 106 | Company / counterparty master |
| 6 | `PRODUCTION_FACILITY` | 89 | Physical facilities |
| 7 | `WELL` | 70 | Well master data |
| 8 | `PRODUCT` | 61 | Hydrocarbon product types |
| 9 | `HYDROCARBON_COMPONENT` | 60 | Component (C1, C2, CO2, etc.) |
| 10 | `STORAGE` | 54 | Storage locations |
| 11 | `FORECAST_GROUP` | 53 | Forecast groupings |
| 12 | `DELIVERY_POINT` | 50 | Delivery/transfer points |
| 13 | `NOMINATION_POINT` | 43 | Nomination locations |
| 14 | `CURRENCY` | 38 | Currency master |
| 15 | `LIFTING_ACCOUNT` | 30 | Entitlement accounts |

**Core production hierarchy:** `GEOGRAPHICAL_AREA` → `PRODUCTION_FACILITY` → `WELL` → `STREAM`

---

## Architectural Patterns

### 1. Universal Audit Framework
Every table carries these 7 columns (framework-enforced via triggers):

| Column | Purpose |
|--------|---------|
| `CREATED_DATE` | Record creation timestamp |
| `CREATED_BY` | Creating user |
| `LAST_UPDATED_DATE` | Last modification timestamp |
| `LAST_UPDATED_BY` | Last modifying user |
| `RECORD_STATUS` | Active/inactive flag |
| `REV_NO` | Revision number |
| `REV_TEXT` | Revision comment |

The 10,725 triggers are primarily audit triggers enforcing this framework on every DML operation.

### 2. Journal / History Tables (`_JN`)
~4,200 tables carry `JN_DATETIME`, `JN_OPERATION`, `JN_ORACLE_USER`, `JN_SESSION`, `JN_NOTES`, `JN_APPLN` columns. Roughly one-third of all tables have a shadow `_JN` journal table capturing every row change. This underpins the full audit trail visible in the EC UI.

### 3. Temporal Data Model (`DAYTIME`)
`DAYTIME` and `OBJECT_ID` appear in 9,000+ tables. EC uses a time-series-oriented model — most operational data is keyed by `(OBJECT_ID, DAYTIME)`, allowing point-in-time queries across all entities. Always bound custom queries by date range when working with these tables.

### 4. Versioning Pattern (`_VERSION`)
The most FK-laden tables follow the `_VERSION` suffix. Entities have a base record + versioned child records tracking configuration changes over time without losing history.

| Version Table | FK Count |
|---------------|----------|
| `WELL_VERSION` | 34 |
| `CONT_TRANSACTION` | 21 |
| `STRM_VERSION` | 14 |
| `CONTRACT_VERSION` | 11 |
| `EQPM_VERSION` | 11 |

### 5. Object/Class Configuration Model
`CLASS_ATTR_PROPERTY_CNFG` (468K rows) and `CLASS_ATTRIBUTE_CNFG` (55K rows) are the metadata configuration tables. EC uses a class-based attribute model allowing runtime configuration of object types without schema changes — customisation goes here rather than into the schema itself.

---

## Largest Tables by Volume

| Table | Rows | Est. Size | Notes |
|-------|------|-----------|-------|
| `CTRL_PINC` | 750,216 | ~548 MB | Controller process instance data |
| `CLASS_ATTR_PROPERTY_CNFG` | 468,186 | ~112 MB | Attribute configuration metadata |
| `ALLOC_JOB_RUN_MESSAGE` | 438,430 | ~87 MB | Allocation job log messages |
| `CTRL_EVENT_HISTORY` | 297,182 | **~1.85 GB** | Largest by disk — likely CLOB event payloads |
| `CLASS_ATTR_PROPERTY_CNFG_JN` | 210,262 | ~96 MB | Journal of attribute config changes |
| `IMP_STAGING_JN` | 131,902 | ~119 MB | Import staging journal |
| `CNTR_SUB_DAY_STATUS` | 101,400 | ~16 MB | Contract sub-day status |
| `STRM_DAY_COMP_ALLOC` | 84,051 | ~20 MB | Stream daily component allocation |

`CTRL_EVENT_HISTORY` is the single largest disk consumer despite not having the most rows — likely storing large XML/CLOB event payloads from the jBPM workflow engine.

---

## Index Strategy

- **7,706 normal B-tree indexes** + 153 LOB indexes
- No bitmap, function-based, or domain indexes
- Standard OLTP indexing — consistent with heavy transactional write workloads

---

## Object Counts by Type

| Object Type | Count |
|-------------|-------|
| TRIGGER | 10,725 |
| VIEW | 9,786 |
| INDEX | 7,859 |
| TABLE | 3,606 |
| PACKAGE | 2,571 |
| PACKAGE BODY | 2,565 |
| LOB | 153 |
| TYPE | 69 |
| SEQUENCE | 46 |
| TYPE BODY | 12 |
| JOB | 5 |
| PROCEDURE | 1 |

Note: 6 packages have no corresponding body (2,571 specs vs 2,565 bodies).

---

## Column Data Type Distribution

| Data Type | Count | % |
|-----------|-------|---|
| VARCHAR2 | 336,409 | 58% |
| NUMBER | 144,806 | 25% |
| DATE | 76,126 | 13% |
| CHAR | 21,047 | 4% |
| CLOB | 131 | <1% |
| BLOB | 70 | <1% |
| TIMESTAMP(6) | 69 | <1% |

---

## Key Takeaways

1. **Full EC deployment** — covers wells, production, contracts, nominations, cargo, finance, and emissions. A broad footprint suggesting Woodside's full upstream and commercial operations are managed here.
2. **Schema is product-generated** — not bespoke. Customisation happens through configuration tables (`CLASS_ATTR_PROPERTY_CNFG`) rather than schema changes.
3. **Audit and history are built into the fabric** — triggers + `_JN` journal tables provide a complete change log on every entity.
4. **The temporal model (`DAYTIME`) is central** — almost all operational queries will be time-bounded. Always filter by date range when querying time-series tables.
5. **Core production hierarchy to learn first:** `GEOGRAPHICAL_AREA` → `PRODUCTION_FACILITY` → `WELL` → `STREAM`
6. **`CTRL_EVENT_HISTORY`** is a watch-out table — 1.85 GB, avoid full scans.
7. **Views (`DV_` prefix) are the intended query layer** — 9,786 views wrap the raw tables with business logic; prefer views over direct table access for reporting.
