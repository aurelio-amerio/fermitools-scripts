#!/bin/bash

# evclass
# 2048: "SOURCEVETO",
# 1024: "ULTRACLEANVETO",
# 512:  "ULTRACLEAN",
# 256:  "CLEAN",
# 128:  "SOURCE",
# 64:   "TRANSIENT010",
# 16:   "TRANSIENT020"


root=$1 #/archive/home/Xgam/fermi_data
dirname=$2 #"test"

infile=$root/utils/gtselect_fits.txt
outfile=$root/output/$dirname/gtselect.fits 
emin=$3 #1000 
emax=$4 #10000 
evclass=2048 
evtype=1 
ra=INDEF 
dec=INDEF 
rad=INDEF 
tmin=INDEF 
tmax=INDEF 
zmax=90 
chatter=4
clobber=yes
#default for zmax is 180

gtselect infile=$infile outfile=$outfile emin=$emin emax=$emax evclass=$evclass evtype=$evtype ra=$ra dec=$dec rad=$rad tmin=$tmin tmax=$tmax zmax=$zmax clobber=$clobber chatter=$chatter