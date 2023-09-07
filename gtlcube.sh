#!/bin/bash

root=$1 #/archive/home/Xgam/fermi_data
dirname=$2 #"test"

scfile=$root/spacecraft/lat_spacecraft_merged.fits
evfile=$root/output/$dirname/gtmktime.fits 

zmax=90
dcostheta=0.025
binsz=1
outfile=$root/output/$dirname/gtltcube.fits 
chatter=4
clobber=yes


gtltcube scfile=$scfile evfile=$evfile zmax=$zmax dcostheta=$dcostheta \
    binsz=$binsz outfile=$outfile chatter=$chatter clobber=$clobber
