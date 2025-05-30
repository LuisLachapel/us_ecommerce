import streamlit as st
st.set_page_config(page_title= "Ecommerce dashboard",page_icon=":bar_chart:",layout='wide')
from formatter import format_file
from components import navbar, sidebar,filter_data,products_graphics


#Titulo
st.title("Dasboard productos")

#navbar

navbar(st)

data = format_file()


#sidebar

segment, category, region = sidebar(st, data)

data_selection = filter_data(data,segment, category, region)

#Graficos
products_graphics(st, data_selection)


