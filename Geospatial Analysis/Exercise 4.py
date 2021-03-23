# Exercise 4 : Manipulating Geospatial Data
import math
import pandas as pd
import geopandas as gpd
from learntools.geospatial.tools import geocode
import folium
from folium import Marker
from folium.plugins import MarkerCluster
from learntools.core import binder
binder.bind(globals())
from learntools.geospatial.ex4 import *

def embed_map(m, file_name):
    from IPython.display import IFrame
    m.save(file_name)
    return IFrame(file_name, width='100%', height='500px')

## 1) Geocode the missing locations.
## Run the next code cell to create a DataFrame starbucks containing Starbucks locations in the state of California.
starbucks = pd.read_csv("../input/geospatial-learn-course-data/starbucks_locations.csv")
print(starbucks.isnull().sum())
rows_with_missing = starbucks[starbucks["City"]=="Berkeley"]

## Answer:
def my_geocoder(row):
    point = geocode(row, provider='nominatim').geometry[0]
    return pd.Series({'Longitude': point.x, 'Latitude': point.y})
berkeley_locations = rows_with_missing.apply(lambda x: my_geocoder(x['Address']), axis=1)
starbucks.update(berkeley_locations)

## 2) View Berkeley locations.
## Let's take a look at the locations you just found. Visualize the (latitude, longitude) locations in Berkeley in the OpenStreetMap style.

## Answer:
for idx, row in starbucks[starbucks["City"]=='Berkeley'].iterrows():
    Marker([row['Latitude'], row['Longitude']]).add_to(m_2)

## 3) Consolidate your data.
## Run the code below to load a GeoDataFrame CA_counties containing the name, area (in square kilometers), and a unique id (in the "GEOID" column) for each county in the state of California. The "geometry" column contains a polygon with county boundaries.
CA_counties = gpd.read_file("../input/geospatial-learn-course-data/CA_county_boundaries/CA_county_boundaries/CA_county_boundaries.shp")
CA_pop = pd.read_csv("../input/geospatial-learn-course-data/CA_county_population.csv", index_col="GEOID")
CA_high_earners = pd.read_csv("../input/geospatial-learn-course-data/CA_county_high_earners.csv", index_col="GEOID")
CA_median_age = pd.read_csv("../input/geospatial-learn-course-data/CA_county_median_age.csv", index_col="GEOID")
CA_stats["density"] = CA_stats["population"] / CA_stats["area_sqkm"]

## Answer:
cols_to_add = CA_pop.join([CA_high_earners, CA_median_age]).reset_index()
CA_stats = CA_counties.merge(cols_to_add, on="GEOID")

## 4) Which counties look promising?
## Collapsing all of the information into a single GeoDataFrame also makes it much easier to select counties that meet specific criteria.
## Use the next code cell to create a GeoDataFrame sel_counties that contains a subset of the rows (and all of the columns) from the CA_stats GeoDataFrame. In particular, you should select counties where:
##     there are at least 100,000 households making $150,000 per year,
##     the median age is less than 38.5, and
##     the density of inhabitants is at least 285 (per square kilometer).
## Additionally, selected counties should satisfy at least one of the following criteria:
##     there are at least 500,000 households making $150,000 per year,
##     the median age is less than 35.5, or
##     the density of inhabitants is at least 1400 (per square kilometer).

## Answer:
sel_counties = CA_stats[((CA_stats.high_earners > 100000) &
                         (CA_stats.median_age < 38.5) &
                         (CA_stats.density > 285) &
                         ((CA_stats.median_age < 35.5) |
                         (CA_stats.density > 1400) |
                         (CA_stats.high_earners > 500000)))]

## 5) How many stores did you identify?
## When looking for the next Starbucks Reserve Roastery location, you'd like to consider all of the stores within the counties that you selected. So, how many stores are within the selected counties?
## To prepare to answer this question, run the next code cell to create a GeoDataFrame starbucks_gdf with all of the starbucks locations.
starbucks_gdf = gpd.GeoDataFrame(starbucks, geometry=gpd.points_from_xy(starbucks.Longitude, starbucks.Latitude))
starbucks_gdf.crs = {'init': 'epsg:4326'}

## Answer:
locations_of_interest = gpd.sjoin(starbucks_gdf, sel_counties)
num_stores = len(locations_of_interest)

## 6) Visualize the store locations.
## Create a map that shows the locations of the stores that you identified in the previous question.
m_6 = folium.Map(location=[37,-120], zoom_start=6)

## Answer:
mc = MarkerCluster()
locations_of_interest = gpd.sjoin(starbucks_gdf, sel_counties)
for idx, row in locations_of_interest.iterrows():
    if not math.isnan(row['Longitude']) and not math.isnan(row['Latitude']):
        mc.add_child(folium.Marker([row['Latitude'], row['Longitude']]))
m_6.add_child(mc)
