#!/bin/sh
# Compile / fill / package a downgraded JRXML with JasperReports 6.17.0.
#
#   jr6build.sh <report> compile                 validate against the 6.x XSD
#   jr6build.sh <report> fill                    compile + fill from the local Oracle -> jr6/*.pdf
#   jr6build.sh <report> jasper                  produce the deployable jr6/*.jasper
#
# e.g. jr6build.sh R07.012 fill
#
# Two things that are load-bearing:
#  - the Arial font EXTENSION must be on the classpath, or 6.x resolves fontName="Arial" to
#    nothing, falls back to Helvetica, and SILENTLY ignores isBold/isItalic (README "two traps")
#  - the run happens in output/, so a relative logo.png resolves during fill
D="c:/Projects/ChoongYin_OS/workstreams/crystal-to-jasper-conversion/_jr6-downgrade"
REPORT="$1"
MODE="$2"
if [ -z "$REPORT" ] || [ -z "$MODE" ]; then
    echo "usage: jr6build.sh <report> compile|fill|jasper    e.g. jr6build.sh R07.012 fill"
    exit 2
fi

OUT="C:/Projects/INPEX/sources/CrystalReports/$REPORT/output"
JRXML=$(ls "$OUT/jr6/"*_jr6.jrxml 2>/dev/null | head -1)
if [ -z "$JRXML" ]; then
    echo "no converted JRXML in $OUT/jr6/ - run jr7_to_jr6.py first"
    exit 1
fi
STEM=$(basename "$JRXML" .jrxml)

FONTS="$OUT/fonts/inpex-arial-fonts.jar"
[ -f "$FONTS" ] || FONTS="C:/Projects/INPEX/sources/CrystalReports/R07.001/output/fonts/inpex-arial-fonts.jar"
CP="$D/jr6170-lib/*;$FONTS;$D/classes"

mkdir -p "$D/classes"
javac -cp "$D/jr6170-lib/*" -d "$D/classes" "$D/Jr6Build.java" || exit 1

cd "$OUT" || exit 1
case "$MODE" in
    compile)   java -cp "$CP" Jr6Build compile "jr6/$STEM.jrxml" ;;
    fill)      java -cp "$CP" Jr6Build fill    "jr6/$STEM.jrxml" "jr6/$STEM.pdf" ;;
    jasper)    java -cp "$CP" Jr6Build jasper  "jr6/$STEM.jrxml" "jr6/$STEM.jasper" ;;
    # fillempty needs the SAME record count the 7.x PDF was built with, else page counts differ
    fillempty) java -cp "$CP" Jr6Build fillempty "jr6/$STEM.jrxml" "jr6/$STEM.pdf" "${3:-1}" ;;
    *) echo "unknown mode: $MODE"; exit 2 ;;
esac
