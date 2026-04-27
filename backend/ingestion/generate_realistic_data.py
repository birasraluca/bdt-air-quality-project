import os
import pandas as pd
import numpy as np


def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    output_path = os.path.join(project_root, "data", "raw", "raw_air_quality_real.csv")

    cities = ["Timisoara", "Cluj", "Bucharest", "Iasi", "Brasov"]
    parameters = ["pm25", "pm10", "no2"]

    dates = pd.date_range(start="2024-01-01", end="2024-02-29")  # ~60 days

    rows = []

    for city in cities:
        for parameter in parameters:
            base = np.random.uniform(10, 40)

            for date in dates:
                noise = np.random.normal(0, 2)
                value = max(0, base + noise)

                rows.append({
                    "city": city,
                    "parameter": parameter,
                    "value": round(value, 2),
                    "date": date.strftime("%Y-%m-%d"),
                    "unit": "µg/m³",
                    "source": "simulated"
                })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)

    print("Generated realistic dataset!")
    print(f"Rows: {len(df)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()