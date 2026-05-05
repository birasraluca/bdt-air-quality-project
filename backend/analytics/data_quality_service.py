import pandas as pd
from analytics.data_service import load_dataset


EXPECTED_PARAMETERS = ["pm25", "pm10"]


def get_data_quality_report():
    df = load_dataset()

    total_rows = int(len(df))

    missing_values = {
        column: int(df[column].isna().sum())
        for column in df.columns
    }

    duplicate_rows = int(
        df.duplicated(subset=["city", "parameter", "date"]).sum()
    )

    invalid_values = int(
        ((df["value"] < 0) | (df["value"] > 1000)).sum()
    )

    date_min = df["date"].min()
    date_max = df["date"].max()

    records_by_city = (
        df.groupby("city")
        .size()
        .sort_values(ascending=False)
        .to_dict()
    )

    records_by_parameter = (
        df.groupby("parameter")
        .size()
        .sort_values(ascending=False)
        .to_dict()
    )

    available_parameters = sorted(df["parameter"].dropna().unique().tolist())
    missing_expected_parameters = [
        parameter
        for parameter in EXPECTED_PARAMETERS
        if parameter not in available_parameters
    ]

    city_parameter_coverage = []

    grouped = (
        df.groupby(["city", "parameter"])
        .agg(
            records=("value", "count"),
            first_date=("date", "min"),
            last_date=("date", "max"),
            min_value=("value", "min"),
            max_value=("value", "max"),
            avg_value=("value", "mean"),
        )
        .reset_index()
        .sort_values(["city", "parameter"])
    )

    for _, row in grouped.iterrows():
        city_parameter_coverage.append({
            "city": row["city"],
            "parameter": row["parameter"],
            "records": int(row["records"]),
            "first_date": row["first_date"].strftime("%Y-%m-%d"),
            "last_date": row["last_date"].strftime("%Y-%m-%d"),
            "min_value": round(float(row["min_value"]), 2),
            "max_value": round(float(row["max_value"]), 2),
            "avg_value": round(float(row["avg_value"]), 2),
        })

    return {
        "total_rows": total_rows,
        "date_range": {
            "min": date_min.strftime("%Y-%m-%d"),
            "max": date_max.strftime("%Y-%m-%d"),
        },
        "available_parameters": available_parameters,
        "missing_expected_parameters": missing_expected_parameters,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "invalid_values": invalid_values,
        "records_by_city": records_by_city,
        "records_by_parameter": records_by_parameter,
        "city_parameter_coverage": city_parameter_coverage,
        "quality_notes": [
            "Rows with missing required values are removed during PySpark processing.",
            "Pollution values are cast to numeric format during cleaning.",
            "Negative values and extremely high values above 1000 are treated as invalid.",
            "Duplicate records are checked using city, parameter, and date.",
        ]
    }