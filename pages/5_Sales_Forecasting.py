import streamlit as st
import pandas as pd
from src.forecasting.demand_prediction import forecast_future
import plotly.graph_objects as go

st.set_page_config(page_title="Forecasting", layout="wide")
st.title("🔮 5. Sales Forecasting Module")

if 'processed_data' not in st.session_state:
    st.warning("Please preprocess data first")
    st.stop()

if 'best_model_name' not in st.session_state:
    st.warning("Please train models first")
    st.stop()

df = st.session_state['processed_data']
best_name = st.session_state['best_model_name']

st.info(f"Using Best Model: **{best_name}**")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Forecast 7 Days"):
        with st.spinner("Forecasting..."):
            forecast_7, _ = forecast_future(df, 7)
            st.session_state['forecast_7'] = forecast_7
with col2:
    if st.button("Forecast 30 Days", type="primary"):
        with st.spinner("Forecasting..."):
            forecast_30, _ = forecast_future(df, 30)
            st.session_state['forecast_30'] = forecast_30
with col3:
    if st.button("Forecast 90 Days"):
        with st.spinner("Forecasting..."):
            forecast_90, _ = forecast_future(df, 90)
            st.session_state['forecast_90'] = forecast_90

# Display forecasts
for days, key in [(7,'forecast_7'), (30,'forecast_30'), (90,'forecast_90')]:
    if key in st.session_state:
        forecast = st.session_state[key]
        st.subheader(f"Next {days} Days Forecast")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Forecast", f"${forecast['forecast'].sum():,.0f}")
        col2.metric("Daily Average", f"${forecast['forecast'].mean():,.0f}")
        col3.metric("Peak Day", f"${forecast['forecast'].max():,.0f}")
        
        # Plot
        historical = df.groupby('order_date')['sales_amount'].sum().reset_index().tail(60)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=historical['order_date'], y=historical['sales_amount'], name='Historical', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=forecast['date'], y=forecast['forecast'], name='Forecast', line=dict(color='red', dash='dash')))
        fig.update_layout(title=f'{days}-Day Sales Forecast', template='plotly_white', height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(forecast, use_container_width=True)