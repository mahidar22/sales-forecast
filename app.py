import streamlit as st
import pandas as pd
from utils.helper import load_sample_data

st.set_page_config(
    page_title="Sales Forecasting & Inventory System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #1e3a8a; font-weight: 700;}
    .metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white;}
</style>
""", unsafe_allow_html=True)

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2721/2721297.png", width=80)
st.sidebar.title("Navigation")
st.sidebar.info("Upload data in **Data Upload** page to begin")

st.markdown('<p class="main-header">📊 Intelligent Sales Forecasting & Inventory Optimization</p>', unsafe_allow_html=True)
st.markdown("AI-powered system to predict demand, optimize inventory, and boost profitability.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Modules", "8", "Complete")
with col2:
    st.metric("Models", "4", "LR, RF, XGB, ARIMA")
with col3:
    st.metric("Forecast Horizon", "90 Days")
with col4:
    st.metric("Reports", "PDF & Excel")

st.markdown("---")

st.subheader("🚀 Quick Start")
st.write("""
1. **Go to Data Upload** → Upload your CSV/Excel or use sample data
2. **Preprocess** → Clean and engineer features automatically
3. **EDA Analysis** → Explore trends and patterns
4. **Train Models** → Compare 4 algorithms
5. **Forecast** → Get 7/30/90 day predictions
6. **Optimize Inventory** → Calculate reorder points
7. **Generate Reports** → Download PDF/Excel
8. **Dashboard** → View KPIs
""")

if st.button("🔄 Load Sample Dataset", type="primary"):
    df = load_sample_data()
    st.session_state['raw_data'] = df
    df.to_csv('data/raw/sales_data.csv', index=False)
    st.success(f"✅ Sample data loaded! {len(df)} records. Go to Data Upload page to view.")

st.markdown("---")
st.subheader("📋 Expected Data Format")
sample = pd.DataFrame({
    'order_date': ['2024-01-01', '2024-01-02'],
    'product_name': ['Laptop', 'Mouse'],
    'category': ['Electronics', 'Accessories'],
    'quantity_sold': [5, 20],
    'unit_price': [999.99, 25.50],
    'sales_amount': [4999.95, 510.00],
    'profit': [1000, 102],
    'region': ['North', 'South'],
    'customer_segment': ['Corporate', 'Consumer'],
    'inventory_level': [50, 150]
})
st.dataframe(sample, use_container_width=True)

st.markdown("---")
st.caption("Built with Streamlit • Python • Scikit-Learn • XGBoost • Plotly")