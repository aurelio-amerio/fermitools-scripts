#!/bin/bash

root=$1 #/archive/home/Xgam/fermi_data
dirname=$2 #"test"

evfile=$root/output/$dirname/gtmktime.fits
algorithm=HEALPIX
scfile=$root/spacecraft/lat_spacecraft_merged.fits
hpx_ordering_scheme=RING
hpx_order=$3 # to change back to 11
coordsys=GAL
hpx_ebin=yes
ebinalg=FILE
ebinfile_txt=$root/utils/ebins.txt
ebinfile_fits=$root/utils/ebins.fits
outfile=$root/output/$dirname/gtbin.fits
clobber=yes
hpx_region=""

echo "creating ebinning file"
gtbindef bintype=E binfile=$ebinfile_txt outfile=$ebinfile_fits energyunits=MeV

echo "running gtbin"

gtbin evfile=$evfile scfile=$scfile outfile=$outfile algorithm=$algorithm \
    ebinalg=$ebinalg hpx_ordering_scheme=$hpx_ordering_scheme hpx_order=$hpx_order \
    coordsys=$coordsys hpx_ebin=$hpx_ebin ebinfile=$ebinfile_fits \
    clobber=$clobber hpx_region=$hpx_region
