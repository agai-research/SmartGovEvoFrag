"""First test of HyFragComp on the scenario repository: the paper scenario (partial reuse, variant switch, rejections) and its two change events.

Run: python Test/first_test.py   (writes out/first_test/*.json, *.md and BPMN-style figures; exits non-zero when an assertion fails)
"""
import json
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from Test.common import make_env, make_gen
from Data.build_events import bridge_for, item_of
from hfc import report
from hfc.data import frag_to_dict, edge_to_dict
from hfc.methods import make
from hfc.req import request_from

OUT = ROOT / "out" / "first_test"
FID = lambda s: "MAR.longstay." + s


def main():
    cfg, models, repo = make_env(100, 0)
    gen = make_gen(cfg, repo, 11)
    P = [p for p in gen.procs if p["pid"] == "MAR.longstay"][0]
    queries = json.loads((ROOT / "Prompts" / "prompts.json").read_text())["queries"]
    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))
        print("  [%s] %s" % ("ok" if cond else "FAIL", name))

    # stored record c_17 and a history of three users so that the shared region becomes a composite
    m = make("ours", repo, cfg, models, 0)
    c17 = gen.record("c17", 0.0, "u17", [(P, "std")], "first", prio=False)
    print("== history: three users with the same first application ==")
    for i in range(3):
        h = gen.request("h%d" % i, 1.0 + i, "hist%d" % i, [(P, "std")], "first", pii=False, channel="SMS")
        rh = m.serve(request_from(h))
        print("  %s mode=%s promoted composites=%d" % (h["rid"], rh.mode, m.promo.promoted))
    m.preload([c17], 0.0)
    comps = {k: v for k, v in m.promo.members.items()}
    check("composite C1 over {F2, F3, F4} promoted", any(set(v) == {FID("elig_f"), FID("docs"), FID("fee")} for v in comps.values()))
    print("== scenario request ==")
    q = request_from(dict(queries[0], t=10.0))
    r = m.serve(q)
    print(report.summary(r, "scenario"))
    report.write(r, OUT, "scenario")
    kinds = {g.gid: g.key[1] for g in r.graph.goals}
    by = {kinds[g]: s for g, s in r.status.items()}
    check("mode is partial", r.mode == "partial")
    check("rho = 3/5", abs(r.rho - 3 / 5) < 1e-9 and r.n_goals == 5)
    check("documents reused (F3)", by["docs"] == "reuse" and FID("docs") in r.cover[[g for g, k in kinds.items() if k == "docs"][0]])
    check("submission reused with channel SMS", by["sub"] == "reuse" and any(g.slots.get("channel") == "SMS" for g in r.graph.goals if g.key[1] == "sub"))
    check("appointment switched F5 -> F7 with the fee fragment kept", by["appt"] == "switch" and set(r.cover[[g for g, k in kinds.items() if k == "appt"][0]]) >= {FID("appt_p"), FID("fee")})
    check("eligibility and contract validation recomposed", by["elig"] == "new" and by["extra"] == "new")
    check("renewal eligibility failed re-validation at V3", r.info["failed_checks"].get([g for g, k in kinds.items() if k == "elig"][0]) == "V3")
    rej = dict((a, b) for a, b in r.info["rejections"])
    check("F2 rejected by chi_fun and F17 by chi_rol", rej.get(FID("elig_f")) == "chi_fun" and rej.get(FID("extra_b")) == "chi_rol")
    check("F2r and F16 selected", FID("elig_r") in r.frags and FID("extra_a") in r.frags and FID("elig_f") not in r.frags)
    check("all feasibility checks hold", r.ok and all(r.info["feas"].values()))
    print("  junctions checked (touching new fragments): %d of %d connections" % (len(r.junctions), len(r.conns)))
    new = {FID("elig_r"), FID("extra_a"), FID("appt_p")}
    touching = {c[:2] for c in r.conns if c[0] in new or c[1] in new}
    check("every connection touching a new fragment is junction-checked", touching <= set(map(tuple, r.junctions)))

    print("== other queries ==")
    for d in queries[1:]:
        rr = m.serve(request_from(d))
        print(report.summary(rr, d["rid"]))
        report.write(rr, OUT, d["rid"])
        check("%s is served" % d["rid"], rr.ok)

    print("== change events ==")
    hg = m.w.hg
    f4 = hg.frag(FID("fee"))
    ev1 = {"type": "update", "new": frag_to_dict(replace(f4, dmax=f4.dmax + 2, rev=f4.rev + 1)), "t": 20.0, "adds": [], "kind": "subst", "id": "ev_i"}
    out1 = m.handle(ev1)
    print("  (i) fee schedule revised, substitutable: ", {k: out1[k] for k in ("changed", "rebound", "suspect", "evicted", "evals")})
    check("event (i) invalidates nothing and rebinds", out1["suspect"] == 0 and out1["evicted"] == 0 and out1["rebound"] >= 1)
    f3 = hg.frag(FID("docs"))
    new3 = replace(f3, inp=f3.inp | {item_of(f3)}, rev=f3.rev + 1)
    b, es = bridge_for(hg, f3, "MAR")
    ev2 = {"type": "update", "new": frag_to_dict(new3), "t": 21.0, "adds": [{"frag": frag_to_dict(b), "edges": [edge_to_dict(e) for e in es]}], "kind": "nonsub", "id": "ev_ii"}
    out2 = m.handle(ev2)
    print("  (ii) mandatory document added, not substitutable: ", {k: out2[k] for k in ("changed", "suspect", "repaired", "evicted", "evals", "llm_calls")})
    check("event (ii) marks dependants suspect", out2["suspect"] + out2["repaired"] + out2["evicted"] >= 1)
    c1 = [c for c, v in comps.items() if set(v) == {FID("elig_f"), FID("docs"), FID("fee")}][0]
    c1f = m.w.hg.frag(c1)
    check("composite C1 is withdrawn or re-versioned after event (ii)", c1f is None or not m.w.hg.alive(c1, 21.0) or c1f.rev > 1)
    d = dict(queries[1], rid="after_event", t=22.0, user="u_late")
    ra = m.serve(request_from(d))
    print(report.summary(ra, "after_event"))
    report.write(ra, OUT, "after_event")
    check("a request after the event is served and verified", ra.ok and all(ra.info["feas"].values()))
    check("the revised document fragment is used with its bridge", FID("docs") not in ra.frags or any("bridge" in f for f in ra.frags))
    (OUT / "checks.json").write_text(json.dumps(checks, indent=1))
    bad = [n for n, ok in checks if not ok]
    print("\n%d checks, %d failed" % (len(checks), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
