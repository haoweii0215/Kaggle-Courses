# Your First Map
import geopandas as gpd

### Read in the data
full_data = gpd.read_file('./DEClands.shp')

data = full_data.loc[:, ["CLASS", "COUNTY", "geometry"]].copy()

### Select lands that fall under the "WILD FOREST" or "WILDERNESS" category
wild_lands = data.loc[data.CLASS.isin(['WILD FOREST', 'WILDERNESS'])].copy()

### Create map
wild_lands.plot()

### Campsites in New York state (Point)
POI_data = gpd.read_file("./Decptsofinterest.shp")
campsites = POI_data.loc[POI_data.ASSET=='PRIMITIVE CAMPSITE'].copy()

### Foot trails in New York state (LineString)
roads_trails = gpd.read_file("./Decroadstrails.shp")
trails = roads_trails.loc[roads_trails.ASSET=='FOOT TRAIL'].copy()

### County boundaries in New York state (Polygon)
counties = gpd.read_file("./NY_county_boundaries.shp")

### Define a base map with county boundaries
ax = counties.plot(figsize=(10,10), color='none', edgecolor='gainsboro', zorder=3)

### Add wild lands, campsites, and foot trails to the base map
wild_lands.plot(color='lightgreen', ax=ax)
campsites.plot(color='maroon', markersize=2, ax=ax)
trails.plot(color='black', markersize=1, ax=ax)

# Coordinate Reference Systems
import pandas as pd

# Load a GeoDataFrame containing regions in Ghana
regions = gpd.read_file("../input/geospatial-learn-course-data/ghana/ghana/Regions/Map_of_Regions_in_Ghana.shp")
print(regions.crs)
