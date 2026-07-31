# JOURNAL - Driver (CO.0266) plain-OV IUD

## 2026-07-31
- **Branch:** `feature/driver-iud`. Group A #7, completing the Truck/Trailer/Driver cluster.
- **Recon (executed):** empty navigator (GO only), custom grid `driver_object:form:T_data`, view
  OV_DRIVER = 0 rows. Registry-first check confirmed Driver was genuinely unbuilt.
- **EC's save message beat the yellow-cell scan again:** the scan flagged only Code/Name/Start Date +
  Gender, but the save was rejected with "Required fields are empty: Driver Licence No
  [DRIVER_LICENCE_NUMBER]" - that field renders WHITE. Added it; 8/8 immediately. This is the second
  screen (after Truck) where EC's rejection message was the reliable field spec.
- All 5 verify gates PASS. Vocabulary validator (issue #278) clean on both rows - the family-aware
  registry AND scorecard templates now emit correct plain-OV text with no manual correction.

## Lessons
- Treat the yellow-cell heuristic as a HINT and EC's save-time rejection as the SPEC: two of three
  plain-OV screens in this cluster had a mandatory field that rendered white.
