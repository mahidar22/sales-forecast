import numpy as np

def calculate_safety_stock(daily_demand_std, lead_time_days=7, service_level_z=1.65):
    """Service level 95% => z=1.65"""
    return service_level_z * daily_demand_std * np.sqrt(lead_time_days)