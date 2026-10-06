#!/bin/bash

nside=128

time python utils/flux_sensitivity.py \
    --nbin=16 \
    --emin=100\
    --emax=1000000\
    --ltcube=/lhome/ific/a/aamerio/data/fermi/output/source_nside_2048_front+back_0.1-1000GeV_zmax90/gtltcube.fits \
    --output=sensitivity_map_${nside}_dmhalos.fits \
    --galdiff=/lhome/ific/a/aamerio/data/fermi/output/sourceveto-w9-w870-7bins/gll_iem_v07.fits \
    --isodiff=/lhome/ific/a/aamerio/data/fermi/output/sourceveto-w9-w870-7bins/iso_P8R3_SOURCE_V3_v1.txt \
    --event_class=P8R3_SOURCE_V3 \
    --map_type=hpx \
    --hpx_nside=${nside}
