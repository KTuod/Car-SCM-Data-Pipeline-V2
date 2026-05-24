""" @bruin
name: streamlit_dashboard
type: python
depends:
    - gold.load_to_motherduck
description: "Upload raw Olist dataset from local storage to Cloudflare R2 (Bronze layer)."
@bruin """

import streamlit as st
import duckdb
import pandas as pd
import os
from dotenv import load_dotenv
import plotly.express as px

st.set_page_config(
    page_title = "Car SCM Data Dashboard",
    layout = "wide"
)

st.markdown("""
<style>
div[data-testid="stMetric"] {
    background-color: #262730; 
    border: 1px solid #3a3b45; 
    padding: 15px 20px;
    border-radius: 10px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3); 
    transition: transform 0.2s ease-in-out, border-color 0.2s ease-in-out; /* Bổ sung transition cho viền */
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.5); 
    border-color: #ff4b4b; /* <-- DÒNG MỚI BỔ SUNG: Đổi màu viền sang đỏ */
}


div[data-testid="stMetricLabel"] > div > div > p {
    color: #aeb4b9; 
    font-weight: 600;
    font-size: 1.1rem;
}
</style>
""", unsafe_allow_html=True)

# Load the environment variables
load_dotenv()

# Function for reading SQL files
def read_sql_file(filepath):
    with open(filepath, "r", encoding = "utf-8") as file:
        return file.read()

@st.cache_resource
def get_db_connection():
    try:
        token = os.getenv("MOTHERDUCK_TOKEN")
        if not token:
            st.error("MOTHERDUCK_TOKEN not found in the .env file")
            st.stop()
            
        con = duckdb.connect(f'md:?motherduck_token={token}')
        return con
    except Exception as e:
        st.error(f"MotherDuck connection error: {e}")
        st.stop()

con = get_db_connection()

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Sales Summary", "Customer Feedback"])

from db_queries import (
    mostPopularCarType,
    mostPopularCarMaker,
    mostCarColour,
    totalSales,
    highestSupplierSales,

    chart_salesByMonth,
    chart_carColour,
    chart_creditCard,
    chart_jobGroup,
    chart_carGroup,
    chart_carMaker,
    charts_revenueByCarMaker,
    matrix_carType_Color,
    matrix_jobGroup_carMaker
)

if page == "Sales Summary":
    # PAGE 1: SALES SUMMARY
    ## Metrics

    st.header("SALES SUMMARY")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        df_sales = totalSales(con)
        if not df_sales.empty:
            val_sales = df_sales.iloc[0, 0] 
            st.metric(label="Total Sales", value=f"{val_sales:,.0f}")

    with col2:
        df_type = mostPopularCarType(con)
        if not df_type.empty:
            val_type = df_type.iloc[0, 0]
            st.metric(label="Most Popular Type", value=str(val_type))

    with col3:
        df_maker = mostPopularCarMaker(con)
        if not df_maker.empty:
            val_maker = df_maker.iloc[0, 0]
            st.metric(label="Top Car Maker", value=str(val_maker))

    with col4:
        df_color = mostCarColour(con)
        if not df_color.empty:
            val_color = df_color.iloc[0, 0]
            st.metric(label="Most Popular Colour", value=str(val_color))

    with col5:
        df_supplier = highestSupplierSales(con)
        if not df_supplier.empty:
            val_supplier = df_supplier.iloc[0, 0]
            st.metric(label="Highest Supplier Sales", value=str(val_supplier))
        

    st.markdown("---")
    
    # Line 1
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        df_month = chart_salesByMonth(con)
        if not df_month.empty:
            fig_month = px.line(
                df_month, 
                x = df_month.columns[0],
                y = df_month.columns[1],
                title = "Revenue by Months",
                color_discrete_sequence = ['#8B0000'],
                markers = True
            )
            st.plotly_chart(fig_month, use_container_width = True)
            
    with col_chart2:
        df_carMaker = chart_carMaker(con).head(10)
        if not df_carMaker.empty:
            fig_carMaker = px.bar(
                df_carMaker,
                x = df_carMaker.columns[0],
                y = df_carMaker.columns[1],
                title = "Number of Car Sold by Car Maker",
                color = df_carMaker.columns[0]
            )
            fig_carMaker.update_layout(showlegend = False)
            st.plotly_chart(fig_carMaker, use_container_width = True)
            
    # Line 2
    df_trend = charts_revenueByCarMaker(con) 

    if not df_trend.empty:
        fig_line = px.line(
            df_trend,
            x = 'YearMonth',
            y = 'Total_Count',
            color = 'CarMaker',
            title = "Car Sales Trend by Car Maker"
        )
        
        fig_line.update_layout(
            title = {
                'font': {'size': 24}
            },
            xaxis_title = "Datetime",
            yaxis_title = "Number of Car Sold",
            legend_title = "Car Maker" 
        )
        
        fig_line.update_traces(line_shape='spline')
        st.plotly_chart(fig_line, use_container_width = True)
    
    # Line 3
    col_chart4, col_chart5 = st.columns(2)
    with col_chart4:
        df_color = chart_carColour(con).head(10)
        if not df_color.empty:
            fig_color = px.bar(
                df_color, 
                x = df_color.columns[0], 
                y = df_color.columns[1], 
                title = "Car Colour by Car Sold",
                color = df_color.columns[0]
            )
            fig_color.update_layout(showlegend = False)
            st.plotly_chart(fig_color, use_container_width = True)

    with col_chart5:
        df_credit = chart_creditCard(con).head(10)
        if not df_credit.empty:
            fig_credit = px.bar(df_credit, 
                                x = df_credit.columns[0], 
                                y = df_credit.columns[1],
                                title = "Credit Cards Used",
                                color = df_credit.columns[0])
            fig_credit.update_layout(showlegend = False)
            st.plotly_chart(fig_credit, use_container_width = True)

    # Line 4
    col_chart6, col_chart7 = st.columns(2)

    with col_chart6:
        df_job = chart_jobGroup(con).head(10)
        if not df_job.empty:
            fig_job = px.bar(df_job, 
                             x = df_job.columns[0], 
                             y = df_job.columns[1], 
                             title = "Job Group Buying Car", 
                             text_auto = '.2s',
                             color = df_job.columns[0])
            fig_job.update_layout(showlegend = False)
            st.plotly_chart(fig_job, use_container_width=True)

    with col_chart7:
        df_group = chart_carGroup(con)
        if not df_group.empty:
            fig_group = px.bar(df_group, 
                               x = df_group.columns[0], 
                               y = df_group.columns[1], 
                               title = "Number of Car Type by Car Sold",
                               color = df_group.columns[0],
                               text_auto='.2s')
            fig_group.update_layout(showlegend = False)
            st.plotly_chart(fig_group, use_container_width = True)

    # Line 4
    st.markdown("---")

    st.markdown("Car Type and Color Matrix")
    df_mat_color = matrix_carType_Color(con)
    
    if not df_mat_color.empty:
        df_heat1 = df_mat_color.pivot(
                index = df_mat_color.columns[0], 
                columns = df_mat_color.columns[1], 
                values = df_mat_color.columns[2])
        fig_heat1 = px.imshow(
            df_heat1,
            text_auto = True,
            aspect = "auto",
            color_continuous_scale = "Blues"
        )
        
        fig_heat1.update_layout(
            xaxis_title = "Car Color",
            yaxis_title = "Car Type",
            coloraxis_showscale = True
        )
        st.plotly_chart(fig_heat1, use_container_width = True)

    st.markdown("Carrier and Car Maker Matrix")
    df_mat_maker = matrix_jobGroup_carMaker(con)
    
    if not df_mat_maker.empty:
        if len(df_mat_maker.columns) == 3:
            df_heat2 = df_mat_maker.pivot(
                index=df_mat_maker.columns[0], 
                columns=df_mat_maker.columns[1], 
                values=df_mat_maker.columns[2]
            ).fillna(0)
        else:
            df_heat2 = df_mat_maker.set_index(df_mat_maker.columns[0])
            
        fig_heat2 = px.imshow(
            df_heat2,
            text_auto=True,
            aspect="auto",
            color_continuous_scale = "Oranges"
        )
        
        fig_heat2.update_layout(
            xaxis_title = "Car Maker",
            yaxis_title = "Job Group"
        )
        st.plotly_chart(fig_heat2, use_container_width = True)
        
elif page == "Customer Feedback":
    st.header("CUSTOMER FEEDBACK")
    
    