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
def chart_carMaker(_con):
    filepath = "queries/page_1/charts/charts_carMaker.sql"
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

@st.cache_data(ttl = 600)
def charts_revenueByCarMaker(_con):
    filepath = "queries/page_1/charts/charts_revenueByCarMaker.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def mostNegativeReviewJobGroup(_con):
    filepath = "queries/page_2/metrics/metrics_mostNegativeReviewJobGroup.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def mostPopularFeedback(_con):
    filepath = "queries/page_2/metrics/metrics_mostPopularFeedback.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def mostPopularShipMode(_con):
    filepath = "queries/page_2/metrics/metrics_mostPopularShipMode.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def mostPositiveCarMaker(_con):
    filepath = "queries/page_2/metrics/metrics_mostPositiveCarMaker.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def mostPositiveCarType(_con):
    filepath = "queries/page_2/metrics/metrics_mostPositiveCarType.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def chart_shipModeShipping(_con):
    filepath = "queries/page_2/charts/charts_ShipMode&Shipping.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def chart_shippingLeadtime(_con):
    filepath = "queries/page_2/charts/charts_ShippingLeadtime.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def chart_positiveCarMaker(_con):
    filepath = "queries/page_2/charts/charts_PositiveCarMaker.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def chart_negativeCarMaker(_con):
    filepath = "queries/page_2/charts/charts_NegativeCarMaker.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def chart_positiveCarType(_con):
    filepath = "queries/page_2/charts/charts_PositiveCarType.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def chart_negativeCarType(_con):
    filepath = "queries/page_2/charts/charts_NegativeCarType.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def matrix_feedback_carMaker(_con):
    filepath = "queries/page_2/charts/matrix_CustomerFeedback_CarMaker.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def matrix_feedback_carType(_con):
    filepath = "queries/page_2/charts/matrix_CustomerFeedback_CarType.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()

@st.cache_data(ttl = 600)
def matrix_feedback_jobGroup(_con):
    filepath = "queries/page_2/charts/matrix_CustomerFeedback_JobGroup.sql"
    query = read_sql_file(filepath)
    return _con.execute(query).df()