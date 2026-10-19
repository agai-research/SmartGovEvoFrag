"""Gradient check of the autograd engine and the AllSet encoder."""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hfc import nn
from hfc.allset import AllSet, Packed


def numeric_grad(f, p, eps=1e-5):
    g = np.zeros_like(p.d)
    it = np.nditer(p.d, flags=["multi_index"])
    for _ in it:
        i = it.multi_index
        o = p.d[i]
        p.d[i] = o + eps
        a = f()
        p.d[i] = o - eps
        b = f()
        p.d[i] = o
        g[i] = (a - b) / (2 * eps)
    return g


def test_allset_grad():
    nn.DTYPE = np.float64
    rng = np.random.default_rng(1)
    n, d = 7, 8
    edges = [([0], [1, 2, 3], 1), ([1, 2, 3], [4, 5], 2), ([4], [6], 0), ([5], [6], 0)]
    P = Packed(n, edges, cap_set=4, cap_inc=3)
    h0 = rng.normal(size=(n, d)).astype(np.float64)
    enc = AllSet(d=d, dp=4, layers=2, seed=3)
    tgt = rng.normal(size=(n, d)).astype(np.float64)

    def loss():
        with nn.no_grad():
            h = enc.zstr(enc.forward(h0, P, masked=np.array([0, 0, 1, 0, 0, 0, 0], bool)))
        return float(((h.d - tgt) ** 2).sum() * 0.01)

    h = enc.zstr(enc.forward(h0, P, masked=np.array([0, 0, 1, 0, 0, 0, 0], bool)))
    diff = nn.add(h, nn.T(-tgt))
    l = nn.reshape(nn.scale(nn.mul(diff, diff), 0.01), (-1,))
    s = nn.matmul(nn.reshape(l, (1, -1)), nn.T(np.ones((n * d, 1), dtype=np.float64)))
    for p in enc.params():
        p.g = None
    s.backward()
    worst = 0.0
    for p in [enc.wz, enc.layers[0].e1, enc.layers[1].pma_h.wk, enc.layers[0].pma_t.seed, enc.mask_vec]:
        num = numeric_grad(loss, p)
        ana = p.g if p.g is not None else np.zeros_like(p.d)
        denom = np.abs(num).max() + np.abs(ana).max() + 1e-6
        e = np.abs(num - ana).max() / denom
        print(' param err %.5f' % e)
        worst = max(worst, e)
    assert worst < 0.05, worst
    print("allset grad ok, worst rel err %.4f" % worst)


if __name__ == "__main__":
    test_allset_grad()
