import streamlit as st
import pandas as pd

st.title("""
         Welcome to SOGRIM <3
         """)

def load_all_data():
  data = pd.read_csv("./app/data.csv")
  data.rename(columns={"LAT_CNTR":"lat", "LONG_CNTR":"lon"}, inplace=True)
  return data

def load_predictions():
  data = pd.read_csv("./app/predictions.csv")
  return data

st.sidebar.Title("Sogrim")
nav = st.sidebar.radio("Navigation", ("Data Exploration", "Model Performance", "Location Optimizer"))
st.sidebar.Header("About")
st.sidebar.write("""The purpose of SOGRIM is to help Migros optimize their store locations.""")

if nav == "Data Exploration":
  st.write("This is Data Exploration")
elif nav == "Model Performance":
  st.write("This is Model Performance")
elif nav == "Location Optimizer":
  st.write("This is Location Optimizier")