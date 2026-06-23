# Disposable merge-probe
Temporary file to give the test PR a real diff. Verifies that squash-merge (no --delete-branch)
does NOT delete the head branch. This branch + its base are deleted immediately after the check.
