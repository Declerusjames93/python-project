
import io
from lib2to3.pytree import convert
from re import I
from matplotlib.axis import XAxis
import pandas as pd 
import numpy as np
from sqlalchemy import false 
import streamlit as st
import plotly_express as px
import plotly

# https://www.webfx.com/tools/emoji-cheat-sheet/
# configure the page
st.set_page_config(page_title="Sales Dashboard",
 page_icon=":bar_chart:",
 layout="wide"
                    )
# convert the excel spreadsheet into a pd.DataFrame series
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io ='G:\My Drive\python project\supermarkt_sales.xlsx',
        engine = 'openpyxl',
        sheet_name='Sales',
        skiprows=3,
     usecols='B:R',
        nrows=1000,
        )
#add hour column to datafram
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df
df = get_data_from_excel()
# print(df.head(10))
#display the dataframe using the page setup
test = df.astype(str)
# st.dataframe(test)
st.sidebar.header("Please, filter here: ")
city = st.sidebar.multiselect(
    "Select the City",
    options=test["City"].unique(),
    default=test["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the customer type",
    options=test["Customer_type"].unique(),
    default=test["Customer_type"].unique()
)


gender = st.sidebar.multiselect(
    "Select the gender",
    options=test["Gender"].unique(),
    default=test["Gender"].unique()
)

df_selection=test.query(
    "City== @city & Customer_type==@customer_type & Gender==@gender"
)

#Main page
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

#Key Performance Indicators
total_sales = int(df_selection["Total"].apply(lambda x: float(x)).sum())

average_rating = round(df_selection["Rating"].apply(lambda x: float(x)).mean(), 1)
star_rating = ":low_brightness:" * int(round(average_rating, 0))
average_sales_by_transaction = round(df_selection["Total"].apply(lambda x: float(x)).mean(),1)

left_column, middle_comlumn, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales")
    st.subheader(f"US $ {total_sales: }")
with middle_comlumn:
    st.subheader("Rating Everage")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average sales per transaction")
    st.subheader(F" US $ {average_sales_by_transaction}")

st.markdown("---")

#sales by product lines

df_selection["Total"]=df_selection["Total"].astype(float)
sales_by_product_line = (
    
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by=["Total"])
    )
print(sales_by_product_line)

fig_product_sales = px.bar(
sales_by_product_line, 
x="Total",
y=sales_by_product_line.index, 
orientation="h",
title="<b>Sales by product lines</b>",
color_discrete_sequence=["#0083B8"]*len(sales_by_product_line), 
template="simple_white",
)

fig_product_sales.update_layout(
    plot_bgcolor= "rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),

)
# st.plotly_chart(fig_product_sales)

#sales by hour
df_selection["hour"]=df_selection["hour"].astype(float)
sales_by_hour = (
    df_selection.groupby(by=["hour"]).sum()[["Total"]]
    )
# print(sales_by_hour)

fig_hourly_sales = px.bar(
sales_by_hour, 
x=sales_by_hour.index,
y="Total", 
# orientation="h",
title="<b>Sales by hour</b>",
color_discrete_sequence=["#0083B8"]*len(sales_by_hour), 
template="simple_white",
)

fig_hourly_sales.update_layout(
    plot_bgcolor= "rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),

)

left_column, right_column =st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)
# st.plotly_chart(fig_hourly_sales)
hide_st_style = """
                <style>
                #MainMenu {visibility:hidden;}
                footer {visibility:hidden;}
                header {visibility:hidden;}
                </style>

                """
st.markdown(hide_st_style,unsafe_allow_html=True)