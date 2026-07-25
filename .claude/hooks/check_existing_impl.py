#!/usr/bin/env python3
"""PreToolUse WARN hook (non-blocking) for EC automation.

Fires on Write/Edit. If about to CREATE A NEW file under ec-automation/{py,pageobjects,tests,screens}
whose screen-slug already has an implementation elsewhere, it injects an advisory so the parallel-copy
mistake (a 3rd Bank stack) surfaces at the moment of the Write. It NEVER blocks: any error or any
non-matching case emits an 'allow' with no message and exits 0. Purely advisory.
"""
import json
import os
import sys


def _allow(context=None):
    out = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}
    if context:
        out["hookSpecificOutput"]["additionalContext"] = context
    print(json.dumps(out))
    sys.exit(0)


def main():
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        _allow()
    try:
        target = (data.get("tool_input", {}) or {}).get("file_path", "") or ""
        norm = target.replace("\\", "/")
        marker = "workstreams/master-plan/ec-automation/"
        if marker not in norm:
            _allow()
        # only the code/test/page/screen dirs
        rel = norm.split(marker, 1)[1]
        top = rel.split("/", 1)[0]
        if top not in ("py", "pageobjects", "tests", "screens"):
            _allow()
        # only warn when CREATING a new file (editing an existing one is fine)
        if os.path.exists(target):
            _allow()
        root = norm.split(marker, 1)[0] + marker  # absolute ec-automation root
        stem = os.path.splitext(os.path.basename(norm))[0]
        slug = stem
        for suf in ("_iud", "_page", "_status", "_grid", "_setup"):
            if slug.endswith(suf):
                slug = slug[: -len(suf)]
        # strip a trailing _iud_<variant>
        if "_iud_" in stem:
            slug = stem.split("_iud_", 1)[0]
        if len(slug) < 3:
            _allow()
        # search sibling implementations by filename substring
        hits = []
        for d in ("py", "pageobjects", "tests", "screens"):
            base = os.path.join(root, d)
            if not os.path.isdir(base):
                continue
            for dirpath, _dirs, files in os.walk(base):
                if "__pycache__" in dirpath or "/results" in dirpath.replace("\\", "/"):
                    continue
                for f in files:
                    if not f.endswith((".py", ".robot", ".resource")):
                        continue
                    fstem = os.path.splitext(f)[0]
                    full = os.path.join(dirpath, f).replace("\\", "/")
                    if full == norm:
                        continue
                    if slug in fstem:
                        hits.append(full.split(marker, 1)[1])
        hits = sorted(set(hits))[:8]
        if not hits:
            _allow()
        msg = (
            "[check-existing-first] Creating NEW EC automation file '%s' (slug '%s'). "
            "Possible existing implementation(s) already present:\n  - %s\n"
            "Per ec-ui-knowledge/EC_OBJECT_CONFIG_IUD.md Step 0: REUSE/EXTEND these + the shared "
            "engine (py/ec_object_iud.py) + DbVerify.py rather than creating a parallel copy. "
            "If this is genuinely a new/distinct screen, proceed."
        ) % (os.path.basename(norm), slug, "\n  - ".join(hits))
        _allow(msg)
    except Exception:
        _allow()


if __name__ == "__main__":
    main()
