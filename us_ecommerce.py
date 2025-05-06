import pandas as pd
import streamlit as st
import plotly.express as px
from formatter import format_file

st.set_page_config(page_title= "Ecommerce dashboard",page_icon=":bar_chart:",layout='wide')
data = format_file()
st.dataframe(data.head(10))