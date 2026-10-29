# Backtest results

Horizon 3, stride 1, trained once. Country columns: mean CRPS on log(1 + cases) over all provinces and splits, linked to the run folder (metrics.csv, eval.html, eval.nc). Mean columns: unweighted mean over the three countries. Lower CRPS is better; coverage should be near 0.80.

Foundation = zero-shot foundation model, CHAP = existing CHAP model, Baseline = seasonal naive.

## Big run (36 splits)

| Model | Type | Vietnam<br>log CRPS | Laos<br>log CRPS | Thailand<br>log CRPS | **Mean<br>log CRPS** | Mean<br>CRPS | Mean coverage<br>10–90 |
|---|---|---|---|---|---|---|---|
| [timestral](models/timestral) | Foundation | [0.347](results/timestral_vietnam_h3_s36/) | [0.573](results/timestral_laos_h3_s36/) | [0.444](results/timestral_thailand_h3_s36/) | **0.455** | 28.1 | 0.79 |
| [chronos2](models/chronos2) | Foundation | [0.364](results/chronos2_vietnam_h3_s36/) | [0.572](results/chronos2_laos_h3_s36/) | [0.453](results/chronos2_thailand_h3_s36/) | **0.463** | 30.6 | 0.77 |
| [tabpfn_ts](models/tabpfn_ts) | Foundation | [0.367](results/tabpfn_ts_vietnam_h3_s36/) | [0.610](results/tabpfn_ts_laos_h3_s36/) | [0.470](results/tabpfn_ts_thailand_h3_s36/) | **0.483** | 29.5 | 0.76 |
| [auto_regressive_v2](https://github.com/chap-models/auto_regressive_monthly_v2) | CHAP | [0.346](results/auto_regressive_monthly_v2_vietnam_h3_s36/) | [0.673](results/auto_regressive_monthly_v2_laos_h3_s36/) | [0.459](results/auto_regressive_monthly_v2_thailand_h3_s36/) | **0.493** | 29.3 | 0.77 |
| [mstl_arima](https://github.com/chap-models/mstl_arima) | CHAP | [0.395](results/mstl_arima_vietnam_h3_s36/) | [0.642](results/mstl_arima_laos_h3_s36/) | [0.465](results/mstl_arima_thailand_h3_s36/) | **0.501** | 31.3 | 0.71 |
| [chap_pymc](https://github.com/dhis2-chap/chap_pymc) | CHAP | [0.416](results/chap_pymc_vietnam_h3_s36/) | [0.644](results/chap_pymc_laos_h3_s36/) | [0.528](results/chap_pymc_thailand_h3_s36/) | **0.529** | 33.8 | 0.77 |
| [mantis](models/mantis) | Foundation | [0.603](results/mantis_vietnam_h3_s36/) | [0.734](results/mantis_laos_h3_s36/) | [0.582](results/mantis_thailand_h3_s36/) | **0.640** | 35.5 | 0.55 |
| [chtorch](https://github.com/dhis2-chap/chtorch) | CHAP | [0.602](results/chtorch_vietnam_h3_s36/) | [0.869](results/chtorch_laos_h3_s36/) | [0.488](results/chtorch_thailand_h3_s36/) | **0.653** | 46.2 | 0.77 |
| [seasonal_naive](models/seasonal_naive) | Baseline | [0.541](results/seasonal_naive_vietnam_h3_s36/) | [1.056](results/seasonal_naive_laos_h3_s36/) | [0.800](results/seasonal_naive_thailand_h3_s36/) | **0.799** | 47.4 | 0.68 |

## Small run (6 splits)

| Model | Type | Vietnam<br>log CRPS | Laos<br>log CRPS | Thailand<br>log CRPS | **Mean<br>log CRPS** | Mean<br>CRPS | Mean coverage<br>10–90 |
|---|---|---|---|---|---|---|---|
| [chronos2](models/chronos2) | Foundation | [0.524](results/chronos2_vietnam/) | [0.680](results/chronos2_laos/) | [0.413](results/chronos2_thailand/) | **0.539** | 70.6 | 0.69 |
| [timestral](models/timestral) | Foundation | [0.467](results/timestral_vietnam/) | [0.744](results/timestral_laos/) | [0.435](results/timestral_thailand/) | **0.549** | 67.5 | 0.76 |
| [t0_gamma](models/t0_gamma) | Foundation | [0.491](results/t0_gamma_vietnam/) | [0.801](results/t0_gamma_laos/) | [0.428](results/t0_gamma_thailand/) | **0.573** | 67.9 | 0.72 |
| [timesfm3](models/timesfm3) | Foundation | [0.495](results/timesfm3_vietnam/) | [0.806](results/timesfm3_laos/) | [0.422](results/timesfm3_thailand/) | **0.574** | 72.4 | 0.72 |
| [mstl_arima](https://github.com/chap-models/mstl_arima) | CHAP | [0.557](results/mstl_arima_vietnam/) | [0.746](results/mstl_arima_laos/) | [0.434](results/mstl_arima_thailand/) | **0.579** | 74.1 | 0.65 |
| [tabpfn_ts](models/tabpfn_ts) | Foundation | [0.504](results/tabpfn_ts_vietnam/) | [0.846](results/tabpfn_ts_laos/) | [0.477](results/tabpfn_ts_thailand/) | **0.609** | 69.9 | 0.68 |
| [mantis](models/mantis) | Foundation | [0.617](results/mantis_vietnam/) | [0.741](results/mantis_laos/) | [0.489](results/mantis_thailand/) | **0.616** | 78.4 | 0.62 |
| [chap_pymc](https://github.com/dhis2-chap/chap_pymc) | CHAP | [0.537](results/chap_pymc_vietnam/) | [0.789](results/chap_pymc_laos/) | [0.593](results/chap_pymc_thailand/) | **0.640** | 73.8 | 0.68 |
| [seasonal_naive](models/seasonal_naive) | Baseline | [0.910](results/seasonal_naive_vietnam/) | [1.680](results/seasonal_naive_laos/) | [0.588](results/seasonal_naive_thailand/) | **1.059** | 113.6 | 0.59 |
| [chtorch](https://github.com/dhis2-chap/chtorch) | CHAP | [0.667](results/chtorch_vietnam/) | [2.112](results/chtorch_laos/) | [0.423](results/chtorch_thailand/) | **1.067** | 109.2 | 0.60 |

## Perfect future weather

The runs above use climatology as future weather (per province and calendar month, the mean over the training history). Observed = the real ERA5-Land values for the forecast months, as if the weather forecast were perfect.

| Model | Splits | Weather | Vietnam<br>log CRPS | Laos<br>log CRPS | Thailand<br>log CRPS | **Mean<br>log CRPS** |
|---|---|---|---|---|---|---|
| auto_regressive_v2 | 36 | climatology | [0.346](results/auto_regressive_monthly_v2_vietnam_h3_s36/) | [0.673](results/auto_regressive_monthly_v2_laos_h3_s36/) | [0.459](results/auto_regressive_monthly_v2_thailand_h3_s36/) | **0.493** |
| auto_regressive_v2 | 36 | observed | [0.344](results/auto_regressive_monthly_v2_vietnam_h3_s36_observed/) | [0.658](results/auto_regressive_monthly_v2_laos_h3_s36_observed/) | [0.460](results/auto_regressive_monthly_v2_thailand_h3_s36_observed/) | **0.487** |
| timestral | 6 | climatology | [0.467](results/timestral_vietnam/) | [0.744](results/timestral_laos/) | [0.435](results/timestral_thailand/) | **0.549** |
| timestral | 6 | observed | [0.465](results/timestral_vietnam_observed/) | [0.741](results/timestral_laos_observed/) | [0.440](results/timestral_thailand_observed/) | **0.549** |
| chap_pymc (control) | 6 | climatology | [0.537](results/chap_pymc_vietnam/) | [0.789](results/chap_pymc_laos/) | – | – |
| chap_pymc (control) | 6 | observed | [0.538](results/chap_pymc_vietnam_observed/) | [0.785](results/chap_pymc_laos_observed/) | – | – |

chap_pymc only uses weather from before the forecast, so its two rows should match; they do, up to sampling noise.

## Notes

- chap_pymc, chtorch (default config) and auto_regressive_v2 big runs ran on Fox.
- chronos2: the big run used every column chap passes as covariates; the small run only rainfall and temperature, like the other foundation models.
- timesfm3 only outputs the 0.1–0.9 quantiles, so its tails are cut off.
- No significance test yet.
