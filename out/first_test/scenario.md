# scenario

- mode: **partial**, rho = 0.60, sub-goals 5, to recompose 2, repair rounds 0
- LLM calls: 7; latency 17074 ms (LLM part analytic)
- verification: C1=True, C2=True, C3=True, C4=True, C5=True

## Decisions

- g0 `MAR.longstay/elig/renew`: **new** -> MAR.longstay.elig_r
- g1 `MAR.longstay/docs/`: **reuse** -> MAR.longstay.docs
- g2 `MAR.longstay/extra/`: **new** -> MAR.longstay.extra_a
- g3 `MAR.longstay/appt/`: **switch** -> MAR.longstay.fee, MAR.longstay.appt_p
- g4 `MAR.longstay/sub/`: **reuse** -> MAR.longstay.sub

## Explanation

verify my renewal eligibility for the long-stay residence pe: composed anew with ['MAR.longstay.elig_r'] (previous reuse refused: V3)
check my documents for the long-stay residence permit in Mor: reused from record c-09e31095 (tier C_e), match 0.94 = 0.45 + 0.30 + 0.20, valid at t=10.0 within window [0, 10000000]
validate my proof of funds from the new employment contract : composed anew with ['MAR.longstay.extra_a'] (previous reuse refused: no-match)
book the earliest priority appointment for the long-stay res: switched variant of from record c-09e31095 (tier C_e), match 0.78 = 0.30 + 0.28 + 0.20, valid at t=10.0 within window [0, 10000000], ['MAR.longstay.fee', 'MAR.longstay.appt_s'] replaced by ['MAR.longstay.fee', 'MAR.longstay.appt_p'] because the guard no longer holds
notify me by <CHANNEL> for the long-stay residence permit in: reused from record c-09e31095 (tier C_e), match 0.93 = 0.44 + 0.29 + 0.20, valid at t=10.0 within window [0, 10000000], slots channel := SMS
rejected ['C:866f7c1f7166d81a', 'MAR.longstay.elig_f'] by chi_fun
rejected ['MAR.longstay.extra_b'] by chi_rol

## Figures

- scenario_workflow.png
- scenario_workflow.svg
- scenario_goals.png
- scenario_goals.svg