"""Shared helpers for tests and scripts: build the environment and a request/record constructor."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hfc import config
from hfc.repo import Models, Repo
from hfc.req import request_from


def make_env(size=1000, seed=0, overrides=None):
    """Return (cfg, models, repo) for a repository of about `size` fragments."""
    cfg = config.load()
    for k, v in (overrides or {}).items():
        cfg.set(k, v)
    models = Models(cfg, seed)
    repo = Repo(cfg, models, size)
    return cfg, models, repo


def make_gen(cfg, repo, seed=1):
    from Data.build_requests import Gen
    return Gen(cfg, repo.pids, seed)
