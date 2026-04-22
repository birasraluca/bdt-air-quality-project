import pandas as pd
from sklearn.linear_model import LinearRegression
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

    if len(filtered_df) < 2:
        return {
            "error": "Not enough data points to build a prediction"
        }

    filtered_df["date"] = pd.to_datetime(filtered_df["date"])
    filtered_df = filtered_df.sort_values("date").reset_index(drop=True)

    filtered_df["day_index"] = range(len(filtered_df))

    X = filtered_df[["day_index"]]
    y = filtered_df["value"]

    model = LinearRegression()
    model.fit(X, y)

    next_day_index = pd.DataFrame([[len(filtered_df)]], columns=["day_index"])
    predicted_value = model.predict(next_day_index)[0]

    last_date = filtered_df["date"].max()
    next_date = last_date + pd.Timedelta(days=1)

    return {
        "city": city,
        "parameter": parameter,
        "predicted_value": round(float(predicted_value), 2),
        "predicted_date": next_date.strftime("%Y-%m-%d"),
        "based_on_records": int(len(filtered_df))
    }