import pandas as pd

def analyze_inventory(df):
    if 'inventory_level' not in df.columns:
        return None
    
    product_stats = df.groupby('product_name').agg({
        'quantity_sold': ['sum', 'mean'],
        'inventory_level': 'last',
        'sales_amount': 'sum'
    }).reset_index()
    
    product_stats.columns = ['product_name', 'total_sold', 'avg_daily_sold', 'current_inventory', 'total_sales']
    
    # Classify
    q80 = product_stats['total_sold'].quantile(0.8)
    q20 = product_stats['total_sold'].quantile(0.2)
    
    def classify(row):
        if row['total_sold'] >= q80:
            return 'Fast-Moving'
        elif row['total_sold'] <= q20:
            return 'Slow-Moving'
        else:
            return 'Medium'
    
    product_stats['movement'] = product_stats.apply(classify, axis=1)
    
    # Overstocked: inventory > 60 days of sales
    product_stats['days_of_stock'] = product_stats['current_inventory'] / product_stats['avg_daily_sold'].replace(0, 1)
    product_stats['status'] = product_stats['days_of_stock'].apply(
        lambda x: 'Overstocked' if x > 60 else ('Stockout Risk' if x < 7 else 'Healthy')
    )
    
    return product_stats