# after_event

- mode: **partial**, rho = 0.75, sub-goals 4, to recompose 1, repair rounds 1
- LLM calls: 7; latency 16132 ms (LLM part analytic)
- verification: C1=True, C2=True, C3=True, C4=True, C5=True

## Decisions

- g0 `MAR.longstay/elig/first`: **reuse** -> MAR.longstay.elig_f
- g1 `MAR.longstay/docs/`: **new** -> MAR.longstay.docs
- g2 `MAR.longstay/appt/`: **reuse** -> MAR.longstay.appt_s, MAR.longstay.fee
- g3 `MAR.longstay/sub/`: **reuse** -> MAR.longstay.sub

## Explanation

confirm my eligibility for the long-stay residence permit in: reused from record c-5831b91c (tier C_e), match 1.00 = 0.50 + 0.30 + 0.20, valid at t=22.0 within window [0, 10000000]
prepare the documentation file for the long-stay residence p: composed anew with ['MAR.longstay.docs'] (previous reuse refused: V2)
schedule an appointment for the long-stay residence permit i: reused from record c-5831b91c (tier C_e), match 0.99 = 0.50 + 0.30 + 0.20, valid at t=22.0 within window [0, 10000000]
submit my long-stay residence permit file in Morocco: reused from record c-5831b91c (tier C_e), match 1.00 = 0.50 + 0.30 + 0.20, valid at t=22.0 within window [0, 10000000]
rejected ['MAR.longstay.docs'] by chi_dat

## Figures

- after_event_workflow.png
- after_event_workflow.svg
- after_event_goals.png
- after_event_goals.svg