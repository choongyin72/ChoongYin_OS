# Stream Oil Component Analysis (PO.0019) — SME deep-dive (Phase 0)

_Pre-build deep-dive 2026-06-17 (per "understand the screen before automating it"). Sibling of the gas
analysis [[COMPONENT-ANALYSIS-SME]] (PO.0020) and part of the Lab/Sample-Analysis lineage
[[LAB-SAMPLE-ANALYSIS-LINEAGE]]. **Sources:** ECpedia (BPR "Polar Bear - Component Analysis";
XEM Stream Configuration + Emission calc reference; XCA Recombined Analysis); EC tech-doc Analysis Data
Management BPM (DOC-04); sandbox DB recon (`tmp/scripts/recon_oilcomp_sme.py`); Jira UC "Oil/Condensate
Stream Component Analysis". Read-only._

## 1. What the screen is
**Stream Oil Component Analysis (PO.0019)** — a.k.a. **"Oil / Condensate Stream Component Analysis"** —
captures the **composition of a produced oil/condensate stream** (per-component **weight %**) plus the
stream's **reference density** and (for emissions) **carbon wt%**, from laboratory / analyser samples.
It is the **oil/liquid sibling of PO.0020** (gas) and lives in the same **Laboratory → Sample Analysis**
area. Family:
- **PO.0020 Stream Gas Component Analysis** — gas composition, **mol %**, to C6+ (gas export).
- **PO.0019 Stream Oil Component Analysis** — oil/condensate composition, **wt %**, to C8+ (oil to
  storage / oil + condensate export).
- **Well Oil/Condensate Component Analysis** — well-level oil composition.
- **Stream Emission Component Analysis (XEM)** — an *extension* of the gas/oil screen storing carbon wt%,
  density, MolWt + uncertainties for emissions.

## 2. Why it matters (business purpose) — differs from gas
Trigger (per the Pluto/EC use-cases): _"enter the Component Analysis results for Oil streams"_ / _"enter
data after Lab Analysis for Condensate sales."_ Oil composition + density drive:
- **Oil & condensate allocation / to-Storage / Export** quality.
- **Condensate sales** quality (composition + density = the saleable-product spec).
- **Emissions** — carbon wt% + fuel density feed emission factor **EF.010** (liquid-fuel CO2, e.g.
  diesel): `ρfuel` and `fcarbon` are read from Stream Oil Component Analysis.
- **Recombined analysis (XCA)** — **Cn+ density and Cn+ MW** stored here are used to compute the **C7+ GE
  factor** when recombining oil/liquid with gas composition.

## 3. Data model — SHARES the gas view, ANALYSIS_TYPE discriminates
Oil composition lives in the **same view `DV_STRM_COMP_ANALYSIS`** as gas, with
**`ANALYSIS_TYPE = 'STRM_OIL_COMP'`** (gas = `STRM_GAS_COMP`). Per-COMPONENT rows, key
**(OBJECT_ID, DAYTIME, COMPONENT_NO)**. Columns: `MOL_PCT`, **`WT_PCT`**, `MOL_WT`, `DENSITY`,
`RECORD_STATUS`, `COMPONENT_NO`.
- ⚠️ **KEY DIFFERENCE: oil composition is reported/edited in `WT_PCT`, not `MOL_PCT`.** DB recon: every
  sandbox `STRM_OIL_COMP` analysis has **`WT_PCT` populated and `MOL_PCT` NULL** (the inverse of gas). So
  the editable measured cell on PO.0019 is the **wt% column**, not the mol% column gas used.
- Sandbox component set (12): **C1 · C2 · C3 · iC4 · nC4 · iC5 · nC5 · C5+ · C6 · C7+ · CO2 · N2** (heavier
  cuts than gas; the "to C8+" in the BPR doc is the generic-EC description — this Pluto sandbox tops out at
  **C7+**).
- ⚠️ **Sandbox oil-comp data is sparse / synthetic** (e.g. `P1 ALLOC S001 OIL` @ 2023-06-01: 12 comps, all
  wt%≈0.1, sum≈1 — NOT a normalised real composition). Fine for an edit→verify→revert test, but the
  98–102% sum rule would not pass on it (we don't run validations in the suite).

## 4. Config / processing / validations — same family as gas
- **Component Constant (CO.0103)** per-component MW/GCV; **Component Set List** (oil set + order).
- Processing buttons + **Analysis Data Management BPM** (bulk **Wt↔Mol**, **Mol→Energy**, **Normalize** =
  normalise-to-100-then-calc) — identical to gas; for oil the Wt→Mol direction is the natural one (entry is
  wt%).
- Validations: **component sum 98–102%** (rules 1156/1157 family), missing-component, frozen checks; record
  status governance **P → V → A** (the lab-supervisor + production-chemist sign-off from the lineage).

## 5. Lineage (same as gas — see [[LAB-SAMPLE-ANALYSIS-LINEAGE]])
Analysis Point (type=Sample Point) → Sample schedule → SAMPLE_REGISTRATION (Sample Manager) → LAB_ANALYSIS
(per Analysis Template; P→V→A) → ANALYSIS_TARGET distribution → **`STRM_COMP_ANALYSIS` (ANALYSIS_TYPE=
STRM_OIL_COMP)** → Analysis Data Management BPM → oil/condensate allocation + emissions + recombination.

## 6. Automation implications (for Phase 1 recon + Phase 2 build)
- **Expect the SAME screen mechanics as PO.0020** (same layout per the BPR doc → that symmetry is exactly
  why we mirror the PR structure): 8-field navigator (2 dates + PU/Area/Facility/Stream/Analysis Status/
  Sampling Method) → GO **`go_button:form:B`**; grid loads only when Analysis Status + Sampling match the
  analysis; two grids (`analysis:form` header + `component_set:form` component grid).
- **The editable cell is the WT_PCT column** — recon (Phase 1) must DOM-map which `component_set:form:T:{row}:C{n}_in`
  is wt% (gas's mol% was `C1_in`; oil's wt% may be a **different C{n}** — DON'T assume C1). Then the build
  reuses the existing **`component_value_should_be(view, oid, date, component_no, 'WT_PCT', expected)`**
  keyword verbatim (no DbVerify change → no R12 canary expected).
- **Target candidate:** `P1 ALLOC S001 OIL` @ 2023-06-01 (status P, SPOT, 12 comps, wt% populated) — Phase 1
  confirms it loads + picks the editable component; guard a 2nd component for no-normalize-on-save, revert
  to self-clean. Don't click Normalize/Mol→Wt.

## 7. Sources
- ECpedia: BPR *Polar Bear - Component Analysis* (1184137220); XEM *Stream Configuration* / *Emission
  calculations reference* (density + carbon wt% → EF.010); XCA *Recombined Analysis for Well and Stream*
  (Cn+ density/MW → C7+ GE factor).
- DB recon: `tmp/scripts/recon_oilcomp_sme.py`. Companions: `COMPONENT-ANALYSIS-SME.md` (gas, PO.0020),
  `LAB-SAMPLE-ANALYSIS-LINEAGE.md`, local `chemistry.md`.
