import streamlit as st
import pandas as pd

# Page 1
## Metrics
def read_sql_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

@st.cache_data(ttl = 600)
def mostPopularCarType(_con):
    filepath = "queries/page_1/metrics/metrics_mostPopularCarType.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def mostPopularCarMaker(_con):
    filepath = "queries/page_1/metrics/metrics_mostPopularCarMaker.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def mostCarColour(_con):
    filepath = "queries/page_1/metrics/metrics_mostPopularCarColour.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def totalSales(_con):
    filepath = "queries/page_1/metrics/metrics_totalSales.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def highestSupplierSales(_con):
    filepath = "queries/page_1/metrics/metrics_highestSupplierSale.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

## Charts
@st.cache_data(ttl = 600)
def chart_carColour(_con):
    filepath = "queries/page_1/charts/charts_carColor.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def chart_carGroup(_con):
    filepath = "queries/page_1/charts/charts_carGroup.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def chart_creditCard(_con):
    filepath = "queries/page_1/charts/charts_creditCard.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def chart_jobGroup(_con):
    filepath = "queries/page_1/charts/charts_jobGroup.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def chart_salesByMonth(_con):
    filepath = "queries/page_1/charts/charts_salesByMonth.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def matrix_carType_Color(_con):
    filepath = "queries/page_1/charts/matrix_carType_Color.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def matrix_jobGroup_carMaker(_con):
    filepath = "queries/page_1/charts/matrix_jobGroup_carMaker.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()