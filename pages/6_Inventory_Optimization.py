import streamlit as st
import pandas as pd
from src.inventory.inventory_health import analyze_inventory
from src.inventory.reorder_point import calculate_reorder_point
import plotly.express as px

st.set_page_config(page_title="Inventory", layout="wide")
st.title("📦 6. Inventory Optimization Module")

if 'processed_data' not in st.session_state:
    st.warning("Please preprocess data first")
    st.stop()

df = st.session_state['processed_data']

lead_time = st.sidebar.slider("Lead Time (days)", 3, 21, 7)
service_level = st.sidebar.selectbox("Service Level", [90, 95, 99], index=1)
z_score = {90:1.28, 95:1.65, 99:2.33}[service_level]

if st.button("Calculate Inventory Metrics", type="primary"):
    inventory_df = analyze_inventory(df)
    
    if inventory_df is not None:
        # Calculate reorder points
        results = []
        for _, row in inventory_df.iterrows():
            product_data = df[df['product_name'] == row['product_name']]
            daily_sales = product_data.groupby('order_date')['quantity_sold'].sum()
            avg_daily = daily_sales.mean()
            std_daily = daily_sales.std()
            
            rop, ss = calculate_reorder_point(avg_daily, lead_time, std_daily)
            
            results.append({
                'product_name': row['product_name'],
                'avg_daily_demand': round(avg_daily, 2),
                'safety_stock': round(ss, 2),
                'reorder_point': round(rop, 2),
                'current_inventory': row['current_inventory'],
                'recommended_order': max(0, round(rop * 1.5 - row['current_inventory'], 0)),
                'movement': row['movement'],
                'status': row['status'],
                'days_of_stock': round(row['days_of_stock'], 1)
            })
        
        inventory_results = pd.DataFrame(results)
        st.session_state['inventory_results'] = inventory_results
        st.success("✅ Inventory analysis complete!")

if 'inventory_results' in st.session_state:
    inv = st.session_state['inventory_results']
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Fast-Moving", len(inv[inv['movement']=='Fast-Moving']))
    col2.metric("Slow-Moving", len(inv[inv['movement']=='Slow-Moving']))
    col3.metric("Overstocked", len(inv[inv['status']=='Overstocked']))
    col4.metric("Stockout Risk", len(inv[inv['status']=='Stockout Risk']))
    
    tab1, tab2, tab3 = st.tabs(["Recommendations", "Stockout Risks", "Overstocked"])
    
    with tab1:
        st.dataframe(inv.sort_values('recommended_order', ascending=False), use_container_width=True)
        fig = px.bar(inv, x='product_name', y='recommended_order', color='movement', title='Recommended Order Quantities')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        risks = inv[inv['status']=='Stockout Risk']
        if not risks.empty:
            st.warning(f"⚠️ {len(risks)} products at risk!")
            st.dataframe(risks[['product_name','current_inventory','reorder_point','days_of_stock']], use_container_width=True)
        else:
            st.success("No stockout risks!")
    
    with tab3:
        over = inv[inv['status']=='Overstocked']
        if not over.empty:
            st.info(f"📦 {len(over)} overstocked products")
            st.dataframe(over[['product_name','current_inventory','days_of_stock','movement']], use_container_width=True)
        else:
            st.success("Inventory levels healthy!")