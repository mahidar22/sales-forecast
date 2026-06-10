import pandas as pd
import streamlit as st

def load_sample_data():
    """Generate sample sales data for demo"""
    import numpy as np
    from datetime import datetime, timedelta
    
    np.random.seed(42)
    dates = pd.date_range(end=datetime.today(), periods=365, freq='D')
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones']
    categories = ['Electronics', 'Accessories']
    regions = ['North', 'South', 'East', 'West']
    
    data = []
    for date in dates:
        for _ in range(np.random.randint(5, 15)):
            product = np.random.choice(products)
            category = 'Electronics' if product in ['Laptop', 'Monitor'] else 'Accessories'
            qty = np.random.randint(1, 10)
            price = np.random.uniform(20, 1200)
            data.append({
                'order_date': date,
                'product_name': product,
                'category': category,
                'quantity_sold': qty,
                'unit_price': round(price, 2),
                'sales_amount': round(qty * price, 2),
                'profit': round(qty * price * 0.2, 2),
                'region': np.random.choice(regions),
                'customer_segment': np.random.choice(['Consumer', 'Corporate', 'SMB']),
                'inventory_level': np.random.randint(20, 200)
            })
    
    return pd.DataFrame(data)

def format_number(num):
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return f"{num:.0f}"