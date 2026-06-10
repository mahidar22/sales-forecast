import streamlit as st
import pandas as pd
from src.models.train_models import train_all_models
from src.models.best_model_selector import select_best_model
import plotly.graph_objects as go

st.set_page_config(page_title="Model Training", layout="wide")
st.title("🤖 4. Model Training Module")

if 'processed_data' not in st.session_state:
    st.warning("Please preprocess data first")
    st.stop()

df = st.session_state['processed_data']

if st.button("🎯 Train All Models", type="primary"):
    with st.spinner("Training Linear Regression, Random Forest, XGBoost, and ARIMA..."):
        models, results, daily, X_test, y_test, predictions = train_all_models(df)
        best_name, best_model = select_best_model(models, results)
        
        st.session_state['models'] = models
        st.session_state['results'] = results
        st.session_state['best_model_name'] = best_name
        st.session_state['daily_data'] = daily
        st.session_state['test_predictions'] = predictions
        
        st.success(f"✅ Training complete! Best model: {best_name}")

if 'results' in st.session_state:
    results = st.session_state['results']
    best_name = st.session_state['best_model_name']
    
    st.subheader(f"🏆 Best Model: {best_name}")
    
    results_df = pd.DataFrame(results).T.reset_index().rename(columns={'index':'Model'})
    st.dataframe(results_df, use_container_width=True)
    
    # Visualization
    fig = go.Figure()
    metrics = ['MAE', 'RMSE', 'MAPE']
    for metric in metrics:
        fig.add_trace(go.Bar(name=metric, x=results_df['Model'], y=results_df[metric]))
    fig.update_layout(title="Model Comparison", barmode='group', template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    
    # Predictions vs Actual
    st.subheader("Predictions vs Actual (Test Set)")
    daily = st.session_state['daily_data']
    predictions = st.session_state['test_predictions']
    
    test_dates = daily['order_date'].tail(len(list(predictions.values())[0]))
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=test_dates, y=st.session_state['daily_data']['sales_amount'].tail(len(test_dates)), name='Actual', line=dict(color='black')))
    for name, pred in predictions.items():
        fig2.add_trace(go.Scatter(x=test_dates, y=pred, name=name, mode='lines'))
    fig2.update_layout(template='plotly_white', height=400)
    st.plotly_chart(fig2, use_container_width=True)