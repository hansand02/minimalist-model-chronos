# Timestral (CHAP wrapper)

> **Vibe-coded, not reviewed.** Written in an AI-assisted session (Oct 2026) to get a quick
> comparison running. It has not been checked line by line, tested beyond `chap eval`, or
> tuned. Treat the results as indicative only.

Zero-shot [Timestral-209M](https://github.com/mistralai/timestral) (Mistral) through chap.

- Target is modelled as `log1p(disease_cases)` and transformed back with `expm1`; forecasts
  are capped at 10x the location's highest recorded count and floored at 0.
- Rainfall and mean temperature are passed as known-future covariates.
- Each location is a separate series, so there is **no cross-learning** between locations.
- Timestral's 21 quantiles are interpolated to 100 levels (0.01-0.99) and written as
  `sample_0..sample_99`, the same grid as the Chronos-2 model in the repo root.

Run: `make MODEL=timestral DATA=vietnam`
