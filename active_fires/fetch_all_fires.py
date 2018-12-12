# Runs the Active Fire Fetch script on all available data from the last 60 days

import active_fire_fetch as ff
import json
import datetime

class Fetch_all_fires():

    # Class Attributes
    fire_locations = 'fire_locations.json'

    def update_fire_locations(self):
        oldJSON = {}
        with open(self.fire_locations, 'r') as jsonFile:
            oldJSON = json.load(jsonFile)
            last_date = oldJSON["Date"][-1]
            print('last_date: '+last_date)


        return 'test'
    

    def get_day_num_from_date(self, date):
        month = date[5:7]
        day = date[8:10]
        current_date = datetime.date
        print(str(current_date.day))
        return current_date


if __name__ == "__main__":
    new_fetch = ff.Active_Fire_Fetch()
    new_fetch.convert_archive_data()

