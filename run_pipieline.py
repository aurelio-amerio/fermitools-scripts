
#%%
import yaml
import argparse
import numpy
import os

from utils.download_fermi_data import fermi_data_dowloader
from utils.make_selection_txt import gtselect_utils
from utils.make_bin_txt import make_bin_txt
from utils import gt_tools
from utils.msgbox import print_msg_box
#%%
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", type=str, default="config/config.yaml")

args = parser.parse_args()
config_file = args.config
#%%
with open(config_file, "r") as file:
    config = yaml.safe_load(file)

#%%
CBLUE = '\033[34m'
CEND = '\033[0m'
def print_msg_box(msg, indent=1, width=None, title=None):
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(CBLUE + box + CEND)
#%%

ZMAX = config["ZMAX"]
EVCLASS = config["EVCLASS"]
EVTYPE = config["EVTYPE"]
IRFS = config["IRFS"]
HPX_MAP_ORDER = config["healpixorder"]
FILTER_CUT = 'DATA_QUAL==1&&LAT_CONFIG==1&&LAT_MODE==5&&IN_SAA!=T&&((ABS(ROCK_ANGLE)<52))'
OUT_LABEL = config["OUT_LABEL"]
Emin = config["Emin"]
Emax = config["Emax"]
Earr = config["Earr"]
tmin = config["tmin"]
tmax = config["tmax"]
nenergies = config["nenergies"]

psf_theta_max = config["psf_theta_max"]
psf_npoints = config["psf_npoints"]

week_in = config["week_in"]
week_out = config["week_out"]

root = config["root"]

SC_FILE = f"{root}/spacecraft/lat_spacecraft_merged.fits"

ebinfile_txt=f"{root}/output/{OUT_LABEL}/utils/ebins.txt"
ebinfile_fits=f"{root}/output/{OUT_LABEL}/utils/ebins.fits"


GTSELECT_DICT = {'infile': f"{root}/utils/gtselect_fits.txt",
                 'emin': Emin,
                 'emax': Emin,
                 'zmax': ZMAX,
                 'evclass': EVCLASS,
                 'evtype': EVTYPE,
                 'outfile': f"{root}/output/{OUT_LABEL}/gtselect.fits",
                 'chatter': 4,
                 'clobber': 'no',
                 'tmin': tmin,
                 'tmax': tmax}

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
              'scfile': SC_FILE, 
              'outfile': f"{root}/output/{OUT_LABEL}/gtbin.fits",
              'algorithm': 'HEALPIX',
              'hpx_ordering_scheme': 'RING',
              'hpx_order': HPX_MAP_ORDER,
              'hpx_ebin': 'yes',
              "hpx_region": "",
              'coordsys': 'GAL',
              'ebinfile': ebinfile_fits,
              'clobber': 'no',
              'evtable': 'EVENTS',
              'sctable': 'SC_DATA',
              'efield': 'ENERGY',
              'tfield': 'TIME'
              }

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
                   'ebinfile': ebinfile_fits,
                   'bincalc': 'CENTER',
                   'clobber': 'no'}



GTPSF_DICT =    {
    "expcube" : f"{root}/output/{OUT_LABEL}/gtltcube.fits",
    "outfile" : f"{root}/output/{OUT_LABEL}/gtpsf.fits",
    "irfs" : IRFS,
    "evtype" : EVTYPE,
    "emin" : Emin,
    "emax" : Emax,
    "nenergies" : nenergies,
    "thetamax" : psf_theta_max,
    "ntheta" : psf_npoints,
}


# prepare data
os.makedirs(f"{root}/output/{OUT_LABEL}", exist_ok=True)
fermi_data_dowloader(week_in, week_out, root).download_all()
gtselect_utils(week_in, week_out,f"{root}/output/{OUT_LABEL}").make_selection_txt()
make_bin_txt(f"{root}/output/{OUT_LABEL}", Emin, Emax, Earr, nenergies).write()

#run fermi analysis
gt_tools.gtselect(GTSELECT_DICT)
gt_tools.gtmktime(GTMKTIME_DICT)
gt_tools.gtbindef(GTBINDEF_DICT)
gt_tools.gtbin(GTBIN_DICT)
gt_tools.gtltcube(GTLTCUBE_DICT)
gt_tools.gtexpcube2(GTEXPCUBE2_DICT)
gt_tools.gtpsf(GTPSF_DICT)
gt_tools.make_hdf5(root, OUT_LABEL)
print_msg_box("done")

