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
merge_code = ["BPLR",
    "ARCT",
    "SARC+NECS",
    "NADR+GFST",
    "NADR+GFST",
    "MEDI+NASE+NASW+NATR+CNRY",
    "MEDI+NASE+NASW+NATR+CNRY",
    "GUIA+WTRA",
    "ETRA+GUIN",
    "BENG+SATL+BRAZ",
    "SARC+NECS",
    "MEDI+NASE+NASW+NATR+CNRY",
    "ETRA+GUIN",
    "GUIA+WTRA",
    "NWCS",
    "MEDI+NASE+NASW+NATR+CNRY",
    "CARB",
    "MEDI+NASE+NASW+NATR+CNRY",
    "BENG+SATL+BRAZ",
    "FKLD",
    "BENG+SATL+BRAZ",
    "MONS+INDE+INDW+REDS+ARAB",
    "EAFR+ISSG",
    "EAFR+ISSG",
    "MONS+INDE+INDW+REDS+ARAB",
    "MONS+INDE+INDW+REDS+ARAB",
    "MONS+INDE+INDW+REDS+ARAB",
    "MONS+INDE+INDW+REDS+ARAB",
    "AUSW",
    "BERS+PSAW",
    "ALSK+PSAE+CCAL",
    "BERS+PSAW",
    "KURO+NPPF",
    "KURO+NPPF",
    "NPSW+NPTG",
    "AUSE+ARCH+SPSG+TASM",
    "AUSE+ARCH+SPSG+TASM",
    "NPSW+NPTG",
    "CAMR+PNEC",
    "PEQD",
    "WARM+SUND",
    "AUSE+ARCH+SPSG+TASM",
    "ALSK+PSAE+CCAL",
    "ALSK+PSAE+CCAL",
    "CAMR+PNEC",
    "CHIL",
    "CHIN",
    "WARM+SUND",
    "AUSE+ARCH+SPSG+TASM",
    "NEWZ",
    "SSTC",
    "SANT+FKLD",
    "ANTA+APLR",
    "ANTA+APLR"
]
lh_provs.insert(3, "merge_code", merge_code)
# I have no idea why you have to do this. Geopandas doesn't like you referencing the 0th column of a geodataframe?
lh_provs.insert(4, "merge_code1", merge_code)
lh_provs = lh_provs.dissolve(by="merge_code")

# create dataframe of polygons defined by cGENIE grid edges and points defined by cGENIE grid
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
for index1, row1 in lh_provs.iterrows():
    for index2, row2 in cgenie_cells.iterrows():
        if row2["point"].within(row1["geometry"]) == True:
            row_to_add = gpd.GeoDataFrame({"geometry": row2["geometry"], "province": row1["merge_code1"], "POC_export": row2["POC_export"]}, index=[0])
            cgenie_check = pd.concat([cgenie_check, row_to_add])

# dissolve cGENIE grid polygons according to province and sum the POC export within them
cgenie_provs = cgenie_check.dissolve(by="province", aggfunc="sum")
# divide POC export by province area to find POC export rate
cgenie_provs = gpd.GeoDataFrame({"geometry": cgenie_provs["geometry"], "POC_export": cgenie_provs["POC_export"], "POC_export_rate": cgenie_provs["POC_export"]/(cgenie_provs["geometry"].area)})
# normalise POC export contribution
cgenie_provs = gpd.GeoDataFrame({"geometry": cgenie_provs["geometry"], "POC_export": cgenie_provs["POC_export"], "POC_export_rate": cgenie_provs["POC_export_rate"], 
                                 "POC_export_contribution": cgenie_provs["POC_export_rate"]/(cgenie_provs["POC_export_rate"].sum()*0.01)})

# reorder and rename in dataframe as they appear in Li et al. 2023
cgenie_provs = cgenie_provs.reindex(["PEQD", "CAMR+PNEC", "CARB", "BENG+SATL+BRAZ", "ETRA+GUIN", "GUIA+WTRA", "CHIL", "MEDI+NASE+NASW+NATR+CNRY", "NWCS", "SARC+NECS", "NADR+GFST", "ARCT", "SSTC", "AUSW", "EAFR+ISSG", "MONS+INDE+INDW+REDS+ARAB", "ALSK+PSAE+CCAL", "BPLR", "SANT+FKLD", "NEWZ", "AUSE+ARCH+SPSG+TASM", "WARM+SUND", "NPSW+NPTG", "CHIN", "KURO+NPPF", "BERS+PSAW", "ANTA+APLR"])

# export dataframe to Excel
cgenie_provs.to_excel("cgenie_provs.xlsx")
# make cloropleth plot
cgenie_provs.plot(column="POC_export_contribution", edgecolor="black", legend=True, 
                  legend_kwds={"label": "Province POC export contribution (%)", "orientation": "horizontal"})
plt.show()


