# Pluto As-Built 05 — Interfaces (deep dive, 2026-06-13) — ECIS-focused read

Source: `WSPLU_EC_AsBuilt05_Interfaces_v1.0.docx` (V1.0 26-Aug-2024, 120 pages).
**Read so far (targeted, NOT cover-to-cover): the interface inventory tables + I_IN_PHD_DAILY
(§2.3.4) + the manual-Excel interfaces (I_IN_MISMEASURED_CORRECTED §2.3.7, I_IN_THIRD_PARTY_
MEAS_PROD) + ZWP_INTERIM_DATA_UPLOAD pattern (§2.3.13/2.3.14). NOT read: DOMGAS/CARGO/TAS
inbound detail, all outbound interfaces, full data-element tables.**

## 🔑 THE reframing for the ECIS real task
My prior assumption needed correction. **I_IN_PHD_DAILY is NOT an Excel upload** — it's an
**automated OPC UA tag-data feed**:
- Source: Honeywell **PHD Supershadow Server** (Perth), field tag data — water/gas/condensate
  volume, pressure (WHP/BHP), choke position, onstream hours; LIMS lab data + LNG Train
  technical-max capacity are FOLDED IN (I_IN_LIMS, I_IN_LNG_DAILY are NOT separate imports).
- Mechanism: **ECIS Agent** (lightweight standalone app near the data source) → **OPC Adapter**
  → OPC UA. DEV endpoint: `opc.tcp://<PHD_SERVER_ADDRESS>:6100`, Security Mode Sign+Encrypt,
  Basic256, Basic auth `woodside\<svc>`. Trigger: Automated. ISA ref I-PHDSS-ECAAS-01-PH.
- Quality gate before post-import: e.g. fail if a tag's value is identical across 2
  consecutive reads; user can reset last-transfer-datetime on invalid tags to re-read.

So a **"PHD-backup via Excel"** task is NOT rebuilding I_IN_PHD_DAILY — it's a MANUAL Excel
fallback that lands the same data when the OPC feed is down. The real precedents for that are:

## The manual-Excel inbound interfaces (the actual ECIS-task pattern)
- **ZWP_INTERIM_DATA_UPLOAD** — the GENERIC Excel→staging→class loader, **reused across
  multiple interfaces** (§2.3.13 Monthly Failures Inputs → class `ZWP_I_SCTR_ACC_DAY_STATUS`;
  §2.3.14 LNG Train 1 Manager → `ZWP_I_CNTR_ACC_MTH_STATUS`). Flow = exactly what I built:
  Mapping Configuration (interface code ZWP_INTERIM_DATA_UPLOAD) → Upload Files (IS.0006) →
  EC Schedule job processes per mapping → data visible in the target report. **This is the
  proven CLAUDE_WELL_TEST pattern** → confirms my hands-on build is the right shape.
- **I_IN_MISMEASURED_CORRECTED** (§2.3.7): "covered by screen update (copy/paste) functionality"
  + Excel loader **per EC screen** (WR.0001 Daily Prod Well Status 1 PLU, WR.0027 Status 2 SCA,
  …). Manual. The corrections/mismeasurement path → closest to a "fix/replace PHD data" backup.
- **I_IN_THIRD_PARTY_MEAS_PROD**: Excel, manual, third-party measurement/production (e.g. KGP).
- Several interfaces marked **"No longer in scope / will not be implemented"** (I_IN_POB_DAILY,
  I_IN_PERF_CURVE, I_IN_HSE_DAILY, I_IN_LIMS-as-separate) — don't chase these.

## 🔑 REST API option (big for automating the backup)
Every manual upload also supports REST: **`POST /services/ecis/interfaces/<INTERFACE_CODE>/files`**
to push the file instead of the Upload Files screen. So the backup path can be either
operator-driven (Upload Files + Schedule) or automated (REST POST). Good design option to
raise with Choong-Yin.

## Inbound interface inventory (names seen, for orientation)
I_IN_PHD_DAILY (OPC tag, auto) · I_IN_DOMGAS (REST, auto, daily user-group gas) ·
I_IN_CARGO_JV_ENT_DAILY (REST, offtake/shipping from SDS) · I_IN_TAS (truck LNG) ·
I_IN_MISMEASURED_CORRECTED (Excel, manual) · I_IN_THIRD_PARTY_MEAS_PROD (Excel, manual) ·
I_IN_ANNUAL_CAPCITY / I_IN_120D_PROD_FORECAST / I_IN_ANNUAL_PROD_FORECAST (Excel forecast
uploads, manual, scheduled) · ZWP_INTERIM_DATA_UPLOAD (generic Excel loader, reused) ·
ZWP_PROD_TARGET (REST/Excel forecast). DOMGAS/CARGO use REST JSON (saw a PUT payload sample:
DAYTIME/OBJECT_CODE/EVENT_TYPE/QTY).

## Action for the ECIS real task (when resumed with Choong-Yin)
1. Confirm the backup's TARGET data = PHD daily field data → which EC daily-status classes
   (WR.0001/WR.0027 etc.) — same targets as I_IN_MISMEASURED_CORRECTED.
2. Decide manual (Upload Files + Schedule, my proven build) vs REST (`POST .../files`).
3. Reuse ZWP_INTERIM_DATA_UPLOAD pattern OR a dedicated ZWP interface per class family.
4. Deliver via Flyway (As-Built 05 is the spec to mirror); never hand-config COPSDEV.

## Next reads
As-Built 06 Calculations (ZWP_ALLOC_* + NGER) · As-Built 09 Validations (Issue_1052) ·
finish As-Built 14 GHG/Emissions + monthly.
