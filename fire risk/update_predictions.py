import os, json, datetime, subprocess, glob
from build_dataset import combineChannels
from fire_predictor import predict
import skimage.io as skio

FOLDER_LIST = ['Surf_Ref_Daily_500m_v6/b1_Red', 'Surf_Ref_Daily_500m_v6/b2_NIR', 'Surf_Ref_Daily_500m_v6/b4_Green', 'Surf_Ref_Daily_500m_v6/b3_Blue', 'Surf_Ref_Daily_500m_v6/b5_SWIR', 'Surf_Ref_Daily_500m_v6/b6_SWIR', 'Surf_Ref_Daily_500m_v6/b7_SWIR']

def main():
    """
    1. set up json file settings for download
    2. call download
    3. stack images
    4. feed stacked image to predictor
    5. process predicted image
    6. delete everything but predicted imag
    """
    owd = os.getcwd()
    # setupDownload(owd)
    # subprocess.call("Rscript MODIS_download.r")
    print(owd)
    files_to_combine = []
    for folder in FOLDER_LIST[:3]:
        os.chdir(folder)
        filename = glob.glob('*.tif')
        files_to_combine.append(folder + "/" + filename[0])
        os.chdir(owd)
    
    combineChannels(files_to_combine, "curr_input.tif")
    predict("curr_input.tif", "curr_predictions.tif")

    #delete folders & curr_input.tif

def setupDownload(owd):
    modis_settings_filename = "settings.json"
    today = datetime.datetime.today().strftime("%Y-%m-%d")

    with open(modis_settings_filename, "r") as modis_settings:
        download_settings = json.load(modis_settings)
    download_settings['out_folder'] = owd
    download_settings['out_folder_mod'] = owd
    download_settings['delete_hdf'] = "Yes"
    download_settings['start_date'] = today
    download_settings['end_date'] = today
    with open(modis_settings_filename, "w") as jsonFile:
        json.dump(download_settings, jsonFile)


main()



