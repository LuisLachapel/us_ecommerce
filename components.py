import streamlit as st
import plotly.express as px


def metrics(st,data, data_selection):
 col1, col2, col3, col4, col5 = st.columns(5)

 unique_customers = int(data['Customer_Id'].nunique())
 number_orders = int(data_selection['Order _id'].count())
 total_sales = data_selection['Sales'].sum()
 total_profit = data_selection['Profit'].sum()
 avg_satisfaction_Score = round(data_selection['Satisfaction_Score'].mean(),2)





 with col1:
  st.info("Clientes", icon="👥")
  st.metric(
    label = "&#35; Clientes",
    value= unique_customers
)
 
 with col2:
    st.info("Ordenes",icon="📦")
    st.metric(
    label="&#35; Ordenes",
    value= f"{number_orders:,}"
)

 with col3:
   st.info("Ventas", icon="💵")
   st.metric(
    label="Ventas totales",
    value= f"{total_sales:,.2f}"
)

 with col4:
   st.info("Ganancias", icon="📈")
   st.metric(
    label="Ganancias totales",
    value= f"{total_profit:,.2f}"
)

 with col5:
      st.info( "Puntuación", icon="⭐")
      st.metric(
         label="puntuación promedio",
         value = f"{avg_satisfaction_Score}"
      )


def graphics(st, data_selection):
  # Grafico de barras
 sale_by_subcategory = round(data_selection.groupby("Sub_Category")['Sales'].sum().sort_values(ascending=True).reset_index(),2)

 fig_subcategory_sales = px.bar(sale_by_subcategory, title="Ventas por subcategoria", x="Sales", y="Sub_Category", orientation="h", color_discrete_sequence= ["#00b4d8"] * len(sale_by_subcategory))


 fig_subcategory_sales.update_layout(
   yaxis_title=None
 )


#Grafico de Pastel

 color_pie = ["#003566","#f1faee", "#ffd60a"]

 fig_pie = px.pie(data_selection, values="Sales", names="Category", color_discrete_sequence=color_pie,title="Ventas por categoria")

    #st.dataframe(data_selection)


    #Color de la pagina principal
 st.markdown("""

    <style>
    section[data-testid="stSidebar"] {
    background-color: #001d3d;
    color: white;
        }
                
    </style>
    """, unsafe_allow_html=True)


    #Grafico de lineas


    # Crear columna de mes (primer día del mes)
 data_selection["Month"] = data_selection["Order Date"].dt.to_period("M").dt.to_timestamp()

    # Crear nombre del mes (formato texto) para mostrar en hover
 data_selection["month_name"] = data_selection["Month"].dt.strftime('%B %Y')

    # Agrupar Profit por mes
 monthly_profit = data_selection.groupby(["Month", "month_name"])["Profit"].sum().reset_index()

    # Crear gráfico de línea
 fig_profit_month = px.line(
        monthly_profit,
        x="Month",
        y="Profit",
        title="Ganancia Mensual",
        markers=True,
        line_shape="spline",
        color_discrete_sequence=["#00b4d8"],
        hover_name="month_name"  
    )

 fig_profit_month.update_layout(
    yaxis_title=None
    )

 st.plotly_chart(fig_profit_month, use_container_width=True)

 left_column, right_column = st.columns(2)

 left_column.plotly_chart(fig_subcategory_sales,use_container_width=True)
 right_column.plotly_chart(fig_pie,use_container_width=True)



def sidebar(st, data):
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

    if not segment or not category or not region:
        st.warning("Por favor selecciona al menos una opción en cada filtro para ver los datos.")
        st.stop()

    return segment, category, region
