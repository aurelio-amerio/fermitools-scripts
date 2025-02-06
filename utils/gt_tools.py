# %%
import numpy as np
# from gt_apps import filter, maketime, counts_map, expCube, gtexpcube2
import gt_apps 
import os
from GtApp import GtApp
# %%
gtbindef_app = GtApp('gtbindef', 'evtbin')
gtpsf_app = GtApp('gtpsf', 'Likelihood')

#%%

def gtselect(gtselect_dict):
    """
    Calls gtselect from Science Tools.
    """
    print('Running gtselect...')
    
    for key in gtselect_dict.keys():
        gt_apps.filter[key] = gtselect_dict[key]

    gt_apps.filter.run()

    return

def gtmktime(maketime_dict):
    """
    Calls gtmktime from Science Tools.
    """
    print('Running gtmktime...')

    for key in maketime_dict.keys():
        gt_apps.maketime[key] = maketime_dict[key]

    gt_apps.maketime.run()

    return 

def gtbindef(gtbindef_dict):
    """
    Calls gtbin from Science Tools.

    """
    print('Running gtbindef...')
    for key in gtbindef_dict.keys():
        gtbindef_app[key] = gtbindef_dict[key]

    gtbindef_app.run()

    return 

def gtbin(gtbin_dict):
    """
    Calls gtbin from Science Tools.

    """
    print('Running gtbin...')
    for key in gtbin_dict.keys():
        gt_apps.counts_map[key] = gtbin_dict[key]

    gt_apps.counts_map.run()

    return 

def gtltcube(expcube_dict):
    """
    Calls gtltcube from Science Tools.


    """
    print('Running gtltcube...')
    for key in expcube_dict.keys():
        gt_apps.expCube[key] = expcube_dict[key]

    gt_apps.expCube.run()

    return
    

def gtexpcube2(expcube2_dict):
    """
    Calls gtexpcube2 from Science Tools.

    """

    print('Running gtexpcube2...')
    for key in expcube2_dict.keys():
        gt_apps.gtexpcube2[key] = expcube2_dict[key]

    gt_apps.gtexpcube2.run()

    return


def gtpsf(gtpsf_dict):
    """
    Calls gtpsf from Science Tools

    """
    print('Running gtpsf...')
    for key in gtpsf_dict.keys():
        gtpsf_app[key] = gtpsf_dict[key]

    gtpsf_app.run()

    return

def make_hdf5(root, dirname):
    print("Converting fits files to hdf5")
    os.makedirs(f"{root}/output/{dirname}/hdf5", exist_ok=True)
    os.system(f"fits2hdf -c gzip {root}/output/{dirname} {root}/output/{dirname}/hdf5")
    return

# def gtEbindef(ebinning_array, file_name='ebinning.txt'):
#     """
#     Produces a fits file defining the enrgy binning to fed gtbin.

# 	Parameters
# 	----------
#     ebinning_array: numpy array
#         array in which the energy binnin is defined.
#     file_name : str
#         file name for the output txt file. (Default = 'ebinning.txt')

#     Returns
#     -------
#     str
#         file name of the fits file created
#     """
#     if not os.path.exists(X_OUT):
#         os.makedirs(X_OUT)
#     txt_file_name = os.path.join(X_OUT, file_name)
#     txt_file = open(txt_file_name, 'w')
#     fits_file_name = os.path.join(X_OUT,
#                                   file_name.replace('.txt', '.fits'))
#     for emin, emax in zip(ebinning_array[:-1], ebinning_array[1:]):
#         txt_file.write('%.4f %.4f\n'%(emin, emax))
#     txt_file.close()
#     os.system('gtbindef bintype=E binfile=%s outfile=%s energyunits=MeV' \
#                   %(txt_file_name, fits_file_name))
#     print('Created %s...'%fits_file_name)
#     return fits_file_name
