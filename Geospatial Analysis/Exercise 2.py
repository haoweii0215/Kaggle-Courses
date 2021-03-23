# Exercise 2 : Coordinate Reference Systems
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
from learntools.core import binder
binder.bind(globals())
from learntools.geospatial.ex2 import *

## 1) Load the data.
## Run the next code cell (without changes) to load the GPS data into a pandas DataFrame birds_df.
birds_df = pd.read_csv("../input/geospatial-learn-course-data/purple_martin.csv", parse_dates=['timestamp'])
print("There are {} different birds in the dataset.".format(birds_df["tag-local-identifier"].nunique()))

## Answer:
birds = gpd.GeoDataFrame(birds_df, geometry=gpd.points_from_xy(birds_df["location-long"], birds_df["location-lat"]))
birds.crs = {'init': 'epsg:4326'}

## 2) Plot the data.
## Next, we load in the 'naturalearth_lowres' dataset from GeoPandas, and set americas to a GeoDataFrame containing the boundaries of all countries in the Americas (both North and South America).
## Run the next code cell without changes.
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
americas = world.loc[world['continent'].isin(['North America', 'South America'])]

## Answer:
ax = americas.plot(figsize=(10,10), color='red', linestyle=':', edgecolor='gray')
birds.plot(ax=ax, markersize=10)

## 3) Where does each bird start and end its journey? (Part 1)
## Now, we're ready to look more closely at each bird's path. Run the next code cell to create two GeoDataFrames:
##    path_gdf contains LineString objects that show the path of each bird. It uses the LineString() method to create a LineString object from a list of Point objects.
##    start_gdf contains the starting points for each bird.
path_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: LineString(x)).reset_index()
path_gdf = gpd.GeoDataFrame(path_df, geometry=path_df.geometry)
path_gdf.crs = {'init' :'epsg:4326'}
start_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: x[0]).reset_index()
start_gdf = gpd.GeoDataFrame(start_df, geometry=start_df.geometry)
start_gdf.crs = {'init' :'epsg:4326'}

## Answer:
end_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: x[-1]).reset_index()
end_gdf = gpd.GeoDataFrame(end_df, geometry=end_df.geometry)
end_gdf.crs = {'init': 'epsg:4326'}

## 4) Where does each bird start and end its journey? (Part 2)
## Use the GeoDataFrames from the question above (path_gdf, start_gdf, and end_gdf) to visualize the paths of all birds on a single map. You may also want to use the americas GeoDataFrame.

## Answer:
ax = americas.plot(figsize=(10, 10), color='red', linestyle=':', edgecolor='gray')
start_gdf.plot(ax=ax, color='white',  markersize=30)
path_gdf.plot(ax=ax, cmap='tab20b', linestyle='-', linewidth=1, zorder=1)
end_gdf.plot(ax=ax, color='black', markersize=30)

## 5) Where are the protected areas in South America? (Part 1)
## It looks like all of the birds end up somewhere in South America. But are they going to protected areas?
## In the next code cell, you'll create a GeoDataFrame protected_areas containing the locations of all of the protected areas in South America. The corresponding shapefile is located at filepath protected_filepath.
protected_filepath = "../input/geospatial-learn-course-data/SAPA_Aug2019-shapefile/SAPA_Aug2019-shapefile/SAPA_Aug2019-shapefile-polygons.shp"

## Answer:
protected_areas = gpd.read_file(protected_filepath)

## 6) Where are the protected areas in South America? (Part 2)
## Create a plot that uses the protected_areas GeoDataFrame to show the locations of the protected areas in South America. (_You'll notice that some protected areas are on land, while others are in marine waters._)
south_america = americas.loc[americas['continent']=='South America']

## Answer:
ax = south_america.plot(figsize=(10,10), color='white', edgecolor='gray')
protected_areas.plot(ax=ax, alpha=0.4)

## 7) What percentage of South America is protected?
## You're interested in determining what percentage of South America is protected, so that you know how much of South America is suitable for the birds.
## As a first step, you calculate the total area of all protected lands in South America (not including marine area). To do this, you use the "REP_AREA" and "REP_M_AREA" columns, which contain the total area and total marine area, respectively, in square kilometers.
## Run the code cell below without changes.
P_Area = sum(protected_areas['REP_AREA']-protected_areas['REP_M_AREA'])
print("South America has {} square kilometers of protected areas.".format(P_Area))

## Answer:
totalArea = sum(south_america.geometry.to_crs(epsg=3035).area) / 10**6

## 8) Where are the birds in South America?
## So, are the birds in protected areas?
## Create a plot that shows for all birds, all of the locations where they were discovered in South America. Also plot the locations of all protected areas in South America.
## To exclude protected areas that are purely marine areas (with no land component), you can use the "MARINE" column (and plot only the rows in protected_areas[protected_areas['MARINE']!='2'], instead of every row in the protected_areas GeoDataFrame).

## Answer:
ax = south_america.plot(figsize=(10,10), color='red', edgecolor='gray')
protected_areas[protected_areas['MARINE']!='2'].plot(ax=ax, alpha=0.4, zorder=1)
birds[birds.geometry.y < 0].plot(ax=ax, color='white', alpha=0.6, markersize=10, zorder=2)