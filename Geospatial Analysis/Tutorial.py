# Class1 - Your First Map
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

# Class2 - Coordinate Reference Systems
import pandas as pd

### Load a GeoDataFrame containing regions in Ghana
regions = gpd.read_file("./Map_of_Regions_in_Ghana.shp")
print(regions.crs)

### Create a DataFrame with health facilities in Ghana
facilities_df = pd.read_csv("./health_facilities.csv")

### Convert the DataFrame to a GeoDataFrame
facilities = gpd.GeoDataFrame(facilities_df, geometry=gpd.points_from_xy(facilities_df.Longitude, facilities_df.Latitude))

### Set the coordinate reference system (CRS) to EPSG 4326
facilities.crs = {'init': 'epsg:4326'}

### View the first five rows of the GeoDataFrame
facilities.head()

### Create a map
ax = regions.plot(figsize=(8,8), color='whitesmoke', linestyle=':', edgecolor='black')
facilities.to_crs(epsg=32630).plot(markersize=1, ax=ax)

### The "Latitude" and "Longitude" columns are unchanged
facilities.to_crs(epsg=32630).head()

### Change the CRS to EPSG 4326
regions.to_crs("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs").head()

### Calculate the area (in square meters) of each polygon in the GeoDataFrame 
regions.loc[:, "AREA"] = regions.geometry.area / 10**6
print(f"Area of Ghana: {regions.AREA.sum()} square kilometers")
print("CRS:", regions.crs)

# Class3 - Interactive Maps
import folium
from folium import Choropleth, Circle, Marker
from folium.plugins import HeatMap, MarkerCluster

### Create a map
m_1 = folium.Map(location=[42.32,-71.0589], tiles='openstreetmap', zoom_start=10)

### Load the data
crimes = pd.read_csv("./crime.csv", encoding='latin-1')

### Drop rows with missing locations
crimes.dropna(['Lat', 'Long', 'DISTRICT'], inplace=True)

### Focus on major crimes in 2018
cols = [
  'Larceny', 'Auto Theft', 'Robbery', 'Larceny From Motor Vehicle', 'Residential Burglary',
  'Simple Assault', 'Harassment', 'Ballistics', 'Aggravated Assault', 'Other Burglary', 
  'Arson', 'Commercial Burglary', 'HOME INVASION', 'Homicide', 'Criminal Harassment', 
  'Manslaughter']
crimes = crimes[(crimes.OFFENSE_CODE_GROUP.isin(cols)) & (crimes.YEAR>=2018)]

### Plotting points
daytime_robberies = crimes[((crimes.OFFENSE_CODE_GROUP == 'Robbery') & (crimes.HOUR.isin(range(9,18))))]

### folium.Marker:Create a map
m_2 = folium.Map(location=[42.32,-71.0589], tiles='cartodbpositron', zoom_start=13)

### folium.Marker:Add points to the map
for idx, row in daytime_robberies.iterrows():
    Marker([row['Lat'], row['Long']]).add_to(m_2)

### folium.plugins.MarkerCluster:Create the map
m_3 = folium.Map(location=[42.32,-71.0589], tiles='cartodbpositron', zoom_start=13)

### folium.plugins.MarkerCluster:Add points to the map
mc = MarkerCluster()
for idx, row in daytime_robberies.iterrows():
    if not math.isnan(row['Long']) and not math.isnan(row['Lat']):
        mc.add_child(Marker([row['Lat'], row['Long']]))
m_3.add_child(mc)

### Bubble maps:Create a base map
m_4 = folium.Map(location=[42.32,-71.0589], tiles='cartodbpositron', zoom_start=13)

def color_producer(val):
    if val <= 12:
        return 'forestgreen'
    else:
        return 'darkred'

### Bubble maps:Add a bubble map to the base map
for i in range(0,len(daytime_robberies)):
    Circle(
      location=[daytime_robberies.iloc[i]['Lat'],
                daytime_robberies.iloc[i]['Long']],radius=20,
      color=color_producer(daytime_robberies.iloc[i]['HOUR'])).add_to(m_4)
    
### Heatmaps:Create a base map
m_5 = folium.Map(location=[42.32,-71.0589], tiles='cartodbpositron', zoom_start=12)

### Heatmaps:Add a heatmap to the base map
HeatMap(data=crimes[['Lat', 'Long']], radius=10).add_to(m_5)

### GeoDataFrame with geographical boundaries of Boston police districts
districts_full = gpd.read_file('.Police_Districts.shp')
districts = districts_full[["DISTRICT", "geometry"]].set_index("DISTRICT")

### Create a base map
m_6 = folium.Map(location=[42.32,-71.0589], tiles='cartodbpositron', zoom_start=12)

### Add a choropleth map to the base map
Choropleth(geo_data=districts.__geo_interface__, 
           data=plot_dict, 
           key_on="feature.id", 
           fill_color='YlGnBu', 
           legend_name='Major criminal incidents (Jan-Aug 2018)'
          ).add_to(m_6)
