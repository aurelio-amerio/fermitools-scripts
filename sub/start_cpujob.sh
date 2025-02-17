#!/bin/bash

JOB_ENVIRONMENT="fermipy"
eval "$(conda shell.bash hook)"
conda activate $JOB_ENVIRONMENT

cd /lhome/ific/a/aamerio/github/fermitools-scripts
python run_pipeline.py --config $1