import streamlit as st
import plotly.express as px
from formatter import format_file
from components import metrics, graphics, sidebar

st.set_page_config(page_title= "Ecommerce dashboard",page_icon=":bar_chart:",layout='wide')
st.title("Ecommerce Dasboard")
data = format_file()

#sidebar

segment, category, region = sidebar(st, data)

data_selection = data.query(
   " Segment == @segment & Region == @region & Category == @category "
)

#metricas

metrics(st,data, data_selection)


# Graficos 

graphics(st,data_selection)

