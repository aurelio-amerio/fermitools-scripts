# fermitools-scripts
This repository contains a short series of scripts needed to obtain the fits files for for the simulator used in "Extracting the gamma-ray source-count distribution below the Fermi-LAT detection limit with deep learning" (https://arxiv.org/abs/2302.01947).

## Requirements
The scripts are written in Bash and Python 3 and require the following packages:
- The fermi tools as installed via the official conda channel (`conda create -n fermi -c conda-forge -c fermi fermitools numpy=1.20`)
- tqdm (`conda install tqdm`)

## Usage
It is recommended to run the scripts through the `run_pipeline.sh` script with the desired configuration.
The user is supposed to edit the `run_pipeline.sh` script to set the correct paths to the data and the output directory. 

The `run_pipeline.sh` script will run the following scripts:
- `download_fermi_data.py`: downloads the data from the Fermi-LAT data server
- `make_bin_txt.py`: creates the energy binning file for the `gtselect` tool
- `make_selection_txt.py`: creates the week selection file for the `gtselect` tool

The `run_pipeline.sh` script will then run the fermi-tools suite to create the fits files, which will appear in the output folder under the specified directory name.
- `gtselect`
- `gtmktime`
- `gtbin`
- `gtltcube`
- `gtexpcube2`
- `gtpsf`

