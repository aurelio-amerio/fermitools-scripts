#/bin/bash
root=$1 #/archive/home/Xgam/fermi_data
dirname=$2 #"test"

scfile=$root/spacecraft/lat_spacecraft_merged.fits
evfile=$root/output/$dirname/gtselect.fits 
filter='DATA_QUAL==1&&LAT_CONFIG==1&&LAT_MODE==5&&IN_SAA!=T&&((ABS(ROCK_ANGLE)<52))'
roicut=no
outfile=$root/output/$dirname/gtmktime.fits
clobber=yes

gtmktime scfile=$scfile filter=$filter roicut=$roicut evfile=$evfile outfile=$outfile clobber=$clobber