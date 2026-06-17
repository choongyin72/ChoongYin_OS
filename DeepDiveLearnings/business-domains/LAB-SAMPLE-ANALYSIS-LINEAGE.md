# Laboratory / Sample-Analysis lineage in EC — deep dive

_Deep dive 2026-06-17 (user-requested): trace where lab/sample data ORIGINATES and how it FLOWS into the
composition screens we automated (PO.0020 Stream Gas Component Analysis, [[project_ec_coverage_resume_2026_06_17]]).
Read-only — no DB writes. **Sources:** ECpedia "ECE ChemSphere" space (Laboratory Information Management,
Manage samples, Sample analysis, Sample schedule editor, Laboratory analysis screens — energycomponents.atlassian.net/wiki/spaces/ECS);
EC tech-doc DOC-04 (Analysis Data Management BPM); sandbox DB recon (`tmp/scripts/recon_lab_sample_lineage.py`);
the composition SME doc `COMPONENT-ANALYSIS-SME.md`; local `chemistry.md`._

## 1. The module: Laboratory Information Management (LIM / "ECE ChemSphere")
EC's lab layer is a **lightweight LIMS**. It manages **Sample Management · Sample analysis · Field analysis**,
all tagged to a facility via the **Analysis Point** object. Composition (mol% to C6+) that the production
calc chain consumes is the OUTPUT of this layer.

## 2. The lineage — origin → composition → calc (end to end)
```
Analysis Point (type=Sample Point)        ANALYSIS_POINT(+_VERSION)        ← the "where" (virtual sample/measure location)
        │  risk model → sample frequency
        ▼
Sample Schedule (sample program)          (schedule tables; SAMPLE_SCHEDULE_EDIT, SCHEDULE_SAMPLE_REF)
        │  scheduled OR ad-hoc
        ▼
Sample registered + shipped to lab        SAMPLE_REGISTRATION  (+ per-object *_SAMPLE: PWEL_SAMPLE 25k,
        │                                  WBI_SAMPLE, PFLW_SAMPLE, IWEL_SAMPLE, TEST_DEVICE_SAMPLE …)
        ▼
Lab reports analysis (element/method/uom) LAB_ANALYSIS ──FK──> SAMPLE_REGISTRATION
        │  per Analysis Template (what to measure)   ANALYSIS_TEMPLATE(+_ITEM/_PROP) ; ANALYSIS_ITEM ─> HYDROCARBON_COMPONENT
        │  validated: lab supervisor + production chemist  →  RECORD_STATUS  P → V → A
        ▼
Analysis distributed to consuming tables  ANALYSIS_TARGET(+_MAP)  →  composition/fluid analysis tables:
        │                                  • STRM_COMP_ANALYSIS  (view DV_STRM_COMP_ANALYSIS) ← PO.0020 we automated
        │                                  • OBJECT_FLUID_ANALYSIS → FLUID_ANALYSIS_COMPONENT (4088 rows) → HYDROCARBON_COMPONENT
        │                                  • STRM_ANALYSIS_COMPONENT / STRM_PC_COMP_ANALYSIS / STRM_WATER_ANALYSIS
        │                                  • CARGO_ANALYSIS / PARCEL_ANALYSIS / TANK_ANALYSIS / WELL_FLUID_ANALYSIS
        ▼
Analysis Data Management BPM              bulk Mol↔Wt↔Energy + Normalization (DOC-04) — the processing
        │                                  behind the composition screen's Mol→Wt / Mol→Energy / Normalize buttons
        ▼
Allocation / energy / emissions / contract-account quality   (the calc chain — composition is the quality input)
```

## 3. The key entities (ECpedia model ↔ DB)
- **Analysis Point** (`ANALYSIS_POINT`/`_VERSION`) — a *virtual* representation of the physical sample/measurement
  point; tags sample+analysis to a facility; optionally links to other facility objects/streams. **Must exist
  before any Lab feature is used.** Type **"Sample Point"** = where a physical sample is taken (vs plain
  "Analysis Point" = where analysis/metering is performed). The composition screen's Sample Point dd lists
  Analysis Points of type Sample Point, filtered by Facility Class 1.
- **Analysis** = elements, compositions, properties measured by an **analytical method**. **Unique analysis =
  (element + method + UOM)** — method matters (ICP vs IC measure different things). Elements/methods/UOM are
  user-configurable code lists.
- **Analysis list / template** (`ANALYSIS_TEMPLATE`/`_ITEM`/`_PROP`) — user-defined groups of analysis
  combinations = the registration template (the component set + methods). `ANALYSIS_ITEM ─> HYDROCARBON_COMPONENT`.
- **Sample schedule** — sample *programs*: location + frequency (daily/weekly/monthly/yearly, time-limited or
  not) + required analysis; can be **shared across multiple sample points** (e.g. 11-ion water analysis from
  many wells); viewed in the **Sample and Schedule Status** screen.
- **Sample registration** (`SAMPLE_REGISTRATION`) — the Sample Manager hub: ad-hoc or from schedule; carries
  sample date, location, auto sample number, sample point, preservation, **receiving laboratory**, comments,
  and references to objects/streams (co-mingled) or chemical product/storage/tank. Every `LAB_*` analysis
  (`LAB_ANALYSIS`, `LAB_SAMPLE_PROPERTIES`, `LAB_COUPON_ANALYSIS`, `LAB_CORROSION_FLUID`, `LAB_SCALE_FLUID_REF`)
  **FK→SAMPLE_REGISTRATION**.
- **Lab analysis** (`LAB_ANALYSIS`, 36 cols) — the result row: OBJECT_ID, ANALYSIS_POINT_ID, ANALYSIS_TYPE/
  ELEMENT/METHOD, ANALYSIS_VAL/UOM, MIN/MAX, REL/ABS uncertainty, STD_DEV, VARIANCE, **ACCREDITED**,
  ANALYSIS_TEMPLATE, **RECORD_STATUS**.

## 4. The validation lifecycle (why P → V → A exists)
ECpedia: the analysis is **validated by BOTH the laboratory supervisor and the production chemist** who
receives it; indicators feed a **risk model** that can re-classify the system and change sample frequency/type.
In data terms that double sign-off is the **RECORD_STATUS P (Preliminary) → V (Verified) → A (Approved)**
lifecycle — the same one our N3 status-process suites lift, and the same `RECORD_STATUS` the composition
screen exposes. (This is why the composition sum 98–102% rules 1156/1157 and frozen checks live here — they
guard the analysis before it is Approved and feeds allocation.)

## 5. How the data ARRIVES (import paths)
1. **Manual entry** on the Sample Manager / composition screens (what we automated for PO.0020).
2. **Sample schedule → registration** (scheduled program generates the samples to register).
3. **Lab/analyser import** — bulk results from the laboratory; and the **ECIS Advanced-Excel upload**
   (the parked ECIS task) is a manual backup path that can land composition the same way.
4. **Inline instruments / field analysis** — direct measurement tagged to an Analysis Point.

## 6. Connection to our automation + next targets
- **Automated:** PO.0020 Stream Gas Component Analysis = editing `STRM_COMP_ANALYSIS.MOL_PCT` (PR #43) — this
  is the *consuming/composition* end of the lineage.
- **Parked, now explained:** the N3 V→A **`WELL_FLUID_ANALYSIS`** target (parked: needs WHERE-var resolution +
  data) is one of the analysis consuming tables in step 2's distribution — its lifecycle is this P→V→A.
- **Candidate next builds (same lineage, richer data):** `OBJECT_FLUID_ANALYSIS`/`FLUID_ANALYSIS_COMPONENT`
  (660/4088 rows — the fluid composition store), the **Sample Manager / Sample registration** screen, the
  **Sample and Schedule Status** screen, and **Stream Oil Component Analysis (PO.0019)** / **Well Gas
  Component Analysis (WR.0010.01)** (composition siblings of PO.0020 — near-turnkey T3 reuse).
- **Automation note:** these screens are the per-component / per-analysis grid pattern proven in PR #43
  (8-field nav + `go_button:form:B` + component grid + the new `component_value_should_be` DbVerify keyword).

## 7. Sources (for re-verification)
- ECpedia (ECE ChemSphere / ECS): *Laboratory Information Management* (892963871), *Manage samples* (892965476),
  *Sample analysis* (892965844), *Sample schedule editor* (892964512), *Laboratory analysis screens* (898105685).
- EC tech doc: DOC-04 Production §Analysis Data Management BPM (`DeepDiveLearnings/ec-docs/DOC-04-production.md`).
- DB recon: `tmp/scripts/recon_lab_sample_lineage.py` (tables/row-counts/FK edges).
- Companion: `COMPONENT-ANALYSIS-SME.md` (PR #40), local `chemistry.md`.
