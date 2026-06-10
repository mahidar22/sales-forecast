import streamlit as st
import pandas as pd
import os
from utils.helper import load_sample_data

st.set_page_config(page_title="Data Upload", layout="wide")
st.title("📤 1. Data Upload Module")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=['csv', 'xlsx', 'xls'])

col1, col2 = st.columns([2,1])
with col2:
    if st.button("Use Sample Data"):
        df = load_sample_data()
        st.session_state['raw_data'] = df
        os.makedirs('data/raw', exist_ok=True)
        df.to_csv('data/raw/sales_data.csv', index=False)
        st.success("Sample data loaded!")

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.session_state['raw_data'] = df
        os.makedirs('data/raw', exist_ok=True)
        df.to_csv('data/raw/sales_data.csv', index=False)
        st.success(f"✅ File uploaded: {uploaded_file.name}")
    except Exception as e:
        st.error(f"Error: {e}")

if 'raw_data' in st.session_state:
    df = st.session_state['raw_data']
    
    st.subheader("Dataset Preview")
    st.dataframe(df.head(20), use_container_width=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", f"{df.shape[0]:,}")
    col2.metric("Columns", df.shape[1])
    col3.metric("Date Range", f"{pd.to_datetime(df['order_date']).min().date()} to {pd.to_datetime(df['order_date']).max().date()}" if 'order_date' in df.columns else "N/A")
    col4.metric("Missing Values", df.isnull().sum().sum())
    
    tab1, tab2, tab3 = st.tabs(["Statistics", "Column Info", "Missing Values"])
    
    with tab1:
        st.dataframe(df.describe(include='all').T, use_container_width=True)
    
    with tab2:
        info_df = pd.DataFrame({
            'Column': df.columns,
            'Dtype': df.dtypes.astype(str),
            'Non-Null': df.count().values,
            'Unique': [df[c].nunique() for c in df.columns]
        })
        st.dataframe(info_df, use_container_width=True)
    
    with tab3:
        missing = df.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        if len(missing) > 0:
            st.bar_chart(missing)
            st.dataframe(missing.reset_index().rename(columns={'index':'Column', 0:'Missing Count'}))
        else:
            st.success("No missing values!")
else:
    st.info("👆 Upload a file or use sample data to begin")