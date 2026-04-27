import os
import shutil


def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    source_path = os.path.join(project_root, "data", "raw", "raw_air_quality.csv")
    destination_path = os.path.join(project_root, "data", "raw", "ingested_air_quality.csv")

    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source file not found: {source_path}")

    shutil.copyfile(source_path, destination_path)

    print("Raw dataset ingested successfully.")
    print(f"Source: {source_path}")
    print(f"Destination: {destination_path}")


if __name__ == "__main__":
    main()