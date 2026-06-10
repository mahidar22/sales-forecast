import streamlit as st
import pandas as pd
from src.preprocessing.clean_data import preprocess_pipeline
import os

st.set_page_config(page_title="Preprocessing", layout="wide")
st.title("🧹 2. Data Preprocessing Module")

if 'raw_data' not in st.session_state:
    st.warning("Please upload data first in Data Upload page")
    st.stop()

df = st.session_state['raw_data']

if st.button("🚀 Run Preprocessing Pipeline", type="primary"):
    with st.spinner("Processing..."):
        processed_df, report = preprocess_pipeline(df)
        
        st.session_state['processed_data'] = processed_df
        st.session_state['preprocess_report'] = report
        
        os.makedirs('data/processed', exist_ok=True)
        processed_df.to_csv('data/processed/processed_sales.csv', index=False)
        
        st.success("✅ Preprocessing Complete!")

if 'processed_data' in st.session_state:
    processed = st.session_state['processed_data']
    report = st.session_state['preprocess_report']
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Original Rows", report['original_shape'][0])
    col2.metric("Duplicates Removed", report['duplicates_removed'])
    col3.metric("Final Rows", report['final_shape'][0])
    
    st.subheader("Preprocessing Summary")
    st.json(report)
    
    tab1, tab2 = st.tabs(["Original Data", "Processed Data"])
    with tab1:
        st.dataframe(df.head(20), use_container_width=True)
    with tab2:
        st.dataframe(processed.head(20), use_container_width=True)
        st.download_button("Download Processed CSV", processed.to_csv(index=False), "processed_sales.csv")
else:
    st.info("Click button to run preprocessing")