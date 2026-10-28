#!/bin/bash
# One model on one dataset on Fox:  [WEATHER=observed] sbatch fox.sbatch <MODEL> <DATA> [SPLITS]  (see fox.mk)
#SBATCH --account=ec12
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --output=slurm-%j.log

module load ${MODULES:-GCC/14.3.0 Python/3.13.5-GCCcore-14.3.0}  # pytensor needs a C compiler
export UV_PYTHON_DOWNLOADS=never  # use the module's Python
# Own working folder per job, so parallel jobs don't share runs/<model>/latest
work=work/$2_$(basename $1)${WEATHER:+_$WEATHER} && mkdir -p $work results
ln -sfn $PWD/{Makefile,summary.py,input,models,results} $work/
make -C $work MODEL=$1 DATA=$2 SPLITS=${3:-36}
