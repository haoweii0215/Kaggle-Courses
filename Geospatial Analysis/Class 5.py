# Proximity Analysis
import folium
from folium import Marker, GeoJson
from folium.plugins import HeatMap
import pandas as pd
import geopandas as gpd

### Read Data
releases = gpd.read_file("./toxic_release_pennsylvania.shp")
stations = gpd.read_file("./PhillyHealth_Air_Monitoring_Stations.shp")

### Select one release incident in particular
recent_release = releases.iloc[360]

### Measure distance from release to each station
distances = stations.geometry.distance(recent_release.geometry)
print('Mean distance to monitoring stations: {} feet'.format(distances.mean()))
print('Closest monitoring station ({} feet):'.format(distances.min()))
print(stations.iloc[distances.idxmin()][["ADDRESS", "LATITUDE", "LONGITUDE"]])

### Creating a buffer
two_mile_buffer = stations.geometry.buffer(2*5280)

### Create map with release incidents and monitoring stations
m = folium.Map(location=[39.9526,-75.1652], zoom_start=11)
HeatMap(data=releases[['LATITUDE', 'LONGITUDE']], radius=15).add_to(m)
for idx, row in stations.iterrows():
    Marker([row['LATITUDE'], row['LONGITUDE']]).add_to(m)
    
### Plot each polygon on the map
GeoJson(two_mile_buffer.to_crs(epsg=4326)).add_to(m)

### Turn group of polygons into single multipolygon
my_union = two_mile_buffer.geometry.unary_union
print('Type:', type(my_union))

### The closest station is less than two miles away
my_union.contains(releases.iloc[360].geometry)

### The closest station is more than two miles away
my_union.contains(releases.iloc[358].geometry)
