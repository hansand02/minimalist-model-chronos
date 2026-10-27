# Mantis (CHAP wrapper)

> **Vibe-coded, not reviewed.** Written in an AI-assisted session (Oct 2026) to get a quick
> comparison running. It has not been checked line by line, tested beyond `chap eval`, or
> tuned. Treat the results as indicative only.

Zero-shot [Mantis](https://github.com/carsondudley1/Mantis) through chap, using the
8-step-horizon checkpoint without covariates (`mantis_8w_nocov.pt`, 1.2 GB, downloaded once
to `~/.cache/mantis` by `train.py`).

Known mismatches with how Mantis was trained:

- Mantis is trained on **weekly** data; we feed it monthly data and keep the first steps of
  the 8-step forecast.
- Its covariate slot only takes another epidemiological series (cases / hospitalisations /
  deaths), so climate is **not used**.
- Missing case values are interpolated, because Mantis cannot take NaN.
- Mantis already works on `log1p` counts internally, so no extra transform is applied.
- It outputs 9 quantiles (0.05-0.95); levels outside that range repeat the outermost quantile,
  so the tails are too narrow.
- One location at a time, so **no cross-learning**.

Run: `make MODEL=mantis DATA=vietnam`
