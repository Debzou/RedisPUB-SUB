# RedisPUB-SUB
The goal of this mini project is to create a geolocalized announcement system. 

## PART 1

In the first part of the lab we don't use the redis' PUB/SUB system yet.
we make queries to redis in order to find the ads on a given perimeter.
From this point we can retrieve the ads of a user near its city with a perimeter of 35Km

cf main.py

## PART 2
Later we became interested in a real time announcement system with the help of redis and the PUB/SUB system.
A user with a latitude and longitude subscribes to the announcements of cities around 35km. 
This person will receive a message when there is a job offer in this perimeter which has just appeared.

cf mainSUBPUB.py

### how it works ?

start redis server
```{bash}
redis-server
```
start script python ( before install the required librairies (pandas, redis & geopy))
```{}
python3 mainSUBPUB.py
````
Go in the redis-cli to simulate an announcer

```{bash}
redis-cli
```
now you can PUBLISH ads in redis-cli

### Example 

go in mainSUBPUB.py

define gps coordinates on client
```{python3}
    bob_lat = 49.8986514
    bob_lon = 2.2145979
    bob = Listener(customer, bob_lat, bob_lon)
    bob.start()
```
execute cf mainSUBPUB.py

resulat
```{bash}
city next to 49.8986514 2.2145979 is Longueau
city next to 49.8986514 2.2145979 is Corbie
city next to 49.8986514 2.2145979 is Albert
city next to 49.8986514 2.2145979 is Doullens
city next to 49.8986514 2.2145979 is Amiens
```
Bob is subcribed to Longuau , Corbie , Albert ect

go in redis-cli as an announcer
```{bash}
PUBLISH Corbie gardening
```
In the python console we can see that the user (bob) received the ad "gardening"

Be careful it only works for cities within a 35 km zone, after BOB will no longer be subscribed to the cities outside and won't receive any announcements.

