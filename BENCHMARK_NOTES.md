# Chronos-2 benchmark notes (21-22 Sep 2026)

> **Vibe-coded, indicative only.** These runs were produced in an exploratory
> AI-assisted session. Nothing here has been peer-reviewed or reproduced, the
> scoring scripts were written ad hoc, and several variants are no longer in
> this repo. Treat the numbers as a direction to investigate, not as evidence.

## Setup

- Data: `dhis2/climate-health-data` (LAO 18 provinces, VNM 63, THA 77), monthly.
- Protocol: `chap eval`, 12 splits x 3-month horizon, stride 1 (as recommended
  in the `mstl_arima` README).
- Baseline: [`chap-models/mstl_arima`](https://github.com/chap-models/mstl_arima)
  (STL + AutoARIMA, no covariates).
- Skill = 1 - CRPS_model / CRPS_baseline, 95% CI bootstrapped over locations.
  CRPS itself is an error measure, so lower is better; the skill score flips the
  sign so that **positive = better than the baseline**. +8.5% means the model's
  CRPS was 8.5% lower (48.9 vs 53.5 on LAO).

## Results: skill vs mstl_arima (positive = lower CRPS = better)

| Model | LAO | VNM | THA |
|---|---|---|---|
| Chronos-2, zero-shot (this repo) | -2.1% (ns) | +4.5% (ns) | **-16.8% worse** |
| Chronos-2 + log1p + seasonal/lagged climate covariates | **+8.5%** | **+7.9%** | -1.4% (ns) |
| Ensemble: Chronos + pymc + baseline (LAO only) | **+11.7%** | - | - |

ns = not significantly different from the baseline.

### Raw CRPS behind those percentages (lower is better)

| Model | LAO | VNM | THA |
|---|---|---|---|
| mstl_arima (baseline) | 53.46 | 71.00 | 12.35 |
| Chronos-2, zero-shot | 54.60 | 67.77 | 14.42 |
| Chronos-2 variant | 48.94 | 65.39 | 12.52 |
| Ensemble | 47.23 | - | - |

The baseline uses no covariates, so its CRPS is identical under both weather
settings below; that is a useful sanity check on the comparison.

### chap_pymc: 1 split only, not comparable to the table above

pymc is slow (~5 h for the full 12-split protocol on all three datasets), so it
was run on a single split. These CRPS values are scored on exactly the forecasts
pymc produced (target months Oct-Dec), with every other model restricted to the
same rows:

| Model | LAO (48 forecasts) | VNM (189) | THA (231) |
|---|---|---|---|
| mstl_arima | 46.55 | 98.44 | **12.21** |
| Chronos-2 variant | 37.82 | 88.83 | 13.82 |
| chap_pymc | **37.31** | 93.20 | 22.49 |

One split is 3 months per location, so only the THA gap (pymc ~84% worse than
the baseline) is larger than the noise. On LAO and VNM, nothing separates them.

Weather provider: the zero-shot row was run on chap 2.1.0 (observed future
weather); the variant and ensemble rows on chap 2.3.1 with `climatology`. The
variant scored the same either way (48.94 climatology vs 49.52 observed on LAO),
which is what "climate covariates added almost nothing" means.

The variant model (log1p target, month sin/cos, lagged climate, cap on extreme
quantiles) is **not in this repo** - it was reverted along with the rest of the
session's experiments.

Chap's own `evaluate-ensemble` (chap-core >= 2.3.1) fitted these weights on
held-out data: Chronos 67%, pymc 28%, mstl_arima 5%.

## Things worth knowing

- **Climate covariates added almost nothing.** Scores were the same whether the
  model saw observed future weather or climatology. The skill comes from the
  foundation model plus the log transform, not from climate information.
- **chap 2.1.0 leaks future weather**: it passes the observed future covariates
  to the model. chap 2.3.1 defaults to `climatology`. Use 2.3.1+ for anything
  that should reflect production conditions.
- **Intervals are too narrow** for every model tried, baseline included
  (10-90 coverage ~0.70 against a 0.80 target).
- **Also tried and dropped**: TimesFM 3.0 (no consistent skill; weights are
  non-commercial licensed) and chap_pymc (84% worse than baseline on THA, but
  only one split was run, so that number is weak).
- **Not held out**: the variant's design was tuned while looking at Vietnamese
  data, so the VNM result is optimistic.

## If picking this up again

1. Re-derive the variant's settings on one dataset only, then test on the others.
2. Ablate the covariates - the evidence suggests they are not doing any work.
3. Calibrate the intervals (coverage is ~0.70, should be 0.80).
4. Run the baseline and any candidate with the same chap version and the same
   `future-weather-provider`.
