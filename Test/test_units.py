"""Unit tests of the main components: HNSW, count-min sketch, ontology, substitutability, role engine, Hungarian alignment, checks, memory."""
import itertools
import sys
import unittest
from dataclasses import replace
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from Test.common import make_env, make_gen
from hfc.index import HNSW
from hfc.mem import CountMin
from hfc.model import Onto, subst_ok
from hfc.methods import make
from hfc.req import request_from
from hfc.util import Stats

ENV = {}


def env():
    if not ENV:
        ENV["v"] = make_env(100, 0)
    return ENV["v"]


class TestIndex(unittest.TestCase):
    def test_recall_and_filter(self):
        rng = np.random.default_rng(3)
        X = rng.normal(size=(600, 24)).astype(np.float32)
        X /= np.linalg.norm(X, axis=1, keepdims=True)
        h = HNSW(24, 12, 64, seed=1, cap=700)
        for i, x in enumerate(X):
            h.add(x, i)
        hit = 0
        for q in X[:40]:
            ex = {k for _, k in h.exact(q, 10)}
            hit += len(ex & {k for _, k in h.knn(q, 10, ef=64)})
        self.assertGreater(hit / 400, 0.9)
        even = lambda k: k % 2 == 0
        res = h.knn(X[1], 10, ef=32, pred=even)
        self.assertEqual(len(res), 10)
        self.assertTrue(all(k % 2 == 0 for _, k in res))


class TestSketch(unittest.TestCase):
    def test_never_underestimates(self):
        cm = CountMin(256, 4, 10 ** 9)
        truth = {}
        rng = np.random.default_rng(0)
        for _ in range(3000):
            k = "r%d" % int(rng.zipf(1.5) % 400)
            cm.add(k)
            truth[k] = truth.get(k, 0) + 1
        self.assertTrue(all(cm.est(k) >= v for k, v in truth.items()))

    def test_halving(self):
        cm = CountMin(64, 3, 4)
        for _ in range(8):
            cm.add("a")
            cm.tick()
        self.assertLess(cm.est("a"), 8)


class TestModel(unittest.TestCase):
    def test_ontology(self):
        o = Onto()
        self.assertTrue(o.entails({"fee_paid:x"}, {"fee_paid"}))
        self.assertFalse(o.entails({"fee_paid"}, {"fee_paid:x"}))
        self.assertFalse(o.consistent({"no_valid_permit", "valid_permit_held"}))

    def test_substitutability(self):
        cfg, models, repo = env()
        f = repo.base.frags["MAR.longstay.fee"]
        o = Onto()
        self.assertTrue(subst_ok(replace(f, dmax=f.dmax + 2), f, o))
        self.assertFalse(subst_ok(replace(f, inp=f.inp | {"new_item"}), f, o))
        self.assertFalse(subst_ok(replace(f, dmin=f.dmin + 1), f, o))


class TestRoles(unittest.TestCase):
    def test_masking_and_plan(self):
        cfg, models, repo = env()
        m = make("scratch", repo, cfg, models, 0)
        gen = make_gen(cfg, repo, 5)
        P = [p for p in gen.procs if p["pid"] == "MAR.longstay"][0]
        d = gen.request("t1", 1.0, "u1", [(P, "std")], "first", pii=True, channel="SMS")
        req = request_from(d)
        st = Stats()
        graph, _, a = m.front(req, st)
        self.assertFalse(m.roles.has_pii(a["template"]))
        keys = sorted(g.key for g in graph.goals)
        truth = sorted(tuple(x) for x in req.truth["goals"])
        self.assertEqual(keys, truth)
        self.assertEqual(st.calls["cur"], 1)
        self.assertEqual(st.calls["pln"], 1)


class TestAlignment(unittest.TestCase):
    def test_hungarian_is_optimal(self):
        from scipy.optimize import linear_sum_assignment
        rng = np.random.default_rng(1)
        for _ in range(20):
            W = rng.random((5, 6))
            r, c = linear_sum_assignment(-W)
            best = max(sum(W[i, p[i]] for i in range(5)) for p in itertools.permutations(range(6), 5))
            self.assertAlmostEqual(W[r, c].sum(), best)


class TestPipeline(unittest.TestCase):
    def test_serve_reuse_and_verify(self):
        cfg, models, repo = env()
        gen = make_gen(cfg, repo, 7)
        P = [p for p in gen.procs if p["pid"] == "MAR.longstay"][0]
        m = make("ours", repo, cfg, models, 0)
        r1 = m.serve(request_from(gen.request("a", 1.0, "u1", [(P, "std")], "first", pii=False, channel="SMS")))
        r2 = m.serve(request_from(gen.request("b", 2.0, "u1", [(P, "std")], "first", pii=False, channel="SMS")))
        self.assertTrue(r1.ok and r2.ok)
        self.assertEqual(r1.mode, "scratch")
        self.assertEqual(r2.mode, "full")
        self.assertEqual(r2.stats["calls"].get("ret", 0), 0)
        self.assertTrue(all(r2.info["feas"].values()))

    def test_private_record_not_shared(self):
        cfg, models, repo = env()
        gen = make_gen(cfg, repo, 9)
        P = [p for p in gen.procs if p["pid"] == "MAR.longstay"][0]
        m = make("ours", repo, cfg, models, 0)
        rec = gen.record("p1", 0.0, "owner", [(P, "std")], "first", scope="u")
        m.preload([rec], 0.0)
        r = m.serve(request_from(gen.request("x", 3.0, "other", [(P, "std")], "first", pii=False, channel="SMS")))
        self.assertNotEqual(r.mode, "full")
        self.assertTrue(r.ok)


if __name__ == "__main__":
    unittest.main()
