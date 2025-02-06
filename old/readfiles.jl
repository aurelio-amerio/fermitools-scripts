#%%
using FITSIO
#%%
basepath = "/lhome/ific/a/aamerio/data/fermi/output/sourceveto_nside2048_front_1_10_GeV_w9-745_v2/"
filepath = "$basepath/gtselect.fits"

f = FITS(filepath, "r") 
GTI_gtselect= read(f["GTI"], "START")
close(f)
#%%
filepath = "$basepath/gtmktime.fits"
f = FITS(filepath, "r") 
GTI_gtmktime= read(f["GTI"], "START")
close(f)
#%%
filepath = "$basepath/gtbin.fits"
f = FITS(filepath, "r") 
GTI_gtbin= read(f["GTI"], "START")
close(f)
#%%
filepath = "$basepath/gtltcube.fits"
f = FITS(filepath, "r") 
GTI_gtltcube= read(f["GTI"], "START")
close(f)
#%%
photondir = "/lhome/ific/a/aamerio/data/fermi/photon"

file = "$photondir/lat_photon_weekly_w9_p305_v001.fits"
f = FITS(filepath, "r")
tstart9=read(f["GTI"],"START")
tstop9=read(f["GTI"],"STOP")
close(f)

file = "$photondir/lat_photon_weekly_w745_p305_v001.fits"
f = FITS(filepath, "r")
tstart745=read(f["GTI"],"START")
tstop745=read(f["GTI"],"STOP")
close(f)

#%%
spacecraft_file = "/lhome/ific/a/aamerio/data/fermi/spacecraft/lat_spacecraft_merged.fits"
f = FITS(spacecraft_file, "r")

read(f["SC_DATA"],"START")
read(f["SC_DATA"],"STOP")