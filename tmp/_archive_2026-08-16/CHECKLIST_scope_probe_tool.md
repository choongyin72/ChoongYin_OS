# CHECKLIST - scripts/find_populated_scope.py: mechanize the recurring scope-trap lesson

## Why this exists (owner's diagnosis, verified against the actual pattern)
- [x] The SAME "first-available scope may have no real data underneath it" defect recurred on Service
      (contract/transport system saved wrong) and then again on Collection Point (first-available PU's
      cascade children empty). Confirmed by re-reading each park/build record. Message Group's failure was
      investigated in the same period but has a DIFFERENT, still-unresolved root cause (see caveat below)
      - it is not a third instance of this defect, just a related-looking one at the time.
- [x] The only artifact produced after Service was a DOC PARAGRAPH (`ov-gm-navigator-capability.md`) - a
      thing I could read, not a thing that forces me to check. I was about to repeat the live-debug cycle
      again on Collection Point when stopped. Same failure shape as the `check_known_issue.py` lesson,
      recurring in a new area.

## The tool
- [x] `scripts/find_populated_scope.py <VIEW>` - queries the view's OWN rows for the most-used values of
      every candidate scope column, so a nav/dropdown value is chosen from PROVEN data instead of
      "first available". Lives in `scripts/` (keeper), not `tmp/` (scratch).
- [x] Deliberately NOT over-automated: it does not pick a value or resolve CODE->LABEL for you (that step
      genuinely needs a targeted per-class query) - it replaces the AD-HOC DB SCRIPT step of recon with ONE
      reusable, already-tested command. The judgment of which scope to build against stays with the builder.

## Proven against the 2 known scope-population failure cases, in ONE command each
- [x] `OV_SERVICE` -> `CONTRACT_CODE` top `TS3_FIRM2` (10), `TRANSPORT_SYSTEM_CODE` -> `TS3_SYSTEM` (43/43).
- [x] `OV_COLLECTION_POINT` -> `CP_PRODUCTIONUNIT_CODE [('P3_PU',3),('FRMW_PU',1)]`.
- [x] `OV_MESSAGE_GROUP` -> `FUNCTIONAL_AREA_CODE [('EC',2),('MHM13_PROD',2)]` - NOT proof this tool would
      have caught Message Group's failure: `Administration` was already proven a valid, selectable UI
      option (read-only probe, `ov-gm-navigator-capability.md` RESOLVED note); the divergence happens
      server-side at/after Submit, mechanism still unknown. Included here for completeness only.

## Guards tested by making them fail, not assumed to work
- [x] zero-row view: found `OV_TEST_OC_EXT` (0 rows) by sampling -> **exit 1** with the explicit "do not
      default to __FIRST__ and hope" message.
- [x] nonexistent view name -> **exit 2** with a clear "no such view" message.
- [x] sanity-checked on 2 already-shipped screens (`OV_NODE`, `OV_AREA`) - ran clean, no crash, correct
      column exclusion (audit/generic columns filtered out); `OV_AREA` genuinely has both
      `OP_PRODUCTIONUNIT_CODE` and `CP_PRODUCTIONUNIT_CODE` - verified as real schema, not a tool defect,
      by re-running and reading the full untruncated output.

## Documentation (working doc I already own, not a locked governance file)
- [x] Added to `ov-gm-navigator-capability.md` as a MANDATORY pre-build step, with the 3 proof cases quoted
      verbatim so a future me does not have to re-derive why it matters.
- [x] Did NOT touch `CLAUDE.md` or any `*_SOP.md` - those are owner-governance files; this is a working doc
      under `workstreams/master-plan/ec-automation/docs/`, the same file already edited in PR #293 without
      objection.

## Gates
- [x] `check_bundle_hygiene.py` -> RESULT PASS.

## Not yet done (separate decision)
- [ ] Whether to make this step ENFORCED (e.g. wired into the recon skill or a pre-flight script) rather
      than documented-and-mandatory-by-convention. Left as a follow-up rather than bundled here, per
      today's lesson about not scope-creeping a tool PR into a workflow-enforcement PR.
