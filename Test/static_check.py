"""Static scan of the sources: syntax, constant returns, random in decision paths, forbidden comments and wording."""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"__pycache__", "seed"}
BAD_COMMENT = re.compile(r"#.*(we chose|simpler|ambiguous|could not use|workaround|for now|todo|fixme|placeholder|hack)", re.I)
GENERATE = re.compile(r"\bgenerat(e|es|ed|ing|ion)\b", re.I)
DECISION = ("hfc/reuse.py", "hfc/delta.py", "hfc/chk.py", "hfc/inval.py", "hfc/system.py", "hfc/mem.py", "hfc/promo.py", "hfc/llm.py")


def files():
    # the scanner itself holds the patterns it looks for
    for p in sorted(ROOT.rglob("*.py")):
        if not (set(p.relative_to(ROOT).parts) & SKIP) and "Data/seed" not in str(p) and p.name != "static_check.py":
            yield p


def main():
    bad = []
    for p in files():
        rel = str(p.relative_to(ROOT))
        src = p.read_text()
        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            bad.append((rel, "syntax", str(e)))
            continue
        for n in ast.walk(tree):
            if isinstance(n, ast.Return) and isinstance(n.value, ast.Constant) and n.value.value in (0.8,):
                bad.append((rel, n.lineno, "constant return"))
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "random" and isinstance(n.func.value, ast.Name) and n.func.value.id == "random" and rel in DECISION:
                bad.append((rel, n.lineno, "random in decision path"))
        for i, line in enumerate(src.splitlines(), 1):
            if BAD_COMMENT.search(line):
                bad.append((rel, i, "forbidden comment"))
            if GENERATE.search(line) and (line.strip().startswith("#") or '"""' in line):
                bad.append((rel, i, "wording: generate"))
        if rel in DECISION and re.search(r"^\s*import random|from random import", src, re.M):
            bad.append((rel, 0, "random module in decision module"))
    for r in bad:
        print(*r)
    print("%d files scanned, %d findings" % (len(list(files())), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
