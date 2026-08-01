"""Generic pre-flight mandatory-field gate. STANDALONE - imports nothing from ec_object_iud.py and does
not modify it; a driver opts in by importing this module alongside the shared engine.

WHY THIS EXISTS: today's safety net is REACTIVE, not proactive - EC's own Save-time error banner
("Required fields are empty. Please enter data for these fields: ...") tells you what you missed only
AFTER you click. That cost a live-run failure + diagnosis cycle multiple times this session (Message
Group, Service, Collection Point, Contract Capacity all had cascades that added a NEW mandatory field
only after an earlier one was set - a class of gap a one-time hand-run scan can miss).

WHAT THIS DOES: before ever clicking GO or Save, scan for MANDATORY-AND-EMPTY fields under a given DOM
scope (navigator, objectForm, updateAttributes, or a TV-style grid), using the SAME yellow-background
rule ('rgb(252, 249, 192)') that EC itself uses to mark a field mandatory - and if any are found, raise
with the EXACT field list before the click happens, instead of after.

This is deliberately additive/opt-in: it does not touch or wrap click_go()/save()/insertObjectRecord() in
the shared engine, so every already-shipped screen (18+) is completely unaffected. A driver calls
assert_no_empty_mandatory() explicitly, at the point it chooses, or does not call it at all.

Usage:
    import mandatory_field_gate as gate
    gate.assert_no_empty_mandatory(page, "nav:form", action_label="GO")
    gate.assert_no_empty_mandatory(page, "tab:tabPanel:objectForm:form", action_label="Save (insert)")
"""

YELLOW = "rgb(252, 249, 192)"


def find_empty_mandatory(page, scope_prefix):
    """Scan every input/select/textarea whose id starts with scope_prefix for the mandatory-yellow
    background AND an empty current value. Returns a list of {id, label} dicts - empty list = safe to
    proceed. Label is resolved the same way the recon scanner does: the cell immediately to the LEFT
    (same row, column 0), not guessed from the field's own id."""
    return page.evaluate(
        """(args) => {
            const [prefix, YELLOW] = args;
            const out = [];
            document.querySelectorAll('input,select,textarea').forEach(e => {
                if (!e.id || !e.id.startsWith(prefix)) return;
                if (e.type === 'hidden') return;
                if (!e.offsetParent) return;   // skip hidden/off-screen elements
                const y = getComputedStyle(e).backgroundColor === YELLOW;
                if (!y) return;
                const val = (e.value || '').trim();
                if (val !== '') return;
                const m = e.id.match(/^(.*:R:\\d+):C:\\d+:/);
                let lab = '';
                if (m) {
                    const lc = document.getElementById(m[1] + ':C:0:la');
                    if (lc) lab = (lc.innerText || '').trim();
                }
                out.push({id: e.id, label: lab});
            });
            return out;
        }""",
        [scope_prefix, YELLOW],
    )


def assert_no_empty_mandatory(page, scope_prefix, action_label="proceed"):
    """Gate: raise RuntimeError naming every mandatory-and-empty field under scope_prefix, BEFORE the
    caller clicks GO/Save - the proactive counterpart to reading EC's error banner after a failed Save."""
    empty = find_empty_mandatory(page, scope_prefix)
    if empty:
        detail = "; ".join("%s (%s)" % (f["label"] or "?", f["id"]) for f in empty)
        raise RuntimeError(
            "BLOCKED before %s: %d mandatory field(s) still empty: %s"
            % (action_label, len(empty), detail)
        )
