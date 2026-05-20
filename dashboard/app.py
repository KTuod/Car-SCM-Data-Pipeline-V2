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
/* Bo góc, đổ bóng cho các khối Metric (Chế độ tối) */
div[data-testid="stMetric"] {
    background-color: #262730; 
    border: 1px solid #3a3b45; 
    padding: 15px 20px;
    border-radius: 10px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3); 
    transition: transform 0.2s ease-in-out, border-color 0.2s ease-in-out; /* Bổ sung transition cho viền */
}

/* Hiệu ứng nổi lên và HIỆN VIỀN ĐỎ khi di chuột vào */
div[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.5); 
    border-color: #ff4b4b; /* <-- DÒNG MỚI BỔ SUNG: Đổi màu viền sang đỏ */
}

/* Đổi màu tiêu đề của Metric (chữ sáng màu) */
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
        

    st.markdown("---") # Thêm một đường kẻ ngang phân cách
    st.subheader("📊 Phân tích Chi tiết")

    # =================================================================
    # HÀNG 1: BIỂU ĐỒ ĐƯỜNG (TIME SERIES) - CHIẾM TOÀN BỘ CHIỀU NGANG
    # =================================================================
    df_month = chart_salesByMonth(con)
    if not df_month.empty:
        fig_month = px.line(
            df_month, 
            x=df_month.columns[0], # Cột thời gian
            y=df_month.columns[1], # Cột doanh số
            title="Xu hướng Doanh số theo tháng",
            markers=True # Hiển thị các điểm chấm trên đường
        )
        st.plotly_chart(fig_month, use_container_width=True)

    # =================================================================
    # HÀNG 2: BIỂU ĐỒ TRÒN (PIE/DONUT CHART) - CHIA 2 CỘT
    # =================================================================
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        df_color = chart_carColour(con)
        if not df_color.empty:
            # Biểu đồ Donut (có lỗ ở giữa)
            fig_color = px.pie(df_color, names=df_color.columns[0], values=df_color.columns[1], title="Tỷ lệ ưa chuộng Màu xe", hole=0.4)
            st.plotly_chart(fig_color, use_container_width=True)

    with col_chart2:
        df_credit = chart_creditCard(con)
        if not df_credit.empty:
            # Biểu đồ tròn cơ bản
            fig_credit = px.pie(df_credit, names=df_credit.columns[0], values=df_credit.columns[1], title="Phân bổ Phương thức thanh toán (Thẻ)")
            st.plotly_chart(fig_credit, use_container_width=True)

    # =================================================================
    # HÀNG 3: BIỂU ĐỒ CỘT (BAR CHART) - CHIA 2 CỘT
    # =================================================================
    col_chart3, col_chart4 = st.columns(2)

    with col_chart3:
        df_job = chart_jobGroup(con)
        if not df_job.empty:
            fig_job = px.bar(df_job, x=df_job.columns[0], y=df_job.columns[1], title="Khách hàng theo Nhóm nghề nghiệp", text_auto='.2s')
            st.plotly_chart(fig_job, use_container_width=True)

    with col_chart4:
        df_group = chart_carGroup(con)
        if not df_group.empty:
            fig_group = px.bar(df_group, x=df_group.columns[0], y=df_group.columns[1], title="Doanh số theo Phân khúc xe", text_auto='.2s')
            st.plotly_chart(fig_group, use_container_width=True)

    # =================================================================
    # HÀNG 4: MATRIX (BẢNG DỮ LIỆU ĐA CHIỀU)
    # =================================================================
    st.markdown("---")
    st.subheader("🔥 Biểu đồ nhiệt Ma trận (Heatmap)")

    col_mat1, col_mat2 = st.columns(2)

    with col_mat1:
        st.markdown("**Ma trận Loại xe & Màu sắc**")
        df_mat_color = matrix_carType_Color(con)
        
        if not df_mat_color.empty:
            # Mẹo: Đặt cột chữ đầu tiên làm hàng (Index) để Plotly hiểu nhãn của trục Y
            df_heat1 = df_mat_color.set_index(df_mat_color.columns[0])
            
            # Vẽ Heatmap bằng Plotly Express
            fig_heat1 = px.imshow(
                df_heat1,
                text_auto=True,               # Hiện số lượng trực tiếp lên từng ô màu
                aspect="auto",                # Tự động co giãn vừa vặn khung hình
                color_continuous_scale="Blues" # Tông màu xanh dương (từ nhạt đến đậm)
            )
            
            # Cập nhật layout cho đẹp hơn
            fig_heat1.update_layout(
                xaxis_title="Màu sắc xe",
                yaxis_title="Loại xe",
                coloraxis_showscale=True      # Hiện thanh thước đo màu ở bên cạnh
            )
            st.plotly_chart(fig_heat1, use_container_width=True)

    with col_mat2:
        st.markdown("**Ma trận Nghề nghiệp & Hãng xe**")
        df_mat_maker = matrix_jobGroup_carMaker(con)
        
        if not df_mat_maker.empty:
            # ĐỀ PHÒNG: Nếu SQL trả về dạng 3 cột dọc (Long format) thay vì bảng ma trận
            # Ta dùng lệnh .pivot để tự động xếp thành ma trận 2 chiều trước khi vẽ
            if len(df_mat_maker.columns) == 3:
                df_heat2 = df_mat_maker.pivot(
                    index=df_mat_maker.columns[0], 
                    columns=df_mat_maker.columns[1], 
                    values=df_mat_maker.columns[2]
                ).fillna(0)
            else:
                df_heat2 = df_mat_maker.set_index(df_mat_maker.columns[0])
                
            # Vẽ Heatmap
            fig_heat2 = px.imshow(
                df_heat2,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="Oranges" # Tông màu cam sang trọng
            )
            
            fig_heat2.update_layout(
                xaxis_title="Hãng xe",
                yaxis_title="Nhóm nghề nghiệp"
            )
            st.plotly_chart(fig_heat2, use_container_width=True)