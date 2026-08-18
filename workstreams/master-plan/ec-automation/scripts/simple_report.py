"""Reformat a Robot Framework output.xml into a compact, single-file HTML report.

The stock report.html/log.html are exhaustive (every internal keyword call, every
library-level detail) - useful for debugging, too much noise for a quick review.
This produces ONE row per test case with just: Test name, a PROCESS FLOW narrative
written in plain business language (hand-written per keyword in FRIENDLY_STEPS
below - e.g. "Inserted a new bank record with the test data" instead of either
the bare technical name "Insert Bank From Properties" OR its raw automation
[Documentation], which is written for engineers and full of jargon/variable
placeholders a non-technical client reader wouldn't follow), the test's
screenshot (embedded inline, base64, so the output is a single portable .html
file), and PASS/FAIL status. A keyword with no FRIENDLY_STEPS entry falls back
to its own [Documentation] (still better than the bare name) so new keywords
never produce a blank line - add a FRIENDLY_STEPS entry for it when convenient.

Uses Robot Framework's own official robot.api.ExecutionResult + ResultVisitor -
the supported way to build custom reports - rather than hand-parsing the XML.

Usage:
    py scripts/simple_report.py <path-to-output.xml> [output.html]

If output.html is omitted, writes simple_report.html next to output.xml.
"""
import base64
import glob
import html
import os
import sys

from robot.api import ExecutionResult, ResultVisitor


# Plain-business-language description per keyword, for a non-technical (e.g. client)
# reader - NOT the automation [Documentation], which targets engineers and is full of
# jargon ("auto-detecting its kind"), variable placeholders (${code}), and file paths.
# "Capture Step" is intentionally absent - it's evidence capture, not a test action,
# and the screenshot column already shows its result.
FRIENDLY_STEPS = {
    # Per-TC top-level steps (bank_iud.robot, owner-requested 2026-08-18 5-line design)
    "Login To EC Application": "Logged in to the EC application.",
    "Open Bank Screen": "Opened the Bank screen.",
    "Verify Bank Record Does Not Exist": "Confirmed the bank record does not already exist in the list.",
    "Insert Bank Record And Save": "Inserted a new bank record with the test data and saved it.",
    "Verify Bank Record Exists": "Confirmed the bank record now appears in the list and was correctly saved to the database.",
    "Update Bank Record And Save": "Updated the bank record's details and saved it.",
    "Verify Bank Record Updated": "Confirmed the updated details now appear in the list and the database.",
    "Find Bank Record": "Found and opened the bank record.",
    "Verify Bank Record Found": "Confirmed the record's grid and full details are correctly shown on screen.",
    "Delete Bank Record And Save": "Deleted the bank record.",
    "Verify Bank Record Removed": "Confirmed the bank record was permanently removed from the list and the database.",
    "Logout From EC Application": "Logged out of the EC application.",
    # Lower-level keywords (kept in case any test calls them directly rather than
    # through the friendly wrappers above)
    "Bank Row Should Not Exist": "Confirmed the bank record is not present in the list.",
    "Bank Row Should Exist": "Confirmed the bank record now appears in the list.",
    "Insert Bank From Properties": "Inserted a new bank record with the test data (Code, Name, Start Date, Description, Swift Code, Address, Country).",
    "Should Be Equal": "Confirmed the result matches what was expected.",
    "Bank Should Exist In DB": "Confirmed the bank record was saved to the database.",
    "Bank Fields Should Equal In DB": "Confirmed the saved record's details match exactly what was entered.",
    "Update Bank From Properties": "Updated the bank record's details with the test data (Name, Description).",
    "Bank Row Should Show Name": "Confirmed the list now shows the updated name.",
    "Find Bank": "Found and opened the bank record.",
    "Bank Row Should Match Properties": "Confirmed the list correctly shows the record's Code, Name, and Start Date.",
    "Bank Form Should Match Properties": "Confirmed the record's full details are correctly shown on screen.",
    "Delete Bank": "Deleted the bank record (ended it on its own start date).",
    "Bank Should Not Exist In DB": "Confirmed the bank record was permanently removed from the database.",
}


def process_flow_step(kw):
    """Return a plain-business-language description of this keyword call.
    Looks up FRIENDLY_STEPS first; falls back to the keyword's own
    [Documentation] (still better than the bare technical name) for anything
    not yet mapped, so a new keyword never produces a blank/robotic line.
    """
    if kw.name in FRIENDLY_STEPS:
        return FRIENDLY_STEPS[kw.name]
    doc = (kw.doc or "").replace("\n", " ").replace("...", "").strip()
    doc = " ".join(doc.split())  # collapse repeated whitespace
    if not doc:
        return kw.name
    if " - " in doc:
        return doc.split(" - ", 1)[0].strip()
    if ". " in doc:
        return doc.split(". ", 1)[0].strip() + "."
    return doc


def find_capture_step_screenshots(test, result_dir):
    # Convention in this suite: "Capture Step    <label>" screenshots to <label>.png in the same
    # directory as output.xml (see resources/utils.resource). Labels use ${TEST NAME} (owner-
    # requested 2026-08-18: one screenshot per business step, e.g. login/open screen/action/
    # verify/logout) so kw.args can't be used to reconstruct the filename - robot.api's Keyword
    # .args reports the UNRESOLVED source text ('${TEST NAME}_login'), not the runtime-resolved
    # value, for EVERY keyword call in this result model, not just this one. Globbing by test
    # name instead sidesteps that entirely: every screenshot for this test starts with
    # "<test.name>_", so glob + sort by file mtime (creation order = execution order) recovers
    # them correctly regardless of how the label was constructed. Empty list if
    # EC_CAPTURE_SCREENSHOTS was off for the run (no .png files exist to find).
    pattern = os.path.join(result_dir, f"{glob.escape(test.name)}_*.png")
    matches = glob.glob(pattern)
    matches.sort(key=os.path.getmtime)
    return matches


def build_rows(result, result_dir):
    rows = []

    class Collector(ResultVisitor):
        def visit_test(self, test):
            top_level = [
                kw for kw in test.body
                if kw.type == kw.KEYWORD and kw.name != "Capture Step"
            ]
            steps = [process_flow_step(kw) for kw in top_level]
            statuses = [kw.status for kw in top_level]
            rows.append({
                "name": test.name,
                "status": test.status,
                "steps": steps,
                "step_statuses": statuses,
                "screenshots": find_capture_step_screenshots(test, result_dir),
            })

    result.visit(Collector())
    return rows


def screenshot_link(path):
    if not path:
        return "<em>(no screenshot)</em>"
    # Relative to the report file (both live in the same result_dir), so the link keeps
    # working as long as the .html and the .png files are moved/copied together.
    return f'<a href="{html.escape(os.path.basename(path))}" target="_blank">View</a>'


def render_html(rows, suite_name):
    parts = [
        "<html><head><meta charset='utf-8'>",
        f"<title>{html.escape(suite_name)} - Simple Report</title>",
        "<style>",
        "body{font-family:Segoe UI,Arial,sans-serif;margin:24px}",
        "table{border-collapse:collapse;width:100%}",
        "th,td{border:1px solid #ccc;padding:8px;vertical-align:top;text-align:left}",
        "th{background:#f0f0f0}",
        ".center{text-align:center}",
        ".PASS{color:#2e7d32;font-weight:bold}",
        ".FAIL{color:#c62828;font-weight:bold}",
        ".test-name{font-weight:bold;background:#fafafa}",
        "</style></head><body>",
        f"<h2>{html.escape(suite_name)} - Simple Test Report</h2>",
        "<table>",
        "<tr><th>Test Name</th><th>#</th><th>Process Flow</th><th class='center'>Screenshot</th><th class='center'>Status</th></tr>",
    ]
    for row in rows:
        n_steps = len(row["steps"])
        for i in range(n_steps):
            shot = row["screenshots"][i] if i < len(row["screenshots"]) else None
            status = row["step_statuses"][i]
            parts.append("<tr>")
            if i == 0:
                # Test name spans every step-row for this test (rowspan), so each step still
                # gets its OWN <tr> (own border line) instead of being nested inside one cell.
                parts.append(f"<td class='test-name' rowspan='{n_steps}'>{html.escape(row['name'])}</td>")
            parts.append(f"<td>{i + 1}</td>")
            parts.append(f"<td>{html.escape(row['steps'][i])}</td>")
            parts.append(f"<td class='center'>{screenshot_link(shot)}</td>")
            parts.append(f"<td class='center {status}'>{status}</td>")
            parts.append("</tr>")
    parts.append("</table></body></html>")
    return "\n".join(parts)


def main():
    if len(sys.argv) < 2:
        print("Usage: py scripts/simple_report.py <path-to-output.xml> [output.html]")
        sys.exit(1)

    output_xml = sys.argv[1]
    result_dir = os.path.dirname(os.path.abspath(output_xml))
    out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(result_dir, "simple_report.html")

    result = ExecutionResult(output_xml)
    result.configure(stat_config={"suite_stat_level": 2})
    rows = build_rows(result, result_dir)
    suite_name = result.suite.name

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(render_html(rows, suite_name))

    print(f"Wrote {out_path} ({len(rows)} test(s))")


if __name__ == "__main__":
    main()
