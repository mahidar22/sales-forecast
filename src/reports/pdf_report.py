from fpdf import FPDF
import pandas as pd
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'Sales Forecasting & Inventory Report', ln=True, align='C')
        self.set_font('Helvetica', '', 10)
        self.cell(0, 8, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', ln=True, align='C')
        self.ln(5)
    
    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(30, 58, 138)
        self.cell(0, 10, title, ln=True)
        self.ln(2)
    
    def chapter_body(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, text)
        self.ln()

def generate_pdf(summary, forecast_df, inventory_df, model_results, output_path):
    pdf = PDFReport()
    pdf.add_page()
    
    pdf.chapter_title('1. Executive Summary')
    pdf.chapter_body(
        f"Total Sales: ${summary.get('total_sales',0):,.2f}\n"
        f"Total Revenue: ${summary.get('total_revenue',0):,.2f}\n"
        f"Average Daily Sales: ${summary.get('avg_daily',0):,.2f}\n"
        f"Best Model: {summary.get('best_model','N/A')}"
    )
    
    pdf.chapter_title('2. Model Performance')
    for model, metrics in model_results.items():
        pdf.chapter_body(f"{model}: RMSE={metrics['RMSE']}, MAE={metrics['MAE']}, R2={metrics['R2']}, MAPE={metrics['MAPE']}%")
    
    pdf.chapter_title('3. Sales Forecast (Next 30 Days)')
    total_forecast = forecast_df['forecast'].sum() if not forecast_df.empty else 0
    pdf.chapter_body(f"Projected 30-day sales: ${total_forecast:,.2f}\nAverage daily forecast: ${forecast_df['forecast'].mean():,.2f}")
    
    pdf.chapter_title('4. Inventory Recommendations')
    if inventory_df is not None and not inventory_df.empty:
        fast = len(inventory_df[inventory_df['movement']=='Fast-Moving'])
        slow = len(inventory_df[inventory_df['movement']=='Slow-Moving'])
        over = len(inventory_df[inventory_df['status']=='Overstocked'])
        risk = len(inventory_df[inventory_df['status']=='Stockout Risk'])
        pdf.chapter_body(f"Fast-Moving Products: {fast}\nSlow-Moving Products: {slow}\nOverstocked Items: {over}\nStockout Risks: {risk}")
    
    pdf.output(output_path)