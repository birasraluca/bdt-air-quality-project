import pandas as pd
from app.utils import get_dataset_path


def load_dataset():
    dataset_path = get_dataset_path()
    return pd.read_csv(dataset_path)


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


def get_pollution_trend(city: str, parameter: str):
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

    first_row = filtered_df.iloc[0]
    last_row = filtered_df.iloc[-1]

    first_value = float(first_row["value"])
    latest_value = float(last_row["value"])

    absolute_change = latest_value - first_value

    if first_value != 0:
        percentage_change = (absolute_change / first_value) * 100
    else:
        percentage_change = None

    if absolute_change > 0:
        direction = "increasing"
    elif absolute_change < 0:
        direction = "decreasing"
    else:
        direction = "stable"

    return {
        "city": city,
        "parameter": parameter,
        "from_date": first_row["date"].strftime("%Y-%m-%d"),
        "to_date": last_row["date"].strftime("%Y-%m-%d"),
        "first_value": round(first_value, 2),
        "latest_value": round(latest_value, 2),
        "absolute_change": round(absolute_change, 2),
        "percentage_change": round(percentage_change, 2) if percentage_change is not None else None,
        "direction": direction
    }