# Stream Item - EC Object IUD bundle

**Screen:** Configuration > Assets > Stream_Objects > Stream Item (BF CD.0008). Custom-URL OV
(Manage-Object), date-effective. **INSERT + DELETE only** - Update is out of scope, blocked by an
unconfigured EC scheduler job (`UpdateStreamItem` / BF VO.0031, genuine sandbox config gap, not a code
defect). See `stream_item_sow.md` + `VERIFY-REPORT.md` + `JOURNAL.md` for the full investigation.
Driver `py/stream_item_iud.py`; T3/suite under `Configuration/Assets/Stream_Objects`.
