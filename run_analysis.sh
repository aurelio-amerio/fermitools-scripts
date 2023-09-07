#!/bin/bash
root="/lhome/ific/a/aamerio/data/fermi"
dirname="test_run"
weak_in=9
weak_out=795 #795
Emin=1000
Emax=10000
nenergies=10
healpixorder=11 #11

dowload_data=0
run_analysis=0
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
    src/gtselect.sh $root $dirname $Emin $Emax

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
    src/gtexpcube2.sh $root $dirname $healpixorder

    echo " "
    echo "-----gtpsf-----"
    echo " "
    src/gtpsf.sh $root $dirname $Emin $Emax
else
    echo "Skipping analysis"
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