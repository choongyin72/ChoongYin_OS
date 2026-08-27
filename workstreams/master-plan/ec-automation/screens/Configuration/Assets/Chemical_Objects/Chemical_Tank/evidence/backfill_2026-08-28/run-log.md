# Chemical Tank — backfill live re-run (2026-08-28)

**Command:**
```
EC_HEADLESS=true robot --outputdir results/_chemtank_backfill tests/Configuration/Assets/Chemical_Objects/chemical_tank_iud.robot
```

**Result:** 5 tests, 5 passed, 0 failed.

```
TC01 Verify Clean State                                               | PASS |
TC02 Insert Chemical Tank Data                                        | PASS |
TC03 Update Chemical Tank Data                                        | PASS |
TC04 Find Chemical Tank Data                                          | PASS |
TC05 Delete Chemical Tank Data                                        | PASS |
```

This is a one-time evidence-capture re-run of the already-proven suite converted in PR #549 —
no automation file was modified to produce this result. Retry policy: none needed (passed on the
first attempt).

Artifacts in this folder: `log.html`, `report.html`, `output.xml` (raw Robot Framework outputs from
the run above).
