# Runs the Active Fire Fetch script on all available data from the last 60 days

import active_fire_fetch as ff

if __name__ == "__main__":
    for i in range(61):
        new_fetch = ff.Active_Fire_Fetch()
        new_fetch.main_function(243 + i)
        print("Fetched day " + str(243 + i))
