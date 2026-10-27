# Foundation models for dengue forecasting with CHAP

Each folder in `models/` is a CHAP model (`MLproject` + `train.py` + `predict.py`).
`input/` holds the chap_benchmarking datasets (Vietnam, Laos, Thailand, monthly admin-1), from
[climate-health-data](https://github.com/dhis2/climate-health-data) at commit `af362d5`.

Run one model on one dataset (needs the `chap` CLI):

```bash
make MODEL=chronos2                     # all three datasets + mean
make MODEL=chronos2 DATA=laos           # one dataset
make MODEL=https://github.com/dhis2-chap/chap_pymc
```

The backtest is the chap_benchmarking one: horizon 3, 6 splits, stride 1, trained once,
climatology future weather. Results go to `results/<model>_<data>/`.

| Model | What |
|---|---|
| `chronos2` | Chronos-2 zero-shot, log1p target, cross-learning |
| `chronos2_spatial` | `chronos2` + neighbour-incidence covariate (`adjacency.json`) |
| `timestral` | Timestral zero-shot |
| `tabpfn_ts` | TabPFN-TS (needs `~/.tabpfn_token`) |
| `mantis` | Mantis zero-shot, no covariates |
| `seasonal_naive` | Baseline |

`timestral`, `tabpfn_ts` and `mantis` are vibe coded; see the README in their folder.
