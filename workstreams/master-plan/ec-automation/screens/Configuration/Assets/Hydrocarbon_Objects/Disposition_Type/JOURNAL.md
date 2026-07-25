# JOURNAL — Disposition Type IUD

_Screen: Configuration > Assets > Hydrocarbon Objects > Disposition Type (CO.0208, OV, date-effective). View `OV_DISPOSITION_TYPE`._
_Branch: feature/disposition-type-iud (stacked on PR #194 for the shared engine). 2026-07-25._

## Built
- **Playwright:** thin driver `py/disposition_type_iud.py` on the shared engine `py/ec_object_iud.py` + `libraries/DbVerify.py` — **zero engine changes** (first reuse-target from the OV tracker).
- **RF:** T3 `pageobjects/.../Hydrocarbon_Objects/disposition_type_page.resource` + suite `tests/.../disposition_type_iud.robot` (reuse T2 `manage_object` + `DbVerify.py`).
- KB map `ec-ui-knowledge/screens/disposition_type.md`.

## Done well
- Full I-U-D DB-verified vs `OV_DISPOSITION_TYPE`: Playwright **7/7** (insert+NAME, update NAME+DESCRIPTION, delete End=Start absent), RF **4/4** (update DB-verified via the new `Field Should Equal In View` keyword). Self-clean 0 residual.
- Recon-first: caught that mandatory fields are at **R2/R3/R4** (R0/R1 are optional Master System Code/Name) — did NOT copy Bank's R0/R1. Engine resolves by label anyway.
- Check-existing gate + hook fired correctly (warned the RF was a sibling of the py driver — same screen, two tools — non-blocking).

## Problems / blockers -> resolution (this session)
1. **Self-inflicted hook block.** The check-existing PreToolUse hook's *wiring* (in local `settings.local.json`) is active on every branch, but the *script* is only committed on PR #194's branch. On a branch off master the script was absent -> the hook command errored -> it **blocked a Write**. The "fail-safe" only covered script logic errors, not a missing script file. Fix: restored the script + **hardened the wiring** with a file-exists guard (`[ -f ] && py ... || exit 0`) so a missing script can never block.
2. **Windows git-bash mangled `git show branch:path`** (`:`->`;`, `/`->`\`). Fix: `MSYS_NO_PATHCONV=1`.
3. **Branch checkout aborted** — an untracked restored hook script would be overwritten. Fix: removed the untracked copy first (target branch has it tracked).
4. **Cross-ref substring bug (caught pre-ship).** The OV-tracker coverage match used substring, so `OV_STREAM` could falsely match `OV_STREAM_CATEGORY`. Caught before persisting; fixed with word-boundary matching (re-ran -> same 36/35, no bad data shipped).
5. **Grid needs GO (recon finding, not a blocker).** Disposition Type's list does not auto-load on open (Bank does) — driver + T3 click GO / `Apply Navigator` after open.
6. **Treeview folder unknown (resolved).** Tree inventory only gave "Configuration"; a flat depth-walk gave a wrong breadcrumb ("Data purging"). Resolved authoritatively from the DB treeview JSON (`TV_CTRL_CONFIGURATION_STORAGE`, screen=CO.0208) -> Configuration > Assets > Hydrocarbon Objects.

No hard blocker stopped the work; Playwright hit 7/7 first try.

## Decisions
- Kept Playwright + RF as the two required tools sharing one `DbVerify.py`. Engine unchanged (plain OV, no mandatory dropdowns).
- Driver lives in `py/` (per the owner's "all py in ec-automation/py" rule); bundle folder holds docs/investigation/evidence.

## Evidence
- Playwright: `evidence/disp_0[1-5]_*.png` (7/7, 2026-07-25).
- RF: `evidence/rf_report.html` + `results/_disp/report.html` (4/4, 2026-07-25).
