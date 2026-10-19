# Environment

- Python 3.13 (3.10 or later works), CPU only, no GPU needed.
- Packages: see `requirements.txt` (NumPy, SciPy, scikit-learn, PyYAML, matplotlib, networkx, pandas, python-docx).
- Optional: Graphviz `dot` (BPMN-style drawings are also written as `.dot` files), `pdflatex` (for the `.tex` files in `docs/`).
- Language-model backend: `llm.backend: rule` in `configs/default.yaml`. The eight role configurations run on a local rule-and-embedding engine; the latency of an LLM call is priced analytically with `llm.latency`.
- Seeds: `seed: 0` for models and data; the five experiment runs use seeds 0-4; tuning uses seeds 100-101.
- Memory: 4 GB is enough for the largest repository (20,000 fragments).
- Expected run times on two CPU cores: encoder training 2-3 min (cached in `results/ckpt`), `Test/first_test.py` 10 s, one smoke series 1 min, the full protocol several hours.
