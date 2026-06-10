from .safety_stock import calculate_safety_stock

def calculate_reorder_point(avg_daily_demand, lead_time_days=7, daily_demand_std=0):
    safety_stock = calculate_safety_stock(daily_demand_std, lead_time_days)
    reorder_point = avg_daily_demand * lead_time_days + safety_stock
    return reorder_point, safety_stock