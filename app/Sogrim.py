from calendar import c
from cmath import sqrt
import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.request import urlopen
from shapely.geometry import Polygon, MultiPolygon, shape, Point
import geopandas as gpd
import json

st.set_page_config(
    page_title="Sogrim",
    page_icon="🇨🇭",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache
def load_all_data():
  data = pd.read_csv("./app/data.csv")
  data.rename(columns={"LAT_CNTR": "lat", "LONG_CNTR": "lon"}, inplace=True)
  return data

@st.cache
def load_predictions():
  data = pd.read_csv("./app/predictions.csv")
  data.rename(columns={"LAT_CNTR": "lat", "LONG_CNTR": "lon"}, inplace=True)
  return data

@st.cache
def load_aggregated():
  data = pd.read_csv("./app/aggregated.csv")
  return data

@st.cache
def load_geojson():
  with urlopen('https://datahub.io/cividi/ch-municipalities/r/gemeinden-geojson.geojson') as response:
    json_data = json.load(response)
    gdf_data = gpd.GeoDataFrame.from_features(json_data)
  return gdf_data


@st.cache
def get_data_unit(feature):
  data_unit = {
      "BEVDICHTE_SQKM_2019": "p/sqkm",
      "AUSLAENDER_ANTEIL_2019": "%",
      "ALTERSVERTEILUNG_ANTEIL_0_19_2019": "%",
      "ALTERSVERTEILUNG_ANTEIL_20_64_2019": "%",
      "ALTERSVERTEILUNG_ANTEIL_65PLUS_2019": "%",
      "PRIVATHAUSHALTE_2019": "Hshlt.",
      "GESAMTFLAECHE_SQKM_2016": "sqkm",
      "LANDWIRTSCHAFTSFLAECHE_ANTEIL_2004": "%",
      "WALD_GEHOELZE_ANTEIL_2004": "%",
      "UNPRODUKTIVE_FLAECHE_ANTEIL_2004": "%",
      "BESCHAEFTIGTE_ERSTERSEKTOR_2018": "p.",
      "BESCHAEFTIGTE_ZWEITERSEKTOR_2018": "p.",
      "BESCHAEFTIGTE_DRITTERSEKTOR_2018": "p.",
      "NEUWOHNUNGEN_PRO_1000_2018": "Wo./1,000p",
      "SOZAILHILFEQUOTE_2019": "%",
      "WAEHLERANTEIL_SP_2019": "%",
      "WAEHLERANTEIL_SVP_2019": "%",
      "AVG_INCOME_PRO_STEUERPFLPERSON": "Chf/p.",
      "ANZAHL_FAHRZEUGE": "Fhrz.",
      "ANZAHL_HALTESTELLEN_OV": "Hltst.",
      "ANZAHL_FILIALEN_MIGROS": "Fil."
  }
  return data_unit[feature]


st.sidebar.title("Sogrim")
nav = st.sidebar.radio("Navigation", ("Data Exploration", "Location Optimizer"))
st.sidebar.header("About")
st.sidebar.write("""The purpose of SOGRIM is to help Migros optimize their store locations.
For this purpose, we leverage a wide range of data points from various pubic data sources such as the Federal Bureau of Statistics.""")

if nav == "Data Exploration":
  st.write("This is Data Exploration")
  all_data = load_all_data()
  choice_data_exp = st.selectbox("Select a Feature", list(all_data.columns))
  col1, col2, col3, col4, col5, col6 = st.columns(6)
  col1.metric("Min", str(all_data[choice_data_exp].min().round(
      2))+" "+get_data_unit(choice_data_exp))
  col2.metric("q1", str(all_data[choice_data_exp].quantile(
      q=0.25).round(2))+" "+get_data_unit(choice_data_exp))
  col3.metric("Average", str(all_data[choice_data_exp].mean().round(
      2))+" "+get_data_unit(choice_data_exp))
  col4.metric("q3", str(all_data[choice_data_exp].quantile(
      q=0.75).round(2))+" "+get_data_unit(choice_data_exp))
  col5.metric("Max", str(all_data[choice_data_exp].max().round(
      2))+" "+get_data_unit(choice_data_exp))
  col6.metric("SD", str(all_data[choice_data_exp].std().round(
      2))+" "+get_data_unit(choice_data_exp))
  fig = px.histogram(all_data[choice_data_exp], nbins=int(
      len(all_data[choice_data_exp])**0.5))
  st.plotly_chart(fig, use_container_width=True)
  st.dataframe(all_data)

elif nav == "Location Optimizer":
  predictions = load_predictions()
  col1, col2 = st.columns(2)
  choice_model = col1.selectbox("Select a Model", list(predictions.drop(["GMDNAME", "lat", "lon", "ANZAHL_FILIALEN_MIGROS"], axis=1).columns))
  choice_option = col2.selectbox("Select a Group", ("Consolidation", "Perfect", "Opportunities"))

  if choice_option == "Consolidation":
    location_data = predictions[predictions[choice_model] < predictions.ANZAHL_FILIALEN_MIGROS]
  elif choice_option == "Perfect":
    location_data = predictions[predictions[choice_model] == predictions.ANZAHL_FILIALEN_MIGROS]
  elif choice_option == "Opportunities":
    location_data = predictions[predictions[choice_model] > predictions.ANZAHL_FILIALEN_MIGROS]
  
  col1, col2, col3 = st.columns(3)

  col1.metric("# Consolidations", len(predictions[predictions[choice_model] < predictions.ANZAHL_FILIALEN_MIGROS]))
  col2.metric("# Same", len(predictions[predictions[choice_model] == predictions.ANZAHL_FILIALEN_MIGROS]))
  col3.metric("# Opportunities", len(predictions[predictions[choice_model] > predictions.ANZAHL_FILIALEN_MIGROS]))

  st.map(location_data[[choice_model,"lat", "lon"]])

  st.dataframe(location_data.drop(["lat", "lon"], axis=1))

  # gpd_geojson = load_geojson()
  st.dataframe(load_geojson())

  df = load_predictions()
  geo_df = gpd.GeoDataFrame.from_features(gpd_geojson["features"]).merge(df, left_on="gemeinde.NAME", right_on="GMDNAME").set_index("GMDNAME")

  fig = px.choropleth_mapbox(geo_df,
                           geojson=geo_df.geometry,
                           locations=geo_df.index,
                           color="ANZAHL_FILIALEN_MIGROS",
                           center={"lat": 45.5517, "lon": -73.7073},
                           mapbox_style="open-street-map",
                           zoom=8.5)
  
  st.map(fig)