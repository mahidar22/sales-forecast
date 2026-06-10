import pandas as pd
from .handle_missing import handle_missing
from .outlier_detection import detect_outliers_iqr
from .feature_engineering import engineer_features

def preprocess_pipeline(df):
    report = {}
    
    original_shape = df.shape
    report['original_shape'] = original_shape
    
    # Remove duplicates
    df = df.drop_duplicates()
    report['duplicates_removed'] = original_shape[0] - df.shape[0]
    
    # Handle missing
    df, missing_summary = handle_missing(df)
    report['missing_handled'] = missing_summary
    
    # Feature engineering
    df = engineer_features(df)
    
    # Outlier detection on numeric
    numeric_cols = ['quantity_sold', 'unit_price', 'sales_amount', 'profit']
    numeric_cols = [c for c in numeric_cols if c in df.columns]
    df, outliers = detect_outliers_iqr(df, numeric_cols)
    report['outliers_capped'] = outliers
    
    # Sort by date
    if 'order_date' in df.columns:
        df = df.sort_values('order_date')
    
    report['final_shape'] = df.shape
    
    return df, report