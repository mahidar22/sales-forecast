# Intelligent Sales Forecasting & Inventory Optimization System

AI-powered Streamlit application for sales forecasting and inventory optimization.

## Features

- 📤 Data Upload (CSV/Excel)
- 🧹 Automated Preprocessing
- 📊 Exploratory Data Analysis with Plotly
- 🤖 Model Training (Linear Regression, Random Forest, XGBoost, ARIMA)
- 🔮 Sales Forecasting (7/30/90 days)
- 📦 Inventory Optimization (Reorder Point, Safety Stock)
- 📑 PDF & Excel Reports
- 📈 Interactive Dashboard

## Tech Stack

Python, Streamlit, Pandas, Scikit-Learn, XGBoost, Statsmodels, Plotly

## Project Structure
```
sales_forecasting_system/
├── app.py
├── pages/
├── src/
├── data/
├── models/
└── requirements.txt
```

## Local Setup

```bash
# 1. Clone/unzip project
cd sales_forecasting_system

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Streamlit
streamlit run app.py
```
App opens at http://localhost:8501

## Sample Dataset Columns
```
order_date, product_name, category, quantity_sold, unit_price, sales_amount, profit, region, customer_segment, inventory_level
```

## Deploy to Render

### Option 1: Web Service (Manual)
1. Push code to GitHub
2. Create New Web Service on Render
3. Connect repository
4. Settings:
   - **Environment:** Python 3.11
   - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false`
   - **Instance Type:** Free or Starter

### Option 2: render.yaml (Infrastructure as Code)
Included `render.yaml` for one-click deploy.

## Environment Variables (Optional)
- `PYTHON_VERSION=3.11.9`

## License
MIT