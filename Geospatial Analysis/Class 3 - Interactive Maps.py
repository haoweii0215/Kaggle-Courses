# Interactive Maps
import folium
from folium import Choropleth, Circle, Marker
from folium.plugins import HeatMap, MarkerCluster

### Create a map
m_1 = folium.Map(location=[42.32,-71.0589], tiles='openstreetmap', zoom_start=10)

### Load the data
crimes = pd.read_csv("./Data/crime.csv", encoding='latin-1')

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
districts_full = gpd.read_file('./Data/Police_Districts.shp')
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
