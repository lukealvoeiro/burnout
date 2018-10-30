# Script that appends active fires to CSV file

from ftplib import FTP
import csv
import random
import json


class Active_Fire_Fetch():
    
    # Class Attributes
    nasa_server = 'nrt3.modaps.eosdis.nasa.gov'
    username = 'lukealvoeiro'
    pword = 'Burnout1'
    modis_dir = '/FIRMS/c6/USA_contiguous_and_Hawaii/'
    modis_7d = 'MODIS_C6_USA_contiguous_and_Hawaii_7d.csv'
    modis_24hr = 'MODIS_C6_USA_contiguous_and_Hawaii_24hr.csv'
    # modis_file = 'MODIS_C6_USA_contiguous_and_Hawaii_MCD14DL_NRT_2018238.txt'
    modis_file = 'MODIS_C6_USA_contiguous_and_Hawaii_MCD14DL_NRT_2018'
    modis_file_end = 242
    local_download = 'new_data.csv'
    fire_locations = 'fire_locations.json'
    non_fire_locations = 'non_fire_locations.json'
    ca_north_lat = 42
    ca_south_lat = 32.7
    ca_east_long = -116.3
    ca_west_long = -123.7

    def access_data_file(self):
        '''
        Logs into the NASA server via FTP protocol
        to prepare to access the data; returns the
        FTP interface.
        '''
        ftp = FTP(self.nasa_server)
        ftp.login(self.username, self.pword)
        ftp.cwd(self.modis_dir)
        return ftp


    def download_file(self, ftp, filename):
        '''
        Dowloads a file from a provided FTP interface
        and copies it over to a local version of the file.
        '''
        localfile = open(self.local_download, 'wb')
        print("filename: "+filename)
        ftp.retrbinary('RETR ' + filename, localfile.write, 1024)

        ftp.quit()
        localfile.close()


    def extract_active_fires(self):
        '''
        Parses through the downloaded data in the CSV file to find
        all instances of active fires with a 100% confidence. It also produces a list of
        coordinates that are verified to not have any active fires in them. Returns a 
        tuple containing the active fire object along with the non-fire object.
        '''
        active_fires = {"Date": [], "Time": [], "Latitude": [], "Longitude": []}
        # active_fires = []
        with open(self.local_download, 'r') as csvfile:
            table = csv.DictReader(csvfile)
            non_fire_coords = self.generate_random_coordinates()
            date = ''

            for row in table:
                if row['confidence'] == '100':
                    active_fires["Date"].append(row['acq_date'])
                    active_fires["Time"].append(row['acq_time'])
                    active_fires["Latitude"].append(row['latitude'])
                    active_fires["Longitude"].append(row['longitude'])
                    date = row['acq_date']
                    # active_fires.append({'acq_date': row['acq_date'], 'acq_time': row['acq_time'], 'latitude': row['latitude'], 'longitude': row['longitude']})
                    # print(row['latitude'], row['longitude'])
                non_fire_coords = self.find_non_fires(row, non_fire_coords)
                # for coord in non_fire_coords:
                #     if abs(float(row['latitude']) - coord[0]) <= 0.1 & abs(float(row['longitude']) - coord[1]) <= 0.1:
                #         non_fire_coords.remove(coord)
        csvfile.close()
        return {'active_fires': active_fires, 'non_fire_coords': non_fire_coords, 'date': date}
        # return (active_fires, non_fire_coords, date)


    def add_active_fires(self, active_fire_list):
        '''
        Converts a provided active fire object into a JSON object, and adds
        this to the active fire JSON file.
        '''
        oldJSON = {}
        with open(self.fire_locations, 'r') as jsonFile:
            oldJSON = json.load(jsonFile)
            if (oldJSON == None) | (oldJSON == {}):
                oldJSON = {"Date": [], "Time": [], "Latitude": [], "Longitude": []}
            
            oldJSON["Date"] += active_fire_list["Date"]
            oldJSON["Time"] += active_fire_list["Time"]
            oldJSON["Latitude"] += active_fire_list["Latitude"]
            oldJSON["Longitude"] += active_fire_list["Longitude"]
        jsonFile.close()

        with open(self.fire_locations, 'w') as jsonFile:
            json.dump(oldJSON, jsonFile)
        jsonFile.close()

        print('Fires successfully added to file')

        # with open(self.fire_locations, 'a') as csvfile:
        #     writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #     for fire in active_fire_list:
        #         writer.writerow([fire['acq_date'], fire['acq_time'], fire['latitude'], fire['longitude']])
        # csvfile.close()
        # print('Fires successfully added to file')
    

    def generate_random_coordinates(self):
        '''
        Generates a list of 100 coordinates within the general bounds of California,
        and returns this list.
        '''
        non_fire_coords = []
        for i in range(100):
            rand_lat = random.uniform(self.ca_south_lat, self.ca_north_lat)
            rand_long = random.uniform(self.ca_west_long, self.ca_east_long)
            non_fire_coords.append({'Latitude': rand_lat, 'Longitude': rand_long})
        return non_fire_coords
    

    def find_non_fires(self, row, non_fire_coords):
        '''
        Checks if any of the randomly generated coordinates are within the immediate area
        of any active fires. If so, it removes them from the list and returns the resulting
        non-fire list.
        '''
        for coord in non_fire_coords:
            if (abs(float(row['latitude']) - float(coord['Latitude'])) <= 0.1) & (abs(float(row['longitude']) - float(coord['Longitude'])) <= 0.1):
                non_fire_coords.remove(coord)
            else:
                coord['Latitude'] = str(coord['Latitude'])
                coord['Longitude'] = str(coord['Longitude'])
        return non_fire_coords
    

    def add_non_fires(self, non_fire_coords, date):
        '''
        Adds confirmed non-fire coordinates to a JSON file.
        '''
        oldJSON = {}
        with open(self.non_fire_locations, 'r') as jsonFile:
            oldJSON = json.load(jsonFile)
            if (oldJSON == None) | (oldJSON == {}):
                oldJSON = {"Date": [], "Latitude": [], "Longitude": []}
            
            for coord in non_fire_coords:
                oldJSON["Date"].append(date)
                oldJSON["Latitude"].append(coord["Latitude"])
                oldJSON["Longitude"].append(coord["Longitude"])
        jsonFile.close()

        with open(self.non_fire_locations, 'w') as jsonFile:
            json.dump(oldJSON, jsonFile)
        jsonFile.close()

        print('Non-fires successfully added to file')

        # with open(self.non_fire_locations, 'a') as csvfile:
        #     writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #     for coord in non_fire_coords:
        #         writer.writerow([coord[0], coord[1]])
        # csvfile.close()
        # print('Non fires successfully added to file')

    def main_function(self, day_num):
        ftp = self.access_data_file()
        # for i in range(60):
        filename = self.modis_file + str(day_num) + '.txt'
        # filename = self.modis_file + str(self.modis_file_end) + '.txt'
        self.modis_file_end += 1
        self.download_file(ftp, filename)
        fire_lists = self.extract_active_fires()
        self.add_active_fires(fire_lists['active_fires'])
        self.add_non_fires(fire_lists['non_fire_coords'], fire_lists['date'])

if __name__ == "__main__":
    new_fetch = Active_Fire_Fetch()
    new_fetch.main_function(243)


#domain name or server ip:
# nasa_server = 'nrt3.modaps.eosdis.nasa.gov'
# username = 'lukealvoeiro'
# pword = 'Burnout1'
# modis_dir = '/FIRMS/c6/USA_contiguous_and_Hawaii/'
# modis_7d = 'MODIS_C6_USA_contiguous_and_Hawaii_7d.csv'
# modis_24hr = 'MODIS_C6_USA_contiguous_and_Hawaii_24hr.csv'
# modis_file = 'MODIS_C6_USA_contiguous_and_Hawaii_MCD14DL_NRT_2018281.txt'
# local_download = 'new_data.csv'
# fire_locations = 'fire_locations.csv'

# def access_data_file():
#     ftp = FTP(nasa_server)
#     ftp.login(username, pword)
#     ftp.cwd(modis_dir)
#     return ftp


# def download_file(ftp, filename):

#     localfile = open(local_download, 'wb')
#     ftp.retrbinary('RETR ' + filename, localfile.write, 1024)

#     ftp.quit()
#     localfile.close()


# def extract_active_fires():
#     active_fires = []
#     with open(local_download, 'r') as csvfile:
#         table = csv.DictReader(csvfile)
#         for row in table:
#             if row['confidence'] == '100':
#                 active_fires.append({'acq_date': row['acq_date'], 'acq_time': row['acq_time'], 'latitude': row['latitude'], 'longitude': row['longitude']})
#                 # print(row['latitude'], row['longitude'])
#     csvfile.close()
#     return active_fires


# def add_active_fires(active_fire_list):
#     with open(fire_locations, 'a') as csvfile:
#         writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         for fire in active_fire_list:
#             writer.writerow([fire['acq_date'], fire['acq_time'], fire['latitude'], fire['longitude']])
#     csvfile.close()
#     print('Fires successfully added to file')


# def main_function():
#     ftp = access_data_file()
#     download_file(ftp, 'MODIS_C6_USA_contiguous_and_Hawaii_MCD14DL_NRT_2018281.txt')
#     active_fires = extract_active_fires()
#     add_active_fires(active_fires)

# main_function()
