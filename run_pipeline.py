
#%%
import yaml
import argparse
import numpy
import os
import sys
sys.path.append("utils")

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

initial_step = config["initial_step"]

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

clobber = config["clobber"]

psf_theta_max = config["psf_theta_max"]
psf_nt_points = config["psf_nt_points"]
psf_ne_points = config["psf_ne_points"]

week_in = config["week_in"]
week_out = config["week_out"]

root = config["root"]

SC_FILE = f"{root}/spacecraft/lat_spacecraft_merged.fits"

ebinfile_txt=f"{root}/output/{OUT_LABEL}/utils/ebins.txt"
ebinfile_fits=f"{root}/output/{OUT_LABEL}/utils/ebins.fits"


GTSELECT_DICT = {'infile': f"{root}/output/{OUT_LABEL}/utils/gtselect_fits.txt",
                 'emin': Emin,
                 'emax': Emin,
                 'zmax': ZMAX,
                 'evclass': EVCLASS,
                 'evtype': EVTYPE,
                 'outfile': f"{root}/output/{OUT_LABEL}/gtselect.fits",
                 'chatter': 4,
                 'clobber': clobber,
                 'tmin': tmin,
                 'tmax': tmax}

GTMKTIME_DICT = {'evfile': f"{root}/output/{OUT_LABEL}/gtselect.fits",
                 'scfile': SC_FILE,
                 'filter': FILTER_CUT,
                 'roicut': 'no',
                 'outfile': f"{root}/output/{OUT_LABEL}/gtmktime.fits",
                 'clobber': clobber}

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
              'ebinalg': 'FILE',
              'ebinfile': ebinfile_fits,
              'clobber': clobber,
              'evtable': 'EVENTS',
              'sctable': 'SC_DATA',
              'efield': 'ENERGY',
              'tfield': 'TIME',
              }

GTLTCUBE_DICT = {'evfile': f"{root}/output/{OUT_LABEL}/gtmktime.fits",
                 'scfile':  SC_FILE,
                 'zmax': ZMAX,
                 'dcostheta': 0.025,
                 'binsz': 1,
                 'outfile': f"{root}/output/{OUT_LABEL}/gtltcube.fits",
                 'chatter': 4,
                 'clobber': clobber}

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
                   'clobber': clobber}



GTPSF_DICT =    {
    "expcube" : f"{root}/output/{OUT_LABEL}/gtltcube.fits",
    "outfile" : f"{root}/output/{OUT_LABEL}/gtpsf.fits",
    "irfs" : IRFS,
    "evtype" : EVTYPE,
    "ra": "",
    "dec": "",
    "emin" : Emin,
    "emax" : Emax,
    "thetamax" : psf_theta_max,
    "nenergies" : psf_ne_points,
    "ntheta" : psf_nt_points,
    'clobber': clobber,
}


# prepare data, step 0 
if initial_step < 1:
    os.makedirs(f"{root}/output/{OUT_LABEL}", exist_ok=True)
    fermi_data_dowloader(week_in, week_out, root).download_all()
    gtselect_utils(week_in, week_out,root,f"{root}/output/{OUT_LABEL}/utils").make_selection_txt()
    make_bin_txt(f"{root}/output/{OUT_LABEL}", Emin, Emax, Earr, nenergies).write()

#run fermi analysis
if initial_step < 2:
    gt_tools.gtselect(GTSELECT_DICT) # step 1
if initial_step < 3:
    gt_tools.gtmktime(GTMKTIME_DICT) # step 2
if initial_step < 4:
    gt_tools.gtbindef(GTBINDEF_DICT) # step 3
    gt_tools.gtbin(GTBIN_DICT)
if initial_step < 5:
    gt_tools.gtltcube(GTLTCUBE_DICT) # step4
if initial_step < 6:
    gt_tools.gtexpcube2(GTEXPCUBE2_DICT) # step 5
if initial_step < 7:
    gt_tools.gtpsf(GTPSF_DICT) # step 6
if initial_step < 8:
    gt_tools.make_hdf5(root, OUT_LABEL) # step 7


# gt_tools.gtselect(GTSELECT_DICT) # step 1
# gt_tools.gtmktime(GTMKTIME_DICT) # step 2
# gt_tools.gtbindef(GTBINDEF_DICT) # step 3
# gt_tools.gtbin(GTBIN_DICT)
# gt_tools.gtltcube(GTLTCUBE_DICT) # step4
# gt_tools.gtexpcube2(GTEXPCUBE2_DICT) # step 5
# gt_tools.gtpsf(GTPSF_DICT) # step 6
# gt_tools.make_hdf5(root, OUT_LABEL) # step 7
print_msg_box("done")

