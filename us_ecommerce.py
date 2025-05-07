import pandas as pd
import streamlit as st
import plotly.express as px
from formatter import format_file

st.set_page_config(page_title= "Ecommerce dashboard",page_icon=":bar_chart:",layout='wide')
data = format_file()


#metricas

col1, col2, col3, col4 = st.columns(4)

unique_customers = data['Customer_Id'].nunique()
number_orders = data['Order _id'].count()
total_sales = data['Sales'].sum()
total_profit = data['Profit'].sum()




with col1:
 st.metric(
    label= "# Clientes",
    value= unique_customers
)
 
with col2:
    st.metric(
    label="# Ordenes",
    value= number_orders
)

with col3:
   st.metric(
    label="Ventas",
    value= f"{total_sales:,.2f}"
)

with col4:
   st.metric(
    label="Ganancias",
    value= f"{total_profit:,.2f}"
)


#sidebar

cities = data['City'].unique() 
regions = data["Region"].unique()

st.sidebar.header("Filtros:")

city = st.sidebar.selectbox(
   label= "Ciudad",
   options= cities
)

region = st.sidebar.selectbox(
   label="Región",
   options= regions
   
)
st.dataframe(data.head(10))