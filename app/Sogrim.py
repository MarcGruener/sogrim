import streamlit as st
import pandas as pd

st.title("""
         Welcome to SOGRIM <3
         """)

def load_all_data():
  data = pd.read_csv("/data.csv")
  data.rename(columns={"LAT_CNTR":"lat", "LONG_CNTR":"lon"}, inplace=True)
  return data

def load_predictions():
  data = pd.read_csv("/predictions.csv")
  return data

st.sidebar.write("Welcome to Sogrim")
st.sidebar.write("Navigation")
st.sidebar.radio("Navigation", ("Data Exploration", "Model Performance", "Lication Optimizer"))
st.sidebar.write("About")
st.sidebar.write("""The purpose of SOGRIM is to help Migros optimize their store locations.""")

all_data = load_all_data()

st.dataframe(all_data)
st.map(all_data)