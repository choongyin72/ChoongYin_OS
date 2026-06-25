# Well Gas Component Analysis (WR.0010.01) — SME deep-dive (Phase 0)

_Pre-build deep-dive 2026-06-17. The WELL-level gas-composition sibling of the stream gas analysis
[[COMPONENT-ANALYSIS-SME]] (PO.0020); part of the Lab/Sample-Analysis lineage
[[LAB-SAMPLE-ANALYSIS-LINEAGE]]. **Sources:** ECpedia (BPR "Polar Bear - Component Analysis";
EPR "How to configure AGA3/8 for Well and Streams", "XCA Recombined Analysis for Well and Stream",
"Gas Allocations"; "Oil/Condensate Well Component Analysis"); DB recon (`tmp/scripts/recon_wellcomp_db.py`,
`recon_wellcomp_screen.py`). Read-only._

## 1. What the screen is
**Well Gas Component Analysis (WR.0010.01)** — a.k.a. "Gas Well Component Analysis" — captures the
**per-well gas composition (component mol %)** from laboratory / analyser samples. It is the **well-level
analogue of PO.0020** (stream gas comp): same per-COMPONENT grid, same processing, but the object is a
**WELL** instead of a stream. Family: PO.0020 stream gas / PO.0019 stream oil / WR.0010.01 well gas /
Oil-Condensate Well Component Analysis (well oil).

## 2. Why it matters (business purpose) — well-specific uses
A well's approved gas composition drives:
- **Base compressibility (Z-factor) for AGA3/8 gas metering** — _"the component analysis must be present
  with **approved status** for the well in Well Gas Analysis (WR.0010-01) … used to calculate the base
  compressibility"_ (the well's meter run reads it). So the **P→V→A** lifecycle gates real gas metering.
- **Recombined analysis** — for a gas-producer well, the **gas + condensate** component analyses are
  **recombined into one rich gas composition** (expressed as gas + gas-equivalent in **mol fractions**)
  linked to a target "Recombined" stream → feeds **well-level gas allocation**.
- **Well test interpretation / back-allocation** — per-well composition supports the well allocation
  process during a production phase.

## 3. Data model — same shape as stream comp, WELL object
View **`DV_WELL_COMP_ANALYSIS`** (138 rows), **structurally identical** to `DV_STRM_COMP_ANALYSIS`:
OBJECT_ID, OBJECT_CODE, DAYTIME, **ANALYSIS_TYPE**, SAMPLING_METHOD, PHASE, ANALYSIS_NO, **COMPONENT_NO**,
**MOL_PCT**, **WT_PCT**, RECORD_STATUS, APPROVAL_STATE. `ANALYSIS_TYPE` values: **`WELL_GAS_COMP`**
(this screen), WELL_OIL_COMP, WELL_RES_COMP, WELL_INJ_COMP, COMP_01.
- **Gas ⇒ the measure is `MOL_PCT`** (like stream gas PO.0020 — so the editable cell is the mol% column,
  expected `C1_in`, NOT the wt%/C2 column that oil PO.0019 uses).
- Target candidate: **`P1_W260_GP_COMP_GAS` @ 2025-04-01** (Preliminary, SPOT, **9 components, MOL_PCT
  populated**); also an Approved one @ 2025-04-02; `P1 W004` @ 2011-01-01 (8 comps, mol%). Name source is
  the WELL object (likely `WELL_VERSION`, not `OV_STREAM`) — Phase-1 recon confirms.

## 4. Config / processing / validations — same family
Component Constant (CO.0103) + Component Set List; **Wt↔Mol / Mol→Energy / Normalize** buttons (the
"Oil/Condensate Well Component Analysis" page confirms "Wt to Mol calculates mol% when all wt% not null");
**sum 98–102%** + missing-component + frozen validations; **RECORD_STATUS P → V → A** (lab supervisor +
production chemist sign-off — see lineage). Same Analysis Data Management BPM.

## 5. How it DIFFERS from PO.0020 (the build deltas)
| Aspect | PO.0020 stream gas | WR.0010.01 well gas |
|---|---|---|
| Object / view | stream, `DV_STRM_COMP_ANALYSIS` | **well, `DV_WELL_COMP_ANALYSIS`** (ANALYSIS_TYPE=WELL_GAS_COMP) |
| Navigator | **8 fields** (2 dates + 6 dd) | **9 fields** (2 dates + **7** dd) — the well hierarchy is deeper (an extra Well/Well-Hookup dropdown) ⚠️ recon maps it |
| Name source | `OV_STREAM` | likely **`WELL_VERSION`** (recon confirms) |
| GO / grid / cell | `go_button:form:B`, `component_set:form`, mol%=`C1_in` | **same** (`go_button:form:B` + component grid confirmed live; mol% cell expected `C1_in` — recon confirms) |
| Measure | MOL_PCT | **MOL_PCT** (same — gas) |

## 6. Automation implications (Phase 1 recon + Phase 2 build)
- Screen confirmed live: 2 dates + **7 dropdowns** + `go_button:form:B` (component grid loads after
  nav+GO). Phase-1 recon must: identify the **extra well dropdown** + the well-scope cascade, confirm the
  **mol% cell is `C1_in`**, resolve the well name source, and run the edit→Save→DB→revert probe.
- Reuse the existing **`component_value_should_be(view, oid, date, component_no, 'MOL_PCT', expected)`** —
  **no DbVerify change → no R12 canary.** TC03 reload-before-revert (composition-screen quirk).
- Follows the PO.0019 3-phase structure (SME → recon → build) per the same-screen-family decision.

## 7. Sources
ECpedia: BPR *Polar Bear - Component Analysis*; EPR *How to configure AGA3/8 for Well and Streams*
(approved well gas analysis → base compressibility), *XCA Recombined Analysis for Well and Stream*,
*Gas Allocations*; *Oil/Condensate Well Component Analysis* (Wt→Mol). DB recon:
`tmp/scripts/recon_wellcomp_db.py` + `recon_wellcomp_screen.py`. Companions: `COMPONENT-ANALYSIS-SME.md`,
`STREAM-OIL-COMPONENT-ANALYSIS-SME.md`, `LAB-SAMPLE-ANALYSIS-LINEAGE.md`.
