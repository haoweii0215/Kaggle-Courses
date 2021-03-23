# Exercise 5 : Proximity Analysis
import math
import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiPolygon
import folium
from folium import Choropleth, Marker
from folium.plugins import HeatMap, MarkerCluster
from learntools.core import binder
binder.bind(globals())
from learntools.geospatial.ex5 import *

def embed_map(m, file_name):
    from IPython.display import IFrame
    m.save(file_name)
    return IFrame(file_name, width='100%', height='500px')

## 1) Visualize the collision data.
## Run the code cell below to load a GeoDataFrame collisions tracking major motor vehicle collisions in 2013-2018.
collisions = gpd.read_file("../input/geospatial-learn-course-data/NYPD_Motor_Vehicle_Collisions/NYPD_Motor_Vehicle_Collisions/NYPD_Motor_Vehicle_Collisions.shp")

## Answer:
m_1 = folium.Map(location=[40.7, -74], zoom_start=11)
HeatMap(data=collisions[['LATITUDE', 'LONGITUDE']], radius=9).add_to(m_1)
embed_map(m_1, "q_1.html")

## 2) Understand hospital coverage.
## Run the next code cell to load the hospital data.
hospitals = gpd.read_file("../input/geospatial-learn-course-data/nyu_2451_34494/nyu_2451_34494/nyu_2451_34494.shp")

## Answer:
m_2 = folium.Map(location=[40.7, -74], zoom_start=11)
for idx, row in hospitals.iterrows():
    Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m_2)
embed_map(m_2, "q_2.html")

## 3) When was the closest hospital more than 10 kilometers away?
## Create a DataFrame outside_range containing all rows from collisions with crashes that occurred more than 10 kilometers from the closest hospital.
## Note that both hospitals and collisions have EPSG 2263 as the coordinate reference system, and EPSG 2263 has units of meters.

## Answer:
coverage = gpd.GeoDataFrame(geometry=hospitals.geometry).buffer(10000)
my_union = coverage.geometry.unary_union
outside_range = collisions.loc[~collisions["geometry"].apply(lambda x: my_union.contains(x))]

## 4) Make a recommender.
## When collisions occur in distant locations, it becomes even more vital that injured persons are transported to the nearest available hospital.
## With this in mind, you decide to create a recommender that:
##     takes the location of the crash (in EPSG 2263) as input,
##     finds the closest hospital (where distance calculations are done in EPSG 2263), and
##     returns the name of the closest hospital.

## Answer:
def best_hospital(collision_location):
    idx_min = hospitals.geometry.distance(collision_location).idxmin()
    my_hospital = hospitals.iloc[idx_min]
    name = my_hospital["name"]
    return name
print(best_hospital(outside_range.geometry.iloc[0]))

## 5) Which hospital is under the highest demand?
## Considering only collisions in the outside_range DataFrame, which hospital is most recommended?
## Your answer should be a Python string that exactly matches the name of the hospital returned by the function you created in 4).

## Answer:
highest_demand = outside_range.geometry.apply(best_hospital).value_counts().idxmax()

## 6) Where should the city construct new hospitals?
## Run the next code cell (without changes) to visualize hospital locations, in addition to collisions that occurred more than 10 kilometers away from the closest hospital.
m_6 = folium.Map(location=[40.7, -74], zoom_start=11)
coverage = gpd.GeoDataFrame(geometry=hospitals.geometry).buffer(10000)
folium.GeoJson(coverage.geometry.to_crs(epsg=4326)).add_to(m_6)
HeatMap(data=outside_range[['LATITUDE', 'LONGITUDE']], radius=9).add_to(m_6)
folium.LatLngPopup().add_to(m_6)
embed_map(m_6, 'm_6.html')

## Answer:
lat_1 = 40.6714
long_1 = -73.8492
lat_2 = 40.6702
long_2 = -73.7612
try:
    new_df = pd.DataFrame(
        {'Latitude': [lat_1, lat_2],
         'Longitude': [long_1, long_2]})
    new_gdf = gpd.GeoDataFrame(new_df, geometry=gpd.points_from_xy(new_df.Longitude, new_df.Latitude))
    new_gdf.crs = {'init' :'epsg:4326'}
    new_gdf = new_gdf.to_crs(epsg=2263)
    # get new percentage
    new_coverage = gpd.GeoDataFrame(geometry=new_gdf.geometry).buffer(10000)
    new_my_union = new_coverage.geometry.unary_union
    new_outside_range = outside_range.loc[~outside_range["geometry"].apply(lambda x: new_my_union.contains(x))]
    new_percentage = round(100*len(new_outside_range)/len(collisions), 2)
    print("(NEW) Percentage of collisions more than 10 km away from the closest hospital: {}%".format(new_percentage))
    # Did you help the city to meet its goal?
    q_6.check()
    # make the map
    m = folium.Map(location=[40.7, -74], zoom_start=11)
    folium.GeoJson(coverage.geometry.to_crs(epsg=4326)).add_to(m)
    folium.GeoJson(new_coverage.geometry.to_crs(epsg=4326)).add_to(m)
    for idx, row in new_gdf.iterrows():
        Marker([row['Latitude'], row['Longitude']]).add_to(m)
    HeatMap(data=new_outside_range[['LATITUDE', 'LONGITUDE']], radius=9).add_to(m)
    folium.LatLngPopup().add_to(m)
    display(embed_map(m, 'q_6.html'))
except:
    q_6.hint()