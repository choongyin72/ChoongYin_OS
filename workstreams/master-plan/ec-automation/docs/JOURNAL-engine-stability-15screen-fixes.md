# JOURNAL — feature/engine-stability-15screen-fixes

Branch scope: stability-test the Universal Screen Engine against 60 real EC screens (4 rounds
of 15, no repeats) that already had existing hand-written Playwright/RF drivers, fix any real
engine defects found, and document new EC UI facts discovered along the way.

## What shipped (PR #398)

Three real, `engine_canary.py`-verified fixes to `engine.py`:
1. **`click("Save")` re-queries the grid via GO** after a successful save, matching every
   hand-written driver — fixes a stale-grid gap where `select_row()` could fail right after Insert.
2. **`fill()`'s verification-echo tolerates EC's own numeric auto-formatting** (e.g. typed `1`
   redisplaying as `1.00`) instead of raising a false failure.
3. **`ensure_dialog_in_view()`** — drags an off-screen PrimeFaces popup dialog into view by its
   own title bar (owner-diagnosed; scrolling does not work on these dialogs). Wired into the
   shared `_PopupHandle.pick_by_code()` path.

Plus knowledge-base updates: `ec-ui-knowledge/screens/chemical_stream.md`,
`EC_KNOWLEDGE_BASE.md` (draggable-dialog technique), `EC_KNOWN_ISSUES.md` (EC's generic "Object
not found" banner hides the real `ORA-XXXXX` — check server.log). Two hard rules added to
`CLAUDE.md` from real mistakes made and corrected during this branch (see below).

## Stability test results, 60 screens across 4 rounds

| Round | Screens | Result |
|---|---|---|
| 1 | 15 (Bank/Berth/Canal/Channel/Contract/Driver/Pilot/Port/TugBoat/Truck/Trailer/Property/ChemicalTank/Node/Well) | 15/15 clean after fixing test-harness config gaps (zero engine defects) |
| 2 | 15 (RoyaltyContract/LoadingArm/Storage/InventoryArea/PriceObject/PriceIndex/PriceRate/DocTemplate/DocSequence/ConversionGroup/ConstantStandard/DispositionType/TestDevice/ExternalLocation/ReportArea) | 14/15 clean, Royalty Contract's Delete correctly out-of-scope by design (EC product limitation) |
| 3 | 15 (ActionTrigger/Blend/CalcContext/CalcGroupContext/CalcLibrary/CargoPlanningForecast/ChemInjectionPoint/ChemStreamHookup/ChemicalStream/ChemTransportTank/Choke/ChokeModel/CollectionPoint/ConfigVariable/ContactGroupSet) | 14/15 clean; Chemical Stream's popup timeout led to the `ensure_dialog_in_view()` fix |
| 4 | 15 (ContractAreaSetup/ContractCapacity/ContractInventory/DataExtractSet/DataExtractSetup/DefermentGroup/DivisionOrder/EcCodeObject/FacilityClass1/HcbSystem/InputList/LiftingAccount/MessageGroup/MeterRun/OperatorRoute) | 14/15 clean; Meter Run's numeric-fill false-failure fix, Contract Inventory investigated separately (see below) |

## Two real mistakes made and corrected on this branch (both now hard rules)

1. **Extrapolating test config instead of checking real drivers** (round 1). Guessed
   navigator/field config for 10 screens from the simplest screens' patterns instead of reading
   their own existing `*_iud.py` drivers. Produced a false "10 engine failures" report — the
   engine had zero defects. See `feedback_check_real_driver_before_test_config` +
   `CLAUDE.md`'s NO GUESSING section.

2. **Editing a real production row without verifying row identity** (Contract Inventory, item 2
   of post-hoc investigation). An incomplete 3-level navigator scope left my own test row
   invisible in the grid; `select_row()`'s substring match then selected a real, unrelated
   production object (`TS5_OBA_FO_PEP_INV`) instead. I updated and attempted to delete it without
   checking its Code first, then reported the resulting EC rejection as a screen defect. Recovered
   the real original value from EC's own `CNTR_INVENTORY_VERSION_JN` audit journal (not a guess),
   reverted it, then re-ran the actual task correctly with Code verification before every Save.
   See `feedback_verify_row_identity_before_save` + `CLAUDE.md`.

## Self-clean status

All round 1-4 test codes confirmed clean via fresh DB connections, except the two Royalty
Contract screens' documented permanent residuals (EC product limitation, not fixable) - and
those were subsequently cleared by the owner directly, outside this branch's automation.

## Not covered / left open

- Chemical Stream's popup fix was verified live multiple times but only manually, not folded
  back into a permanent automated regression suite beyond `tmp/stability_test_round3.py`.
- Round 1/2/3/4 stability harnesses live in `tmp/` (scratch, not committed) - useful as a
  reference for a future permanent multi-screen regression suite if one is ever built.
