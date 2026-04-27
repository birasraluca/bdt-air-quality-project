import os
import pandas as pd


def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    input_path = os.path.join(project_root, "data", "raw", "ingested_air_quality.csv")
    output_path = os.path.join(project_root, "data", "processed", "sample_air_quality.csv")

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_csv(input_path)

    # Keep only relevant columns
    df = df[["city", "parameter", "value", "date"]].copy()

    # Drop missing values
    df = df.dropna()

    # Standardize text columns
    df["city"] = df["city"].astype(str).str.strip()
    df["parameter"] = df["parameter"].astype(str).str.strip().str.lower()

    # Ensure correct types
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop rows that became invalid after conversion
    df = df.dropna(subset=["value", "date"])

    # Format date back to string for API use
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    # Sort cleanly
    df = df.sort_values(by=["city", "parameter", "date"]).reset_index(drop=True)

    # Save processed file
    df.to_csv(output_path, index=False)

    print("Processed dataset created successfully.")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"Rows: {len(df)}")


if __name__ == "__main__":
    main()