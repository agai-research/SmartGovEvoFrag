"""Construct Prompts/prompts.json: the scenario request of the paper plus four further queries on the scenario repository."""
import json
from Test.common import *
from hfc.data import jsave

cfg, models, repo = make_env(100, 0)
gen = make_gen(cfg, repo, 7)
P = [p for p in gen.procs if p["pid"] == "MAR.longstay"][0]
Q = []
q = gen.request("scenario", 2.0, "u_scn", [(P, "ext")], "renew", prio=True, channel="SMS", pii=False)
q["text"] = ("Hello, I am Sara Benali, my email is sara.benali@mail.com. I want to renew my long-stay residence permit in Morocco. "
             "First verify my renewal eligibility for the long-stay residence permit in Morocco, then check my documents, validate my proof of funds from the new employment contract, "
             "pay the fee and book the earliest priority appointment, and finally submit the application and notify me by SMS.")
q["note"] = "paper scenario: renewal as a priority case, new employment contract, SMS notification"
Q.append(q)
q = gen.request("first_std", 3.0, "u_a", [(P, "std")], "first", prio=False, channel="email", pii=True)
q["note"] = "first application, standard appointment: matches the stored record"
Q.append(q)
q = gen.request("light_unseen", 3.5, "u_b", [(P, "light")], "first", unseen_p=0.9, channel="SMS", pii=False)
q["note"] = "paraphrased light request with words unseen by the encoder"
Q.append(q)
q = gen.request("terse", 4.0, "u_c", [(P, "std")], "first", terse=True, pii=True)
q["note"] = "ten-word prompt"
Q.append(q)
q = gen.request("trap", 4.5, "u_d", [(P, "std")], "first", prio=True, channel="mobile app", pii=True, n_trap=2, n_fill=2)
q["note"] = "priority request with distractor sentences"
Q.append(q)
jsave({"queries": Q}, ROOT / "Prompts" / "prompts.json")
print(len(Q), "queries")
