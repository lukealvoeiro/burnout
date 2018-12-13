"""
Created by Luke Alvoeiro and Gray Kline for Burnout - CS701 Project
MIT License
"""


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
import getopt

FOLDER_LIST = ['Surf_Ref_Daily_500m_v6/b1_Red', 'Surf_Ref_Daily_500m_v6/b2_NIR', 'Surf_Ref_Daily_500m_v6/b4_Green', 'Surf_Ref_Daily_500m_v6/b3_Blue', 'Surf_Ref_Daily_500m_v6/b5_SWIR', 'Surf_Ref_Daily_500m_v6/b6_SWIR', 'Surf_Ref_Daily_500m_v6/b7_SWIR']

def processDataJSON(json_file, out_filename, tiles, downloadImages, writeStackedImages):
    owd = os.getcwd()
    with open(json_file) as src:  
        data = json.load(src)
        lat = data['Latitude']
        lon = data['Longitude']
        dates = data['Date']
        fireBoolean = data['FireBoolean']

    start_x, end_x, start_y, end_y = tiles
    # Convert dates to datetime objects (to allow comparison)
    tmp_dates = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in dates]
    dates_before = [(date - datetime.timedelta(days=10)) for date in tmp_dates]

    contiguousDates = groupContiguousDates(dates_before)
    
    # Get YYYYDDD (Julian Date) for each entry in dates
    mod_dates = [date.strftime("%Y_%j") for date in dates_before]
    
    modis_settings_filename = "settings.json"
    with open(modis_settings_filename, "r") as modis_settings:
        data = json.load(modis_settings)

    data['start_x'] = start_x
    data['end_x'] = end_x
    data['start_y'] = start_y
    data['end_y'] = end_y
    data['out_folder'] = owd
    data['out_folder_mod'] = owd
    data['delete_hdf'] = "No"
    if(downloadImages):
        for start, end in contiguousDates:
            data['start_date'] = start
            data['end_date'] = end
            with open(modis_settings_filename, "w") as jsonFile:
                json.dump(data, jsonFile)
            # Call R Script:
            subprocess.call("Rscript MODIS_download.r")
        
    # Process the Images downloaded previously
    indices = getIndicesOfCoordinate('sample.tif', lat, lon)
    if(writeStackedImages): writeStackedImg(mod_dates, FOLDER_LIST, owd)
    # Write to CSV file:
    processImagesIntoDataset(out_filename, lat, mod_dates, indices, fireBoolean)

    
def groupContiguousDates(converted_datetimes):
    prev = converted_datetimes[0]
    start = converted_datetimes[0]
    res = []
    for index in range(len(converted_datetimes)):
        diff = (converted_datetimes[index] - prev).days
        if(diff > 1):
            res.append((start.strftime("%Y-%m-%d"), prev.strftime("%Y-%m-%d")))
            start = converted_datetimes[index]
            prev = converted_datetimes[index]
        else:
            prev = converted_datetimes[index]
        if(index == len(converted_datetimes) - 1):
            res.append((start.strftime("%Y-%m-%d"), prev.strftime("%Y-%m-%d")))
    return res

def processImagesIntoDataset(output_file, lat, dates, indices, fireTF):
    with open(output_file,'w') as output:
        for i in range(len(lat)):
            curr_date, curr_index, curr_fireTF = dates[i], indices[i], fireTF[i]
            # Search for specific file that corrresponds to this lat/lon and date
            file = glob.glob('*' + curr_date + '_stacked.tif')

            if file != []:
                # We have found said file!
                file = file[0]
                # Read in stacked image as a (Width x Height x #Bands) image
                stacked_file = produceStackedArray(file)
                # Get the value of the pixel
                val = strelOperation(stacked_file, curr_index[0], curr_index[1])
                #print(type(val[0]))
                # Append that value to our CSV file
                res = []
                for i in val:
                    res.append(str(i))
                    res.append(" ")
                res.append(str(curr_fireTF))
                line = "".join(res)
                print("Appending...", line)
                output.write(line)
                output.write('\n')

def writeStackedImg(dates, folder_list, owd, outName = None):
    dates = list(set(dates))
    for date in dates:
        print(date)
        curr_files = []
        for folder in folder_list:
            # Change to correct folder
            os.chdir(folder)
            # Start to describe current file
            curr_file = [folder + "/"]

            # Get filename we are interested in
            file = glob.glob('*' + date + '.tif')
            if file != []:
                curr_file.append(file[0])
                # Append this filename to our array of files
                curr_files.append("".join(curr_file))

            # Return to orginal working directory
            os.chdir(owd)
        if(curr_files != []):
            output_name = date + '_stacked.tif'
            if outName != None: output_name = outName
            # Write stacked image
            combineChannels(curr_files, output_name)

def strelOperation(img, indexRow, indexColumn):
    """
    Given an img and the row and column indices, perform an operation on this pixel
    (and potentially nearby ones). Then return the corresponding value(s).

    NOTE: as of right now, this is just returning the pixel values themselves
    """
    return img[indexRow][indexColumn]

def combineChannels(file_list, output_name):
    """
    Given a list of n files, stacks them on top of each other producing a geotiff with
    the same metadata, but with all bands available.
    """
    # Read metadata of first file
    with rasterio.open(file_list[0]) as src0:
        meta = src0.meta

    # Update meta to reflect the number of layers
    meta.update(count = len(file_list))

    # Read each layer and write it to stack
    with rasterio.open(output_name, 'w', **meta) as dst:
        for id, layer in enumerate(file_list, start=1):
            with rasterio.open(layer) as src1:
                dst.write_band(id, src1.read(1))

def getCoordinatesFromIndices(filename, x_index, y_index):
    """
    Given a file and indices x and y, get their position in real 
    latitude and longitude coordinates
    """
    if(len(x_index) != len(y_index) or len(y_index) == 0 or len(x_index) == 0):
        return []

    # Read raster
    with rasterio.open(filename, 'r') as src:
        if(src.crs.is_valid):
            # Determine Affine object and CRS projection
            trans = src.transform
            inProj = Proj(src.crs)
            outProj = Proj(init='epsg:4326')

            res = []
            for i in range(len(x_index)):
                curr_x, curr_y = x_index[i], y_index[i]
                print(curr_x)
                # Determines East/Northing 
                x, y = rasterio.transform.xy(trans, curr_x, curr_y)
                # Convert these to latitude / longitude
                tmp = transform(inProj,outProj,x,y)
                res.append(tmp)
            
            return res
        
def getIndicesOfCoordinate(filename, y_coord, x_coord):
    """
    Given an image file and latitude and longitude coordinates x and y, 
    get their corresponding indices in the image
    """
    
    if(len(x_coord) != len(y_coord) or len(y_coord) == 0 or len(x_coord) == 0):
        return []
    
    # Read raster
    with rasterio.open(filename, 'r') as src:
        # Determine Affine object and CRS projection
        trans = src.transform
        inProj = Proj(init='epsg:4326')
        outProj = Proj(src.crs)

        res = []
        for i in range(len(x_coord)):
            curr_x, curr_y = x_coord[i], y_coord[i]
            # Determines East/Northing 
            x, y = transform(inProj, outProj, curr_x, curr_y)
            # Convert the point to indices in the image
            tmp = rasterio.transform.rowcol(trans, x, y)
            res.append(tmp)
        
        return res

def produceStackedArray(filename):
    """
    Given a image file, combines all the bands into a numPy array
    where each pixel corresponds to a list of n values, where n is the number
    channels in the image provided
    """
    with rasterio.open(filename, 'r') as src:
        count = src.count
        base = src.read(1)
        for band_num in range(2, count+1):
            base = np.dstack((base, src.read(band_num)))
        return base


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ds")
        opts = dict(opts)
        downloadImages = True
        stackImages = True
        if(len(args) == 3):
            in_file, tiles, outfile = args[0], args[1], args[2]
            if '-d' in opts.keys(): downloadImages = False
            if '-s' in opts.keys(): stackImages = False
            arr_tiles = tiles.split(",")
            start_x, end_x = int(arr_tiles[0][1:3]), int(arr_tiles[0][1:3])
            start_y, end_y = int(arr_tiles[0][4:6]), int(arr_tiles[0][4:6])
            for tile in arr_tiles:
                x = int(tile[1:3])
                y = int(tile[4:6])
                if(x < start_x): start_x = x
                elif(x > end_x): end_x = x
                if(y < start_y): start_y = y
                elif(x > end_y): end_y = y
            processDataJSON(in_file, outfile, (start_x, end_x, start_y, end_y), downloadImages, stackImages)
            print('Dataset build complete!')        
    except:
        print("Something went wrong!")