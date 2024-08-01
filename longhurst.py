import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
import netCDF4 as ncdf
import matplotlib.pyplot as plt

lh_provs = gpd.read_file("Longhurst_world_v4_2010.shp")
biogem = ncdf.Dataset("biogem/fields_biogem_2d.nc", "r")
lon = np.array(biogem["lon"])
lat = np.array(biogem["lat"])
poc = biogem['bio_fexport_POC']

merge_code = [0,1,2,3,3,5,5,7,8,9,10,5,8,7,14,5,16,5,9,19,9,21,22,22,21,21,21,21,28,29,30,29,32,32,34,35,35,34,38,39,40,35,30,30,38,45,46,40,35,49,50,19,52,52,]
lh_provs.insert(3, "merge_code", merge_code)
li_provs = lh_provs.dissolve(by="merge_code")

# does this exclude some cells?
cgenie_centroids = gpd.GeoDataFrame()
for x in range(len(lon)-1):
    for y in range(len(lat)-1):
        poly = Polygon(((lon[x], lat[y]), (lon[x], lat[y+1]), (lon[x+1], lat[y+1]), (lon[x+1], lat[y])))
        cell = gpd.GeoDataFrame({"geometry": poly.centroid, "cell": poly}, index=[0])
        cgenie_centroids = pd.concat([cgenie_centroids, cell])
# add cells along borders

cgenie_check = pd.DataFrame()

# use iterrows here instead
for index1, row1 in li_provs.iterrows():
    for index2, row2 in cgenie_centroids.iterrows():
        if row2["geometry"].within(row1["geometry"]) == True:
            row_to_add = gpd.GeoDataFrame({"geometry": row2["cell"], "province": row1["ProvCode"]}, index=[0])
            cgenie_check = pd.concat([cgenie_check, row_to_add])


cgenie_provs = cgenie_check.dissolve(by="province")

cgenie_provs.plot()

plt.show()

