#!/bin/sh
# Build R07.001's PDF.
#
# Three things that have each cost a wasted run:
#  - cp.txt and target/ live at the REPORT ROOT, not under java/ (java/ holds only src).
#  - `$(cat cp.txt)` inside a compound `cd X && java ...` is expanded BEFORE the cd runs, so
#    it must be read in a separate statement after the cd, as here.
#  - the run must happen in output/, because that is where logo.png sits and the report
#    references it relatively. cp.txt's entries are absolute so only target/classes needs
#    fixing up to an absolute path.
ROOT="C:/Projects/INPEX/sources/CrystalReports/R07.001"
CP="$ROOT/target/classes;$(cat "$ROOT/cp.txt")"
OUT="${1:-_t.pdf}"
cd "$ROOT/output" || exit 1
java -cp "$CP" com.example.reports.R07001Verify \
    "R07_001_Offshore_Daily_Ops_Report.jrxml" "$OUT"
