# IUD Task — Deliverable Checklist (definition of done)

**Single source of truth for what an EC Object IUD task must deliver.** Both sides use this:
- **Worker:** copy this list into the screen bundle as `CHECKLIST.md`, tick every item with evidence, and raise the PR **only when all items are green**.
- **Reviewer:** verify the PR against this list. **ALL 19 items are HARD GATES** — any missing or failing item ⇒ **MUST-FIX: do NOT approve/merge, leave the PR open, post a note-back listing the exact gaps** (template below), re-review next run.

_Locked 2026-06-28 (owner): all items are hard gates — no NICE-TO-HAVE exceptions._
_Updated 2026-07-25: added Step 0 (check-existing gate) + items 20–21 (KB MD map, reuse clause) after the
Bank Account gap — a screen had passing tests but was missing its KB map + JOURNAL, so "Done" was declared
too shallow. Count is now 21 hard gates._

---

## Step 0. CHECK-EXISTING-FIRST GATE (before building anything — not optional)
- [ ] **0a.** Read `ec-ui-knowledge/screens/<screen>.md` if it exists (use its selectors; don't re-scan).
- [ ] **0b.** `grep -ril "<screen-slug>" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → **found ⇒ REUSE/EXTEND, never build a parallel copy** (the Bank 3rd-stack mistake). State "existing impl: `<path>` / none" in the plan.
- [ ] **0c.** Prefer the shared engine over new code: `py/ec_object_iud.py` (OV IUD) + `libraries/DbVerify.py` (single DB-verify). A new OV screen = a thin driver (copy `py/bank_iud.py`, swap config), not new plumbing.

## A. Bundle artifacts — `screens/<menu path>/<Screen>/`
- [ ] **1. `<screen>_sow.md`** — SOW: classification (type/pattern), nav/grid/cells, test data, dev story, lessons.
- [ ] **2. `README.md`** — bundle overview + exact run commands.
- [ ] **3. `JOURNAL.md`** — per-branch work journal (built / done-wrong / done-well / improve / blockers→resolution / decisions / evidence).
- [ ] **4. `playwright/ec_iud_<slug>.py`** — standalone Playwright reference flow (env-var creds, ASCII-clean).
- [ ] **5. `investigation/`** — the read-only recon + pre-flight scripts (resolve, scan, DB pre-checks).
- [ ] **6. `evidence/`** — step screenshots + `results.json` from a real run.
- [ ] **7. `CHECKLIST.md`** — this list, copied into the bundle, all items ticked with evidence.

## B. RF files — treeview-mirrored (reuse T1/T2; no shared-file edits unless justified + canaried)
- [ ] **8. T3 page object** `pageobjects/<menu path>/<screen>_page.resource` (locators in Variables; docstring matches Variables — R7).
- [ ] **9. Suite** `tests/<menu path>/<screen>_iud.robot` — TC structure clean → insert → update → delete → cleanup.

## C. Verification gates (record the evidence in CHECKLIST + the PR body)
> **These ticks are NOT hand-typed.** Run `py scripts/verify_screen.py --name … --t3 … --suite … --driver … --out <bundle>/VERIFY-REPORT.md`
> — it RUNS robocop + hygiene + dryrun + live suite + driver and emits the ticks from real exit codes. It must print
> `OVERALL: PASS` before the PR. Ticking a gate the verifier did not pass = hard violation (CLAUDE.md 'NO GUESSING').
- [ ] **10. robocop clean** (the new T3 + suite).
- [ ] **11. `--dryrun` N/N PASS** (suite).
- [ ] **12. LIVE headed run N/N PASS** — the proof (`EC_HEADLESS=false`).
- [ ] **13. DB ground-truth** — the **exact DbVerify assertion** cited, and each op verified at DB level (insert/update/delete).
- [ ] **14. FULL I-U-D scope** — Insert **+ Update +** Delete all present (not I/D only — the RC.0050 lesson).
- [ ] **15. Self-clean confirmed** — independent DB re-read = 0 residual; any pre-existing rows verified intact.
- [ ] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (R16 env-creds, R20 ASCII in `playwright/*.py` + `investigation/*.py`).

## D. Delivery
- [ ] **17. Registry row** appended to `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` (append-only, R23).
- [ ] **18. Scorecard row** appended to `docs/automation-scorecard.md` (append-only, R23).
- [ ] **19. PR** with the R9 6-field body (What / Files / DB ground-truth evidence / Self-clean / Rules applied / Base branch); R8 sync first; **never self-merge**.

## E. Knowledge base (added 2026-07-25 — MD-only, tool-agnostic)
- [ ] **20. KB selector map** `ec-ui-knowledge/screens/<screen>.md` — nav path, DB view, grid id, insert/update/delete
      selectors, mandatory-yellow fields, quirks, last-verified date + EC version/env. Serves BOTH Playwright & RF
      (it's the single selector reference; code files cite it). `ec-ui-knowledge/` holds MD only — no code.
- [ ] **21. Reuse clause.** If Step 0 finds the screen ALREADY implemented, a "reuse run" is NOT done at green
      tests alone — it must still produce/refresh the deliverables that document it: **#3 JOURNAL**, **#6 evidence**,
      and **#20 KB map**. "Done" = tests + KB MD + JOURNAL + evidence, never just passing tests.

---

## Reviewer gate (how to enforce)
1. Open the bundle's `CHECKLIST.md` + diff; verify each of the 19 against the artifacts/evidence in the PR.
2. Spot-check the substance (not just the tick): item 12 has a real N/N; item 13's DbVerify assertion is real; item 16 reproduces PASS; items 17/18 are 0-deletion appends (R23).
3. **Any gap ⇒ MUST-FIX, do not merge, post the note-back** (below). Re-review next run after the worker pushes fixes to the same branch.

### Note-back template (reviewer → worker)
> ⛔ **IUD deliverable-checklist gate — MUST-FIX (PR not approved).**
> Missing/failing items vs `docs/IUD-DELIVERABLE-CHECKLIST.md`:
> - [ ] **#N** — `<item>` — `<what's missing / which evidence>`
> - [ ] **#M** — `<item>` — `<...>`
> Complete these, tick them in the bundle `CHECKLIST.md`, and push to this branch. Re-review next run. No code change needed for doc-only gaps.

---

## F. Engine-only bundle variant (owner-approved 2026-08-16, PR #379)

For a screen built via the Universal Screen Engine (`workstreams/master-plan/ec-automation/py/engine.py`)
where an RF T3/suite has not yet been built, items **8, 9** (RF T3/suite) and their dependent gates
**10, 11, 12** (robocop-on-RF, `--dryrun`, live RF suite) may be **explicitly deferred** rather than
built or faked as passing - this is a reduced-but-honest shape, not silently equivalent to full "Done."

**How the deferral must be recorded (all of these, not a subset):**
- [ ] **8/9** in `CHECKLIST.md` stay unticked, each with a one-line reason (e.g. "screen built via
      engine.py, not the classic T2/T3 pattern - will revisit once RF can call the engine directly").
- [ ] **10/11/12** in `CHECKLIST.md` and `VERIFY-REPORT.md` stay unticked, marked N/A with the same
      reason - never ticked from a partial or assumed run.
- `VERIFY-REPORT.md` is **hand-assembled** (since `scripts/verify_screen.py` requires `--t3`/`--suite`
      and cannot run without RF files) - it must self-declare this plainly at the top, cite the exact
      command + exit code for every tick it DOES make (Playwright driver, hygiene, DB ground-truth,
      full I-U-D, self-clean), and state **OVERALL: PARTIAL PASS** - never a bare "PASS" implying gates
      that didn't run.
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows say
      **"OK Done (engine-only bundle)"**, not a bare "OK Done" - with the RF deferral called out in the
      row text, not just implied by reading the linked bundle.
- Items 4-7 (playwright driver + delegator, investigation/, evidence/, this CHECKLIST) and 13-21
      (DB ground-truth, full I-U-D, self-clean, hygiene, delivery, KB) are **NOT reduced** by this
      variant - they still apply in full, backed by real evidence, same as any other screen.

**When this variant does NOT apply:** a screen with an existing RF suite that's merely out of date,
a screen where building the RF layer is trivial (reusing an already-proven T2 pattern with no new
gestures), or a screen the owner has not explicitly approved for this treatment. Defaulting to this
variant to avoid RF work is exactly the shortcut this checklist exists to prevent - use it only when
the owner has approved it for that specific screen, as was done for Financial Item Definition/Template.

This variant does not replace or loosen items A-E for any screen NOT explicitly approved for it.

---

## G. Owner-approved variant: lean RF-only build for brand-new Bank-shaped screens (2026-08-23)

_Owner decision 2026-08-23 (recorded by the reviewer at the merge of PR #481): a BRAND-NEW EC screen
whose layout matches Bank (plain manage-object OV / custom-URL OV, no mandatory navigator cascade)
MAY be delivered as the lean RF-only shape defined in
`.claude/skills/ec-bank-pattern-new-screen/SKILL.md` - RF page object + 5-TC suite + 4 properties
files + registry/scorecard rows, verified by the 5-step gate (robocop parity, full-tree dryrun,
live 5/5, fresh-connection DB self-clean, filter-fired grep)._

**What this variant waives for such screens:** the SOW, Playwright bundle + investigation/,
JOURNAL, evidence screenshots, KB MD map, and the `verify_screen.py` gate (items 1, 3, 4, 5, and
the KB items of the 21-item list). It does NOT waive: live 5/5 with real cited output, DB
ground-truth + self-clean via a fresh connection, hygiene (R16/R20), registry/scorecard rows,
the 6-field PR body, or never-self-merge.

**When it does NOT apply:** a screen that is not Bank-shaped (needs the full 21-item treatment via
`ec-object-iud-builder`), a screen with ANY existing automation (that is `ec-bank-pattern-converter`
territory - upgrade, don't duplicate), or any case where the owner asks for the full deliverable.
This section exists so a reviewer does not MUST-FIX a lean-built new screen against items this
variant waives; sections A-F are otherwise unchanged.
