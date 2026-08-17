"""Plain-module RF library (same convention as DbVerify.py) - reads a simple key=value
properties file into a dict, for data-driven form fills (e.g. Insert Bank Record from
testdata/bank_entry.properties). One entry per line, '#' starts a full-line comment, blank
lines ignored. No section headers, no escaping - deliberately simple for this project's use case.
"""


def read_properties(path):
    """Return an ordered dict of {column_label: value} from a simple key=value properties file."""
    result = {}
    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(f"Malformed properties line (no '='): {raw_line!r}")
            key, _, value = line.partition("=")
            result[key.strip()] = value.strip()
    return result
