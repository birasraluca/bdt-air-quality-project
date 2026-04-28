import os
import requests
import pandas as pd
from dotenv import load_dotenv


BASE_URL = "https://api.openaq.org/v3/parameters/2/latest"


def load_api_key():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    env_path = os.path.join(project_root, ".env")
    load_dotenv(env_path)

    api_key = os.getenv("OPENAQ_API_KEY")

    if not api_key:
        raise ValueError("OPENAQ_API_KEY is missing. Add it to your .env file.")

    return api_key


def fetch_measurements(limit=1000):
    api_key = load_api_key()

    headers = {
        "X-API-Key": api_key
    }

    params = {
        "limit": limit,
        "page": 1
    }

    response = requests.get(BASE_URL, headers=headers, params=params, timeout=30)
    response.raise_for_status()

    return response.json()


def normalize_results(api_response):
    results = api_response.get("results", [])
    rows = []

    for item in results:
        datetime_info = item.get("datetime", {})
        coordinates = item.get("coordinates", {})

        rows.append({
            "city": item.get("locationsId"),
            "parameter": "pm25",
            "value": item.get("value"),
            "date": datetime_info.get("utc"),
            "unit": "µg/m³",
            "source": "OpenAQ",
            "latitude": coordinates.get("latitude"),
            "longitude": coordinates.get("longitude"),
            "sensor_id": item.get("sensorsId"),
            "location_id": item.get("locationsId")
        })

    return pd.DataFrame(rows)


def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    output_path = os.path.join(project_root, "data", "raw", "openaq_measurements.csv")

    print("Fetching OpenAQ measurements...")

    api_response = fetch_measurements(limit=1000)
    df = normalize_results(api_response)

    if df.empty:
        raise ValueError("No data returned from OpenAQ API.")

    df.to_csv(output_path, index=False)

    print("OpenAQ data fetched successfully.")
    print(f"Rows: {len(df)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()