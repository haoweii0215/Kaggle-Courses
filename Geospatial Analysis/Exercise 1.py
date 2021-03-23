# Exercise 1 : Your First Map
import geopandas as gpd
from learntools.core import binder
binder.bind(globals())
from learntools.geospatial.ex1 import *

## 1) Get the data.
## Use the next cell to load the shapefile located at loans_filepath to create a GeoDataFrame world_loans.
loans_filepath = "../input/geospatial-learn-course-data/kiva_loans/kiva_loans/kiva_loans.shp"

## Answer:
world_loans = gpd.read_file(loans_filepath)

## 2) Plot the data.
## Run the next code cell without changes to load a GeoDataFrame world containing country boundaries.
world_filepath = gpd.datasets.get_path('naturalearth_lowres')
world = gpd.read_file(world_filepath)

## Answer:
ax = world.plot(figsize=(20,20), color='whitesmoke', linestyle=':', edgecolor='black')
world_loans.plot(ax=ax, markersize=2)

## 3) Select loans based in the Philippines.
## Next, you'll focus on loans that are based in the Philippines.
## Use the next code cell to create a GeoDataFrame PHL_loans which contains all rows from world_loans with loans that are based in the Philippines.

## Answer:
PHL_loans = world_loans.loc[world_loans.country=="Philippines"]

## 4) Understand loans in the Philippines.
## Run the next code cell without changes to load a GeoDataFrame PHL containing boundaries for all islands in the Philippines.
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
PHL = gpd.read_file("../input/geospatial-learn-course-data/Philippines_AL258.kml", driver='KML')

## Answer:
ax = PHL.plot(figsize=(12,12), color='whitesmoke', linestyle=':', edgecolor='lightgray')
PHL_loans.plot(ax=ax, markersize=2)
