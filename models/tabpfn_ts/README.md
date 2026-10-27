# TabPFN-TS (CHAP wrapper)

> **Vibe-coded, not reviewed.** Written in an AI-assisted session (Oct 2026) to get a quick
> comparison running. It has not been checked line by line, tested beyond `chap eval`, or
> tuned. Treat the results as indicative only.

Zero-shot [TabPFN-TS](https://github.com/PriorLabs/tabpfn-time-series) (Prior Labs) through
chap. TabPFN is a foundation model for tables: each month becomes a row of features
(calendar, seasonal terms, covariates) and TabPFN predicts the target in context.

**Setup (once):** the local weights require accepting Prior Labs' licence.

1. Log in at https://ux.priorlabs.ai and accept the licence on the Licenses tab.
2. Copy your API key from https://ux.priorlabs.ai/account.
3. `export TABPFN_TOKEN="<your-api-key>"` before running chap.

The model runs **locally** (`TabPFNMode.LOCAL`); no data is sent to Prior Labs' API.
Telemetry is turned off with `TABPFN_DISABLE_TELEMETRY=1`.

- Target is modelled as `log1p(disease_cases)` and transformed back with `expm1`; forecasts
  are capped at 10x the location's highest recorded count and floored at 0.
- Rainfall and mean temperature are passed as known-future covariates.
- Each location is a separate table, so there is **no cross-learning** between locations.
- 100 quantiles (0.01-0.99) are requested directly and written as `sample_0..sample_99`.

Run: `make MODEL=tabpfn_ts DATA=vietnam`
