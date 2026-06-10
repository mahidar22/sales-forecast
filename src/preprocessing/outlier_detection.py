import pandas as pd
import numpy as np

def detect_outliers_iqr(df, columns):
    df = df.copy()
    outliers_count = {}
    
    for col in columns:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            
            outliers = ((df[col] < lower) | (df[col] > upper)).sum()
            outliers_count[col] = int(outliers)
            
            # Cap outliers
            df[col] = np.where(df[col] < lower, lower, df[col])
            df[col] = np.where(df[col] > upper, upper, df[col])
    
    return df, outliers_count