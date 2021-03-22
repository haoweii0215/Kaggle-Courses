import geopandas as gpd

# Read in the data
full_data = gpd.read_file('./DEClands.shp')

# View the first five rows of the data
full_data.head()