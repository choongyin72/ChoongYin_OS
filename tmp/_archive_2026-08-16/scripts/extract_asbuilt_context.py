"""Extract readable context windows around keywords in a saved As-Built tool-result
(lines are huge — Read/Grep can't show them). Usage: edit FILE + TERMS below."""
import re
import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else \
    r"C:/Users/choong-yin.lee/.claude/projects/c--Projects-ChoongYin-OS/bb141381-f9c0-4dba-ba72-3b1d7b818ceb/tool-results/mcp-claude_ai_Microsoft_365-read_resource-1781328233844.txt"
TERMS = sys.argv[2:] or ["I_IN_PHD_DAILY"]
WIN = 600

text = open(FILE, encoding="utf-8").read()
# normalize the doc's spaced-out characters lightly for readability
for term in TERMS:
    print(f"\n{'='*70}\nTERM: {term}\n{'='*70}")
    for m in re.finditer(re.escape(term), text):
        s = max(0, m.start() - WIN)
        e = min(len(text), m.end() + WIN)
        snippet = text[s:e].replace("\n", " ")
        snippet = re.sub(r"\s{2,}", " ", snippet)
        print(f"...{snippet}...\n---")
