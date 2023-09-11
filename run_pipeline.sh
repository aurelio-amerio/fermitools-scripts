#!/bin/bash
root="/lhome/ific/a/aamerio/data/fermi"
dirname="sourceveto_nside2048_front_1_200_GeV"
weak_in=9
weak_out=795 #795
Emin=1000 # 1 GeV
Emax=200000 # 200 GeV
nenergies=30
healpixorder=11 #11

# evclass
# 2048: "SOURCEVETO",
# 1024: "ULTRACLEANVETO",
# 512:  "ULTRACLEAN",
# 256:  "CLEAN",
# 128:  "SOURCE",
# 64:   "TRANSIENT010",
# 16:   "TRANSIENT020"
evclass=2048
evtype=1 #front

dowload_data=1
run_analysis=1
hdf5=1
cleanup=1

mkdir -p $root/output/$dirname

if [ $dowload_data = 1 ]; then
    echo "Downloading data"
    python src/download_fermi_data.py -r $root --weak_in $weak_in --weak_out $weak_out # download data
    python src/make_bin_txt.py -r $root --Emin $Emin --Emax $Emax -n $nenergies # make binning file
    python src/make_selection_txt.py -r $root --weak_in $weak_in --weak_out $weak_out # make selection file
else
    echo "Skipping data download"
fi

# 1) gtselect
# 2) gtmktime
# 3) gtbin
# 4) gtltcube
# 5) gtexpcube2
# 6) gtpsf

if [ $run_analysis = 1 ]; then

    echo "Running analysis"

    echo " "
    echo "-----gtselect-----"
    echo " "
    src/gtselect.sh $root $dirname $Emin $Emax $evclass $evtype

    echo " "
    echo "-----gtmktime-----"
    echo " "
    src/gtmktime.sh $root $dirname

    echo " "
    echo "-----gtbin-----"
    echo " "
    src/gtbin.sh $root $dirname $healpixorder

    echo " "
    echo "-----gtltcube-----"
    echo " "
    src/gtltcube.sh $root $dirname

    echo " "
    echo "-----gtexpcube2-----"
    echo " "
    src/gtexpcube2.sh $root $dirname $evtype $healpixorder

    echo " "
    echo "-----gtpsf-----"
    echo " "
    src/gtpsf.sh $root $dirname $Emin $Emax $evtype
else
    echo "Skipping analysis"
fi

# hdf5 conversion
if [ $hdf5 = 1 ]; then
    echo "Converting fits files to hdf5"
    mkdir -p $root/output/$dirname/hdf5
    fits2hdf -f $root/output/$dirname $root/output/$dirname/hdf5 -c gzip

else
    echo "Skipping hdf5 conversion"
fi

# cleanup
if [ $cleanup = 1 ]; then
    echo "Performing cleanup"
    rm -r *.par
    rm -r $root/utils/*
else
    echo "Skipping cleanup"
fi

echo "Done!"