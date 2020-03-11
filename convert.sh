#!/bin/sh
### /data0/data/REFERENCE_DATA/OCEAN_REP/ARMOR3D/data/2009

###  dataset-armor-3d-rep-weekly_20100310T1200Z_P20190301T0000Z.nc


dir_i=/data0/data/REFERENCE_DATA/OCEAN_REP/ARMOR3D/data
file=dataset-armor-3d-rep-weekly_
dir_o=/home/lgarcia/Documents/data_ARMOR



#for year in {1979..2018}; do
#    cdo sellonlatbox,-180,180,-90,90 $dir/$file       $dir/$file2
#    ncks -d latitude,10.,85. -d longitude,-90.,50. $dir/$file2 $dir/out.nc
#echo $month
#done

for year in in {2010..2018}; do
    mkdir $dir_o/tmp

    for f in *.nc; do
    ncks -O -h --mk_rec_dmn time $dir_i/$year/$f $dir_o/tmp/$f-2.nc
    done 

    ncrcat -h $dir_o/tmp/$f-2.nc $dir_o/tmp/tmp_year.nc

    cdo sellonlatbox,-180,180,-90,90 $dir_o/tmp/tmp_year.nc $dir_o/ARGO_$year.nc
    ncks -d latitude,10.,85. -d longitude,-90.,50. $dir_o/ARGO_$year.nc $dir_o/ARGO_$year.nc

    rm -rI $dir_o/tmp
done
