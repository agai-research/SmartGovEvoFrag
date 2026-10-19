# light_unseen

- mode: **partial**, rho = 1.00, sub-goals 3, to recompose 0, repair rounds 0
- LLM calls: 4; latency 10412 ms (LLM part analytic)
- verification: C1=True, C2=True, C3=True, C4=True, C5=True

## Decisions

- g0 `MAR.longstay/docs/`: **reuse** -> MAR.longstay.docs
- g1 `MAR.longstay/appt/`: **reuse** -> MAR.longstay.fee, MAR.longstay.appt_s
- g2 `MAR.longstay/sub/`: **reuse** -> MAR.longstay.sub

## Explanation

prepare the documentation file for the long-stay residence p: reused from record c-09e31095 (tier C_e), match 0.99 = 0.50 + 0.29 + 0.20, valid at t=3.5 within window [0, 10000000]
reserve my appointment for the long-stay residence permit in: reused from record c-09e31095 (tier C_e), match 0.93 = 0.47 + 0.26 + 0.20, valid at t=3.5 within window [0, 10000000]
hand in my long-stay residence permit application in Morocco: reused from record c-09e31095 (tier C_e), match 0.98 = 0.48 + 0.29 + 0.20, valid at t=3.5 within window [0, 10000000], slots channel := SMS

## Figures

- light_unseen_workflow.png
- light_unseen_workflow.svg
- light_unseen_goals.png
- light_unseen_goals.svg