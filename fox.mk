# 36-split backtests on Fox (UiO Educloud), one Slurm job per dataset (fox.sbatch).
#
#   make -f fox.mk setup               # once: chap CLI (same commit as locally) on the module Python
#   make -f fox.mk pymc TEST=1         # 1 split on laos in the devel queue, ~10 min
#   make -f fox.mk pymc chtorch        # full runs; watch with squeue --me
#
# Results land in results/ as locally.

DATA ?= vietnam laos thailand
SPLITS ?= 36
PY313 := GCC/14.3.0 Python/3.13.5-GCCcore-14.3.0
# chtorch on 3.12 gets chap-core 1.0.17 (as on the Mac); on 3.13 it gets 2.5.1, which fails
PY312 := GCC/13.3.0 Python/3.12.3-GCCcore-13.3.0
CHAP := git+https://github.com/dhis2-chap/chap-core@607377a2c842ac9ea946598c860a3fa30437ce46

ifdef TEST
DATA := laos
SPLITS := 1
SBATCH_OPTS := --qos=devel --time=00:30:00
endif

submit = for d in $(DATA); do MODULES="$(2)" sbatch $(SBATCH_OPTS) fox.sbatch https://github.com/dhis2-chap/$(1) $$d $(SPLITS); done

.PHONY: setup pymc chtorch
setup:
	bash -lc 'module load $(PY313) && UV_PYTHON_DOWNLOADS=never uv tool install --force --python "$$(which python3)" $(CHAP)'

pymc:
	$(call submit,chap_pymc,$(PY313))

chtorch:
	$(call submit,chtorch,$(PY312))
