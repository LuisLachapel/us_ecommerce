import pandas as pd
import streamlit as st
import plotly.express as px
from formatter import format_file

st.set_page_config(page_title= "Ecommerce dashboard",page_icon=":bar_chart:",layout='wide')
data = format_file()




#sidebar
st.sidebar.header("Filtros:")




segment = st.sidebar.multiselect(
   label="Segmento",
   options = data['Segment'].unique(),
   default = data['Segment'].unique()
)

category = st.sidebar.multiselect(
   label="Categoria",
   options = data['Category'].unique(),
   default= data['Category'].unique()
)


region = st.sidebar.multiselect(
   label="Región",
   options= data["Region"].unique(),
   default= data["Region"].unique()
   
)


data_selection = data.query(
   " Segment == @segment & Region == @region & Category == @category "
)


#metricas

col1, col2, col3, col4, col5 = st.columns(5)

unique_customers = int(data['Customer_Id'].nunique())
number_orders = int(data_selection['Order _id'].count())
total_sales = data_selection['Sales'].sum()
total_profit = data_selection['Profit'].sum()
avg_satisfaction_Score = round(data_selection['Satisfaction_Score'].mean(),2)
star_rating = ":star:" * int(round(data_selection['Satisfaction_Score'].mean(),0))
max_stars = 5
stars = "⭐" * int(min(round(avg_satisfaction_Score), max_stars))




with col1:
 st.metric(
    label = "&#35; Clientes",
    value= unique_customers
)
 
with col2:
    st.metric(
    label="&#35; Ordenes",
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
   
   with col5:
      st.metric(
         label="AVG Puntuación",
         value = f"{avg_satisfaction_Score}"
      )


st.dataframe(data_selection)