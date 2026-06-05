# Pabot Parallel Execution Guide

## Installation
```bash
pip install robotframework-pabot
```

## Basic Usage
```bash
# Run 4 parallel processes
pabot --processes 4 --variablefile vars/local.py tests/

# Suite-level split (default) — each .robot file in separate process
pabot --processes 4 tests/

# Test-level split — each TEST in separate process (faster but needs full isolation)
pabot --testlevelsplit --processes 4 tests/
```

## Key CLI Flags
| Flag | Description | Recommended |
|---|---|---|
| `--processes N` | Number of parallel workers | 2-4 for EC |
| `--testlevelsplit` | Split by test not suite | Use with caution — needs full isolation |
| `--pabotlib` | Enable shared resource locking | Required when tests share DB data |
| `--resourcefile file.robot` | Shared resource file for all workers | For common setup |
| `--verbose` | Show worker output in real time | Debug mode |
| `--output` | Output directory | `results/` |

## Worker Configuration for EC Test Suite
```bash
# Local testing — 2 workers (conservative, easy to debug)
pabot --processes 2 --variablefile vars/local.py tests/

# CI (COPS DEV) — 4 workers
pabot --processes 4 --variablefile vars/test.py tests/

# Do NOT use > 4 workers for EC — Oracle connection pool exhaustion
```

## Lock/Unlock — Prevent Test Data Conflicts
```robot
# In test that modifies shared data
Acquire Lock    EC_CHECK_RULE_LOCK
Insert Check Rule    PHD_TEST_RULE
Release Lock    EC_CHECK_RULE_LOCK
```

```bash
# Run with pabotlib enabled
pabot --processes 4 --pabotlib tests/
```

## Merging Results
```bash
# Combine multiple shards/workers into one report
rebot --outputdir merged_results results/*/output.xml
```
