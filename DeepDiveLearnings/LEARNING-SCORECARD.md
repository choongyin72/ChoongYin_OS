# Learning Scorecard — Choong Yin + Claude, growing up together
**Purpose:** turn "am I making progress?" from a *feeling* into a *number*. Updated once per
working session. Measures capability against GROUND TRUTH, not hours spent. Two people, one team:
**Claude produces; Choong Yin judges, supplies domain truth, and verifies — the judge is
accountable for what ships.** (Origin: 2026-06-13, after the Sheng Tong habit-coaching chat.)

## How to read this
- **Coverage %** — what fraction of the in-scope work is automated + DB-verified (not just "tried").
- **Autonomy rungs** — per area: **A** = Claude does it unaided & verified · **B** = needs one
  hint / domain fact · **C** = not yet / blocked. Goal is to move areas C→B→A.
- **Calibration** — how often "Claude is confident" == "actually correct". The whole point of the
  human-as-judge model. Low-calibration days are logged honestly; that's the metric working.

---
## 1. EC automation coverage (anchored to ec_screen_registry.md + coverage_pluto_prioritized.md)
| Layer | Pattern types | State | Rung |
|---|---|---|---|
| Master data (Basic/Financial/Commercial/Dispatching/System objects) | OV, OV-GM, TV, PC | ~50 screens automated, live + DB-verified | **A** |
| Validation run | RUN-verify (Validation Overview) | automated + DB-verified | **A** |
| Daily/Monthly STATUS grids (N1) | N1 edit-in-place | ✅ SOLVED + GENERALIZES — TWO screens live 3/3 DB-verified self-cleaning: WR.0001 (PWEL_DAY_STATUS) + PO.0002 (STRM_DAY_STREAM); T2 reuses, save gesture transfers | **A** |
| Allocation / calc runs (N2) | RUN-verify ext. | designed, not built (sandbox scheduler dependency) | **C** |
| Status processes P→V→A (N3) | — | studied, not built | **C** |

**Rough coverage of the Pluto transactional value:** master-data foundation ≈ done; the
operational core (N1/N2/N3 — where PHD data + validations + allocation live) ≈ **just opened
(~1 screen in recon/build, 0 fully closed).** Honest headline: **foundation strong, operational
core barely started.** Next single highest-value unlock = the N1 commit gesture (headed).

## 2. Domain knowledge (generic EC + Pluto As-Built)
| Area | State | Rung |
|---|---|---|
| EC web internals (JSF/PrimeFaces id grammar, screen types, gestures) | field guide written | **A** |
| Pluto As-Built series (02/05/06/07/09/11/14) | synthesized; only 01/03 xlsx left | **A−** |
| Allocation / emissions / PRRT business chain | mapped end-to-end (capstone) | **B** |
| ECIS Excel upload | built once end-to-end; set aside | **B** |
| Issue_1052 validations | rules pinned to As-Built 09 | **B** |

## 3. Calibration log (honest — confident vs ground truth)
| Date | Claimed | Reality | Lesson |
|---|---|---|---|
| 2026-06-13 | "N1 cell↔column mapping confirmed" | WRONG — based on one coincidental value match (24==24) | one matching value ≠ a mapping proof; verify by edit→commit→diff |
| 2026-06-13 | "N1 toolbar Save should commit" (×14 attempts) | did NOT persist; SME confirmed Save IS correct → my gesture bug | exhaust reasoning (good) but a real-save *observation* would've been faster than 14 blind tries |
| 2026-06-13 | repeatedly "checkpointed"/asked instead of continuing | user had to redirect 3× | bias to action; only stop for genuine forks/blockers, not status posture |
| 2026-06-13 | "master-data layer is rung-A solid" | RIGHT — live headed demo of Nomination Cycle IUD passed 4/4, DB-verified each step, self-cleaning (zero residue) | confident-and-right; the foundation claim holds under live proof. N1 is this minus one save gesture. |
| 2026-06-13 | N1 write gesture (after 14 fails) | SOLVED — a HEADED capture of the user's real save revealed it (change-event stages + menubar @all commits); automated replica DB-verified 24→22→24; suite now live 3/3 | the keystone moment: the human did in 1 try what I failed 14×; observation > blind iteration. New rung: N1 = A. |
| 2026-06-13 | N2 allocation run "blocked by Process Automation" | WRONG ×2 — the run works via a "RUN CALCULATIONS" button (synchronous, not BPM); jobs execute in 1-2s. I over-concluded from a red-herring toolbar flag + not reading the log_list grid | don't infer an environmental block from one UI flag; read the actual result table. (SME corrected; then I found it.) |
| 2026-06-13 | N2 allocation calc itself | runs but EXIT=Failure (equation errors) on P1/2021-10-01 — real finding, not a block | the engine runs; the specific allocation errors (missing input/config). Use Simulate to iterate safely. |
| (next session…) | | | |

## 4. Update protocol (the habit)
At the end of each working session, append: (a) any coverage rung change, (b) one calibration-log
row (where was I confident-but-wrong, or confident-and-right?), (c) the single highest-value next
unlock. Keep it to ~5 minutes. **What gets measured is what we'll keep doing.**

## 5. Standing reminders for the human (the judge's job)
- Set explicit success criteria up front ("keep going until X / done = Y DB-verified") so Claude
  doesn't default to checkpointing.
- Before asking Claude a question, form your own answer first — that's how you build the judgment
  to catch Claude's confident errors (see calibration log: they happen regularly).
- The value isn't out-typing the AI; it's verifying ground truth + supplying domain knowledge the
  AI cannot derive (e.g. the one-sentence Save answer that beat 14 of Claude's attempts).
