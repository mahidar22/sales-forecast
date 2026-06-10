import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.helper import format_number

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📈 8. Executive Dashboard")

if 'processed_data' not in st.session_state:
    st.warning("Please upload and process data first")
    st.stop()

df = st.session_state['processed_data']
df['order_date'] = pd.to_datetime(df['order_date'])

# KPIs
total_sales = df['sales_amount'].sum()
total_orders = len(df)
avg_order = df['sales_amount'].mean()
forecast_30 = st.session_state.get('forecast_30', pd.DataFrame())
forecasted_sales = forecast_30['forecast'].sum() if not forecast_30.empty else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Sales", f"${format_number(total_sales)}", delta=f"{total_sales/1e6:.1f}M")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Avg Order Value", f"${avg_order:.0f}")
col4.metric("Forecasted (30d)", f"${format_number(forecasted_sales)}")
col5.metric("Inventory Health", "85%", delta="Good")

st.markdown("---")

col1, col2 = st.columns([2,1])

with col1:
    st.subheader("Sales Trend & Forecast")
    historical = df.groupby('order_date')['sales_amount'].sum().reset_index().tail(90)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=historical['order_date'], y=historical['sales_amount'], name='Actual', fill='tozeroy'))
    
    if not forecast_30.empty:
        fig.add_trace(go.Scatter(x=forecast_30['date'], y=forecast_30['forecast'], name='Forecast', line=dict(dash='dash', color='red')))
    
    fig.update_layout(template='plotly_white', height=350, margin=dict(l=0,r=0,t=30,b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top Products")
    top = df.groupby('product_name')['sales_amount'].sum().sort_values(ascending=False).head(5)
    for i, (prod, sales) in enumerate(top.items(), 1):
        st.write(f"**{i}. {prod}**")
        st.progress(min(sales/top.max(), 1.0))
        st.caption(f"${sales:,.0f}")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Category Mix")
    cat = df.groupby('category')['sales_amount'].sum()
    fig = go.Figure(data=[go.Pie(labels=cat.index, values=cat.values, hole=0.5)])
    fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Regional Performance")
    if 'region' in df.columns:
        reg = df.groupby('region')['sales_amount'].sum().sort_values()
        st.bar_chart(reg)

with col3:
    st.subheader("Inventory Status")
    inv = st.session_state.get('inventory_results')
    if inv is not None:
        status_counts = inv['status'].value_counts()
        for status, count in status_counts.items():
            color = "🟢" if status=="Healthy" else "🟡" if status=="Overstocked" else "🔴"
            st.write(f"{color} {status}: **{count}**")
    else:
        st.info("Run Inventory Optimization")

st.markdown("---")
st.subheader("Key Insights")
col1, col2 = st.columns(2)
with col1:
    best_model = st.session_state.get('best_model_name', 'Not trained')
    st.success(f"✅ Best performing model: **{best_model}**")
    if not forecast_30.empty:
        growth = ((forecast_30['forecast'].mean() - historical['sales_amount'].mean()) / historical['sales_amount'].mean() * 100)
        st.info(f"📈 Projected growth: **{growth:.1f}%** vs last 90 days")
with col2:
    if inv is not None:
        risks = len(inv[inv['status']=='Stockout Risk'])
        if risks > 0:
            st.warning(f"⚠️ Action needed: {risks} products at stockout risk")
        else:
            st.success("✅ Inventory levels optimal")