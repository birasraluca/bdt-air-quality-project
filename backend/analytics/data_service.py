import pandas as pd
from app.utils import get_dataset_path


def load_dataset():
    dataset_path = get_dataset_path()

    df = pd.read_csv(dataset_path)

    df["city"] = df["city"].astype(str).str.strip()
    df["parameter"] = df["parameter"].astype(str).str.lower().str.strip()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df.dropna(subset=["city", "parameter", "value", "date"])

    return df


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

    filtered_df = filtered_df.sort_values("date")

    data = [
        {
            "date": row["date"].strftime("%Y-%m-%d"),
            "value": round(float(row["value"]), 2)
        }
        for _, row in filtered_df.iterrows()
    ]

    return {
        "city": city,
        "parameter": parameter,
        "records": int(len(data)),
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
        "change": round(absolute_change, 2),
        "percentage_change": round(percentage_change, 2) if percentage_change is not None else None,
        "direction": direction,
        "trend_direction": direction
    }


def get_descriptive_statistics(parameter: str = None):
    df = load_dataset()

    if parameter:
        df = df[df["parameter"].str.lower() == parameter.lower()].copy()

        if df.empty:
            return {
                "error": f"No data found for parameter='{parameter}'"
            }

    grouped_df = (
        df.groupby(["city", "parameter"])["value"]
        .agg(["count", "min", "max", "mean", "median", "std"])
        .reset_index()
        .sort_values(["parameter", "mean"], ascending=[True, False])
    )

    stats = []

    for _, row in grouped_df.iterrows():
        stats.append({
            "city": row["city"],
            "parameter": row["parameter"],
            "records": int(row["count"]),
            "min": round(float(row["min"]), 2),
            "max": round(float(row["max"]), 2),
            "mean": round(float(row["mean"]), 2),
            "median": round(float(row["median"]), 2),
            "std": round(float(row["std"]), 2) if pd.notna(row["std"]) else 0,
        })

    return {
        "parameter": parameter if parameter else "all",
        "statistics": stats
    }


def get_city_profile(city: str):
    df = load_dataset()

    filtered_df = df[df["city"].str.lower() == city.lower()].copy()

    if filtered_df.empty:
        return {
            "error": f"No data found for city='{city}'"
        }

    parameter_stats = (
        filtered_df.groupby("parameter")["value"]
        .agg(["count", "min", "max", "mean", "median", "std"])
        .reset_index()
    )

    pollutants = []

    for _, row in parameter_stats.iterrows():
        pollutants.append({
            "parameter": row["parameter"],
            "records": int(row["count"]),
            "min": round(float(row["min"]), 2),
            "max": round(float(row["max"]), 2),
            "mean": round(float(row["mean"]), 2),
            "median": round(float(row["median"]), 2),
            "std": round(float(row["std"]), 2) if pd.notna(row["std"]) else 0,
        })

    return {
        "city": city,
        "total_records": int(len(filtered_df)),
        "date_range": {
            "min": filtered_df["date"].min().strftime("%Y-%m-%d"),
            "max": filtered_df["date"].max().strftime("%Y-%m-%d"),
        },
        "pollutants": pollutants
    }


def get_monthly_average(city: str = None, parameter: str = None):
    df = load_dataset()

    if city:
        df = df[df["city"].str.lower() == city.lower()].copy()

    if parameter:
        df = df[df["parameter"].str.lower() == parameter.lower()].copy()

    if df.empty:
        return {
            "error": "No data found for the provided filters"
        }

    df["month"] = df["date"].dt.to_period("M").astype(str)

    grouped_df = (
        df.groupby(["month", "city", "parameter"], as_index=False)["value"]
        .mean()
        .sort_values(["month", "city", "parameter"])
    )

    data = [
        {
            "month": row["month"],
            "city": row["city"],
            "parameter": row["parameter"],
            "avg_value": round(float(row["value"]), 2)
        }
        for _, row in grouped_df.iterrows()
    ]

    return {
        "city": city if city else "all",
        "parameter": parameter if parameter else "all",
        "data": data
    }