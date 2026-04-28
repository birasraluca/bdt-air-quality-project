from ingestion.load_sample_data import main as run_ingestion
from processing.clean_air_quality_data_spark import main as run_spark_processing


def main():
    print("Starting air quality data pipeline...\n")

    run_ingestion()
    print("\nIngestion completed.\n")

    run_spark_processing()
    print("\nProcessing completed.\n")

    print("Pipeline finished successfully.")


if __name__ == "__main__":
    main()