# Pluto-Prioritized Coverage Backlog (2026-06-13)
Cross-reference: Pluto As-Built 02 screen catalog (the screens Pluto ACTUALLY uses) × the
automated-screen registry. Purpose: stop automating generic Assets screens blindly; target the
screens that matter for Pluto business-test suites (coverage-goal phase 2). Derived from
DeepDiveLearnings/business-domains/ASBUILT02-SCREENS.md + ec_screen_registry.md.

## Already automated (Pluto-relevant master data) ✅
Basic Objects (Area, Sub Area, Country, County, State, Region, Business Unit, Functional Area,
Object List(+Setup), Production Unit); Financial (Account, Cost Centre, Currency, DOA Credit
Limit, Exchange Rate Source, Payment Scheme, Product Description, Revenue Order, Sales Order,
VAT Code, WBS, Bank(+Account), Cost Object Mapping, Account Mapping); Commercial (Company,
Customer, Vendor, Licence, MMS/State/Operator Lease, Field, Field Group, Commercial Entity,
Company Contact); Equipment; Dispatching (Delivery Point/Stream, Meter, Nomination Point/Cycle,
Pipeline Segment, Transport System/Zone); System (MIME, Language); Validation Overview (RUN).
= the master-data layer the Pluto flow runs on. Solid foundation.

## Gap analysis — Pluto screens NOT yet automated, by NEW pattern type
My framework covers OV / TV / OV-GM / PC (master-data IUD) + RUN-verify (Validation Overview).
The unautomated Pluto screens cluster into pattern types I DON'T yet have a T2 for:

### Pattern N1 — Daily/Monthly STATUS data-entry grids (the biggest, highest-value gap)
Date-navigator + editable grid of measured values per object/day. The core operational screens.
- WR.0001 Daily Prod Well Status (PLU) · WR.0027 (SCA) · WR.0032/0033 by-well
- PO.0002 Daily Gas Stream Status (+PO.0060 by-stream) · PO.0001 Daily Liquid (+PO.0059)
- PO.0066 Daily Electrical (+PO.0079) · PO.0003 Daily Water (+PO.0033) · PO.0028 Sub-Daily Gas
- CO.0011 Daily Equipment Status · PO.0005.02 Daily Tank Status (VCF) · PO.0008 Op Comments
- Monthly variants: PO.0024/0041/0114, WR.0078, PO.0080
- Component analysis: PO.0020 Stream Gas Comp · PO.0019 Stream Liquid Comp · WR.0010.01 Well Gas Comp
→ **Build a T2 "daily-status grid" pattern** (date nav + GO + cell edit + DB-verify on
*_DAY_STATUS). This unlocks the most Pluto business tests (it's where PHD data + Issue_1052
validations live). HIGHEST PRIORITY.

### Pattern N2 — RUN / calculation screens
- HA.0002 Daily Allocation · HA.0003 Monthly Allocation (run calc over a day/range)
- RP.0003 Report Administration (+RP.0013/0014 generate/publish) · CO.0130 Schedules (set aside w/ ECIS)
→ Extend the RUN-verify pattern (already have it for Validation Overview): trigger → wait →
DB-verify the result tables (PWEL_DAY_ALLOC, STRM_MTH_ALLOC). NOTE: blocked while sandbox
scheduler stalled.

### Pattern N3 — Status-process screens (P→V→A governance)
- HA.0001 Daily Data Status Processes (+by-Facility) · HA.0004 Monthly Data Status Processes
→ select data scope → run status process → assert RECORD_STATUS transition + edit-lock. Tests
the governance spine (backlog P2).

### Pattern N4 — Config/validation screens (partly studied via Issue_1052)
- CO.0079 Check Group · CO.0080 Rule Group Combination · CO.0078 Check Rule (Issue_1052 turf)
- CO.0076 Status Processes · CO.0226 Mismeasurement Event · XEM.0002 Stream Emission Configuration
→ master-data-like config; some are OV/TV variants I can reach with existing patterns.

### Pattern N5 — Finder / search screens
- WR.0066 Well Finder · PO.0102 Stream Finder
→ search + navigate (read-only assert); low priority.

### Deferment / cargo / contract-account (domain-specific)
- ZZ.0001 Master Deferment Event · ZZ.0002 Daily Deferment Entry · TO.0017 BL/MR Light ·
  TO.0012 Month End Not Lifted · PO.0043 Truck Ticket · SA.0008/0009/0019 Contract Account
→ mix of N1/N3; build after N1 pattern exists.

## Recommended next slices (priority order)
1. **N1 daily-status grid** — pick ONE representative (WR.0001 Daily Prod Well Status PLU; rich,
   central, PHD-fed, ties to Issue_1052). Build the T2 pattern + that screen. ← do first.
2. Add PO.0002 Daily Gas Stream Status (reuse N1) — proves the pattern generalizes.
3. N3 status-process (HA.0001) — enables the P→V→A governance tests.
4. N2 allocation run (HA.0002) — once sandbox scheduler/app healthy.
Hold: ECIS-adjacent (CO.0130/IS.0006/IS.0001 — set aside), reporting RP.* (after N1/N2).

## Note
This supersedes "next alphabetical Assets section" as the coverage strategy — Pluto value lives
in the transactional/status screens (As-Built 02 §2.3), not more master-data OV. The master-data
foundation is largely done.
