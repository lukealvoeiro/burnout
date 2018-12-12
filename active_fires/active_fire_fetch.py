# Script that appends active fires to CSV file

from ftplib import FTP
import csv
import random
import json
import datetime


class Active_Fire_Fetch():
    
    # Class Attributes
    nasa_server = 'nrt3.modaps.eosdis.nasa.gov'
    username = 'lukealvoeiro'
    pword = 'Burnout1'
    modis_dir = '/FIRMS/c6/USA_contiguous_and_Hawaii/'
    modis_7d = 'MODIS_C6_USA_contiguous_and_Hawaii_7d.csv'
    modis_24hr = 'MODIS_C6_USA_contiguous_and_Hawaii_24hr.csv'
    modis_file = 'MODIS_C6_USA_contiguous_and_Hawaii_MCD14DL_NRT_2018'
    modis_file_end = 256
    local_download = 'new_data.csv'
    fire_locations = 'fire_locations.json'
    non_fire_locations = 'non_fire_locations.json'
    archive_data = ['../fire_archive_data/fire_archive_M6_33217.csv', 
                    '../fire_archive_data/fire_nrt_M6_33217.csv']
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

    
    def active_fire_check(self, confidence, latitude, longitude):
        '''
        Returns if the active fire is roughly within the state of California.
        '''
        if confidence == '100':
            latitude_bound = (float(latitude) <= self.ca_north_lat) & (float(latitude) >= self.ca_south_lat)
            longitude_bound = (float(longitude) <= self.ca_east_long) & (float(longitude) >= self.ca_west_long)
            return latitude_bound & longitude_bound
        else:
            return False


    def extract_active_fires(self):
        '''
        Parses through the downloaded data in the CSV file to find
        all instances of active fires with a 100% confidence. It also produces a list of
        coordinates that are verified to not have any active fires in them. Returns a 
        tuple containing the active fire object along with the non-fire object.
        '''
        active_fires = {"Date": [], "Time": [], "Latitude": [], "Longitude": []}
        with open(self.local_download, 'r') as csvfile:
            table = csv.DictReader(csvfile)
            non_fire_coords = self.generate_random_coordinates()
            date = ''

            for row in table:
                if self.active_fire_check(row['confidence'], row['latitude'], row['longitude']):
                    active_fires["Date"].append(row['acq_date'])
                    active_fires["Time"].append(row['acq_time'])
                    active_fires["Latitude"].append(row['latitude'])
                    active_fires["Longitude"].append(row['longitude'])
                date = row['acq_date']
                non_fire_coords = self.cross_check_fires(row, non_fire_coords)
        csvfile.close()
        return {'active_fires': active_fires, 'non_fire_coords': non_fire_coords, 'date': date}
    

    def extract_archive_fires(self, csv_file):
        '''
        Extract archived fire data from CSV files.
        
        To Do: Make active_fires an empty list; add dict object as each elt in list;
        Once a comprehensive list is complete, sort it by date (convert to datetime);
        Return a sorted JSON object based on sorted dict.
        '''

        active_fires = []
        datetime_format = '%Y-%m-%d'
        with open(csv_file, 'r') as csvfile:
            table = csv.DictReader(csvfile)
            date = ''

            for row in table:
                if self.active_fire_check(row['confidence'], row['latitude'], row['longitude']):
                    date_time_obj = datetime.datetime.strptime(row['acq_date'], datetime_format)
                    date_time_since_epoch = int(date_time_obj.strftime("%s")) * 1000
                    active_fires.append({"Date": row['acq_date'], "Datetime": date_time_since_epoch, "Time": row['acq_time'], "Latitude": row['latitude'], "Longitude": row['longitude']})
                    print("Extracted Fire on " + row['acq_date'])
        csvfile.close()
        return active_fires


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


    def add_archive_fires(self, active_fire_list):
        '''
        Adds active fires from archive data to the destination JSON file
        '''
        with open(self.fire_locations, 'r') as jsonFile:
            oldJSON = json.load(jsonFile)
            for fire in active_fire_list:
                oldJSON["Date"].append(fire["Date"])
                oldJSON["Time"].append(fire["Time"])
                oldJSON["Latitude"].append(fire["Latitude"])
                oldJSON["Longitude"].append(fire["Longitude"])
        jsonFile.close()

        with open(self.fire_locations, 'w') as jsonFile:
            json.dump(oldJSON, jsonFile)
        jsonFile.close()

        print('Fires successfully added to file')
    

    def generate_random_coordinates(self):
        '''
        Generates a list of 100 coordinates within the general bounds of California,
        and returns this list.
        '''
        non_fire_coords = []
        for i in range(140):
            rand_lat = random.uniform(self.ca_south_lat, self.ca_north_lat)
            rand_long = random.uniform(self.ca_west_long, self.ca_east_long)
            non_fire_coords.append({'Latitude': rand_lat, 'Longitude': rand_long})
        return non_fire_coords

    
    def generate_non_fires(self):
        '''
        Returns a list of non-fire coordinate dictionaries for days a week apart.
        '''
        unconfirmed_non_fires = {} # key is date, val is other dict with coords
        start_date = datetime.datetime.strptime("2014-01-01", "%Y-%m-%d")
        while (start_date < datetime.datetime.today()):
            date_str = start_date.strftime('%Y-%m-%d')
            print("Generating non_fire on " + date_str)
            random_coords = self.generate_random_coordinates()
            unconfirmed_non_fires[date_str] = random_coords

            start_date += datetime.timedelta(days = 7)
        
        return unconfirmed_non_fires

    

    def cross_check_fires(self, active_fire_coords, non_fire_coords):
        '''
        Checks if any of the randomly generated coordinates are within the immediate area
        of any active fires. If so, it removes them from the list and returns the resulting
        non-fire list.

        Which active fire list should this take in??
        '''
        checked_fire_coords = []
        for fire in active_fire_coords:
            if fire["Date"] in non_fire_coords:
                for coord in non_fire_coords[fire["Date"]]:
                    if (abs(float(fire["Latitude"]) - float(coord["Latitude"])) <= 0.1) & (abs(float(fire["Longitude"]) - float(coord["Longitude"])) <= 0.1):
                        non_fire_coords[fire["Date"]].remove(coord)
        
        return non_fire_coords
    

    def add_non_fires(self, non_fire_coords):
        '''
        Adds confirmed non-fire coordinates to a JSON file.
        '''
        oldJSON = {}
        with open(self.non_fire_locations, 'r') as jsonFile:
            oldJSON = json.load(jsonFile)
                
            for date in non_fire_coords:
                for coord in non_fire_coords[date]:
                    oldJSON["Date"].append(date)
                    oldJSON["Latitude"].append(coord["Latitude"])
                    oldJSON["Longitude"].append(coord["Longitude"])

        jsonFile.close()

        with open(self.non_fire_locations, 'w') as jsonFile:
            json.dump(oldJSON, jsonFile)
        jsonFile.close()

        print('Non-fires successfully added to file')
    

    def convert_archive_data(self):
        '''
        Adds archived data object into a JSON object
        '''
        fire_lists = []
        for file in self.archive_data:
            fire_lists += self.extract_archive_fires(file)
        
        fire_lists.sort(key=lambda k: k["Datetime"])
        
        self.add_archive_fires(fire_lists)


    def main_function(self, day_num):
        ftp = self.access_data_file()
        # for i in range(60):
        filename = self.modis_file + str(day_num) + '.txt'
        self.modis_file_end += 1
        self.download_file(ftp, filename)
        fire_lists = self.extract_active_fires()
        self.add_active_fires(fire_lists['active_fires'])
        # self.add_non_fires(fire_lists['non_fire_coords'], fire_lists['date'])

if __name__ == "__main__":
    new_fetch = Active_Fire_Fetch()
    new_fetch.main_function(243)
