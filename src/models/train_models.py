import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from statsmodels.tsa.arima.model import ARIMA
import joblib
import os
from utils.metrics import evaluate
from utils.config import MODELS_DIR

def prepare_features(df):
    # Aggregate daily
    daily = df.groupby('order_date').agg({
        'sales_amount': 'sum',
        'quantity_sold': 'sum'
    }).reset_index().sort_values('order_date')
    
    # Create lags
    for lag in [1,2,3,7,14]:
        daily[f'lag_{lag}'] = daily['sales_amount'].shift(lag)
    
    daily['rolling_7'] = daily['sales_amount'].rolling(7).mean()
    daily['rolling_30'] = daily['sales_amount'].rolling(30).mean()
    daily['day_of_week'] = pd.to_datetime(daily['order_date']).dt.weekday
    daily['month'] = pd.to_datetime(daily['order_date']).dt.month
    
    daily = daily.dropna()
    
    features = [c for c in daily.columns if c not in ['order_date', 'sales_amount']]
    X = daily[features]
    y = daily['sales_amount']
    
    return X, y, daily, features

def train_all_models(df):
    X, y, daily, features = prepare_features(df)
    
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    models = {}
    results = {}
    
    # Linear Regression
    lr = LinearRegression()
    lr.fit(X_train_scaled, y_train)
    pred_lr = lr.predict(X_test_scaled)
    models['Linear Regression'] = lr
    results['Linear Regression'] = evaluate(y_test, pred_lr)
    
    # Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    pred_rf = rf.predict(X_test)
    models['Random Forest'] = rf
    results['Random Forest'] = evaluate(y_test, pred_rf)
    
    # XGBoost
    xgb = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42, verbosity=0)
    xgb.fit(X_train, y_train)
    pred_xgb = xgb.predict(X_test)
    models['XGBoost'] = xgb
    results['XGBoost'] = evaluate(y_test, pred_xgb)
    
    # ARIMA
    try:
        arima = ARIMA(y_train, order=(5,1,0))
        arima_fit = arima.fit()
        pred_arima = arima_fit.forecast(steps=len(y_test))
        models['ARIMA'] = arima_fit
        results['ARIMA'] = evaluate(y_test, pred_arima)
    except:
        results['ARIMA'] = {'MAE': 9999, 'RMSE': 9999, 'MAPE': 9999, 'R2': -1}
    
    # Save scaler and features
    joblib.dump(scaler, os.path.join(MODELS_DIR, 'scaler.pkl'))
    joblib.dump(features, os.path.join(MODELS_DIR, 'features.pkl'))
    
    return models, results, daily, X_test, y_test, {'Linear Regression': pred_lr, 'Random Forest': pred_rf, 'XGBoost': pred_xgb}