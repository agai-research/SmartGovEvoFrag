# first_std

- mode: **full**, rho = 1.00, sub-goals 4, to recompose 0, repair rounds 0
- LLM calls: 4; latency 13363 ms (LLM part analytic)
- verification: C1=True, C2=True, C3=True, C4=True, C5=True

## Decisions

- g0 `MAR.longstay/elig/first`: **reuse** -> MAR.longstay.elig_f
- g1 `MAR.longstay/docs/`: **reuse** -> MAR.longstay.docs
- g2 `MAR.longstay/appt/`: **reuse** -> MAR.longstay.appt_s, MAR.longstay.fee
- g3 `MAR.longstay/sub/`: **reuse** -> MAR.longstay.sub

## Explanation

confirm my eligibility for the long-stay residence permit in: reused from record c-5831b91c (tier C_e), match 1.00 = 0.50 + 0.30 + 0.20, valid at t=3.0 within window [0, 10000000]
prepare the documentation file for the long-stay residence p: reused from record c-5831b91c (tier C_e), match 0.97 = 0.47 + 0.30 + 0.20, valid at t=3.0 within window [0, 10000000]
schedule an appointment for the long-stay residence permit i: reused from record c-5831b91c (tier C_e), match 0.99 = 0.50 + 0.30 + 0.20, valid at t=3.0 within window [0, 10000000]
submit my long-stay residence permit file in Morocco: reused from record c-5831b91c (tier C_e), match 1.00 = 0.50 + 0.30 + 0.20, valid at t=3.0 within window [0, 10000000]

## Figures

- first_std_workflow.png
- first_std_workflow.svg
- first_std_goals.png
- first_std_goals.svg