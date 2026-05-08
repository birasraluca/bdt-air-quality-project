import os
import math
import random
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta


BASE_URL = "https://api.openaq.org/v3/locations"

PARAMETERS = {
    2: "pm25",
    1: "pm10",
    5: "no2"
}

ROMANIA_BBOX = "20.0,43.5,30.0,48.5"

START_DATE = datetime(2024, 1, 1)
DAYS_TO_GENERATE = 854

# Fixed seed for reproducibility.
# This means the generated dataset is stable across runs.
random.seed(42)


CITY_BASE_MULTIPLIERS = {
    "Bucharest": 1.25,
    "Timisoara": 1.00,
    "Cluj-Napoca": 1.05,
    "Brasov": 0.90,
    "Craiova": 1.10,
    "Iasi": 1.08,
    "Targu Mures": 0.95,
    "Voluntari": 1.20,
}


POLLUTANT_BASE_VALUES = {
    "pm25": 14,
    "pm10": 28,
    "no2": 22,
}


POLLUTANT_NOISE_LEVELS = {
    "pm25": 3.0,
    "pm10": 5.0,
    "no2": 4.0,
}


def load_api_key():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    env_path = os.path.join(project_root, ".env")
    load_dotenv(env_path)

    api_key = os.getenv("OPENAQ_API_KEY")

    if not api_key:
        raise ValueError("OPENAQ_API_KEY is missing. Add it to your .env file.")

    return api_key


def fetch_locations(parameter_id, limit=1000):
    api_key = load_api_key()

    headers = {
        "X-API-Key": api_key
    }

    params = {
        "parameters_id": parameter_id,
        "bbox": ROMANIA_BBOX,
        "limit": limit,
        "page": 1
    }

    response = requests.get(BASE_URL, headers=headers, params=params, timeout=30)
    response.raise_for_status()

    return response.json()


def infer_city(location_name):
    lower_name = location_name.lower()

    if "bucharest" in lower_name or "bucuresti" in lower_name:
        return "Bucharest"
    if "timisoara" in lower_name or "timișoara" in lower_name:
        return "Timisoara"
    if "cluj" in lower_name:
        return "Cluj-Napoca"
    if "brasov" in lower_name:
        return "Brasov"
    if "craiova" in lower_name:
        return "Craiova"
    if "iasi" in lower_name:
        return "Iasi"
    if "targu-mures" in lower_name or "targu mures" in lower_name:
        return "Targu Mures"
    if "voluntari" in lower_name:
        return "Voluntari"

    return None


def is_allowed_location(location_name):
    allowed_city_keywords = [
        "Bucharest", "Bucuresti", "BUCURESTI",
        "Timisoara", "Timișoara",
        "Cluj", "Cluj Napoca",
        "Brasov",
        "Craiova",
        "Iasi",
        "Targu-Mures",
        "Targu Mures",
        "Voluntari"
    ]

    return any(keyword.lower() in location_name.lower() for keyword in allowed_city_keywords)


def generate_pollution_value(city, parameter_name, day_index, current_date):
    base = POLLUTANT_BASE_VALUES.get(parameter_name, 10)
    city_multiplier = CITY_BASE_MULTIPLIERS.get(city, 1.0)
    noise_level = POLLUTANT_NOISE_LEVELS.get(parameter_name, 3.0)

    # Seasonal effect:
    # Particulate matter is often higher in colder months due to heating and stagnant air.
    # The cosine function gives higher values around winter and lower values around summer.
    yearly_cycle = math.cos((2 * math.pi * day_index) / 365)

    if parameter_name in ["pm25", "pm10"]:
        seasonal_effect = yearly_cycle * 5.0
    elif parameter_name == "no2":
        seasonal_effect = yearly_cycle * 3.0
    else:
        seasonal_effect = yearly_cycle * 2.0

    # Small long-term trend, useful for trend and prediction demos.
    trend = day_index * 0.015

    # Weekend effect:
    # NO2 can be slightly lower during weekends due to reduced traffic.
    weekend_effect = 0
    if current_date.weekday() >= 5:
        if parameter_name == "no2":
            weekend_effect = -2.0
        else:
            weekend_effect = -0.8

    # Random daily variation.
    noise = random.uniform(-noise_level, noise_level)

    # Occasional pollution spike.
    # This simulates events such as traffic peaks, local heating, dust, or stagnant weather.
    spike = 0
    if random.random() < 0.04:
        spike = random.uniform(6, 16)

    value = (base * city_multiplier) + seasonal_effect + trend + weekend_effect + noise + spike

    return max(0, round(value, 2))


def normalize_results(api_response, parameter_name):
    results = api_response.get("results", [])
    rows = []

    for item in results:
        location_id = item.get("id")
        location_name = item.get("name") or f"Location {location_id}"

        if not is_allowed_location(location_name):
            continue

        city = infer_city(location_name)

        if not city:
            continue

        coordinates = item.get("coordinates", {})
        latitude = coordinates.get("latitude")
        longitude = coordinates.get("longitude")

        for day_index in range(DAYS_TO_GENERATE):
            current_date = START_DATE + timedelta(days=day_index)

            value = generate_pollution_value(
                city=city,
                parameter_name=parameter_name,
                day_index=day_index,
                current_date=current_date
            )

            rows.append({
                "city": city,
                "parameter": parameter_name,
                "value": value,
                "date": current_date.strftime("%Y-%m-%d"),
                "unit": "µg/m³",
                "source": "OpenAQ + simulated daily time series",
                "latitude": latitude,
                "longitude": longitude,
                "location_id": location_id,
                "original_location_name": location_name
            })

    return pd.DataFrame(rows)


def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    output_path = os.path.join(project_root, "data", "raw", "openaq_measurements.csv")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    all_frames = []

    for parameter_id, parameter_name in PARAMETERS.items():
        print(f"Fetching OpenAQ locations for {parameter_name}...")

        api_response = fetch_locations(parameter_id=parameter_id, limit=1000)
        df = normalize_results(api_response, parameter_name)

        print(f"{parameter_name}: {len(df)} rows after filtering and generation")

        if not df.empty:
            all_frames.append(df)

    if not all_frames:
        raise ValueError("No data returned after filtering OpenAQ results.")

    final_df = pd.concat(all_frames, ignore_index=True)

    final_df.to_csv(output_path, index=False)

    print("OpenAQ-based air quality dataset generated successfully.")
    print(f"Generated days per location: {DAYS_TO_GENERATE}")
    print(f"Total rows: {len(final_df)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()