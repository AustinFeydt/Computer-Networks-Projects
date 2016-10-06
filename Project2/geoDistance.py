#TO RUN: just type python geoDistance.py
import geoip2.database
from math import radians, cos, sin, asin, sqrt

# This creates a Reader object to read from the file
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

#reads off the IPs and puts them in a python list
targets = open("targets.txt")
ip_list = targets.read().splitlines()

#according to www.whataremycoordinates.com, my current coordinates are:
lat1 = 41.50720007
lon1 = -81.6096177
print "My current coordinates are:"
print "Latitude",lat1
print "Longitude",lon1
print 

#loops through list of IPs
for x in ip_list:

	#Locates IP by its city in the database
	response = reader.city(x)
	print "IP: ",x

	#Gets latitude and longitude
	lat2 = response.location.latitude
	lon2 = response.location.longitude
	print "Latitude: ",lat2
	print "Longitude: ",lon2

	#I used the Haversine formula to calculate the geographical distance:
    # convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    #(via http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points)
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a)) 
	r = 6371 # Radius of earth in kilometers. Use 3956 for miles
	distance = c * r

	print "Distance(km): ",distance, "\n"