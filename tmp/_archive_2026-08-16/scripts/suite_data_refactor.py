"""Data/variable refactor across IUD test suites.

1. Date literals in *** Variables *** -> central constants from environment.py:
     ${START_DATE}  2000-01-01 -> ${TEST_START_DATE}
     ${START_DATE}  2003-01-01 -> ${TEST_START_DATE_REFDD}
     (same for ${END_DATE})
   ONLY for vars named START_DATE / END_DATE - data-anchored dates in Validation
   evidence suites (2026-05-26 etc.) are untouched.

2. Bank/Equipment naming outliers: ${BANK_NAME}/${EQP_NAME} -> ${OBJ_NAME} (suite-local).

3. Suite Setup boilerplate -> Prepare IUD Object Data:
     ${code}    Generate Unique Code    <PREFIX>
     VAR    ${TEST_CODE}    ${code}    scope=SUITE
     VAR    ${OBJ_NAME}    <Label> ${code}    scope=SUITE
     VAR    ${OBJ_NAME_UPD}    <Label> ${code} UPD    scope=SUITE
   -> Prepare IUD Object Data    <PREFIX>    <Label>
   Only the EXACT pattern is rewritten; anything custom is left and reported.
"""
import re
from pathlib import Path

TESTS = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/tests")

DATE_RULES = [
    (re.compile(r"^(\$\{(?:START|END)_DATE\}\s{2,})2000-01-01\s*$", re.M), r"\g<1>${TEST_START_DATE}"),
    (re.compile(r"^(\$\{(?:START|END)_DATE\}\s{2,})2003-01-01\s*$", re.M), r"\g<1>${TEST_START_DATE_REFDD}"),
]

SETUP_PAT = re.compile(
    r"    \$\{code\}[=]?\s{2,}Generate Unique Code\s{2,}(\S+)\n"
    r"    VAR    \$\{TEST_CODE\}    \$\{code\}    scope=SUITE\n"
    r"    VAR    \$\{OBJ_NAME\}    (.+?) \$\{code\}    scope=SUITE\n"
    r"    VAR    \$\{OBJ_NAME_UPD\}    \2 \$\{code\} UPD    scope=SUITE\n")

report = {"dates": [], "renamed": [], "setup": [], "setup_miss": []}

for f in sorted(TESTS.rglob("*.robot")):
    rel = str(f.relative_to(TESTS))
    text = orig = f.read_text(encoding="utf-8")

    n_dates = 0
    for pat, repl in DATE_RULES:
        text, n = pat.subn(repl, text)
        n_dates += n
    if n_dates:
        report["dates"].append((rel, n_dates))

    for old in ("BANK_NAME", "EQP_NAME"):
        if "${" + old + "}" in text:
            text = text.replace("${" + old + "_UPD}", "${OBJ_NAME_UPD}")
            text = text.replace("${" + old + "}", "${OBJ_NAME}")
            report["renamed"].append((rel, old))

    new, n = SETUP_PAT.subn(lambda m: f"    Prepare IUD Object Data    {m.group(1)}    {m.group(2)}\n", text)
    if n:
        text = new
        report["setup"].append(rel)
    elif "Generate Unique Code" in text:
        report["setup_miss"].append(rel)

    if text != orig:
        f.write_text(text, encoding="utf-8")

print(f"date literals centralized in {len(report['dates'])} suites")
print(f"naming standardized: {report['renamed']}")
print(f"setup boilerplate collapsed in {len(report['setup'])} suites")
print("\nsuites with Generate Unique Code NOT matching the canonical setup pattern:")
for rel in report["setup_miss"]:
    print(f"  !! {rel}")
