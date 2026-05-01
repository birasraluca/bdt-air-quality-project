import pandas as pd
from analytics.data_service import load_dataset


def get_project_summary():
    try:
        df = load_dataset()

        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["value"] = pd.to_numeric(df["value"], errors="coerce")

        df = df.dropna(subset=["date", "value"])

        summary = {
            "total_records": int(len(df)),
            "records": int(len(df)),
            "cities": int(df["city"].nunique()),
            "parameters": int(df["parameter"].nunique()),
            "pollutants": sorted(df["parameter"].dropna().unique().tolist()),
            "date_range": {
                "min": df["date"].min().strftime("%Y-%m-%d"),
                "max": df["date"].max().strftime("%Y-%m-%d"),
            },
            "value_statistics": {
                "min": round(float(df["value"].min()), 2),
                "max": round(float(df["value"].max()), 2),
                "mean": round(float(df["value"].mean()), 2),
                "median": round(float(df["value"].median()), 2),
                "std": round(float(df["value"].std()), 2),
            },
            "records_by_parameter": (
                df.groupby("parameter")
                .size()
                .sort_values(ascending=False)
                .to_dict()
            ),
            "records_by_city": (
                df.groupby("city")
                .size()
                .sort_values(ascending=False)
                .to_dict()
            ),
        }

        return summary

    except Exception as e:
        return {
            "error": str(e)
        }