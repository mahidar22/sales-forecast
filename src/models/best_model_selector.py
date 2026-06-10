import joblib
import os
from utils.config import MODELS_DIR

def select_best_model(models, results):
    # Select by lowest RMSE
    best_name = min(results, key=lambda k: results[k]['RMSE'])
    best_model = models[best_name]
    
    # Save
    joblib.dump(best_model, os.path.join(MODELS_DIR, 'best_model.pkl'))
    joblib.dump(best_name, os.path.join(MODELS_DIR, 'best_model_name.pkl'))
    
    return best_name, best_model