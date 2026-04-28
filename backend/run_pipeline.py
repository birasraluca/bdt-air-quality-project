from ingestion.fetch_openaq_data import main as fetch_openaq_data
from processing.clean_air_quality_data_spark import main as run_spark_processing


def main():
    print("Starting real OpenAQ air quality data pipeline...\n")

    fetch_openaq_data()
    print("\nOpenAQ ingestion completed.\n")

    run_spark_processing()
    print("\nSpark processing completed.\n")

    print("Pipeline finished successfully.")


if __name__ == "__main__":
    main()