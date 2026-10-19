# terse

- mode: **full**, rho = 1.00, sub-goals 4, to recompose 0, repair rounds 0
- LLM calls: 4; latency 9817 ms (LLM part analytic)
- verification: C1=True, C2=True, C3=True, C4=True, C5=True

## Decisions

- g0 `MAR.longstay/elig/first`: **reuse** -> MAR.longstay.elig_f
- g1 `MAR.longstay/docs/`: **reuse** -> MAR.longstay.docs
- g2 `MAR.longstay/appt/`: **reuse** -> MAR.longstay.appt_s, MAR.longstay.fee
- g3 `MAR.longstay/sub/`: **reuse** -> MAR.longstay.sub

## Explanation

long-stay residence permit Morocco: verify eligibility: reused from record c-5831b91c (tier C_e), match 0.90 = 0.41 + 0.30 + 0.20, valid at t=4.0 within window [0, 10000000]
verify documents for the long-stay residence permit in Moroc: reused from record c-5831b91c (tier C_e), match 0.99 = 0.49 + 0.30 + 0.20, valid at t=4.0 within window [0, 10000000]
book appointment for the long-stay residence permit in Moroc: reused from record c-5831b91c (tier C_e), match 0.97 = 0.47 + 0.30 + 0.20, valid at t=4.0 within window [0, 10000000]
submit application for the long-stay residence permit in Mor: reused from record c-5831b91c (tier C_e), match 0.91 = 0.41 + 0.30 + 0.20, valid at t=4.0 within window [0, 10000000]

## Figures

- terse_workflow.png
- terse_workflow.svg
- terse_goals.png
- terse_goals.svg