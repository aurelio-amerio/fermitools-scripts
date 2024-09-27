
#%%
import yaml
import argparse
import numpy
import os

from utils.download_fermi_data import fermi_data_dowloader
from utils.make_selection_txt import gtselect_utils
from utils.make_bin_txt import make_bin_txt
#%%
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", type=str, default="config/config.yaml")

args = parser.parse_args()
config_file = args.config
#%%
config_file = "config/config.yaml"
with open(config_file, "r") as file:
    config = yaml.safe_load(file)

#%%

ZMAX = 90
EVCLASS = config["EVCLASS"]
EVTYPE = config["EVTYPE"]
IRFS = config["IRFS"]
HPX_MAP_ORDER = config["healpixorder"]
FILTER_CUT = 'DATA_QUAL==1&&LAT_CONFIG==1&&LAT_MODE==5&&IN_SAA!=T' +\
    '&&((ABS(ROCK_ANGLE)<52))'

OUT_LABEL = config["OUT_LABEL"]
Emin = config["Emin"]
Emax = config["Emax"]
Earr = config["Earr"]
nenergies = config["nenergies"]

week_in = config["week_in"]
week_out = config["week_out"]

root = config["root"]

SC_FILE = f"{root}/spacecraft/lat_spacecraft_merged.fits"

ebinfile_txt=f"{root}/utils/ebins.txt"
ebinfile_fits=f"{root}/utils/ebins.fits"


GTSELECT_DICT = {'infile': f"{root}/utils/gtselect_fits.txt",
                 'emin': Emin,
                 'emax': Emin,
                 'zmax': ZMAX,
                 'evclass': EVCLASS,
                 'evtype': EVTYPE,
                 'outfile': f"{root}/output/{OUT_LABEL}/gtselect.fits",
                 'chatter': 4,
                 'clobber': 'no',
                 'tmin': 'INDEF',
                 'tmax': 'INDEF'}

GTMKTIME_DICT = {'evfile': f"{root}/output/{OUT_LABEL}/gtselect.fits",
                 'scfile': SC_FILE,
                 'filter': FILTER_CUT,
                 'roicut': 'no',
                 'outfile': f"{root}/output/{OUT_LABEL}/gtmktime.fits",
                 'clobber': 'no'}

GTBINDEF_DICT = {
    "bintype":"E", 
    "binfile": ebinfile_txt, 
    "outfile": ebinfile_fits, 
    "energyunits": "MeV"
}

GTBIN_DICT = {'evfile': f"{root}/output/{OUT_LABEL}/gtmktime.fits",
              'algorithm': 'HEALPIX',
              'scfile': SC_FILE,
              'hpx_ordering_scheme': 'RING',
              'hpx_order': HPX_MAP_ORDER,
              'coordsys': 'GAL',
              'hpx_ebin': 'yes',
              'ebinalg': 'FILE',
              'ebinfile': ebinfile_fits,
              'outfile': f"{root}/output/{OUT_LABEL}/gtbin.fits",
              'clobber': 'no'}

GTLTCUBE_DICT = {'evfile': f"{root}/output/{OUT_LABEL}/gtmktime.fits",
                 'scfile':  SC_FILE,
                 'zmax': ZMAX,
                 'dcostheta': 0.025,
                 'binsz': 1,
                 'outfile': f"{root}/output/{OUT_LABEL}/gtltcube.fits",
                 'chatter': 4,
                 'clobber': 'no'}

GTEXPCUBE2_DICT = {'infile': f"{root}/output/{OUT_LABEL}/gtltcube.fits",
                   'cmap': f"{root}/output/{OUT_LABEL}/gtbin.fits",
                   'irfs': IRFS,
                   'evtype': EVTYPE,
                   'hpx_ordering_scheme': 'RING',
                   'hpx_order': HPX_MAP_ORDER,
                   'outfile': f"{root}/output/{OUT_LABEL}/gtexpcube2.fits",
                   'ebinalg': 'FILE',
                   'ebinfile': f"{root}/output/{OUT_LABEL}/gtbin.fits",
                   'bincalc': 'CENTER',
                   'clobber': 'no'}


# prepare data
fermi_data_dowloader(week_in, week_out, root).download_all()
gtselect_utils(week_in, week_out, root).make_selection_txt()
make_bin_txt(root, Emin, Emax, Earr, nenergies).write()