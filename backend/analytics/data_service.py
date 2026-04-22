import os
import pandas as pd


DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../data/processed/sample_air_quality.csv"
)


def load_dataset():
    return pd.read_csv(DATA_PATH)


def get_available_cities():
    df = load_dataset()
    cities = sorted(df["city"].dropna().unique().tolist())
    return cities


def get_available_parameters():
    df = load_dataset()
    parameters = sorted(df["parameter"].dropna().unique().tolist())
    return parameters


def get_pollution_timeseries(city: str, parameter: str):
    df = load_dataset()

    filtered_df = df[
        (df["city"].str.lower() == city.lower()) &
        (df["parameter"].str.lower() == parameter.lower())
    ].copy()

    if filtered_df.empty:
        return {
            "error": f"No data found for city='{city}' and parameter='{parameter}'"
        }

    filtered_df["date"] = pd.to_datetime(filtered_df["date"])
    filtered_df = filtered_df.sort_values("date")

    data = [
        {
            "date": row["date"].strftime("%Y-%m-%d"),
            "value": float(row["value"])
        }
        for _, row in filtered_df.iterrows()
    ]

    return {
        "city": city,
        "parameter": parameter,
        "data": data
    }


def get_average_by_city(parameter: str):
    df = load_dataset()

    filtered_df = df[df["parameter"].str.lower() == parameter.lower()].copy()

    if filtered_df.empty:
        return {
            "error": f"No data found for parameter='{parameter}'"
        }

    grouped_df = (
        filtered_df.groupby("city", as_index=False)["value"]
        .mean()
        .sort_values("value", ascending=False)
    )

    cities = [
        {
            "city": row["city"],
            "avg_value": round(float(row["value"]), 2)
        }
        for _, row in grouped_df.iterrows()
    ]

    return {
        "parameter": parameter,
        "cities": cities
    }


def get_latest_by_city(parameter: str):
    df = load_dataset()

    filtered_df = df[df["parameter"].str.lower() == parameter.lower()].copy()

    if filtered_df.empty:
        return {
            "error": f"No data found for parameter='{parameter}'"
        }

    filtered_df["date"] = pd.to_datetime(filtered_df["date"])
    filtered_df = filtered_df.sort_values(["city", "date"])

    latest_rows = filtered_df.groupby("city", as_index=False).tail(1)
    latest_rows = latest_rows.sort_values("value", ascending=False)

    latest = [
        {
            "city": row["city"],
            "date": row["date"].strftime("%Y-%m-%d"),
            "value": round(float(row["value"]), 2)
        }
        for _, row in latest_rows.iterrows()
    ]

    return {
        "parameter": parameter,
        "latest": latest
    }