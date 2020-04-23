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


