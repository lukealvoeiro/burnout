#!/bin/bash

rm -rf tiles

gdalwarp -t_srs EPSG:4326 2014_188_fireprob_gray.tif output.tif

gdal_translate -srcwin 3000 0 3472 2048 output.tif cropped.tif

gdal2tiles.py -z 0-12 cropped.tif tiles
