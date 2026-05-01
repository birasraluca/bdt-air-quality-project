def get_model_info():
    return {
        "model_name": "Baseline Linear Regression",
        "model_type": "Regression",
        "purpose": "Predict the next daily pollutant value for a selected city and pollutant.",
        "features": ["day_index"],
        "target": "pollution value",
        "evaluation": {
            "split": "chronological 80/20 train-test split",
            "metrics": ["MAE", "RMSE", "R2 score"],
            "baseline": "previous observed value"
        },
        "notes": (
            "This is a baseline predictive model. It is intentionally simple and interpretable, "
            "which makes it suitable for demonstrating predictive analytics in the first version "
            "of the platform."
        )
    }