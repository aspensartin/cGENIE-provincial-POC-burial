import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point
import netCDF4 as ncdf
import matplotlib.pyplot as plt

# read in Longhurst provinces shapefile
lh_provs = gpd.read_file("Longhurst_world_v4_2010.shp")
# read in cGENIE 2D biogem output
biogem = ncdf.Dataset("biogem/fields_biogem_2d.nc", "r")
lon = np.array(biogem["lon"])
lat = np.array(biogem["lat"])
lon_edges = np.array(biogem["lon_edges"])
lat_edges = np.array(biogem["lat_edges"])
# select final timeslice of POC export
poc = np.array(biogem['bio_fexport_POC'][12, :, :])
# rotate POC export grid to align with lon & lat axes
poc = np.flip(np.rot90(poc, k=3, axes=(1,0)), axis=0)
# mask out land cell values
poc = np.ma.masked_greater(poc, 1e36)

# define Longhurst provinces to be merged to provinces of Li et al. (2023) Nature 613 90-95
merge_code = [0,1,2,3,3,5,5,7,8,9,10,5,8,7,14,5,16,5,9,19,9,21,22,22,21,21,21,21,28,29,30,29,32,32,34,35,35,34,38,39,40,35,30,30,38,45,46,40,35,49,50,19,52,52]
lh_provs.insert(3, "merge_code", merge_code)
li_provs = lh_provs.dissolve(by="merge_code")

# create GeoDataFrame of polygons defined by cGENIE grid edges and points defined by cGENIE grid
cgenie_cells = gpd.GeoDataFrame()
for x in range(len(lon)):
    for y in range(len(lat)):
            cell = gpd.GeoDataFrame({
                 "geometry": Polygon([(lon_edges[x], lat_edges[y]), (lon_edges[x+1], lat_edges[y]), (lon_edges[x+1], lat_edges[y+1]), (lon_edges[x], lat_edges[y+1])]),
                 "point": Point([lon[x], lat[y]])}, index=[0])
            cgenie_cells = pd.concat([cgenie_cells, cell])

# add POC export per grid cell to GeoDataFrame
cgenie_cells = gpd.GeoDataFrame({"geometry": cgenie_cells["geometry"], "point": cgenie_cells["point"], "POC_export": poc.flatten()})
cgenie_check = pd.DataFrame()

# iterate over Li et al. provinces and cGENIE grid points to identify which grid cells belong to which province
for index1, row1 in li_provs.iterrows():
    for index2, row2 in cgenie_cells.iterrows():
        if row2["point"].within(row1["geometry"]) == True:
            row_to_add = gpd.GeoDataFrame({"geometry": row2["geometry"], "province": row1["ProvCode"], "POC_export": row2["POC_export"]}, index=[0])
            cgenie_check = pd.concat([cgenie_check, row_to_add])

# dissolve cGENIE grid polygons according to province and sum the POC export within them
cgenie_provs = cgenie_check.dissolve(by="province", aggfunc="sum")
# divide POC export by province area to find POC export rate
cgenie_provs = gpd.GeoDataFrame({"geometry": cgenie_provs["geometry"], "POC_export": cgenie_provs["POC_export"], "POC_export_rate": cgenie_provs["POC_export"]/(cgenie_provs["geometry"].area)})
# normalise POC export contribution
cgenie_provs = gpd.GeoDataFrame({"geometry": cgenie_provs["geometry"], "POC_export": cgenie_provs["POC_export"], "POC_export_rate": cgenie_provs["POC_export_rate"], 
                                 "POC_export_contribution": cgenie_provs["POC_export_rate"]/(cgenie_provs["POC_export_rate"].sum()*0.01)})

# export GeoDataFrame to Excel
cgenie_provs.to_excel("cgenie_provs.xlsx")
# make cloropleth plot
cgenie_provs.plot(column="POC_export_contribution", edgecolor="black", legend=True, 
                  legend_kwds={"label": "Province POC export contribution (%)", "orientation": "horizontal"})
plt.show()

