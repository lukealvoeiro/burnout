#!/bin/bash
echo Predicting Fire Locations
eval conda activate ml
eval python3 fire_predictor.py

echo Step 1/5: Reprojecting Image
eval gdalwarp -t_srs EPSG:4326 fireprob.tif reprojected.tif

echo Step 2/5: Cropping Result
eval gdal_translate -srcwin 3000 0 3472 2048 reprojected.tif cropped.tif

echo Step 3/5: Creating Heatmap
eval gdaldem color-relief cropped.tif style.txt -alpha recolored.tif

echo Step 4/5: Reseting tiles
eval rm -rf tiles
eval gdal2tiles.py -z 0-12 recolored.tif tiles

echo Step 5/5: Removing unecessary files
eval rm fireprob.tif
eval rm reprojected.tif 
eval rm cropped.tif

echo Done!