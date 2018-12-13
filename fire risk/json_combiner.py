import json
import glob

def combineJSON():
    non_burning = 'non_fire_locations.json'
    burning = 'fire_locations.json'
    with open(burning, 'r') as fire_file:  
        data = json.load(fire_file)
        lat = data['Latitude']
        lon = data['Longitude']
        dates = data['Date']
        fire = [1]*len(data['Latitude'])

    with open(non_burning, 'r') as nofire_file:  
        data = json.load(nofire_file)
        lat += data['Latitude']
        lon += data['Longitude']
        dates += data['Date']
        fire += [0]*len(data['Latitude'])
    
    data.pop('Time', None)

    with open("combined.json", "w") as comb_file:
        data['Latitude'] = lat
        data['Longitude'] = lon
        data['Date'] = dates
        data['FireBoolean'] = fire
        json.dump(data, comb_file)

combineJSON()