import pandas as pd

def generate_excel(summary, forecast_df, inventory_df, model_results, output_path):
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Summary
        pd.DataFrame([summary]).to_excel(writer, sheet_name='Summary', index=False)
        
        # Model results
        model_df = pd.DataFrame(model_results).T.reset_index().rename(columns={'index':'Model'})
        model_df.to_excel(writer, sheet_name='Model_Performance', index=False)
        
        # Forecast
        forecast_df.to_excel(writer, sheet_name='Forecast_30D', index=False)
        
        # Inventory
        if inventory_df is not None:
            inventory_df.to_excel(writer, sheet_name='Inventory_Health', index=False)