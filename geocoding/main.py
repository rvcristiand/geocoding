from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="holi")
location = geolocator.geocode("AUTOPISTA MEDELLIN # 10 60,TENJO,CUNDINAMARCA")

print(location.address)
print(location.latitude, location.longitude)
