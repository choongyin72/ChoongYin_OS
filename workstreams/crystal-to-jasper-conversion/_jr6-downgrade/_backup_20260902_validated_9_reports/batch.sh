#!/bin/sh
# Convert -> compile(6.17.0) -> fill -> verify, for a set of reports.
#
# Each entry is "<report>:<jrxml-stem>:<empty-datasource-records>". The record count must match
# what the 7.x PDF was produced with (read from that report's *Verify.java), otherwise the page
# counts differ and the comparison is meaningless.
D="c:/Projects/ChoongYin_OS/workstreams/crystal-to-jasper-conversion/_jr6-downgrade"
BASE="C:/Projects/INPEX/sources/CrystalReports"

for spec in "$@"; do
    R=$(echo "$spec" | cut -d: -f1)
    STEM=$(echo "$spec" | cut -d: -f2)
    N=$(echo "$spec" | cut -d: -f3)
    echo ""
    echo "################ $R ################"
    mkdir -p "$BASE/$R/output/jr6"

    py "$D/jr7_to_jr6.py" "$BASE/$R/output/$STEM.jrxml" \
        "$BASE/$R/output/jr6/${STEM}_jr6.jrxml" 2>&1 | grep -v -i warning | tail -1 || continue

    if [ -n "$N" ]; then
        sh "$D/jr6build.sh" "$R" fillempty "$N" 2>&1 \
            | grep -v -i 'warning\|note:' | grep -E 'COMPILE|FILL|EXPORT|FAILED|Attribute|cvc-'
    else
        sh "$D/jr6build.sh" "$R" fill 2>&1 \
            | grep -v -i 'warning\|note:' | grep -E 'COMPILE|FILL|EXPORT|FAILED|Attribute|cvc-'
    fi

    py "$D/verify_jr6.py" "$R" --no-image 2>&1 | grep -v -i warning \
        | grep -E 'font families|pages|text spans|drawing rects|RESULT|->'
done
