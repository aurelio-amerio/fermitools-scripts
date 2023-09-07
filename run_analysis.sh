#!/bin/bash
root="/home/aure/Github/fermi-scripts/test"
dirname="test"
weak_in=9
weak_out=15 #795
Emin=1000
Emax=10000
nenergies=10
healpixorder=3 #11

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