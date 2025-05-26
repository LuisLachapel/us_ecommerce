import streamlit as st
import plotly.express as px
from formatter import format_file
from components import metrics, graphics, sidebar
from streamlit_option_menu import option_menu




st.set_page_config(page_title= "Ecommerce dashboard",page_icon=":bar_chart:",layout='wide')
st.title("Ecommerce Dasboard")
data = format_file()

#navbar

main, user, products = st.columns(3)

main.button("Main",icon=":material/home:",use_container_width=True)


user.button("User",icon=":material/person:",use_container_width=True) 

products.button("Product",icon=":material/sell:",use_container_width=True)
    

#sidebar

segment, category, region = sidebar(st, data)

data_selection = data.query(
   " Segment == @segment & Region == @region & Category == @category "
)

#metricas

metrics(st,data, data_selection)


# Graficos 

graphics(st,data_selection)

