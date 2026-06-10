import pandas as pd
import numpy as np

def handle_missing(df):
    df = df.copy()
    summary = {}
    
    for col in df.columns:
        missing = df[col].isnull().sum()
        if missing > 0:
            summary[col] = missing
            if df[col].dtype in ['float64', 'int64']:
                df[col].fillna(df[col].median(), inplace=True)
            else:
                df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown', inplace=True)
    
    return df, summary