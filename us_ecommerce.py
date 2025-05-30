import streamlit as st
st.set_page_config(page_title= "Ecommerce dashboard",page_icon=":bar_chart:",layout='wide')



from formatter import format_file
from components import metrics, main_graphics, sidebar, navbar,filter_data



data = format_file()


#Titulo
st.title("Dasboard principal")

#navbar
navbar(st)


#sidebar

segment, category, region = sidebar(st, data)

data_selection = filter_data(data,segment, category, region)


#metricas

metrics(st,data, data_selection)


# Graficos 

main_graphics(st,data_selection)

