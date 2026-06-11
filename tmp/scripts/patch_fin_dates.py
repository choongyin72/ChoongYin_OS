"""Add per-screen test-date overrides to both Financial Objects generators:
reference dropdowns are EFFECTIVE-DATE-FILTERED, so Bank Account and Cost
Object Mapping need Start Date 2003-01-01 (seed customers/cost objects start
then) - user-explained 2026-06-12."""
from pathlib import Path

ADD = '''# per-screen test dates: reference dropdowns are EFFECTIVE-DATE-FILTERED, so the
# form Start Date must postdate the referenced seed objects (customers/cost
# objects start 2003-01-01) - user-explained 2026-06-12
SCREEN_DATES = {"Bank Account": "2003-01-01", "Cost Object Mapping": "2003-01-01"}

'''

for fp, anchor in [
    (r"c:/Projects/ChoongYin_OS/tmp/scripts/generate_financial_objects.py",
     "# mandatory reference DROPDOWNS"),
    (r"c:/Projects/ChoongYin_OS/tmp/scripts/generate_financial_objects_bundles.py",
     "# mandatory reference dropdowns"),
]:
    p = Path(fp)
    src = p.read_text(encoding="utf-8")
    if "SCREEN_DATES" not in src:
        src = src.replace(anchor, ADD + anchor, 1)
    src = src.replace("${{START_DATE}}       2000-01-01", "${{START_DATE}}       {start_date}")
    src = src.replace("${{END_DATE}}         2000-01-01", "${{END_DATE}}         {start_date}")
    src = src.replace('"start_date": "2000-01-01",', '"start_date": "{start_date}",')
    src = src.replace('"end_date": "2000-01-01",', '"end_date": "{start_date}",')
    src = src.replace("Start=End `2000-01-01`", "Start=End `{start_date}`")
    src = src.replace("ctx = dict(label=label, slug=slug, UP=up,",
                      'ctx = dict(start_date=SCREEN_DATES.get(label, "2000-01-01"), label=label, slug=slug, UP=up,')
    src = src.replace("ctx = dict(label=label, slug=slug,",
                      'ctx = dict(start_date=SCREEN_DATES.get(label, "2000-01-01"), label=label, slug=slug,')
    p.write_text(src, encoding="utf-8")
    print("patched", p.name)
