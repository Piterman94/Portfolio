from geopy.geocoders import Nominatim
from geopy import exc
import geopy
import random
import csv

# Create a geocoder instance
geolocator = Nominatim(user_agent="teste1")

# Define the city and country
city = "Belo Horizonte"
country = "Brazil"

# Generate random addresses for employees
employee_addresses = []
for _ in range(1000):
    location = geolocator.geocode(city + ", " + country)
    latitude = location.latitude + random.uniform(-0.05, 0.05)  # Add slight variation
    longitude = location.longitude + random.uniform(-0.05, 0.05)  # Add slight variation
    ##address = geolocator.reverse((latitude, longitude)).address
    address = (str(latitude) + ", " + str(longitude))
    employee_addresses.append(address)

# Generate random addresses for stores
store_addresses = []
for _ in range(50):
    location = geolocator.geocode(city + ", " + country)
    latitude = location.latitude + random.uniform(-0.05, 0.05)  # Add slight variation
    longitude = location.longitude + random.uniform(-0.05, 0.05)  # Add slight variation
    ##address = geolocator.reverse((latitude, longitude)).address
    address = (str(latitude) + ", " + str(longitude))
    store_addresses.append(address)

# Save employee addresses to a CSV file
with open('employee_addresses.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Address'])
    for address in employee_addresses:
        writer.writerow([address])

# Save store addresses to a CSV file
with open('store_addresses.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Address'])
    for address in store_addresses:
        writer.writerow([address])