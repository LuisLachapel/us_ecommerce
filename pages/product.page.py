import streamlit as st
import plotly.express as px
from formatter import format_file
from components import navbar

#navbar
navbar(st)

data_selection = format_file()

#Grafico pastel


color_pie = ["#1b263b", "#cae9ff", "#415a77", "#c1121f", "#e9edc9", "#2a9d8f", "#ccd5ae"]
fig_pie = px.pie(data_selection, values="Sales",names="PreferredPaymentMode", color_discrete_sequence= color_pie)

fig_pie.update_traces(textinfo="percent",                 # Solo porcentaje
    textposition="inside",             # Texto dentro del sector
    insidetextorientation="auto")

st.plotly_chart(fig_pie,use_container_width=True)