import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from analytics.data_service import load_dataset


def predict_next_value(city: str, parameter: str):
    df = load_dataset()

    filtered_df = df[
        (df["city"].str.lower() == city.lower()) &
        (df["parameter"].str.lower() == parameter.lower())
    ].copy()

    if filtered_df.empty:
        return {
            "error": f"No data found for city='{city}' and parameter='{parameter}'"
        }

    if len(filtered_df) < 10:
        return {
            "error": "Not enough data points to build and evaluate a prediction model. At least 10 records are required."
        }

    filtered_df = filtered_df.sort_values("date").reset_index(drop=True)
    filtered_df["day_index"] = range(len(filtered_df))

    X = filtered_df[["day_index"]]
    y = filtered_df["value"]

    split_index = int(len(filtered_df) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]
    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    model = LinearRegression()
    model.fit(X_train, y_train)

    test_predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, test_predictions)
    rmse = mean_squared_error(y_test, test_predictions) ** 0.5

    if len(y_test) > 1:
        r2 = r2_score(y_test, test_predictions)
    else:
        r2 = None

    # Simple baseline: predict next value as the previous observed value
    baseline_predictions = y_test.shift(1).fillna(y_train.iloc[-1])
    baseline_mae = mean_absolute_error(y_test, baseline_predictions)
    baseline_rmse = mean_squared_error(y_test, baseline_predictions) ** 0.5

    # Refit on full available data before predicting the next day
    final_model = LinearRegression()
    final_model.fit(X, y)

    next_day_index = pd.DataFrame([[len(filtered_df)]], columns=["day_index"])
    predicted_value = final_model.predict(next_day_index)[0]

    last_date = filtered_df["date"].max()
    next_date = last_date + pd.Timedelta(days=1)

    return {
        "city": city,
        "parameter": parameter,
        "predicted_value": round(float(predicted_value), 2),
        "predicted_date": next_date.strftime("%Y-%m-%d"),
        "based_on_records": int(len(filtered_df)),
        "train_records": int(len(X_train)),
        "test_records": int(len(X_test)),

        # Top-level metrics for frontend compatibility
        "mae": round(float(mae), 3),
        "rmse": round(float(rmse), 3),
        "r2_score": round(float(r2), 3) if r2 is not None else None,

        "baseline": {
            "method": "previous value",
            "mae": round(float(baseline_mae), 3),
            "rmse": round(float(baseline_rmse), 3),
        },

        "model": {
            "type": "Linear Regression",
            "features": ["day_index"],
            "target": "value",
            "mae": round(float(mae), 3),
            "rmse": round(float(rmse), 3),
            "r2_score": round(float(r2), 3) if r2 is not None else None,
            "coefficient": round(float(final_model.coef_[0]), 5),
            "intercept": round(float(final_model.intercept_), 5),
        }
    }