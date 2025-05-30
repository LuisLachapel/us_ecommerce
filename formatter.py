import os
import pandas as pd 
from dotenv import load_dotenv
import streamlit as st

@st.cache_data
def format_file():
 load_dotenv()
 #source = os.getenv("SOURCE")
 data = pd.read_excel("US  E-commerce records.xlsx")
 data['Order Date'] = pd.to_datetime(data['Order Date'])
 data['Formatted_Date'] = data['Order Date'].dt.strftime('%d/%m/%Y')
 data["Order Date"] = data["Order Date"].dt.normalize()
 data['Hours_On_App'] = data['Hours_On_App'].fillna(data['Hours_On_App'].median())
 data = data.convert_dtypes()
 return data


data = format_file()



#print(product.head(10))
#print(sub_category_sales)
#print(data['Customer_Id'].nunique())