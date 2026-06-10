import pandas as pd
import numpy as np
import joblib
import os
from utils.config import MODELS_DIR

def forecast_future(df, days=30):
    # Load model
    model_path = os.path.join(MODELS_DIR, 'best_model.pkl')
    scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
    features_path = os.path.join(MODELS_DIR, 'features.pkl')
    name_path = os.path.join(MODELS_DIR, 'best_model_name.pkl')
    
    if not os.path.exists(model_path):
        raise Exception("Train models first")
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    features = joblib.load(features_path)
    best_name = joblib.load(name_path)
    
    # Prepare daily data
    daily = df.groupby('order_date').agg({'sales_amount': 'sum', 'quantity_sold': 'sum'}).reset_index().sort_values('order_date')
    
    for lag in [1,2,3,7,14]:
        daily[f'lag_{lag}'] = daily['sales_amount'].shift(lag)
    daily['rolling_7'] = daily['sales_amount'].rolling(7).mean()
    daily['rolling_30'] = daily['sales_amount'].rolling(30).mean()
    daily['day_of_week'] = pd.to_datetime(daily['order_date']).dt.weekday
    daily['month'] = pd.to_datetime(daily['order_date']).dt.month
    daily = daily.dropna()
    
    last_data = daily.tail(30).copy()
    forecasts = []
    last_date = pd.to_datetime(daily['order_date'].max())
    
    for i in range(days):
        next_date = last_date + pd.Timedelta(days=i+1)
        
        # Create features for prediction
        row = {
            'lag_1': last_data['sales_amount'].iloc[-1],
            'lag_2': last_data['sales_amount'].iloc[-2] if len(last_data) > 1 else last_data['sales_amount'].iloc[-1],
            'lag_3': last_data['sales_amount'].iloc[-3] if len(last_data) > 2 else last_data['sales_amount'].iloc[-1],
            'lag_7': last_data['sales_amount'].iloc[-7] if len(last_data) > 6 else last_data['sales_amount'].mean(),
            'lag_14': last_data['sales_amount'].iloc[-14] if len(last_data) > 13 else last_data['sales_amount'].mean(),
            'rolling_7': last_data['sales_amount'].tail(7).mean(),
            'rolling_30': last_data['sales_amount'].tail(30).mean(),
            'day_of_week': next_date.weekday(),
            'month': next_date.month,
            'quantity_sold': last_data['quantity_sold'].tail(7).mean()
        }
        
        X_pred = pd.DataFrame([row])[features]
        
        if best_name == 'Linear Regression':
            X_pred_scaled = scaler.transform(X_pred)
            pred = model.predict(X_pred_scaled)[0]
        elif best_name in ['Random Forest', 'XGBoost']:
            pred = model.predict(X_pred)[0]
        else:  # ARIMA fallback
            pred = last_data['sales_amount'].tail(7).mean()
        
        pred = max(0, pred)
        forecasts.append({'date': next_date, 'forecast': pred})
        
        # Update last_data for next iteration
        new_row = last_data.iloc[-1].copy()
        new_row['order_date'] = next_date
        new_row['sales_amount'] = pred
        last_data = pd.concat([last_data, pd.DataFrame([new_row])], ignore_index=True)
    
    return pd.DataFrame(forecasts), best_name