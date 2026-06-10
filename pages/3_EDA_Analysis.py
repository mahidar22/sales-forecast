import streamlit as st
import pandas as pd
from src.eda.visualization import *

st.set_page_config(page_title="EDA", layout="wide")
st.title("📊 3. Exploratory Data Analysis")

if 'processed_data' not in st.session_state:
    st.warning("Please preprocess data first")
    st.stop()

df = st.session_state['processed_data']
df['order_date'] = pd.to_datetime(df['order_date'])

st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${df['sales_amount'].sum():,.0f}")
col2.metric("Total Orders", f"{len(df):,}")
col3.metric("Avg Order Value", f"${df['sales_amount'].mean():.2f}")
col4.metric("Unique Products", df['product_name'].nunique())

tab1, tab2, tab3, tab4 = st.tabs(["Trends", "Products", "Categories", "Correlations"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_daily_sales(df), use_container_width=True)
    with col2:
        st.plotly_chart(plot_monthly_sales(df), use_container_width=True)

with tab2:
    st.plotly_chart(plot_product_sales(df), use_container_width=True)
    top_products = df.groupby('product_name').agg({'quantity_sold':'sum', 'sales_amount':'sum'}).sort_values('sales_amount', ascending=False).head(10)
    st.dataframe(top_products, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_category_pie(df), use_container_width=True)
    with col2:
        st.plotly_chart(plot_heatmap(df), use_container_width=True)

with tab4:
    st.plotly_chart(plot_correlation(df), use_container_width=True)
    
    st.subheader("Seasonal Patterns")
    df['month_name'] = df['order_date'].dt.month_name()
    seasonal = df.groupby('month_name')['sales_amount'].sum().reindex(['January','February','March','April','May','June','July','August','September','October','November','December'])
    st.bar_chart(seasonal)