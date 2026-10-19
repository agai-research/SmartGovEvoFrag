"""Quick end-to-end check: stored records, a stream of requests, every method."""
import time
from Test.common import *
from hfc.methods import make, NAMES

cfg, models, repo = make_env(1000, 0)
gen = make_gen(cfg, repo, 1)
eco, bl = gen.pick_blocks(["std", "ext"])
rec = gen.record("r0", 0.0, "u0", bl, "first")
reqs = [gen.request("q%d" % i, 1.0 + i, "u%d" % (i % 2), bl, "first", unseen_p=0.3, n_trap=1) for i in range(3)]
for name in NAMES:
    m = make(name, repo, cfg, models, 0)
    m.preload([rec])
    for q in reqs:
        t0 = time.time()
        res = m.serve(request_from(q))
        print(name, res.mode, res.ok, res.n_goals, round(res.rho, 2), res.repairs, "calls", res.stats["calls_total"], "ms %.0f" % res.stats["total_ms"], round(time.time() - t0, 2), res.info.get("failure"))
print({k: (round(v), res.stats["tok_in"].get(k), res.stats["tok_out"].get(k)) for k, v in res.stats["llm_ms"].items()})
m = make("ours", repo, cfg, models, 0); m.preload([rec])
r = m.serve(request_from(reqs[1]))
print({k: (round(v), r.stats["tok_in"].get(k), r.stats["tok_out"].get(k)) for k, v in r.stats["llm_ms"].items()}, r.stats["t"])
print(r.status, r.info.get("failed_checks"))
