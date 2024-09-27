#!/bin/bash

root=$1 #/archive/home/Xgam/fermi_data
dirname=$2 #"test"

scfile=$root/utils/spacecraft_list.txt
evfile=$root/output/$dirname/gtmktime.fits 

zmax=90
dcostheta=0.025
binsz=1
outfile=$root/output/$dirname/gtltcube.fits 
chatter=4
clobber=yes


gtltcube scfile=$scfile evfile=$evfile evtable="EVENTS" zmin=0.0 zmax=$zmax dcostheta=$dcostheta \
    binsz=$binsz outfile=$outfile chatter=$chatter clobber=$clobber mode="ql"
