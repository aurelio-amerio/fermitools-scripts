#!/bin/bash

JOB_ENVIRONMENT="fermi"
eval "$(conda shell.bash hook)"
conda activate $JOB_ENVIRONMENT

cd /lhome/ific/a/aamerio/github/fermitools-scripts
./run_pipeline2.sh