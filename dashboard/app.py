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

@st.cache_data(ttl=600)
def get_highest_sales_car():
    query = """
        SELECT 
            p.CarMaker,
            p.CarModel,
            SUM(CAST(f.Quantity AS DOUBLE)) AS Total_Quantity_Sold
        FROM scm_db.main.fact_sales f
        JOIN scm_db.main.dim_product p ON f.ProductID = p.ProductID
        GROUP BY p.CarMaker, p.CarModel
        ORDER BY Total_Quantity_Sold DESC
        LIMIT 1;
    """
    return con.execute(query).df()



# ----------------------------------------------------------------------
# PAGE 1: SALES OVERVIEW
# ----------------------------------------------------------------------
if page == "Sales Overview":
    st.header("Sales & Revenue Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        highest_car_df = get_highest_sales_car()
        if not highest_car_df.empty:
            maker = highest_car_df['CarMaker'].iloc[0]
            model = highest_car_df['CarModel'].iloc[0]
            qty = highest_car_df['Total_Quantity_Sold'].iloc[0]
            st.metric("Best Selling Car", f"{maker} {model}", f"{qty:,.0f} units")
            
    with col2:
        avg_sales_df = average_sales()
        if not avg_sales_df.empty:
            avg_val = avg_sales_df['Average_Order_Value'].iloc[0]
            if pd.notnull(avg_val):
                st.metric("Average Order Value", f"${avg_val:,.2f}")
            else:
                st.metric("Average Order Value", "$0.00")
            
    with col3:
        supplier_df = get_revenue_by_supplier()
        if not supplier_df.empty:
            total_rev = supplier_df['Total_Revenue'].sum()
            st.metric("Total System Revenue", f"${total_rev:,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Revenue per Month")
        df_rev_month = revenue_per_month()
        if not df_rev_month.empty:
            df_rev_month['Date'] = pd.to_datetime(df_rev_month['Year'].astype(str) + '-' + df_rev_month['Month'].astype(str) + '-01')
            df_rev_month = df_rev_month.sort_values('Date')
            fig_month = px.line(df_rev_month, x='Date', y='Monthly_Revenue', markers=True, labels={'Monthly_Revenue': 'Revenue ($)', 'Date': 'Time'})
            st.plotly_chart(fig_month, use_container_width=True)

    with col_chart2:
        st.subheader("Average Revenue by Car Type")
        df_sales_car = sales_per_car()
        if not df_sales_car.empty:
            fig_type = px.bar(df_sales_car, x='car_type', y='Average_Revenue_Per_Transaction', color='car_type', text_auto='.2s')
            st.plotly_chart(fig_type, use_container_width=True)

    col_chart3, col_chart4 = st.columns(2)
    with col_chart3:
        st.subheader("Top 10 Car Models by Revenue")
        df_rev_model = revenue_per_carmodel().head(10)
        if not df_rev_model.empty:
            fig_model = px.bar(df_rev_model, x='Total_Revenue', y='CarModel', orientation='h', text_auto='.2s').update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig_model, use_container_width=True)
            
    with col_chart4:
        st.subheader("Revenue Distribution by Credit Card Type")
        df_credit = revenue_per_credit()
        if not df_credit.empty:
            fig_credit = px.pie(df_credit, values='Total_Revenue', names='CreditCardType', hole=0.3)
            st.plotly_chart(fig_credit, use_container_width=True)

# ----------------------------------------------------------------------
# PAGE 2: CUSTOMER FEEDBACK
# ----------------------------------------------------------------------
elif page == "Customer Feedback":
    st.header("Customer Feedback Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Feedback Ratio")
        df_feedback = get_feedback_distribution()
        if not df_feedback.empty:
            fig_fb = px.pie(df_feedback, values='Total_Feedbacks', names='CustomerFeedback')
            st.plotly_chart(fig_fb, use_container_width=True)
            
    with col2:
        st.subheader("Revenue by Feedback Level")
        df_rev_feedback = get_revenue_by_feedback()
        if not df_rev_feedback.empty:
            fig_rev_fb = px.bar(df_rev_feedback, x='CustomerFeedback', y='Total_Revenue', color='CustomerFeedback', text_auto='.2s')
            st.plotly_chart(fig_rev_fb, use_container_width=True)
            
    st.markdown("---")
    
    st.subheader("Top 10 Cities with Highest Negative Feedback Rate (Bad / Very Bad)")
    df_neg_city = get_negative_feedback_by_city()
    if not df_neg_city.empty:
        fig_neg = px.bar(df_neg_city, x='City', y='Negative_Rate', text_auto='.2f', labels={'Negative_Rate': 'Negative Rate (%)'})
        st.plotly_chart(fig_neg, use_container_width=True)

    st.markdown("---")
    
    st.subheader("Customer Preference Lookup (Interactive)")
    df_prefs = get_customer_preferences()
    
    if not df_prefs.empty:
        col_sel1, col_sel2 = st.columns(2)
        with col_sel1:
            job_groups = df_prefs['job_group'].dropna().unique()
            selected_job = st.selectbox("Select Job Group:", sorted(job_groups))
        with col_sel2:
            car_models = df_prefs[df_prefs['job_group'] == selected_job]['CarModel'].dropna().unique()
            selected_model = st.selectbox("Select Car Model:", sorted(car_models))
            
        if st.button("View Concentration Area", type="primary"):
            df_focus = get_customer_location_focus(selected_job, selected_model)
            if not df_focus.empty:
                st.dataframe(df_focus, use_container_width=True, hide_index=True)
            else:
                st.info("No order data for this job group and car model combination.")
