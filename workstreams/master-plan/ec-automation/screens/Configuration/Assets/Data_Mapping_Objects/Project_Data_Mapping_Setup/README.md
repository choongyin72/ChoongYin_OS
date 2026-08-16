# Project Data Mapping Setup - Universal Screen Engine IUD bundle

**Screen:** Configuration > Assets > Data_Mapping_Objects > Project Data Mapping Setup (BF SP.0039,
class `COST_MAPPING`). OV, NONSTANDARD navigator (`StandardNavigator:form:...`, real GO =
`buttongo:form:B` - not the usual `nav:form:...` prefix), date-effective. Built via the engine
(`engine.py`) as Phase 4 Pilot 3 - by far the deepest pilot, see `project_data_mapping_setup_sow.md`
and `docs/universal_screen_engine_design.md` "Pilot 3" section for the full build narrative
(cross-screen master-data dependency chain, several real engine bugs found and fixed).

**Run:** `EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/project_data_mapping_setup_iud.py`
