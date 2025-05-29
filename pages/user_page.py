import streamlit as st
import plotly.express as px
from formatter import format_file
from components import navbar, sidebar

#navbar
navbar(st)

data = format_file()


segment, category, region = sidebar(st, data)

data_selection = data.query(
   " Segment == @segment & Region == @region & Category == @category "
)

#Grafico pastel


color_pie = ["#1b263b", "#cae9ff", "#415a77", "#c1121f", "#e9edc9", "#2a9d8f", "#ccd5ae"]
fig_pie = px.pie(data_selection, names="PreferredPaymentMode", color_discrete_sequence= color_pie, title="Métodos de Pago Preferidos")


#Grafico historigrama
fig_histogram= px.histogram(data_selection,nbins=10, x="Hours_On_App", color_discrete_sequence= ["#00b4d8"], title="Distribución de Horas en la Aplicación")

fig_histogram.update_layout(
    yaxis_title = None,
    xaxis_title = "Horas en la app"
)

fig_pie.update_traces(textinfo="percent",                 # Solo porcentaje
    textposition="inside"            # Texto dentro del sector
)

fig_bar = px.bar(
    data_selection.groupby("PreferredLoginDevice")["Order _id"].count().reset_index(),
    x="Order _id",
    y="PreferredLoginDevice",
    color_discrete_sequence= ["#00b4d8"],
    labels={"PreferredLoginDevice": "Dispositivo", "Order _id": "Cantidad de usuarios"},
    title="Dispositivos de inicio de sesión preferidos"
)


fig_bar.update_layout(
    yaxis_title = None
)

col1, col2 = st.columns(2)



col1.plotly_chart(fig_pie,use_container_width=True)
col2.plotly_chart(fig_histogram)
st.plotly_chart(fig_bar, use_container_width=True)
