# TODO

Status as of 2026-10-26: restarted from scratch. Old results were on untrusted data and are
archived in `../archive/`. Run models with `make` (see README).

## 1. Verified preliminary results

Goal: how good are the time-series foundation models zero-shot, compared with simple
baselines and pymc?

- [x] Wrap Timestral, Mantis and TabPFN-TS as chap models (`models/`)
- [x] log1p target (+ 10x cap on extreme quantiles) for Chronos-2, Timestral, TabPFN-TS
- [x] Datasets: chap_benchmarking set (Vietnam 63, Laos 18, Thailand 77 provinces), `input/`
- [x] Protocol: chap_benchmarking (horizon 3, 6 splits, stride 1, climatology), `Makefile`
- [ ] Run every model in `models/` + chap_pymc + mstl_arima on all three datasets
- [ ] Compare with the chap models' scores on chap-benchmarking.dhis2.org (needs API token)
- [ ] Score: CRPS and CRPS log1p, bootstrap CI over locations
- [ ] Write up in a results page

## 2. Spatial cross-learning ("liquid flowing" between provinces and over time)

Idea: let outbreaks in one province inform its neighbours, with the influence spreading
over the map and decaying over time, like a liquid flowing through the province graph.

- [x] Province polygons: `input/*.geojson`
- [ ] Adjacency graph (provinces sharing a border)
- [ ] Diffusion features: neighbour incidence at lags 1-3, weighted by graph distance and
      decaying with time (e.g. heat-kernel / exponential decay on the graph)
- [ ] Feed them as covariates to Chronos-2 and TabPFN-TS; compare with plain cross-learning
- [ ] Ablation: Chronos-2 with `cross_learning=False` (is the current cross-learning doing anything?)
- [ ] Variant: Chronos-2 / Timestral cross-learning restricted to regions or neighbourhoods
- [ ] Tune on Vietnam only, test once on the held-out datasets

## 3. Later

- [ ] Fine-tune Chronos-2 on OpenDengue (excluding eval countries) and compare with zero-shot
      (thesis issue #2)
- [ ] Cross-learning between diseases (Thai multi-disease data in the Mantis repo `eval/`,
      or DHIS2 instances with several diseases per district)
- [ ] Small, pre-chosen feature set: lagged climate (1-3 months), incidence per capita,
      growth rate, cases over the past 12-24 months (immunity proxy)
- [ ] Ensemble of pymc + best foundation model (from existing `eval.nc` files)
- [ ] Calibrate the intervals (coverage is well below 0.80 for most models)
- [ ] Explain why Chronos-2's log CRPS on Vietnam got worse with log1p (0.328 -> 0.577)
- [ ] Rotate the TabPFN API key (it was pasted in a chat transcript); key lives in `~/.tabpfn_token`
- [ ] Standard chap baselines that need R/INLA (chap_auto_ewars, INLA_baseline_model)
