import streamlit as st
import pandas as pd

st.set_page_config(
  page_title="Sogrim",
  page_icon="🇨🇭",
  layout="wide",
  initial_sidebar_state="expanded"
)

def load_all_data():
  data = pd.read_csv("./app/data.csv")
  data.rename(columns={"LAT_CNTR":"lat", "LONG_CNTR":"lon"}, inplace=True)
  return data

def load_predictions():
  data = pd.read_csv("./app/predictions.csv")
  return data

def get_data_unit(feature):
  data_unit={
    "BEVDICHTE_SQKM_2019":"p/sqkm",
    "AUSLAENDER_ANTEIL_2019":"%",
    "ALTERSVERTEILUNG_ANTEIL_0_19_2019":"p.",
    "ALTERSVERTEILUNG_ANTEIL_20_64_2019":"p.",
    "ALTERSVERTEILUNG_ANTEIL_65PLUS_2019":"p.",
    "PRIVATHAUSHALTE_2019":"Haushalte",
    "GESAMTFLAECHE_SQKM_2019":"sqkm",
    "LANDWIRTSCHAFTSFLAECHE_Anteil_2004/09":"%",
    "WLAD_GEHOELZE_Anteil_2004/09":"%",
    "UNPRODUKTIVE_FLAECHE_Anteil_2004/09":"%",
    "BESCHÄFTIGTE_ERSTERSEKTOR_2018":"p.",
    "BESCHÄFTIGTE_ZWEITERRSEKTOR_2018":"p.",
    "BESCHÄFTIGTE_DRITTERSEKTOR_2018":"p.",
    "NEUWOHNUNGEN_PRO_1000_2018":"Wohnungen/1,000p",
    "SOZIALHILFEQUOTE_2019":"%",
    "WAEHLERANTEIL_SP_2019":"%",
    "WAEHLERANTEIL_SVP_2019":"%",
    "AVG_INCOME_PRO_STEUERPFPERSON":"Chf/p.",
    "ANZAHL_FAHRZEUGE":"Fahrzeuge",
    "ANZAHL_HALTESTELLEN_OV":"Haltestellen",
    "Anzahl Filialen Migros":"Filialen"
  }
  return data_unit[feature]


st.sidebar.title("Sogrim")
nav = st.sidebar.radio("Navigation", ("Data Exploration", "Model Performance", "Location Optimizer"))
st.sidebar.header("About")
st.sidebar.write("""The purpose of SOGRIM is to help Migros optimize their store locations.
For this purpose, we leverage a wide range of data points from various pubic data sources such as the Federal Bureau of Statistics.""")

if nav == "Data Exploration":
  st.write("This is Data Exploration")
  all_data = load_all_data()
  choice_data_exp = st.selectbox("Select a Feature", list(all_data.columns))
  st.write(choice_data_exp)
  col1, col2, col3, col4, col5 = st.columns(5)
  col1.metric("Min", all_data[choice_data_exp].min().round(2)+" "+get_data_unit(choice_data_exp))
  col2.metric("q1", all_data[choice_data_exp].quantile(q=0.25).round(2)+" "+get_data_unit(choice_data_exp))
  col3.metric("Average", all_data[choice_data_exp].mean().round(2)+" "+get_data_unit(choice_data_exp))
  col4.metric("q3", all_data[choice_data_exp].quantile(q=0.75).round(2)+" "+get_data_unit(choice_data_exp))
  col5.metric("Max", all_data[choice_data_exp].max().round(2)+" "+get_data_unit(choice_data_exp))
  st.dataframe(all_data)
elif nav == "Model Performance":
  st.write("This is Model Performance")
elif nav == "Location Optimizer":
  st.write("This is Location Optimizier")