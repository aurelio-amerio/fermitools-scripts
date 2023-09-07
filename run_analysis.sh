#!/bin/bash
root="/home/aure/Github/fermitools-scripts/test_run"
dirname="test_run"
weak_in=9
weak_out=15 #795
Emin=1000
Emax=10000
nenergies=10
healpixorder=3 #11
cleanup=true

python download_fermi_data.py -r $root --weak_in $weak_in --weak_out $weak_out # download data
python make_bin_txt.py -r $root --Emin $Emin --Emax $Emax -n $nenergies # make binning file
python make_selection_txt.py -r $root --weak_in $weak_in --weak_out $weak_out # make selection file

# 1) gtselect
# 2) gtmktime
# 3) gtbin
# 4) gtltcube
# 5) gtexpcube2
# 6) gtpsf

./gtselect.sh $root $dirname $Emin $Emax
./gtmktime.sh $root $dirname
./gtbin.sh $root $dirname $healpixorder
./gtltcube.sh $root $dirname
./gtexpcube2.sh $root $dirname $healpixorder
./gtpsf.sh $root $dirname $Emin $Emax

# cleanup
if $cleanup then
	echo "Performing cleanup"
    rm -r *.par
fi

echo "Done!"