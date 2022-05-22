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
  st.metric("Min", all_data[choice_data_exp].min())
  st.metric("q1", all_data[choice_data_exp].quantile(q=0.25))
  st.metric("Average", all_data[choice_data_exp].mean())
  st.metric("q3", all_data[choice_data_exp].quantile(q=0.75))
  st.metric("Max", all_data[choice_data_exp].max())
  st.dataframe(all_data)
elif nav == "Model Performance":
  st.write("This is Model Performance")
elif nav == "Location Optimizer":
  st.write("This is Location Optimizier")