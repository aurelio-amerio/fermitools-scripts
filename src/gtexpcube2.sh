#!/bin/bash

root=$1 #/archive/home/Xgam/fermi_data
dirname=$2 #"test"

infile=$root/output/$dirname/gtltcube.fits 
cmap=$root/output/$dirname/gtbin.fits 
irfs="P8R3_SOURCEVETO_V3"
evtype=$3 #1
hpx_ordering_scheme=RING
hpx_order=$4 #11
outfile=$root/output/$dirname/gtexpcube2.fits 
ebinalg=FILE
ebinfile=$root/utils/ebins.fits
bincalc=CENTER
clobber=yes


gtexpcube2 infile=$infile cmap=$cmap outfile=$outfile irfs=$irfs \
    evtype=$evtype hpx_ordering_scheme=$hpx_ordering_scheme \
    hpx_order=$hpx_order ebinalg=$ebinalg ebinfile=$ebinfile \
    bincalc=$bincalc clobber=$clobber