import streamlit as st
import pandas as pd
import os
from src.reports.pdf_report import generate_pdf
from src.reports.excel_report import generate_excel
from datetime import datetime

st.set_page_config(page_title="Reports", layout="wide")
st.title("📑 7. Reports Module")

if 'processed_data' not in st.session_state:
    st.warning("Please complete previous steps")
    st.stop()

df = st.session_state['processed_data']
results = st.session_state.get('results', {})
best_model = st.session_state.get('best_model_name', 'N/A')
forecast = st.session_state.get('forecast_30', pd.DataFrame())
inventory = st.session_state.get('inventory_results', None)

summary = {
    'total_sales': df['sales_amount'].sum(),
    'total_revenue': df['sales_amount'].sum(),
    'avg_daily': df.groupby('order_date')['sales_amount'].sum().mean(),
    'best_model': best_model,
    'report_date': datetime.now().strftime('%Y-%m-%d')
}

st.subheader("Generate Reports")

col1, col2 = st.columns(2)

with col1:
    if st.button("📄 Generate PDF Report", type="primary"):
        os.makedirs('data/reports', exist_ok=True)
        pdf_path = 'data/reports/report.pdf'
        generate_pdf(summary, forecast, inventory, results, pdf_path)
        with open(pdf_path, 'rb') as f:
            st.download_button("Download PDF", f, file_name="sales_forecast_report.pdf", mime="application/pdf")
        st.success("PDF generated!")

with col2:
    if st.button("📊 Generate Excel Report", type="primary"):
        os.makedirs('data/reports', exist_ok=True)
        excel_path = 'data/reports/report.xlsx'
        generate_excel(summary, forecast, inventory, results, excel_path)
        with open(excel_path, 'rb') as f:
            st.download_button("Download Excel", f, file_name="sales_forecast_report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        st.success("Excel generated!")

st.markdown("---")
st.subheader("Report Contents")
st.write("""
**PDF Report Includes:**
- Executive Summary with KPIs
- Model Performance Comparison
- 30-Day Sales Forecast
- Inventory Health Analysis
- Recommendations

**Excel Report Includes:**
- Summary sheet
- Model_Performance sheet
- Forecast_30D sheet
- Inventory_Health sheet
""")

if not forecast.empty:
    st.subheader("Preview: Forecast Data")
    st.dataframe(forecast.head(10))