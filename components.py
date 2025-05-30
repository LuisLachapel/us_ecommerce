import plotly.express as px


def navbar(st):
 
 main, user, products = st.columns(3)

 with main:
   mainButton = st.button("Principal",icon=":material/home:",use_container_width=True)
   if mainButton:
    st.switch_page("us_ecommerce.py")

 with user:
  userButton  = st.button("Usuarios",icon=":material/person:",use_container_width=True)
  if userButton:
    st.switch_page(r"pages\user_page.py")

 with products:
  productsButton = st.button("Productos",icon=":material/sell:",use_container_width=True)
  if productsButton:
    st.switch_page(r"pages\product_page.py")

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

 

def set_sidebar_color(st):
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            background-color: #001d3d; 
        }
        </style>
        """,
        unsafe_allow_html=True
    )



def sidebar(st, data):
    
    set_sidebar_color(st)
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


def filter_data(data, segment, category, region):
    return data.query(
        "Segment == @segment & Region == @region & Category == @category"
    ).copy()


"""Principal"""
def main_graphics(st,data_selection):
  # Grafico de barras
  sale_by_subcategory = round(data_selection.groupby("Sub_Category")['Sales'].sum().sort_values(ascending=True).reset_index(),2)

  fig_subcategory_sales = px.bar(sale_by_subcategory, title="Ventas por subcategoria", x="Sales", y="Sub_Category", orientation="h", color_discrete_sequence= ["#00b4d8"] * len(sale_by_subcategory))


  fig_subcategory_sales.update_layout(
   yaxis_title=None
 )


  #Grafico de Pastel

  color_pie = ["#003566","#f1faee", "#415a77"]

  fig_pie = px.pie(data_selection, values="Sales", names="Category", color_discrete_sequence=color_pie,title="Ventas por categoria")


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


"""Usuarios"""

def user_graphics(st,data_selection):
  
  col1, col2 = st.columns(2)

  #Grafico pastel
  color_pie = ["#1b263b", "#cae9ff", "#415a77", "#c1121f", "#e9edc9", "#2a9d8f", "#ccd5ae"]
  fig_pie = px.pie(data_selection, names="PreferredPaymentMode", color_discrete_sequence= color_pie, title="Métodos de Pago Preferidos")
  fig_pie.update_traces(
    textinfo="percent",  # Solo porcentaje
    textposition="inside" # Texto dentro del sector
)

  #Grafico historigrama
  fig_histogram= px.histogram(data_selection,nbins=10, x="Hours_On_App", color_discrete_sequence= ["#00b4d8"], title="Distribución de Horas en la Aplicación")

  fig_histogram.update_layout(
    yaxis_title = None,
    xaxis_title = "Horas en la app"
)
  

   #Grafico de barras

  fig_bar = px.bar(
    data_selection.groupby("PreferredLoginDevice")["Order _id"].count().reset_index(),
    x="Order _id",
    y="PreferredLoginDevice",
    color="PreferredLoginDevice",
    color_discrete_sequence= ["#f1faee","#2a9d8f","#415a77"],
    labels={"PreferredLoginDevice": "Dispositivo", "Order _id": "Cantidad de usuarios"},
    title="Dispositivos de inicio de sesión preferidos"
)


  fig_bar.update_layout(
    yaxis_title = None
)
  
  col1.plotly_chart(fig_pie,use_container_width=True)
  col2.plotly_chart(fig_histogram)
  st.plotly_chart(fig_bar, use_container_width=True)
    

"""Productos"""
def products_graphics(st,data_selection):
  
  col1, col2 = st.columns(2)
  col3, col4 = st.columns(2)

  #top 5 productos mas vendidos
  top_products = (
    data_selection.groupby("Product_Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head()
    .reset_index()
)
  
  fig_top_sales = px.bar(
    top_products,
    x="Sales",
    y="Product_Name",
    orientation="h",
    color_discrete_sequence= ["#00b4d8"] * len(top_products),
    title="Top 5 Productos Más Vendidos",
)

  fig_top_sales.update_layout(yaxis=dict(autorange="reversed"),yaxis_title = None)

  #grafica pastel del ship mode
  color_pie = ["#239b56","#cae9ff","#233d4d", "#2a9d8f"]
  ship_mode_order = ["Same Day", "First Class", "Second Class", "Standard Class"]
  fig_pie = px.pie(data_selection,names="Ship_Mode",color_discrete_sequence=color_pie,title="Modo de envío",category_orders={"Ship_Mode": ship_mode_order})

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
  


  #Grafico de dispersion
  fig_scatter_sales_profit = px.scatter(
    data_selection,
    x="Sales",
    y="Profit",
    color="Sub_Category",
    size="Quantity",
    hover_data=["Product_Name"],
    title="Relación entre ventas y ganancia por producto",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

  fig_scatter_sales_profit.update_layout(
    xaxis_title="Ventas ($)",
    yaxis_title="Ganancia ($)"
)
  

#Color treemap
  color_treemap = ["#003566","#f1faee", "#415a77"]

  fig_treemap = px.treemap(
    data_selection,
    path=["Category", "Sub_Category", "Product_Name"],
    values="Sales",
    title="Treemap de Ventas por categoría y producto",
    color_discrete_sequence= color_treemap
    
)
  
  col1.plotly_chart(fig_top_sales,use_container_width=True)
  col2.plotly_chart(fig_pie,use_container_width=True)
  #col3.plotly_chart(fig_pie)
  #col4.plotly_chart(fig_line_ship_mode,use_container_width=True)
  #st.plotly_chart(fig_scatter_sales_profit)
