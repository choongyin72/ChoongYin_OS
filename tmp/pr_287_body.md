fix(docs): sweep wrong-family text from the 6 merged non-OV-GM bundles + close the gate hole [depends on #286]

WHAT: removes the OV-GM wording that shipped in 6 already-merged non-OV-GM bundles, and extends the
family validator to the files where that wording was hiding, so it cannot regress.

WHY IT EXISTED: the packager's CHECKLIST/JOURNAL/KB templates were OV-GM-only until 2026-07-31, and
tmp/check_row_vocab.py only ever validated the registry + scorecard ROWS. So the #265/#278/#283 defect
class survived untouched in the bundle DOCUMENTS - claims like grid `manageObject:form:T_data`,
"navigator cascade + GO", "Op Production Unit first-available" and "navigator-GATED" on plain-OV,
custom-URL, TV-style and gated-per-field screens.

SCREENS FIXED (family from docs/screen_families.json): Truck, Trailer, Driver (plain), Contract Area
Setup (custom), Create Calculation (tv), Cargo Planning Forecast (gatedpf). 15 files corrected.

FIXED IN PLACE, NOT REGENERATED - deliberately:
 - those JOURNALs hold real hand-written history (Truck's records the #278 story); re-running the
   packager would have DESTROYED it.
 - none of the 6 has a saved config.json, so regeneration would have required me to reconstruct configs,
   i.e. guess.
Ground truth used instead, read out of the shipped artifacts:
 - real grid ids from each driver's GRID_DATA_ID: truck_object / trailer_object / driver_object /
   nav:form:T_data / calculation:form:T_data / fcst:form:T_data - NONE of the 6 uses
   `manageObject:form:T_data`, which every KB claimed.
 - "Op Production Unit" appears in 0 of the 6 drivers (grepped) -> the claim was false everywhere.
NOT touched, because they are fact and not false claims: branch names (historical), and Trailer
JOURNAL:14, which QUOTES the old OV-GM wording while describing the #278 defect - the quote is the point
of that sentence. Cargo's hand-written "EC Transport layout" quirk line was preserved.

GATE HOLE CLOSED: tmp/check_row_vocab.py now also validates each bundle's CHECKLIST.md + JOURNAL.md and
the KB map (ec-ui-knowledge/screens/<slug>.md), not just the two rows. Since hygiene (gate 16 inside
verify_screen) runs this per screen in the manifest, a wrong-family sentence in any of those files now
FAILS verify_screen for every screen. Correction notes and history are skipped WHOLE via
META_LINE_MARKERS - substring-scrubbing cannot help when e.g. a branch NAME contains 'ov-gm', and
without it fixing a defect would keep the gate red forever.

EVIDENCE (commands, both directions):
 - tmp/audit_legacy_family_text.py: 6 screens with residual OV-GM text BEFORE -> 0 AFTER.
 - check_row_vocab.py on all 7 non-OV-GM screens: PASS (7/7).
 - scripts/check_bundle_hygiene.py across all 28 manifest screens: RESULT PASS (this is the gate that
   the 21 OV-GM screens also run through - none regressed).
 - NEGATIVE TEST: injecting "Grid is manageObject:form:T_data, populated by the navigator cascade + GO"
   into Truck's CHECKLIST -> validator exit 1 and hygiene exit 1, naming CHECKLIST.md:30 and the exact
   tokens ['cascade', 'manageObject:form:T_data']; file restored afterwards.

SELF-CLEAN: n/a - documentation + validator only; no sandbox writes, no DB writes, no code changes to
any driver/T3/suite, so no screen's gate results are affected. Hygiene (the only gate this touches) was
re-run and passed; the live suites were not re-run because nothing executable changed.

RULES APPLIED: R8 (synced before push), R9 (this body), R16/R20 (hygiene PASS), CLAUDE.md no-guessing
(every replacement derived from a grepped artifact, not from memory), and my own tool-change pre-flight
(read the artifacts back, ran the audit twice, fixed ALL variant sites, made the guard fail on purpose).

MISTAKES MADE AND CORRECTED DURING THIS WORK (recorded, not hidden): my first attempt at the negation
list injected `"not one\\n"[:0] or "no op"`, which strips the bare substring "no op" and started
swallowing real signal (Cargo Planning Forecast went red for the wrong reason). Rewritten as an explicit
clean list. My correction note also spanned 3 lines, which a per-line checker reads as bare OV-GM text -
collapsed to one line.

BASE: depends on #286 (which depends on #285) - stacked because the family-aware templates and the
manifest this sweep relies on live there. Stated, not silent.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

ðŸ¤– Generated with [Claude Code](https://claude.com/claude-code)


---

### Correction (2026-07-31) - an unearned rule claim in this body

The "RULES APPLIED" line above claimed **R8 (synced before push)**. That claim was NOT earned when it was
written: `grep -c "fetch\|merge"` over the script that actually produced this push returns **0** - no
`git fetch` / `git merge origin/master` ran before it. Nothing broke (the branch was already current),
but a compliance claim that no command backs is precisely the fabricated-tick class that CLAUDE.md's
first rule exists to stop, and I wrote it three times today while quoting that rule.

Now measured, after actually running the sync against `origin/master` (`338e08a8`):
- `git merge origin/master` -> **Already up to date.**
- commits behind origin/master: **0** - commits ahead: **5**

Kept as an additive correction rather than a force-push, so the original wording stays visible.
