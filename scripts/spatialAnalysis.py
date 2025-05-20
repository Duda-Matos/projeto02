# -*- coding: utf-8 -*-
"""
Created on Tue May 13 13:55:22 2025

@author: duda Matos
"""

#%% importação 
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import os
import folium
import matplotlib.pyplot as plt
import raterio as rio
#%%
#caminho para o arquivo shp

munPath = r"C:\Users\dudad\Documents\GitHub\ENS5132\projeto02\imputs\BR_municipios"

geoMun = gpd.read_file(munPath)

geoMun.crs

#extraindo a área - cuidado ainda não converti
geoMun['AREA_graus'] = geoMun.geometry.area 


 # Converter o CRS do gdf para o mesmo dos estados (se necessário)
geoMun = geoMun.to_crs("EPSG:3857")

geoMun['AREA_km2novo']= geoMun.geometry.area/(10**6)

geoMun = geoMun.to_crs("EPSG:4326")

geoMun['centroide']= geoMun.centroid

geoMun['boundary']= geoMun.boundary

geoMun.geometry[0].bounds

#criando um ponto e transformando em geopanda

ponto = Point(-27,-49)
pontoQualquer = gpd.GeoSeries(ponto, crs=4326) 

geoMun['dist']= [float(ponto.distance(centroid))/1000 for centroid in geoMun.centroid]

stationPath = r"C:\Users\dudad\Documents\GitHub\ENS5132\projeto02\imputs\Monitoramento_QAr_BR_latlon_2024.csv"


stations = pd.read_csv(stationPath)

gdf = gpd.GeoDataFrame(stations,
                       geometry=gpd.points_from_xy(
                           stations.LONGITUDE,stations.LATITUDE),  
                       crs="EPSG:4326")
                           

# plotando
fig, ax = plt.subplots()
geoMun.boundary.plot(ax=ax,color='gray', linewidth = 0.2)
gdf.plot(ax=ax)

# Plot usando folium 
gdf.geometry.explore()


# Buffer ao redor das estações
gdf['buffer'] = gdf.to_crs('epsg:3857').buffer(3000).to_crs('epsg:4236')

# área total monitorada
areaMonitorada = gdf['buffer'].to_crs('epsg:3857').unary_union.area/(10**6)

# área do BR
areaBR = geoMun.AREA_km2novo.sum()

# Porcentagem monitorada
porcentagemMonitorada = (areaMonitorada/areaBR)*100
print(porcentagemMonitorada)

# Unindo geometrias
geoUnion = gpd.sjoin(geoMun,gdf,how='inner')

#FIGURA COM MAPA DE FUNDO 
ax = gdf.to_crs('epsg:3857').plot(collumn=gdf['ESTADO'],figsize=(10,10),alpha=)

cx.add_basemap(ax, source = cx.providers.Esri.WorldPhysical)

#%% abrindo algum acoisa

mapBiomasPath = r"C:\Users\dudad\Documents\GitHub\ENS5132\projeto02\imputs\mapbiomas_10m_collection2_integration_v1-classification_2023.tif.crdownload"

src = rio.open(mapBiomasPath)

coord_list = [(x,y)for x,y in zip (gdf.geometry.x, gdf.geometry.y)]

#amostrando



























