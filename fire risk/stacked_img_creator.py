import rasterio
import numpy as np 
from pyproj import Proj, transform
import subprocess
import calendar
import os
import glob
import json
import datetime
import sys
from build_dataset import writeStackedImg, combineChannels

FOLDER_LIST = ['Surf_Ref_Daily_500m_v6/b1_Red', 'Surf_Ref_Daily_500m_v6/b2_NIR', 'Surf_Ref_Daily_500m_v6/b4_Green', 'Surf_Ref_Daily_500m_v6/b3_Blue', 'Surf_Ref_Daily_500m_v6/b5_SWIR', 'Surf_Ref_Daily_500m_v6/b6_SWIR', 'Surf_Ref_Daily_500m_v6/b7_SWIR']

def main():
    createStackedImg()

def createStackedImg():
    curr_date = datetime.datetime.today() - datetime.timedelta(days=2)
    owd = os.getcwd()

    modis_settings_filename = "settings.json"
    with open(modis_settings_filename, "r") as modis_settings:
        data = json.load(modis_settings)
    data['out_folder'] = owd
    data['out_folder_mod'] = owd
    data['delete_hdf'] = "Yes"
    data['start_date'] = curr_date.strftime("%Y-%m-%d")
    data['end_date'] = curr_date.strftime("%Y-%m-%d")
    with open(modis_settings_filename, "w") as jsonFile:
        json.dump(data, jsonFile)
    
    # Call R Script:
    subprocess.call("Rscript MODIS_download.r")

    # Create stacked image
    writeStackedImg([curr_date.strftime("%Y_%j")],FOLDER_LIST, owd, outName="curr_stacked.tif")

    subprocess.call("rm -rf Surf_Ref_Daily_500m_v6")

if __name__ == "__main__":
    main()