import os
import pandas as pd 
from dotenv import load_dotenv


def format_file():
 load_dotenv()
 source = os.getenv("SOURCE")
 data = pd.read_excel(source)
 data['Order Date'] = pd.to_datetime(data['Order Date'])
 data['Formatted_Date'] = data['Order Date'].dt.strftime('%d/%m/%Y')
 data["Order Date"] = data["Order Date"].dt.normalize()
 data['Hours_On_App'] = data['Hours_On_App'].fillna(data['Hours_On_App'].median())
 data = data.convert_dtypes()
 return data


data = format_file()


sub_category_sales = round(data.groupby("Sub_Category")['Sales'].sum().sort_values(ascending=False).reset_index(),2) 
category_sales = data.groupby("Category")['Sales'].sum().reset_index()


#print(sub_category_sales)
#print(data['Customer_Id'].nunique())