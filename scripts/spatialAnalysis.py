# -*- coding: utf-8 -*-
"""
Created on Tue May 13 13:55:22 2025

@author: duda Matos
"""

#%% importação 
import geopandas as gpd
import pandas as pd
from shapely.geometry import point
import os
import folium
#%%
#caminho para o arquivo shp

munPath = r"C:\Users\dudad\Documents\GitHub\ENS5132\projeto02\imputs\BR_municipios"

geoMun = gpd.read_file(munPath)

geoMun.crs

#extraindo a área - cuidado ainda não converti
geoMun['AREA_graus'] = geoMun.geometry.area 


 # Converter o CRS do gdf para o mesmo dos estados (se necessário)
geoMun = geoMun.to_crs("EPSG:3857")

geoMun['area_km2novo']= geoMun.geometry.area/(10**6)

geoMun = geoMun.to_crs("EPSG:4326")

geoMun['centroide']= geoMun.centroid

geoMun['boundary']= geoMun.boundary

geoMun.geometry[0].bounds

#criando um ponto e transformando em geopanda

ponto = point(-27,-49)
gpd.GeoSeries(ponto, crs=4326) 

geoMun['dist']= [float(ponto.distance(centroid))/1000 for centroid in geoMun.centroid]

stationPath = r"C:\Users\dudad\Documents\GitHub\ENS5132\projeto02\imputs\Monitoramento_QAr_BR_latlon_2024.csv"


stations = pd.read_csv(stationsPath)

gpf = gpd.points_from_xy(
                           stations.LONGITUDE,stations.LATITUDE),
                       crs="EPS:4326")

#%% plotando
fig, ax = plot.subplots