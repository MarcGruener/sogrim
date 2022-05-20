import streamlit as st
import pandas as pd

st.title("""
         Welcome to SOGRIM <3
         """)

def load_data():
  data = pd.read_excel("./models/aggregated.xlsx", "Main")
  data.rename(columns={"LAT_CNTR":"lat", "LONG_CNTR":"lon"}, inplace=True)
  return data
  
data = load_data()

st.dataframe(data)
st.map(data)