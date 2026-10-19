"""Run experiment series: python main-exp.py --exp e1 e2 ... --runs 5 --profile full"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from Exp import core


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", nargs="+", default=["e%d" % i for i in range(1, 12)])
    ap.add_argument("--runs", type=int, default=None)
    ap.add_argument("--profile", default="full", choices=["smoke", "full"])
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--methods", nargs="*", default=None)
    ap.add_argument("--no-tuned", action="store_true")
    ap.add_argument("--only", choices=["run", "aggregate", "figures"], default=None, help="run a single stage from stored results")
    a = ap.parse_args()
    for e in a.exp:
        t0 = time.time()
        if a.only in (None, "run"):
            core.run_series(e, a.runs, a.profile, a.methods, a.jobs, tuned=not a.no_tuned)
        if a.only in (None, "run", "aggregate", "figures"):
            agg = core.aggregate(e, a.profile, a.methods, a.runs)
            core.write_tables(e, agg, a.profile)
            core.render_figures(e, agg, a.profile)
        print("%s finished in %.0fs" % (e, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
