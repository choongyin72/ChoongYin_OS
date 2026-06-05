# Robotidy & Robocop Linting Guide

## Robotidy (Formatter)

### Installation
```bash
pip install robotframework-tidy
```

### Usage
```bash
robotidy tests/                   # format in place
robotidy --check tests/           # check without modifying (CI mode)
robotidy --diff tests/            # show diff without modifying
```

### .robotidy Config for EC Project
```toml
# .robotidy (in project root)
[tool.robotidy]
transformers = [
    "AlignKeywordsTestCases",
    "NormalizeSeparators",
    "OrderSettings",
    "SmartSortKeywords",
    "RenameKeywords",
]
line_length = 120
```

## Robocop (Linter)

### Installation
```bash
pip install robotframework-robocop
```

### Usage
```bash
robocop tests/ resources/          # lint all
robocop --include W tests/         # warnings only
robocop --no-dotfile-discovery tests/  # CI mode
```

### Key Rules to Enforce for EC Project

| Rule | Severity | Description |
|---|---|---|
| `missing-doc-keyword` | W | Every keyword must have [Documentation] |
| `missing-doc-test-case` | W | Every test must have [Documentation] |
| `too-long-keyword` | W | Keyword > 20 steps — split it |
| `not-allowed-char-in-name` | E | No special chars in keyword names |
| `duplicated-library-import` | E | Same library imported twice |
| `wrong-case-in-keyword-name` | W | Keywords must be Title Case |
| `no-sleep-keyword` | E | Sleep is forbidden — use waits |

### .robocop Config for EC Project
```ini
# .robocop (in project root)
[robocop]
include = missing-doc-keyword,missing-doc-test-case,no-sleep-keyword,duplicated-library-import
exclude = too-many-calls-in-test-case
filemask = *.robot,*.resource
```

### Rules Disabled for EC (with justification)
| Rule | Reason disabled |
|---|---|
| `too-long-test-case` | EC test cases can be up to 20 steps for end-to-end flows |
| `requires-version` | Not using versioned keywords |
