# Load the Pandas libraries with alias 'pd'
import pandas as pd
import redis
from geopy.distance import geodesic

##############################################################################
#                                                                            #
# geolocation of the advertisements around 35km according to the cities      #
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
    for item in customer.keys('*&lat'):
        nameCity = str(item).replace('&lat', '').replace('\'', '')[1:]
        long2 = str(customer.get(nameCity + "&long")).replace('\'', '')[1:]
        lat2 = str(customer.get(nameCity+"&lat")).replace('\'', '')[1:]
        # 21.748 miles = 35km
        if(radius(lat1, long1, float(lat2), float(long2)) < 21.748):
            print("city next to %s %s is %s"%(lat1,long1,nameCity))
        # customer.get('&long')

def findAds35km(city):
    # longitude/latitude city
    long1 = str(customer.get(city + "&long")).replace('\'', '')[1:]
    lat1 = str(customer.get(city+"&lat")).replace('\'', '')[1:]
    # find keys 
    for item in customer.keys('*&name'):
        #id ads
        idAds = str(item).replace('&name', '').replace('\'', '')[1:]
        #city ads
        nameCity = str(customer.get(idAds + "&citie")).replace('\'', '')[1:]
        long2 = str(customer.get(nameCity + "&long")).replace('\'', '')[1:]
        lat2 = str(customer.get(nameCity+"&lat")).replace('\'', '')[1:]
        if(radius(lat1, long1, float(lat2), float(long2)) < 21.748):
            offre = str(customer.get(idAds + "&name")).replace('\'', '')[1:]
            print('demand of %s in %s'%(offre,nameCity))
        


if __name__ == "__main__":
    # open csv to dataframe
    cities = pd.read_csv("cities.csv")
    ads = pd.read_csv("ads.csv")
    customer = redis.Redis(host='localhost', port=6379, db=0)
    # clean cash redis
    customer.flushdb()
    # init dictionary
    longitude = {}
    latitude = {}
    # idOffre : nomoffre
    adsNames = {}
    # idOffre : ville
    adsCities = {}
    for i in cities.index:
        # dictionary
        latitude[cities['Ville'][i]+"&lat"] = cities['Latitude'][i]
        longitude[cities['Ville'][i]+"&long"] = cities['Longitude'][i]

    for i in ads.index:
        # dictioanry
        adsNames[str(i)+"&name"] = ads['Offre'][i]
        adsCities[str(i)+"&citie"] = ads['Ville'][i]

    # mset in redis latitude and longitude
    customer.mset(latitude)
    customer.mset(longitude)
    # mset in redis offre
    customer.mset(adsNames)
    customer.mset(adsCities)

    # find cities in around 35km 
    radius35km(49.8986514, 2.2145979)
    # find an ad around amiens (35km)
    findAds35km("Amiens")

