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
lh_provs = lh_provs.dissolve(by="merge_code")
lh_provs.to_excel("lh_provs.xlsx")