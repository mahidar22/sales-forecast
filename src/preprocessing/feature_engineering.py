import pandas as pd
import numpy as np

def engineer_features(df):
    df = df.copy()
    
    # Ensure date
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df['year'] = df['order_date'].dt.year
        df['month'] = df['order_date'].dt.month
        df['day'] = df['order_date'].dt.day
        df['weekday'] = df['order_date'].dt.weekday
        df['is_weekend'] = df['weekday'].isin([5,6]).astype(int)
        df['quarter'] = df['order_date'].dt.quarter
    
    # Calculate sales_amount if missing
    if 'sales_amount' not in df.columns and 'quantity_sold' in df.columns and 'unit_price' in df.columns:
        df['sales_amount'] = df['quantity_sold'] * df['unit_price']
    
    # Revenue per item
    if 'quantity_sold' in df.columns and 'sales_amount' in df.columns:
        df['avg_order_value'] = df['sales_amount'] / df['quantity_sold'].replace(0, 1)
    
    return df