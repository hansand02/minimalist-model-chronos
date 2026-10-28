# Backtest results

Horizon 3, stride 1, trained once. Cells: CRPS on log(1 + cases), linked to the run folder (metrics.csv, eval.html, eval.nc). Mean over the three countries. Lower is better; coverage should be near 0.80.

## Big run (36 splits)

| Model | Vietnam | Laos | Thailand | Mean log CRPS | Mean CRPS | Coverage 10–90 |
|---|---|---|---|---|---|---|
| [timestral](models/timestral) | [0.347](results/timestral_vietnam_h3_s36/) | [0.573](results/timestral_laos_h3_s36/) | [0.444](results/timestral_thailand_h3_s36/) | **0.455** | 28.1 | 0.79 |
| [chronos2](models/chronos2) | [0.364](results/chronos2_vietnam_h3_s36/) | [0.572](results/chronos2_laos_h3_s36/) | [0.453](results/chronos2_thailand_h3_s36/) | **0.463** | 30.6 | 0.77 |
| [tabpfn_ts](models/tabpfn_ts) | [0.367](results/tabpfn_ts_vietnam_h3_s36/) | [0.610](results/tabpfn_ts_laos_h3_s36/) | [0.470](results/tabpfn_ts_thailand_h3_s36/) | **0.483** | 29.5 | 0.76 |
| [mstl_arima](https://github.com/chap-models/mstl_arima) | [0.395](results/mstl_arima_vietnam_h3_s36/) | [0.642](results/mstl_arima_laos_h3_s36/) | [0.465](results/mstl_arima_thailand_h3_s36/) | **0.501** | 31.3 | 0.71 |
| [chap_pymc](https://github.com/dhis2-chap/chap_pymc) | [0.416](results/chap_pymc_vietnam_h3_s36/) | [0.644](results/chap_pymc_laos_h3_s36/) | [0.528](results/chap_pymc_thailand_h3_s36/) | **0.529** | 33.8 | 0.77 |
| [mantis](models/mantis) | [0.603](results/mantis_vietnam_h3_s36/) | [0.734](results/mantis_laos_h3_s36/) | [0.582](results/mantis_thailand_h3_s36/) | **0.640** | 35.5 | 0.55 |
| [chtorch](https://github.com/dhis2-chap/chtorch) | [0.602](results/chtorch_vietnam_h3_s36/) | [0.869](results/chtorch_laos_h3_s36/) | [0.488](results/chtorch_thailand_h3_s36/) | **0.653** | 46.2 | 0.77 |
| [seasonal_naive](models/seasonal_naive) | [0.541](results/seasonal_naive_vietnam_h3_s36/) | [1.056](results/seasonal_naive_laos_h3_s36/) | [0.800](results/seasonal_naive_thailand_h3_s36/) | **0.799** | 47.4 | 0.68 |

## Small run (6 splits)

| Model | Vietnam | Laos | Thailand | Mean log CRPS | Mean CRPS | Coverage 10–90 |
|---|---|---|---|---|---|---|
| [chronos2](models/chronos2) | [0.500](results/chronos2_vietnam/) | [0.716](results/chronos2_laos/) | [0.422](results/chronos2_thailand/) | **0.546** | 70.7 | 0.78 |
| [timestral](models/timestral) | [0.467](results/timestral_vietnam/) | [0.744](results/timestral_laos/) | [0.435](results/timestral_thailand/) | **0.549** | 67.5 | 0.76 |
| [t0_gamma](models/t0_gamma) | [0.491](results/t0_gamma_vietnam/) | [0.801](results/t0_gamma_laos/) | [0.428](results/t0_gamma_thailand/) | **0.573** | 67.9 | 0.72 |
| [mstl_arima](https://github.com/chap-models/mstl_arima) | [0.557](results/mstl_arima_vietnam/) | [0.746](results/mstl_arima_laos/) | [0.434](results/mstl_arima_thailand/) | **0.579** | 74.1 | 0.65 |
| [chap_pymc](https://github.com/dhis2-chap/chap_pymc) | [0.537](results/chap_pymc_vietnam/) | [0.789](results/chap_pymc_laos/) | [0.593](results/chap_pymc_thailand/) | **0.640** | 73.8 | 0.68 |
| [seasonal_naive](models/seasonal_naive) | [0.910](results/seasonal_naive_vietnam/) | [1.680](results/seasonal_naive_laos/) | [0.588](results/seasonal_naive_thailand/) | **1.059** | 113.6 | 0.59 |
| [chtorch](https://github.com/dhis2-chap/chtorch) | [0.667](results/chtorch_vietnam/) | [2.112](results/chtorch_laos/) | [0.423](results/chtorch_thailand/) | **1.067** | 109.2 | 0.60 |
