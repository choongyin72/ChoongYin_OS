# EFK Phase A2 — Calculation Framework — 2026-06-13

EFK calc pages are mostly **training wrappers** (objectives + slide images; little body text).
I already hold deep calc-framework knowledge in `ec-docs/DOC-12`; this section adds two
concrete, high-value items + confirms the model. Pages: EC Calculations parts 1-4, Calc Engine
PM Basics (Type/Versions), calculation editor prototype (MathML), + 3 how-tos.

## 🔑 How To Run an Allocation — step-by-step recipe (page 1845417)
The generic product recipe BEHIND Pluto's daily allocation (As-Built §2.1.1). Setup→run chain:
1. Production Unit (opt) → Area (opt) → **Facility Class 1** (mark injection type) → Stream →
   2 Wells.
2. **Allocation Network → Allocation Network List → Alloc Network Calc Job Conn → Stream Set
   List** — the network wiring (these config objects make allocation runnable).
3. **Initiate Day** → insert values on Stream + Well → **Run Allocation** → view result on
   daily (water injection) well status.
4. Iterate: unmark "Allocate all Phases Fixed" on a well → re-run → verify **Alloc Inj Vol** +
   **Alloc Factor** match the other well.
→ This is the concrete shape of my TEST-CASE-BACKLOG **P1 (daily-cycle smoke)**: the oracle is
the allocated volume + alloc factor on the well status after Run Allocation. The network
objects (Allocation Network / List / Calc Job Conn / Stream Set List) are PREREQUISITES —
same dependency-screen / groupmodel family I keep meeting (Pipeline op-PU lives here).

## Engine model (parts 2-4, confirmed vs DOC-12)
- Calculations are modelled with **variables + objects + SETS** (the "set concept" =
  collections of objects a calc iterates over). A calc references variables that resolve to
  RV-attributes / constants / function calls / subqueries (same formula engine as Check Rules
  → why Issue_1052 validations and allocation share syntax).
- **Three calc types** (Calculation Engine Calculation Type): **MathML equation** (the
  Calculation Editor, MathML prototype), **Excel workbook**, **Calculation Library**.
  → Excel-workbook calc type is distinct from ECIS Excel IMPORT (calc reads a workbook to
  compute; ECIS imports a workbook as data). Worth not conflating.
- **Calculation Versions** — calcs are version/date-effective like every EC object (the
  ZWP_ALLOC_*_V0 naming = version 0).

## Cross-links / decision
- Deepens: production.md (allocation), ASBUILT14 (daily flow), TEST-CASE-BACKLOG P1.
- Authoritative depth stays in DOC-12 + (Pluto-specific) As-Built 06 Calculations (still to read).
- Diminishing returns on EFK calc wrappers → A2 DONE. Next: A3 ECIS + "How to Set up PI DAS and
  ECIS" (product/ops angle on the OPC/PHD agent — complements As-Built 05).
