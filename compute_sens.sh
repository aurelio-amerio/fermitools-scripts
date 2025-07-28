#!/bin/bash

nside=512

time python utils/flux_sensitivity.py \
    --nbin=7 \
    --ebins=500,1000,2000,5000,10000,50000,200000,1000000 \
    --ltcube=/lhome/ific/a/aamerio/data/fermi/output/sourceveto-w9-w870-7bins/gtltcube.fits \
    --output=sensitivity_map_${nside}.fits \
    --galdiff=/lhome/ific/a/aamerio/data/fermi/output/sourceveto-w9-w870-7bins/gll_iem_v07.fits \
    --isodiff=/lhome/ific/a/aamerio/data/fermi/output/sourceveto-w9-w870-7bins/iso_P8R3_SOURCE_V3_v1.txt \
    --event_class=P8R3_SOURCEVETO_V3 \
    --map_type=hpx \
    --hpx_nside=${nside}
