# SOW — Target Mapping Configuration (IS.0002)

_Backfilled 2026-08-28 (Batch 12 of `docs/lean-deliverable-backfill-workorder.md`) — this bundle
was skipped when the screen was originally built under the 2026-08-23/26 lean-waiver rule (Section G
of `docs/IUD-DELIVERABLE-CHECKLIST.md`), which the owner retired 2026-08-27 (Section H). Original
build: PR #488, merged 2026-08-24T08:21:22Z._

## Screen identity
- **Path:** Configuration > Integration Services > Import > Target Mapping Configuration
- **BF code:** IS.0002
- **Classification:** TV-style read-only grid, bespoke page object — brand-new build, zero prior
  automation existed for this screen before PR #488.
- **DB:** class `IMP_TARGET_MAPPING` (label "Import Target Mapping"), `CLASS_TYPE=OBJECT`,
  `TIME_SCOPE_CODE=INVARIANT` (no version table). Verify view: `OV_IMP_TARGET_MAPPING`.

## Find-only classification — owner-confirmed, NOT a build limitation
The owner directly stated this screen does not support Insert/Update/Delete, despite the toolbar
icons appearing enabled. The original build session's own live, read-only DOM probe independently
confirmed rather than contradicted that claim:
- Insert and Delete toolbar `<li>` both carry class `ui-submenu-state-disabled`.
- There is no Update icon at all (count=0).

No discrepancy was found between the owner's statement and live recon, so the full 5-TC
Insert/Update/Delete suite was intentionally never built. This is a permanent scope decision for
this screen, not a temporary gap to revisit.

## Navigator / grid / cell shape
Non-standard ids on this screen only (do not copy the generic `manage_object.resource`
navigator/GO ids):
- Navigator filters (Class / Attribute / EC Key), none mandatory:
  `StandardNavigator:form:G:0:R:1:C:0:in` / `C:1:in` / `C:2:in`
- GO button: `buttongo:form:B` (NOT `button:form:B` / `go_button:form:B`)
- Grid body: `imp_target_mapping_table:form:T_data` (~20 real rows on the sandbox)
- Grid columns are autocomplete-dropdown cells (`Cn_dd_input`), not plain `<td>` text — the shared
  `table.resource` `Get Table Rows` (textContent-based) returns blank cells here, so the page
  object reads `.value` via JS instead.
- Column order (0-based): 0=Class, 1=Attribute, 2=Ec Key, 3=Class Key 1, 4=Class Key 2 (Class Key
  3-10, Condition 1-3, From/To Unit, Constant String/Number/Date follow, unused by this suite).

## Test data (real, pre-existing row — owner-supplied, live-verified)
| Field | Value |
|---|---|
| Class | `PWEL_DAY_STATUS` |
| Attribute | `AVG_LIQ_VOL` |
| EC Key | `ecValue16` |
| Class Key 1 | `Key 1` |
| Class Key 2 | `Key 2` |

## Dev story (from PR #488's real body)
Built on `feature/target-mapping-configuration-find-only` off `origin/master`. The screen was
brand-new automation with zero prior coverage. Rather than assuming a standard Bank/Area-shaped
IUD build, the session live-reconned first and found the toolbar Insert/Delete `<li>` disabled and
no Update icon present at all — confirming the owner's own statement about this screen ahead of
writing any test code. Result: a reduced-scope, 2-TC (`TC01` clean-load + `TC04` find) suite named
`_find.robot` instead of the tree's usual `_iud.robot` suffix, since the suite never performs an
Insert, Update, or Delete. Live run: 2/2 pass. Full `tests/` tree `--dryrun`: 792/792 pass (both
before and after the live run, no collisions). Robocop clean (0 issues) on both new files. No
self-clean needed in the usual DB sense since nothing is ever inserted — instead a fresh oracledb
connection proved `OV_IMP_TARGET_MAPPING` row count unchanged across the live run (117 → 117, via
`tmp/tmc_rowcount_check.py`). One deviation was flagged in the PR body: the prompt asked for an
isolated sparse-checkout clone under `Workplaces/`, but the build was done directly on the feature
branch in the main worktree instead, matching recent practice on PRs #486/#487 — disclosed rather
than silently diverged.

## Lessons
- Live DOM recon before writing test code caught the Find-only nature independently of the
  owner's statement — the two facts corroborated each other rather than one substituting for the
  other.
- The non-standard navigator/GO ids (`StandardNavigator:form:...`, `buttongo:form:B`) do not match
  the generic manage-object navigator pattern used by most OV/OV-GM screens — this needed its own
  page object rather than reuse of `manage_object.resource`.
