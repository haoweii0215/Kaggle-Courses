# Manipulating Geospatial Data
!pip install geopy==1.22.0
import pandas as pd
import geopandas as gpd
import numpy as np
import folium
from folium import Marker

### Geocoding
from geopandas.tools import geocode
result = geocode("The Great Pyramid of Giza", provider="nominatim")
print(result)
point = result.geometry.iloc[0]
print("Latitude:", point.y)
print("Longitude:", point.x)

universities = pd.read_csv("./Data/top_universities.csv")
def my_geocoder(row):
    try:
        point = geocode(row, provider='nominatim').geometry.iloc[0]
        return pd.Series({'Latitude': point.y, 'Longitude': point.x, 'geometry': point})
    except:
        return None

universities[['Latitude', 'Longitude', 'geometry']] = universities.apply(lambda x: my_geocoder(x['Name']), axis=1)
print("{}% of addresses were geocoded!".format((1 - sum(np.isnan(universities["Latitude"])) / len(universities)) * 100))

### Drop universities that were not successfully geocoded
universities = universities.loc[~np.isnan(universities["Latitude"])]
universities = gpd.GeoDataFrame(universities, geometry=universities.geometry)
universities.crs = {'init': 'epsg:4326'}
universities.head()

### Create a map
m = folium.Map(location=[54, 15], tiles='openstreetmap', zoom_start=2)

### Add points to the map
for idx, row in universities.iterrows():
    Marker([row['Latitude'], row['Longitude']], popup=row['Name']).add_to(m)
    
### Table join
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
europe = world.loc[world.continent == 'Europe'].reset_index(drop=True)
europe_stats = europe[["name", "pop_est", "gdp_md_est"]]
europe_boundaries = europe[["name", "geometry"]]

### Use an attribute join to merge data about countries in Europe
europe = europe_boundaries.merge(europe_stats, on="name")

### Use spatial join to match universities to countries in Europe
european_universities = gpd.sjoin(universities, europe)

### Investigate the result
print("We located {} universities.".format(len(universities)))
print("Only {} of the universities were located in Europe (in {} different countries).".format(len(european_universities), len(european_universities.name.unique())))
