#%%
from astropy.io import fits
import numpy as np
#%%
fits_file = "/lhome/ific/a/aamerio/data_artemisa/github/fermitools-scripts/sensitivity_map_128_dmhalos.fits"
f = fits.open("/lhome/ific/a/aamerio/data_artemisa/github/fermitools-scripts/sensitivity_map_128_dmhalos.fits")
# %%
f[2].header
#%%
data = {}
for key in f[2].data.columns.names:
    data[key] = f[2].data[key]
#%%
f[2].data["dnde"] #cm^-2 ph s^-1
#%%
f[2].data["flux"][0]*(12*128**2 / (4*np.pi))
#%%
f[4].data
#%%
np.median(f[4].data["CHANNEL1"])
#%%
indexes = [4, 3, 1, 0, 0]
#%%
min_flux = data["flux"][indexes]
data["min_flux"] = min_flux
data["mDM"] = [10, 30, 100, 300, 1000]
# %%
np.savez("sensitivity_map_128_dmhalos.npz", **data)
#%%
1*data["min_flux"]
#%%
# index_dict = {}
# index_dict[10] = 4
# index_dict[30] = 3
# index_dict[100] = 1
# index_dict[300] = 0
# index_dict[1000] = 0
#%%
min_flux
# f[2].data["flux"]
# #%%
# f[1].data["flux"]
# # %%
# f[1].data["e_min"]
# # %%
# f[1].data["e_max"]
# %%
from astropy.table import Table

tab = Table.read('fits_file','DIFF_FLUX')
print(tab['e_min'], tab['e_max'], tab['flux'])
# %%
