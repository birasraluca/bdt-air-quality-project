def get_model_info():
    return {
        "model_name": "Baseline Linear Regression",
        "model_type": "Regression",
        "purpose": "Predict next pollutant value for a selected city and parameter",
        "features": ["day_index"],
        "target": "pollution value",
        "metrics": ["MAE", "RMSE"],
        "notes": "This is a baseline predictive model used for the initial version of the project."
    }