import streamlit as st
st.set_page_config(page_title= "Ecommerce dashboard",page_icon=":bar_chart:",layout='wide')
from formatter import format_file
from components import navbar, sidebar, user_graphics,filter_data


#Titulo
st.title("Dasboard de usuarios")

#navbar
navbar(st)

data = format_file()


segment, category, region = sidebar(st, data)

data_selection = filter_data(data,segment, category, region)



#Graficos
user_graphics(st,data_selection)


