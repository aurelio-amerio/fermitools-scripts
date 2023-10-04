#!/bin/bash
root="/lhome/ific/a/aamerio/data/fermi"
dirname="sourceveto_nside2048_front_0.5_1000_GeV"
weak_in=9
weak_out=795 #795
Emin=500 # MeV # 0.5 GeV
Emax=1000000 # MeV # 1000 GeV
Earr="500 1000 2000 5000 10_000 50_000 200_000 1_000_000" # MeV
nenergies=10 # number of energies per bin, if Earr is specfied, else it's the total number of energies between Emin - Emax, in log scale
healpixorder=11 #11

# evclass
# 2048: "SOURCEVETO",
# 1024: "ULTRACLEANVETO",
# 512:  "ULTRACLEAN",
# 256:  "CLEAN",
# 128:  "SOURCE",
# 64:   "TRANSIENT010",
# 16:   "TRANSIENT020"
evclass=2048 # default 2048
evtype=1 #front

dowload_data=0

run_analysis=1
gtselect=1
gtmktime=1
gtbin=1
gtltcube=1
gtexpcube2=1
gtpsf=1

hdf5=1
cleanup=1

mkdir -p $root/output/$dirname

if [ $dowload_data = 1 ]; then
    echo "Downloading data"
    python src/download_fermi_data.py -r $root --weak_in $weak_in --weak_out $weak_out # download data
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

    python src/make_bin_txt.py -r $root --Emin $Emin --Emax $Emax -n $nenergies --ebins $Earr # make binning file
    python src/make_selection_txt.py -r $root --weak_in $weak_in --weak_out $weak_out # make selection file

    echo " "
    echo "-----gtselect-----"
    echo " "
    if [ $gtselect = 1 ]; then
        src/gtselect.sh $root $dirname $Emin $Emax $evclass $evtype
    else
        echo "Skipping gtselect"
    fi

    if [ $gtmktime = 1 ]; then
        echo " "
        echo "-----gtmktime-----"
        echo " "
        src/gtmktime.sh $root $dirname
    else
        echo "Skipping gtmktime"
    fi

    if [ $gtbin = 1 ]; then
        echo " "
        echo "-----gtbin-----"
        echo " "
        src/gtbin.sh $root $dirname $healpixorder
    else
        echo "Skipping gtbin"
    fi

    if [ $gtltcube = 1 ]; then
        echo " "
        echo "-----gtltcube-----"
        echo " "
        src/gtltcube.sh $root $dirname
    else
        echo "Skipping gtltcube"
    fi

    if [ $gtexpcube2 = 1 ]; then
        echo " "
        echo "-----gtexpcube2-----"
        echo " "
        src/gtexpcube2.sh $root $dirname $evtype $healpixorder
    else
        echo "Skipping gtexpcube2"
    fi

    if [ $gtpsf = 1 ]; then
        echo " "
        echo "-----gtpsf-----"
        echo " "
        src/gtpsf.sh $root $dirname $Emin $Emax $evtype
    else
        echo "Skipping gtpsf"
    fi
else
    echo "Skipping analysis"
fi

# hdf5 conversion
if [ $hdf5 = 1 ]; then
    echo "Converting fits files to hdf5"
    mkdir -p $root/output/$dirname/hdf5
    fits2hdf -c gzip $root/output/$dirname $root/output/$dirname/hdf5 

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