# Load the Pandas libraries with alias 'pd'
import pandas as pd
import redis
# convert lat lon to miles
from geopy.distance import geodesic
import threading


##############################################################################
#                                                                            #
# geolocation PUB/SUB around 35km according to the cities                    #
#                                                                            #
##############################################################################

def radius(lat1, lon1, lat2, lon2):
    """
    calcul miles with latitude and longitude
    """
    pt1 = (lat1, lon1)
    pt2 = (lat2, lon2)
    return geodesic(pt1, pt2).miles


def radius35km(lat1, long1):
    """
    find all cities in radius 35km.
    """
    # print(customer.keys('*&lat'))
    l = []
    # find keys with &lat at the end
    for item in customer.keys('*&lat'):
        # list cities < 35km
        
        nameCity = str(item).replace('&lat', '').replace('\'', '')[1:]
        long2 = str(customer.get(nameCity + "&long")).replace('\'', '')[1:]
        lat2 = str(customer.get(nameCity+"&lat")).replace('\'', '')[1:]
        # 21.748 miles = 35km
        if(radius(lat1, long1, float(lat2), float(long2)) < 21.748):
            print("city next to %s %s is %s" % (lat1, long1, nameCity))
            l.append(nameCity)        
    return l


class Listener(threading.Thread):
    def __init__(self, r, bob_lat, bob_lon):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub() 
        self.pubsub.subscribe(radius35km(bob_lat, bob_lon))

    def run(self):
        for item in self.pubsub.listen():
            print(item['data'])


if __name__ == "__main__":
    # init server redis
    customer = redis.Redis(host='localhost', port=6379, db=0)
    # open csv to dataframe
    cities = pd.read_csv("cities.csv")
    ads = pd.read_csv("ads.csv")

    # clean cash redis
    customer.flushdb()

    # init dictionary
    longitude = {}
    latitude = {}
    for i in cities.index:
        # dictionary
        latitude[cities['Ville'][i]+"&lat"] = cities['Latitude'][i]
        longitude[cities['Ville'][i]+"&long"] = cities['Longitude'][i]

    # mset in redis latitude and longitude
    customer.mset(latitude)
    customer.mset(longitude)

    # start threading
    # bob subscribe to ads in Amiens
    bob_lat = 49.8986514
    bob_lon = 2.2145979
    bob = Listener(customer, bob_lat, bob_lon)
    bob.start()
    
    # publish new music in the channel epic_music
    customer.publish('Amiens', 'mcdo intership')
    customer.publish('Corbie', 'gardener' )
    