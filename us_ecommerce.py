import streamlit as st
st.set_page_config(page_title= "Ecommerce dashboard",page_icon=":bar_chart:",layout='wide')


import plotly.express as px
from formatter import format_file
from components import metrics, graphics, sidebar, navbar



data = format_file()


#Titulo
st.title("Dasboard principal")

#navbar
navbar(st)


#sidebar

segment, category, region = sidebar(st, data)

data_selection = data.query(
   " Segment == @segment & Region == @region & Category == @category "
)

#metricas

metrics(st,data, data_selection)


# Graficos 

graphics(st,data_selection)

