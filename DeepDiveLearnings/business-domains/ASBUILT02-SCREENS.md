# Pluto As-Built 02 — Screen Configuration (deep dive, 2026-06-13)
Source: `WSPLU_EC_AsBuilt02_ScreenConfig_v1.0.docx` (286 pages). **Read: TOC (full screen
catalog) + intro/design decisions. The per-screen attribute tables (body) not read line-by-line
— the catalog + key facts are the durable value for the coverage track.**

## 🔑 SI UNITS (critical for automation test data!)
Pluto uses **SI units**, converted from the Global Template:
| Dimension | Template | **Pluto (screen + DB)** |
|---|---|---|
| Temperature | °F | **°C** |
| Pressure | PSI | **MPa** |
| Gross Volume | — | **m³** |
| Std Volume | Mscf / Bbl | **Sm³** |
| Energy Density | Btu/scf | **GJ/Sm³** |
→ When I build/verify daily-status or allocation test data, values are °C / MPa / Sm³ / GJ —
not imperial. (Explains masking: volumes/mass/energy 1 dp, % 2 dp, fractions 2 dp from DDS14.)

## Config conventions (DDS 02)
- A screen whose attributes are ALL "Product" context = **Out-of-the-Box (OOTB)**; ZWP context =
  Pluto-custom. The doc lists only the attributes RELEVANT to Pluto, not every product attribute.
- Key decisions live in DDS14 (Business Processes — already read).

## Pluto screen catalog (by group + EC code) — the coverage-track master list
**Object/Config**: CO.1033 Production Day Table · CO.0076 Status Processes · CO.0077 Initiate Day ·
CO.1011 EC Codes · CO.1021 Units · CO.1016 Unit Conversion · CO.1022 Measurement Types ·
MHM.0010/0012/0001/0004/0013 (messaging) · CO.0060 Maintain Equipment · CO.1002 Object Maint ·
CO.1001 Role Maint · CO.1000 User Maint · CO.2018 Contract Parties · CO.0018 Maintain Equity Share ·
CO.3001 Sale Contract Attributes · CO.0036 Manage Tank.
**Interface**: CO.1017 Maintain Templates · CO.1018 Maintain Mappings · **CO.0130 Schedules** ·
MHM.0007 Message Journal · **IS.0006 Upload Files** · **IS.0001 Mapping Configuration**.
**Transactional** (the daily/monthly allocation flow): WR.0066 Well Finder · CO.0211 Swing Well
Conn · **WR.0001 Daily Prod Well Status (PLU)** / WR.0032 by-well · **WR.0027 Daily Prod Well
Status 2 (SCA)** / WR.0033 · PT.0003 Well Performance Curves · WR.0010.01 Well Gas Component
Analysis · PO.0102 Stream Finder · **PO.0020 Stream Gas Component Analysis** · PO.0019 Stream
Liquid Comp · PO.0028 Sub Daily Gas by Stream · **PO.0002 Daily Gas Stream Status** /PO.0060 ·
PO.0001 Daily Liquid /PO.0059 · PO.0066 Daily Electrical /PO.0079 · PO.0003 Daily Water /PO.0033 ·
CO.0011 Daily Equipment Status · SA.0008/0009/0019.CPY Daily Contract Account · PO.0008 Operational
Comments · **HA.0002 Daily Allocation** · WR.0078 Monthly Alloc Well Data · PO.0024/0041/0114
Monthly Gas/Liquid/Electrical Stream Status · PO.0151 Monthly Stream Allocation Result ·
SA.0015/0010/0020.CPY Monthly Contract Account · PO.0080 Monthly Op Comments · **HA.0003 Monthly
Allocation** · ZZ.0001 Master Deferment Event Mgmt · ZZ.0002 Daily Deferment Entry · TO.0017 BL/MR
Light · TO.0012 Month End Not Lifted · PO.0043 Truck Ticket · **HA.0001 Daily Data Status
Processes** /HA.0003 by-Facility · **HA.0004 Monthly Data Status Processes** · CO.0226
Mismeasurement Event · PO.0116 Facility Object Analysis · PO.0005.02 Daily Tank Status VCF ·
ZWT.0001 Monthly Management Reporting · PT.0013 Single Production Well Test Result.
**Reporting**: RP.0001 Template · RP.0002 Definition · RP.0003 Administration · RP.0013 Generation ·
RP.0014 Publishing · PR.0015 Display Published Report.
**Forecasting**: PP.0039 Forecast and Scenarios · PP.0033 Daily Facility Class 1 Forecast.
**Validations** (Issue_1052 screens): CO.0079 Check Group · CO.0080 Rule Group Combination ·
**CO.0203 Validation Overview – Pluto Scarborough** · CO.0078 Check Rule.
**Environmental**: XEM.0010 Emission Pollutant · XEM.0002 Stream Emission Configuration ·
XEM.0001 Stream Emissions Daily.
**Audit**: CO.1095 Authentication Audit.

## ⚠️ Discrepancy to verify
Validation Overview = **CO.0203** here (As-Built 02), but **CO.0204** in As-Built 14. Two screen
variants or a doc inconsistency — confirm the live code (my automation uses the one behind
"Validation Overview - Pluto Scarborough"; verify CO.0203 vs CO.0204 on the sandbox/registry).

## Value / cross-links
- Coverage track: this is the DEFINITIVE Pluto screen list (vs the generic Assets scan) — the
  screens that actually matter for Pluto business test suites. Feeds ec_screen_registry + the
  TEST-CASE-BACKLOG (real screen codes now attached to each flow).
- SI-units fact → update test-data conventions in the automation framework.
- Issue_1052 screens confirmed: CO.0079/0080/0203/0078.
