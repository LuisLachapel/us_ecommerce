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

#top 10 productos mas vendidos

top_products = (
    data_selection.groupby("Product_Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head()
    .reset_index()
)

top_products_by_quantity = data_selection.groupby("Product_Name")["Quantity"].sum().sort_values(ascending=False).head(10).reset_index()

col1, col2 = st.columns(2)
# Crear gráfico de barras
fig_top_sales = px.bar(
    top_products,
    x="Sales",
    y="Product_Name",
    orientation="h",
    color_discrete_sequence= ["#00b4d8"] * len(top_products),
    title="Top 10 Productos Más Vendidos",
)



fig_top_sales.update_layout(yaxis=dict(autorange="reversed"),yaxis_title = None)




#grafica pastel del ship mode
color_pie = ["#233d4d","#2471a3","#239b56", "#ffd60a"]
ship_mode_order = ["Same Day", "First Class", "Second Class", "Standard Class"]
fig_pie = px.pie(data_selection,names="Ship_Mode",color_discrete_sequence=color_pie,title="Modo de Envío",category_orders={"Ship_Mode": ship_mode_order})


# grafica de lineas de ship mode

data_selection["Month"] = data_selection["Order Date"].dt.to_period("M").dt.to_timestamp()
# Crear nombre del mes en formato texto para mostrar en hover
data_selection["month_name"] = data_selection["Month"].dt.strftime('%B %Y')
monthly_shipments = data_selection.groupby(["Month", "month_name", "Ship_Mode"])["Order _id"].count().reset_index()
monthly_shipments.rename(columns={"Order _id": "Ordenes"}, inplace=True)

fig_line_ship_mode = px.line(
    monthly_shipments,
    x="Month",
    y="Ordenes",
    color="Ship_Mode",
    title="Órdenes por modo de envío por mes",
    markers=True,
    line_shape="spline",
    hover_name="month_name",
    color_discrete_sequence=color_pie,
    category_orders={"Ship_Mode": ship_mode_order}
)


fig_line_ship_mode.update_layout(
    yaxis_title = None
)

fig_scatter_sales_profit = px.scatter(
    data_selection,
    x="Sales",
    y="Profit",
    color="Sub_Category",
    size="Quantity",
    hover_data=["Product_Name"],
    title="Relación entre Ventas y Ganancia por Producto",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig_scatter_sales_profit.update_layout(
    xaxis_title="Ventas ($)",
    yaxis_title="Ganancia ($)"
)


fig_treemap = px.treemap(
    data_selection,
    path=["Category", "Sub_Category", "Product_Name"],
    values="Sales",
    title="Treemap de Ventas por categoría y producto"
)



col1, col2 = st.columns(2)
col3, col4 = st.columns(2)


col1.plotly_chart(fig_top_sales,use_container_width=True)
col2.plotly_chart(fig_treemap,use_container_width=True)
col3.plotly_chart(fig_pie)
col4.plotly_chart(fig_line_ship_mode,use_container_width=True)
st.plotly_chart(fig_scatter_sales_profit)
