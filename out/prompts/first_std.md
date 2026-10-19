# first_std

- mode: **scratch**, rho = 0.00, sub-goals 4, to recompose 4, repair rounds 0
- LLM calls: 10; latency 17293 ms (LLM part analytic)
- verification: C1=True, C2=True, C3=True, C4=True, C5=True

## Decisions

- g0 `MAR.longstay/elig/first`: **new** -> MAR.longstay.elig_f
- g1 `MAR.longstay/docs/`: **new** -> MAR.longstay.docs
- g2 `MAR.longstay/appt/`: **new** -> MAR.longstay.appt_s, MAR.longstay.fee
- g3 `MAR.longstay/sub/`: **new** -> MAR.longstay.sub

## Explanation

confirm my eligibility for the long-stay residence permit in: composed anew with ['MAR.longstay.elig_f'] (previous reuse refused: no-match)
prepare the documentation file for the long-stay residence p: composed anew with ['MAR.longstay.docs'] (previous reuse refused: no-match)
schedule an appointment for the long-stay residence permit i: composed anew with ['MAR.longstay.appt_s', 'MAR.longstay.fee'] (previous reuse refused: no-match)
submit my long-stay residence permit file in Morocco: composed anew with ['MAR.longstay.sub'] (previous reuse refused: no-match)
rejected ['MAR.longstay.elig_r'] by chi_fun
rejected ['MAR.longstay.appt_s'] by c4
rejected ['MAR.longstay.appt_p'] by guard

## Figures

- first_std_workflow.png
- first_std_workflow.svg
- first_std_goals.png
- first_std_goals.svg