# Backtest one model on the chap_benchmarking datasets, with its setup:
# horizon 3, 6 splits, stride 1, trained once, climatology future weather.
#
#   make MODEL=chronos2                     # all three datasets + average
#   make MODEL=chronos2 DATA=laos           # one dataset
#   make MODEL=https://github.com/dhis2-chap/chap_pymc
#   make MODEL=chronos2 HORIZON=3 SPLITS=36     # longer test window: 36 splits, ~3 years
#
# MODEL is a folder in models/ or a GitHub URL. Output per dataset goes to
# results/<model>_<data>/ (eval.nc, eval.html, metrics.csv, eval.log). A dataset whose
# metrics.csv is newer than the model's files is not rerun.

SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

MODEL ?= chronos2
DATA ?= vietnam laos thailand
HORIZON ?= 3
SPLITS ?= 6

NAME := $(notdir $(MODEL))
MODEL_PATH := $(if $(findstring ://,$(MODEL)),$(MODEL),models/$(MODEL))
# Runs with other than the chap_benchmarking horizon/splits get their own folders
SUFFIX := $(if $(filter-out 3_6,$(HORIZON)_$(SPLITS)),_h$(HORIZON)_s$(SPLITS))
METRICS := $(foreach d,$(DATA),results/$(NAME)_$(d)$(SUFFIX)/metrics.csv)
export TABPFN_TOKEN ?= $(shell cat ~/.tabpfn_token 2>/dev/null)

.PHONY: eval
eval: $(METRICS)
	@python3 summary.py $(METRICS)

results/$(NAME)_%$(SUFFIX)/metrics.csv: input/%.csv $(wildcard $(MODEL_PATH)/*)
	mkdir -p $(@D)
	chap eval --model-name $(MODEL_PATH) --dataset-csv $< --output-file $(@D)/eval.nc \
		--backtest-params.n-periods $(HORIZON) --backtest-params.n-splits $(SPLITS) \
		--backtest-params.stride 1 --backtest-params.n-retrain 1 \
		--run-config.run-directory-type latest --plot 2>&1 | tee $(@D)/eval.log
	chap export-metrics --input-files $(@D)/eval.nc --output-file $@
