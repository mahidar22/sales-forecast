import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_daily_sales(df):
    daily = df.groupby('order_date')['sales_amount'].sum().reset_index()
    fig = px.line(daily, x='order_date', y='sales_amount', title='Daily Sales Trend', template='plotly_white')
    fig.update_layout(height=400)
    return fig

def plot_monthly_sales(df):
    df['month_year'] = df['order_date'].dt.to_period('M').astype(str)
    monthly = df.groupby('month_year')['sales_amount'].sum().reset_index()
    fig = px.bar(monthly, x='month_year', y='sales_amount', title='Monthly Sales', template='plotly_white', color='sales_amount')
    return fig

def plot_product_sales(df):
    prod = df.groupby('product_name')['sales_amount'].sum().sort_values(ascending=False).reset_index()
    fig = px.bar(prod.head(10), x='product_name', y='sales_amount', title='Top 10 Products by Sales', color='sales_amount', template='plotly_white')
    return fig

def plot_category_pie(df):
    cat = df.groupby('category')['sales_amount'].sum().reset_index()
    fig = px.pie(cat, names='category', values='sales_amount', title='Sales by Category', hole=0.4)
    return fig

def plot_heatmap(df):
    df['weekday'] = df['order_date'].dt.day_name()
    df['hour'] = 12  # placeholder if no time
    pivot = df.pivot_table(values='sales_amount', index='weekday', columns='month', aggfunc='sum', fill_value=0)
    fig = px.imshow(pivot, title='Sales Heatmap: Weekday vs Month', aspect='auto', color_continuous_scale='Blues')
    return fig

def plot_correlation(df):
    numeric = df.select_dtypes(include=['number']).corr()
    fig = px.imshow(numeric, text_auto=True, title='Correlation Matrix', color_continuous_scale='RdBu_r')
    return fig