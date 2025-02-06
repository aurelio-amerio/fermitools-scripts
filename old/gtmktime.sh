#/bin/bash
root=$1 #/archive/home/Xgam/fermi_data
dirname=$2 #"test"

scfile=$root/utils/spacecraft_list.txt
evfile=$root/output/$dirname/gtselect.fits 
filter="DATA_QUAL==1&&LAT_CONFIG==1&&LAT_MODE==5&&IN_SAA!=T&&((ABS(ROCK_ANGLE)<52))"
roicut=no
outfile=$root/output/$dirname/gtmktime.fits
clobber=yes

# gtmktime scfile=$scfile sctable="SC_DATA" filter=$filter roicut=$roicut evfile=$evfile evtable="EVENTS" outfile=$outfile \
#     clobber=$clobber apply_filter=yes header_obstimes=yes \
#     tstart=0.0 tstop=0.0 gtifile="default" mode="ql" overwrite=no

gtmktime scfile=$scfile filter=$filter roicut=$roicut evfile=$evfile outfile=$outfile \
    clobber=$clobber