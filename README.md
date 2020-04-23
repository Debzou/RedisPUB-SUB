# RedisPUB-SUB
The goal of this mini project is to create a geolocalized announcement system. 

## PART 1

In the first part of the tp we didn't use the PUB/SUB of redis.
we make queries on redis in order to find the ads on a perimeter.
This way we will be able to attribute the ads to the person in the perimeter (35km).

cf main.py

## PART 2
Later we became interested in a real time announcement system with the help of redis (PUB/SUB).
A person (with a latitude and longitude) subscribes to the announcements of cities around 35km. 
This person will receive a message when there is a job offer in his perimeter which has just appeared.

cf mainSUBPUB.py

### how it works ?

start redis server
```{bash}
redis-server
```
start script python ( before install library python )
```{}
python3 mainSUBPUB.py
````
Go in redis customer

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
```{bas}
city next to 49.8986514 2.2145979 is Longueau
city next to 49.8986514 2.2145979 is Corbie
city next to 49.8986514 2.2145979 is Albert
city next to 49.8986514 2.2145979 is Doullens
city next to 49.8986514 2.2145979 is Amiens
```
Bob is subcribed to Longuau , Corbie , Albert ....

go in redis-cli
```{bash}
PUBLISH Corbie gardened
```
on python3 console we can see appear "gardened"
Attention it works only for cities within a 35 km zone, after BOB will no longer be subscribed and will receive by announcements.

