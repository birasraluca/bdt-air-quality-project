from analytics.data_service import load_dataset


def get_project_summary():
    try:
        df = load_dataset()

        summary = {
            "records": int(len(df)),
            "cities": int(df["city"].nunique()),
            "pollutants": df["parameter"].unique().tolist(),
            "date_range": {
                "min": df["date"].min(),
                "max": df["date"].max()
            }
        }

        return summary

    except Exception as e:
        return {
            "error": str(e)
        }