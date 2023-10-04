#!/bin/bash

root=$1 #/archive/home/Xgam/fermi_data
dirname=$2 #"test"

expcube=$root/output/$dirname/gtltcube.fits #it's the livetime cube
outfile=$root/output/$dirname/gtpsf.fits
irfs=P8R3_SOURCEVETO_V3
event_type_selections=$5 #1
source_right_ascensio=0
source_declination=0
emin=$3 #1000
emax=$4 #10000
Ne=200
max_radius=20
Nangle=300


gtpsf expcube=$expcube outfile=$outfile irfs=$irfs evtype=$event_type_selections \
    ra=$source_right_ascensio dec=$source_declination emin=$emin emax=$emax \
    nenergies=$Ne thetamax=$max_radius ntheta=$Nangle

