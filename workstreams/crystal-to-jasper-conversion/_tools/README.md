# `_tools` — generation and verification for the INPEX report conversion

Promoted out of `tmp/` on 2026-09-06 at the owner's instruction ("do keep this kind of py code"),
because these are the scripts worth re-running rather than one-off scratch work.

All are **read-only unless given `--apply`**, and all print a full report before changing anything.

## The pattern worth keeping

`verify_r10_sql.py` is the one to copy when writing a new check. Every earlier verification on
this project asked *"does the output contain the things I expect?"* — which only ever finds what
you thought to look for. It is how a whole `P_REPORT_DATE` registration block went missing from
38 generated files and had to be caught by the owner instead of by me: I checked for `JRXML` and
`FORMAT`, found them, and reported success.

The fix is to ask the opposite question — *"did anything at all change that shouldn't have?"* —
by normalising away the few things that are **meant** to differ and diffing the WHOLE file
against its template:

```python
def norm(path, code, stem):
    t = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    return t.replace(code, "<CODE>").replace(stem, "<STEM>")

assert norm(generated, "R10_001_JCC_PRICE_6_17", "R10_001_JCC_Price_Calculation") == \
       norm(template,  "R07_016_PC_LIFTING_6_17", "R07_016_PC_Lifting_Report")
```

Any omission, reordering or stray edit shows up, including ones nobody predicted. The same shape
appears in `r07_workspace_drift.py` and `r10_deploy_drift.py`, which normalise away a generated
header comment and compare the rest.

## Contents

| script | what it does |
|---|---|
| `gen_r10_report_sql.py` | Generates the 38 R10 EC registration scripts from the `R07_016_PC_LIFTING` pair. Enforces the 32-char `TEMPLATE_CODE` cap, rejects duplicate codes, and refuses to write if anything from the template leaks through. |
| `gen_load_all_r10.py` | Builds `LOAD_ALL_R10.sql` from the files actually on disk; aborts if a pair is incomplete or any `@@` target is missing. |
| `verify_r10_sql.py` | The whole-file template diff, plus code cap, registered parameters, and artifact existence. **Run after any regeneration.** |
| `sql_reg_audit.py` | Audits every 6.17/V7 registration pair: does the 6.17 script point at a `_6_17` artifact, do both halves point at the same file, do the artifacts exist. Found the R07.012 defect. |
| `r10_deploy_drift.py` | Are the artifacts in the EC extension folder still what we produce today? |
| `r07_workspace_drift.py` | Do the Studio workspace copies match current converter output? Run after ANY change to `jr7_to_jr6.py`. |
| `logo_std_audit.py` | The logo contract across R07 + R10: `P_BASE_URL` default, `$P{}` vs `$F{}`, filename, box aspect. |
| `r10_logo_std.py` | Brings R10 JRXMLs onto that contract. |

## Two facts these encode

**`TEMPLATE_CODE` is capped at 32 characters, and the `_6_17` suffix is part of it** — not just
part of the filename or the artifact path. Size against `<BASE>_6_17`, the longer of the pair.

**The two registrations of a report must carry DIFFERENT codes.** Each script opens with a
`DELETE` block keyed on its own code; with one shared code they delete each other and only the
last one loaded survives. That is the actual defect in the hand-written `R07_012_FC_LIFT` pair,
which also points its 6.17 half at the V7 artifact.

## Not promoted

`r10_audit.py` and the `r10_034_*` scripts stay in `tmp/` — they invoke their sibling `r10_*.py`
passes by path and only work alongside them.
