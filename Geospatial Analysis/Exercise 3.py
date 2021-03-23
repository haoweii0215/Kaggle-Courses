# Exercise 3 : Coordinate Reference Systems
import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth
from folium.plugins import HeatMap
from learntools.core import binder
binder.bind(globals())
from learntools.geospatial.ex3 import *

def embed_map(m, file_name):
    from IPython.display import IFrame
    m.save(file_name)
    return IFrame(file_name, width='100%', height='500px')

## 1) Do earthquakes coincide with plate boundaries?
## Run the code cell below to create a DataFrame plate_boundaries that shows global plate boundaries. The "coordinates" column is a list of (latitude, longitude) locations along the boundaries.
plate_boundaries = gpd.read_file("../input/geospatial-learn-course-data/Plate_Boundaries/Plate_Boundaries/Plate_Boundaries.shp")
plate_boundaries['coordinates'] = plate_boundaries.apply(lambda x: [(b,a) for (a,b) in list(x.geometry.coords)], axis='columns')
plate_boundaries.drop('geometry', axis=1, inplace=True)
earthquakes = pd.read_csv("../input/geospatial-learn-course-data/earthquakes1970-2014.csv", parse_dates=["DateTime"])

## Answer:
m_1 = folium.Map(location=[35,136], tiles='cartodbpositron', zoom_start=5)
for i in range(len(plate_boundaries)):
    folium.PolyLine(locations=plate_boundaries.coordinates.iloc[i], weight=2, color='black').add_to(m_1)
HeatMap(data=earthquakes[['Latitude', 'Longitude']], radius=15).add_to(m_1)
embed_map(m_1, 'q_1.html')

## 2) Is there a relationship between earthquake depth and proximity to a plate boundary in Japan?
## You recently read that the depth of earthquakes tells us important information about the structure of the earth. You're interested to see if there are any intereresting global patterns, and you'd also like to understand how depth varies in Japan.
m_2 = folium.Map(location=[35, 136], tiles='cartodbpositron', zoom_start=5)
for i in range(len(plate_boundaries)):
    folium.PolyLine(locations=plate_boundaries.coordinates.iloc[i], weight=2, color='black').add_to(m_2)

## Answer:
def color_producer(val):
    if val < 50:
        return 'forestgreen'
    elif val < 100:
        return 'darkorange'
    else:
        return 'darkred'
for i in range(0, len(earthquakes)):
    folium.Circle(
        location=[earthquakes.iloc[i]['Latitude'], earthquakes.iloc[i]['Longitude']],
        radius=2000,
        color=color_producer(earthquakes.iloc[i]['Depth'])).add_to(m_2)
embed_map(m_2, 'q_2.html')

## 3) Which prefectures have high population density?
## Run the next code cell (without changes) to create a GeoDataFrame prefectures that contains the geographical boundaries of Japanese prefectures.
prefectures = gpd.read_file("../input/geospatial-learn-course-data/japan-prefecture-boundaries/japan-prefecture-boundaries/japan-prefecture-boundaries.shp")
prefectures.set_index('prefecture', inplace=True)
population = pd.read_csv("../input/geospatial-learn-course-data/japan-prefecture-population.csv")
population.set_index('prefecture', inplace=True)
area_sqkm = pd.Series(prefectures.geometry.to_crs(epsg=32654).area / 10**6, name='area_sqkm')
stats = population.join(area_sqkm)
stats['density'] = stats["population"] / stats["area_sqkm"]

## Answer:
m_3 = folium.Map(location=[35,136], tiles='cartodbpositron', zoom_start=5)
Choropleth(geo_data=prefectures['geometry'].__geo_interface__,
           data=stats['density'],
           key_on="feature.id",
           fill_color='YlGnBu',
           legend_name='Population density (per square kilometer)'
          ).add_to(m_3)
embed_map(m_3, 'q_3.html')

## 4) Which high-density prefecture is prone to high-magnitude earthquakes?
## Create a map to suggest one prefecture that might benefit from earthquake reinforcement. Your map should visualize both density and earthquake magnitude.

## Answer:
m_4 = folium.Map(location=[35,136], tiles='cartodbpositron', zoom_start=5)
def color_producer(magnitude):
    if magnitude > 6.5:
        return 'red'
    else:
        return 'green'
Choropleth(
    geo_data=prefectures['geometry'].__geo_interface__,
    data=stats['density'],
    key_on="feature.id",
    fill_color='BuPu',
    legend_name='Population density (per square kilometer)').add_to(m_4)
for i in range(0,len(earthquakes)):
    folium.Circle(
        location=[earthquakes.iloc[i]['Latitude'], earthquakes.iloc[i]['Longitude']],
        popup=("{} ({})").format(
            earthquakes.iloc[i]['Magnitude'],
            earthquakes.iloc[i]['DateTime'].year),
        radius=earthquakes.iloc[i]['Magnitude']**5.5,
        color=color_producer(earthquakes.iloc[i]['Magnitude'])).add_to(m_4)
embed_map(m_4, 'q_4.html')